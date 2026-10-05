from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_computing_in_action._diagrams import render_bloch, render_circuit, render_counts


def test_render_circuit_writes_file(tmp_path) -> None:
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    output = tmp_path / "circuit.png"
    assert render_circuit(circuit, output) == output
    assert output.exists()


def test_render_counts_writes_file(tmp_path) -> None:
    output = tmp_path / "counts.png"
    assert render_counts({"0": 5, "1": 7}, output) == output
    assert output.exists()


def test_render_bloch_writes_file(tmp_path) -> None:
    output = tmp_path / "bloch.png"
    states = [("|0>", Statevector.from_label("0"))]
    assert render_bloch(states, output) == output
    assert output.exists()
