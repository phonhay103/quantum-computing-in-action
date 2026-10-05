import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from quantum_computing_in_action.ch05 import (
    bell_circuit,
    bell_counts,
    bell_statevector,
    classical_two_coins,
    cnot_circuit,
    cnot_truth_table,
    draw,
    independent_counts,
    states,
)


def test_bell_circuit_has_hadamard_and_cnot() -> None:
    names = [instruction.operation.name for instruction in bell_circuit().data]
    assert names.count("h") == 1
    assert names.count("cx") == 1


def test_cnot_circuit_has_one_cx() -> None:
    names = [instruction.operation.name for instruction in cnot_circuit().data]
    assert names.count("cx") == 1


def test_bell_statevector_amplitudes() -> None:
    amplitudes = states.amplitudes(bell_statevector().data)
    root = 1 / np.sqrt(2)
    assert amplitudes["00"] == pytest.approx(root)
    assert amplitudes["11"] == pytest.approx(root)
    assert amplitudes["01"] == pytest.approx(0.0)
    assert amplitudes["10"] == pytest.approx(0.0)


def test_bell_state_helper_matches_circuit() -> None:
    assert np.allclose(states.bell_state(0), bell_statevector().data)


def test_bell_counts_only_correlated_outcomes() -> None:
    counts = bell_counts(600)
    assert sum(counts.values()) == 600
    assert set(counts) <= {"00", "11"}


def test_independent_counts_use_all_four_outcomes() -> None:
    counts = independent_counts(2000)
    assert set(counts) == {"00", "01", "10", "11"}
    assert sum(counts.values()) == 2000


def test_classical_two_coins_use_all_four_outcomes() -> None:
    counts = classical_two_coins(4000)
    assert set(counts) == {"00", "01", "10", "11"}
    assert sum(counts.values()) == 4000
    for value in counts.values():
        assert 0.15 < value / 4000 < 0.35


def test_cnot_truth_table() -> None:
    assert cnot_truth_table() == [
        ("00", "00"),
        ("01", "01"),
        ("10", "11"),
        ("11", "10"),
    ]


@pytest.mark.parametrize("shots", [0, -1])
def test_shots_must_be_positive(shots: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        bell_counts(shots)
    with pytest.raises(ValueError, match="at least 1"):
        independent_counts(shots)
    with pytest.raises(ValueError, match="at least 1"):
        classical_two_coins(shots)


def test_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch05-bell.png"
    assert draw(output) == output
    assert output.exists()


def test_cnot_matrix_matches_qiskit() -> None:
    circuit = QuantumCircuit(2)
    circuit.cx(1, 0)
    assert np.allclose(states.CNOT, Operator(circuit).data)


def test_cnot_matrix_flips_the_target() -> None:
    assert np.allclose(states.CNOT @ states.ket("10"), states.ket("11"))
    assert np.allclose(states.CNOT @ states.ket("11"), states.ket("10"))
    assert np.allclose(states.CNOT @ states.ket("01"), states.ket("01"))


def test_ket_and_tensor_agree() -> None:
    assert np.allclose(states.tensor(states.qubit_ket("0"), states.qubit_ket("1")), states.ket("01"))
    assert np.allclose(states.tensor(states.qubit_ket("1"), states.qubit_ket("0")), states.ket("10"))


def test_bell_state_is_entangled() -> None:
    assert states.is_entangled(bell_statevector().data)
    assert states.schmidt_rank(bell_statevector().data) == 2


def test_product_state_is_not_entangled() -> None:
    plus = np.array([1, 1], dtype=complex) / np.sqrt(2)
    product = states.tensor(plus, plus)
    assert not states.is_entangled(product)
    assert states.schmidt_rank(product) == 1


def test_ket_rejects_unknown_label() -> None:
    with pytest.raises(ValueError, match="label must be one of"):
        states.ket("2")


def test_bell_state_rejects_unknown_index() -> None:
    with pytest.raises(ValueError, match="index must be"):
        states.bell_state(9)


def test_bell_probabilities() -> None:
    probabilities = states.probabilities(bell_statevector().data)
    assert probabilities["00"] == pytest.approx(0.5)
    assert probabilities["11"] == pytest.approx(0.5)
    assert probabilities["01"] == pytest.approx(0.0)
    assert probabilities["10"] == pytest.approx(0.0)
