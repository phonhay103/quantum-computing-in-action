"""Chapter 6 — controlled-Z and measurement: a change you cannot see.

This module answers the Chapter 6 exercise "Pauli-Z gate and Measurement" (the
book's ``hczmeasure`` sample), and it is the chapter's sharpest illustration of
what a measurement does *not* tell you.

``CZ`` differs from ``CNOT`` in exactly one way: instead of flipping the target's
bit, it flips the target's **phase**. On a pair of superpositions that is enough
to change the nature of the state completely:

* ``H(0), H(1)`` prepares ``|+>`` on both qubits, a **product state**. Measuring
  the pair gives all four outcomes at 25% each.
* Adding ``CZ(0, 1)`` flips the sign of the ``|11>`` amplitude and turns that
  product state into an **entangled** one — yet the four outcomes stay at 25%
  each, because the Born rule squares amplitudes.

So ``CZ`` changed something real and a computational-basis measurement reports
the same histogram either way. Seeing the difference needs a *different*
measurement basis, which is exactly the idea teleportation then builds on.

For contrast, ``CZ`` is completely inert after a *lone* ``H``: qubit 1 stays
``|0>``, the control never fires, and nothing happens at all.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_grouped_counts, render_matrices
from quantum_computing_in_action.ch05.states import schmidt_rank
from quantum_computing_in_action.ch06.protocol import Builder, gate, measure, run, sample_counts

#: The two-qubit basis labels, in Chapter 5's control-first order: the leftmost
#: character is qubit 1. Note that Qiskit indexes a state vector the other way
#: round, so :func:`_counts` re-keys the sampled labels to match.
BASIS_LABELS: tuple[str, ...] = ("00", "01", "10", "11")

#: How each sample starts the two qubits, keyed by the name used everywhere else.
#: ``h`` is the book's ``hczmeasure`` sample. ``hh`` puts *both* qubits in a
#: superposition — the case where all four outcomes can appear. ``bell`` is the
#: entangled contrast.
PREPARATIONS: dict[str, Builder] = {
    "none": lambda circuit: None,
    "h": lambda circuit: circuit.h(0),
    "hh": lambda circuit: (circuit.h(0), circuit.h(1)),
    "bell": lambda circuit: (circuit.h(0), circuit.cx(0, 1)),
}


def _cz(circuit: QuantumCircuit) -> None:
    """Apply the controlled-Z gate: a phase flip, not a bit flip."""
    circuit.cz(0, 1)


def _state_after(builder: Builder) -> Statevector:
    """Return the two-qubit state a builder reaches, before any measurement."""
    circuit = QuantumCircuit(2)
    builder(circuit)
    return Statevector.from_instruction(circuit)


def cz_circuit(preparation: str = "h") -> QuantumCircuit:
    """Return the circuit ``H`` (optionally) then ``CZ``, with both qubits measured.

    Args:
        preparation: how to start the two qubits; see :data:`PREPARATIONS`.

    Raises:
        ValueError: for an unknown preparation.
    """
    circuit = QuantumCircuit(2, 2)
    _prepare_then_cz(preparation)(circuit)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit


def _prepare_then_cz(preparation: str) -> Builder:
    """Return the builder for ``preparation`` followed by ``CZ``."""
    if preparation not in PREPARATIONS:
        raise ValueError(f"preparation must be one of {sorted(PREPARATIONS)}, got {preparation!r}")

    def build(circuit: QuantumCircuit) -> None:
        PREPARATIONS[preparation](circuit)
        _cz(circuit)

    return build


def cz_statevector(preparation: str = "h") -> Statevector:
    """Return the state :func:`cz_circuit` reaches, before measurement."""
    return _state_after(_prepare_then_cz(preparation))


def _counts(builder: Builder, shots: int, *, seed: int | None = None) -> dict[str, int]:
    """Measure the pair after ``builder`` and count the outcomes."""
    frames = run([gate(builder, 2), measure(0, 1)], n_qubits=2)
    sampled = sample_counts(frames, shots, seed=seed)
    # Qiskit labels a two-qubit outcome with qubit 1 on the right; Chapter 5 (and
    # these notes) put qubit 1 on the left, so reverse each label.
    return {label[::-1]: sampled[label] for label in sampled}


def cz_counts(shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Measure a Hadamard on *both* qubits then ``CZ``: four outcomes, 25% each.

    Both qubits start in ``|+>``, so all four basis states have amplitude 1/2.
    ``CZ`` then flips the sign of the ``|11>`` amplitude — the only thing it does
    here — and the Born rule makes that change invisible: still four outcomes at
    25% each, and still a product state.
    """
    return _counts(_prepare_then_cz("hh"), shots, seed=seed)


def bell_counts(shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Measure the Bell state then ``CZ``: only ``00`` and ``11``.

    ``CNOT`` entangles the pair and ``CZ`` adds a relative sign that costs no
    probability, so the outcome set is unchanged from Chapter 5's Bell state.
    """
    return _counts(_prepare_then_cz("bell"), shots, seed=seed)


def amplitudes(state: Statevector) -> dict[str, complex]:
    """Return the four amplitudes of ``state`` keyed by :data:`BASIS_LABELS`."""
    return {label: complex(state.data[int(label, 2)]) for label in BASIS_LABELS}


def probabilities(state: Statevector) -> dict[str, float]:
    """Return a two-qubit state's measurement probabilities (the Born rule)."""
    return {label: float(abs(amplitude) ** 2) for label, amplitude in amplitudes(state).items()}


def _state_of(preparation: str) -> Statevector:
    """Return the state a preparation reaches, with no ``CZ`` applied."""
    circuit = QuantumCircuit(2)
    PREPARATIONS[preparation](circuit)
    return Statevector.from_instruction(circuit)


def _builder_only(preparation: str) -> Builder:
    """Return a builder that prepares the pair without applying ``CZ``."""

    def build(circuit: QuantumCircuit) -> None:
        PREPARATIONS[preparation](circuit)

    return build


def plain_counts(preparation: str = "hh", shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Measure the pair after ``preparation`` alone, with no ``CZ``."""
    return _counts(_builder_only(preparation), shots, seed=seed)


def cz_effect(preparation: str = "hh") -> dict[str, float]:
    """Return how far ``CZ`` moved each amplitude of a prepared state.

    The whole effect of the gate is one sign: the ``|11>`` amplitude flips and the
    other three stay put. Because the Born rule *squares* amplitudes, no
    measurement probability moves with it — which is why the phase cannot be seen
    in a count histogram.

    On ``"h"`` the change is zero everywhere: qubit 1 stays ``|0>``, so the control
    never fires.
    """
    before = _state_of(preparation)
    after = cz_statevector(preparation)
    return {label: float(abs(after.data[i] - before.data[i])) for i, label in enumerate(BASIS_LABELS)}


def entanglement_rank(preparation: str, *, with_cz: bool = True) -> int:
    """Return the Schmidt rank (1 = product state, 2 = entangled) of the pair.

    This is where ``CZ`` earns its reputation: on ``"hh"`` the rank jumps from 1
    to 2, so the gate really does entangle the qubits — and :func:`cz_counts`
    still returns four outcomes at 25% each either way.
    """
    circuit = QuantumCircuit(2)
    PREPARATIONS[preparation](circuit)
    if with_cz:
        _cz(circuit)
    return schmidt_rank(Statevector.from_instruction(circuit).data)


def amplitude_matrix(state: Statevector) -> np.ndarray:
    """Reshape a two-qubit state into its 2x2 coefficient matrix.

    As in Chapter 5: rank 1 means the state factorises (a product state), rank 2
    means it is entangled.
    """
    return np.asarray(state.data, dtype=complex).reshape(2, 2)


def draw(output: str | Path = "build/ch06-cz-circuit.png") -> Path:
    """Render the ``H`` + ``CZ`` circuit and save it to ``output``."""
    return render_circuit(cz_circuit(), output, reverse_bits=True)


def main() -> None:
    explain(
        "Chapter 6 — controlled-Z and measurement",
        """
Chapter 5 used `CNOT` to **correlate** two qubits: apply `H`, then `CNOT`, and
the pair becomes a Bell state whose outcomes always agree. This is the book's
Chapter 6 exercise, and it asks what the *other* two-qubit gate does.

`CZ`, the **controlled-Z** gate, looks like `CNOT` but flips the target's
**phase** instead of its bit. Put both qubits in a superposition and apply it:

    H(0), H(1)          ->  ( |00> + |01> + |10> + |11> ) / 2   product state
    then CZ(0, 1)       ->  ( |00> + |01> + |10> - |11> ) / 2   entangled

That single sign flip changes the state completely: the coefficient matrix goes
from rank 1 to rank 2, so the qubits are no longer independent. You cannot write
the new state as `|a> |b>`.

Now measure both qubits. You get **all four outcomes at 25% each** — the very
same histogram as before the gate. `CZ` flipped the sign of the `|11>` amplitude
and the Born rule *squares* amplitudes, so |-1/2|² = |+1/2|².

So the state changed and the measurement did not notice. That is the lesson:
measurement probabilities do not determine a state. Detecting the difference
needs a *different* measurement basis — which is precisely what the next section
on teleportation uses.

Two contrast cases:

* `CZ` on a **lone** `H` does nothing at all: qubit 1 stays |0>, so the control
  never fires.
* `CZ` on the **Bell state** flips the same single sign; the probabilities stay at
  50/50 and the outcome set stays {00, 11}, because `CNOT` had already done the
  correlating.
""",
    )

    both_h = _state_of("hh")
    both_h_cz = cz_statevector("hh")
    bell = _state_of("bell")
    bell_cz = cz_statevector("bell")

    steps(
        "Chapter 6 — step by step",
        [
            ("Apply H to q0 and q1", "both qubits are |+>, so all four outcomes are possible"),
            ("Check the state", "coefficient-matrix rank 1 — the qubits are still independent"),
            ("Apply CZ(0, 1)", "only the |11> amplitude flips sign; the rank becomes 2 — now entangled"),
            ("Measure both qubits", "still four outcomes at 25% each: the change is invisible here"),
        ],
    )

    console.rule("What CZ changes: one sign, and the rank")
    phase_table = Table(title="H on q0 and q1, then CZ(0, 1)", header_style="heading")
    phase_table.add_column("state", style="bits")
    phase_table.add_column("amplitude before CZ", style="value")
    phase_table.add_column("amplitude after CZ", style="value")
    phase_table.add_column("probability (unchanged)", style="value")
    before = amplitudes(both_h)
    after = amplitudes(both_h_cz)
    probs = probabilities(both_h_cz)
    for label in BASIS_LABELS:
        moved = abs(after[label] - before[label]) > 1e-9
        marker = " [muted](sign flipped)[/muted]" if moved else ""
        phase_table.add_row(
            f"|{label}>",
            f"{before[label]:+.3f}",
            f"{after[label]:+.3f}{marker}",
            f"{probs[label]:.2f}",
        )
    console.print(phase_table)

    rank_table = Table(title="The state really changed — the histogram does not say so", header_style="heading")
    rank_table.add_column("state", style="bits")
    rank_table.add_column("coefficient-matrix rank", style="value")
    rank_table.add_column("reading", style="muted")
    for preparation, plain, gated in (
        ("H on q0 and q1", entanglement_rank("hh", with_cz=False), entanglement_rank("hh")),
        ("lone H on q0", entanglement_rank("h", with_cz=False), entanglement_rank("h")),
        ("Bell state", entanglement_rank("bell", with_cz=False), entanglement_rank("bell")),
    ):
        verdict = "unchanged by CZ"
        if plain != gated:
            verdict = f"entangled by CZ: {plain} -> {gated}"
        rank_table.add_row(preparation, f"{plain} -> {gated}", verdict)
    console.print(rank_table)
    console.print(
        "[muted]On two superpositions CZ takes the state from a product state to an entangled "
        "one — the sign flip changes the rank from 1 to 2 — yet every probability stays at 1/4, "
        "because the Born rule squares amplitudes.[/muted]"
    )

    console.rule("Bell + CZ: the same invisible sign")
    bell_table = Table(title="Bell state, then CZ(0, 1)", header_style="heading")
    bell_table.add_column("state", style="bits")
    bell_table.add_column("amplitude before CZ", style="value")
    bell_table.add_column("amplitude after CZ", style="value")
    bell_table.add_column("probability (unchanged)", style="value")
    bell_before = amplitudes(bell)
    bell_after = amplitudes(bell_cz)
    bell_probs = probabilities(bell_cz)
    for label in BASIS_LABELS:
        moved = abs(bell_after[label] - bell_before[label]) > 1e-9
        marker = " [muted](sign flipped)[/muted]" if moved else ""
        bell_table.add_row(
            f"|{label}>",
            f"{bell_before[label]:+.3f}",
            f"{bell_after[label]:+.3f}{marker}",
            f"{bell_probs[label]:.2f}",
        )
    console.print(bell_table)

    console.rule("What measurement sees")
    cz_sample = cz_counts(1000, seed=3)
    plain_sample = plain_counts("hh", 1000, seed=3)
    bell_sample = bell_counts(1000, seed=3)
    console.print(
        "  [heading]H+H:      [/heading]" + ", ".join(f"{label}={plain_sample.get(label, 0)}" for label in BASIS_LABELS)
    )
    console.print(
        "  [heading]H+H+CZ:   [/heading]" + ", ".join(f"{label}={cz_sample.get(label, 0)}" for label in BASIS_LABELS)
    )
    console.print(
        "  [heading]Bell+CZ:  [/heading]" + ", ".join(f"{label}={bell_sample.get(label, 0)}" for label in BASIS_LABELS)
    )
    console.print(
        "\n  [muted]The first two rows are indistinguishable by measurement even though the "
        "states are a product state and an entangled one respectively. Only the Bell pair's "
        "correlation — the outcome set shrinking to {00, 11} — is visible at all.[/muted]"
    )
    console.print(
        "[muted]Teleportation does exactly what `CZ` cannot: it recovers the state on the far "
        "side from the shared entanglement plus two classical bits. That recovery step is what "
        "makes a phase matter again.[/muted]"
    )

    circuit_path = draw()
    comparison_path = render_grouped_counts(
        [
            ("H + H (product)", plain_sample),
            ("H + H + CZ (entangled)", cz_sample),
            ("Bell + CZ (entangled)", bell_sample),
        ],
        "build/ch06-cz-vs-bell.png",
        title="CZ entangles the pair without changing any probability",
        xlabel="outcome of (q1, q0)",
        ylabel="count",
    )
    matrices_path = render_matrices(
        [
            ("H+H (rank 1)", amplitude_matrix(both_h)),
            ("H+H+CZ (rank 2)", amplitude_matrix(both_h_cz)),
            ("Bell (rank 2)", amplitude_matrix(bell)),
            ("Bell + CZ (rank 2)", amplitude_matrix(bell_cz)),
        ],
        "build/ch06-cz-matrices.png",
        title="Coefficient matrices: one sign flip takes rank 1 to rank 2",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, comparison_path, matrices_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
