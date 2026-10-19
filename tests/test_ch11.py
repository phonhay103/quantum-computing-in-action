import numpy as np
import pytest
from qiskit.quantum_info import Operator

from quantum_computing_in_action.ch11 import classical, qft, shor

# ---------------------------------------------------------------- classical


@pytest.mark.parametrize(("n", "expected"), [(15, 3), (91, 7), (97, 97), (2, 2), (999983, 999983)])
def test_trial_division(n: int, expected: int) -> None:
    assert classical.trial_division(n) == expected


def test_trial_division_rejects_small_input() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        classical.trial_division(1)


def test_steps_to_factor_grows_with_n() -> None:
    assert classical.steps_to_factor(15) == 2
    assert classical.steps_to_factor(999983) > 100


def test_steps_to_factor_rejects_small_input() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        classical.steps_to_factor(1)


@pytest.mark.parametrize(("a", "n", "expected"), [(2, 15, 4), (2, 21, 6), (7, 15, 4), (3, 7, 6)])
def test_classical_period(a: int, n: int, expected: int) -> None:
    assert classical.classical_period(a, n) == expected


def test_classical_period_rejects_non_coprime() -> None:
    with pytest.raises(ValueError, match="coprime"):
        classical.classical_period(5, 15)


def test_factor_from_order() -> None:
    assert classical.factor_from_order(2, 15, 4) == 3


def test_factor_from_order_rejects_odd_period() -> None:
    assert classical.factor_from_order(2, 15, 3) is None


def test_factor_from_order_rejects_minus_one() -> None:
    """a^(r/2) = -1 gives the trivial +1 side, so the attempt must fail."""
    # 2^2 = 4 = -1 mod 5, period of 2 mod 5 is 4.
    assert classical.factor_from_order(2, 5, 4) is None


@pytest.mark.parametrize(("n", "expected"), [(15, 3), (21, 7), (35, 7), (91, 7)])
def test_semiclassic_factor(n: int, expected: int) -> None:
    assert classical.semiclassic_factor(n) == expected


def test_semiclassic_factor_rejects_small_input() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        classical.semiclassic_factor(1)


def test_period_function_repeats() -> None:
    values = classical.period_function(2, 15, 8)
    assert list(values.values()) == [1, 2, 4, 8, 1, 2, 4, 8]


def test_period_function_rejects_non_coprime() -> None:
    with pytest.raises(ValueError, match="coprime"):
        classical.period_function(5, 15)


def test_reduction_steps_reproduce_the_book_larger_example() -> None:
    """The book's jshell snippets: a = 6, N = 493, period 112, gcds 29 and 17."""
    worked = classical.reduction_steps(6, 493)
    assert worked["period"] == 112
    assert worked["a^(r/2) mod n"] == 407
    assert {worked["gcd(a^(r/2) - 1, n)"], worked["gcd(a^(r/2) + 1, n)"]} == {29, 17}


def test_reduction_steps_reject_an_odd_period() -> None:
    """The order of 2 modulo 7 is 3, so a^(r/2) has no integer exponent."""
    assert classical.classical_period(2, 7) == 3
    with pytest.raises(ValueError, match="odd"):
        classical.reduction_steps(2, 7)


def test_random_semiclassic_factor_finds_a_factor() -> None:
    n, factor = classical.random_semiclassic_factor(seed=7)
    assert 1 < factor < n
    assert n % factor == 0


def test_random_semiclassic_factor_rejects_a_small_upper_bound() -> None:
    with pytest.raises(ValueError, match="at least 4"):
        classical.random_semiclassic_factor(upper=3)


def test_classical_curve_rejects_small_limit() -> None:
    with pytest.raises(ValueError, match="at least 3"):
        classical.steps_curve(2)


def test_classical_draws_write_files(tmp_path) -> None:
    assert classical.draw_classical(tmp_path / "ch11-classical.png").exists()
    assert classical.draw_period(tmp_path / "ch11-period.png").exists()


# ---------------------------------------------------------------------- qft


def test_qft_matrix_is_unitary() -> None:
    matrix = qft.qft_matrix(3)
    assert np.allclose(matrix @ matrix.conj().T, np.eye(8))


def test_qft_circuit_matches_the_fourier_matrix() -> None:
    assert np.allclose(Operator(qft.qft_circuit(3)).data, qft.qft_matrix(3))


def test_inverse_qft_undoes_the_qft() -> None:
    forward = Operator(qft.qft_circuit(3)).data
    backward = Operator(qft.qft_circuit(3, inverse=True)).data
    assert np.allclose(backward @ forward, np.eye(8))


def test_qft_matrix_rejects_bad_width() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        qft.qft_matrix(0)
    with pytest.raises(ValueError, match="at least 1"):
        qft.qft_circuit(0)


def test_phase_ramp_is_linear() -> None:
    ramp = qft.phase_ramp(3)
    assert set(ramp) == set(range(8))
    expected = [2 * np.pi * index / 8 for index in range(8)]
    for index, angle in ramp.items():
        assert np.cos(angle) == pytest.approx(np.cos(expected[index]))
        assert np.sin(angle) == pytest.approx(np.sin(expected[index]))


def test_qft_draws_write_files(tmp_path) -> None:
    assert qft.draw_circuit(tmp_path / "ch11-qft-circuit.png").exists()
    assert qft.draw_phase(tmp_path / "ch11-qft-phase.png").exists()


# --------------------------------------------------------------------- shor


def test_modular_multiplier_is_a_permutation() -> None:
    matrix = shor.modular_multiplier(2, 15, 4)
    assert np.allclose(matrix.sum(axis=0), 1.0)
    assert np.allclose(matrix.sum(axis=1), 1.0)


def test_modular_multiplier_rejects_non_coprime() -> None:
    with pytest.raises(ValueError, match="coprime"):
        shor.modular_multiplier(5, 15, 4)


def test_register_widths() -> None:
    assert shor.work_width(15) == 4
    assert shor.counting_width(15) == 8
    assert shor.work_width(21) == 5
    assert shor.counting_width(21) == 10


def test_register_widths_reject_small_input() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        shor.work_width(1)
    with pytest.raises(ValueError, match="at least 2"):
        shor.counting_width(1)


def test_convergents() -> None:
    assert shor.convergents(64, 256) == [(0, 1), (1, 4)]
    assert shor.convergents(0, 16) == [(0, 1)]


def test_convergents_reject_zero_denominator() -> None:
    with pytest.raises(ValueError, match="denominator"):
        shor.convergents(1, 0)


def test_period_from_outcome() -> None:
    assert shor.period_from_outcome(64, 8, 15, 2) == 4
    assert shor.period_from_outcome(192, 8, 15, 2) == 4
    # k = 0 and k = 2 are not coprime to r = 4, so they must be rejected.
    assert shor.period_from_outcome(0, 8, 15, 2) is None
    assert shor.period_from_outcome(128, 8, 15, 2) is None


def test_order_distribution_concentrates_on_the_peaks() -> None:
    distribution = shor.order_distribution(2, 15)
    peaks = {outcome: round(probability, 3) for outcome, probability in distribution.items() if probability > 1e-9}
    assert peaks == {0: 0.25, 64: 0.25, 128: 0.25, 192: 0.25}
    assert sum(distribution.values()) == pytest.approx(1.0)


def test_quantum_order_finds_the_period() -> None:
    assert shor.quantum_order(2, 15) == 4
    assert shor.quantum_order(7, 15) == 4


def test_shor_factors_the_small_semiprimes() -> None:
    assert shor.shor(15) == (3, 5)
    assert shor.shor(21) == (3, 7)


def test_shor_handles_an_even_number_directly() -> None:
    assert shor.shor(14) == (2, 7)


def test_shor_rejects_small_input() -> None:
    with pytest.raises(ValueError, match="at least 4"):
        shor.shor(3)


def test_order_finding_circuit_measures_the_counting_register() -> None:
    names = [instruction.operation.name for instruction in shor.order_finding_circuit(2, 15, m=4, width=4).data]
    assert names.count("measure") == 4


def test_shor_draws_write_files(tmp_path) -> None:
    assert shor.draw(tmp_path / "ch11-peaks.png").exists()
    assert shor.draw_circuit(tmp_path / "ch11-circuit.png").exists()


# ------------------------------------------------------------------ package


def test_chapter_runs_all_three_samples_in_order() -> None:
    from quantum_computing_in_action import ch11

    assert (classical, qft, shor) == ch11.SAMPLES
