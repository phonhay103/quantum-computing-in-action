"""Chapter 9 — reversible operations: the rule every oracle obeys.

The book's ``reversibleX`` sample applies an ``X`` gate twice and shows the qubit
come back untouched. It is the simplest possible reversible operation, and it is
worth stating plainly because the whole chapter depends on it:

**every quantum gate is reversible.** Whatever a gate does, you can undo it. That
is not a convention, it is a property of unitary matrices, and it rules out the
gates a classical circuit is built from.

An ``AND`` gate is the standard example of the problem. It takes two bits in and
returns one; ``00``, ``01`` and ``10`` all give ``0``, so the output does not say
which of them went in. Information is gone, and no circuit can bring it back.
Quantum circuits replace it with the **Toffoli** gate, which writes ``AND`` onto a
spare qubit and keeps both inputs — the reversible addition of Chapter 7.

So an "oracle" is not a function that can be called and forgotten. It is a
reversible circuit, and :mod:`...ch09.oracles` shows what that looks like.
"""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit


def double_x_circuit() -> QuantumCircuit:
    """Return ``X``, ``X`` on one qubit, with a measurement: always back to ``0``."""
    circuit = QuantumCircuit(1, 1)
    circuit.x(0)
    circuit.x(0)
    circuit.measure(0, 0)
    return circuit


def draw(output: str | Path = "build/ch09-reversible-circuit.png") -> Path:
    """Render the ``X``-then-``X`` circuit and save it to ``output``."""
    return render_circuit(double_x_circuit(), output)


def _and_table() -> Table:
    table = Table(title="A classical AND is not reversible", header_style="heading")
    table.add_column("a", style="bits")
    table.add_column("b", style="bits")
    table.add_column("a AND b", style="value")
    table.add_column("what the output hides", style="muted")
    table.add_row("0", "0", "0", "could have been 01 or 10")
    table.add_row("0", "1", "0", "could have been 00 or 10")
    table.add_row("1", "0", "0", "could have been 00 or 01")
    table.add_row("1", "1", "1", "")
    return table


def main() -> None:
    explain(
        "Chapter 9 — every gate is reversible",
        """
A quantum circuit is built from **reversible** gates: apply one, and you can always
apply its inverse to get back exactly what you had. The simplest example is an
`X` gate used twice.

    |0>  --X-->  |1>  --X-->  |0>

Two flips cancel. If the oracle of the next sections feels abstract, this is the
rule it is built to respect: *nothing may be erased*.

Classical logic breaks that rule everywhere. An `AND` takes two bits and returns
one:

    0 AND 0 = 0
    0 AND 1 = 0
    1 AND 0 = 0
    1 AND 1 = 1

Read the first three lines: three different inputs, the same output `0`. Once the
gate has run, the input is gone — you cannot invert it. `OR` has the same problem
in reverse.

A quantum circuit cannot use `AND` as a black box. It uses the **Toffoli** gate of
Chapter 7 instead, which writes `a AND b` onto a *third* qubit and leaves `a` and
`b` in place:

    Toffoli(a, b, 0)  ->  (a, b, a AND b)

Nothing is lost, so the gate is reversible. Every oracle in this chapter is built
the same way: evaluate the function, keep the input, and put the answer somewhere
new.
""",
    )

    steps(
        "Chapter 9 — reversibility, in two steps",
        [
            ("Apply X(0)", "|0> becomes |1> — a definite bit"),
            ("Apply X(0) again", "|1> becomes |0> — the first gate is undone exactly"),
        ],
    )

    console.rule("Two X gates are the identity")
    console.print("  [bits]X, X[/bits]  returns the qubit to |0> with certainty: nothing was erased.")
    console.print(
        "[muted]Contrast this with a classical AND, where three inputs share one output and the "
        "input can never be recovered. That is why quantum circuits use the Toffoli gate — the "
        "reversible AND of Chapter 7 — whenever they need one.[/muted]"
    )

    console.rule("Why AND cannot be an oracle")
    console.print(_and_table())

    circuit_path = draw()
    console.print("Saved diagrams:")
    console.print(f"  [path]{circuit_path}[/path]")


if __name__ == "__main__":
    main()
