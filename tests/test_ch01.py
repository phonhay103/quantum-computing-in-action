import math

import pytest

from quantum_computing_in_action.ch01 import (
    classical_factoring_time,
    plot,
    sample,
    shor_factoring_time,
)


def test_shor_time_is_cubic() -> None:
    assert shor_factoring_time(10) == 1000.0


def test_classical_time_matches_formula() -> None:
    bits = 64
    expected = math.exp((64.0 / 9.0 * bits * math.log(bits) ** 2) ** (1.0 / 3.0))
    assert classical_factoring_time(bits) == pytest.approx(expected)


@pytest.mark.parametrize("function", [classical_factoring_time, shor_factoring_time])
def test_time_functions_reject_non_positive_bits(function) -> None:
    with pytest.raises(ValueError, match="positive"):
        function(0)


def test_sample_yields_requested_number_of_points() -> None:
    points = list(sample(shor_factoring_time, 1.0, 11.0, div=100))
    assert len(points) == 100
    assert points[0][0] == 1.0
    assert all(time == bits**3.0 for bits, time in points)


def test_plot_writes_file(tmp_path) -> None:
    output = tmp_path / "chart.png"
    assert plot(output=output) == output
    assert output.exists()


def test_plot_classical_only_writes_file(tmp_path) -> None:
    output = tmp_path / "classical.png"
    assert plot(output=output, include_shor=False) == output
    assert output.exists()
