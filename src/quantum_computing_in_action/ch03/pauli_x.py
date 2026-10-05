"""Chapter 3 — the Pauli-X gate: flipping a qubit."""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.panel import Panel

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_bloch, render_circuit


def _x_circuit() -> QuantumCircuit:
    """A one-qubit circuit that applies the Pauli-X gate."""
    circuit = QuantumCircuit(1, 1)
    circuit.x(0)
    return circuit


def pauli_x_circuit() -> QuantumCircuit:
    """The Pauli-X circuit plus a measurement."""
    circuit = _x_circuit()
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


def draw(output: str | Path = "build/pauli-x.png") -> Path:
    """Render the circuit on a dark background and save it to ``output``."""
    return render_circuit(pauli_x_circuit(), output)


def main() -> None:
    explain(
        "Chapter 3 — The Pauli-X gate",
        """
The qubit starts in state `|0>`. The **Pauli-X gate** flips it to `|1>` — the
quantum equivalent of a classical `NOT` gate:

`X|0> = |1>      X|1> = |0>`

Because there is no superposition here, measuring always returns the same
answer: `1`. The result is deterministic, not random.

The circuit below reads left to right: an `X` gate on qubit `q`, then a
measurement `M` that writes the outcome into the classical bit `c`.
""",
    )

    initial = Statevector.from_label("0")
    flipped = Statevector.from_instruction(_x_circuit())
    value = measure_pauli_x()

    steps(
        "Chapter 3 — step by step",
        [
            ("Prepare a qubit in |0>", _probabilities(initial)),
            ("Apply the Pauli-X gate", _probabilities(flipped)),
            ("Measure the qubit", f"always reads {value} (no superposition)"),
        ],
    )

    console.print(f"Value = [value]{value}[/value]")
    console.print(Panel(str(pauli_x_circuit().draw("text")), title="Pauli-X circuit", border_style="bits"))
    circuit_path = draw()
    bloch_path = render_bloch(
        [("before: |0>", initial), ("after X: |1>", flipped)],
        "build/pauli-x-bloch.png",
        title="Pauli-X flips the qubit",
    )
    console.print("Saved diagrams:")
    for path in (circuit_path, bloch_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
