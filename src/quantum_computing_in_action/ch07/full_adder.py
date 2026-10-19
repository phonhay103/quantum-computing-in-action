"""Chapter 7 — adding two qubits *with* a carry: the Toffoli gate.

The book's ``add2`` sample (section 7.6.3). The half-adder of
:mod:`...ch07.half_adder` could not keep the overflow, so ``1 + 1`` read ``0``.
Adding a third qubit plus a **Toffoli** gate fixes that:

    Toffoli(0, 1, 2)   carry = q0 AND q1
    CNOT(0, 1)         sum   = q0 XOR q1

Now ``1 + 1 = 2``: the sum bit wraps to ``0`` exactly as before, and the new carry
qubit holds the ``1`` that used to be thrown away.

The Toffoli (``CCNOT``) is the three-qubit cousin of ``CNOT``: it flips its target
only when **both** controls are ``1``. That makes it the smallest circuit that can
compute a logical **AND**, and doing it into a fresh ``|0>`` target is why the
operation stays reversible — the two inputs are still there afterwards, which a
classical AND gate would have destroyed.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts, render_matrices
from quantum_computing_in_action.ch05.states import CNOT
from quantum_computing_in_action.ch05.states import X as PAULI_X
from quantum_computing_in_action.ch07 import half_adder
from quantum_computing_in_action.ch07.circuits import Builder, basis_state, state_after

#: Two input qubits plus one for the carry: the sum reuses ``q1``.
N_QUBITS = 3

#: The four inputs the truth table walks through.
INPUTS: tuple[tuple[int, int], ...] = ((0, 0), (0, 1), (1, 0), (1, 1))

#: The Toffoli gate as an 8x8 matrix in the book's basis order ``|q0 q1 q2>``.
#: It is the identity except that it swaps ``|110>`` and ``|111>`` — flipping the
#: target exactly when both controls are ``1``.
TOFFOLI: np.ndarray = np.eye(8, dtype=complex)
TOFFOLI[[6, 7]] = TOFFOLI[[7, 6]]


def _check_bit(value: int, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1, got {value!r}")


def _prepare(circuit: QuantumCircuit, a: int, b: int) -> None:
    """Load the input bits: an ``X`` on ``q0``/``q1`` for each ``1``."""
    if a:
        circuit.x(0)
    if b:
        circuit.x(1)


def _adder_builder(a: int, b: int) -> Builder:
    """Return a builder for the full adder on inputs ``a`` and ``b``.

    The ``Toffoli`` must run **before** the ``CNOT``: it needs the original ``q1``
    as its second control, and the ``CNOT`` is about to overwrite it.
    """

    def build(circuit: QuantumCircuit) -> None:
        _prepare(circuit, a, b)
        circuit.ccx(0, 1, 2)  # carry = a AND b
        circuit.cx(0, 1)  # sum = a XOR b

    return build


def full_adder_circuit(a: int, b: int, *, measure: bool = True) -> QuantumCircuit:
    """Return the full-adder circuit for inputs ``a`` and ``b``.

    Args:
        a: the first input bit, ``0`` or ``1``.
        b: the second input bit, ``0`` or ``1``.
        measure: append a measurement on all three qubits (the state helpers want
            the bare circuit instead).

    Raises:
        ValueError: if either input is not ``0`` or ``1``.
    """
    _check_bit(a, "a")
    _check_bit(b, "b")
    circuit = QuantumCircuit(N_QUBITS, N_QUBITS)
    _adder_builder(a, b)(circuit)
    if measure:
        for qubit in range(N_QUBITS):
            circuit.measure(qubit, qubit)
    return circuit


def add_bits(a: int, b: int) -> tuple[int, int]:
    """Return ``(sum bit, carry bit)`` for ``a + b``, read off the final state.

    ``q1`` holds the sum and ``q2`` the carry. Reading the definite basis state
    keeps the answer exact — no sampling, no seed.
    """
    _check_bit(a, "a")
    _check_bit(b, "b")
    label = basis_state(state_after(_adder_builder(a, b), N_QUBITS))
    return int(label[1]), int(label[2])


def add(a: int, b: int) -> int:
    """Return the ordinary integer ``a + b`` (``0``, ``1`` or ``2``)."""
    total, carry = add_bits(a, b)
    return total + (carry << 1)


def carry(a: int, b: int) -> int:
    """Return the carry bit of ``a + b`` — ``1`` only for ``1 + 1``."""
    return add_bits(a, b)[1]


def truth_table() -> dict[tuple[int, int], tuple[int, int]]:
    """Return ``{(a, b): (sum, carry)}`` for all four inputs."""
    return {pair: add_bits(*pair) for pair in INPUTS}


def toffoli_truth_table() -> dict[str, str]:
    """Return the Toffoli's truth table as ``{input: output}`` in ``q0 q1 q2`` order.

    Only ``110`` -> ``111`` and ``111`` -> ``110`` differ; every other input is
    left alone.
    """
    table: dict[str, str] = {}
    for value in range(8):
        bits = format(value, "03b")  # the bits are q0, q1, q2 from left to right
        q0, q1, q2 = (int(character) for character in bits)

        def build(circuit: QuantumCircuit, q0: int = q0, q1: int = q1, q2: int = q2) -> None:
            if q0:
                circuit.x(0)
            if q1:
                circuit.x(1)
            if q2:
                circuit.x(2)
            circuit.ccx(0, 1, 2)

        table[bits] = basis_state(state_after(build, N_QUBITS))
    return table


def draw(output: str | Path = "build/ch07-add2-circuit.png") -> Path:
    """Render the ``1 + 1`` full-adder circuit and save it to ``output``.

    ``1 + 1`` is the case the carry exists for: the ``Toffoli`` fires and ``q2``
    becomes ``1``.
    """
    return render_circuit(full_adder_circuit(1, 1), output)


def _toffoli_table() -> Table:
    table = Table(title="The Toffoli gate: flips the target when both controls are 1", header_style="heading")
    table.add_column("q0 q1 q2 in", style="classical")
    table.add_column("q0 q1 q2 out", style="bits")
    table.add_column("", style="muted")
    for source, target in toffoli_truth_table().items():
        table.add_row(source, target, "flipped" if source != target else "")
    return table


def _adder_table() -> Table:
    table = Table(title="Full adder: sum with a carry", header_style="heading")
    table.add_column("a", style="bits")
    table.add_column("b", style="bits")
    table.add_column("sum", style="value")
    table.add_column("carry", style="value")
    table.add_column("a + b", style="value")
    for pair in INPUTS:
        total, carry_bit = truth_table()[pair]
        table.add_row(str(pair[0]), str(pair[1]), str(total), str(carry_bit), str(add(*pair)))
    return table


def main() -> None:
    explain(
        "Chapter 7 — adding two qubits with a carry",
        """
The half-adder was correct only while the answer fit in one bit: `CNOT` computes
`a XOR b`, and `1 + 1` wraps to `0` because there is nowhere to put the carry.

Classical logic would fix this with an **AND** gate. Quantum circuits cannot use a
plain AND — it throws an input away, and every quantum gate has to be reversible.
The reversible stand-in is the **Toffoli** gate (also `CCNOT`): a three-qubit gate
that flips its target only when **both** controls are `1`.

Applied to `(a, b, 0)` the Toffoli leaves `a` and `b` untouched and writes
`a AND b` into the target:

    110 -> 111     111 -> 110     every other input unchanged

That target is the carry. Add the half-adder's `CNOT` for the sum and the circuit
computes a real addition:

    Toffoli(0, 1, 2)   q2 = q0 AND q1   (carry)
    CNOT(0, 1)         q1 = q0 XOR q1   (sum)

so `1 + 1 = 2` at last: the sum bit still wraps to `0`, and `q2` holds the `1` the
half-adder dropped. Nothing was erased, so the whole thing is reversible — which
is why a quantum adder is built from these gates and not from AND and OR.
""",
    )

    steps(
        "Chapter 7 — the full adder, step by step",
        [
            ("Load the inputs", "an X on q0 and q1 for each 1; the example sets 1 + 1"),
            ("Toffoli(0, 1, 2)", "both controls are 1, so q2 flips to 1: carry = a AND b"),
            ("CNOT(0, 1)", "q0 is 1, so q1 flips to 0: sum = a XOR b"),
            ("Measure", "q1 q2 reads 01, i.e. 1 + 1 = 2"),
        ],
    )

    console.rule("The gate that makes the carry possible")
    console.print(_toffoli_table())
    console.print(
        "[muted]Only the two inputs with both controls set change, and the target flips. That is "
        "a reversible AND: the inputs survive, the new bit is written on top of the target.[/muted]"
    )

    console.rule("The truth table")
    console.print(_adder_table())
    console.print(
        "[muted]Compare the ``a + b`` column with the half-adder: every line now agrees with "
        "ordinary arithmetic, because 1 + 1 finally has somewhere to put its carry.[/muted]"
    )

    circuit_path = draw()
    matrices_path = render_matrices(
        [("X (1 qubit)", PAULI_X), ("CNOT (2 qubits)", CNOT), ("Toffoli (3 qubits)", TOFFOLI)],
        "build/ch07-toffoli-matrices.png",
        title="From X to CNOT to Toffoli: each adds one control",
        figsize=(12, 4.6),
        fontsize=7.0,
    )
    comparison_path = render_grouped_counts(
        [
            ("half-adder (no carry)", {f"{a}+{b}": half_adder.add(a, b) for a, b in INPUTS}),
            ("full adder (with carry)", {f"{a}+{b}": add(a, b) for a, b in INPUTS}),
        ],
        "build/ch07-adder-comparison.png",
        title="1 + 1 = 0 without a carry, 2 with one",
        xlabel="input",
        ylabel="result",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, matrices_path, comparison_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
