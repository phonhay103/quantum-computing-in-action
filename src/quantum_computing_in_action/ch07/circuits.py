"""Chapter 7 — shared helpers for building circuits step by step.

Chapter 7 takes the one-line HelloWorld of Chapter 2 apart and shows the *program*
underneath: an ordered list of **steps**, each holding the gates that act at the
same time. The samples in this package (``randombit``, ``randombitdebug``,
``add1``, ``add2``) all describe a program that way, so the plumbing they share
lives here.

It also settles one question of bookkeeping that bites every multi-qubit sample.
Qiskit prints an outcome with the **highest** qubit index on the left (a four-qubit
key reads ``c3c2c1c0``); the book numbers its qubits ``q0 ... q3`` and reads them
the other way round, so ``q0`` should be the **leftmost** character.
:func:`book_label` reverses a Qiskit label — the same trick Chapter 6 used for its
two-qubit bases — and the rest of the module keeps the book's order throughout.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

#: A builder appends the gates of one *step* to a circuit. Multi-statement
#: builders return a tuple of results, so a ``lambda`` needs no braces.
Builder = Callable[[QuantumCircuit], None]

#: The label given to the state before any step has run.
START_LABEL = "start"


def book_label(label: str) -> str:
    """Reverse a Qiskit outcome label so qubit 0 is the leftmost character.

    Qiskit's key for a four-qubit outcome is ``c3c2c1c0``; the book (and these
    notes) write the same outcome ``q0 q1 q2 q3``. This is that mirror.
    """
    return label[::-1]


def state_after(builder: Builder, n_qubits: int) -> Statevector:
    """Return the state ``builder`` reaches from ``|0...0>`` on ``n_qubits``."""
    circuit = QuantumCircuit(n_qubits)
    builder(circuit)
    return Statevector.from_instruction(circuit)


def cumulative_states(
    steps: Sequence[tuple[str, Builder]],
    n_qubits: int,
) -> list[tuple[str, Statevector]]:
    """Return the state after each step, starting with the initial ``|0...0>``.

    ``steps`` is a sequence of ``(label, builder)`` pairs applied in order. The
    result has one entry more than ``steps``: the initial state under
    :data:`START_LABEL`, then one ``(label, state)`` per step. This is what the
    book's debugger draws after every gate.
    """
    circuit = QuantumCircuit(n_qubits)
    states = [(START_LABEL, Statevector.from_instruction(circuit))]
    for label, builder in steps:
        builder(circuit)
        states.append((label, Statevector.from_instruction(circuit)))
    return states


def probabilities(state: Statevector) -> dict[str, float]:
    """Return *every* basis-state probability, keyed with qubit 0 leftmost.

    Unlike Qiskit's ``Statevector.probabilities_dict`` this keeps the zero
    entries, so the result is the full probability vector the book's debugger
    shows, in the book's bit order.
    """
    width = state.num_qubits
    return {
        book_label(format(index, f"0{width}b")): float(abs(amplitude) ** 2)
        for index, amplitude in enumerate(state.data)
    }


def nonzero_probabilities(state: Statevector) -> dict[str, float]:
    """Like :func:`probabilities`, but only the basis states that can occur."""
    return {label: value for label, value in probabilities(state).items() if value > 1e-9}


def prob_one_per_qubit(state: Statevector) -> dict[int, float]:
    """Return ``P(qubit i = 1)`` for every qubit, keyed by plain index ``0..n-1``.

    This is the *marginal* of each qubit on its own: the probability it reads 1
    when measured, whatever the others do.
    """
    width = state.num_qubits
    marginal = dict.fromkeys(range(width), 0.0)
    for label, probability in probabilities(state).items():
        # ``label`` is q0 q1 ... qn, so qubit i sits at position i from the left.
        for qubit in range(width):
            if label[qubit] == "1":
                marginal[qubit] += probability
    return marginal


def sample_counts(state: Statevector, shots: int, *, seed: int | None = None) -> dict[str, int]:
    """Measure ``state`` ``shots`` times; the labels are in the book's bit order.

    Sampling from the exact probabilities keeps the result reproducible when a
    ``seed`` is given, which the tests rely on.
    """
    if shots < 1:
        raise ValueError("shots must be at least 1")
    rng = np.random.default_rng(seed)
    width = state.num_qubits
    distribution = np.abs(np.asarray(state.data, dtype=complex)) ** 2
    distribution = distribution / distribution.sum()
    counts: dict[str, int] = {}
    for outcome in rng.choice(len(distribution), size=shots, p=distribution):
        label = book_label(format(int(outcome), f"0{width}b"))
        counts[label] = counts.get(label, 0) + 1
    return counts


def basis_state(state: Statevector) -> str:
    """Return the book-order label of a definite basis state.

    Opting for a basis-state label rather than a sample makes the adders exact:
    after a ``CNOT`` or a ``Toffoli`` the state is one basis state with certainty,
    so reading it off is both deterministic and free.

    Raises:
        ValueError: if ``state`` is a superposition of more than one basis state.
    """
    significant = [index for index, amplitude in enumerate(state.data) if abs(amplitude) > 1e-9]
    if len(significant) != 1:
        raise ValueError("state is not a single basis state")
    return book_label(format(significant[0], f"0{state.num_qubits}b"))
