"""Chapter 9 — oracles: reversible black boxes for functions.

A quantum algorithm never sees the function it works on. It sees an **oracle**:
a reversible circuit that evaluates the function without erasing anything.

If the function is ``f(x)``, its oracle is the two-register map

    U_f : |x>|y>  -->  |x> |y XOR f(x)>

The input ``x`` comes back unchanged, and the answer is XOR-ed onto a spare
register ``y``. Feed ``y = |0>`` and the spare holds ``f(x)``; feed it ``|->`` and
the same operation becomes a *phase* kickback — that is the trick Deutsch and
Deutsch—Jozsa use.

The four one-bit functions divide into just two kinds:

* **constant** — ``f(0) = f(1)`` (always 0, or always 1);
* **balanced** — ``f(0) != f(1)`` (``f(x) = x``, or ``f(x) = NOT x``).

Classically, telling the two kinds apart on one bit needs two lookups; quantumly,
one query suffices, which is the whole point of the next two modules.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_matrices
from quantum_computing_in_action.ch07.circuits import Builder, basis_state


@dataclass(frozen=True)
class Oracle:
    """A one-bit function together with the circuit that computes it.

    Attributes:
        name: how the function is printed.
        f: the classical function, ``f(0)`` and ``f(1)``.
        build: appends the oracle's gates to a two-qubit circuit, ``q0 = x`` and
            ``q1 = y``.
    """

    name: str
    f: Callable[[int], int]
    build: Builder

    @property
    def constant(self) -> bool:
        """Whether the function gives the same answer on both inputs."""
        return self.f(0) == self.f(1)

    @property
    def balanced(self) -> bool:
        """Whether the function gives different answers on the two inputs."""
        return not self.constant

    def truth_table(self) -> dict[int, int]:
        """Return ``{x: f(x)}`` for the two one-bit inputs."""
        return {x: self.f(x) for x in (0, 1)}

    def matrix(self) -> np.ndarray:
        """Return the 4x4 unitary of the oracle in the book's basis order.

        The basis is ``|00>, |01>, |10>, |11>`` with the leftmost bit equal to
        ``x`` (qubit 0) and the rightmost to ``y`` (qubit 1), so the column index
        is ``2*x + y``.
        """
        matrix = np.zeros((4, 4), dtype=complex)
        for x in (0, 1):
            for y in (0, 1):
                source = 2 * x + y
                target = 2 * x + (y ^ self.f(x))
                matrix[target, source] = 1.0
        return matrix


def _constant_zero(circuit: QuantumCircuit) -> None:
    """``f(x) = 0``: the spare register is left alone."""


def _constant_one(circuit: QuantumCircuit) -> None:
    """``f(x) = 1``: flip the spare register unconditionally."""
    circuit.x(1)


def _balanced_identity(circuit: QuantumCircuit) -> None:
    """``f(x) = x``: flip the spare register when ``x`` is 1."""
    circuit.cx(0, 1)


def _balanced_negation(circuit: QuantumCircuit) -> None:
    """``f(x) = NOT x``: flip the spare register, then conditionally flip it back."""
    circuit.x(1)
    circuit.cx(0, 1)


#: The four one-bit functions, in the order the chapter introduces them.
ORACLES: tuple[Oracle, ...] = (
    Oracle("constant 0", lambda x: 0, _constant_zero),
    Oracle("constant 1", lambda x: 1, _constant_one),
    Oracle("balanced: f(x) = x", lambda x: x, _balanced_identity),
    Oracle("balanced: f(x) = NOT x", lambda x: 1 - x, _balanced_negation),
)


def oracle_circuit(oracle: Oracle, x: int = 0, y: int = 0, *, measure: bool = False) -> QuantumCircuit:
    """Return a two-qubit circuit that evaluates ``oracle`` on ``(x, y)``.

    Args:
        oracle: the oracle to apply.
        x: the input bit, loaded onto ``q0``.
        y: the spare register, loaded onto ``q1``.
        measure: append a measurement on both qubits.
    """
    circuit = QuantumCircuit(2, 2)
    if x:
        circuit.x(0)
    if y:
        circuit.x(1)
    oracle.build(circuit)
    if measure:
        circuit.measure(0, 0)
        circuit.measure(1, 1)
    return circuit


def apply(oracle: Oracle, x: int = 0, y: int = 0) -> tuple[int, int]:
    """Return ``(x, y XOR f(x))`` — the oracle's action on a basis input."""
    circuit = QuantumCircuit(2)
    if x:
        circuit.x(0)
    if y:
        circuit.x(1)
    oracle.build(circuit)
    label = basis_state(Statevector.from_instruction(circuit))
    return int(label[0]), int(label[1])


def dj_oracle(n: int, kind: str) -> QuantumCircuit:
    """Return an ``n``-bit oracle for Deutsch—Jozsa.

    ``n`` input qubits are followed by one ancilla at index ``n``. The three
    kinds are:

    * ``"constant0"`` — the identity (``f`` is always 0);
    * ``"constant1"`` — flip the ancilla (``f`` is always 1);
    * ``"balanced"`` — flip the ancilla once per set input bit, i.e. the parity of
      ``x`` (0 on exactly half of the inputs).

    Raises:
        ValueError: for an unknown ``kind`` or a non-positive ``n``.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if kind not in ("constant0", "constant1", "balanced"):
        raise ValueError(f"kind must be 'constant0', 'constant1' or 'balanced', got {kind!r}")
    circuit = QuantumCircuit(n + 1)
    if kind == "constant1":
        circuit.x(n)
    elif kind == "balanced":
        for qubit in range(n):
            circuit.cx(qubit, n)
    return circuit


def dj_oracles(n: int) -> tuple[tuple[str, QuantumCircuit], ...]:
    """Return the constant and balanced ``n``-bit oracles, named for printing."""
    return (
        ("constant 0", dj_oracle(n, "constant0")),
        ("constant 1", dj_oracle(n, "constant1")),
        ("balanced (parity)", dj_oracle(n, "balanced")),
    )


def draw(output: str | Path = "build/ch09-oracle-matrices.png") -> Path:
    """Render the four one-bit oracle matrices as heatmaps and save them."""
    return render_matrices(
        [(oracle.name, oracle.matrix()) for oracle in ORACLES],
        output,
        title="The four one-bit oracles: |x y> -> |x, y XOR f(x)>",
        figsize=(15, 4.2),
        fontsize=8.0,
    )


def draw_circuit(output: str | Path = "build/ch09-oracle-circuit.png") -> Path:
    """Render the balanced ``f(x) = x`` oracle circuit (a single ``CNOT``)."""
    oracle = next(item for item in ORACLES if item.name == "balanced: f(x) = x")
    return render_circuit(oracle_circuit(oracle), output)


def _truth_table() -> Table:
    table = Table(title="The four one-bit functions, and their oracles", header_style="heading")
    table.add_column("function", style="bits")
    table.add_column("f(0)", style="value")
    table.add_column("f(1)", style="value")
    table.add_column("kind", style="value")
    table.add_column("oracle circuit", style="muted")
    circuits = {
        "constant 0": "nothing",
        "constant 1": "X on y",
        "balanced: f(x) = x": "CNOT(x, y)",
        "balanced: f(x) = NOT x": "X on y, then CNOT(x, y)",
    }
    for oracle in ORACLES:
        table.add_row(
            oracle.name,
            str(oracle.f(0)),
            str(oracle.f(1)),
            "constant" if oracle.constant else "balanced",
            circuits[oracle.name],
        )
    return table


def main() -> None:
    explain(
        "Chapter 9 — oracles and the four one-bit functions",
        """
A quantum algorithm never looks at a function directly; it looks at an **oracle**, a
reversible circuit that evaluates the function and keeps its input. For a one-bit
`f` the oracle acts on two registers:

    U_f : |x>|y>  ->  |x> |y XOR f(x)>

The input `x` comes back untouched and the answer lands on the spare register `y`.
Set `y = 0` and the spare holds `f(x)`; set `y = 1` and it holds `NOT f(x)`. Either
way the input survives, so the operation is reversible and a legitimate quantum
gate.

There are only four functions of one bit, and they fall into two families:

* **constant** — `f(0) = f(1)`: the two functions `0` and `1`;
* **balanced** — `f(0) != f(1)`: the two functions `x` and `NOT x`.

Each family has a one-gate oracle. `f(x) = x` is a single `CNOT`, which is why the
balanced oracle is the one worth drawing. `f(x) = 1` is an `X` on the spare
register; `f(x) = 0` changes nothing at all. Those four circuits are what the
Deutsch algorithm is handed as a black box.
""",
    )

    steps(
        "Chapter 9 — building an oracle",
        [
            ("Choose a function", "one of the four one-bit functions"),
            ("Write down U_f", "|x y> -> |x, y XOR f(x)>: keep x, XOR the answer onto y"),
            ("Realise it with gates", "CNOT for f(x) = x, an X on y for f = 1"),
            ("Hand it over", "the algorithm sees only the circuit, never the function"),
        ],
    )

    console.rule("The four functions")
    console.print(_truth_table())
    console.print(
        "[muted]Two constant functions and two balanced ones. The oracle keeps x, so no information "
        "is lost — and the same four circuits drive both the Deutsch and Deutsch—Jozsa algorithms "
        "that follow.[/muted]"
    )

    matrices_path = draw()
    circuit_path = draw_circuit()
    console.print("Saved diagrams:")
    for path in (matrices_path, circuit_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
