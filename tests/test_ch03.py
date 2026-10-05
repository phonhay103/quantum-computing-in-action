import pytest

from quantum_computing_in_action.ch03 import (
    double_pauli_x_circuit,
    draw,
    measure_pauli_x,
    pauli_x_circuit,
    repeat_double_pauli_x,
    repeat_pauli_x,
)


def test_pauli_x_measures_one() -> None:
    assert measure_pauli_x() == 1


def test_pauli_x_circuit_has_x_gate() -> None:
    instructions = pauli_x_circuit().data
    assert any(instruction.operation.name == "x" for instruction in instructions)


def test_double_pauli_x_circuit_has_two_x_gates() -> None:
    names = [instruction.operation.name for instruction in double_pauli_x_circuit().data]
    assert names.count("x") == 2


def test_repeat_pauli_x_is_always_one() -> None:
    counts = repeat_pauli_x(500)
    assert counts == {"1": 500}


def test_repeat_double_pauli_x_is_always_zero() -> None:
    counts = repeat_double_pauli_x(500)
    assert counts == {"0": 500}


@pytest.mark.parametrize("shots", [0, -1])
def test_repeat_pauli_x_rejects_non_positive_shots(shots: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        repeat_pauli_x(shots)
    with pytest.raises(ValueError, match="at least 1"):
        repeat_double_pauli_x(shots)


def test_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "pauli-x.png"
    assert draw(output=output) == output
    assert output.exists()


def test_draw_double_writes_file(tmp_path) -> None:
    output = tmp_path / "pauli-x2.png"
    assert draw(output=output, double=True) == output
    assert output.exists()
