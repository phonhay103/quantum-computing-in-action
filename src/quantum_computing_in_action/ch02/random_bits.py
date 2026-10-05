"""Chapter 2 — "Hello World", quantum computing style: random bits."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_computing_in_action._console import console, explain


def random_bit_circuit() -> QuantumCircuit:
    """A one-qubit circuit that puts the qubit in superposition and measures it.

    Applying a Hadamard gate to ``|0>`` yields ``(|0> + |1>) / sqrt(2)``, so a
    measurement returns ``0`` or ``1`` with equal probability.
    """
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    circuit.measure(0, 0)
    return circuit


def _sampled_counts(circuit: QuantumCircuit, shots: int) -> dict[str, int]:
    circuit.remove_final_measurements(inplace=True)
    state = Statevector.from_instruction(circuit)
    return {str(bit): int(count) for bit, count in state.sample_counts(shots).items()}


def random_bits(count: int = 1) -> list[int]:
    """Return ``count`` random bits produced by the quantum circuit."""
    if count < 1:
        raise ValueError("count must be at least 1")
    counts = _sampled_counts(random_bit_circuit(), count)
    return [0] * counts.get("0", 0) + [1] * counts.get("1", 0)


def random_bit() -> int:
    """Return a single random bit (``0`` or ``1``)."""
    return random_bits(1)[0]


def main() -> None:
    explain(
        "Chapter 2 — Random bits from a qubit",
        """
A qubit starts in state `|0>`. A **Hadamard gate** (`H`) puts it into an equal
superposition of `|0>` and `|1>`:

`H|0> = (|0> + |1>) / sqrt(2)`

Measuring collapses that superposition, giving `0` or `1` with a 50% chance.
Unlike a normal `random()` function, the outcome is not determined by a hidden
seed — it is genuinely random.
""",
    )

    console.rule("Using Qiskit to generate random bits")
    console.print(f"Generate one random bit, which can be 0 or 1. Result = [value]{random_bit()}[/value]")
    bits = random_bits(10000)
    zeros = bits.count(0)
    ones = bits.count(1)
    console.print(f"Generated 10000 random bits, [zero]{zeros}[/zero] of them were 0, and [one]{ones}[/one] were 1.")
    console.print("[muted]The two counts land near 5000/5000, confirming the 50/50 superposition.[/muted]")


if __name__ == "__main__":
    main()
