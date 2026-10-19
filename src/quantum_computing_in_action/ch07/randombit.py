"""Chapter 7 — the HelloWorld circuit, built gate by gate.

Chapter 2's HelloWorld was a single call: it asked the simulator for a random bit
and got one. This module is the book's ``randombit`` sample (section 7.5.1),
which opens that call up into an explicit **program** of four qubits and two
steps:

    H(0), X(3)     -- put q0 into an even superposition and flip q3 to |1>
    CNOT(0, 1)     -- entangle q0 and q1

Only ``q0`` and ``q1`` end up interesting. Measuring all four qubits always
returns ``q3 = 1`` (set by the ``X``) and ``q2 = 0`` (never touched), while ``q0``
and ``q1`` come out *equal* — the ``CNOT`` glued them together, the same
correlation Chapter 5 built a Bell state from.
"""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_counts
from quantum_computing_in_action.ch07.circuits import (
    Builder,
    cumulative_states,
    prob_one_per_qubit,
    sample_counts,
    state_after,
)

#: The program runs on four qubits, even though only two of them matter.
N_QUBITS = 4


def _prepare(circuit: QuantumCircuit) -> None:
    """Step 1: put ``q0`` in an even superposition and flip ``q3`` to ``|1>``."""
    circuit.h(0)
    circuit.x(3)


def _entangle(circuit: QuantumCircuit) -> None:
    """Step 2: tie ``q1`` to ``q0`` with a ``CNOT``."""
    circuit.cx(0, 1)


#: The two steps, in the order the book builds them.
STEPS: tuple[tuple[str, Builder], ...] = (
    ("H(0), X(3)", _prepare),
    ("CNOT(0, 1)", _entangle),
)


def _program(circuit: QuantumCircuit) -> None:
    """Apply every step of the program to ``circuit``."""
    for _, builder in STEPS:
        builder(circuit)


def program_circuit(*, measure: bool = True) -> QuantumCircuit:
    """Return the four-qubit program, optionally with a measurement on every qubit.

    ``measure=False`` gives the bare circuit, which is what the state helpers
    need: ``Statevector`` refuses a circuit that already contains measurements.
    """
    circuit = QuantumCircuit(N_QUBITS, N_QUBITS)
    _program(circuit)
    if measure:
        for qubit in range(N_QUBITS):
            circuit.measure(qubit, qubit)
    return circuit


def step_states() -> list[tuple[str, Statevector]]:
    """Return the state after each step, starting from ``|0000>``."""
    return cumulative_states(STEPS, N_QUBITS)


def program_state() -> Statevector:
    """Return the state the whole program reaches, before any measurement."""
    return state_after(_program, N_QUBITS)


def random_bits(shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Measure the program ``shots`` times, keyed ``q0 q1 q2 q3``.

    Every outcome has ``q2 = 0`` and ``q3 = 1``; the randomness is confined to
    ``q0``, with ``q1`` trailing it.
    """
    return sample_counts(program_state(), shots, seed=seed)


def qubit_probabilities() -> dict[int, float]:
    """Return ``P(qi = 1)`` for each of the four qubits."""
    return prob_one_per_qubit(program_state())


def draw(output: str | Path = "build/ch07-randombit-circuit.png") -> Path:
    """Render the four-qubit program with its measurements and save it to ``output``.

    Qiskit draws ``q0`` at the top, matching the book's ``Qubit[0] ... Qubit[3]``.
    """
    return render_circuit(program_circuit(), output)


def _state_table() -> Table:
    table = Table(title="What each step does to the four qubits", header_style="heading")
    table.add_column("step", style="bits")
    table.add_column("P(q0=1)", style="value")
    table.add_column("P(q1=1)", style="value")
    table.add_column("P(q2=1)", style="value")
    table.add_column("P(q3=1)", style="value")
    for label, state in step_states():
        marginal = prob_one_per_qubit(state)
        table.add_row(label, *(f"{marginal[qubit]:.2f}" for qubit in range(N_QUBITS)))
    return table


def main() -> None:
    explain(
        "Chapter 7 — the HelloWorld circuit, step by step",
        """
Chapter 2 asked for a random bit and got one, without saying how. This sample
opens the box. A quantum program is not a function call — it is an ordered list
of **steps**, each holding the gates that act at the same time, and you can watch
the state move after every one.

This four-qubit program is two steps:

    H(0), X(3)     step 1: q0 into an even superposition, q3 flipped to |1>
    CNOT(0, 1)     step 2: flip q1 exactly when q0 is |1>

`H` makes `q0` a 50/50 mix of `|0>` and `|1>`. `X` turns `q3` into a definite
`|1>`; `q2` is never touched and stays `|0>`. Then `CNOT` ties `q1` to `q0`: the
pair is now the state `( |00> + |11> ) / sqrt(2)`, so whatever `q0` measures,
`q1` agrees.

Measured, that is a random bit with a witness: `q0` is the random value and `q1`
is a copy of it that the circuit produced for free — not by cloning (Chapter 6
forbids that) but by *entangling*, which is the only way a circuit can share an
unknown value.
""",
    )

    steps(
        "Chapter 7 — the program",
        [
            ("Prepare q0, q1, q2, q3", "|0000> — four qubits, all in |0>"),
            ("Step 1: H(0), X(3)", "q0 -> (|0> + |1>)/√2; q3 -> |1>; q1, q2 untouched"),
            ("Step 2: CNOT(0, 1)", "q1 follows q0: (|00> + |11>)/√2 on the pair"),
            ("Measure all four", "q3 = 1 and q2 = 0 always; q0 is random, q1 copies it"),
        ],
    )

    console.rule("The state after each step")
    console.print(_state_table())
    console.print(
        "[muted]Only q0 moves on its own. X pins q3 to 1 in the first step, and CNOT shows up "
        "in the last column pair: q1 starts at 0 and ends at 0.50, exactly like q0.[/muted]"
    )

    console.rule("Measured 1000 times")
    counts = random_bits(1000, seed=7)
    interesting = {"0001": counts.get("0001", 0), "1101": counts.get("1101", 0)}
    console.print(
        "  [heading]only outcomes possible: [/heading]"
        + ", ".join(f"q0q1q2q3={label}: {value}" for label, value in interesting.items())
    )
    console.print(
        "  [muted]Every other 4-bit string has probability 0: q2 is always 0, q3 is always 1, "
        f"and q0 = q1. The {sum(counts.values())} shots split into two mirror outcomes.[/muted]"
    )

    circuit_path = draw()
    counts_path = render_counts(
        interesting,
        "build/ch07-randombit-counts.png",
        title="1000 runs: only q0 varies, and q1 follows",
        xlabel="outcome (q0 q1 q2 q3)",
        ylabel="count",
    )
    qubits_path = render_counts(
        {f"q{qubit}": probability for qubit, probability in qubit_probabilities().items()},
        "build/ch07-randombit-qubits.png",
        title="Probability each qubit reads 1",
        xlabel="qubit",
        ylabel="P(1)",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, counts_path, qubits_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
