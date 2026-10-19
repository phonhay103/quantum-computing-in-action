"""Chapter 8 — using superposition: a whole register in every state at once.

The book's ``superposition`` sample sits between the naive channel and BB84, and
it answers the obvious objection to the naive channel. Sending plain bits is
readable by everyone, so surely the fix is to put *everything* in superposition?
A four-qubit register can hold all sixteen basis states at once, after all.

It can, and that is what this sample shows — and then it shows why that is not
enough. Every qubit is Hadamarded, so the register is spread evenly over all
``2^4`` states, and then every qubit is Hadamarded **again**. Two Hadamards are
the identity (``H·H = I``), so the register collapses right back to the state it
was prepared in, and Bob receives Alice's bits **exactly**.

So superposition is real and usable — the register genuinely passes through all
sixteen states — but it does not hide anything, because Bob, who applies the
inverse, reads it perfectly. Making the bits *secret* still needs the element
BB84 adds: a base only Alice knows.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts
from quantum_computing_in_action.ch07.circuits import Builder, basis_state, probabilities, state_after

#: Four qubits: all sixteen basis states at once.
SIZE = 4

#: The bit string the diagram is drawn for, so the picture never changes.
EXAMPLE_BITS: tuple[int, ...] = (0, 1, 1, 0)

#: ``(label, Hadamard rounds)`` for each stage the sample prints.
STAGES: tuple[tuple[str, int], ...] = (
    ("prepared", 0),
    ("after one H (all 16 states)", 1),
    ("after two H (recovered)", 2),
)


@dataclass(frozen=True)
class Exchange:
    """One pass of the naive superposition channel.

    Attributes:
        alice_bits: the bits Alice prepared, one per qubit.
        bob_bits: the bits Bob measured after the second Hadamard round.
    """

    alice_bits: tuple[int, ...]
    bob_bits: tuple[int, ...]

    @property
    def matches(self) -> bool:
        """Whether Bob received the bits Alice sent."""
        return self.alice_bits == self.bob_bits

    @property
    def alice_string(self) -> str:
        """Alice's bits as a string, ``q0`` first."""
        return "".join(str(bit) for bit in self.alice_bits)

    @property
    def bob_string(self) -> str:
        """Bob's bits as a string, ``q0`` first."""
        return "".join(str(bit) for bit in self.bob_bits)


def _random_bits(size: int, seed: int | None) -> tuple[int, ...]:
    rng = np.random.default_rng(seed)
    return tuple(int(value) for value in rng.integers(0, 2, size=size))


def _builder(bits: Sequence[int], rounds: int) -> Builder:
    """Return the gates up to (not including) the measurement.

    ``rounds`` is how many Hadamard rounds to apply to every qubit: 0 for the
    prepared state, 1 for the superposition, 2 for the recovered state.
    """

    def build(circuit: QuantumCircuit) -> None:
        for qubit, bit in enumerate(bits):
            if bit:
                circuit.x(qubit)
        for _ in range(rounds):
            circuit.h(range(len(bits)))

    return build


def superposition_circuit(bits: Sequence[int], *, measure: bool = True) -> QuantumCircuit:
    """Return the sample's circuit: prepare, ``H`` on every qubit twice, measure.

    Args:
        bits: the bits Alice prepares, one per qubit.
        measure: append a measurement on every qubit.
    """
    width = len(bits)
    circuit = QuantumCircuit(width, width)
    _builder(bits, 2)(circuit)
    if measure:
        for qubit in range(width):
            circuit.measure(qubit, qubit)
    return circuit


def after_rounds(bits: Sequence[int], rounds: int) -> Statevector:
    """Return the state after ``rounds`` Hadamard rounds on every qubit."""
    return state_after(_builder(bits, rounds), len(bits))


def stage_distributions(bits: Sequence[int]) -> list[tuple[str, dict[str, float]]]:
    """Return the full probability vector after each of :data:`STAGES`.

    The labels are in the book's bit order, so ``q0`` is the leftmost character.
    """
    return [(label, probabilities(after_rounds(bits, rounds))) for label, rounds in STAGES]


def recover(bits: Sequence[int]) -> tuple[int, ...]:
    """Return the bits Bob reads after the two Hadamard rounds — always Alice's.

    The two rounds cancel, so the register ends in a single definite basis state;
    reading it off is both deterministic and free.
    """
    width = len(bits)
    label = basis_state(state_after(_builder(bits, 2), width))
    return tuple(int(character) for character in label)


def run(size: int = SIZE, *, seed: int | None = None) -> Exchange:
    """Run one pass of the sample: Alice prepares ``size`` bits, Bob reads them.

    Raises:
        ValueError: if ``size`` is less than 1.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    alice_bits = _random_bits(size, seed)
    return Exchange(alice_bits=alice_bits, bob_bits=recover(alice_bits))


def superposition_probability(bits: Sequence[int]) -> float:
    """Return the probability of each basis state after one Hadamard round.

    It is ``1 / 2^n`` — every state equally likely — which is what makes the
    register "in superposition" rather than in one definite state.
    """
    distribution = probabilities(after_rounds(bits, 1))
    return max(distribution.values())


def draw(output: str | Path = "build/ch08-superposition-circuit.png") -> Path:
    """Render the four-qubit superposition circuit and save it to ``output``."""
    return render_circuit(superposition_circuit(EXAMPLE_BITS), output)


def states_diagram(output: str | Path = "build/ch08-superposition-states.png") -> Path:
    """Render the register's distribution before and after the second Hadamard."""

    def clean(distribution: dict[str, float]) -> dict[str, float]:
        # Drop the float-noise entries (1e-16) so the chart has no stray bars.
        return {label: (0.0 if probability < 1e-9 else probability) for label, probability in distribution.items()}

    distributions = stage_distributions(EXAMPLE_BITS)
    return render_grouped_counts(
        [(distributions[1][0], clean(distributions[1][1])), (distributions[2][0], clean(distributions[2][1]))],
        output,
        title="A register in superposition, and the same register recovered",
        xlabel="basis state (q0 q1 q2 q3)",
        ylabel="probability",
        rotation=90.0,
        bar_labels=False,
    )


def main() -> None:
    explain(
        "Chapter 8 — using superposition",
        """
The naive channel of the previous section sends plain bits, and Bob reads every
one of them exactly — which means Eve does too. The obvious fix is to send the
bits *in superposition*: Hadamard every qubit and the four-qubit register sits in
all sixteen basis states at once, each with amplitude `1/4`.

That much is true, and it is worth seeing. What it does **not** do is hide
anything, and the reason is the rule from the top of the chapter: `H·H = I`.

    prepare     X on the qubits whose bit is 1
    H, H        every qubit Hadamarded, then Hadamarded again
    measure     Bob reads exactly what Alice prepared

The register really does pass through the full superposition — after the first
Hadamard round all sixteen states carry probability `1/16` — but the second round
undoes the first, so the state that reaches the measurement is the prepared one.
Bob, who knows to apply the inverse, reads Alice's bits perfectly.

So a superposition is not a secret. It is a *rotation*, and whoever knows how to
rotate back sees everything. That is exactly the gap BB84 fills: it makes the
rotation depend on a **base** that Alice chooses at random and only reveals after
the qubits are gone.
""",
    )

    steps(
        "Chapter 8 — superposition, and why it is not secrecy",
        [
            ("Prepare", "X on the qubits whose bit is 1 — a definite basis state"),
            ("H on all four qubits", "all 16 states at once, each with probability 1/16"),
            ("H on all four again", "H·H = I, so the register returns to the prepared state"),
            ("Measure", "Bob reads Alice's bits exactly — and so could Eve"),
        ],
    )

    console.rule("The register, stage by stage (bits 0110)")
    for label, distribution in stage_distributions(EXAMPLE_BITS):
        live = {state: probability for state, probability in distribution.items() if probability > 1e-9}
        if len(live) == 1:
            only, probability = next(iter(live.items()))
            summary = f"one state, {only}, with probability {probability:.2f}"
        else:
            summary = f"{len(live)} states, each with probability {1 / len(live):.4f}"
        console.print(f"  [bits]{label:<26}[/bits] {summary}")

    exchange = run(seed=3)
    console.print()
    console.print(
        f"  [bits]Alice sent[/bits] [value]{exchange.alice_string}[/value]   "
        f"[bits]Bob received[/bits] [value]{exchange.bob_string}[/value]   "
        f"[muted]identical: {exchange.matches}[/muted]"
    )
    console.print(
        "[muted]All sixteen states at once in the middle, the prepared bits at the end: two "
        "Hadamards are the identity, so the superposition is free to enter and free to leave.[/muted]"
    )

    circuit_path = draw()
    diagram_path = states_diagram()
    console.print("Saved diagrams:")
    for path in (circuit_path, diagram_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
