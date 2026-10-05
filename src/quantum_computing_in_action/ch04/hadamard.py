"""Chapter 4 — the Hadamard gate: creating and cancelling superposition."""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.panel import Panel
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import (
    render_bloch,
    render_circuit,
    render_counts,
    render_matrices,
)
from quantum_computing_in_action.ch04 import matrices


def _single_hadamard() -> QuantumCircuit:
    """A one-qubit circuit that applies the Hadamard gate once."""
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    return circuit


def _double_hadamard() -> QuantumCircuit:
    """A one-qubit circuit that applies the Hadamard gate twice.

    Because ``H`` is its own inverse, ``H·H = I``: the second gate undoes the
    first one and the qubit returns to ``|0>``.
    """
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.h(0)
    return circuit


def single_hadamard_circuit() -> QuantumCircuit:
    """The single-``H`` circuit plus a measurement (a 50/50 random bit)."""
    circuit = _single_hadamard()
    circuit.measure(0, 0)
    return circuit


def double_hadamard_circuit() -> QuantumCircuit:
    """The ``H``-then-``H`` circuit plus a measurement (always ``0``)."""
    circuit = _double_hadamard()
    circuit.measure(0, 0)
    return circuit


def _sampled_counts(circuit: QuantumCircuit, shots: int) -> dict[str, int]:
    base = circuit.copy()
    base.remove_final_measurements(inplace=True)
    state = Statevector.from_instruction(base)
    return {str(bit): int(count) for bit, count in state.sample_counts(shots).items()}


def _probabilities(state: Statevector) -> str:
    probs = state.probabilities_dict()
    return f"P(0) = {float(probs.get('0', 0.0)):.2f}, P(1) = {float(probs.get('1', 0.0)):.2f}"


def _format_matrix(matrix) -> str:
    rows = []
    for row in matrix:
        cells = (f"{value.real:+.2f}" if abs(value.imag) < 1e-9 else f"{value:+.2f}" for value in row)
        rows.append("[ " + "  ".join(cells) + " ]")
    return "\n".join(rows)


def random_bit() -> int:
    """Return a single bit obtained by measuring ``H|0>``."""
    counts = _sampled_counts(single_hadamard_circuit(), 1)
    return 1 if counts.get("1", 0) else 0


def repeat_single_hadamard(shots: int = 1000) -> dict[str, int]:
    """Measure ``H|0>`` ``shots`` times; returns a roughly balanced ``{"0": .., "1": ..}``."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    return _sampled_counts(single_hadamard_circuit(), shots)


def repeat_double_hadamard(shots: int = 1000) -> dict[str, int]:
    """Measure ``H·H|0> = |0>`` ``shots`` times; always returns ``{"0": shots}``."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    return _sampled_counts(double_hadamard_circuit(), shots)


def draw(
    output: str | Path = "build/ch04-hadamard-circuit.png",
    *,
    double: bool = False,
) -> Path:
    """Render the single (or double) Hadamard circuit and save it to ``output``."""
    circuit = double_hadamard_circuit() if double else single_hadamard_circuit()
    return render_circuit(circuit, output)


def main() -> None:
    explain(
        "Chapter 4 — The Hadamard gate",
        """
The **Hadamard gate** (`H`) is the gate that *creates* superposition. Applied to
`|0>` it produces an even mix of `|0>` and `|1>`:

`H|0> = (|0> + |1>) / sqrt(2)`

Measuring now gives `0` or `1` with a 50% chance.

The surprising part is what happens when you apply `H` a **second** time. Every
quantum gate is reversible, and `H` is its own inverse:

`H·H = I`

So `H·H|0> = |0>`: the second gate *undoes* the first, the superposition
disappears, and measuring always returns `0` again. The canvas below shows both
the random single-`H` case and the deterministic double-`H` case.

Under the hood, a single qubit is a **state vector** `[alpha, beta]` and every
gate is a **2x2 matrix** that multiplies it. The Pauli-X and Hadamard gates are
therefore

`X = [[0, 1], [1, 0]]        H = 1/sqrt(2) * [[1, 1], [1, -1]]`

and `H·H` is the identity matrix — the matrix way of saying "two Hadamards
cancel".
""",
    )

    initial = Statevector.from_label("0")
    superposed = Statevector.from_instruction(_single_hadamard())
    restored = Statevector.from_instruction(_double_hadamard())

    first = random_bit()
    single = repeat_single_hadamard(1000)
    double = repeat_double_hadamard(1000)
    zeros = single.get("0", 0)
    ones = single.get("1", 0)

    steps(
        "Chapter 4 — step by step",
        [
            ("Prepare a qubit in |0>", _probabilities(initial)),
            ("Apply H once", _probabilities(superposed)),
            ("Measure (single H)", f"random outcome: {first}"),
            ("Apply H a second time", _probabilities(restored)),
            ("Measure (H·H)", f"always 0 — got {double.get('0', 0)}/1000 zeros"),
        ],
    )

    console.rule("Applying the Hadamard gate")
    console.print(f"Single run of H: value = [value]{first}[/value] (random)")
    console.print(f"1000 runs of H: [zero]{zeros}[/zero] times 0 and [one]{ones}[/one] times 1 (roughly balanced).")
    console.print(
        f"1000 runs of H·H: [zero]{double.get('0', 0)}[/zero] times 0 and "
        f"[one]{double.get('1', 0)}[/one] times 1 (always 0)."
    )
    console.print("[muted]Two Hadamards cancel: the qubit returns exactly to |0>.[/muted]")

    console.print(Panel(str(single_hadamard_circuit().draw("text")), title="Single H", border_style="bits"))
    console.print(Panel(str(double_hadamard_circuit().draw("text")), title="H then H", border_style="bits"))

    console.rule("Gates as matrices")
    matrix_table = Table(title="Gates as 2x2 matrices (state = alpha|0> + beta|1>)")
    matrix_table.add_column("gate", style="bits")
    matrix_table.add_column("matrix", style="value")
    matrix_table.add_row("X", _format_matrix(matrices.X))
    matrix_table.add_row("H", _format_matrix(matrices.H))
    matrix_table.add_row("H·H", _format_matrix(matrices.H @ matrices.H))
    console.print(matrix_table)

    zero = matrices.state_vector(1, 0)
    superposed_vector = matrices.apply(matrices.H, zero)
    p0, p1 = matrices.probabilities(superposed_vector)
    console.print(
        f"H|0> = [{superposed_vector[0]:.2f}, {superposed_vector[1]:.2f}]  ->  P(0) = {p0:.2f}, P(1) = {p1:.2f}"
    )
    console.print("[muted]A gate is a matrix; the state is a vector; measuring squares the amplitudes.[/muted]")

    circuit_path = draw("build/ch04-hadamard-circuit.png")
    double_circuit_path = draw("build/ch04-hadamard2-circuit.png", double=True)
    bloch_path = render_bloch(
        [("|0>", initial), ("after H", superposed), ("after H·H: |0>", restored)],
        "build/ch04-hadamard-bloch.png",
        title="H creates superposition, another H cancels it",
    )
    counts_path = render_counts(single, "build/ch04-hadamard-counts.png", title="1000 runs of H")
    double_counts_path = render_counts(double, "build/ch04-hadamard2-counts.png", title="1000 runs of H·H")
    matrix_path = render_matrices(
        [("X", matrices.X), ("H", matrices.H), ("H·H = I", matrices.H @ matrices.H)],
        "build/ch04-gate-matrices.png",
        title="Gates as 2x2 matrices",
    )
    console.print("Saved diagrams:")
    for path in (
        circuit_path,
        double_circuit_path,
        bloch_path,
        counts_path,
        double_counts_path,
        matrix_path,
    ):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
