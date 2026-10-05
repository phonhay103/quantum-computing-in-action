import pytest

from quantum_computing_in_action.ch02 import random_bit, random_bits


def test_random_bit_is_zero_or_one() -> None:
    assert random_bit() in (0, 1)


def test_random_bits_returns_requested_count() -> None:
    bits = random_bits(32)
    assert len(bits) == 32
    assert set(bits) <= {0, 1}


def test_random_bits_rejects_non_positive_count() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        random_bits(0)


def test_random_bits_are_roughly_balanced() -> None:
    bits = random_bits(2000)
    ones = bits.count(1)
    assert 0.4 < ones / len(bits) < 0.6
