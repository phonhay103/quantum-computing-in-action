"""Chapter 8 — secure communication: bases, sifting, and a detectable wiretap.

The chapter follows the book's samples in the order they build on each other:

* :mod:`...ch08.identity` — section 8.2: the Hadamard trick. ``H·H = I`` means a
  base can be entered and left again for free, which is what makes a base a
  choice worth hiding.
* :mod:`...ch08.attempts` — the two designs that fail: a plain bit channel (Bob
  reads everything — so does Eve) and a random base that is never reconciled
  (a quarter of the key comes out wrong).
* :mod:`...ch08.superposition` — section 8.3: putting the whole register in
  superposition. All ``2^n`` states at once in the middle, and ``H·H = I`` means
  the prepared bits come back untouched — so superposition is not secrecy.
* :mod:`...ch08.bb84` — the protocol itself: bases announced, bits kept where the
  bases agree, and an intercept-resend eavesdropper detected by a ~25% error
  rate.

:func:`main` runs all four in that order, which is what ``make ch08`` does. Run
an individual sample with, for example, ``python -m
quantum_computing_in_action.ch08.bb84``.

The thread running through all four is that a qubit carries a bit only relative
to a **base**, and that measuring in the wrong base leaves a trace an
eavesdropper cannot erase.
"""

from __future__ import annotations

from quantum_computing_in_action.ch08 import attempts, bb84, identity, protocol, superposition
from quantum_computing_in_action.ch08.attempts import (
    blind_exchange,
    naive_exchange,
)
from quantum_computing_in_action.ch08.bb84 import (
    error_distribution,
    exchange,
    mean_error_rate,
)
from quantum_computing_in_action.ch08.identity import haha_circuit, step_states
from quantum_computing_in_action.ch08.protocol import (
    BASES,
    Run,
    X,
    Z,
    base_name,
    bb84_circuit,
    measure,
    prepare_circuit,
    prepare_state,
    run,
    state_probabilities,
)
from quantum_computing_in_action.ch08.superposition import (
    Exchange,
    recover,
    superposition_circuit,
)

#: The samples in the order the chapter builds them up.
SAMPLES = (identity, attempts, superposition, bb84)


def main() -> None:
    """Run every Chapter 8 sample in order, as ``make ch08`` does."""
    for sample in SAMPLES:
        sample.main()


__all__ = [
    "BASES",
    "SAMPLES",
    "Exchange",
    "Run",
    "X",
    "Z",
    "attempts",
    "base_name",
    "bb84",
    "bb84_circuit",
    "blind_exchange",
    "error_distribution",
    "exchange",
    "haha_circuit",
    "identity",
    "main",
    "mean_error_rate",
    "measure",
    "naive_exchange",
    "prepare_circuit",
    "prepare_state",
    "protocol",
    "recover",
    "run",
    "state_probabilities",
    "step_states",
    "superposition",
    "superposition_circuit",
]
