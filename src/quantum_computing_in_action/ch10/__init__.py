"""Chapter 10 — Grover's search algorithm: a quadratic speed-up for a plain list.

The chapter follows the book's samples, from the motivation to the algorithm:

* :mod:`...ch10.search` — the ``classicsearch`` and ``quantumsearch`` samples: a
  small address book, a linear scan, and a Grover search over the same entries.
* :mod:`...ch10.oracle` — the ``groveroracle`` sample: the phase oracle that marks
  the answer with a sign.
* :mod:`...ch10.step_by_step` — the ``stepbystepgrover`` sample: two qubits, where
  the whole amplitude vector can be printed after every round.
* :mod:`...ch10.grover` — the ``grover`` sample: the general algorithm, its
  iteration count, and the rise-and-overshoot of the success probability.

:func:`main` runs all four in that order, which is what ``make ch10`` does. Run an
individual sample with, for example, ``python -m
quantum_computing_in_action.ch10.grover``.

The thread running through all four is that the oracle only flips a **sign**, and
that the diffusion operator turns signs into probabilities through interference —
a **quadratic** speed-up, and provably the best possible for an unstructured list.
"""

from __future__ import annotations

from quantum_computing_in_action.ch10 import grover, oracle, search, step_by_step
from quantum_computing_in_action.ch10.grover import (
    diffusion,
    grover_circuit,
    measured_counts,
    optimal_iterations,
    success_curve,
    success_probability,
)
from quantum_computing_in_action.ch10.oracle import (
    index_set,
    marked_label,
    oracle_matrix,
    phase_oracle,
)
from quantum_computing_in_action.ch10.search import (
    DATABASE,
    Person,
    classical_search,
    quantum_search,
    success_rate,
    tries_distribution,
)
from quantum_computing_in_action.ch10.step_by_step import round_distributions, round_states

#: The samples in the order the chapter builds them up.
SAMPLES = (search, oracle, step_by_step, grover)


def main() -> None:
    """Run every Chapter 10 sample in order, as ``make ch10`` does."""
    for sample in SAMPLES:
        sample.main()


__all__ = [
    "DATABASE",
    "SAMPLES",
    "Person",
    "classical_search",
    "diffusion",
    "grover",
    "grover_circuit",
    "index_set",
    "main",
    "marked_label",
    "measured_counts",
    "optimal_iterations",
    "oracle",
    "oracle_matrix",
    "phase_oracle",
    "quantum_search",
    "round_distributions",
    "round_states",
    "search",
    "step_by_step",
    "success_curve",
    "success_probability",
    "success_rate",
    "tries_distribution",
]
