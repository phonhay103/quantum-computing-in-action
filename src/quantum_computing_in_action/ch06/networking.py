"""Chapter 6 — networking basics: a byte over a socket, and why qubits differ.

The book starts Chapter 6 with the humblest possible network: one byte sent from
a process to another over a TCP socket (section 6.2.1). It then shows that the
same thing is *impossible* for a qubit, because you cannot copy an unknown state
(section 6.2.2, the no-cloning theorem).

Both halves live here:

* :func:`send_byte` opens a real socket on ``localhost`` and ships one byte,
  printing the sender's and receiver's progress the way the Java sample does.
* The copy half contrasts :func:`classic_copy` — a classical bit that survives
  being copied — with :func:`clone_attempt_state`, a CNOT-based attempt to clone
  a superposition. The attempt does not fail with an error; it fails quietly, and
  :func:`clone_attempts` tabulates how badly.
"""

from __future__ import annotations

import socket
import threading
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import DensityMatrix, Statevector, partial_trace, state_fidelity
from rich.table import Table

from quantum_computing_in_action._console import console, explain, steps
from quantum_computing_in_action._diagrams import render_circuit, render_counts, render_grouped_counts
from quantum_computing_in_action.ch06.protocol import Builder, gate, measure, run, sample_counts

#: The port used by the book's Java sample.
DEFAULT_PORT = 9753

#: The loopback address; the sample never leaves the machine.
HOST = "localhost"


def _identity(circuit: QuantumCircuit) -> None:
    """Prepare ``|0>``: a fresh circuit is already in the right state."""


def _minus(circuit: QuantumCircuit) -> None:
    """Prepare ``|-> = (|0> - |1>) / sqrt(2)``."""
    circuit.x(0)
    circuit.h(0)


#: The single-qubit states used to compare a real copy with clone attempts. The
#: keys are the bare labels, printed as ``|0>``, ``|+>``, ... by :func:`as_ket`.
TEST_STATES: dict[str, Builder] = {
    "0": _identity,
    "1": lambda circuit: circuit.x(0),
    "+": lambda circuit: circuit.h(0),
    "-": _minus,
}


def as_ket(label: str) -> str:
    """Return the ``|...>`` form of a state label."""
    return f"|{label}>"


def _check_state(state: str) -> None:
    if state not in TEST_STATES:
        raise ValueError(f"state must be one of {sorted(TEST_STATES)}, got {state!r}")


def _single(builder: Builder) -> QuantumCircuit:
    """Run a one-qubit builder on a fresh circuit."""
    circuit = QuantumCircuit(1)
    builder(circuit)
    return circuit


def _two(builder: Builder) -> QuantumCircuit:
    """Run a two-qubit builder on a fresh circuit."""
    circuit = QuantumCircuit(2)
    builder(circuit)
    return circuit


def send_byte(value: int = 0x8, *, port: int = DEFAULT_PORT, timeout: float = 5.0) -> int:
    """Send a single byte to a receiver on this machine and return what arrived.

    This mirrors the book's ``classic`` sample: a receiver binds the port and
    waits, a sender connects and writes, and both report their progress. Only
    ``localhost`` is involved, so nothing leaves the machine.

    Args:
        value: the byte to send; only the low 8 bits are used.
        port: the TCP port to use. Pass ``0`` to let the OS pick a free one,
            which is what the tests do to avoid clashing with a fixed port.
        timeout: seconds to wait for the connection and for the byte.

    Returns:
        The byte the receiver read back.

    Raises:
        ValueError: if ``value`` does not fit in a byte.
        OSError: if the socket fails.
        TimeoutError: if the receiver gets no byte.
    """
    if not 0 <= value <= 0xFF:
        raise ValueError("value must be a single byte (0-255)")

    payload = bytes([value])
    received: list[int] = []
    failures: list[BaseException] = []
    bound: list[int] = []

    def sender() -> None:
        try:
            console.print(f"[bits][Sender][/bits] Create a connection to port {bound[0]}")
            with socket.create_connection((HOST, bound[0]), timeout=timeout) as client:
                console.print(f"[bits][Sender][/bits] Write a byte: {value}")
                client.sendall(payload)
            console.print(f"[bits][Sender][/bits] Wrote a byte: {value}")
        except OSError as error:
            failures.append(error)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, port))
        # Port 0 means "any free port"; ask the OS which one it picked.
        bound.append(server.getsockname()[1])
        server.listen(1)
        console.print(f"[bits][Receiver][/bits] Starting to listen for incoming data at port {bound[0]}")
        thread = threading.Thread(target=sender, name="ch06-sender", daemon=True)
        thread.start()
        try:
            connection, _ = server.accept()
        except OSError as error:
            failures.append(error)
        else:
            with connection:
                connection.settimeout(timeout)
                chunk = connection.recv(1)
            if chunk:
                received.append(chunk[0])
                console.print(f"[bits][Receiver][/bits] Got a byte {chunk[0]}")
        thread.join(timeout)

    if failures:
        raise failures[0]
    if not received:
        raise TimeoutError("the receiver got no byte")
    return received[0]


def classic_copy(source: bool) -> bool:
    """Copy a classical bit and hand back the copy.

    The book's ``classiccopy`` sample makes a new ``Boolean`` holding the same
    value; both objects keep existing and can be used independently. Nothing here
    is mysterious — it is exactly the operation a quantum state refuses.
    """
    return bool(source)


def clone_attempt_circuit(state: str = "+") -> QuantumCircuit:
    """Return the two-qubit circuit that tries to clone ``state``.

    ``state`` is prepared on ``q0``, then ``CNOT`` copies ``q0`` into ``q1``. The
    control qubit is never touched, so ``q0`` still holds the original — but
    ``q1`` only matches it when the input was a basis state.
    """
    _check_state(state)

    def build(circuit: QuantumCircuit) -> None:
        TEST_STATES[state](circuit)
        circuit.cx(0, 1)

    circuit = QuantumCircuit(2, 2)
    build(circuit)
    circuit.measure(0, 0)
    circuit.measure(1, 1)
    return circuit


def clone_attempt_state(state: str = "+") -> Statevector:
    """Return the state the clone attempt reaches, before any measurement."""
    _check_state(state)

    def build(circuit: QuantumCircuit) -> None:
        TEST_STATES[state](circuit)
        circuit.cx(0, 1)

    circuit = QuantumCircuit(2)
    build(circuit)
    return Statevector.from_instruction(circuit)


def marginal(state: Statevector, qubit: int) -> DensityMatrix:
    """Return qubit ``qubit``'s reduced state of a two-qubit state.

    The result is generally **mixed** — that is the whole point: after the clone
    attempt neither qubit holds a definite pure state any more.
    """
    if qubit not in (0, 1):
        raise ValueError("qubit must be 0 or 1")
    return partial_trace(state, [1 - qubit])


def fidelity(left: Statevector | DensityMatrix, right: Statevector | DensityMatrix) -> float:
    """Return ``|<left|right>|^2``, the fidelity between two single-qubit states."""
    return float(state_fidelity(left, right))


@dataclass(frozen=True)
class CloneAttempt:
    """How well one way of copying an unknown state reproduces it.

    Attributes:
        state: the input state label, one of :data:`TEST_STATES`.
        perfect_copy: ``(copy, source)`` fidelity a classical bit would achieve.
        cnot_clone: the same pair for the ``CNOT`` attempt of
            :func:`clone_attempt_state`. The source survives; the copy is only
            right for basis states.
        fresh_superposition: the same pair when the "copy" is a brand-new ``|+>``
            instead. Right for superpositions, wrong for basis states.
    """

    state: str
    perfect_copy: tuple[float, float]
    cnot_clone: tuple[float, float]
    fresh_superposition: tuple[float, float]

    @property
    def cnot_copy(self) -> float:
        """Fidelity of the ``CNOT`` attempt's copy (qubit 1)."""
        return self.cnot_clone[0]

    @property
    def cnot_source(self) -> float:
        """Fidelity of the ``CNOT`` attempt's source (qubit 0)."""
        return self.cnot_clone[1]

    @property
    def fresh_copy(self) -> float:
        """Fidelity of the fresh-superposition attempt's copy (qubit 1)."""
        return self.fresh_superposition[0]


def clone_attempts() -> list[CloneAttempt]:
    """Compare a perfect copy with two ways of trying to clone on a quantum computer.

    Returns one :class:`CloneAttempt` per input state, holding the ``(copy,
    source)`` fidelity of each strategy. No single strategy among the two
    quantum ones covers all four inputs — that is the no-cloning theorem,
    measured.
    """

    def fresh_superposition(circuit: QuantumCircuit) -> None:
        """Prepare a brand-new ``|+>`` on the copy instead of copying the source."""
        circuit.h(0)
        circuit.h(1)

    attempts: list[CloneAttempt] = []
    for label, builder in TEST_STATES.items():
        original = Statevector.from_instruction(_single(builder))
        attempt = clone_attempt_state(label)
        fresh = Statevector.from_instruction(_two(fresh_superposition))
        attempts.append(
            CloneAttempt(
                state=label,
                perfect_copy=(1.0, 1.0),
                cnot_clone=(
                    fidelity(marginal(attempt, 1), original),
                    fidelity(marginal(attempt, 0), original),
                ),
                fresh_superposition=(
                    fidelity(marginal(fresh, 1), original),
                    fidelity(marginal(fresh, 0), original),
                ),
            )
        )
    return attempts


def clone_outcome_counts(state: str = "+", shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Measure the clone attempt on ``state`` and count the joint outcome.

    A perfect clone of a superposition would only ever produce ``00`` or ``11``
    (matching bits); the ``CNOT`` attempt spreads over all four.
    """

    _check_state(state)

    def build(circuit: QuantumCircuit) -> None:
        TEST_STATES[state](circuit)
        circuit.cx(0, 1)

    frames = run([gate(build, 2), measure(0, 1)], n_qubits=2)
    return sample_counts(frames, shots, seed=seed)


def ideal_clone_state(state: str = "+") -> Statevector:
    """Return the state a *perfect* clone of ``state`` would produce.

    Two **independent** copies: ``|ψ> ⊗ |ψ>``, prepared independently. No
    machine can build this from an unknown ``ψ`` — it is the reference the
    :func:`clone_attempt_state` attempt is compared against.
    """
    _check_state(state)
    single = np.asarray(Statevector.from_instruction(_single(TEST_STATES[state])).data)
    return Statevector(np.kron(single, single))


def ideal_clone_counts(state: str = "+", shots: int = 1000, *, seed: int | None = None) -> dict[str, int]:
    """Return the outcome counts a *perfect* clone of ``state`` would produce.

    A true clone leaves the two qubits **independent**, so for a superposition
    all four outcomes appear at 25% each. The ``CNOT`` attempt instead produces
    ``(|00> + |11>) / √2``, which is entangled: the outcomes are perfectly
    *correlated*, so ``01`` and ``10`` never occur at all. Correlated where they
    should be independent is the signature of the failure.
    """
    _check_state(state)
    frames = run([gate(_ideal_clone(state), 2), measure(0, 1)], n_qubits=2)
    return sample_counts(frames, shots, seed=seed)


def _ideal_clone(state: str) -> Builder:
    """Prepare two independent copies of ``state`` — the impossible ideal."""

    def build(circuit: QuantumCircuit) -> None:
        circuit.barrier(0)
        prepare(circuit, 0, state)
        circuit.barrier(0)
        prepare(circuit, 1, state)

    return build


def prepare(circuit: QuantumCircuit, qubit: int, state: str) -> None:
    """Apply the preparation for ``state`` to ``qubit``.

    ``TEST_STATES`` holds one-qubit builders, so run the builder on a scratch
    circuit and re-append every gate it produced onto ``qubit``.
    """
    _check_state(state)
    scratch = _single(TEST_STATES[state])
    for instruction in scratch.data:
        circuit.append(instruction.operation, [qubit])


def draw(output: str | Path = "build/ch06-clone-attempt-circuit.png") -> Path:
    """Render the clone-attempt circuit and save it to ``output``."""
    return render_circuit(clone_attempt_circuit(), output, reverse_bits=True)


def _clone_table(attempts: list[CloneAttempt]) -> Table:
    table = Table(title="Fidelity of the copy (q1) and of the source (q0) against the input", header_style="heading")
    table.add_column("input", style="bits")
    table.add_column("perfect copy", style="value")
    table.add_column("CNOT clone: copy", style="value")
    table.add_column("CNOT clone: source", style="value")
    table.add_column("H, H: copy", style="value")
    for attempt in attempts:
        table.add_row(
            as_ket(attempt.state),
            "1.00 / 1.00",
            f"{attempt.cnot_copy:.2f}",
            f"{attempt.cnot_source:.2f}",
            f"{attempt.fresh_copy:.2f}",
        )
    return table


def main() -> None:
    explain(
        "Chapter 6 — networking basics",
        """
A network moves information between parties. Chapter 6 opens with the simplest
one that exists: a single byte over a TCP socket on this machine, then asks what
changes when the thing being moved is a **qubit**.

The answer is: everything. A classical bit can be copied, because reading it
does not disturb it. A qubit **cannot** be copied — not because it is hard, but
because it is impossible: the **no-cloning theorem**. Trying anyway with a
`CNOT` raises no error; it just quietly produces the wrong answer.

The argument is short. Suppose a machine copies *any* state `|ψ>` and leaves the
original alone. Feed it `|+>` and the copy looks fine. But feed it
`( |0> + |1> ) / √2` and, by linearity, the copy must come out as
`( |00> + |11> ) / √2`. Measure **one** qubit of that state and the outcome is
0 or 1 with certainty, so the copy collapses to `|0>` or `|1>` — never `|+>`
again. Contradiction.

So a quantum network has to **move** a state without **copying** it. That is what
teleportation does, and it needs two classical bits to say it worked.
""",
    )

    console.rule("A byte over a socket")
    received = send_byte(0x8)
    console.print(f"  [muted]The receiver read back [/muted][value]{received}[/value][muted].[/muted]")

    steps(
        "Chapter 6 — step by step",
        [
            ("Receiver binds the port", f"{HOST}:{DEFAULT_PORT} and waits for a connection"),
            ("Sender connects", "the OS hands the socket to the other process"),
            ("Sender writes one byte", "value 8 travels as 8 bits, exactly as sent"),
            ("Receiver reads it", f"got {received} — the byte arrived intact, the sender is gone"),
        ],
    )

    console.rule("A classical bit can be copied")
    for source in (True, False):
        copy = classic_copy(source)
        console.print(f"  source={source!s:>5}, copy={copy!s:>5}  [muted]— both still exist and work[/muted]")

    console.rule("A qubit cannot")
    attempts = clone_attempts()
    console.print(_clone_table(attempts))
    console.print(
        "[muted]The CNOT attempt handles basis states and fails on superpositions, where both "
        "qubits drop to 0.50. Preparing a fresh superposition does the opposite: right for |+>, "
        "wrong for |0> and |1>. Neither covers all four.[/muted]"
    )

    attempt = clone_outcome_counts("+", shots=1000, seed=11)
    ideal = ideal_clone_counts("+", shots=1000, seed=11)
    labels = ("00", "01", "10", "11")
    console.print(
        "\n  [heading]A perfect clone of |+> would give: [/heading]"
        + ", ".join(f"{label}={ideal.get(label, 0)}" for label in labels)
    )
    console.print(
        "  [heading]The CNOT attempt gives:             [/heading]"
        + ", ".join(f"{label}={attempt.get(label, 0)}" for label in labels)
    )
    console.print(
        "[muted]Two real copies would be independent: all four outcomes at 25%. The attempt "
        "gives them perfectly correlated instead — 01 and 10 vanish, because it built the "
        "entangled state ( |00> + |11> ) / √2 rather than |+> ⊗ |+>.[/muted]"
    )
    console.print(
        "[muted]This is why a quantum network cannot use the trick ordinary networking "
        "relies on: copying a packet and forwarding the copy.[/muted]"
    )

    circuit_path = draw()
    fidelity_path = render_counts(
        {as_ket(attempt.state): attempt.cnot_copy for attempt in attempts},
        "build/ch06-clone-fidelity.png",
        title="Fidelity of the CNOT copy against the input",
        xlabel="input state",
        ylabel="fidelity |<copy|input>|^2",
    )
    agreement_path = render_grouped_counts(
        [("perfect clone (impossible)", ideal), ("CNOT attempt", attempt)],
        "build/ch06-clone-agreement.png",
        title="Clone of |+>: independent copies vs. the CNOT attempt",
        xlabel="outcome of (q0, q1)",
        ylabel="count",
    )

    console.print("Saved diagrams:")
    for path in (circuit_path, fidelity_path, agreement_path):
        console.print(f"  [path]{path}[/path]")


if __name__ == "__main__":
    main()
