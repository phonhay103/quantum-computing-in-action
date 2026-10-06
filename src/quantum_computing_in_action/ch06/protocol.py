"""Chapter 6 — a small frame simulator for protocols with classical feedback.

Every sample in this chapter shares one ingredient: a quantum circuit with a
**mid-circuit measurement** whose outcome drives *classical* gates on a different
qubit — the correction step of quantum teleportation, repeated by the repeater.

``Statevector.from_instruction`` refuses circuits containing control-flow
operations (``IfElseOp``), so this module simulates such a program the way the
protocol is actually described. It keeps one :class:`Frame` per possible
measurement outcome, applies the quantum gates to every frame, and *branches* a
frame into up to ``2 ** len(qubits)`` children when its qubits are measured.

    >>> frames = run([gate(h(2), 3), measure(0, 1)], n_qubits=3)
    >>> sorted(frame.bits for frame in frames)
    ['00', '01', '10', '11']

Each frame carries the state vector, the classical bits read so far, and the
probability of reaching that frame. Because the branches partition the total
probability, the frames of one run always sum to one.

Qubit-index convention
----------------------

Qubits are addressed by plain Qiskit index (``q0``, ``q1``, ...) and the states
are stored in Qiskit's little-endian order, exactly as
:class:`~qiskit.quantum_info.Statevector` does. Unlike Chapter 5, the *labels*
used for tables are written in the order the bits are **measured** (see
:func:`measure`), which is stated wherever it matters. The book's Java samples
use the same plain qubit indices, so ``q0`` is the qubit at ``q[0]``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, replace
from itertools import product

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

#: A function that adds gates to a circuit. Kept as a named type because the
#: diagram circuits below reuse the very same gate sequences.
#:
#: The return value is deliberately ignored: Qiskit's gate methods hand back an
#: ``InstructionSet``, while a hand-written builder returns ``None``, and both
#: are fine here since only the circuit itself matters.
Builder = Callable[[QuantumCircuit], object]

#: Branches whose remaining norm falls below this value are dropped as
#: impossible outcomes.
TOLERANCE = 1e-12


@dataclass(frozen=True)
class Frame:
    """One possible history of a run: a state plus the classical bits so far.

    Attributes:
        state: the ``2 ** n_qubits`` amplitude vector of this branch.
        bits: the measured bits, in the order the qubits were measured.
        weight: the probability of reaching this branch (the squares of the
            amplitudes of :attr:`state`, times the weights of its parents).
    """

    state: np.ndarray
    bits: str
    weight: float


#: One step of a program: it maps the current list of frames to the next one.
Operation = Callable[[list[Frame]], list[Frame]]

#: A whole protocol: the operations to run, in order.
Program = Sequence[Operation]


def _matrix(builder: Builder, n_qubits: int) -> np.ndarray:
    """Build the full ``2 ** n_qubits`` matrix of a gate sequence."""
    circuit = QuantumCircuit(n_qubits)
    builder(circuit)
    return np.asarray(Operator(circuit).data, dtype=complex)


def gate(builder: Builder, n_qubits: int) -> Operation:
    """Return an operation applying a fixed gate sequence to every frame.

    This is the unitary part of a protocol — the part that does not depend on
    any measurement outcome.
    """
    matrix = _matrix(builder, n_qubits)

    def apply(frames: list[Frame]) -> list[Frame]:
        return [replace(frame, state=matrix @ frame.state) for frame in frames]

    return apply


def _condition(bit: int, matrix: np.ndarray) -> Operation:
    """Return an operation that applies ``matrix`` only where ``bits[bit] == '1'``.

    ``bit`` indexes the classical bit string in measurement order. This is how a
    protocol applies Alice's measurement results to Bob's qubit: classically
    conditioned, and therefore no faster than light.
    """
    if bit < 0:
        raise ValueError("bit must not be negative")

    def apply(frames: list[Frame]) -> list[Frame]:
        corrected = []
        for frame in frames:
            if bit >= len(frame.bits):
                raise ValueError(f"bit {bit} has not been measured yet")
            state = matrix @ frame.state if frame.bits[bit] == "1" else frame.state
            corrected.append(replace(frame, state=state))
        return corrected

    return apply


def x_if(bit: int, qubit: int, n_qubits: int) -> Operation:
    """Flip ``qubit`` on the branches whose classical bit ``bit`` is ``1``.

    This is the ``X`` half of the teleportation correction.
    """
    matrix = _matrix(lambda circuit: circuit.x(qubit), n_qubits)
    return _condition(bit, matrix)


def z_if(bit: int, qubit: int, n_qubits: int) -> Operation:
    """Apply ``Z`` to ``qubit`` on the branches whose classical bit ``bit`` is ``1``.

    This is the ``Z`` half of the teleportation correction; the book's Java
    sample spells it as a controlled-``Z`` between the measured qubit and Bob's.
    """
    matrix = _matrix(lambda circuit: circuit.z(qubit), n_qubits)
    return _condition(bit, matrix)


def _matches(indices: np.ndarray, qubits: tuple[int, ...], outcome: tuple[int, ...]) -> np.ndarray:
    """Return the boolean mask of basis-state indices matching ``outcome``.

    Qiskit stores a state vector in little-endian order, so qubit ``q`` occupies
    bit ``q`` of the index. Testing every qubit separately (rather than masking)
    matters: a measured ``0`` contributes nothing to a mask, which would make
    ``index & mask == mask`` true for *every* index.
    """
    mask = np.ones(indices.shape, dtype=bool)
    for qubit, bit in zip(qubits, outcome, strict=True):
        mask &= ((indices >> qubit) & 1) == bit
    return mask


def measure(*qubits: int) -> Operation:
    """Measure ``qubits`` and branch every frame on the outcome.

    Each frame becomes one child per outcome that still has a non-zero
    probability. The child's classical bits are **appended in the order the
    qubits are given**, so ``measure(0, 1)`` appends qubit 0's bit first.
    """
    if not qubits:
        raise ValueError("measure needs at least one qubit")
    if len(set(qubits)) != len(qubits):
        raise ValueError("measure needs distinct qubits")

    def apply(frames: list[Frame]) -> list[Frame]:
        children: list[Frame] = []
        for frame in frames:
            # Projecting leaves the surviving amplitudes at their old scale, so
            # the probability of the branch is norm(projected)^2 / norm(frame)^2.
            parent = float(np.linalg.norm(frame.state)) ** 2
            indices = np.arange(frame.state.size)
            for outcome in product((0, 1), repeat=len(qubits)):
                projected = np.where(_matches(indices, qubits, outcome), frame.state, 0.0)
                norm = float(np.linalg.norm(projected))
                if norm <= TOLERANCE:
                    continue
                bits = "".join(str(bit) for bit in outcome)
                children.append(
                    replace(
                        frame,
                        state=projected / norm,
                        bits=frame.bits + bits,
                        weight=frame.weight * norm**2 / parent,
                    )
                )
        return children

    return apply


def run(program: Program, n_qubits: int, initial: np.ndarray | None = None) -> list[Frame]:
    """Execute ``program`` and return the final list of frames.

    ``initial`` is the starting state vector; it defaults to ``|00...0>``. The
    returned frames partition the total probability, so their weights sum to one.
    """
    if n_qubits < 1:
        raise ValueError("n_qubits must be at least 1")
    size = 2**n_qubits
    if initial is None:
        state = np.zeros(size, dtype=complex)
        state[0] = 1.0
    else:
        state = np.asarray(initial, dtype=complex).reshape(size)
    frames = [Frame(state=state, bits="", weight=1.0)]
    for operation in program:
        frames = operation(frames)
    return frames


def qubit_state(
    state: np.ndarray,
    qubit: int,
    n_qubits: int,
    *,
    fixed: dict[int, int] | None = None,
) -> np.ndarray:
    """Return the two amplitudes of ``qubit``, taking the other qubits as known.

    This reads the two surviving amplitudes out of a *branch* of a run, which is
    a valid single-qubit state only once the other qubits have been measured.

    Args:
        state: the branch's amplitude vector.
        qubit: the qubit whose amplitudes to return.
        n_qubits: how many qubits the branch spans.
        fixed: the known value of each **other** qubit. Qubits left out are taken
            to be ``0``. This matters: after ``measure(0, 1)`` qubits 0 and 1 sit
            at their measured values, which are usually not ``0`` — collapsing
            them to ``|0>`` would report the wrong pair of amplitudes.
    """
    if not 0 <= qubit < n_qubits:
        raise ValueError(f"qubit must be in 0..{n_qubits - 1}, got {qubit}")
    values = dict(fixed or {})
    for index in range(n_qubits):
        if index == qubit:
            continue
        value = values.get(index, 0)
        if value not in (0, 1):
            raise ValueError(f"qubit {index} must be known as 0 or 1, got {value!r}")
    # The flat amplitude index is q0 + 2*q1 + 4*q2 + ..., so reshaping puts the
    # axes in *descending* qubit order: tensor[q_{n-1}][...][q1][q0].
    selector = [values.get(index, 0) for index in reversed(range(n_qubits))]
    selector[n_qubits - 1 - qubit] = slice(None)
    return np.asarray(state, dtype=complex).reshape((2,) * n_qubits)[tuple(selector)]


def probabilities(frames: Sequence[Frame]) -> dict[str, float]:
    """Merge the frames into a ``{bits: probability}`` mapping."""
    merged: dict[str, float] = {}
    for frame in frames:
        merged[frame.bits] = merged.get(frame.bits, 0.0) + frame.weight
    return merged


def sample_counts(frames: Sequence[Frame], shots: int, *, seed: int | None = None) -> dict[str, int]:
    """Sample ``shots`` runs from the branch probabilities.

    Args:
        frames: the frames returned by :func:`run`.
        shots: how many times to repeat the protocol.
        seed: optional seed for reproducible sample counts.

    Returns:
        The number of runs per classical bit string. Every qubit must have been
        measured for the labels to be unambiguous, so the labels are as long as
        the number of qubits.

    Raises:
        ValueError: if ``shots`` is below 1, or if some qubit was never measured.
    """
    if shots < 1:
        raise ValueError("shots must be at least 1")
    merged = probabilities(frames)
    labels = sorted(merged)
    if not labels:
        raise ValueError("the frames carry no probability")
    n_qubits = frames[0].state.size.bit_length() - 1
    if any(len(label) != n_qubits for label in labels):
        raise ValueError("every qubit must be measured before counting results")
    weights = np.array([merged[label] for label in labels], dtype=float)
    total = weights.sum()
    if total <= 0:
        raise ValueError("the frames carry no probability")
    draws = np.random.default_rng(seed).multinomial(shots, weights / total)
    return dict(zip(labels, (int(count) for count in draws), strict=True))
