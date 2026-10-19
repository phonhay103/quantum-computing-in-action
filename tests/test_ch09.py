import numpy as np
import pytest

from quantum_computing_in_action.ch09 import deutsch, deutschjozsa, oracles, reversible
from quantum_computing_in_action.ch09.oracles import ORACLES, Oracle

# --------------------------------------------------------------- reversible


def test_double_x_is_x_then_x_then_measure() -> None:
    names = [instruction.operation.name for instruction in reversible.double_x_circuit().data]
    assert names == ["x", "x", "measure"]


def test_reversible_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch09-reversible.png"
    assert reversible.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------ oracles


def test_there_are_four_one_bit_functions() -> None:
    assert len(ORACLES) == 4
    assert [oracle.constant for oracle in ORACLES] == [True, True, False, False]
    assert [oracle.balanced for oracle in ORACLES] == [False, False, True, True]


@pytest.mark.parametrize("oracle", ORACLES, ids=[item.name for item in ORACLES])
def test_truth_table_matches_the_function(oracle: Oracle) -> None:
    assert oracle.truth_table() == {0: oracle.f(0), 1: oracle.f(1)}


@pytest.mark.parametrize("oracle", ORACLES, ids=[item.name for item in ORACLES])
@pytest.mark.parametrize("x", [0, 1])
def test_oracle_keeps_the_input_and_xors_the_answer_onto_the_spare(oracle: Oracle, x: int) -> None:
    assert oracles.apply(oracle, x, 0) == (x, oracle.f(x))
    assert oracles.apply(oracle, x, 1) == (x, 1 ^ oracle.f(x))


@pytest.mark.parametrize("oracle", ORACLES, ids=[item.name for item in ORACLES])
def test_oracle_matrix_is_a_permutation_matching_the_circuit(oracle: Oracle) -> None:
    matrix = oracle.matrix()
    assert matrix.shape == (4, 4)
    # Exactly one 1 per row and column: a permutation (hence reversible).
    assert np.allclose(matrix.sum(axis=0), 1.0)
    assert np.allclose(matrix.sum(axis=1), 1.0)
    for x in (0, 1):
        for y in (0, 1):
            assert matrix[2 * x + (y ^ oracle.f(x)), 2 * x + y] == pytest.approx(1.0)


def test_oracle_circuit_loads_both_registers() -> None:
    oracle = next(item for item in ORACLES if item.name == "balanced: f(x) = x")
    names = [instruction.operation.name for instruction in oracles.oracle_circuit(oracle, 1, 1, measure=True).data]
    assert names == ["x", "x", "cx", "measure", "measure"]


def test_constant_oracle_of_one_is_just_an_x_on_the_spare() -> None:
    oracle = next(item for item in ORACLES if item.name == "constant 1")
    names = [instruction.operation.name for instruction in oracles.oracle_circuit(oracle).data]
    assert names == ["x"]


def test_dj_oracle_validates_its_arguments() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        oracles.dj_oracle(0, "balanced")
    with pytest.raises(ValueError, match="kind must be"):
        oracles.dj_oracle(2, "nope")


def test_oracles_draw_writes_files(tmp_path) -> None:
    matrices = oracles.draw(tmp_path / "ch09-matrices.png")
    circuit = oracles.draw_circuit(tmp_path / "ch09-oracle.png")
    assert matrices.exists() and circuit.exists()


# ------------------------------------------------------------------ deutsch


@pytest.mark.parametrize("oracle", ORACLES, ids=[item.name for item in ORACLES])
def test_deutsch_classifies_every_function_in_one_query(oracle: Oracle) -> None:
    expected = 1 if oracle.balanced else 0
    assert deutsch.deutsch_result(oracle) == expected
    assert deutsch.classify(oracle) == ("balanced" if oracle.balanced else "constant")


@pytest.mark.parametrize("oracle", ORACLES, ids=[item.name for item in ORACLES])
def test_deutsch_probabilities_are_deterministic(oracle: Oracle) -> None:
    probability = deutsch.prob_one(oracle)
    assert probability == pytest.approx(1.0 if oracle.balanced else 0.0, abs=1e-9)


def test_deutsch_circuit_measures_only_the_answer_qubit() -> None:
    names = [instruction.operation.name for instruction in deutsch.deutsch_circuit(ORACLES[2]).data]
    assert names.count("measure") == 1
    assert names.count("h") == 3  # two on q0 (once before, once after), one on q1


def test_deutsch_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch09-deutsch.png"
    assert deutsch.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------- deutschjozsa


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_constant_oracles_always_return_all_zeros(n: int) -> None:
    for kind in ("constant0", "constant1"):
        assert deutschjozsa.all_zero_probability(n, kind) == pytest.approx(1.0, abs=1e-9)
        assert deutschjozsa.is_constant(n, kind)


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_balanced_oracles_never_return_all_zeros(n: int) -> None:
    assert deutschjozsa.all_zero_probability(n, "balanced") == pytest.approx(0.0, abs=1e-9)
    assert not deutschjozsa.is_constant(n, "balanced")


def test_dj_outcome_is_a_distribution() -> None:
    for kind in ("constant0", "constant1", "balanced"):
        outcome = deutschjozsa.dj_outcome(3, kind)
        assert sum(outcome.values()) == pytest.approx(1.0)
        assert all(len(label) == 3 for label in outcome)


def test_dj_reproduction_of_the_parity_function_lands_on_the_answer() -> None:
    """For a linear balanced f(x) = a.x, the input register measures exactly a."""
    # The parity oracle over n=3 corresponds to a = 111.
    outcome = deutschjozsa.dj_outcome(3, "balanced")
    assert outcome["111"] == pytest.approx(1.0, abs=1e-9)


def test_classical_queries_grow_exponentially() -> None:
    assert deutschjozsa.classical_queries(1) == 2
    assert deutschjozsa.classical_queries(2) == 3
    assert deutschjozsa.classical_queries(3) == 5
    assert deutschjozsa.classical_queries(10) == 2**9 + 1


def test_classical_queries_rejects_bad_width() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        deutschjozsa.classical_queries(0)


def test_dj_circuit_measures_the_input_register() -> None:
    names = [instruction.operation.name for instruction in deutschjozsa.dj_circuit(3, "balanced").data]
    assert names.count("measure") == 3


def test_dj_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "ch09-dj.png"
    assert deutschjozsa.draw(output) == output
    assert output.exists()


# ------------------------------------------------------------------ package


def test_chapter_runs_all_four_samples_in_order() -> None:
    from quantum_computing_in_action import ch09

    assert (reversible, oracles, deutsch, deutschjozsa) == ch09.SAMPLES
