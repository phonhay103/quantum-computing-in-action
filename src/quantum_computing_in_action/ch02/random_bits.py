"""Chapter 2 — "Hello World", quantum computing style: random bits."""

from __future__ import annotations

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.panel import Panel

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_bloch, render_circuit, render_counts


def _hadamard_circuit() -> QuantumCircuit:
    """A one-qubit circuit that puts the qubit in an equal superposition."""
    circuit = QuantumCircuit(1, 1)
    circuit.h(0)
    return circuit


def random_bit_circuit() -> QuantumCircuit:
    """The superposition circuit plus a measurement.

    Applying a Hadamard gate to ``|0>`` yields ``(|0> + |1>) / sqrt(2)``, so a
    measurement returns ``0`` or ``1`` with equal probability.
    """
    circuit = _hadamard_circuit()
    circuit.measure(0, 0)
    return circuit


def _sampled_counts(circuit: QuantumCircuit, shots: int) -> dict[str, int]:
    circuit.remove_final_measurements(inplace=True)
    state = Statevector.from_instruction(circuit)
    return {str(bit): int(count) for bit, count in state.sample_counts(shots).items()}


def _probabilities(state: Statevector) -> str:
    probs = state.probabilities_dict()
    return f"P(0) = {float(probs.get('0', 0.0)):.2f}, P(1) = {float(probs.get('1', 0.0)):.2f}"


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

    initial = Statevector.from_label("0")
    superposed = Statevector.from_instruction(_hadamard_circuit())
    first = random_bit()
    bits = random_bits(10000)
    zeros = bits.count(0)
    ones = bits.count(1)

    steps(
        "Chapter 2 — step by step",
        [
            ("Prepare a qubit in |0>", _probabilities(initial)),
            ("Apply the Hadamard gate H", _probabilities(superposed)),
            ("Measure the qubit", f"collapses to a single value: {first}"),
            ("Repeat 10000 times", f"0 -> {zeros}, 1 -> {ones}"),
        ],
    )

    console.rule("Using Qiskit to generate random bits")
    console.print(f"Generate one random bit, which can be 0 or 1. Result = [value]{first}[/value]")
    console.print(f"Generated 10000 random bits, [zero]{zeros}[/zero] of them were 0, and [one]{ones}[/one] were 1.")
    console.print("[muted]The two counts land near 5000/5000, confirming the 50/50 superposition.[/muted]")

    console.print(Panel(str(random_bit_circuit().draw("text")), title="Random-bit circuit", border_style="bits"))
    circuit_path = render_circuit(random_bit_circuit(), "build/random-bits-circuit.png")
    counts_path = render_counts({"0": zeros, "1": ones}, "build/random-bits-counts.png", title="10000 random bits")
    bloch_path = render_bloch([("after H", superposed)], "build/random-bits-bloch.png", title="Superposition state")
    console.print("Saved diagrams:")
    for path in (circuit_path, counts_path, bloch_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
