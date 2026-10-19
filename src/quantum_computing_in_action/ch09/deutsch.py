"""Chapter 9 — the Deutsch algorithm: one query, two answers.

Deutsch's problem is the smallest interesting quantum question. You are handed a
one-bit function ``f`` as an oracle and asked only *what kind* it is:

* **constant** (``f(0) = f(1)``), or
* **balanced** (``f(0) != f(1)``)?

Classically you must look at both inputs, two queries. Quantumly, **one** query is
enough, and the circuit is tiny:

    X(1)                     prepare the spare register in |1>
    H(0), H(1)               put both registers in superposition
    oracle                   evaluate f once, on both inputs at the same time
    H(0)                     interfere the two paths
    measure q0              0 -> constant, 1 -> balanced

The reason it works is the **phase kickback** of the oracle: with ``q1`` prepared
in ``|->``, evaluating ``U_f`` on a superposition ``|x>`` flips the *sign* of the
``|x>`` component whenever ``f(x) = 1``. A constant function flips nothing (or
everything, which is a global phase and invisible); a balanced function flips one
term relative to the other. The final Hadamard turns that relative sign into a
definite bit.
"""

from __future__ import annotations

from pathlib import Path

from qiskit import QuantumCircuit
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_counts
from quantum_computing_in_action.ch07.circuits import Builder, prob_one_per_qubit, state_after
from quantum_computing_in_action.ch09.oracles import ORACLES, Oracle

#: Short labels for the four one-bit functions, used in charts.
SHORT_NAMES: dict[str, str] = {
    "constant 0": "const 0",
    "constant 1": "const 1",
    "balanced: f(x) = x": "f(x) = x",
    "balanced: f(x) = NOT x": "f(x) = NOT x",
}


def _builder(oracle: Oracle) -> Builder:
    """Return the Deutsch circuit's gates up to (not including) the measurement."""

    def build(circuit: QuantumCircuit) -> None:
        circuit.x(1)
        circuit.h(0)
        circuit.h(1)
        oracle.build(circuit)
        circuit.h(0)

    return build


def deutsch_circuit(oracle: Oracle, *, measure: bool = True) -> QuantumCircuit:
    """Return the Deutsch circuit for ``oracle`` (``q0`` is the answer).

    Only ``q0`` is measured: one bit is the entire answer.
    """
    circuit = QuantumCircuit(2, 1)
    _builder(oracle)(circuit)
    if measure:
        circuit.measure(0, 0)
    return circuit


def prob_one(oracle: Oracle) -> float:
    """Return ``P(q0 = 1)`` after one query — the probability the answer is "balanced"."""
    state = state_after(_builder(oracle), 2)
    return prob_one_per_qubit(state)[0]


def deutsch_result(oracle: Oracle) -> int:
    """Return the measured bit: ``0`` for a constant function, ``1`` for a balanced one."""
    return 1 if prob_one(oracle) > 0.5 else 0


def classify(oracle: Oracle) -> str:
    """Return ``"constant"`` or ``"balanced"`` from a single query."""
    return "balanced" if deutsch_result(oracle) == 1 else "constant"


def draw(output: str | Path = "build/ch09-deutsch-circuit.png") -> Path:
    """Render the Deutsch circuit for the balanced ``f(x) = x`` oracle."""
    oracle = next(item for item in ORACLES if item.name == "balanced: f(x) = x")
    return render_circuit(deutsch_circuit(oracle), output)


def _results_table() -> Table:
    table = Table(title="Deutsch, one query per function", header_style="heading")
    table.add_column("function", style="bits")
    table.add_column("f(0)", style="value")
    table.add_column("f(1)", style="value")
    table.add_column("measured q0", style="value")
    table.add_column("verdict", style="value")
    for oracle in ORACLES:
        table.add_row(
            SHORT_NAMES[oracle.name],
            str(oracle.f(0)),
            str(oracle.f(1)),
            str(deutsch_result(oracle)),
            classify(oracle),
        )
    return table


def main() -> None:
    explain(
        "Chapter 9 — the Deutsch algorithm",
        """
Deutsch's problem gives you a one-bit function as a sealed **oracle** and asks a
single yes/no question: is it **constant** (`f(0) = f(1)`) or **balanced**
(`f(0) != f(1)`)?

Classically the question needs both inputs looked at — two queries. Quantumly one
query is enough, and the trick is the same **phase kickback** that will power
Deutsch—Jozsa and Grover.

Prepare the spare register in `|->`, then run the oracle on a superposition:

    X(1), H(0), H(1)          q0 = (|0> + |1>)/sqrt(2),  q1 = |->
    oracle                    U_f
    H(0)                      interfere the two branches

With `q1` in `|->`, the oracle leaves both registers alone but multiplies the whole
state by `(-1)^f(x)`: it writes the function's value into the **sign**. Now the two
branches of `q0` carry `(-1)^f(0)` and `(-1)^f(1)`.

* If `f` is **constant**, both signs are equal and the final Hadamard brings `q0`
  back to `|0>`. Measurement gives `0`.
* If `f` is **balanced**, the signs differ — a relative minus sign — and the final
  Hadamard turns `q0` into `|1>`. Measurement gives `1`.

Follow the balanced oracle `f(x) = x` in amplitudes:

    start        |0>|1>
    H(0), H(1)   (|0>+|1>)/sqrt(2)  x  (|0>-|1>)/sqrt(2)
    oracle       (|0>-|1>)/sqrt(2)  x  |->    x=1 branch gets a minus
    H(0)         |1>  x  |->
    measure q0   1  ->  balanced

The constant-0 oracle changes nothing in step 3, so `H(0)` sends `|+>` back to
`|0>`: measurement `0`, constant. Same circuit, one bit of answer, one query.

One query. Constant leaves the qubit where it was; balanced flips it. The next
section scales the same idea from one bit to `n`.
""",
    )

    steps(
        "Chapter 9 — the Deutsch circuit",
        [
            ("X(1)", "the spare register becomes |1>"),
            ("H(0), H(1)", "both registers in superposition; q1 is |->"),
            ("oracle", "one evaluation writes (-1)^f(x) into the sign of q0"),
            ("H(0)", "constant -> |0>, balanced -> |1>"),
            ("measure q0", "the full answer, from a single query"),
        ],
    )

    console.rule("One query per function")
    console.print(_results_table())
    console.print(
        "[muted]The two constant functions measure 0 and the two balanced functions measure 1 — "
        "always, with certainty, after a single oracle call.[/muted]"
    )

    circuit_path = draw()
    outcomes_path = render_counts(
        {SHORT_NAMES[oracle.name]: prob_one(oracle) for oracle in ORACLES},
        "build/ch09-deutsch-outcomes.png",
        title="One query: constant measures 0, balanced measures 1",
        xlabel="function",
        ylabel="P(q0 = 1)",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, outcomes_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
