import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_computing_in_action.ch07 import circuits, debugging, full_adder, half_adder, randombit

# ----------------------------------------------------------------- circuits


def test_book_label_puts_qubit_zero_first() -> None:
    """Qiskit's c3c2c1c0 becomes the book's q0 q1 q2 q3."""
    assert circuits.book_label("1000") == "0001"


def test_probabilities_keep_the_zero_entries() -> None:
    """The book's debugger shows the whole vector, zeros included."""
    state = Statevector.from_label("00")
    assert circuits.probabilities(state) == {"00": pytest.approx(1.0), "01": 0.0, "10": 0.0, "11": 0.0}
    assert len(circuits.probabilities(Statevector.from_label("0000"))) == 16


def test_nonzero_probabilities_drop_the_zeros() -> None:
    # ``Statevector.from_label`` is in Qiskit order (q2 q1 q0); the result is in
    # the book's order, so it is the mirror of the label that went in.
    label = "011"
    assert circuits.nonzero_probabilities(Statevector.from_label(label)) == {
        circuits.book_label(label): pytest.approx(1.0)
    }


def test_prob_one_per_qubit_reads_the_marginals() -> None:
    state = Statevector.from_label("101")  # q0 = 1, q1 = 0, q2 = 1
    assert circuits.prob_one_per_qubit(state) == {0: pytest.approx(1.0), 1: 0.0, 2: pytest.approx(1.0)}


def test_prob_one_per_qubit_of_a_superposition() -> None:
    circuit = QuantumCircuit(1)
    circuit.h(0)
    state = Statevector.from_instruction(circuit)
    assert circuits.prob_one_per_qubit(state)[0] == pytest.approx(0.5)


def test_cumulative_states_start_with_the_initial_state() -> None:
    steps = [("H", lambda circuit: circuit.h(0))]
    states = circuits.cumulative_states(steps, 1)
    assert [label for label, _ in states] == [circuits.START_LABEL, "H"]
    assert circuits.prob_one_per_qubit(states[1][1])[0] == pytest.approx(0.5)


def test_sample_counts_are_reproducible_and_sum_to_shots() -> None:
    state = randombit.program_state()
    first = circuits.sample_counts(state, 500, seed=5)
    second = circuits.sample_counts(state, 500, seed=5)
    assert first == second
    assert sum(first.values()) == 500


def test_sample_counts_rejects_bad_shots() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        circuits.sample_counts(randombit.program_state(), 0)


def test_basis_state_reads_a_single_basis_state() -> None:
    # The input label is in Qiskit order; the answer is in the book's order.
    label = "011"
    assert circuits.basis_state(Statevector.from_label(label)) == circuits.book_label(label)


def test_basis_state_rejects_a_superposition() -> None:
    circuit = QuantumCircuit(1)
    circuit.h(0)
    with pytest.raises(ValueError, match="not a single basis state"):
        circuits.basis_state(Statevector.from_instruction(circuit))


# --------------------------------------------------------------- randombit


def test_program_circuit_is_h_x_and_a_cnot_with_measurements() -> None:
    circuit = randombit.program_circuit()
    names = [instruction.operation.name for instruction in circuit.data]
    assert names.count("h") == 1
    assert names.count("x") == 1
    assert names.count("cx") == 1
    assert names.count("measure") == 4


def test_program_state_correlates_q0_and_q1() -> None:
    """The only outcomes are 0001 and 1101: q2 = 0, q3 = 1, q0 = q1."""
    state = randombit.program_state()
    assert circuits.nonzero_probabilities(state) == {"0001": pytest.approx(0.5), "1101": pytest.approx(0.5)}


def test_step_states_show_where_each_qubit_changes() -> None:
    states = dict(randombit.step_states())
    start = circuits.prob_one_per_qubit(states["start"])
    assert start == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
    after_h = circuits.prob_one_per_qubit(states["H(0), X(3)"])
    assert after_h == {0: pytest.approx(0.5), 1: 0.0, 2: 0.0, 3: pytest.approx(1.0)}
    after_cnot = circuits.prob_one_per_qubit(states["CNOT(0, 1)"])
    assert after_cnot == {0: pytest.approx(0.5), 1: pytest.approx(0.5), 2: 0.0, 3: pytest.approx(1.0)}


def test_random_bits_only_ever_agree_on_q0_and_q1() -> None:
    counts = randombit.random_bits(4000, seed=3)
    assert sum(counts.values()) == 4000
    assert set(counts) == {"0001", "1101"}
    for label in counts:
        assert label[2] == "0"  # q2 never fires
        assert label[3] == "1"  # q3 was set by X
        assert label[0] == label[1]  # the CNOT glued q0 and q1


def test_qubit_probabilities_pin_q2_and_q3() -> None:
    assert randombit.qubit_probabilities() == {
        0: pytest.approx(0.5),
        1: pytest.approx(0.5),
        2: 0.0,
        3: pytest.approx(1.0),
    }


def test_randombit_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch07-randombit.png"
    assert randombit.draw(output) == output
    assert output.exists()


# --------------------------------------------------------------- debugging


def test_debug_circuit_marks_each_step_with_a_barrier() -> None:
    names = [instruction.operation.name for instruction in debugging.debug_circuit().data]
    assert names == ["barrier", "h", "x", "barrier", "cx", "barrier"]


def test_step_probabilities_are_normalised() -> None:
    for _, distribution in debugging.step_probabilities():
        assert sum(distribution.values()) == pytest.approx(1.0)


def test_step_probabilities_track_the_single_sign_change_free_program() -> None:
    by_step = dict(debugging.step_probabilities())
    assert by_step["start"] == {"0000": pytest.approx(1.0)}
    assert by_step["H(0), X(3)"] == {"0001": pytest.approx(0.5), "1001": pytest.approx(0.5)}
    assert by_step["CNOT(0, 1)"] == {"0001": pytest.approx(0.5), "1101": pytest.approx(0.5)}


def test_step_marginals_match_the_states() -> None:
    marginals = dict(debugging.step_marginals())
    assert marginals["start"] == {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
    assert marginals["CNOT(0, 1)"] == {0: pytest.approx(0.5), 1: pytest.approx(0.5), 2: 0.0, 3: pytest.approx(1.0)}


def test_debugging_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch07-debug.png"
    assert debugging.draw(output) == output
    assert output.exists()


# -------------------------------------------------------------- half_adder


@pytest.mark.parametrize(("a", "b"), [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_half_adder_is_addition_modulo_two(a: int, b: int) -> None:
    assert half_adder.add(a, b) == (a + b) % 2


def test_half_adder_drops_the_carry_on_one_plus_one() -> None:
    assert half_adder.add(1, 1) == 0


def test_half_adder_truth_table_covers_every_input() -> None:
    assert half_adder.truth_table() == {(0, 0): 0, (0, 1): 1, (1, 0): 1, (1, 1): 0}


def test_half_adder_circuit_is_load_cnot_measure() -> None:
    names = [instruction.operation.name for instruction in half_adder.add_sum_circuit(1, 1).data]
    assert names == ["x", "x", "cx", "measure", "measure"]


def test_half_adder_circuit_loads_only_the_ones() -> None:
    names = [instruction.operation.name for instruction in half_adder.add_sum_circuit(1, 0).data]
    assert names.count("x") == 1


def test_half_adder_rejects_bad_inputs() -> None:
    with pytest.raises(ValueError, match="must be 0 or 1"):
        half_adder.add(2, 0)


def test_half_adder_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch07-add1.png"
    assert half_adder.draw(output) == output
    assert output.exists()


# -------------------------------------------------------------- full_adder


@pytest.mark.parametrize(("a", "b"), [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_full_adder_is_ordinary_addition(a: int, b: int) -> None:
    assert full_adder.add(a, b) == a + b


def test_full_adder_carries_only_on_one_plus_one() -> None:
    assert full_adder.carry(0, 0) == 0
    assert full_adder.carry(0, 1) == 0
    assert full_adder.carry(1, 0) == 0
    assert full_adder.carry(1, 1) == 1


def test_full_adder_one_plus_one_splits_into_sum_zero_and_carry_one() -> None:
    """q1 reads 0 (the sum) and q2 reads 1 (the carry) — the answer 1 + 1 = 2."""
    assert full_adder.add_bits(1, 1) == (0, 1)


def test_full_adder_truth_table_covers_every_input() -> None:
    assert full_adder.truth_table() == {
        (0, 0): (0, 0),
        (0, 1): (1, 0),
        (1, 0): (1, 0),
        (1, 1): (0, 1),
    }


def test_full_adder_circuit_is_toffoli_then_cnot() -> None:
    """The Toffoli must come first: the CNOT overwrites its second control."""
    names = [instruction.operation.name for instruction in full_adder.full_adder_circuit(1, 1).data]
    assert names == ["x", "x", "ccx", "cx", "measure", "measure", "measure"]


def test_toffoli_flips_the_target_only_when_both_controls_are_one() -> None:
    table = full_adder.toffoli_truth_table()
    assert set(table) == {format(value, "03b") for value in range(8)}
    flipped = {source for source, target in table.items() if source != target}
    assert flipped == {"110", "111"}
    assert table["110"] == "111"
    assert table["111"] == "110"


def test_toffoli_matrix_is_the_reversible_and() -> None:
    """The matrix is the identity except that it swaps |110> and |111>."""
    expected = np.eye(8, dtype=complex)
    expected[[6, 7]] = expected[[7, 6]]
    assert np.allclose(full_adder.TOFFOLI, expected)
    assert full_adder.TOFFOLI.shape == (8, 8)


def test_full_adder_rejects_bad_inputs() -> None:
    with pytest.raises(ValueError, match="must be 0 or 1"):
        full_adder.add(0, 3)


def test_full_adder_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch07-add2.png"
    assert full_adder.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------ package


def test_chapter_runs_all_four_samples_in_order() -> None:
    from quantum_computing_in_action import ch07

    assert (randombit, debugging, half_adder, full_adder) == ch07.SAMPLES
