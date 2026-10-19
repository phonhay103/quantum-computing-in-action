"""Chapter 10 — searching a database: the classical way and with Grover.

The book's search chapter uses a small address book of people and one question —
*find the 29-year-old in Mexico* — that has no structure to exploit. A classical
program checks names one at a time; on average it finds the answer at ``N/2``.
Grover finds it in about ``(pi/4)*sqrt(N)``.

This module holds the classical side (the ``classicsearch`` sample) and a Grover
search over the same table (the ``quantumsearch`` sample). It is the concrete face
of the abstract list the rest of the chapter talks about: eight people, three
qubits, two Grover rounds.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_counts
from quantum_computing_in_action.ch10 import grover


@dataclass(frozen=True)
class Person:
    """One entry in the address book."""

    name: str
    age: int
    country: str


#: The address book: eight people, exactly one of them the search target.
DATABASE: tuple[Person, ...] = (
    Person("Alice", 42, "Nigeria"),
    Person("Bob", 36, "Australia"),
    Person("Eve", 85, "USA"),
    Person("Niels", 18, "Greece"),
    Person("Albert", 29, "Mexico"),
    Person("Roger", 29, "Belgium"),
    Person("Marie", 15, "Russia"),
    Person("Janice", 52, "China"),
)

#: The qubits a Grover search of the address book needs (8 entries = 3 qubits).
WIDTH = 3


def is_target(person: Person) -> bool:
    """The predicate the search looks for: 29 years old and in Mexico."""
    return person.age == 29 and person.country == "Mexico"


def target_index(people: tuple[Person, ...] = DATABASE) -> int:
    """Return the index of the (unique) target, or raise if there is none."""
    matches = [index for index, person in enumerate(people) if is_target(person)]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one match, found {len(matches)}")
    return matches[0]


def classical_search(people: tuple[Person, ...] = DATABASE) -> tuple[int, int]:
    """Return ``(index, tries)`` for a linear scan of ``people``.

    Tries counts from 1, so a hit on the first entry is one try — the classical
    cost Grover is compared against.
    """
    for index, person in enumerate(people):
        if is_target(person):
            return index, index + 1
    raise ValueError("no match in the database")


def tries_distribution(trials: int = 2000, *, seed: int | None = None) -> dict[int, int]:
    """Shuffle the book ``trials`` times and count how many tries the scan needed.

    The result is the flat distribution of the classical baseline: 1 to 8 tries,
    each equally likely, averaging 4.5.
    """
    if trials < 1:
        raise ValueError("trials must be at least 1")
    rng = np.random.default_rng(seed)
    counts: dict[int, int] = {}
    for _ in range(trials):
        order = rng.permutation(len(DATABASE))
        for position, index in enumerate(order, start=1):
            if is_target(DATABASE[index]):
                counts[position] = counts.get(position, 0) + 1
                break
    return counts


def quantum_search(*, seed: int | None = None) -> Person:
    """Run Grover once and return the person whose index is measured.

    With three qubits and `(pi/4)*sqrt(8) = 1` round the answer is right about 78%
    of the time; two rounds push it to about 94%. Either way a single run usually
    returns the target, where the classical scan needs 4.5 tries on average.
    """
    counts = grover.measured_counts(WIDTH, target_index(), 1, seed=seed)
    (label,) = counts
    return DATABASE[int(label[::-1], 2)]


def success_rate(runs: int = 200, *, seed: int | None = None) -> float:
    """Return the fraction of ``runs`` Grover searches that land on the target."""
    if runs < 1:
        raise ValueError("runs must be at least 1")
    rng = np.random.default_rng(seed)
    hits = sum(quantum_search(seed=int(rng.integers(1 << 30))) is DATABASE[target_index()] for _ in range(runs))
    return hits / runs


def draw(output: str | Path = "build/ch10-classical-tries.png") -> Path:
    """Render the classical search's tries distribution."""
    return render_counts(
        {str(tries): count for tries, count in sorted(tries_distribution(seed=3).items())},
        output,
        title="Classical scan: how many tries to find the target",
        xlabel="tries",
        ylabel="shuffles (of 2000)",
    )


def main() -> None:
    explain(
        "Chapter 10 — searching a database",
        """
The list Grover searches is deliberately **unstructured**: there is no sorted key
to binary-search, only a test you can apply to one item at a time. The chapter's
example is a small address book and the question *who is 29 and lives in Mexico?*

Classically there is nothing to do but look, one entry at a time. The match is
somewhere in the list, so on average that is `N/2` tries, and the *worst* case is
all `N`.

Grover's advantage is that the list becomes a quantum register of `log2(N)` qubits
and the test becomes an oracle. For eight entries that is three qubits, and the
search is a handful of rounds rather than a handful of entries:

* `N = 8`  -> `(pi/4)*sqrt(8) ~ 2` rounds;
* `N = 64` -> `6` rounds instead of an average of `32` tries.

The speed-up is **quadratic**, not exponential: doubling the list multiplies the
classical work by four but the quantum work by only about two. That is the honest
size of Grover's gift — real, useful, and modest — and it is provably the best
possible for a list with no structure.
""",
    )

    steps(
        "Chapter 10 — classical versus Grover",
        [
            ("Build the address book", f"{len(DATABASE)} people, one match"),
            ("Classical scan", "check entry after entry; 4.5 tries on average"),
            ("Encode as a register", f"{WIDTH} qubits hold the {len(DATABASE)} indices"),
            ("Grover", "one oracle query per round, sampling the answer in a few rounds"),
        ],
    )

    index, tries = classical_search()
    console.rule("The classical baseline")
    console.print(f"  [bits]the target is[/bits] {DATABASE[index].name} at index {index}, found in {tries} tries")
    console.print(
        "  [muted]A shuffled list puts the target at each position equally often, so the average "
        "is (1+2+...+8)/8 = 4.5 tries. That is the bar Grover has to beat.[/muted]"
    )

    console.rule("The same search with Grover")
    console.print(
        f"  [bits]marked index[/bits] {target_index()}  "
        f"[muted]({len(DATABASE)} entries -> {WIDTH} qubits, "
        f"{grover.optimal_iterations(WIDTH)} rounds)[/muted]"
    )
    console.print(
        f"  [bits]success rate[/bits] {success_rate(seed=5):.3f}  "
        "[muted]one Grover run, versus a 1-in-8 chance of guessing[/muted]"
    )
    console.print(
        "[muted]Each run returns the answer with high probability, using about sqrt(N) rounds rather "
        "than N/2 lookups.[/muted]"
    )

    path = draw()
    console.print("Saved diagrams:")
    console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
