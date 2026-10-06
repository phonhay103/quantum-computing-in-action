"""Chapter 6 — the quantum repeater: teleportation over a chain of nodes.

Section 6.5 of the book extends teleportation across a *number* of nodes. Alice
sends a qubit to Bob through a relay in the middle, and the relay plays the part
of both receiver and sender: it receives the state from Alice, then teleports it
on to Bob.

Qubit roles (five qubits, matching the book's ``repeater`` sample)
-----------------------------------------------------------------

============  =========================================================
``q0``        Alice's qubit — the state to be delivered.
``q1``,``q2`` Alice and the relay share one Bell pair.
``q3``,``q4`` The relay and Bob share another Bell pair.
============  =========================================================

The relay is the interesting part. It *measures* its qubits in step one, exactly
as Alice does, so it never holds the state as a clean quantum object in between.
What travels is not the state: it is the chain of **correlations** plus four
classical bits. The relay can do this because no-cloning stops it from simply
reading the state, but the same structure that makes teleportation work also lets
it pass the state along.

What to check
-------------

The book's sample initialises q0 to a mixed-looking probability and observes
that Bob's qubit has *the same* distribution. That is the load-bearing claim:
after two rounds of entangle-measure-correct, the state that arrives at q4 has
the statistics it started with at q0. :func:`input_distribution` and
:func:`bob_distribution` make that directly comparable.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts
from quantum_computing_in_action.ch06.protocol import (
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

#: How many qubits the chain needs: one at Alice, two per link.
QUBITS_PER_LINK = 2


def repeater_circuit(prob_one: float = 0.4) -> QuantumCircuit:
    """Return the five-qubit repeater circuit of the book's ``repeater`` sample.

    The state on q0 is prepared by a rotation with ``P(1) = prob_one``, standing
    in for the Java sample's ``program.initializeQubit(0, .4)``: Alice's qubit is
    *not* a clean basis state, which makes it obvious that the statistics at Bob
    really came from Alice.

    The corrections are wrapped in ``if_test`` blocks, as they would be in a real
    circuit. The numbers come from :mod:`...ch06.protocol`, because
    ``Statevector`` cannot run control flow.

    Args:
        prob_one: the probability that Alice's qubit starts in ``|1>``.

    Raises:
        ValueError: if ``prob_one`` is outside ``[0, 1]``.
    """
    _check_probability(prob_one)

    def build(circuit: QuantumCircuit) -> None:
        circuit.ry(_ry_angle(prob_one), 0)
        circuit.barrier(0)
        # Two Bell pairs: (q1, q2) for Alice->relay and (q3, q4) for relay->Bob.
        circuit.h(1)
        circuit.h(3)
        circuit.cx(1, 2)
        circuit.cx(3, 4)
        circuit.barrier()
        # Hop 1: Alice spreads q0 over q0 and q1, then measures both.
        circuit.cx(0, 1)
        circuit.h(0)
        circuit.measure(0, 0)
        circuit.measure(1, 1)
        # The relay corrects q2 with Alice's two bits.
        with circuit.if_test((circuit.clbits[1], 1)):
            circuit.x(2)
        with circuit.if_test((circuit.clbits[0], 1)):
            circuit.z(2)
        circuit.barrier()
        # Hop 2: the relay plays Alice, spreading q2 over q2 and q3.
        circuit.cx(2, 3)
        circuit.h(2)
        circuit.measure(2, 2)
        circuit.measure(3, 3)
        # Bob corrects q4 with the relay's two bits.
        with circuit.if_test((circuit.clbits[3], 1)):
            circuit.x(4)
        with circuit.if_test((circuit.clbits[2], 1)):
            circuit.z(4)
        circuit.measure(4, 4)

    circuit = QuantumCircuit(5, 5)
    build(circuit)
    return circuit


def _check_probability(prob_one: float) -> None:
    if not 0.0 <= prob_one <= 1.0:
        raise ValueError("prob_one must be between 0 and 1")


def _ry_angle(prob_one: float) -> float:
    """Return the ``RY`` angle that makes ``P(1) = prob_one``."""
    _check_probability(prob_one)
    return 2.0 * math.asin(math.sqrt(prob_one))


def repeater_program(prob_one: float = 0.4, *, final_measure: bool = True) -> Program:
    """Return the branch program for :func:`repeater_circuit`.

    Args:
        prob_one: Alice's starting probability of ``|1>``.
        final_measure: measure Bob's q4 at the end. Turn it off to inspect the
            delivered state before it is measured.
    """
    _check_probability(prob_one)
    program: Program = [
        gate(lambda circuit: circuit.ry(_ry_angle(prob_one), 0), 5),
        gate(_bell_pairs, 5),
        gate(_spread, 5),
        measure(0, 1),
        x_if(1, 2, 5),
        z_if(0, 2, 5),
        gate(_spread_relay, 5),
        measure(2, 3),
        x_if(3, 4, 5),
        z_if(2, 4, 5),
    ]
    if final_measure:
        program.append(measure(4))
    return program


def _bell_pairs(circuit: QuantumCircuit) -> None:
    """Prepare the two Bell pairs: (q1, q2) and (q3, q4)."""
    circuit.h(1)
    circuit.h(3)
    circuit.cx(1, 2)
    circuit.cx(3, 4)


def _spread(circuit: QuantumCircuit) -> None:
    """Alice's hop: entangle q0 with q1, then rotate q0."""
    circuit.cx(0, 1)
    circuit.h(0)


def _spread_relay(circuit: QuantumCircuit) -> None:
    """The relay's hop: entangle q2 with q3, then rotate q2."""
    circuit.cx(2, 3)
    circuit.h(2)


def corrected_frames(prob_one: float = 0.4) -> list[Frame]:
    """Run the chain up to (but not including) Bob's measurement.

    Each frame is one combination of Alice's two classical bits and the relay's
    two, with all four corrections already applied. ``bits`` holds just those
    four results; Bob's qubit holds the delivered state.
    """
    return run(repeater_program(prob_one, final_measure=False), n_qubits=5)


def repeater_frames(prob_one: float = 0.4) -> list[Frame]:
    """Run the whole chain, including Bob's measurement.

    ``bits`` is ``q0 q1 q2 q3 q4`` — Alice's two classical results, then the
    relay's two, then Bob's outcome.
    """
    return run(repeater_program(prob_one), n_qubits=5)


def bob_state(frame: Frame) -> np.ndarray:
    """Return Bob's reconstructed qubit for one branch of :func:`corrected_frames`.

    ``frame.bits`` holds the four measured values, which is what pins down which
    two amplitudes of the branch belong to q4.
    """
    return qubit_state(
        frame.state,
        qubit=4,
        n_qubits=5,
        fixed={index: int(frame.bits[index]) for index in range(4)},
    )


def bob_states(prob_one: float = 0.4) -> list[np.ndarray]:
    """Return Bob's reconstructed qubit for every branch of the chain.

    Each element is a normalised two-amplitude vector: what Bob's q4 holds once
    all four classical corrections are applied, *before* he measures. There is one
    element per combination of Alice's and the relay's measurement results.
    """
    return [bob_state(frame) for frame in corrected_frames(prob_one)]


def input_state(prob_one: float = 0.4) -> np.ndarray:
    """Return the two amplitudes of the single-qubit state Alice starts with."""
    circuit = QuantumCircuit(1)
    circuit.ry(_ry_angle(prob_one), 0)
    return np.asarray(Statevector.from_instruction(circuit).data)


def input_distribution(prob_one: float = 0.4) -> dict[str, float]:
    """Return ``{"0": P(0), "1": P(1)}`` for Alice's starting qubit."""
    amplitudes = input_state(prob_one)
    return {str(index): float(abs(amplitudes[index]) ** 2) for index in (0, 1)}


def bob_distribution(prob_one: float = 0.4) -> dict[str, float]:
    """Return ``{"0": P(0), "1": P(1)}`` measured from what Bob actually ends up with.

    The probabilities are accumulated over every branch of the chain and weighted
    by the probability of that branch, so this is a genuine measurement of the
    delivered qubit rather than a restatement of the input. Compare with
    :func:`input_distribution`: they match, which is the repeater's whole claim.
    """
    totals = {"0": 0.0, "1": 0.0}
    for frame in corrected_frames(prob_one):
        state = bob_state(frame)
        totals["0"] += frame.weight * float(abs(state[0]) ** 2)
        totals["1"] += frame.weight * float(abs(state[1]) ** 2)
    return totals


def bob_counts(prob_one: float = 0.4, shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Count only Bob's measurement outcomes, discarding the four classical bits."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    counts = sample_counts(repeater_frames(prob_one), shots, seed=seed)
    totals: dict[str, int] = {"0": 0, "1": 0}
    for bits, count in counts.items():
        totals[bits[4]] += count
    return totals


def record_counts(prob_one: float = 0.4, shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Count every five-bit record, i.e. Alice's bits, the relay's bits, Bob's bit."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    return sample_counts(repeater_frames(prob_one), shots, seed=seed)


def _consistency_rows(prob_one: float = 0.4) -> list[tuple[str, float, float]]:
    """Return ``(label, input probability, bob probability)`` for several inputs."""
    return [
        (f"P(1) = {value:.1f}", input_distribution(value)["1"], bob_distribution(value)["1"])
        for value in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
    ]


def draw(output: str | Path = "build/ch06-repeater-circuit.png", prob_one: float = 0.4) -> Path:
    """Render the repeater circuit and save it to ``output``."""
    return render_circuit(repeater_circuit(prob_one), output, reverse_bits=True)


def main() -> None:
    explain(
        "Chapter 6 — the quantum repeater",
        """
Teleportation moves a state across a link. A **repeater** chains several links
together so the state can cross a much longer distance, with a node in the middle
acting as both receiver and sender.

    Alice (q0) --- link 1 --- relay (q2) --- link 2 --- Bob (q4)
                     with q1                   with q3

The relay does *not* hold the state cleanly in between. In link 1 it **measures**
q2, exactly as Alice measures her own qubits, so it never possesses the state as
an undisturbed object. What moves down the chain is the *correlations* of the two
Bell pairs plus four classical bits: two from Alice, two from the relay.

To show the state really arrives intact, Alice starts with a qubit that is
**neither** |0> nor |1> — a rotation with P(1) = 0.4. If the protocol merely
forwarded classical bits, Bob could only ever see 0 or 1. Instead:

    Alice's qubit    P(1) = 0.40
    Bob's qubit      P(1) = 0.40   <- the statistics survived the trip

That is the repeater's claim, and it is exactly what the sample measures. Note
that the relay had to *measure* to forward, so the state was never in transit as
a copy — which is why this works even though copying is impossible.
""",
    )

    steps(
        "Chapter 6 — step by step",
        [
            ("Alice prepares q0", "a rotation with P(1) = 0.4 — not a basis state"),
            ("Two Bell pairs are shared", "(q1,q2) for the first hop, (q3,q4) for the second"),
            ("Alice measures q0 and q1", "she destroys her state and sends two classical bits"),
            ("The relay corrects q2", "q2 now holds the state; the relay plays Alice for link 2"),
            ("The relay measures q2 and q3", "two more classical bits go to Bob"),
            ("Bob corrects q4 and measures", "his qubit carries the statistics Alice started with"),
        ],
    )

    console.rule("The statistics survive the trip")
    table = Table(title="Alice's starting qubit vs. Bob's delivered qubit", header_style="heading")
    table.add_column("Alice's qubit", style="bits")
    table.add_column("P(1) at Alice", style="value")
    table.add_column("P(1) at Bob", style="value")
    table.add_column("difference", style="value")
    for label, p_input, p_bob in _consistency_rows():
        table.add_row(label, f"{p_input:.2f}", f"{p_bob:.2f}", f"{abs(p_input - p_bob):.4f}")
    console.print(table)
    console.print(
        "[muted]Bob's qubit reproduces Alice's probabilities for every input. The state was "
        "rebuilt twice on the way, and the statistics came through unchanged.[/muted]"
    )

    console.rule("Running the chain with P(1) = 0.4")
    bob = bob_counts(0.4, shots=4000, seed=13)
    total = sum(bob.values())
    console.print(
        "  [heading]Bob measured:[/heading] "
        f"[zero]0 = {bob.get('0', 0)}[/zero], "
        f"[one]1 = {bob.get('1', 0)}[/one] "
        f"[muted](expected P(1) = 0.40, got {bob.get('1', 0) / total:.3f})[/muted]"
    )
    console.print(
        "[muted]Neither qubit is ever a clean basis state, and Bob still sees a genuine "
        "mixture. That is the evidence that a state — not a bit — was relayed.[/muted]"
    )
    records = record_counts(0.4, shots=4000, seed=13)
    alice_bits = sum(count for bits, count in records.items() if bits[0:2] == "00")
    console.print(
        f"\n  [muted]{len(records)} distinct five-bit records appeared; Alice's message "
        f"'00' alone accounted for {alice_bits}/{total} runs. Four classical bits vary at "
        "random — and none of them changes what Bob ends up with.[/muted]"
    )

    console.print(
        "\n  [heading]What this means for a real network[/heading]\n"
        "  [muted]Distance is limited by loss, not by the speed of light: a state that "
        "decoheres cannot be repaired, because it cannot be copied first. A repeater "
        "does not amplify a weak signal the way a classical repeater does — it "
        "*recreates* the state at each node from shared entanglement plus a classical "
        "message. Chapter 8 turns the same idea into secure communication.[/muted]"
    )

    circuit_path = draw()
    consistency_path = render_grouped_counts(
        [
            (
                "at Alice (start)",
                {f"P(1) = {p_input:.1f}": round(1000 * (1 - p_input)) for _, p_input, _ in _consistency_rows()},
            ),
            (
                "at Bob (delivered)",
                {f"P(1) = {p_input:.1f}": round(1000 * (1 - p_bob)) for _, p_input, p_bob in _consistency_rows()},
            ),
        ],
        "build/ch06-repeater-consistency.png",
        title="The state arrives with the statistics it started with",
        xlabel="Alice's starting P(1)",
        ylabel="expected count of outcome 0 (of 1000)",
    )
    counts_path = render_grouped_counts(
        [
            ("Alice (expected)", {"0": 6000 * (1 - 0.4), "1": 6000 * 0.4}),
            ("Bob (measured)", {key: 6 * value for key, value in bob_counts(0.4, shots=6000, seed=13).items()}),
        ],
        "build/ch06-repeater-counts.png",
        title="P(1) = 0.4 sent through the relay: expected vs. measured",
        xlabel="measured bit",
        ylabel="count",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, consistency_path, counts_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
