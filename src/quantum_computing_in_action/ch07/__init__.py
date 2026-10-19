"""Chapter 7 — our HelloWorld, explained: circuits built gate by gate.

Chapter 2 treated the HelloWorld program as a function call. Chapter 7 opens it
up, following the book's four samples in order:

* :mod:`...ch07.randombit` — section 7.5.1: the four-qubit program (``H``, ``X``,
  ``CNOT``) as an explicit list of **steps**, with the circuit drawn.
* :mod:`...ch07.debugging` — section 7.5.2: the same program with the state
  reported after *every* step, the job the book's probability gates did.
* :mod:`...ch07.half_adder` — section 7.6.2: a ``CNOT`` adds two bits **modulo 2**,
  so ``1 + 1`` wraps to ``0`` — no carry.
* :mod:`...ch07.full_adder` — section 7.6.3: a ``Toffoli`` supplies the carry, and
  ``1 + 1 = 2``.

:func:`main` runs all four in that order, which is what ``make ch07`` does. Run an
individual sample with, for example, ``python -m
quantum_computing_in_action.ch07.full_adder``.

The thread running through all four is that a circuit is nothing but an ordered
list of steps, and the state is one object you can inspect at any point along it.
"""

from __future__ import annotations

from quantum_computing_in_action.ch07 import debugging, full_adder, half_adder, randombit
from quantum_computing_in_action.ch07.circuits import (
    START_LABEL,
    Builder,
    basis_state,
    book_label,
    cumulative_states,
    nonzero_probabilities,
    prob_one_per_qubit,
    probabilities,
    sample_counts,
    state_after,
)
from quantum_computing_in_action.ch07.debugging import debug_circuit, step_marginals, step_probabilities
from quantum_computing_in_action.ch07.full_adder import (
    TOFFOLI,
    add_bits,
    carry,
    full_adder_circuit,
    toffoli_truth_table,
)
from quantum_computing_in_action.ch07.full_adder import (
    add as full_add,
)
from quantum_computing_in_action.ch07.full_adder import (
    truth_table as full_adder_truth_table,
)
from quantum_computing_in_action.ch07.half_adder import (
    add as half_add,
)
from quantum_computing_in_action.ch07.half_adder import (
    add_sum_circuit,
)
from quantum_computing_in_action.ch07.half_adder import (
    truth_table as half_adder_truth_table,
)
from quantum_computing_in_action.ch07.randombit import (
    N_QUBITS,
    STEPS,
    program_circuit,
    program_state,
    qubit_probabilities,
    random_bits,
    step_states,
)

#: The samples in the order the chapter builds them up.
SAMPLES = (randombit, debugging, half_adder, full_adder)


def main() -> None:
    """Run every Chapter 7 sample in order, as ``make ch07`` does.

    Each sample prints its own explanation, results and diagrams. They run in the
    book's order because the later ones build on the earlier: the half-adder
    explains why a carry is needed, and the full adder adds it.
    """
    for sample in SAMPLES:
        sample.main()


__all__ = [
    "N_QUBITS",
    "SAMPLES",
    "START_LABEL",
    "STEPS",
    "TOFFOLI",
    "Builder",
    "add_bits",
    "add_sum_circuit",
    "basis_state",
    "book_label",
    "carry",
    "cumulative_states",
    "debug_circuit",
    "debugging",
    "full_add",
    "full_adder",
    "full_adder_circuit",
    "full_adder_truth_table",
    "half_add",
    "half_adder",
    "half_adder_truth_table",
    "main",
    "nonzero_probabilities",
    "prob_one_per_qubit",
    "probabilities",
    "program_circuit",
    "program_state",
    "qubit_probabilities",
    "random_bits",
    "randombit",
    "sample_counts",
    "state_after",
    "step_marginals",
    "step_probabilities",
    "step_states",
    "toffoli_truth_table",
]
