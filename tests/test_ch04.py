import numpy as np
import pytest
from qiskit.circuit.library import HGate, XGate
from qiskit.quantum_info import Operator

from quantum_computing_in_action.ch04 import (
    double_hadamard_circuit,
    draw,
    matrices,
    random_bit,
    repeat_double_hadamard,
    repeat_single_hadamard,
    single_hadamard_circuit,
)


def test_single_hadamard_circuit_has_one_h_gate() -> None:
    names = [instruction.operation.name for instruction in single_hadamard_circuit().data]
    assert names.count("h") == 1


def test_double_hadamard_circuit_has_two_h_gates() -> None:
    names = [instruction.operation.name for instruction in double_hadamard_circuit().data]
    assert names.count("h") == 2


def test_random_bit_is_zero_or_one() -> None:
    assert random_bit() in (0, 1)


def test_repeat_single_hadamard_returns_requested_shots() -> None:
    counts = repeat_single_hadamard(500)
    assert sum(counts.values()) == 500
    assert set(counts) <= {"0", "1"}


def test_repeat_single_hadamard_is_roughly_balanced() -> None:
    counts = repeat_single_hadamard(2000)
    ones = counts.get("1", 0)
    assert 0.4 < ones / 2000 < 0.6


def test_repeat_double_hadamard_is_deterministic() -> None:
    counts = repeat_double_hadamard(500)
    assert counts == {"0": 500}


@pytest.mark.parametrize("shots", [0, -1])
def test_repeat_hadamard_rejects_non_positive_shots(shots: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        repeat_single_hadamard(shots)
    with pytest.raises(ValueError, match="at least 1"):
        repeat_double_hadamard(shots)


def test_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch04-hadamard.png"
    assert draw(output) == output
    assert output.exists()


def test_x_matrix_matches_qiskit() -> None:
    assert np.allclose(matrices.X, Operator(XGate()).data)


def test_h_matrix_matches_qiskit() -> None:
    assert np.allclose(matrices.H, Operator(HGate()).data)


def test_h_squared_is_identity() -> None:
    assert matrices.is_identity(matrices.H @ matrices.H)


def test_x_squared_is_identity() -> None:
    assert matrices.is_identity(matrices.X @ matrices.X)


def test_compose_two_hadamards_is_identity() -> None:
    assert matrices.is_identity(matrices.compose([matrices.H, matrices.H]))


def test_apply_hadamard_to_zero_gives_even_superposition() -> None:
    state = matrices.apply(matrices.H, matrices.state_vector(1, 0))
    p0, p1 = matrices.probabilities(state)
    assert p0 == pytest.approx(0.5)
    assert p1 == pytest.approx(0.5)


def test_apply_pauli_x_swaps_amplitudes() -> None:
    state = matrices.apply(matrices.X, matrices.state_vector(1, 0))
    assert matrices.probabilities(state) == pytest.approx((0.0, 1.0))
