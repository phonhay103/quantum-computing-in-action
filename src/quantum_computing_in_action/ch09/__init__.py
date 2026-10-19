"""Chapter 9 — the Deutsch—Jozsa algorithm: one query for any function that is constant or balanced.

The chapter follows the book's samples, from the rule that everything is built on
to the algorithm that uses it:

* :mod:`...ch09.reversible` — the ``reversibleX`` sample: every quantum gate is
  reversible (``X·X = I``), so an irreversible gate like ``AND`` cannot be used.
* :mod:`...ch09.oracles` — the ``oracle``, ``function`` and ``applyoracle``
  samples: the four one-bit functions, and their reversible circuits
  ``U_f : |x>|y> -> |x>|y XOR f(x)>``.
* :mod:`...ch09.deutsch` — the ``deutsch`` sample: one query tells a constant
  function from a balanced one.
* :mod:`...ch09.deutschjozsa` — the ``deutschjozsa`` sample: the same question for
  an ``n``-bit input, still in one query.

:func:`main` runs all four in that order, which is what ``make ch09`` does. Run an
individual sample with, for example, ``python -m
quantum_computing_in_action.ch09.deutschjozsa``.

The thread running through all four is **interference**: the oracle writes the
function's value into a *phase*, and Hadamards turn that phase into a bit you can
measure.
"""

from __future__ import annotations

from quantum_computing_in_action.ch09 import deutsch, deutschjozsa, oracles, reversible
from quantum_computing_in_action.ch09.deutsch import classify, deutsch_circuit, deutsch_result, prob_one
from quantum_computing_in_action.ch09.deutschjozsa import (
    all_zero_probability,
    classical_queries,
    dj_circuit,
    dj_outcome,
    is_constant,
)
from quantum_computing_in_action.ch09.oracles import (
    ORACLES,
    Oracle,
    apply,
    dj_oracle,
    dj_oracles,
    oracle_circuit,
)
from quantum_computing_in_action.ch09.reversible import double_x_circuit

#: The samples in the order the chapter builds them up.
SAMPLES = (reversible, oracles, deutsch, deutschjozsa)


def main() -> None:
    """Run every Chapter 9 sample in order, as ``make ch09`` does."""
    for sample in SAMPLES:
        sample.main()


__all__ = [
    "ORACLES",
    "SAMPLES",
    "Oracle",
    "all_zero_probability",
    "apply",
    "classical_queries",
    "classify",
    "deutsch",
    "deutsch_circuit",
    "deutsch_result",
    "deutschjozsa",
    "dj_circuit",
    "dj_oracle",
    "dj_oracles",
    "dj_outcome",
    "double_x_circuit",
    "is_constant",
    "main",
    "oracle_circuit",
    "oracles",
    "prob_one",
    "reversible",
]
