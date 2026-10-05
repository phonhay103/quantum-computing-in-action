"""Chapter 3 — the Pauli-X gate: flipping a qubit."""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.panel import Panel

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_bloch, render_circuit, render_counts


def _x_circuit() -> QuantumCircuit:
    """A one-qubit circuit that applies the Pauli-X gate."""
    circuit = QuantumCircuit(1, 1)
    circuit.x(0)
    return circuit


def _double_x_circuit() -> QuantumCircuit:
    """A one-qubit circuit that applies the Pauli-X gate twice.

    Because ``X`` is its own inverse, ``X·X = I``: the second gate undoes the
    first one and the qubit returns to ``|0>``.
    """
    circuit = QuantumCircuit(1, 1)
    circuit.x(0)
    circuit.x(0)
    return circuit


def pauli_x_circuit() -> QuantumCircuit:
    """The Pauli-X circuit plus a measurement."""
    circuit = _x_circuit()
    circuit.measure(0, 0)
    return circuit


def double_pauli_x_circuit() -> QuantumCircuit:
    """The ``X``-then-``X`` circuit plus a measurement (always ``0``)."""
    circuit = _double_x_circuit()
    circuit.measure(0, 0)
    return circuit


def _probabilities(state: Statevector) -> str:
    probs = state.probabilities_dict()
    return f"P(0) = {float(probs.get('0', 0.0)):.2f}, P(1) = {float(probs.get('1', 0.0)):.2f}"


def measure_pauli_x() -> int:
    """Run the Pauli-X circuit and return the measured value.

    The qubit starts in ``|0>``; the X gate flips it to ``|1>``, so the result
    is deterministically ``1``.
    """
    circuit = _x_circuit()
    state = Statevector.from_instruction(circuit)
    counts = state.sample_counts(1)
    return 1 if counts.get("1", 0) else 0


def repeat_pauli_x(shots: int = 1000) -> dict[str, int]:
    """Measure ``X|0> = |1>`` ``shots`` times; always returns ``{"1": shots}``."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    state = Statevector.from_instruction(_x_circuit())
    return {str(bit): int(count) for bit, count in state.sample_counts(shots).items()}


def repeat_double_pauli_x(shots: int = 1000) -> dict[str, int]:
    """Measure ``X·X|0> = |0>`` ``shots`` times; always returns ``{"0": shots}``."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    state = Statevector.from_instruction(_double_x_circuit())
    return {str(bit): int(count) for bit, count in state.sample_counts(shots).items()}


def draw(output: str | Path = "build/ch03-pauli-x.png", *, double: bool = False) -> Path:
    """Render the single (or double) Pauli-X circuit and save it to ``output``."""
    circuit = double_pauli_x_circuit() if double else pauli_x_circuit()
    return render_circuit(circuit, output)


def main() -> None:
    explain(
        "Chapter 3 — Qubits and quantum gates",
        """
The qubit starts in state `|0>`. The **Pauli-X gate** flips it to `|1>` — the
quantum equivalent of a classical `NOT` gate:

`X|0> = |1>      X|1> = |0>`

Because there is no superposition here, measuring always returns the same
answer: `1`. The result is deterministic, not random.

Like every quantum gate, `X` is **reversible**: it is its own inverse, so
`X·X = I`. Applying `X` twice brings the qubit back to `|0>` — a first taste of
the "gates as reversible operations" idea that Chapter 4 turns into matrices.

The circuit below reads left to right: an `X` gate on qubit `q`, then a
measurement `M` that writes the outcome into the classical bit `c`.
""",
    )

    initial = Statevector.from_label("0")
    flipped = Statevector.from_instruction(_x_circuit())
    restored = Statevector.from_instruction(_double_x_circuit())
    value = measure_pauli_x()
    single = repeat_pauli_x(1000)
    double = repeat_double_pauli_x(1000)

    steps(
        "Chapter 3 — step by step",
        [
            ("Prepare a qubit in |0>", _probabilities(initial)),
            ("Apply the Pauli-X gate", _probabilities(flipped)),
            ("Measure the qubit", f"always reads {value} (no superposition)"),
            ("Apply X a second time", _probabilities(restored)),
            ("Measure (X·X)", f"always 0 — got {double.get('0', 0)}/1000 zeros"),
        ],
    )

    console.print(f"Value = [value]{value}[/value]")
    console.print(
        f"1000 runs of X: [zero]{single.get('0', 0)}[/zero] times 0 and "
        f"[one]{single.get('1', 0)}[/one] times 1 (always 1)."
    )
    console.print(
        f"1000 runs of X·X: [zero]{double.get('0', 0)}[/zero] times 0 and "
        f"[one]{double.get('1', 0)}[/one] times 1 (always 0)."
    )
    console.print(Panel(str(pauli_x_circuit().draw("text")), title="Pauli-X circuit", border_style="bits"))
    console.print(Panel(str(double_pauli_x_circuit().draw("text")), title="X then X", border_style="bits"))

    circuit_path = draw()
    double_circuit_path = draw("build/ch03-pauli-x2-circuit.png", double=True)
    bloch_path = render_bloch(
        [("before: |0>", initial), ("after X: |1>", flipped), ("after X·X: |0>", restored)],
        "build/ch03-pauli-x-bloch.png",
        title="Pauli-X flips the qubit; two X gates cancel",
    )
    counts_path = render_counts(single, "build/ch03-pauli-x-counts.png", title="1000 runs of X")
    double_counts_path = render_counts(double, "build/ch03-pauli-x2-counts.png", title="1000 runs of X·X")
    console.print("Saved diagrams:")
    for path in (circuit_path, double_circuit_path, bloch_path, counts_path, double_counts_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
