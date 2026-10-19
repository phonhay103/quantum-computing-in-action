"""Chapter 8 — BB84: a key from bases that agree, and a trace Eve cannot hide.

The book's ``bb84`` sample, made complete. Alice and Bob each flip a coin per
qubit:

1. **Alice** picks a random bit and a random base, and prepares the qubit.
2. **Bob** picks a random base and measures.
3. They **sift**: they announce their *bases* (never their bits) and keep only the
   qubits where the bases matched. On those, Bob's bit is Alice's bit with
   certainty.
4. What is left is a shared, secret key.

The same machinery detects an eavesdropper. Eve cannot copy a qubit (Chapter 6),
so the best she can do is *intercept-resend*: measure each qubit in a base she
guesses, then re-send the state she collapsed it to. She is right about the base
half the time. When she is wrong, her measurement has already destroyed the state,
and Bob's sifted bits disagree with Alice's about a quarter of the time.

So the protocol is not only a key factory — it is a **wiretap detector**. No Eve,
zero errors; any interception, a measurable 25% error rate.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts
from quantum_computing_in_action.ch08 import protocol
from quantum_computing_in_action.ch08.protocol import Run, base_name

#: The number of qubits exchanged in the worked example.
SIZE = 8

#: The number of exchanges used to show the error rate separating cleanly.
RUNS = 200


def exchange(size: int = SIZE, *, seed: int | None = None, eavesdropper: bool = False) -> Run:
    """Run one BB84 exchange (optionally with an intercept-resend eavesdropper)."""
    return protocol.run(size, seed=seed, eavesdropper=eavesdropper)


def error_distribution(
    size: int = SIZE,
    runs: int = RUNS,
    *,
    seed: int | None = None,
    eavesdropper: bool = False,
) -> dict[int, int]:
    """Count how often each number of sifted errors occurs over ``runs`` exchanges.

    Without an eavesdropper every run gives 0 errors; with one, the errors scatter
    around a quarter of the sifted bits.
    """
    if runs < 1:
        raise ValueError("runs must be at least 1")
    rng = np.random.default_rng(seed)
    counts: dict[int, int] = {}
    for _ in range(runs):
        run = exchange(size, seed=int(rng.integers(1 << 30)), eavesdropper=eavesdropper)
        counts[run.errors] = counts.get(run.errors, 0) + 1
    return counts


def mean_error_rate(
    size: int = SIZE, runs: int = RUNS, *, seed: int | None = None, eavesdropper: bool = False
) -> float:
    """Return the average sifted error rate over ``runs`` exchanges."""
    base = 0 if seed is None else seed
    return float(
        np.mean([exchange(size, seed=base + index, eavesdropper=eavesdropper).error_rate for index in range(runs)])
    )


def draw(output: str | Path = "build/ch08-bb84-circuit.png") -> Path:
    """Render one BB84 circuit (prepare, Bob's base, measure) and save it."""
    run = exchange(seed=2)
    return render_circuit(protocol.bb84_circuit(run.alice_bits, run.alice_bases, run.bob_bases), output)


def _labelled(distribution: dict[int, int]) -> dict[str, int]:
    """Turn an error-count histogram into the string keys the chart wants."""
    return {str(errors): count for errors, count in sorted(distribution.items())}


def _sifting_table(run: Run) -> Table:
    table = Table(title="One BB84 exchange: bases decide which bits survive", header_style="heading")
    table.add_column("#", justify="right", style="muted")
    table.add_column("Alice bit", style="bits")
    table.add_column("Alice base", style="bits")
    table.add_column("Bob base", style="bits")
    table.add_column("Bob bit", style="bits")
    table.add_column("kept?", style="value")
    for index in range(run.size):
        kept = run.alice_bases[index] == run.bob_bases[index]
        verdict = "kept" if kept else "discarded (bases differ)"
        table.add_row(
            str(index),
            str(run.alice_bits[index]),
            base_name(run.alice_bases[index]),
            base_name(run.bob_bases[index]),
            str(run.bob_bits[index]),
            verdict,
        )
    return table


def main() -> None:
    explain(
        "Chapter 8 — BB84: a key from matching bases",
        """
BB84 turns the failed attempts of the last section into a protocol with two
properties at once: Alice and Bob end up with the **same** key, and an
eavesdropper **cannot** stay hidden.

The recipe is a coin flip per qubit on each side.

* Alice picks a random bit and a random base, and prepares the qubit in that base.
* Bob picks a random base and measures.
* They announce their **bases** — never their bits — and keep only the qubits
  where the bases matched. On a match Bob's measurement is Alice's bit with
  certainty, so those bits become the key.

Half the qubits match, so an ``N``-qubit exchange yields about ``N/2`` key bits.
That is the whole protocol: a public conversation about bases, and a private
agreement about bits.

Now the security. Eve cannot copy a qubit — the [no-cloning theorem](ch06-quantum-networking.md)
forbids it — so the best she can do is **intercept-resend**: measure each qubit in
a base she guesses, then send on whatever she collapsed it to. She guesses right
half the time. When she is wrong the state she forwards is no longer Alice's, and
Bob's sifted bits disagree with Alice's about a **quarter** of the time.

That number is the point. With no Eve the sifted error rate is exactly `0`. With
an Eve it jumps to about `0.25`, far above the noise. Alice and Bob simply compare
a sample of their sifted bits, and if too many disagree they throw the key away and
start over.
""",
    )

    steps(
        "Chapter 8 — the protocol",
        [
            ("Alice prepares", "a random bit in a random base (Z or X) for each qubit"),
            ("Bob measures", "in a random base of his own"),
            ("Sift", "announce bases, keep the qubits where they agree — about half"),
            ("Compare a sample", "no Eve: 0% errors; an interceptor: about 25%"),
        ],
    )

    console.rule("One exchange, bit by bit")
    run = exchange(seed=2)
    console.print(_sifting_table(run))
    console.print(
        f"  [heading]Alice's key:[/heading] [value]{run.alice_key}[/value]   "
        f"[heading]Bob's key:[/heading] [value]{run.bob_key}[/value]   "
        f"[muted]({len(run.sifted)} of {run.size} kept, {run.errors} errors)[/muted]"
    )
    console.print(
        "[muted]Where the bases match, the keys agree exactly. The bits measured in the other "
        "base are thrown away — they were never going to agree.[/muted]"
    )

    console.rule("With an eavesdropper")
    clean = mean_error_rate(seed=10)
    tapped = mean_error_rate(seed=10, eavesdropper=True)
    console.print(f"  [bits]no eavesdropper[/bits]       mean sifted error rate [value]{clean:.3f}[/value]")
    console.print(f"  [bits]intercept-resend[/bits]      mean sifted error rate [value]{tapped:.3f}[/value]")
    console.print(
        "[muted]Eve measures in a guessed base and forwards the collapsed state. Half her guesses "
        "are wrong, and half of those turn a key bit into its opposite: about 25% errors, versus "
        "0% on a clean line. The wiretap is impossible to hide.[/muted]"
    )

    circuit_path = draw()
    distribution_path = render_grouped_counts(
        [
            ("no eavesdropper", _labelled(error_distribution(seed=10))),
            ("intercept-resend", _labelled(error_distribution(seed=10, eavesdropper=True))),
        ],
        "build/ch08-eavesdropper-error.png",
        title=f"Sifted errors over {RUNS} exchanges: a clean line vs. a wiretap",
        xlabel="errors among the sifted bits",
        ylabel="exchanges",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, distribution_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
