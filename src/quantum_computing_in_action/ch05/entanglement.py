"""Chapter 5 — entanglement: the CNOT gate and Bell states."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.panel import Panel
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import (
    render_circuit,
    render_counts,
    render_grouped_counts,
    render_matrices,
)
from quantum_computing_in_action.ch05 import states


def _bell_preparation() -> QuantumCircuit:
    """A two-qubit circuit that prepares the Bell state ``(|00> + |11>) / sqrt(2)``.

    A Hadamard on qubit 0 puts it in superposition, then ``CNOT(0, 1)`` flips
    qubit 1 exactly when qubit 0 is ``1``. The two qubits can no longer be
    described separately.
    """
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    return circuit


def bell_circuit() -> QuantumCircuit:
    """The Bell-state circuit plus a measurement of both qubits."""
    circuit = _bell_preparation()
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit


def bell_statevector() -> Statevector:
    """Return the state vector produced by the Bell-state preparation."""
    return Statevector.from_instruction(_bell_preparation())


def _sampled_counts(circuit: QuantumCircuit, shots: int) -> dict[str, int]:
    base = circuit.copy()
    base.remove_final_measurements(inplace=True)
    state = Statevector.from_instruction(base)
    return {str(bit): int(count) for bit, count in state.sample_counts(shots).items()}


def bell_counts(shots: int = 1000) -> dict[str, int]:
    """Measure the Bell state ``shots`` times; only ``00`` and ``11`` appear."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    return _sampled_counts(bell_circuit(), shots)


def _independent_preparation() -> QuantumCircuit:
    """A two-qubit circuit with one Hadamard **per** qubit (no CNOT).

    Each qubit is random on its own, but the joint state is a plain **product**
    state: knowing one outcome tells you nothing about the other.
    """
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.h(1)
    return circuit


def independent_qubits_circuit() -> QuantumCircuit:
    """The two-independent-Hadamard circuit plus measurements."""
    circuit = _independent_preparation()
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit


def independent_counts(shots: int = 1000) -> dict[str, int]:
    """Measure two independent ``H`` qubits; all four outcomes appear (~25% each)."""
    if shots < 1:
        raise ValueError("shots must be at least 1")
    return _sampled_counts(independent_qubits_circuit(), shots)


def classical_two_coins(shots: int = 1000) -> dict[str, int]:
    """Toss two independent classical coins ``shots`` times.

    This is the classical baseline: like the two ``H`` qubits it produces all
    four outcomes, because neither system is entangled.
    """
    if shots < 1:
        raise ValueError("shots must be at least 1")
    counts = {"00": 0, "01": 0, "10": 0, "11": 0}
    for _ in range(shots):
        coin_a = random.getrandbits(1)
        coin_b = random.getrandbits(1)
        counts[f"{coin_a}{coin_b}"] += 1
    return counts


def _label_circuit(label: str) -> QuantumCircuit:
    """Prepare the two-qubit basis state ``label`` (leftmost character = qubit 1)."""
    circuit = QuantumCircuit(2)
    for index, bit in enumerate(reversed(label)):
        if bit == "1":
            circuit.x(index)
    return circuit


def cnot_circuit() -> QuantumCircuit:
    """A bare ``CNOT(0, 1)`` circuit with measurements (used for the truth table)."""
    circuit = QuantumCircuit(2, 2)
    circuit.cx(0, 1)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit


def cnot_truth_table() -> list[tuple[str, str]]:
    """Return ``(input, output)`` pairs for ``CNOT(0, 1)`` on the four basis states."""
    table: list[tuple[str, str]] = []
    for label in states.BASIS_LABELS:
        circuit = _label_circuit(label)
        circuit.cx(0, 1)
        probabilities = Statevector.from_instruction(circuit).probabilities_dict()
        output = max(probabilities, key=lambda key: probabilities[key])
        table.append((label, str(output)))
    return table


def draw(output: str | Path = "build/ch05-bell-circuit.png", *, cnot: bool = False) -> Path:
    """Render the Bell circuit (or the bare CNOT circuit) and save it to ``output``."""
    circuit = cnot_circuit() if cnot else bell_circuit()
    return render_circuit(circuit, output)


def _amplitude_matrix(state: Statevector) -> np.ndarray:
    """Reshape a two-qubit state vector into its 2x2 coefficient matrix."""
    return np.asarray(state.data, dtype=complex).reshape(2, 2)


def main() -> None:
    explain(
        "Chapter 5 — Entanglement",
        """
Two qubits are described by the **tensor product** of their states, giving four
basis states: `|00>`, `|01>`, `|10>`, `|11>`.

The **CNOT gate** has a control and a target. It flips the target exactly when
the control is `1`. Applied after a Hadamard, it produces a **Bell state**:

`H(0)` then `CNOT(0,1)`  ->  `(|00> + |11>) / sqrt(2)`

Measure this state and you only ever see `00` or `11` — never `01` or `10`. The
two qubits are **entangled**: each looks 50/50 on its own, yet their outcomes are
perfectly correlated. Contrast that with two independent Hadamard qubits, which
produce all four outcomes with equal probability.
""",
    )

    bell_state = bell_statevector()
    bell = bell_counts(1000)
    independent = independent_counts(1000)
    coins = classical_two_coins(1000)
    table = cnot_truth_table()

    steps(
        "Chapter 5 — step by step",
        [
            ("Prepare two qubits in |00>", "both qubits definite"),
            ("Apply H to qubit 0", "qubit 0 becomes 50/50, qubit 1 stays |0>"),
            ("Apply CNOT(0,1)", "qubit 1 becomes correlated with qubit 0"),
            ("Measure both", "only 00 or 11, each about half the time"),
        ],
    )

    console.rule("The CNOT truth table")
    truth = Table(title="CNOT(0,1): flip the target when the control is 1", header_style="heading")
    truth.add_column("input", style="bits")
    truth.add_column("output", style="value")
    for input_label, output_label in table:
        truth.add_row(f"|{input_label}>", f"|{output_label}>")
    console.print(truth)

    console.rule("Bell state vs. independent qubits")
    console.print(
        "Bell state amplitudes: "
        + ", ".join(
            f"[value]{label}[/value]={amplitude.real:+.3f}"
            for label, amplitude in states.amplitudes(bell_state.data).items()
        )
    )
    console.print(
        "Bell 1000 runs: "
        f"[zero]00={bell.get('00', 0)}[/zero], [one]11={bell.get('11', 0)}[/one] "
        f"(01 and 10 never appear)."
    )
    console.print(
        "Independent 1000 runs: "
        + ", ".join(f"{label}={independent.get(label, 0)}" for label in states.BASIS_LABELS)
    )
    console.print(
        "Two classical coins: "
        + ", ".join(f"{label}={coins.get(label, 0)}" for label in states.BASIS_LABELS)
    )
    console.print("[muted]The Bell qubits are correlated; the independent qubits and coins are not.[/muted]")

    console.print(Panel(str(bell_circuit().draw("text")), title="Bell circuit", border_style="bits"))
    console.print(Panel(str(cnot_circuit().draw("text")), title="CNOT(0,1)", border_style="bits"))

    circuit_path = draw()
    cnot_path = draw("build/ch05-cnot-circuit.png", cnot=True)
    bell_counts_path = render_counts(bell, "build/ch05-bell-counts.png", title="1000 runs of the Bell state")
    independent_counts_path = render_counts(
        independent, "build/ch05-independent-counts.png", title="1000 runs of two independent H qubits"
    )
    comparison_path = render_grouped_counts(
        [("independent H", independent), ("Bell (entangled)", bell)],
        "build/ch05-bell-vs-independent.png",
        title="Independent vs. entangled qubits",
    )
    matrices_path = render_matrices(
        [
            ("independent (rank 1)", _amplitude_matrix(Statevector.from_instruction(_independent_preparation()))),
            ("Bell (rank 2)", _amplitude_matrix(bell_state)),
        ],
        "build/ch05-amplitude-matrices.png",
        title="Coefficient matrices: product state vs. entangled state",
    )

    console.print("Saved diagrams:")
    for path in (
        circuit_path,
        cnot_path,
        bell_counts_path,
        independent_counts_path,
        comparison_path,
        matrices_path,
    ):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
