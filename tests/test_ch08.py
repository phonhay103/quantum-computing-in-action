import numpy as np
import pytest

from quantum_computing_in_action.ch08 import attempts, bb84, identity, protocol, superposition
from quantum_computing_in_action.ch08.protocol import Run, X, Z

# ----------------------------------------------------------------- protocol


def test_base_names() -> None:
    assert protocol.base_name(Z) == "Z"
    assert protocol.base_name(X) == "X"


@pytest.mark.parametrize(("bit", "base"), [(0, Z), (1, Z), (0, X), (1, X)])
def test_prepare_circuit_uses_x_for_the_bit_and_h_for_the_base(bit: int, base: int) -> None:
    names = [instruction.operation.name for instruction in protocol.prepare_circuit(bit, base).data]
    assert ("x" in names) == bool(bit)
    assert ("h" in names) == (base == X)


def test_prepare_state_encodes_the_four_states() -> None:
    assert np.allclose(protocol.prepare_state(0, Z).data, [1, 0])
    assert np.allclose(protocol.prepare_state(1, Z).data, [0, 1])
    assert np.allclose(protocol.prepare_state(0, X).data, [1, 1] / np.sqrt(2))
    assert np.allclose(protocol.prepare_state(1, X).data, [1, -1] / np.sqrt(2))


def test_state_probabilities_agree_with_the_born_rule() -> None:
    """Same base: certain. Other base: a fair coin. The rule the model is built on."""
    assert protocol.state_probabilities(0, Z, Z) == {"0": pytest.approx(1.0)}
    assert protocol.state_probabilities(1, Z, Z) == {"1": pytest.approx(1.0)}
    for bit in (0, 1):
        mixed = protocol.state_probabilities(bit, Z, X)
        assert mixed == {"0": pytest.approx(0.5), "1": pytest.approx(0.5)}
        mixed_back = protocol.state_probabilities(bit, X, Z)
        assert mixed_back == {"0": pytest.approx(0.5), "1": pytest.approx(0.5)}


def test_measure_in_the_same_base_is_certain() -> None:
    rng = np.random.default_rng(0)
    for bit in (0, 1):
        for base in (Z, X):
            assert protocol.measure(bit, prepared_base=base, measured_base=base, rng=rng) == bit


def test_measure_in_the_other_base_is_a_fair_coin() -> None:
    rng = np.random.default_rng(1)
    outcomes = [protocol.measure(0, prepared_base=Z, measured_base=X, rng=rng) for _ in range(4000)]
    assert set(outcomes) == {0, 1}
    assert outcomes.count(1) / 4000 == pytest.approx(0.5, abs=0.05)


def test_run_rejects_bad_size() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        protocol.run(0)


def test_clean_run_keeps_the_keys_identical() -> None:
    run = protocol.run(64, seed=4)
    assert run.size == 64
    assert run.error_rate == 0.0
    assert run.alice_key == run.bob_key
    assert 0 < len(run.sifted) <= 64


def test_clean_run_sifts_about_half_the_qubits() -> None:
    run = protocol.run(400, seed=5)
    assert 150 < len(run.sifted) < 250


def test_run_is_reproducible() -> None:
    assert protocol.run(16, seed=7) == protocol.run(16, seed=7)


def test_eavesdropper_pushes_the_error_rate_to_a_quarter() -> None:
    rates = [protocol.run(400, seed=seed, eavesdropper=True).error_rate for seed in range(20)]
    assert np.mean(rates) == pytest.approx(0.25, abs=0.03)


def test_eavesdropper_records_her_own_bits() -> None:
    run = protocol.run(64, seed=6, eavesdropper=True)
    assert run.eve_bases is not None and run.eve_bits is not None
    assert len(run.eve_bases) == len(run.eve_bits) == 64


# ----------------------------------------------------------------- identity


def test_haha_circuit_is_x_then_two_hadamards_on_both_qubits() -> None:
    names = [instruction.operation.name for instruction in identity.haha_circuit().data]
    assert names == ["x", "h", "h", "h", "h", "measure", "measure"]


def test_two_hadamards_undo_themselves() -> None:
    """The state after the X is the state after the second pair of Hadamards."""
    states = identity.step_states()
    after_x = np.asarray(states[1][1].data)
    after_second_h = np.asarray(states[3][1].data)
    assert np.allclose(after_x, after_second_h)
    assert np.allclose(after_x, [0, 1, 0, 0])  # Qiskit order |q1 q0> = |01>: q0 = 1


def test_identity_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch08-haha.png"
    assert identity.draw(output) == output
    assert output.exists()


# ----------------------------------------------------------------- attempts


def test_naive_exchange_has_no_raw_errors() -> None:
    """Bob reads every bit — which is exactly why there is no secrecy."""
    run = attempts.naive_exchange(128, seed=3)
    assert run.raw_error_rate == 0.0


def test_blind_exchange_is_wrong_a_quarter_of_the_time() -> None:
    """Bob never learns Alice's base, so half the bits are measured wrong."""
    run = attempts.blind_exchange(800, seed=3)
    assert run.raw_error_rate == pytest.approx(0.25, abs=0.04)


def test_attempts_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch08-attempts.png"
    assert attempts.draw(output) == output
    assert output.exists()


# --------------------------------------------------------------------- bb84


def test_exchange_without_eve_has_matching_keys() -> None:
    run = bb84.exchange(64, seed=8)
    assert run.alice_key == run.bob_key
    assert run.error_rate == 0.0


def test_error_distribution_is_all_zeros_without_eve() -> None:
    distribution = bb84.error_distribution(size=16, runs=50, seed=9)
    assert set(distribution) == {0}


def test_error_distribution_spreads_out_with_eve() -> None:
    distribution = bb84.error_distribution(size=120, runs=50, seed=9, eavesdropper=True)
    assert 0 not in distribution or distribution.get(0, 0) < 10
    assert max(distribution) > 10


def test_mean_error_rate_separates_clean_from_tapped() -> None:
    clean = bb84.mean_error_rate(size=200, runs=10, seed=11)
    tapped = bb84.mean_error_rate(size=200, runs=10, seed=11, eavesdropper=True)
    assert clean == 0.0
    assert tapped == pytest.approx(0.25, abs=0.05)


def test_error_distribution_rejects_bad_runs() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        bb84.error_distribution(runs=0)


def test_bb84_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch08-bb84.png"
    assert bb84.draw(output) == output
    assert output.exists()


def test_bb84_circuit_prepares_and_measures_every_qubit() -> None:
    run = protocol.run(4, seed=1)
    names = [
        instruction.operation.name
        for instruction in protocol.bb84_circuit(run.alice_bits, run.alice_bases, run.bob_bases).data
    ]
    assert names.count("measure") == 4


# ---------------------------------------------------------- superposition


def test_superposition_circuit_matches_the_sample() -> None:
    """Prepare (X on the 1s), H on all four, H on all four, measure."""
    names = [instruction.operation.name for instruction in superposition.superposition_circuit((0, 1, 1, 0)).data]
    assert names == ["x", "x", "h", "h", "h", "h", "h", "h", "h", "h", "measure", "measure", "measure", "measure"]


def test_one_hadamard_round_spreads_the_register_over_all_sixteen_states() -> None:
    distribution = superposition.stage_distributions((0, 1, 1, 0))[1][1]
    assert len(distribution) == 16
    for probability in distribution.values():
        assert probability == pytest.approx(1 / 16)


def test_the_second_hadamard_round_recovers_the_prepared_state() -> None:
    """H·H = I, so the register ends in exactly the state Alice prepared."""
    stages = superposition.stage_distributions((0, 1, 1, 0))
    recovered = stages[2][1]
    assert recovered["0110"] == pytest.approx(1.0)
    # Every other state is empty up to floating-point noise.
    assert sum(p for label, p in recovered.items() if label != "0110") == pytest.approx(0.0, abs=1e-9)


@pytest.mark.parametrize("bits", [(0, 0, 0, 0), (1, 1, 1, 1), (0, 1, 0, 1), (1, 0, 0, 1)])
def test_bob_receives_alice_bits_exactly(bits: tuple[int, ...]) -> None:
    assert superposition.recover(bits) == bits


def test_superposition_run_is_deterministic_and_matches() -> None:
    exchange = superposition.run(size=6, seed=4)
    assert exchange.matches
    assert exchange.alice_string == exchange.bob_string
    assert superposition.run(size=6, seed=4) == exchange


def test_superposition_run_rejects_bad_size() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        superposition.run(0)


def test_superposition_probability_is_one_over_n() -> None:
    assert superposition.superposition_probability((1, 0, 1, 0)) == pytest.approx(1 / 16)


def test_superposition_draws_write_files(tmp_path) -> None:
    assert superposition.draw(tmp_path / "ch08-superposition-circuit.png").exists()
    assert superposition.states_diagram(tmp_path / "ch08-superposition-states.png").exists()


# ------------------------------------------------------------------ package


def test_chapter_runs_all_four_samples_in_order() -> None:
    from quantum_computing_in_action import ch08

    assert (identity, attempts, superposition, bb84) == ch08.SAMPLES


def test_run_dataclass_exposes_the_sift() -> None:
    run = Run(alice_bits=(0, 1), alice_bases=(Z, X), bob_bases=(Z, Z), bob_bits=(0, 0))
    assert run.sifted == (0,)
    assert run.alice_key == "0"
    assert run.bob_key == "0"
    assert run.error_rate == 0.0
    assert run.raw_error_rate == 0.5
