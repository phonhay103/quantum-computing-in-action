"""Chapter 7 — debugging a circuit: the state after every step.

The book's ``randombitdebug`` sample (section 7.5.2) is the ``randombit`` program
with a **probability gate** slipped in after each step. StrangeFX draws the
probability vector at every one of those points, so you can see *when* each qubit
changes instead of guessing from the final histogram.

The Qiskit equivalent needs no extra gate: the simulator's state is the same
object at every point, so this module snapshots it after each step (see
:func:`randombit.step_states`) and reports the full probability vector and each
qubit's marginal. :func:`debug_circuit` adds barriers to the drawn circuit so the
step boundaries are visible in the picture too.
"""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts
from quantum_computing_in_action.ch07 import randombit
from quantum_computing_in_action.ch07.circuits import nonzero_probabilities, prob_one_per_qubit

#: The order the four qubits are printed in everywhere in this chapter.
QUBITS = tuple(range(randombit.N_QUBITS))


def debug_circuit(*, measure: bool = False) -> QuantumCircuit:
    """Return the program with a barrier after each step.

    The barriers play the role of the book's probability gates: they mark where
    one step ends and the next begins, so the drawn circuit matches the table of
    intermediate states.
    """
    circuit = QuantumCircuit(randombit.N_QUBITS, randombit.N_QUBITS)
    circuit.barrier()
    for _, builder in randombit.STEPS:
        builder(circuit)
        circuit.barrier()
    if measure:
        for qubit in QUBITS:
            circuit.measure(qubit, qubit)
    return circuit


def step_probabilities() -> list[tuple[str, dict[str, float]]]:
    """Return the (nonzero) probability vector after each step, in book bit order."""
    return [(label, nonzero_probabilities(state)) for label, state in randombit.step_states()]


def step_marginals() -> list[tuple[str, dict[int, float]]]:
    """Return each qubit's ``P(1)`` after each step: one entry per step."""
    return [(label, prob_one_per_qubit(state)) for label, state in randombit.step_states()]


def draw(output: str | Path = "build/ch07-debug-circuit.png") -> Path:
    """Render the program with its step barriers and save it to ``output``."""
    return render_circuit(debug_circuit(), output)


def _probability_table() -> Table:
    table = Table(title="Probability vector after each step (only nonzero states)", header_style="heading")
    table.add_column("step", style="bits")
    table.add_column("basis state q0 q1 q2 q3", style="classical")
    table.add_column("probability", style="value")
    for label, distribution in step_probabilities():
        for index, (state, probability) in enumerate(sorted(distribution.items())):
            table.add_row(label if index == 0 else "", state, f"{probability:.2f}")
    return table


def _marginal_table() -> Table:
    table = Table(title="P(qubit = 1) after each step", header_style="heading")
    table.add_column("step", style="bits")
    for qubit in QUBITS:
        table.add_column(f"q{qubit}", style="value")
    for label, marginal in step_marginals():
        table.add_row(label, *(f"{marginal[qubit]:.2f}" for qubit in QUBITS))
    return table


def main() -> None:
    explain(
        "Chapter 7 — debugging a circuit",
        """
A histogram at the end tells you *what* a circuit returns; it does not tell you
*where* each qubit changed. The book's debugger answers that by showing the
probability vector after **every** step.

The simulator holds one object — the state — from start to finish. A measurement
is simply the last thing you do to it. So "debugging" is nothing more than
looking at that state at each step, and the whole earlier program is rebuilt here
with a boundary drawn after every step.

Watch the four qubits:

* `q0` starts at `P(1) = 0`, jumps to `0.50` the moment `H` runs, and never moves
  again on its own.
* `q1` sits at `0` until the `CNOT` drags it up to `0.50` — because it only moves
  when `q0` is `|1>`.
* `q2` stays at `0` throughout: nothing in the program touches it.
* `q3` jumps straight to `1` in the first step and stays there.

The table is the picture the debugger draws, one column per qubit. It shows the
`X` and the `H` acting in step 1, and the `CNOT` acting *only* in step 2 — which
is exactly what "a program is a list of steps" means.
""",
    )

    steps(
        "Chapter 7 — where each change happens",
        [
            ("start", "|0000> — every qubit certain, P(1) = 0"),
            ("after step 1 (H, X)", "q0 = 0.50 and q3 = 1; q1 and q2 still 0"),
            ("after step 2 (CNOT)", "q1 = 0.50, tracking q0; q2 stays 0 and q3 stays 1"),
            ("read the vector", "two basis states share the probability: the pair q0 q1 is correlated"),
        ],
    )

    console.rule("The probability vector, step by step")
    console.print(_probability_table())
    console.print(
        "[muted]The vector never has more than two nonzero entries, and after the CNOT the two "
        "are 0001 and 1101: q2 and q3 are fixed, and q0 = q1 always.[/muted]"
    )

    console.rule("One column per qubit")
    console.print(_marginal_table())
    console.print(
        "[muted]q0 changes in the first step (H), q1 in the second (CNOT), and q2 and q3 hold "
        "their values the whole way through. A histogram of the final state could not tell you "
        "that; the intermediate state can.[/muted]"
    )

    circuit_path = draw()
    states_path = render_grouped_counts(
        step_probabilities(),
        "build/ch07-debug-steps.png",
        title="Basis-state probabilities after each step",
        xlabel="basis state (q0 q1 q2 q3)",
        ylabel="probability",
    )
    marginals_path = render_grouped_counts(
        [(label, {f"q{qubit}": value for qubit, value in marginal.items()}) for label, marginal in step_marginals()],
        "build/ch07-debug-marginals.png",
        title="P(qubit = 1) after each step",
        xlabel="qubit",
        ylabel="P(1)",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, states_path, marginals_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
