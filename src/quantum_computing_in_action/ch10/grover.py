"""Chapter 10 — Grover's algorithm: turning a sign into an answer.

The oracle of :mod:`...ch10.oracle` marks the answer with a sign; nothing is
measurable yet. Grover's **diffusion** operator turns that sign into probability.
It is a reflection about the *average amplitude*:

    D = H^n ( 2|0><0| - I ) H^n  =  2|s><s| - I

where ``|s>`` is the uniform superposition. Applied after the oracle, it inverts
every amplitude about the mean. The marked state, which the oracle dragged *below*
the mean by flipping its sign, is the one state that flips back up **above** it —
and the others sink slightly. Repeat the pair and the marked amplitude grows a
little each round, until after about ``(pi/4)*sqrt(N)`` rounds it is near 1.

The count is what matters:

* the classical scan needs about ``N/2`` lookups;
* Grover needs about ``(pi/4)*sqrt(N)`` — a **quadratic** speed-up, and it is
  provably the best a quantum computer can do for an unstructured list.

Run too many rounds and the probability comes back down; the rotation overshoots.
That is why the iteration count is part of the algorithm, not a detail.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain
from quantum_computing_in_action._diagrams import render_circuit, render_counts
from quantum_computing_in_action.ch07.circuits import sample_counts
from quantum_computing_in_action.ch10.oracle import index_set, marked_label, phase_oracle


def optimal_iterations(n_qubits: int) -> int:
    """Return the best number of Grover rounds: ``floor((pi/4) * sqrt(N))``, at least 1."""
    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1")
    n = 1 << n_qubits
    return max(1, int(np.floor(np.pi / 4 * np.sqrt(n))))


def diffusion(n: int) -> QuantumCircuit:
    """Return the diffusion operator ``2|s><s| - I`` on ``n`` qubits.

    ``H^n`` maps ``|s>`` to ``|0...0>``, so the reflection becomes ``X^n`` around a
    phase flip of ``|1...1>`` — a multi-controlled ``Z`` — and back. That
    construction is the reflection times ``-1``; the circuit's global phase is set
    to ``pi`` so the operator is exactly ``2|s><s| - I`` and the amplitudes it
    prints match the "reflect about the mean" arithmetic.

    Raises:
        ValueError: if there are fewer than two qubits (there would be no control).
    """
    if n < 2:
        raise ValueError("diffusion needs at least 2 qubits")
    circuit = QuantumCircuit(n)
    circuit.h(range(n))
    circuit.x(range(n))
    circuit.h(n - 1)
    circuit.mcx(list(range(n - 1)), n - 1)
    circuit.h(n - 1)
    circuit.x(range(n))
    circuit.h(range(n))
    circuit.global_phase = np.pi
    return circuit


def grover_circuit(
    n: int,
    marked: int | Iterable[int],
    iterations: int | None = None,
    *,
    measure: bool = True,
) -> QuantumCircuit:
    """Return the Grover circuit for ``n`` qubits with ``marked`` state(s).

    Args:
        n: the number of qubits.
        marked: the marked basis state index, or several.
        iterations: Grover rounds; ``None`` uses :func:`optimal_iterations`.
        measure: append a measurement on every qubit.

    Raises:
        ValueError: for an invalid ``n`` or a negative iteration count.
    """
    index_set(marked, n)  # validate up front
    if iterations is None:
        rounds = optimal_iterations(n)
    elif iterations < 0:
        raise ValueError("iterations must not be negative")
    else:
        rounds = iterations

    oracle = phase_oracle(n, marked)
    diffusion_operator = diffusion(n)
    circuit = QuantumCircuit(n, n)
    circuit.h(range(n))
    for _ in range(rounds):
        circuit.compose(oracle, inplace=True)
        circuit.compose(diffusion_operator, inplace=True)
    if measure:
        for qubit in range(n):
            circuit.measure(qubit, qubit)
    return circuit


def state_after(n: int, marked: int | Iterable[int], iterations: int) -> Statevector:
    """Return the state after ``iterations`` Grover rounds."""
    return Statevector.from_instruction(grover_circuit(n, marked, iterations, measure=False))


def success_probability(n: int, marked: int | Iterable[int], iterations: int | None = None) -> float:
    """Return the probability of measuring any marked state after ``iterations`` rounds."""
    indices = index_set(marked, n)
    rounds = optimal_iterations(n) if iterations is None else iterations
    state = state_after(n, marked, rounds)
    return float(sum(abs(state.data[index]) ** 2 for index in indices))


def success_curve(n: int, marked: int | Iterable[int], upto: int | None = None) -> dict[int, float]:
    """Return ``{rounds: probability}`` for 0 rounds up to ``upto`` (default optimal + 3)."""
    limit = optimal_iterations(n) + 3 if upto is None else upto
    return {rounds: success_probability(n, marked, rounds) for rounds in range(limit + 1)}


def measured_counts(
    n: int,
    marked: int | Iterable[int],
    shots: int = 2000,
    *,
    seed: int | None = None,
    iterations: int | None = None,
) -> dict[str, int]:
    """Measure the Grover circuit ``shots`` times, keyed in the book's bit order."""
    rounds = optimal_iterations(n) if iterations is None else iterations
    state = state_after(n, marked, rounds)
    return sample_counts(state, shots, seed=seed)


def _curve_as_labels(curve: dict[int, float]) -> dict[str, float]:
    return {str(rounds): probability for rounds, probability in curve.items()}


def draw(output: str | Path = "build/ch10-grover-circuit.png") -> Path:
    """Render a small Grover circuit (3 qubits, 2 rounds) and save it to ``output``."""
    return render_circuit(grover_circuit(3, 5), output)


def _summary_table(n: int, marked: int) -> Table:
    curve = success_curve(n, marked)
    best = max(curve, key=lambda rounds: curve[rounds])
    table = Table(
        title=f"Grover on {n} qubits (N = {1 << n}, marked {marked_label(n, marked)})", header_style="heading"
    )
    table.add_column("rounds", style="bits")
    table.add_column("P(marked)", style="value")
    table.add_column("", style="muted")
    for rounds, probability in curve.items():
        marker = ""
        if rounds == optimal_iterations(n):
            marker = "chosen by floor((pi/4) sqrt N)"
        if rounds == best:
            marker = marker or "peak"
        table.add_row(str(rounds), f"{probability:.3f}", marker)
    return table


def main() -> None:
    explain(
        "Chapter 10 — Grover's algorithm",
        """
The oracle marks the answer with a sign. That sign is invisible, so Grover adds a
second step that makes it *matter*: the **diffusion** operator, a reflection about
the average amplitude.

    D = H^n ( 2|0><0| - I ) H^n

Here is the whole loop:

1. **Start uniform.** `H` on every qubit: all `N` states with amplitude `1/sqrt(N)`.
2. **Oracle.** Flip the sign of the marked state; it is now *below* the average.
3. **Diffusion.** Reflect every amplitude about the mean. The marked one, dragged
   below, comes back up *above* the mean; the rest sink a little.
4. **Repeat** steps 2-3 about `(pi/4)*sqrt(N)` times.

Each round is a small rotation of the amplitude vector, so the marked probability
follows `sin^2((2k+1)*theta)` with `sin(theta) = 1/sqrt(N)`.

Two facts are worth memorising.

* The speed-up is **quadratic**: `(pi/4)*sqrt(N)` rounds against the classical
  `N/2` lookups. On 64 items that is 6 rounds instead of 32 — and no quantum
  algorithm can do better for an unordered list.
* The iteration count matters. Run too few rounds and the probability is still
  small; run too many and it comes back down, because the rotation overshoots. The
  peak is the algorithm, not an afterthought.
""",
    )

    n = 6
    marked = 7
    console.rule("Grover on 64 items, one marked")
    console.print(_summary_table(n, marked))
    console.print(
        f"  [muted]The peak sits at {optimal_iterations(n)} rounds — "
        f"floor((pi/4) sqrt 64) — where P(marked) = "
        f"{success_probability(n, marked):.3f}. A classical scan would average 32 lookups.[/muted]"
    )

    console.rule("Measured after the optimal number of rounds")
    counts = measured_counts(n, marked, 2000, seed=4)
    top = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:3]
    console.print(
        "  [heading]top outcomes: [/heading]"
        + ", ".join(f"{label}: {count}" for label, count in top)
        + f"  [muted](the answer is {marked_label(n, marked)})[/muted]"
    )

    circuit_path = draw()
    curve_path = render_counts(
        _curve_as_labels(success_curve(n, marked)),
        "build/ch10-grover-curve.png",
        title="Grover on 64 items: probability rises, then overshoots",
        xlabel="Grover rounds",
        ylabel="P(marked)",
    )
    outcomes_path = render_counts(
        counts,
        "build/ch10-grover-outcomes.png",
        title="64 outcomes after 6 rounds: the answer dominates",
        xlabel="measured basis state (q0 .. q5)",
        ylabel="count",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, curve_path, outcomes_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
