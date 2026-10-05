"""Dark-styled diagram helpers shared by the chapters.

Every renderer writes a PNG to ``build/`` (or the given path) and returns it, so
chapters can show the resulting diagrams instead of only printing numbers.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Pauli, Statevector

from quantum_computing_in_action._console import (
    DARK_BACKEND,
    DARK_CIRCUIT_STYLE,
    DARK_PLOT_STYLE,
)


def _prepare(output: str | Path) -> Path:
    import matplotlib

    matplotlib.use(DARK_BACKEND)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _bloch_vector(state: Statevector) -> list[float]:
    return [float(state.expectation_value(Pauli(axis)).real) for axis in ("X", "Y", "Z")]


def render_circuit(circuit: QuantumCircuit, output: str | Path) -> Path:
    """Render a quantum circuit diagram on a dark background."""
    path = _prepare(output)
    circuit.draw("mpl", filename=str(path), style=DARK_CIRCUIT_STYLE)
    return path


def render_counts(
    counts: Mapping[str, int],
    output: str | Path,
    *,
    title: str = "Measurement results",
) -> Path:
    """Render a bar chart of measurement counts on a dark background."""
    path = _prepare(output)
    from matplotlib import pyplot as plt

    with plt.style.context(DARK_PLOT_STYLE):
        fig, ax = plt.subplots(figsize=(5, 4))
        labels = list(counts)
        values = [counts[label] for label in labels]
        bars = ax.bar(labels, values, color="#5aa9ff")
        ax.bar_label(bars)
        ax.set_xlabel("measured bit")
        ax.set_ylabel("count")
        ax.set_title(title)
        fig.savefig(path)
        plt.close(fig)
    return path


def render_bloch(
    states: Sequence[tuple[str, Statevector]],
    output: str | Path,
    *,
    title: str | None = None,
) -> Path:
    """Render one Bloch sphere per ``(label, state)`` pair on a dark background."""
    path = _prepare(output)
    from matplotlib import pyplot as plt
    from qiskit.visualization import plot_bloch_vector

    with plt.style.context(DARK_PLOT_STYLE):
        columns = len(states)
        fig = plt.figure(figsize=(4 * columns, 4))
        for index, (label, state) in enumerate(states, start=1):
            ax = fig.add_subplot(1, columns, index, projection="3d")
            plot_bloch_vector(_bloch_vector(state), title=label, ax=ax)
        if title is not None:
            fig.suptitle(title)
        fig.savefig(path)
        plt.close(fig)
    return path
