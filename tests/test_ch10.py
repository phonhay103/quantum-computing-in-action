import numpy as np
import pytest
from qiskit.quantum_info import Operator

from quantum_computing_in_action.ch10 import grover, oracle, search, step_by_step
from quantum_computing_in_action.ch10.oracle import marked_label

# ------------------------------------------------------------------- search


def test_the_address_book_has_one_target() -> None:
    assert len(search.DATABASE) == 8
    assert search.target_index() == 4
    assert search.DATABASE[4].name == "Albert"


def test_classical_search_counts_from_one() -> None:
    index, tries = search.classical_search()
    assert index == 4
    assert tries == 5


def test_tries_distribution_covers_the_whole_list() -> None:
    distribution = search.tries_distribution(4000, seed=2)
    assert set(distribution) == set(range(1, 9))
    assert sum(distribution.values()) == 4000


def test_tries_distribution_is_roughly_flat() -> None:
    distribution = search.tries_distribution(4000, seed=2)
    for count in distribution.values():
        assert 380 < count < 620


def test_quantum_search_finds_the_target() -> None:
    assert search.success_rate(200, seed=7) > 0.9


def test_quantum_search_returns_a_person() -> None:
    assert isinstance(search.quantum_search(seed=1), search.Person)


def test_search_rejects_bad_arguments() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        search.tries_distribution(0)
    with pytest.raises(ValueError, match="at least 1"):
        search.success_rate(0)


def test_search_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch10-tries.png"
    assert search.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------- oracle


def test_index_set_normalises_and_sorts() -> None:
    assert oracle.index_set(3, 2) == (3,)
    assert oracle.index_set([3, 1, 3], 2) == (1, 3)


def test_index_set_rejects_out_of_range() -> None:
    with pytest.raises(ValueError, match=r"\[0, 4\)"):
        oracle.index_set(4, 2)


def test_index_set_rejects_empty() -> None:
    with pytest.raises(ValueError, match="at least one"):
        oracle.index_set([], 2)


def test_marked_label_is_book_order() -> None:
    assert marked_label(2, 3) == "11"
    assert marked_label(6, 7) == "111000"


def test_phase_oracle_flips_exactly_the_marked_sign() -> None:
    operator = Operator(oracle.phase_oracle(2, 3)).data
    assert np.allclose(operator, np.diag([1, 1, 1, -1]))


def test_phase_oracle_matrix_matches_the_circuit() -> None:
    assert np.allclose(oracle.oracle_matrix(2, 3), Operator(oracle.phase_oracle(2, 3)).data.real)


def test_phase_oracle_can_mark_several_states() -> None:
    operator = Operator(oracle.phase_oracle(2, [0, 3])).data
    assert np.allclose(operator, np.diag([-1, 1, 1, -1]))


def test_phase_oracle_leaves_every_amplitude_unchanged() -> None:
    """Only a sign moves; no probability can change."""
    from qiskit import QuantumCircuit
    from qiskit.quantum_info import Statevector

    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.h(1)
    before = Statevector.from_instruction(circuit).probabilities()
    circuit.compose(oracle.phase_oracle(2, 3), inplace=True)
    after = Statevector.from_instruction(circuit).probabilities()
    assert np.allclose(before, after)


def test_oracle_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch10-oracle.png"
    assert oracle.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------- grover


@pytest.mark.parametrize(("n", "expected"), [(2, 1), (3, 2), (4, 3), (6, 6)])
def test_optimal_iterations(n: int, expected: int) -> None:
    assert grover.optimal_iterations(n) == expected


def test_optimal_iterations_rejects_zero_qubits() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        grover.optimal_iterations(0)


def test_diffusion_is_the_reflection_about_the_mean() -> None:
    n = 2
    uniform = np.ones(1 << n) / np.sqrt(1 << n)
    expected = 2 * np.outer(uniform, uniform) - np.eye(1 << n)
    assert np.allclose(Operator(grover.diffusion(n)).data, expected)


def test_diffusion_rejects_a_single_qubit() -> None:
    with pytest.raises(ValueError, match="at least 2"):
        grover.diffusion(1)


def test_two_qubit_grover_reaches_certainty_in_one_round() -> None:
    assert grover.success_probability(2, 3, 0) == pytest.approx(0.25)
    assert grover.success_probability(2, 3, 1) == pytest.approx(1.0)
    assert grover.success_probability(2, 3, 2) == pytest.approx(0.25)


def test_grover_on_64_items_peaks_at_the_optimal_round() -> None:
    optimum = grover.optimal_iterations(6)
    probability = grover.success_probability(6, 7, optimum)
    assert probability > 0.99
    # One round either side is worse: the peak is real, not the first thing tried.
    assert grover.success_probability(6, 7, optimum - 1) < probability
    assert grover.success_probability(6, 7, optimum + 1) < probability


def test_grover_beats_guessing_after_a_single_round() -> None:
    """The default search needs only a handful of rounds for 64 items."""
    probability = grover.success_probability(6, 7)
    assert probability > 1 / 64


def test_measured_counts_favour_the_marked_state() -> None:
    counts = grover.measured_counts(6, 7, 2000, seed=4)
    assert sum(counts.values()) == 2000
    assert max(counts, key=lambda label: counts[label]) == marked_label(6, 7)


def test_success_curve_is_a_probability_per_round() -> None:
    curve = grover.success_curve(3, 5)
    assert set(curve) == set(range(grover.optimal_iterations(3) + 4))
    assert all(0.0 <= value <= 1.0 for value in curve.values())


def test_grover_circuit_rejects_a_negative_iteration_count() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        grover.grover_circuit(3, 5, -1)


def test_grover_circuit_measures_every_qubit() -> None:
    names = [instruction.operation.name for instruction in grover.grover_circuit(3, 5, 1).data]
    assert names.count("measure") == 3


def test_grover_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch10-grover.png"
    assert grover.draw(output) == output
    assert output.exists()


# -------------------------------------------------------------- step_by_step


def test_step_by_step_covers_the_rise_and_the_overshoot() -> None:
    distributions = step_by_step.round_distributions()
    assert [label for label, _ in distributions] == ["after 0 round(s)", "after 1 round(s)", "after 2 round(s)"]
    for _, distribution in distributions:
        assert sum(distribution.values()) == pytest.approx(1.0)
    assert distributions[1][1][marked_label(2, 3)] == pytest.approx(1.0)


def test_step_by_step_states_start_uniform() -> None:
    state = step_by_step.round_states()[0][1]
    assert np.allclose(np.abs(state.data), 0.5)


def test_step_by_step_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch10-step.png"
    assert step_by_step.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------ package


def test_chapter_runs_all_four_samples_in_order() -> None:
    from quantum_computing_in_action import ch10

    assert (search, oracle, step_by_step, grover) == ch10.SAMPLES
