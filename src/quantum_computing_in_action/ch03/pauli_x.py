"""Chapter 3 — the Pauli-X gate: flipping a qubit."""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.panel import Panel

from quantum_computing_in_action._console import DARK_CIRCUIT_STYLE, console


def pauli_x_circuit() -> QuantumCircuit:
    """A one-qubit circuit that applies the Pauli-X gate and measures the qubit."""
    circuit = QuantumCircuit(1, 1)
    circuit.x(0)
    circuit.measure(0, 0)
    return circuit


def measure_pauli_x() -> int:
    """Run the Pauli-X circuit and return the measured value.

    The qubit starts in ``|0>``; the X gate flips it to ``|1>``, so the result
    is deterministically ``1``.
    """
    circuit = pauli_x_circuit()
    circuit.remove_final_measurements(inplace=True)
    state = Statevector.from_instruction(circuit)
    counts = state.sample_counts(1)
    return 1 if counts.get("1", 0) else 0


def draw(output: str | Path = "build/pauli-x.png") -> Path:
    """Render the circuit on a dark background and save it to ``output``."""
    import matplotlib

    matplotlib.use("Agg")

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    pauli_x_circuit().draw("mpl", filename=str(path), style=DARK_CIRCUIT_STYLE)
    return path


def main() -> None:
    console.print(f"Value = [value]{measure_pauli_x()}[/value]")
    console.print(Panel(str(pauli_x_circuit().draw("text")), title="Pauli-X circuit", border_style="bits"))
    path = draw()
    console.print(f"Saved circuit render to [path]{path}[/path]")


if __name__ == "__main__":
    main()
