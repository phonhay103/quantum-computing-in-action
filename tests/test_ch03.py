from quantum_computing_in_action.ch03 import draw, measure_pauli_x, pauli_x_circuit


def test_pauli_x_measures_one() -> None:
    assert measure_pauli_x() == 1


def test_pauli_x_circuit_has_x_gate() -> None:
    instructions = pauli_x_circuit().data
    assert any(instruction.operation.name == "x" for instruction in instructions)


def test_draw_writes_file(tmp_path) -> None:
    output = tmp_path / "pauli-x.png"
    assert draw(output=output) == output
    assert output.exists()
