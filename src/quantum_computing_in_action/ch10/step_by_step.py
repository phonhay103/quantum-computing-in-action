"""Chapter 10 — Grover, step by step: watching the amplitude move.

The book's ``stepbystepgrover`` sample runs Grover on the smallest list where it
still means anything: two qubits, four states, one marked. Because there are so
few states you can print the whole amplitude vector after every round and see the
mechanism instead of trusting it.

The pattern is the whole algorithm in miniature:

    start          all four amplitudes equal, 1/2 each
    oracle         the marked amplitude flips sign: 1/2, 1/2, 1/2, -1/2
    diffusion      every amplitude is reflected about the mean (1/4), so the
                   marked one lands at 1 and the other three at 0

One round already reaches the answer with certainty here. A second round rotates
straight past it — the probability drops back to 1/4 — which is why the iteration
count is part of Grover and not a detail to guess.
"""

from __future__ import annotations

from pathlib import Path

from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_grouped_counts
from quantum_computing_in_action.ch10 import grover
from quantum_computing_in_action.ch10.oracle import marked_label

#: Two qubits: four states, the smallest Grover search that is not trivial.
WIDTH = 2

#: The marked state: index 3, i.e. ``|11>`` (both qubits set).
MARKED = 3


def round_states() -> list[tuple[str, Statevector]]:
    """Return the state before any round, after one, and after two."""
    return [(f"after {rounds} round(s)", grover.state_after(WIDTH, MARKED, rounds)) for rounds in range(3)]


def round_distributions() -> list[tuple[str, dict[str, float]]]:
    """Return the probability of each basis state after 0, 1 and 2 rounds."""
    distributions: list[tuple[str, dict[str, float]]] = []
    for label, state in round_states():
        distribution = {marked_label(WIDTH, index): float(abs(state.data[index]) ** 2) for index in range(1 << WIDTH)}
        distributions.append((label, distribution))
    return distributions


def _amplitude_table() -> Table:
    table = Table(title="The whole state after each round (amplitudes, with signs)", header_style="heading")
    table.add_column("round", style="bits")
    for index in range(1 << WIDTH):
        name = marked_label(WIDTH, index)
        table.add_column("marked " + name if index == MARKED else name, style="value")
    for label, state in round_states():
        cells = []
        for index in range(1 << WIDTH):
            amplitude = complex(state.data[index])
            value = 0.0 if abs(amplitude.real) < 1e-9 else amplitude.real
            cells.append(f"{value:+.2f}")
        table.add_row(label, *cells)
    return table


def draw(output: str | Path = "build/ch10-step-by-step.png") -> Path:
    """Render the per-round probability of each basis state."""
    return render_grouped_counts(
        round_distributions(),
        output,
        title="Grover on 2 qubits: the marked state takes all the probability",
        xlabel="basis state (q0 q1)",
        ylabel="probability",
    )


def main() -> None:
    explain(
        "Chapter 10 — Grover, step by step",
        """
Two qubits give four states; mark one of them and run Grover until the amplitudes
tell the story. The oracle only changes a **sign**, the diffusion only reflects
about the **average**, and those two moves are enough to move all the probability
onto the answer.

Start uniform: every amplitude is `1/2`, so the average is also `1/2`.

    oracle      1/2, 1/2, 1/2, -1/2     the marked state flips below the mean
    diffusion   reflect about the mean:  a -> 2*mean - a

The mean after the oracle is `(1/2 + 1/2 + 1/2 - 1/2)/4 = 1/4`. Reflect:

    1/2  ->  2*(1/4) - 1/2  =  0
    -1/2 ->  2*(1/4) + 1/2  =  1

One round and the marked state has **all** the probability. The other three states
are exactly zero. A second round rotates past the answer — back to `1/4` — which is
the overshoot the previous module warned about.
""",
    )

    steps(
        "Chapter 10 — one round on two qubits",
        [
            ("H on both qubits", "all four amplitudes 1/2: the uniform superposition"),
            ("Oracle", "the marked amplitude becomes -1/2; the average drops to 1/4"),
            ("Diffusion", "reflecting about 1/4 sends the marked to 1 and the rest to 0"),
            ("Measure", "the marked state with certainty — one round was enough"),
            ("A second round", "overshoots: the probability falls back to 1/4"),
        ],
    )

    console.rule("The amplitudes, round by round")
    console.print(_amplitude_table())
    console.print(
        "[muted]The oracle flips one sign (row 2). The diffusion is a reflection about the mean, "
        "which lands the marked state at 1 and the others at 0 (row 3). Row 4 is one round too "
        "many: the rotation carries on past the answer.[/muted]"
    )

    console.rule("The same thing as probabilities")
    for label, distribution in round_distributions():
        cells = ", ".join(f"{state}: {probability:.2f}" for state, probability in distribution.items())
        console.print(f"  [bits]{label:<16}[/bits] {cells}")

    path = draw()
    console.print("Saved diagrams:")
    console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
