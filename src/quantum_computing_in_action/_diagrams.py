"""Dark-styled diagram helpers shared by the chapters.

Every renderer writes a PNG to ``build/`` (or the given path) and returns it, so
chapters can show the resulting diagrams instead of only printing numbers.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

import numpy as np
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


def render_circuit(circuit: QuantumCircuit, output: str | Path, *, reverse_bits: bool = False) -> Path:
    """Render a quantum circuit diagram on a dark background.

    ``reverse_bits=True`` draws the highest-indexed qubit at the top, so a
    circuit can be shown in the conventional "control first" order.
    """
    path = _prepare(output)
    figure = circuit.draw("mpl", filename=str(path), style=DARK_CIRCUIT_STYLE, reverse_bits=reverse_bits)
    # Qiskit's drawer leaves the figure open; close it so long test runs do not
    # pile up figures in memory.
    from matplotlib import pyplot as plt

    plt.close(figure)
    return path


def render_counts(
    counts: Mapping[str, float],
    output: str | Path,
    *,
    title: str = "Measurement results",
    xlabel: str = "measured bit",
    ylabel: str = "count",
    rotation: float = 0.0,
) -> Path:
    """Render a bar chart of measurement results on a dark background.

    Values need not be counts: any numeric mapping works, so the same chart can
    show e.g. measurement *probabilities* or a fidelity. ``rotation`` tilts the
    tick labels, which a chart with many labels (a whole register, say) needs.
    """
    path = _prepare(output)
    from matplotlib import pyplot as plt

    with plt.style.context(DARK_PLOT_STYLE):
        fig, ax = plt.subplots(figsize=(5, 4))
        labels = list(counts)
        values = [counts[label] for label in labels]
        bars = ax.bar(labels, values, color="#5aa9ff")
        ax.bar_label(bars)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        if rotation:
            plt.setp(ax.get_xticklabels(), rotation=rotation, ha="right")
        fig.savefig(path)
        plt.close(fig)
    return path


def render_grouped_counts(
    series: Sequence[tuple[str, Mapping[str, float]]],
    output: str | Path,
    *,
    title: str = "Measurement results",
    xlabel: str = "measured two-bit outcome",
    ylabel: str = "count",
    rotation: float = 0.0,
    bar_labels: bool = True,
) -> Path:
    """Render grouped bars (one bar per series) for several count dictionaries.

    Values need not be counts: any numeric mapping works, so the same chart can
    show e.g. measurement *probabilities* or a fidelity. ``rotation`` tilts the
    tick labels, which a chart with many labels (a whole register, say) needs;
    set ``bar_labels`` to ``False`` to drop the per-bar value labels when there
    are too many bars for them to stay legible.
    """
    path = _prepare(output)
    from matplotlib import pyplot as plt

    labels = sorted({label for _, counts in series for label in counts})
    positions = np.arange(len(labels))
    width = 0.8 / max(len(series), 1)
    with plt.style.context(DARK_PLOT_STYLE):
        fig, ax = plt.subplots(figsize=(7, 4.5))
        for offset, (name, counts) in enumerate(series):
            values = [counts.get(label, 0) for label in labels]
            bars = ax.bar(positions + offset * width, values, width, label=name)
            if bar_labels:
                ax.bar_label(bars, fontsize=8)
        ax.set_xticks(positions + width * (len(series) - 1) / 2)
        ax.set_xticklabels(labels, rotation=rotation, ha="right" if rotation else "center")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontsize=11)
        ax.legend()
        fig.tight_layout()
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


def render_matrices(
    matrices: Sequence[tuple[str, np.ndarray]],
    output: str | Path,
    *,
    title: str | None = None,
    figsize: tuple[float, float] | None = None,
    fontsize: float = 9.0,
) -> Path:
    """Render gate matrices as labelled heatmaps on a dark background.

    ``figsize`` overrides the default width (``3.2`` inches per matrix) and
    ``fontsize`` the cell labels, which is worth raising the size for when a
    matrix is large — the Toffoli gate of Chapter 7 is 8x8.
    """
    path = _prepare(output)
    from matplotlib import pyplot as plt

    with plt.style.context(DARK_PLOT_STYLE):
        columns = len(matrices)
        fig, axes = plt.subplots(1, columns, figsize=figsize or (3.2 * columns, 3.6))
        axes = np.atleast_1d(axes)
        for ax, (label, matrix) in zip(axes, matrices, strict=True):
            values = np.real_if_close(matrix)
            image = ax.imshow(values, cmap="coolwarm", vmin=-1, vmax=1)
            ax.set_title(label)
            ax.set_xticks(range(matrix.shape[1]))
            ax.set_yticks(range(matrix.shape[0]))
            for row in range(matrix.shape[0]):
                for column in range(matrix.shape[1]):
                    value = matrix[row, column]
                    text = f"{value.real:.2f}" if abs(value.imag) < 1e-9 else f"{value:.2f}"
                    ax.text(column, row, text, ha="center", va="center", color="white", fontsize=fontsize)
            fig.colorbar(image, ax=ax, fraction=0.046)
        if title is not None:
            fig.suptitle(title)
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
    return path
