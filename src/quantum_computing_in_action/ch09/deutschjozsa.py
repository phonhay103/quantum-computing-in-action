"""Chapter 9 — Deutsch—Jozsa: constant or balanced, in one query for any ``n``.

Deutsch asked the question for a one-bit function. **Deutsch—Jozsa** asks it for an
``n``-bit function ``f: {0,1}^n -> {0,1}`` that is promised to be either
**constant** (the same output on every input) or **balanced** (0 on exactly half
the inputs, 1 on the other half).

Classically this is expensive. To be *certain* which it is you may have to look at
``2^(n-1) + 1`` inputs: one too many to be fooled by a balanced function that keeps
giving the same answer. Quantumly, one query settles it, and the circuit is the
Deutsch circuit with more wires:

    X(ancilla)                    prepare the spare register in |1>
    H on all n+1 qubits           superposition on every register
    oracle U_f                    phase kickback: (-1)^f(x) on each branch
    H on the n input qubits       interfere all the branches at once
    measure the input register    all zeros <=> constant, anything else <=> balanced

This is the same interference as Deutsch, run over ``2^n`` basis states in
parallel: the amplitudes of every balanced function cancel on ``|0...0>``, so that
one outcome is impossible.
"""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts
from quantum_computing_in_action.ch07.circuits import Builder, probabilities, state_after
from quantum_computing_in_action.ch09.oracles import dj_oracle

#: The input widths demonstrated, smallest first.
WIDTHS: tuple[int, ...] = (1, 2, 3)

#: The oracle kinds the chapter demonstrates, in order.
KINDS: tuple[str, ...] = ("constant0", "constant1", "balanced")


def _builder(n: int, kind: str) -> Builder:
    """Return the Deutsch—Jozsa gates up to (not including) the measurement."""
    oracle = dj_oracle(n, kind)

    def build(circuit: QuantumCircuit) -> None:
        circuit.x(n)
        for qubit in range(n + 1):
            circuit.h(qubit)
        circuit.compose(oracle, inplace=True)
        for qubit in range(n):
            circuit.h(qubit)

    return build


def dj_circuit(n: int, kind: str, *, measure: bool = True) -> QuantumCircuit:
    """Return the Deutsch—Jozsa circuit for an ``n``-bit ``kind`` oracle.

    Only the ``n`` input qubits are measured; the ancilla is not.
    """
    circuit = QuantumCircuit(n + 1, n)
    _builder(n, kind)(circuit)
    if measure:
        for qubit in range(n):
            circuit.measure(qubit, qubit)
    return circuit


def dj_outcome(n: int, kind: str) -> dict[str, float]:
    """Return the measurement distribution over the ``n``-bit input register.

    The keys are ``q0 q1 ... q(n-1)`` in the book's order, so the ``n``-bit string
    of all zeros is ``"0" * n``.
    """
    state = state_after(_builder(n, kind), n + 1)
    distribution: dict[str, float] = {}
    for label, probability in probabilities(state).items():
        key = label[:n]  # the input register (the ancilla is never measured)
        distribution[key] = distribution.get(key, 0.0) + probability
    return distribution


def all_zero_probability(n: int, kind: str) -> float:
    """Return the probability of measuring ``0...0`` — 1 for constant, 0 for balanced."""
    return dj_outcome(n, kind).get("0" * n, 0.0)


def is_constant(n: int, kind: str) -> bool:
    """Return whether the algorithm classifies the oracle as constant."""
    return all_zero_probability(n, kind) > 0.5


def classical_queries(n: int) -> int:
    """Return the worst-case number of queries a classical check needs: ``2^(n-1) + 1``."""
    if n < 1:
        raise ValueError("n must be at least 1")
    return (1 << (n - 1)) + 1


def draw(output: str | Path = "build/ch09-dj-circuit.png") -> Path:
    """Render the ``n = 3`` ambiguous-oracle circuit and save it to ``output``."""
    return render_circuit(dj_circuit(3, "balanced"), output)


def _results_table() -> Table:
    table = Table(title="Deutsch—Jozsa: one query, any width", header_style="heading")
    table.add_column("n", style="bits")
    table.add_column("oracle", style="bits")
    table.add_column("P(0...0)", style="value")
    table.add_column("verdict", style="value")
    table.add_column("classical queries", style="muted")
    for n in WIDTHS:
        for kind in KINDS:
            table.add_row(
                str(n),
                kind,
                f"{all_zero_probability(n, kind):.2f}",
                "constant" if is_constant(n, kind) else "balanced",
                str(classical_queries(n)),
            )
    return table


def main() -> None:
    explain(
        "Chapter 9 — the Deutsch—Jozsa algorithm",
        """
Deutsch handled a function of **one** bit. **Deutsch—Jozsa** handles a function of
`n` bits, `f: {0,1}^n -> {0,1}`, with the promise that it is either **constant**
(the same answer on all `2^n` inputs) or **balanced** (0 on exactly half, 1 on the
other half).

The classical cost is the point of comparison. A balanced function can agree with a
constant one for a long time, so to be *sure* you may have to evaluate
`2^(n-1) + 1` inputs — half the space plus one, past the point where a balanced
function could still be hiding. Quantumly, **one** query does it.

The circuit is Deutsch's with more wires. Prepare the ancilla in `|1>`, Hadamard
every qubit, run the oracle once, then Hadamard the input register:

* The oracle writes `(-1)^f(x)` into the **sign** of each of the `2^n` branches.
* If `f` is **constant**, every sign is the same — a global phase, invisible — and
  the final Hadamards return the register to `|0...0>`. That outcome has
  probability 1.
* If `f` is **balanced**, exactly half the signs are `-1`. The branches now cancel
  **pairwise** on `|0...0>`, whose amplitude becomes `(1/2^n) * sum (-1)^f(x) = 0`.
  So `|0...0>` can never be measured.

One outcome decides it: **all zeros means constant; anything else means balanced**.
Adding wires does not add queries, because the oracle runs on all `2^n` inputs at
once — this is *quantum parallelism*, and interference is what turns it into an
answer.
""",
    )

    steps(
        "Chapter 9 — the Deutsch—Jozsa circuit",
        [
            ("X(ancilla)", "the spare register becomes |1>, ready for phase kickback"),
            ("H on all n+1 qubits", "2^n inputs become one superposition"),
            ("oracle", "one evaluation tags every branch with (-1)^f(x)"),
            ("H on the input register", "constant branches add; balanced branches cancel"),
            ("measure the input register", "0...0 means constant; anything else means balanced"),
        ],
    )

    console.rule("One query, any width")
    console.print(_results_table())
    console.print(
        "[muted]P(0...0) is 1.00 for every constant oracle and 0.00 for every balanced one, no "
        "matter how wide the input — while the classical check needs 2^(n-1)+1 queries and grows "
        "exponentially.[/muted]"
    )

    circuit_path = draw()
    outcomes_path = render_grouped_counts(
        [
            ("constant 0", dj_outcome(2, "constant0")),
            ("balanced (parity)", dj_outcome(2, "balanced")),
        ],
        "build/ch09-dj-outcomes.png",
        title="n = 2: a constant oracle returns 00, a balanced one never does",
        xlabel="measured input register (q0 q1)",
        ylabel="probability",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, outcomes_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
