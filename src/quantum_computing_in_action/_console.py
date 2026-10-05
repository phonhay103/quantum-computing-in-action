"""Shared Rich console with a dark-mode-friendly theme.

The generated plots use matching dark styles so the console output and the
images it references look consistent on a dark terminal.
"""

from __future__ import annotations

from collections.abc import Sequence

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

DARK_THEME = Theme(
    {
        "bits": "bold cyan",
        "classical": "bold yellow",
        "shor": "bold green",
        "value": "bold bright_green",
        "zero": "bold bright_cyan",
        "one": "bold bright_magenta",
        "heading": "bold bright_white",
        "muted": "dim white",
        "path": "bold bright_blue",
    }
)

console = Console(theme=DARK_THEME)


def explain(title: str, body: str) -> None:
    """Print a short explanation panel so samples are not just raw results."""
    console.print(Panel(Markdown(body), title=title, border_style="heading", expand=False))


def steps(title: str, rows: Sequence[tuple[str, str]]) -> None:
    """Print a numbered, step-by-step breakdown of a multi-step process.

    ``rows`` is a sequence of ``(action, detail)`` pairs; ``detail`` usually
    shows the state or result produced by that action.
    """
    table = Table(title=title, header_style="heading", expand=False)
    table.add_column("#", justify="right", style="muted")
    table.add_column("step", style="bits")
    table.add_column("what happens", style="value")
    for index, (action, detail) in enumerate(rows, start=1):
        table.add_row(str(index), action, detail)
    console.print(table)


DARK_BACKEND = "Agg"
DARK_CIRCUIT_STYLE = "iqp-dark"
DARK_PLOT_STYLE = "dark_background"
