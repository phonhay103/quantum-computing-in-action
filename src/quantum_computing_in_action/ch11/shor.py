"""Chapter 11 — Shor's algorithm: factoring by finding an order with the QFT.

The classical half of the chapter turned factoring into **order finding** — the
period ``r`` of ``a^x mod N`` — and left the period search as the expensive step.
This module supplies it quantumly, and the recipe is short:

1. **Preprocess.** Pick ``a`` coprime to ``N``. If ``gcd(a, N) > 1`` you already
   have a factor. Otherwise find the period of ``a``.
2. **Order finding.**
   * two registers: a **counting** register of ``m`` qubits and a **work** register
     wide enough to hold ``N``;
   * ``H`` on the counting register, and set the work register to ``|1>``;
   * apply the controlled modular multiplications ``|y> -> |a^(2^j) * y mod N>`` —
     this writes the periodic function ``a^x mod N`` into a superposition;
   * apply the **inverse QFT** to the counting register; its periodic input
     collapses to peaks at multiples of ``2^m / r``.
3. **Read the period.** Measure the counting register and run the number through a
   **continued-fraction** expansion; the denominator of the best convergent is the
   period ``r``.
4. **Extract.** ``gcd(a^(r/2) +- 1, N)`` gives the factors, with a retry if ``r``
   is odd or ``a^(r/2) = -1``.

One detail worth stating because it is easy to get wrong: the modular
multiplication is a **permutation** of basis states — it must be, to be reversible
— and units that leave the work register alone for ``y >= N`` are how the same
unitary handles every input.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate, UnitaryGate
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_counts
from quantum_computing_in_action.ch07.circuits import probabilities
from quantum_computing_in_action.ch11.classical import factor_from_order, semiclassic_factor


def modular_multiplier(a: int, n: int, width: int) -> np.ndarray:
    """Return the permutation ``|y> -> |a*y mod n>`` on ``width`` qubits.

    Every ``y`` up to the register size is mapped: ``y < n`` goes to ``a*y mod n``
    and everything else is left in place. That keeps the map a permutation (hence
    unitary and reversible) even though the register is wider than ``n``.

    Raises:
        ValueError: if ``a`` and ``n`` are not coprime, which would make the map
            many-to-one instead of a permutation.
    """
    if math.gcd(a, n) != 1:
        raise ValueError("a and n must be coprime")
    size = 1 << width
    matrix = np.zeros((size, size), dtype=complex)
    for y in range(size):
        target = (a * y) % n if y < n else y
        matrix[target, y] = 1.0
    return matrix


def counting_width(n: int) -> int:
    """Return the counting-register width ``2 * ceil(log2(n))`` (``2^m >= n^2``)."""
    if n < 2:
        raise ValueError("n must be at least 2")
    return 2 * n.bit_length()


def work_width(n: int) -> int:
    """Return the work-register width ``ceil(log2(n))`` — enough to hold ``n - 1``."""
    if n < 2:
        raise ValueError("n must be at least 2")
    return n.bit_length()


def order_finding_circuit(
    a: int, n: int, m: int | None = None, width: int | None = None, *, measure: bool = True
) -> QuantumCircuit:
    """Return the order-finding circuit for ``a`` modulo ``n``.

    The counting register is ``q0 .. q(m-1)`` and the work register follows it.
    """
    m = counting_width(n) if m is None else m
    width = work_width(n) if width is None else width
    circuit = QuantumCircuit(m + width, m)
    circuit.x(m)  # the work register starts at |1>
    circuit.h(range(m))
    for j in range(m):
        power = pow(a, 1 << j, n)
        if power == 1:
            continue  # a^(2^j) = 1: this multiplier is the identity, so leave it out
        controlled = UnitaryGate(modular_multiplier(power, n, width)).control(1, annotated=False)
        circuit.append(controlled, [j, *range(m, m + width)])
    circuit.append(QFTGate(m).inverse(), range(m))
    if measure:
        for j in range(m):
            circuit.measure(j, j)
    return circuit


def order_distribution(a: int, n: int, m: int | None = None, width: int | None = None) -> dict[int, float]:
    """Return the exact distribution of the counting register after the inverse QFT.

    The keys are the register read as an integer (``q0`` the least-significant bit).
    A period ``r`` shows up as peaks at multiples of ``2^m / r``.
    """
    m = counting_width(n) if m is None else m
    width = work_width(n) if width is None else width
    state = Statevector.from_instruction(order_finding_circuit(a, n, m, width, measure=False))
    distribution: dict[int, float] = {}
    for label, probability in probabilities(state).items():
        outcome = int(label[:m][::-1], 2)  # the counting register, q0 first
        distribution[outcome] = distribution.get(outcome, 0.0) + probability
    return distribution


def convergents(numerator: int, denominator: int) -> list[tuple[int, int]]:
    """Return the continued-fraction convergents ``(p, q)`` of ``numerator/denominator``.

    The last convergent's denominator, kept below ``N``, is the order Shor looks
    for. A plain ``Fraction(...).limit_denominator`` would work too; writing the
    expansion out shows *why* the measurement points at the period.
    """
    if denominator == 0:
        raise ValueError("denominator must not be zero")
    terms: list[int] = []
    a, b = numerator, denominator
    while b:
        quotient = a // b
        terms.append(quotient)
        a, b = b, a - quotient * b
    if not terms:
        return []

    result: list[tuple[int, int]] = []
    p_prev, p = 1, terms[0]
    q_prev, q = 0, 1
    result.append((p, q))
    for term in terms[1:]:
        p_prev, p = p, term * p + p_prev
        q_prev, q = q, term * q + q_prev
        result.append((p, q))
    return result


def period_from_outcome(outcome: int, m: int, n: int, a: int) -> int | None:
    """Turn a measured counting-register value into the period, or ``None``.

    The measurement approximates ``k/r`` as ``outcome / 2^m``; the continued
    fraction of that number has ``r`` as its denominator, and we check it against
    ``a^r = 1 (mod n)`` so a bad measurement is rejected rather than believed.
    """
    for _, denominator in convergents(outcome, 1 << m):
        if 0 < denominator < n and pow(a, denominator, n) == 1:
            return denominator
    return None


def quantum_order(a: int, n: int, m: int | None = None, width: int | None = None) -> int:
    """Find the period of ``a`` modulo ``n`` with the QFT, most likely outcome first.

    Raises:
        ValueError: if no outcome yields a verifiable period.
    """
    distribution = order_distribution(a, n, m, width)
    m = counting_width(n) if m is None else m
    for outcome in sorted(distribution, key=lambda key: -distribution[key]):
        period = period_from_outcome(outcome, m, n, a)
        if period is not None:
            return period
    raise ValueError(f"no period found for a={a}, n={n}")


def shor(n: int, *, m: int | None = None, width: int | None = None) -> tuple[int, int]:
    """Factor ``n`` with Shor's algorithm; returns ``(smaller, larger)``.

    ``a`` is tried from 2 upwards so the result is deterministic; the guards are
    the same ones the semiclassic sample uses.

    Raises:
        ValueError: if ``n`` is less than 4, or no factor is found.
    """
    if n < 4:
        raise ValueError("n must be at least 4")
    if n % 2 == 0:
        return 2, n // 2
    for a in range(2, n):
        common = math.gcd(a, n)
        if common > 1:
            return min(common, n // common), max(common, n // common)
        period = quantum_order(a, n, m, width)
        factor = factor_from_order(a, n, period)
        if factor is not None:
            other = n // factor
            return min(factor, other), max(factor, other)
    raise ValueError(f"Shor's algorithm failed to factor {n}")


def draw(output: str | Path = "build/ch11-order-peaks.png") -> Path:
    """Render the counting-register peaks for ``2^x mod 15``."""
    distribution = {
        str(outcome): probability for outcome, probability in order_distribution(2, 15).items() if probability > 1e-9
    }
    return render_counts(
        distribution,
        output,
        title="Inverse QFT of the periodic register: four peaks, 64 apart",
        xlabel="measured counting register",
        ylabel="probability",
    )


def draw_circuit(output: str | Path = "build/ch11-order-circuit.png") -> Path:
    """Render a compact order-finding circuit for ``2^x mod 15``.

    The picture uses a 4-qubit counting register (``2^4 = 16``), which is enough
    for ``N = 15`` because its period divides 16. The general rule in
    :func:`counting_width` asks for ``2*m`` qubits so that ``2^m >= n^2``; for a
    small example the extra wires only make the drawing harder to read.
    """
    return render_circuit(order_finding_circuit(2, 15, m=4, width=4), output)


def _peak_table(a: int, n: int) -> Table:
    distribution = order_distribution(a, n)
    period = quantum_order(a, n)
    peaks = sorted(
        ((outcome, probability) for outcome, probability in distribution.items() if probability > 1e-9),
        key=lambda item: item[0],
    )
    table = Table(title=f"Order finding for a = {a}, n = {n}: peaks and the period they give", header_style="heading")
    table.add_column("measured", style="bits")
    table.add_column("probability", style="value")
    table.add_column("continued fraction", style="muted")
    table.add_column("period found", style="value")
    for outcome, probability in peaks:
        period_found = period_from_outcome(outcome, counting_width(n), n, a)
        fraction = " -> ".join(f"{p}/{q}" for p, q in convergents(outcome, 1 << counting_width(n))[:3])
        table.add_row(str(outcome), f"{probability:.3f}", fraction, str(period_found) if period_found else "-")
    table.add_row("[muted]period[/muted]", "", "", f"[value]{period}[/value]")
    return table


def main() -> None:
    explain(
        "Chapter 11 — Shor's algorithm",
        """
Shor's algorithm is the classical reduction of the previous module plus one
genuinely quantum step: finding the **period** of `a^x mod N`. The classical
period search is as hard as factoring; the quantum one is not.

Everything hangs on two registers.

* The **counting** register (`m = 2*ceil(log2 N)` qubits) goes into a uniform
  superposition with Hadamards.
* The **work** register starts at `|1>`, and controlled multiplications write
  `a^x mod N` into it, one power per counting qubit: `|y> -> |a^(2^j) * y mod N>`.

At that point the counting register holds **every `x` at once**, with the periodic
function `a^x mod N` recorded in the work register. Measuring the work register
would collapse it to one value — useless. So instead the circuit applies the
**inverse QFT** to the counting register. A periodic input is exactly what the
Fourier transform turns into sharp **peaks**: the weight concentrates on the
integers near multiples of `2^m / r`, where `r` is the period.

All that is left is arithmetic. Read a peak as `k/r = outcome / 2^m`, run it
through a **continued-fraction** expansion, and the denominator of the best
convergent is `r` — provided `k` and `r` are coprime. When they are not, the
convergent gives a *divisor* of `r` and the check `a^r = 1 (mod N)` rejects it, so
Shor simply looks at another peak. The classical guard and `gcd` finish the job:
`gcd(a^(r/2) +- 1, N)` are the two factors.

For `N = 15`, `a = 2`, the period is `4`, and the peaks sit at `0, 64, 128, 192` —
every `2^m / r = 64` apart. The continued fraction of `64/256` is `1/4`, so
`r = 4`, and `gcd(2^2 - 1, 15) = 3`. Factors: **3 and 5**.
""",
    )

    steps(
        "Chapter 11 — the quantum period search",
        [
            ("Hadamard the counting register", "every exponent x at once"),
            ("Controlled modular multiply", "the work register records a^x mod N"),
            ("Inverse QFT", "the period collapses to peaks at multiples of 2^m / r"),
            ("Measure and continue fractions", "the denominator of the convergents is r"),
            ("gcd", "a^(r/2) +- 1 against N gives the factors"),
        ],
    )

    console.rule("Order finding for 2^x mod 15")
    console.print(_peak_table(2, 15))
    console.print(
        "[muted]The four peaks are equally likely and evenly spaced by 2^m/r = 256/4 = 64. The ones "
        "where the numerator is coprime to r (64 and 192) give r = 4 directly; the others give a "
        "divisor that fails the a^r = 1 check, so Shor tries the next peak.[/muted]"
    )

    console.rule("Factoring small numbers")
    for n in (15, 21):
        smaller, larger = shor(n)
        check = "" if smaller * larger == n else "  <- check failed"
        console.print(f"  [bits]Shor[/bits] {n:>3} = {smaller} x {larger}{check}")
    console.print(
        "  [muted]the same answers, semiclassically: "
        + ", ".join(f"{n} -> {semiclassic_factor(n)}" for n in (15, 21, 33))
        + "[/muted]"
    )
    console.print(
        "[muted]Each extra bit of N widens both registers, so the simulator's cost grows quickly: "
        "15 is instant, 21 takes a few seconds. That is a limit of *this simulation*, not of the "
        "algorithm — Shor is polynomial in the number of bits.[/muted]"
    )

    peaks_path = draw()
    circuit_path = draw_circuit()
    console.print("Saved diagrams:")
    for path in (peaks_path, circuit_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
