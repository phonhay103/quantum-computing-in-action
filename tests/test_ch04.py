import pytest

from quantum_computing_in_action.ch04 import (
    double_hadamard_circuit,
    draw,
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
