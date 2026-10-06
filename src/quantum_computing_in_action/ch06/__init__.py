"""Chapter 6 — quantum networking: moving a state you cannot copy.

The chapter follows the book's four Java samples, in the order they build on each
other:

* :mod:`...ch06.networking` — section 6.2: a byte over a real TCP socket, then
  why the same trick is impossible for a qubit (the **no-cloning** theorem).
* :mod:`...ch06.czmeasure` — section 6.3: ``CZ`` changes a *phase*, which a
  computational-basis measurement cannot see (the Chapter 6 exercise).
* :mod:`...ch06.teleportation` — section 6.4: **quantum teleportation**, moving a
  state with two classical bits and no copy.
* :mod:`...ch06.repeater` — section 6.5: the **quantum repeater**, chaining
  teleportation over several nodes.

:func:`main` runs all four in that order, which is what ``make ch06`` does. Run an
individual sample with, for example, ``python -m
quantum_computing_in_action.ch06.teleportation``.

The thread running through all four is that a quantum network cannot copy a
packet and forward the copy — the way ordinary networking does — and has to
recreate the state at each node instead.

:class:`~quantum_computing_in_action.ch06.protocol.Frame` simulator
------------------------------------------------------------------

Teleportation and the repeater both need a **mid-circuit measurement** whose
result drives classical corrections. Qiskit's ``Statevector`` refuses circuits
containing control flow, so those samples run on a small branch simulator
(:mod:`...ch06.protocol`) that keeps one :class:`~...ch06.protocol.Frame` per
measurement outcome. The circuits the samples *draw* are ordinary Qiskit
circuits with ``if_test`` blocks, exactly as a user would write them.
"""

from __future__ import annotations

from quantum_computing_in_action.ch06 import czmeasure, networking, protocol, repeater, teleportation
from quantum_computing_in_action.ch06.czmeasure import bell_counts, cz_circuit, cz_counts, cz_statevector
from quantum_computing_in_action.ch06.networking import (
    classic_copy,
    clone_attempt_circuit,
    clone_attempts,
    clone_outcome_counts,
    ideal_clone_counts,
    send_byte,
)
from quantum_computing_in_action.ch06.repeater import (
    bob_counts as repeater_counts,
)
from quantum_computing_in_action.ch06.repeater import (
    bob_distribution,
    input_distribution,
    repeater_circuit,
)
from quantum_computing_in_action.ch06.teleportation import (
    bob_counts as teleport_counts,
)
from quantum_computing_in_action.ch06.teleportation import (
    fidelity_by_message,
    outcome_table,
    teleport_circuit,
)

#: The samples in the order the chapter builds them up.
SAMPLES = (networking, czmeasure, teleportation, repeater)


def main() -> None:
    """Run every Chapter 6 sample in order, as ``make ch06`` does.

    Each sample prints its own explanation, results and diagrams. They are run in
    the book's order because the later ones build on the earlier: no-cloning is
    why teleportation is needed, and teleportation is what the repeater repeats.
    """
    for sample in SAMPLES:
        sample.main()


__all__ = [
    "SAMPLES",
    "bell_counts",
    "bob_distribution",
    "classic_copy",
    "clone_attempt_circuit",
    "clone_attempts",
    "clone_outcome_counts",
    "cz_circuit",
    "cz_counts",
    "cz_statevector",
    "czmeasure",
    "fidelity_by_message",
    "ideal_clone_counts",
    "input_distribution",
    "main",
    "networking",
    "outcome_table",
    "protocol",
    "repeater",
    "repeater_circuit",
    "repeater_counts",
    "send_byte",
    "teleport_circuit",
    "teleport_counts",
    "teleportation",
]
