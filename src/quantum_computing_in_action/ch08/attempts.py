"""Chapter 8 — the attempts that do not work: no base, and an unreconciled one.

The book walks through two failed designs before BB84.

* ``naive``: Alice sends plain bits. Bob measures them in the Z base and gets them
  *exactly* — which is the problem. Anything Bob can read, Eve can read just as
  well, because there is no base in play and nothing to disturb.
* ``guess``: Alice picks a random base per qubit, but Bob never learns it. He
  measures everything in Z anyway, so half the qubits were measured in the wrong
  base and a quarter of his bits come out wrong. A key with a 25% error rate is
  worse than useless.

BB84 fixes the second failure by *reconciling bases*: the two of them compare
bases (not bits) and keep only the qubits measured in the matching base.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_counts
from quantum_computing_in_action.ch08 import protocol
from quantum_computing_in_action.ch08.protocol import Run, Z

#: How many qubits each attempt exchanges.
SIZE = 64


def _random_bits(rng: np.random.Generator, count: int) -> tuple[int, ...]:
    return tuple(int(value) for value in rng.integers(0, 2, size=count))


def naive_exchange(size: int = SIZE, *, seed: int | None = None) -> Run:
    """Alice sends plain bits in the Z base; Bob measures in Z and gets them all.

    Every bit arrives intact (``raw_error_rate == 0``) — and an eavesdropper in
    the middle would read exactly the same bits. Zero errors is not success here;
    it is the absence of any secret.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    rng = np.random.default_rng(seed)
    alice_bits = _random_bits(rng, size)
    bob_bits = tuple(protocol.measure(bit, prepared_base=Z, measured_base=Z, rng=rng) for bit in alice_bits)
    zeros = (Z,) * size
    return Run(alice_bits=alice_bits, alice_bases=zeros, bob_bases=zeros, bob_bits=bob_bits)


def blind_exchange(size: int = SIZE, *, seed: int | None = None) -> Run:
    """Alice picks a random base per qubit; Bob measures every qubit in Z.

    Bob never learns Alice's bases, so half his measurements are in the wrong
    base. Of those, half flip — a raw error rate of about ``0.25``.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    rng = np.random.default_rng(seed)
    alice_bits = _random_bits(rng, size)
    alice_bases = _random_bits(rng, size)
    bob_bits = tuple(
        protocol.measure(bit, prepared_base=alice_bases[index], measured_base=Z, rng=rng)
        for index, bit in enumerate(alice_bits)
    )
    return Run(
        alice_bits=alice_bits,
        alice_bases=alice_bases,
        bob_bases=(Z,) * size,
        bob_bits=bob_bits,
    )


def draw(output: str | Path = "build/ch08-attempts-error.png") -> Path:
    """Render the raw error rate of the two failed attempts."""
    naive = naive_exchange(seed=1)
    blind = blind_exchange(seed=1)
    return render_counts(
        {"naive (no base)": naive.raw_error_rate, "blind base (Z only)": blind.raw_error_rate},
        output,
        title="Why bases must be reconciled",
        xlabel="attempt",
        ylabel="raw error rate",
    )


def main() -> None:
    explain(
        "Chapter 8 — two attempts that do not work",
        """
Before BB84 there is the obvious way to send a secret, and it fails for a
subtle reason.

**Attempt 1 — no base at all.** Alice encodes each bit in `|0>` or `|1>` and sends
it. Bob measures in the `Z` base and gets every bit back exactly. If that sounds
like success, look closer: nothing about the qubit is disturbed by Bob's
measurement, so **anything Bob can read, Eve can read too**. With no base in play
there is no secret to protect — only a private conversation between two people
who are not being watched.

**Attempt 2 — a base nobody reconciles.** Alice now flips a coin per qubit and
prepares it in `Z` (`|0>`, `|1>`) or in `X` (`|+>`, `|->`). Bob, who has no idea
which base she used, measures everything in `Z`. When Alice happened to use `Z`,
Bob is right. When she used `X`, the state is a superposition and Bob gets a fair
coin — **half** those bits flip. Since half the qubits are in the wrong base, the
raw error rate is about a quarter.

A key that is wrong one bit in four is not a key. The fix is not more qubits, it
is a short conversation about **bases**: BB84 has Alice and Bob compare which base
they used and throw away the qubits where the bases differ.
""",
    )

    steps(
        "Chapter 8 — where each attempt breaks",
        [
            ("Naive: send plain bits", "Bob reads every bit exactly — and so could Eve"),
            ("Naive: measure", "raw error 0.00, but nothing is secret"),
            ("Blind: random bases, Bob in Z", "half the qubits are measured in the wrong base"),
            ("Blind: measure", "raw error about 0.25 — the key is unusable"),
        ],
    )

    console.rule("Raw error rate of each attempt")
    naive = naive_exchange(seed=1)
    blind = blind_exchange(seed=1)
    console.print(
        f"  [bits]naive (no base)[/bits]      raw error {naive.raw_error_rate:.2f}  "
        "[muted]perfect for Bob — and for Eve[/muted]"
    )
    console.print(
        f"  [bits]blind base (Z only)[/bits]  raw error {blind.raw_error_rate:.2f}  "
        "[muted]a quarter of the key is wrong[/muted]"
    )

    path = draw()
    console.print("Saved diagrams:")
    console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
