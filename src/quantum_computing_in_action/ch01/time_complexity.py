"""Chapter 1 — why quantum computing matters: factoring time complexity."""

from __future__ import annotations

import math
from collections.abc import Callable, Iterator
from pathlib import Path

from rich.console import Console
from rich.table import Table

TimeFunction = Callable[[float], float]

console = Console()


def classical_factoring_time(bits: float) -> float:
    """Estimated time to factor an ``bits``-bit number classically.

    Mirrors the book's sample function for the best known classical algorithm
    (the general number field sieve): ``exp((64/9 * b * ln(b)^2)^(1/3))``.
    """
    _require_positive(bits)
    return math.exp((64.0 / 9.0 * bits * math.log(bits) ** 2) ** (1.0 / 3.0))


def shor_factoring_time(bits: float) -> float:
    """Time to factor an ``bits``-bit number with Shor's algorithm, ``O(b^3)``."""
    _require_positive(bits)
    return bits**3


def _require_positive(bits: float) -> None:
    if bits <= 0:
        raise ValueError("bits must be positive")


def sample(
    function: TimeFunction,
    start: float,
    stop: float,
    div: int = 500,
) -> Iterator[tuple[float, float]]:
    """Yield ``div`` evenly spaced ``(bits, time)`` pairs between ``start`` and ``stop``."""
    step = (stop - start) / div
    for index in range(div):
        x = start + index * step
        yield x, function(x)


def plot(
    start: float = 1e-6,
    stop: float = 20.0,
    output: str | Path = "build/time-complexity.png",
) -> Path:
    """Plot the classical and Shor time-complexity curves and save them to ``output``."""
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    for function, label in (
        (classical_factoring_time, "classical"),
        (shor_factoring_time, "shor"),
    ):
        xs, ys = zip(*sample(function, start, stop), strict=True)
        ax.plot(xs, ys, label=label)

    ax.set_xlabel("number of bits")
    ax.set_ylabel("time required to factor")
    ax.set_title("Time Complexity")
    ax.legend()
    fig.savefig(path)
    plt.close(fig)
    return path


def main() -> None:
    table = Table(title="Time required to factor an n-bit number")
    table.add_column("bits", justify="right", style="cyan")
    table.add_column("classical", justify="right", style="yellow")
    table.add_column("shor", justify="right", style="green")
    for bits in (4, 8, 16, 32, 64):
        table.add_row(
            str(bits),
            f"{classical_factoring_time(bits):.3e}",
            f"{shor_factoring_time(bits):.3e}",
        )
    console.print(table)
    path = plot()
    console.print(f"\nSaved plot to [bold]{path}[/bold]")


if __name__ == "__main__":
    main()
