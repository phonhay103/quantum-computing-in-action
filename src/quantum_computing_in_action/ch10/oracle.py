"""Chapter 10 — the Grover oracle: marking a state with a phase.

Grover's algorithm searches an unstructured list of ``N`` items in about
``(pi/4)*sqrt(N)`` steps. It does not "look at" the list; it asks an **oracle** a
question that can only be answered by *flipping the sign* of the item you want.

The oracle is the map

    U_w : |x>  -->  (-1)^[x == w] |x>

a **phase flip** on the marked state ``w`` and the identity on every other state.
It is a diagonal matrix with a ``-1`` where the answer is. That single sign is the
only thing Grover gets to work with: no amplitude changes, nothing measurable yet.
The next two modules turn that sign into a probability.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import ZGate
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_matrices
from quantum_computing_in_action.ch07.circuits import book_label


def index_set(marked: int | Iterable[int], n: int) -> tuple[int, ...]:
    """Normalise ``marked`` to a sorted tuple of valid basis indices for ``n`` qubits.

    Raises:
        ValueError: if any index is out of range for ``n`` qubits.
    """
    indices = (marked,) if isinstance(marked, int) else tuple(marked)
    if not indices:
        raise ValueError("at least one marked state is required")
    limit = 1 << n
    for index in indices:
        if not 0 <= index < limit:
            raise ValueError(f"marked index must be in [0, {limit}), got {index}")
    return tuple(sorted(set(indices)))


def marked_label(n: int, index: int) -> str:
    """Return the book-order label of basis state ``index`` (``q0`` leftmost)."""
    return book_label(format(index, f"0{n}b"))


def phase_oracle(n: int, marked: int | Iterable[int]) -> QuantumCircuit:
    """Return the phase oracle that flips the sign of the marked basis state(s).

    Built from an explicit multi-controlled ``Z``: bracket the all-ones state with
    ``X`` gates so a chosen basis state is the one that gets flipped. Unlike a raw
    diagonal gate, this keeps the **exact** sign of every amplitude — there is no
    stray global phase — which matters because the printed tables show it.

    Args:
        n: the number of qubits.
        marked: the index of the marked basis state, or several of them.
    """
    indices = index_set(marked, n)
    circuit = QuantumCircuit(n)
    for index in indices:
        _flip_sign_of(circuit, index, n)
    return circuit


def _flip_sign_of(circuit: QuantumCircuit, index: int, n: int) -> None:
    """Append the gates that flip the sign of basis state ``index`` and nothing else.

    Qiskit counts qubit ``q`` as bit ``q`` of the index, so an ``X`` goes on every
    qubit that is ``0`` in ``index``; then a ``Z`` controlled by all but the last
    qubit flips the phase of the all-ones state; then the ``X`` gates undo.
    """
    zeros = [qubit for qubit in range(n) if not (index >> qubit) & 1]
    if zeros:
        circuit.x(zeros)
    if n == 1:
        circuit.z(0)
    else:
        circuit.append(ZGate().control(n - 1, annotated=False), range(n))
    if zeros:
        circuit.x(zeros)


def oracle_matrix(n: int, marked: int | Iterable[int]) -> np.ndarray:
    """Return the oracle as a matrix in the book's basis order.

    The book writes a basis state ``q0 q1 ... q(n-1)``; Qiskit's index counts
    ``q0`` as the least-significant bit, so the marker sits at ``index`` in both
    and the diagonal is the same either way.
    """
    indices = set(index_set(marked, n))
    size = 1 << n
    return np.diag([-1.0 if index in indices else 1.0 for index in range(size)])


def draw(output: str | Path = "build/ch10-oracle-matrix.png") -> Path:
    """Render the two-qubit phase oracle as a matrix and save it to ``output``."""
    return render_matrices(
        [("phase oracle (n = 2, marked 11)", oracle_matrix(2, 3))],
        output,
        title="Grover's oracle: one sign flip, nothing measurable",
        figsize=(4.5, 4.2),
        fontsize=9.0,
    )


def _diagonal_table(n: int, marked: int) -> Table:
    table = Table(title="The oracle flips one sign and nothing else", header_style="heading")
    table.add_column("basis state", style="bits")
    table.add_column("index", style="muted")
    table.add_column("sign", style="value")
    for index in range(1 << n):
        sign = -1 if index == marked else 1
        table.add_row(marked_label(n, index), str(index), f"{sign:+d}")
    return table


def main() -> None:
    explain(
        "Chapter 10 — Grover's oracle",
        """
Grover's problem is **unstructured search**: a list of `N` items, exactly one of
which is the one you want, and no way to order the list so you can binary-search
it. Classically you look one item at a time, `N/2` on average. Grover needs about
`(pi/4) * sqrt(N)` lookups.

The algorithm never *sees* the list. All it gets is an **oracle** that recognises
the answer, and the only thing that oracle may do is *mark* it:

    U_w : |x>  -->  (-1)^[x == w] |x>

One sign flip on the marked state, the identity everywhere else. For two qubits,
with the state `|11>` marked, the oracle is the diagonal matrix below — a `-1` in
one place.

That sign is invisible on its own: a global phase means nothing, and a measurement
of `|x>` before and after the oracle returns the same histogram. Grover's job is
to turn this one hidden sign into a large probability, which is what *amplitude
amplification* (the next modules) does: the sign makes the marked state's amplitude
interfere with all the others, and the average shifts.
""",
    )

    steps(
        "Chapter 10 — marking a state",
        [
            ("Build the uniform superposition", "H on every qubit: all N states equal"),
            ("Ask the oracle", "one state flips sign, everything else is untouched"),
            ("Try to measure", "no change — a sign is not an amplitude"),
            ("Amplify", "the next module reflects about the average to make it visible"),
        ],
    )

    console.rule("One sign, for n = 2")
    console.print(_diagonal_table(2, 3))
    console.print(
        "[muted]The oracle is diagonal: it changes no amplitude, only the sign of the marked state. "
        "A measurement at this point cannot tell it apart from the identity.[/muted]"
    )

    path = draw()
    console.print("Saved diagrams:")
    console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
