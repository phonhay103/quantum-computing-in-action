import numpy as np
import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_computing_in_action.ch06 import (
    cz_circuit,
    cz_counts,
    czmeasure,
    networking,
    protocol,
    repeater,
    teleportation,
)

# ---------------------------------------------------------------- networking


def test_send_byte_delivers_the_byte() -> None:
    assert networking.send_byte(0x8, port=0) == 0x8


@pytest.mark.parametrize("value", [0, 1, 127, 255])
def test_send_byte_round_trips_every_boundary(value: int) -> None:
    assert networking.send_byte(value, port=0) == value


@pytest.mark.parametrize("value", [-1, 256, 1000])
def test_send_byte_rejects_values_outside_a_byte(value: int) -> None:
    with pytest.raises(ValueError, match="single byte"):
        networking.send_byte(value, port=0)


def test_classic_copy_leaves_both_values_usable() -> None:
    for source in (True, False):
        assert networking.classic_copy(source) == source


def test_classical_copy_survives_writing_to_the_copy() -> None:
    source = True
    copy = networking.classic_copy(source)
    copy = not copy  # a real copy, changing it must not touch the source
    assert source is True
    assert copy is False


def test_clone_attempt_circuit_has_hadamard_and_cnot() -> None:
    names = [instruction.operation.name for instruction in networking.clone_attempt_circuit("+").data]
    assert names.count("h") == 1
    assert names.count("cx") == 1


@pytest.mark.parametrize("state", ["0", "1", "+", "-"])
def test_clone_attempt_keeps_basis_states_but_not_superpositions(state: str) -> None:
    """A CNOT copies a control qubit exactly, but only for basis states."""
    attempts = {attempt.state: attempt for attempt in networking.clone_attempts()}
    expected = 1.0 if state in ("0", "1") else 0.5
    assert attempts[state].cnot_copy == pytest.approx(expected)
    assert attempts[state].cnot_source == pytest.approx(expected)


def test_no_single_attempt_clones_every_state() -> None:
    """The heart of no-cloning: CNOT fails on superpositions, H,H on basis states."""
    for attempt in networking.clone_attempts():
        assert attempt.cnot_copy < 1.0 or attempt.fresh_copy < 1.0


def test_perfect_copy_is_the_only_row_with_unit_fidelity() -> None:
    for attempt in networking.clone_attempts():
        assert attempt.perfect_copy == (1.0, 1.0)


def test_clone_attempt_correlates_the_pair_instead_of_copying_it() -> None:
    """The attempt builds (|00> + |11>)/√2, so 01 and 10 must never appear."""
    counts = networking.clone_outcome_counts("+", shots=4000, seed=3)
    assert set(counts) == {"00", "11"}
    assert sum(counts.values()) == 4000


def test_a_real_clone_would_leave_the_two_qubits_independent() -> None:
    """Two independent copies give all four outcomes — what the attempt fails to do."""
    counts = networking.ideal_clone_counts("+", shots=4000, seed=3)
    assert set(counts) == {"00", "01", "10", "11"}
    for value in counts.values():
        assert 0.15 < value / 4000 < 0.35


def test_basis_states_clone_ideally_with_matching_outcomes() -> None:
    for state in ("0", "1"):
        assert networking.ideal_clone_counts(state, shots=100) == {f"{state}{state}": 100}


def test_clone_outcome_counts_rejects_unknown_state() -> None:
    with pytest.raises(ValueError, match="state must be one of"):
        networking.clone_outcome_counts("2")


def test_marginal_rejects_bad_qubit() -> None:
    with pytest.raises(ValueError, match="qubit must be 0 or 1"):
        networking.marginal(networking.clone_attempt_state("+"), 2)


def test_networking_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch06-clone.png"
    assert networking.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------- protocol


def test_measure_gives_each_basis_outcome_its_probability() -> None:
    frames = protocol.run([protocol.gate(lambda c: (c.h(0), c.h(1)), 2), protocol.measure(0, 1)], n_qubits=2)
    probabilities = protocol.probabilities(frames)
    assert set(probabilities) == {"00", "01", "10", "11"}
    assert all(value == pytest.approx(0.25) for value in probabilities.values())


def test_frame_weights_sum_to_one() -> None:
    frames = protocol.run([protocol.gate(lambda c: c.h(0), 1), protocol.measure(0)], n_qubits=1)
    assert sum(frame.weight for frame in frames) == pytest.approx(1.0)


def test_measure_drops_impossible_outcomes() -> None:
    """A basis state has only one non-zero branch."""
    frames = protocol.run([protocol.measure(0, 1)], n_qubits=2)
    assert len(frames) == 1
    assert frames[0].bits == "00"


def test_sample_counts_are_reproducible_and_sum_to_shots() -> None:
    frames = protocol.run([protocol.gate(lambda c: c.h(0), 1), protocol.measure(0)], n_qubits=1)
    first = protocol.sample_counts(frames, 500, seed=11)
    second = protocol.sample_counts(frames, 500, seed=11)
    assert first == second
    assert sum(first.values()) == 500


def test_sample_counts_rejects_bad_shots() -> None:
    frames = protocol.run([protocol.measure(0)], n_qubits=1)
    with pytest.raises(ValueError, match="at least 1"):
        protocol.sample_counts(frames, 0)


def test_sample_counts_requires_every_qubit_measured() -> None:
    frames = protocol.run([protocol.gate(lambda c: c.h(0), 2)], n_qubits=2)
    with pytest.raises(ValueError, match="every qubit must be measured"):
        protocol.sample_counts(frames, 10)


def test_measure_rejects_bad_arguments() -> None:
    with pytest.raises(ValueError, match="at least one qubit"):
        protocol.measure()
    with pytest.raises(ValueError, match="distinct qubits"):
        protocol.measure(0, 0)


def test_run_rejects_zero_qubits() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        protocol.run([], n_qubits=0)


def test_qubit_state_reads_the_right_amplitudes() -> None:
    """The reduced qubit must be picked out using the *measured* values of the others."""
    state = np.zeros(8, dtype=complex)
    state[0b110] = 1.0  # q2=1, q1=1, q0=0
    assert np.allclose(protocol.qubit_state(state, 2, 3, fixed={0: 0, 1: 1}), [0.0, 1.0])
    assert np.allclose(protocol.qubit_state(state, 1, 3, fixed={0: 0, 2: 1}), [0.0, 1.0])
    assert np.allclose(protocol.qubit_state(state, 0, 3, fixed={1: 1, 2: 1}), [1.0, 0.0])


def test_qubit_state_defaults_other_qubits_to_zero() -> None:
    state = np.zeros(8, dtype=complex)
    state[0b100] = 1.0  # q2=1, q1=0, q0=0 — the defaults apply
    assert np.allclose(protocol.qubit_state(state, 2, 3), [0.0, 1.0])


def test_qubit_state_rejects_bad_qubit_and_values() -> None:
    state = np.zeros(4, dtype=complex)
    with pytest.raises(ValueError, match="qubit must be in"):
        protocol.qubit_state(state, 5, 2)
    with pytest.raises(ValueError, match="must be known as 0 or 1"):
        protocol.qubit_state(state, 0, 2, fixed={1: 2})


def _reference_probabilities(circuit) -> dict[str, float]:
    """Return Qiskit's own measurement probabilities for a set of qubits."""
    return {label: float(value) for label, value in Statevector.from_instruction(circuit).probabilities_dict(qargs=[0, 1]).items()}


def test_branch_probabilities_agree_with_qiskit() -> None:
    """The frame simulator must reproduce Qiskit's probabilities exactly.

    Everything in chapter 6 rests on this: the protocol samples branch weights
    itself because ``Statevector`` cannot execute control flow, so the branch
    weights have to match what Qiskit would have reported.
    """
    for builder in (czmeasure.PREPARATIONS["hh"], czmeasure.PREPARATIONS["bell"]):
        circuit = QuantumCircuit(2)
        builder(circuit)
        expected = _reference_probabilities(circuit)
        frames = protocol.run([protocol.gate(builder, 2), protocol.measure(0, 1)], n_qubits=2)
        for label, value in protocol.probabilities(frames).items():
            assert value == pytest.approx(expected[label])


def test_branch_probabilities_agree_with_qiskit_for_the_teleport_prefix() -> None:
    """Same check at the point where teleportation does its mid-circuit measurement."""
    for state in ("|0>", "|1>", "|+>", "|->"):
        circuit = QuantumCircuit(3)
        teleportation.INPUT_STATES[state](circuit)
        circuit.h(2)
        circuit.cx(2, 1)
        circuit.cx(0, 1)
        circuit.h(0)
        expected = {
            label: float(value)
            for label, value in Statevector.from_instruction(circuit).probabilities_dict(qargs=[0, 1]).items()
        }
        program = teleportation.teleport_program(state)
        frames = protocol.run(program[:4], n_qubits=3)
        for label, value in protocol.probabilities(frames).items():
            assert value == pytest.approx(expected[label])


def test_corrected_state_reproduces_the_input_distribution_in_every_branch() -> None:
    """Whatever Alice measured, Bob's rebuilt qubit has the input's statistics.

    The expected values come from Qiskit on the *input* circuit, so this checks the
    whole protocol — spread, measure, correct — against the reference
    implementation rather than against itself.
    """
    for state in ("|0>", "|+>", "|->"):
        circuit = QuantumCircuit(1)
        teleportation.INPUT_STATES[state](circuit)
        expected = Statevector.from_instruction(circuit).probabilities()
        for outcome in teleportation.outcome_table(state):
            assert outcome.bob_prob_one == pytest.approx(float(expected[1]))


def test_conditional_gate_needs_the_bit_already_measured() -> None:
    operation = protocol.x_if(0, 0, 2)
    frames = protocol.run([], n_qubits=2)
    with pytest.raises(ValueError, match="has not been measured yet"):
        operation(frames)


# ------------------------------------------------------------------ czmeasure


def test_cz_circuit_is_h_then_cz_with_measurements() -> None:
    names = [instruction.operation.name for instruction in cz_circuit("h").data]
    assert names == ["h", "cz", "measure", "measure"]


def test_cz_counts_give_four_roughly_equal_outcomes() -> None:
    counts = cz_counts(4000, seed=4)
    assert set(counts) == {"00", "01", "10", "11"}
    assert sum(counts.values()) == 4000
    for value in counts.values():
        assert 0.15 < value / 4000 < 0.35


def test_bell_counts_still_only_give_matching_outcomes() -> None:
    """CZ adds a phase but must not add outcomes: the set stays {00, 11}."""
    counts = czmeasure.bell_counts(4000, seed=4)
    assert set(counts) == {"00", "11"}


def test_cz_changes_only_the_eleven_amplitude() -> None:
    """The gate's entire visible effect is one sign flip — on the entangled state."""
    effect = czmeasure.cz_effect("bell")
    assert effect["11"] == pytest.approx(2 * 1 / np.sqrt(2))
    for label in ("00", "01", "10"):
        assert effect[label] == pytest.approx(0.0)


def test_cz_is_inert_when_the_control_never_fires() -> None:
    """With only q0 in superposition, q1 stays |0> and CZ does nothing at all."""
    assert all(value == pytest.approx(0.0) for value in czmeasure.cz_effect("h").values())


def test_cz_entangles_two_superpositions_without_changing_probabilities() -> None:
    """The chapter's key result: a real change to the state that measurement misses."""
    plain = czmeasure._state_of("hh")
    gated = czmeasure.cz_statevector("hh")
    assert czmeasure.schmidt_rank(plain.data) == 1
    assert czmeasure.schmidt_rank(gated.data) == 2
    plain_probabilities = czmeasure.probabilities(plain)
    gated_probabilities = czmeasure.probabilities(gated)
    for label in czmeasure.BASIS_LABELS:
        assert gated_probabilities[label] == pytest.approx(plain_probabilities[label])


def test_entangled_and_product_states_are_indistinguishable_in_a_histogram() -> None:
    with_plain = czmeasure.plain_counts("hh", shots=1000, seed=3)
    with_cz = cz_counts(1000, seed=3)
    assert with_plain == with_cz  # same seed, same histogram, different state


def test_entanglement_rank_helper() -> None:
    assert czmeasure.entanglement_rank("hh", with_cz=False) == 1
    assert czmeasure.entanglement_rank("hh") == 2
    assert czmeasure.entanglement_rank("h", with_cz=False) == czmeasure.entanglement_rank("h") == 1
    assert czmeasure.entanglement_rank("bell") == 2


def test_cz_circuit_rejects_unknown_preparation() -> None:
    with pytest.raises(ValueError, match="preparation must be one of"):
        cz_circuit("nope")


def test_czmeasure_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch06-cz.png"
    assert czmeasure.draw(output) == output
    assert output.exists()


# -------------------------------------------------------------- teleportation


def test_teleport_circuit_has_the_expected_shape() -> None:
    names = [instruction.operation.name for instruction in teleportation.teleport_circuit("|0>").data]
    assert names.count("measure") == 3
    assert names.count("h") == 2
    assert names.count("cx") == 2
    # The classical corrections live inside control-flow blocks.
    assert any(instruction.operation.name == "if_else" for instruction in teleportation.teleport_circuit("|0>").data)


def test_alice_message_is_uniform_over_the_four_outcomes() -> None:
    for state in ("|0>", "|1>", "|+>", "|->"):
        weights = [outcome.weight for outcome in teleportation.outcome_table(state)]
        assert sum(weights) == pytest.approx(1.0)
        assert weights == pytest.approx([0.25] * 4)


@pytest.mark.parametrize("state", ["|0>", "|1>", "|+>", "|->"])
def test_every_message_reconstructs_the_state_exactly(state: str) -> None:
    """The protocol's whole point: Bob's qubit matches the input in every branch."""
    outcomes = teleportation.outcome_table(state)
    assert all(outcome.fidelity == pytest.approx(1.0) for outcome in outcomes)


def test_fidelity_by_message_is_one_for_every_message() -> None:
    for state in ("|0>", "|1>", "|+>", "|->"):
        by_message = teleportation.fidelity_by_message(state)
        assert set(by_message) == {"00", "01", "10", "11"}
        assert all(value == pytest.approx(0.25) for value in by_message.values())


def test_basis_states_arrive_as_basis_states() -> None:
    for state, expected in (("|0>", 0.0), ("|1>", 1.0)):
        outcomes = teleportation.outcome_table(state)
        assert all(outcome.bob_prob_one == pytest.approx(expected) for outcome in outcomes)


def test_superpositions_arrive_as_superpositions() -> None:
    for state in ("|+>", "|->"):
        outcomes = teleportation.outcome_table(state)
        assert all(outcome.bob_prob_one == pytest.approx(0.5) for outcome in outcomes)


def test_bob_cannot_measure_his_way_to_the_input() -> None:
    """Flipping an input's bit changes Bob's result, so the state is not copied."""
    zero = teleportation.bob_counts("|0>", 2000, seed=8)
    one = teleportation.bob_counts("|1>", 2000, seed=8)
    assert {bits[2] for bits in zero} == {"0"}
    assert {bits[2] for bits in one} == {"1"}
    # Alice's message is unaffected by the input, so both share the same prefixes.
    assert {bits[:2] for bits in zero} == {bits[:2] for bits in one}


def test_superposition_teleportation_produces_both_outcomes() -> None:
    counts = teleportation.bob_counts("|+>", 4000, seed=8)
    outcomes = [bits[2] for bits, count in counts.items() for _ in range(count)]
    assert set(outcomes) == {"0", "1"}
    assert outcomes.count("1") / 4000 == pytest.approx(0.5, abs=0.05)


def test_correction_table_covers_all_four_messages() -> None:
    assert set(teleportation.CORRECTIONS) == {(0, 0), (1, 0), (0, 1), (1, 1)}
    assert teleportation.CORRECTIONS[(0, 0)] == "I"
    assert teleportation.CORRECTIONS[(0, 1)] == "X"
    assert teleportation.CORRECTIONS[(1, 0)] == "Z"


def test_outcome_counts_only_uses_the_message_pair() -> None:
    counts = teleportation.outcome_counts("|0>", 2000, seed=9)
    assert set(counts) == {"00", "01", "10", "11"}
    assert sum(counts.values()) == 2000


@pytest.mark.parametrize("shots", [0, -1])
def test_teleport_counts_rejects_bad_shots(shots: int) -> None:
    with pytest.raises(ValueError, match="at least 1"):
        teleportation.bob_counts("|0>", shots)


def test_teleport_rejects_unknown_state() -> None:
    with pytest.raises(ValueError, match="state must be one of"):
        teleportation.teleport_circuit("|2>")


def test_bob_state_by_bits_rejects_unknown_branch() -> None:
    with pytest.raises(ValueError, match="no branch with bits"):
        teleportation.bob_state_by_bits("|0>", "2")


def test_teleport_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch06-teleport.png"
    assert teleportation.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------ repeater


def test_repeater_circuit_has_two_hops() -> None:
    names = [instruction.operation.name for instruction in repeater.repeater_circuit().data]
    assert names.count("measure") == 5
    assert names.count("cx") == 4
    assert names.count("if_else") == 4


@pytest.mark.parametrize("prob_one", [0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
def test_bob_reproduces_alices_statistics(prob_one: float) -> None:
    """The repeater's load-bearing claim, checked at the level of exact probabilities."""
    start = repeater.input_distribution(prob_one)
    delivered = repeater.bob_distribution(prob_one)
    assert delivered["1"] == pytest.approx(start["1"], abs=1e-9)
    assert delivered["0"] == pytest.approx(start["0"], abs=1e-9)


def test_the_state_survives_rather_than_being_collapsed_to_a_basis_state() -> None:
    """A collapsed state would show P(1) of 0 or 1; a relayed one keeps the mixture."""
    for prob_one in (0.2, 0.4, 0.6, 0.8):
        delivered = repeater.bob_distribution(prob_one)
        assert 0.0 < delivered["1"] < 1.0


def test_every_branch_delivers_the_same_state() -> None:
    """All sixteen combinations of the four classical bits rebuild one and the same qubit."""
    states = repeater.bob_states(0.4)
    assert len(states) == 16
    reference = states[0]
    for state in states[1:]:
        assert np.allclose(state, reference)


def test_bob_counts_match_the_starting_distribution() -> None:
    counts = repeater.bob_counts(0.4, shots=6000, seed=13)
    assert set(counts) == {"0", "1"}
    assert sum(counts.values()) == 6000
    assert counts["1"] / 6000 == pytest.approx(0.4, abs=0.04)


def test_record_counts_include_all_four_classical_bits() -> None:
    records = repeater.record_counts(0.4, shots=6000, seed=13)
    assert all(len(bits) == 5 for bits in records)
    # Alice's and the relay's bits both vary, so more than just two outcomes show up.
    assert len(records) > 2


def test_bob_counts_rejects_bad_shots_and_probability() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        repeater.bob_counts(0.4, 0)
    with pytest.raises(ValueError, match="at least 1"):
        repeater.record_counts(0.4, -1)
    with pytest.raises(ValueError, match="between 0 and 1"):
        repeater.repeater_circuit(1.5)


def test_repeater_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch06-repeater.png"
    assert repeater.draw(output) == output
    assert output.exists()


def test_chapter_runs_all_four_samples_in_order() -> None:
    from quantum_computing_in_action import ch06

    assert (networking, czmeasure, teleportation, repeater) == ch06.SAMPLES
