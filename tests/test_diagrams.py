import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_computing_in_action._diagrams import (
    render_bloch,
    render_circuit,
    render_counts,
    render_grouped_counts,
    render_matrices,
)


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


def test_render_grouped_counts_writes_file(tmp_path) -> None:
    output = tmp_path / "grouped.png"
    series = [("independent", {"00": 1, "11": 2}), ("bell", {"00": 3, "11": 4})]
    assert render_grouped_counts(series, output) == output
    assert output.exists()


def test_render_counts_accepts_a_rotation(tmp_path) -> None:
    output = tmp_path / "rotated.png"
    assert render_counts({"0": 1, "1": 2}, output, rotation=90.0) == output
    assert output.exists()


def test_render_grouped_counts_accepts_rotation_and_hidden_labels(tmp_path) -> None:
    output = tmp_path / "grouped-rotated.png"
    series = [("a", {"00": 1, "01": 2, "10": 3, "11": 4}), ("b", {"00": 4, "01": 3, "10": 2, "11": 1})]
    assert render_grouped_counts(series, output, rotation=90.0, bar_labels=False) == output
    assert output.exists()


def test_render_matrices_writes_file(tmp_path) -> None:
    from qiskit.quantum_info import Operator

    output = tmp_path / "matrices.png"
    matrices = [
        ("X", np.array([[0, 1], [1, 0]], dtype=complex)),
        ("H", Operator(QuantumCircuit(1)).data),  # a second panel exercises the layout
    ]
    assert render_matrices(matrices, output) == output
    assert output.exists()


def test_render_matrices_accepts_figsize_and_fontsize(tmp_path) -> None:
    """The Toffoli matrix of Chapter 7 needs a bigger figure and smaller text."""
    output = tmp_path / "big-matrix.png"
    matrix = np.eye(8, dtype=complex)
    matrices = [("Toffoli", matrix)]
    assert render_matrices(matrices, output, title="8x8", figsize=(6.0, 6.0), fontsize=7.0) == output
    assert output.exists()
