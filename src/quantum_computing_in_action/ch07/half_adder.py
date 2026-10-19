"""Chapter 7 — adding two qubits: a half-adder without a carry.

The book's ``add1`` sample (section 7.6.2). Prepare ``q0`` and ``q1`` to hold the
two input bits (an ``X`` for a ``1``), apply one ``CNOT(0, 1)``, and read the
target as the sum:

    0 + 0 = 0     0 + 1 = 1     1 + 0 = 1     1 + 1 = 0

The last line is the interesting one. ``CNOT`` flips ``q1`` exactly when ``q0``
is ``1``, which is addition **modulo 2**: ``1 + 1`` wraps to ``0``. There is no
carry here, so the circuit can only add single bits and loses the overflow — which
is what the next module, :mod:`...ch07.full_adder`, fixes with a ``Toffoli``.
"""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit
from quantum_computing_in_action.ch07.circuits import Builder, basis_state, state_after

#: A half-adder needs two qubits: the two inputs, the second doubling as the sum.
N_QUBITS = 2

#: The four inputs the truth table walks through.
INPUTS: tuple[tuple[int, int], ...] = ((0, 0), (0, 1), (1, 0), (1, 1))


def _check_bit(value: int, name: str) -> None:
    if value not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1, got {value!r}")


def _prepare(circuit: QuantumCircuit, a: int, b: int) -> None:
    """Load the input bits: an ``X`` on ``q0``/``q1`` for each ``1``."""
    if a:
        circuit.x(0)
    if b:
        circuit.x(1)


def add_sum_circuit(a: int, b: int, *, measure: bool = True) -> QuantumCircuit:
    """Return the half-adder circuit for inputs ``a`` and ``b``.

    Args:
        a: the first input bit, ``0`` or ``1``.
        b: the second input bit, ``0`` or ``1``.
        measure: append a measurement on both qubits (the state helpers want the
            bare circuit instead).

    Raises:
        ValueError: if either input is not ``0`` or ``1``.
    """
    _check_bit(a, "a")
    _check_bit(b, "b")
    circuit = QuantumCircuit(N_QUBITS, N_QUBITS)
    _prepare(circuit, a, b)
    circuit.cx(0, 1)
    if measure:
        for qubit in range(N_QUBITS):
            circuit.measure(qubit, qubit)
    return circuit


def add(a: int, b: int) -> int:
    """Return ``a + b`` **modulo 2**, the half-adder's sum bit.

    The addition happens on the qubits: the ``CNOT`` flips ``q1`` when ``q0`` is
    ``1``. There is no carry, so ``1 + 1`` comes back as ``0``. Reading the final
    state (rather than sampling it) keeps the answer exact.
    """
    _check_bit(a, "a")
    _check_bit(b, "b")
    return int(basis_state(state_after(_adder_builder(a, b), N_QUBITS))[1])


def truth_table() -> dict[tuple[int, int], int]:
    """Return ``{(a, b): sum}`` for all four inputs — the half-adder's table."""
    return {pair: add(*pair) for pair in INPUTS}


def _adder_builder(a: int, b: int) -> Builder:
    """Return a builder that loads ``a`` and ``b`` and applies the ``CNOT``."""

    def build(circuit: QuantumCircuit) -> None:
        _prepare(circuit, a, b)
        circuit.cx(0, 1)

    return build


def draw(output: str | Path = "build/ch07-add1-circuit.png") -> Path:
    """Render the ``1 + 1`` half-adder circuit and save it to ``output``.

    ``1 + 1`` is the case worth drawing: both inputs are set, and the answer comes
    back ``0`` because the circuit has nowhere to put the carry.
    """
    return render_circuit(add_sum_circuit(1, 1), output)


def _truth_table() -> Table:
    table = Table(title="Half-adder (CNOT only): sums modulo 2", header_style="heading")
    table.add_column("a", style="bits")
    table.add_column("b", style="bits")
    table.add_column("a + b (mod 2)", style="value")
    results = truth_table()
    for pair in INPUTS:
        table.add_row(str(pair[0]), str(pair[1]), str(results[pair]))
    return table


def main() -> None:
    explain(
        "Chapter 7 — adding two qubits",
        """
A classical circuit adds with gates like AND and OR. A quantum circuit cannot use
those directly, because every quantum gate must be **reversible** — you may never
erase a bit. The smallest arithmetic a quantum circuit can do is therefore a
`CNOT`, which flips its target exactly when its control is `1`.

That makes `q1` the **sum** of the two input bits, *modulo 2*:

    0 + 0 = 0     0 + 1 = 1     1 + 0 = 1     1 + 1 = 0

The first three lines are ordinary addition. The fourth is not: `1 + 1` wraps back
to `0`, because `CNOT` only ever flips the target between `0` and `1`. Nothing in
the circuit remembers that it carried. This circuit is a **half-adder**: correct
as long as you do not need the carry.

The next sample adds a third qubit and a `Toffoli` gate to keep that carry, and
`1 + 1` comes back as `2`.
""",
    )

    steps(
        "Chapter 7 — the half-adder, step by step",
        [
            ("Load the inputs", "an X on q0 and q1 for each 1; the example sets 1 + 1"),
            ("Apply CNOT(0, 1)", "q1 flips because q0 is 1: sum = a XOR b"),
            ("Measure q1", "1 + 1 reads 0 — the carry was dropped"),
        ],
    )

    console.rule("The truth table")
    console.print(_truth_table())
    console.print(
        "[muted]The sum is a XOR b. Read the last line twice: on a quantum circuit with no carry, 1 + 1 = 0.[/muted]"
    )

    circuit_path = draw()
    console.print("Saved diagrams:")
    console.print(f"  [path]{circuit_path}[/path]")


if __name__ == "__main__":
    main()
