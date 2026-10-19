"""Chapter 11 — factoring the classical way, and the semiclassic shortcut.

The book opens the factoring chapter with two classical programs and a promise.

* The ``classicfactor`` sample: trial division. Try 2, 3, 4, 5 ... up to ``sqrt(N)``
  and stop at the first divisor. Simple, correct, and hopeless — the work grows like
  ``sqrt(N)``, and the *number field sieve* (much better, still sub-exponential) is
  the best classical method known.
* The ``semiclassicfactor`` sample: the **reduction** Shor is built on. Factoring
  is turned into **order finding** — the period of ``a^x mod N`` — and the period
  is then converted into a factor with a couple of ``gcd`` calls. Everything here
  is classical; the quantum part only replaces the one expensive step, finding the
  period.

That reduction is the whole reason factoring is a quantum question: the classical
period search is as hard as factoring, but a quantum computer can find the period
in polynomial time.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_counts


def steps_to_factor(n: int) -> int:
    """Return how many trial divisors are tested before a factor is found.

    Two is tried first, then every odd divisor up to ``sqrt(n)`` — the loop trial
    division actually runs, which is why the cost grows like ``sqrt(n)``.

    Raises:
        ValueError: if ``n`` is less than 2.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    if n % 2 == 0:
        return 1
    count = 1  # the division by 2
    divisor = 3
    while divisor * divisor <= n:
        count += 1
        if n % divisor == 0:
            return count
        divisor += 2
    return count


def trial_division(n: int) -> int:
    """Return the smallest divisor of ``n`` greater than 1 (``n`` itself if prime).

    Raises:
        ValueError: if ``n`` is less than 2.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    if n % 2 == 0:
        return 2
    divisor = 3
    while divisor * divisor <= n:
        if n % divisor == 0:
            return divisor
        divisor += 2
    return n


def classical_period(a: int, n: int) -> int:
    """Return the order of ``a`` modulo ``n``: the smallest ``r > 0`` with ``a^r = 1``.

    This is the step a quantum computer does faster. Brute force is the honest
    classical baseline, and it is why the classical reduction does not by itself
    make factoring easy.
    """
    if math.gcd(a, n) != 1:
        raise ValueError("a and n must be coprime")
    value, period = a % n, 1
    while value != 1:
        value = (value * a) % n
        period += 1
    return period


def factor_from_order(a: int, n: int, period: int) -> int | None:
    """Turn a period into a factor of ``n``, or ``None`` if this attempt fails.

    The two roots of ``1`` are ``gcd(a^(r/2) - 1, n)`` and ``gcd(a^(r/2) + 1, n)``.
    The attempt fails when the period is odd, or when ``a^(r/2) = -1`` (whose ``+1``
    side gives the trivial factor ``n``); then Shor just picks another ``a``.
    """
    if period < 1 or period % 2:
        return None
    half = pow(a, period // 2, n)
    if half in (1, n - 1):
        return None
    for candidate in (math.gcd(half - 1, n), math.gcd(half + 1, n)):
        if 1 < candidate < n:
            return candidate
    return None


def semiclassic_factor(n: int, *, max_tries: int = 100) -> int:
    """Factor ``n`` the semiclassic way: preprocessing, classical period, ``gcd``.

    Every step is classical — this is the book's ``semiclassicfactor`` sample — and
    it shows exactly which piece the quantum algorithm has to supply.

    Raises:
        ValueError: if ``n`` is less than 2 or no factor is found in ``max_tries``.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    for attempt in range(2, 2 + max_tries):
        a = attempt
        if a >= n:
            break
        common = math.gcd(a, n)
        if common != 1:
            return common
        period = classical_period(a, n)
        factor = factor_from_order(a, n, period)
        if factor is not None:
            return factor
    raise ValueError(f"failed to factor {n} after {max_tries} tries")


def reduction_steps(a: int, n: int) -> dict[str, int]:
    """Return the book's worked arithmetic for one ``(a, n)`` pair.

    This is what the book's two ``jshell`` snippets check by hand: the period
    ``r``, the value ``a^(r/2) mod n``, and the two ``gcd``s that turn the period
    into factors. For the book's larger example — ``a = 6``, ``n = 493`` — the
    period is 112, ``6^56 mod 493`` is 407, and the two gcds are 29 and 17, so
    ``493 = 17 x 29``.

    Raises:
        ValueError: if ``a`` and ``n`` are not coprime, or the period is odd (in
            which case ``a^(r/2)`` has no integer exponent).
    """
    period = classical_period(a, n)
    if period % 2:
        raise ValueError(f"the period {period} is odd, so a^(r/2) is not an integer power")
    half = pow(a, period // 2, n)
    return {
        "period": period,
        "a^(r/2) mod n": half,
        "gcd(a^(r/2) - 1, n)": math.gcd(half - 1, n),
        "gcd(a^(r/2) + 1, n)": math.gcd(half + 1, n),
    }


def random_semiclassic_factor(*, seed: int | None = None, upper: int = 10000) -> tuple[int, int]:
    """Factor a random target below ``upper``, the way the book's sample does.

    The book's ``semiclassicfactor`` picks a random ``N`` each run and retries on
    its own; this is the same idea with the randomness made reproducible. Returns
    ``(n, factor)`` for the first target that factorises.

    Raises:
        ValueError: if no target in one hundred draws could be factored.
    """
    if upper < 4:
        raise ValueError("upper must be at least 4")
    rng = np.random.default_rng(seed)
    for _ in range(100):
        n = int(rng.integers(4, upper))
        if n % 2 == 0:
            return n, 2
        try:
            return n, semiclassic_factor(n)
        except ValueError:
            continue
    raise ValueError(f"no factorable target below {upper}")


def steps_curve(limit: int = 200) -> dict[int, float]:
    """Return the number of trial divisions needed for each ``n`` up to ``limit``.

    A rough measure of the classical cost: the loop runs while ``d*d <= n``, so it
    grows like ``sqrt(n)`` — and that is only the *naive* method.
    """
    if limit < 3:
        raise ValueError("limit must be at least 3")
    return {n: float(steps_to_factor(n)) for n in range(3, limit + 1)}


def period_function(a: int = 2, n: int = 15, length: int = 16) -> dict[int, int]:
    """Return ``{x: a^x mod n}`` for ``x`` from 0 to ``length - 1``.

    The values repeat with the period — for ``a = 2`` and ``n = 15`` the sequence is
    ``1, 2, 4, 8, 1, 2, 4, 8, ...``, period 4. That repetition is what Shor hunts.
    """
    if math.gcd(a, n) != 1:
        raise ValueError("a and n must be coprime")
    return {x: pow(a, x, n) for x in range(length)}


def draw_classical(output: str | Path = "build/ch11-classical-factor.png") -> Path:
    """Render the classical trial-division cost for small ``n``."""
    return render_counts(
        {str(n): float(steps) for n, steps in steps_curve(120).items()},
        output,
        title="Classical trial division: work grows like sqrt(n)",
        xlabel="n",
        ylabel="trial divisions",
    )


def draw_period(output: str | Path = "build/ch11-period-function.png") -> Path:
    """Render ``a^x mod n`` and its repetition."""
    return render_counts(
        {str(x): float(value) for x, value in period_function().items()},
        output,
        title="The period of 2^x mod 15 is 4",
        xlabel="x",
        ylabel="2^x mod 15",
    )


def main() -> None:
    explain(
        "Chapter 11 — factoring, and the reduction that makes it quantum",
        """
Factoring a large number is the problem that made quantum computing famous. The
best classical methods (the *general number field sieve*) take **sub-exponential**
time; Shor's algorithm takes polynomial time. Everything in this module is the
*classical* half of the story — the half that tells you what the quantum part has
to do.

**Trial division** is the honest starting point. Try 2, 3, 4, 5 ... until something
divides `N`. Correct, and hopeless: the loop runs about `sqrt(N)` times, and for a
number with hundreds of digits that is already out of reach. Its only virtue is
that it works and is easy to trust.

**Shor's reduction** is where the structure appears. Instead of hunting for a
factor directly, we hunt for the **period** of

    f(x) = a^x mod N

for some `a` coprime to `N`. That sequence is periodic; call its period `r`. Once
you know `r`, a little arithmetic finishes the job:

* if `r` is odd, or `a^(r/2) = -1`, this `a` was unlucky — pick another and retry;
* otherwise `gcd(a^(r/2) - 1, N)` and `gcd(a^(r/2) + 1, N)` are the two factors.

For `N = 15` and `a = 2`, the sequence is `1, 2, 4, 8, 1, 2, 4, 8, ...`, so the
period is `r = 4`. Then `a^(r/2) = 4`, and `gcd(4 - 1, 15) = 3` — one factor, with
`15/3 = 5` its partner.

The catch is that *finding* `r` classically is as hard as factoring, so this
reduction alone buys nothing. What it does is isolate the one step a quantum
computer can do well: **order finding**. The next modules build it.
""",
    )

    steps(
        "Chapter 11 — the semiclassic route",
        [
            ("Preprocess", "pick a coprime to N; gcd(a, N) > 1 would already be a factor"),
            ("Find the period", "the smallest r with a^r = 1 (mod N)"),
            ("Guard", "if r is odd, or a^(r/2) = -1, retry with another a"),
            ("Extract", "gcd(a^(r/2) - 1, N) and gcd(a^(r/2) + 1, N) are the factors"),
        ],
    )

    console.rule("The classical baseline")
    for n in (15, 91, 9999, 999983):
        console.print(
            f"  [bits]trial division[/bits] {n:>7} -> {trial_division(n)}  [muted]({steps_to_factor(n)} divisions)[/muted]"
        )
    console.print("[muted]The work grows like sqrt(n): fine for 999983, impossible for a 300-digit semiprime.[/muted]")

    console.rule("The period, and the factor it gives")
    period = classical_period(2, 15)
    console.print("  [bits]2^x mod 15[/bits] " + ", ".join(str(value) for value in period_function(length=8).values()))
    console.print(
        f"  [bits]period[/bits] r = {period}   "
        f"[bits]factor[/bits] gcd(2^(r/2) - 1, 15) = {factor_from_order(2, 15, period)}"
    )
    console.print(
        "[muted]The sequence repeats every 4 steps, and the two gcd's turn that period into the "
        "factors 3 and 5. Finding the period by brute force is the expensive part — the part the "
        "quantum Fourier transform replaces.[/muted]"
    )

    console.rule("The semiclassic factorization")
    for n in (15, 21, 35, 91):
        factor = semiclassic_factor(n)
        console.print(f"  [bits]semiclassic[/bits] {n:>4} = {factor} x {n // factor}")

    console.rule("The book's larger example (a = 6, N = 493)")
    worked = reduction_steps(6, 493)
    console.print(
        f"  [bits]period[/bits] r = {worked['period']}   [bits]6^(r/2) mod 493[/bits] = {worked['a^(r/2) mod n']}"
    )
    console.print(
        f"  [bits]gcd(6^(r/2) - 1, 493)[/bits] = {worked['gcd(a^(r/2) - 1, n)']}   "
        f"[bits]gcd(6^(r/2) + 1, 493)[/bits] = {worked['gcd(a^(r/2) + 1, n)']}"
    )
    console.print(
        "[muted]493 = 17 x 29. These are the two numbers the book's jshell snippets check by hand: "
        "the period is 112, and the two gcd's split 493.[/muted]"
    )

    classical_path = draw_classical()
    period_path = draw_period()
    console.print("Saved diagrams:")
    for path in (classical_path, period_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
