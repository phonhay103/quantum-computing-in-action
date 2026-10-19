"""Chapter 8 — the Hadamard trick: a base you can rotate into and back.

The book opens the secure-communication chapter with the ``haha`` sample: flip
``q0`` with an ``X``, then apply a Hadamard to both qubits *twice*. The second
Hadamard undoes the first, so the two qubits come out exactly where they started
(``q0 = |1>``, ``q1 = |0>``).

That identity — ``H·H = I`` — is the whole reason bases exist. Rotating into the
X base costs nothing as long as you rotate back before measuring. Measure
*without* rotating back and the state looks completely random, which is what an
interceptor who does not know the base runs into.

The chapter's other lesson is here too: setting a qubit to ``|1>`` and reading it
back gives ``1``, because a single bit travels fine when nobody uses a second
base. It is only the *base* that turns a readable bit into a coin flip.
"""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_bloch, render_circuit

#: Two qubits: one carries a bit, the other is left alone for contrast.
N_QUBITS = 2


def _steps() -> list[tuple[str, QuantumCircuit]]:
    """Return the circuit after each step, so the state can be inspected."""
    sequence: list[tuple[str, QuantumCircuit]] = []
    circuit = QuantumCircuit(N_QUBITS)
    sequence.append(("start: |00>", circuit.copy()))
    circuit.x(0)
    sequence.append(("X(0)", circuit.copy()))
    circuit.h(0)
    circuit.h(1)
    sequence.append(("H(0), H(1)", circuit.copy()))
    circuit.h(0)
    circuit.h(1)
    sequence.append(("H(0), H(1) again", circuit.copy()))
    return sequence


def haha_circuit() -> QuantumCircuit:
    """Return the book's ``haha`` circuit with both qubits measured."""
    circuit = QuantumCircuit(N_QUBITS, N_QUBITS)
    circuit.x(0)
    circuit.h(0)
    circuit.h(1)
    circuit.h(0)
    circuit.h(1)
    for qubit in range(N_QUBITS):
        circuit.measure(qubit, qubit)
    return circuit


def step_states() -> list[tuple[str, Statevector]]:
    """Return the state after each step of :func:`haha_circuit`."""
    return [(label, Statevector.from_instruction(circuit)) for label, circuit in _steps()]


def draw(output: str | Path = "build/ch08-haha-circuit.png") -> Path:
    """Render the ``haha`` circuit and save it to ``output``."""
    return render_circuit(haha_circuit(), output)


def main() -> None:
    explain(
        "Chapter 8 — a base you can rotate into and back",
        """
Secure communication starts with a rule about measurements. A qubit is written
in some **base**: the usual `Z` base with states `|0>` and `|1>`, or the `X` base
with `|+>` and `|->`. A Hadamard rotates one into the other.

The catch is that **H·H = I**: two Hadamards are one full turn, so the state comes
back untouched. Apply an `X` to set a bit, then a Hadamard, then another Hadamard,
and you are exactly where you began:

    |0>  --X-->  |1>  --H-->  |->  --H-->  |1>

The `X` set the bit; the two Hadamards added a base and took it away again. Nothing
was lost, and measuring at the end still gives the original `1`.

Now the other half of the story. Measure in the *wrong* base and even a perfectly
prepared qubit answers with a fair coin. `H·H = I` is what makes a base a choice
you can hide behind: someone who does not know Alice's base is guessing, and a
guess is wrong half the time. That is the seed of BB84.
""",
    )

    steps(
        "Chapter 8 — rotating into a base and back",
        [
            ("Start", "|00> — q0 and q1 both |0>"),
            ("X(0)", "q0 is |1> — a bit, in the Z base"),
            ("H(0), H(1)", "q0 is |->, q1 is |+>: both moved into the X base"),
            ("H(0), H(1) again", "H·H = I — q0 is |1> and q1 is |0> again"),
        ],
    )

    console.rule("Two Hadamards are one round trip")
    for label, state in step_states():
        probabilities = state.probabilities_dict()
        p0 = float(probabilities.get("00", 0.0))
        p1 = float(probabilities.get("01", 0.0))
        p2 = float(probabilities.get("10", 0.0))
        p3 = float(probabilities.get("11", 0.0))
        console.print(f"  [bits]{label:<22}[/bits] P(q1,q0)=00:{p0:.2f} 01:{p1:.2f} 10:{p2:.2f} 11:{p3:.2f}")
    console.print(
        "[muted]Row 2 (after X) and row 4 (after the second Hadamards) are identical: the two "
        "Hadamards cancelled, so the bit survives and q1 never moved. Row 3 is the detour through "
        "the X base — every outcome equally likely, and no trace of it left at the end.[/muted]"
    )

    circuit_path = draw()
    bloch_path = render_bloch(
        list(step_states()),
        "build/ch08-haha-bloch.png",
        title="H·H = I: a base you can rotate into and back",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, bloch_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
