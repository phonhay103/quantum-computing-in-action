"""Chapter 11 — the quantum Fourier transform: the period-finder's engine.

The quantum Fourier transform (QFT) is the discrete Fourier transform done by a
circuit. On a basis state it does nothing but spread a **phase ramp** across the
amplitudes:

    QFT |k>  =  (1/sqrt(N)) * sum_j  e^(2*pi*i*j*k/N) |j>

Read that as "a different ramp for every input". Its power for Shor is what
happens when the input is a **periodic** superposition: the ramps of all the
repetitions line up at multiples of ``N/r`` and cancel everywhere else. A period
hidden in the amplitudes becomes a set of sharp **peaks** in the measurement — and
that is the whole trick.

The matrix is the standard Fourier matrix ``F[j, k] = e^(2*pi*i*j*k/N) / sqrt(N)``:
unitary, symmetric, and its inverse is the same circuit run backwards.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_counts


def qft_matrix(n: int) -> np.ndarray:
    """Return the ``2^n x 2^n`` Fourier matrix ``F[j, k] = exp(2*pi*i*j*k/N)/sqrt(N)``.

    Raises:
        ValueError: if ``n`` is less than 1.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    N = 1 << n
    indices = np.arange(N)
    return np.exp(2j * np.pi * np.outer(indices, indices) / N) / np.sqrt(N)


def qft_circuit(n: int, *, inverse: bool = False) -> QuantumCircuit:
    """Return the QFT circuit (Hadamards and controlled-phase gates).

    ``inverse=True`` gives the adjoint — the same gates in reverse — which is what
    Shor applies at the end of order finding.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    circuit = QuantumCircuit(n)
    gate = QFTGate(n)
    circuit.append(gate.inverse() if inverse else gate, range(n))
    return circuit


def phase_ramp(n: int = 3) -> dict[int, float]:
    """Return the phase of each amplitude of ``QFT|1>``.

    Input ``|1>`` means ``k = 1``, so the amplitude at ``|j>`` is
    ``exp(2*pi*i*j/N)/sqrt(N)``: a uniform magnitude and a linear ramp of phase.
    This is the shape the transform is built from.
    """
    circuit = QuantumCircuit(n)
    circuit.x(0)  # |1>
    circuit.append(QFTGate(n), range(n))
    state = Statevector.from_instruction(circuit)
    return {index: float(np.angle(state.data[index])) for index in range(1 << n)}


def draw_circuit(output: str | Path = "build/ch11-qft-circuit.png") -> Path:
    """Render the three-qubit QFT circuit and save it to ``output``."""
    return render_circuit(qft_circuit(3), output)


def draw_phase(output: str | Path = "build/ch11-qft-phase.png") -> Path:
    """Render the phase ramp of ``QFT|1>`` and save it to ``output``."""
    return render_counts(
        {str(index): angle for index, angle in phase_ramp(3).items()},
        output,
        title="QFT|1>: a uniform magnitude, a linear phase ramp",
        xlabel="output index j",
        ylabel="phase of the amplitude (radians)",
    )


def _matrix_table(n: int) -> Table:
    table = Table(title=f"The {1 << n}x{1 << n} Fourier matrix (n = {n})", header_style="heading")
    table.add_column("j \\ k", style="muted")
    for column in range(1 << n):
        table.add_column(str(column), style="value")
    matrix = qft_matrix(n)
    for row in range(1 << n):
        table.add_row(
            str(row), *(f"{matrix[row, column].real:+.2f}{matrix[row, column].imag:+.2f}i" for column in range(1 << n))
        )
    return table


def main() -> None:
    explain(
        "Chapter 11 — the quantum Fourier transform",
        """
Shor's algorithm needs to find the **period** of `a^x mod N`. The tool that finds
it is the **quantum Fourier transform** (QFT), the discrete Fourier transform
written as a circuit.

The QFT turns a **phase** ramp into an even spread and an even spread into a
**phase** ramp — and, crucially, a *periodic* pattern into a few sharp **peaks**.
On a basis state `|k>` it produces

    QFT |k>  =  (1/sqrt(N)) * sum_j  e^(2*pi*i*j*k/N) |j>

a different ramp for every input. Feed it `|1>` and you get every output with the
same magnitude but a phase that sweeps steadily from 0 to `2*pi`.

The matrix is the familiar Fourier matrix `F[j,k] = e^(2*pi*i*j*k/N)/sqrt(N)`:
symmetric, unitary, and invertible by running the same circuit backwards. That
last property matters: after the oracle has built a periodic superposition, Shor
applies the **inverse** QFT and the period appears as a set of integers you can
measure.

The circuit itself is small — one Hadamard per qubit and a controlled phase gate
for every pair — but that is not the interesting part. The interesting part is
what happens to a periodic input, which is the next module.
""",
    )

    steps(
        "Chapter 11 — how the QFT is built",
        [
            ("Hadamard on q0", "the coarsest bit of the frequency"),
            ("Controlled phase gates", "each later qubit adds a finer phase to the earlier ones"),
            ("Hadamard on each qubit", "one per wire, coarse to fine"),
            ("Optional swap", "reverse the register; Shor needs no swap before measuring"),
        ],
    )

    console.rule("The Fourier matrix for n = 2")
    console.print(_matrix_table(2))
    console.print(
        "[muted]Every entry has magnitude 1/sqrt(N); only the phase changes. The matrix is unitary, "
        "so QFT is reversible, and its inverse is the same circuit run backwards.[/muted]"
    )

    matrix = qft_matrix(3)
    error = float(np.max(np.abs(matrix @ matrix.conj().T - np.eye(8))))
    console.print(f"  [muted]max |F F^dagger - I| for n = 3: {error:.1e} — unitary to machine precision.[/muted]")

    circuit_path = draw_circuit()
    phase_path = draw_phase()
    console.print("Saved diagrams:")
    for path in (circuit_path, phase_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
