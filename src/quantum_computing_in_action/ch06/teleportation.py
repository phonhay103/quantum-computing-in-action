"""Chapter 6 — quantum teleportation: moving a state without moving a particle.

Section 6.4 of the book sends a qubit from Alice to Bob. Because a qubit cannot
be copied (see :mod:`quantum_computing_in_action.ch06.networking`), the obvious
approach is impossible: Alice cannot read her qubit, and she cannot send a copy.
Teleportation gets around this by *destroying* the original and rebuilding an
identical state at the far end — with two classical bits riding alongside.

Qubit roles
-----------

The circuit uses three qubits, matching the book's ``teleport`` sample:

============  =========================================================
``q0``        Alice holds the state to send.
``q1``        Alice's half of a Bell pair she shares with Bob.
``q2``        Bob's half of that pair. The state ends up here.
============  =========================================================

The protocol
------------

1. Alice and Bob prepare the Bell pair (Chapter 5's ``H`` then ``CNOT``).
2. Alice entangles her state (q0) with her own half of the pair (q1), then
   applies ``H`` to q0. These two steps "spread" the state over both her qubits.
3. Alice measures **both** her qubits. That destroys q0 — and it is precisely
   this measurement that lets the state reappear at Bob's end.
4. She reads the two classical results and sends them to Bob over an ordinary
   channel.
5. Bob applies ``X`` and/or ``Z`` to q2 depending on those two bits. His qubit is
   now exactly the state Alice started with.

No faster-than-light communication is involved: step 4 is a classical message,
limited by the speed of light. The state never leaves the pair — it is the
*correlations* that are rebuilt, and the original qubit is gone either way.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts
from quantum_computing_in_action.ch06.protocol import (
    Builder,
    Frame,
    Program,
    gate,
    measure,
    qubit_state,
    run,
    sample_counts,
    x_if,
    z_if,
)

#: The single-qubit states Alice can try to send, keyed by a short label.
INPUT_STATES: dict[str, Builder] = {
    "|0>": lambda circuit: None,
    "|1>": lambda circuit: circuit.x(0),
    "|+>": lambda circuit: circuit.h(0),
    "|->": lambda circuit: (circuit.x(0), circuit.h(0)),
}

#: How the two classical bits map onto Bob's correction, in the order the
#: protocol measures them: ``(bit for q0, bit for q1)``.
CORRECTIONS: dict[tuple[int, int], str] = {
    (0, 0): "I",
    (1, 0): "Z",
    (0, 1): "X",
    (1, 1): "X then Z",
}


def _check_input(state: str) -> None:
    if state not in INPUT_STATES:
        raise ValueError(f"state must be one of {sorted(INPUT_STATES)}, got {state!r}")


def teleport_circuit(state: str = "|0>") -> QuantumCircuit:
    """Return the full teleportation circuit, measurements and corrections included.

    The corrections are wrapped in ``if_test`` blocks because they are conditioned
    on the classical bits — the circuit a real Qiskit user would write. The
    numeric results in this module come from :mod:`...ch06.protocol` instead,
    because ``Statevector`` cannot execute control flow.

    Args:
        state: which state Alice starts with; one of :data:`INPUT_STATES`.
    """
    _check_input(state)

    def build(circuit: QuantumCircuit) -> None:
        INPUT_STATES[state](circuit)
        circuit.barrier(0)
        # Alice and Bob share a Bell pair.
        circuit.h(2)
        circuit.cx(2, 1)
        # Alice entangles her state with her half, then rotates.
        circuit.cx(0, 1)
        circuit.h(0)
        # Alice measures both her qubits; this destroys q0.
        circuit.measure(0, 0)
        circuit.measure(1, 1)
        # Bob's corrections, driven by the classical results.
        with circuit.if_test((circuit.clbits[1], 1)):
            circuit.x(2)
        with circuit.if_test((circuit.clbits[0], 1)):
            circuit.z(2)
        circuit.measure(2, 2)

    circuit = QuantumCircuit(3, 3)
    build(circuit)
    return circuit


def teleport_program(state: str = "|0>") -> Program:
    """Return the branch program that reproduces :func:`teleport_circuit`.

    Each branch is one of Alice's four possible measurement outcomes, with Bob's
    correction already applied — which is the whole protocol in six steps.
    """
    _check_input(state)
    return [
        gate(INPUT_STATES[state], 3),
        gate(_bell_pair, 3),
        gate(_spread, 3),
        measure(0, 1),
        x_if(1, 2, 3),
        z_if(0, 2, 3),
        measure(2),
    ]


def _bell_pair(circuit: QuantumCircuit) -> None:
    """Prepare the Bell pair Alice shares with Bob: ``H`` on q2, ``CNOT`` into q1."""
    circuit.h(2)
    circuit.cx(2, 1)


def _spread(circuit: QuantumCircuit) -> None:
    """Alice's ``CNOT`` then ``H``: spread her state over both her qubits.

    Note the direction: ``cx(0, 1)`` makes **q0** the control and q1 the target,
    even though q0 is the qubit holding Alice's state. That ordering is what the
    following ``H`` expects; the other direction does not reconstruct the state.
    """
    circuit.cx(0, 1)
    circuit.h(0)


def corrected_frames(state: str = "|0>") -> list[Frame]:
    """Run the protocol up to (but not including) Bob's measurement.

    Each frame is one of Alice's four possible outcomes with Bob's correction
    already applied, so its ``bits`` hold just ``q0`` and ``q1``. This is the
    point in the protocol where Bob's qubit holds the reconstructed state, and it
    is where the state should be inspected — measuring it first would destroy it.
    """
    _check_input(state)
    program = teleport_program(state)
    return run(
        [
            *program[:-1],
        ],
        n_qubits=3,
    )


def teleport_frames(state: str = "|0>") -> list[Frame]:
    """Run the whole protocol, including Bob's measurement.

    Each frame's ``bits`` are ``q0`` then ``q1`` then ``q2``, i.e. Alice's two
    classical results followed by Bob's own measurement. All four Alice outcomes
    occur with equal weight, and within each branch Bob's result is certain.
    """
    return run(teleport_program(state), n_qubits=3)


def bob_state(frame: Frame) -> np.ndarray:
    """Return Bob's two amplitude vector for a branch of :func:`corrected_frames`.

    ``frame.bits`` gives the measured values of q0 and q1, which is what pins
    down which two amplitudes of the branch belong to Bob.
    """
    return qubit_state(
        frame.state,
        qubit=2,
        n_qubits=3,
        fixed={0: int(frame.bits[0]), 1: int(frame.bits[1])},
    )


def input_state(state: str = "|0>") -> np.ndarray:
    """Return the two amplitudes Alice wanted to send."""
    _check_input(state)
    circuit = QuantumCircuit(1)
    INPUT_STATES[state](circuit)
    return np.asarray(Statevector.from_instruction(circuit).data)


def bob_state_by_bits(state: str, bits: str) -> np.ndarray:
    """Return Bob's reconstructed qubit for the branch labelled by Alice's ``bits``."""
    for frame in corrected_frames(state):
        if frame.bits == bits:
            return bob_state(frame)
    raise ValueError(f"no branch with bits {bits!r}")


@dataclass(frozen=True)
class Outcome:
    """One branch of the protocol: Alice's message and what Bob ended up with.

    Attributes:
        bits: Alice's two classical bits, ``q0`` first then ``q1``.
        weight: the probability of this message, ``1/4`` for a well-behaved protocol.
        correction: the gate sequence Bob applies in response.
        bob_prob_one: ``P(1)`` when Bob measures his qubit. Exactly 0 or 1 for a
            basis state, and ``0.5`` for a superposition.
        fidelity: ``|<input|bob>|^2``. This is 1 in *every* branch — the protocol
            works whatever Alice happened to measure.
    """

    bits: str
    weight: float
    correction: str
    bob_prob_one: float
    fidelity: float


def outcome_table(state: str = "|0>") -> list[Outcome]:
    """Return one :class:`Outcome` per classical branch of the protocol.

    The fidelity is 1 in every row — that is the protocol working.
    """
    _check_input(state)
    original = input_state(state)
    outcomes: list[Outcome] = []
    for frame in corrected_frames(state):
        bit_q0, bit_q1 = int(frame.bits[0]), int(frame.bits[1])
        corrected = bob_state(frame)
        outcomes.append(
            Outcome(
                bits=frame.bits,
                weight=frame.weight,
                correction=CORRECTIONS[(bit_q0, bit_q1)],
                bob_prob_one=float(abs(corrected[1]) ** 2),
                fidelity=float(abs(np.vdot(original, corrected)) ** 2),
            )
        )
    return outcomes


def fidelity_by_message(state: str = "|0>") -> dict[str, float]:
    """Return Bob's fidelity with the input, keyed by Alice's two classical bits.

    Each key is the message Alice sends, so a constant 1.0 across the four keys
    is the claim that teleportation succeeds for *every* message.
    """
    _check_input(state)
    original = input_state(state)
    merged: dict[str, float] = {}
    for frame in corrected_frames(state):
        fidelity = float(abs(np.vdot(original, bob_state(frame))) ** 2)
        merged[frame.bits] = merged.get(frame.bits, 0.0) + frame.weight * fidelity
    return merged


def bob_counts(state: str = "|0>", shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Measure only Bob's qubit ``shots`` times, keyed by Alice's message pair.

    The three-bit key is ``q0 q1 q2``: Alice's two classical results followed by
    Bob's own measurement, so a flat histogram of the key shows both the message
    and the state that arrived with it.
    """
    if shots < 1:
        raise ValueError("shots must be at least 1")
    return sample_counts(teleport_frames(state), shots, seed=seed)


def outcome_counts(state: str = "|0>", shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Count Alice's message pairs, ignoring what Bob measured."""
    counts = bob_counts(state, shots, seed=seed)
    totals: dict[str, int] = {}
    for bits, count in counts.items():
        totals[bits[:2]] = totals.get(bits[:2], 0) + count
    return totals


def _format_state(vector: np.ndarray) -> str:
    """Render a two-amplitude state compactly for a table cell.

    Basis states become ``|0>`` / ``|1>``; anything else is shown as the pair of
    amplitudes, which is what makes a *phase* visible where a probability is not.
    """
    amplitude_zero, amplitude_one = complex(vector[0]), complex(vector[1])
    if abs(amplitude_one) < 1e-9:
        return "|0>"
    if abs(amplitude_zero) < 1e-9:
        return "|1>"
    return f"({amplitude_zero:+.3f} |0> {amplitude_one:+.3f} |1>)"


def draw(output: str | Path = "build/ch06-teleport-circuit.png", state: str = "|0>") -> Path:
    """Render the teleportation circuit and save it to ``output``."""
    return render_circuit(teleport_circuit(state), output, reverse_bits=True)


def main() -> None:
    explain(
        "Chapter 6 — quantum teleportation",
        """
Chapter 6 showed that you cannot copy a qubit. So how does Alice get her state
to Bob at all?

**Teleportation.** She cannot read q0 — and she cannot send a copy. What she
*can* do is destroy q0 and rebuild an identical state at Bob's end, using
correlations they already share:

    Alice has q0 (the state) and q1; Bob has q2.
    q1 and q2 start as a Bell pair.

    1. H(2), CX(2,1)   Alice and Bob share an entangled pair
    2. CX(0,1), H(0)   Alice entangles her state with her own half
    3. measure q0, q1  Alice reads two classical bits — and destroys q0
    4. -> Bob         ...over an ordinary channel, at light speed
    5. X if q1=1; Z if q0=1   Bob corrects his qubit into exactly |psi>

Bob ends up holding the state Alice started with, to the last amplitude. For
`|0>` he is certain to measure `0`; for `|+>` he is 50/50 — just as if he had
made it himself.

Two things to keep straight:

* **The qubit never moved.** Alice's q0 was measured and destroyed; Bob rebuilds
  a *new* qubit that happens to be in the same state. Compare with the byte over
  the socket in the first sample: there the original survived.
* **No faster-than-light signalling.** Step 4 is an ordinary classical message.
  The state cannot be reconstructed without it — that is the "2 classical bits"
  in the name of the protocol.
""",
    )

    zero = outcome_table("|0>")

    steps(
        "Chapter 6 — step by step",
        [
            ("Alice and Bob share a Bell pair", "q1 and q2 are entangled: ( |00> + |11> ) / √2"),
            ("Alice applies CNOT then H", "the state of q0 is now spread over q0 and q1"),
            ("Alice measures q0 and q1", "two classical bits; q0 is destroyed — that is the point"),
            ("She sends the two bits to Bob", "an ordinary message, limited by light speed"),
            ("Bob applies X and/or Z", "his qubit becomes exactly the state Alice started with"),
        ],
    )

    console.rule("Every branch reconstructs the state")
    table = Table(title="Sending |0>: Alice's 4 messages, Bob's correction, Bob's result", header_style="heading")
    table.add_column("q0 q1 (message)", style="bits")
    table.add_column("probability", style="value")
    table.add_column("Bob applies", style="classical")
    table.add_column("Bob's qubit", style="value")
    table.add_column("fidelity with |0>", style="value")
    for outcome in zero:
        table.add_row(
            outcome.bits,
            f"{outcome.weight:.2f}",
            outcome.correction,
            _format_state(bob_state_by_bits("|0>", outcome.bits)),
            f"{outcome.fidelity:.3f}",
        )
    console.print(table)
    console.print(
        "[muted]All four messages are equally likely and all four reconstruct |0> exactly. "
        "The correction is what makes the result independent of the message.[/muted]"
    )

    console.rule("It works for superpositions too")
    comparison = Table(title="Bob's qubit for each state Alice sends", header_style="heading")
    comparison.add_column("Alice sends", style="bits")
    comparison.add_column("Bob's measured distribution", style="value")
    comparison.add_column("fidelity", style="value")
    for label in INPUT_STATES:
        outcomes = outcome_table(label)
        total = sum(outcome.weight for outcome in outcomes)
        ones = sum(outcome.weight * outcome.bob_prob_one for outcome in outcomes) / total
        fidelity = sum(outcome.weight * outcome.fidelity for outcome in outcomes) / total
        comparison.add_row(label, f"P(0) = {1 - ones:.2f}, P(1) = {ones:.2f}", f"{fidelity:.3f}")
    console.print(comparison)
    console.print(
        "[muted]|0> arrives as |0>, |1> as |1>, |+> as |+> — down to the amplitudes, and "
        "whatever phase they carry. Bob could not have prepared |+> from |0> by himself; "
        "he can only get it by rebuilding a state that already existed elsewhere.[/muted]"
    )

    console.rule("Running the protocol")
    for label in ("|0>", "|1>", "|+>"):
        counts = bob_counts(label, shots=1000, seed=5)
        summary = ", ".join(f"{bits[:2]}->{bits[2]}: {count}" for bits, count in sorted(counts.items()))
        console.print(f"  [heading]{label:>4}[/heading]  {summary}")
    console.print("[muted]Each three-bit key reads q0 q1 (Alice's message) then q2 (Bob's result).[/muted]")

    circuit_path = draw()
    outcome_path = render_grouped_counts(
        [
            ("|0> sent", bob_counts("|0>", 1000, seed=6)),
            ("|1> sent", bob_counts("|1>", 1000, seed=6)),
            ("|+> sent", bob_counts("|+>", 1000, seed=6)),
        ],
        "build/ch06-teleport-outcomes.png",
        title="Teleportation: Bob's result for each state Alice sends",
        xlabel="q0 q1 (message) then q2 (Bob)",
        ylabel="count",
    )
    fidelity_path = render_grouped_counts(
        [
            ("|0>", fidelity_by_message("|0>")),
            ("|1>", fidelity_by_message("|1>")),
            ("|+>", fidelity_by_message("|+>")),
        ],
        "build/ch06-teleport-fidelity.png",
        title="Every message reconstructs the state exactly",
        xlabel="Alice's two classical bits",
        ylabel="fidelity |<in|bob>|^2",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, outcome_path, fidelity_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
