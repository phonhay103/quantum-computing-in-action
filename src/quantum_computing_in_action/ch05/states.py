"""Chapter 5 — multi-qubit states, the tensor product, and the CNOT matrix.

Chapter 4 described a single qubit as a vector ``[alpha, beta]`` and a gate as a
matrix. Two qubits are described by the **tensor product** of two such vectors,
which lives in a four-dimensional space with basis states ``|00>``, ``|01>``,
``|10>`` and ``|11>``. This module exposes those ingredients (and the
:data:`CNOT` matrix) so the entanglement chapter can be built and tested on top
of them instead of hiding everything behind the simulator.

Qubit-order convention
----------------------

Following the book's labels, a two-qubit state is written ``|q1 q0>``: the
**leftmost** character is qubit 1 and the rightmost is qubit 0. For the
controlled-NOT gate the leftmost qubit is the **control** and the rightmost is
the **target**, the usual textbook convention.

Qiskit stores amplitudes in the *opposite* (little-endian) bit order: in a
``Statevector`` label the rightmost character is qubit 0. So to apply a
control-first ``CNOT`` in a Qiskit circuit we call ``qc.cx(1, 0)`` (control
qubit 1, target qubit 0). :func:`ket` and :func:`tensor` still agree with
Qiskit's ``Statevector`` labels.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

#: The two-qubit basis labels, in order, with the leftmost character = qubit 1.
BASIS_LABELS: tuple[str, ...] = ("00", "01", "10", "11")

#: The Pauli-X gate as a matrix (used to prepare definite states).
X: np.ndarray = np.array([[0, 1], [1, 0]], dtype=complex)

#: The controlled-NOT gate ``CNOT`` in the **usual textbook convention**: the
#: control is the first (leftmost) qubit and the target is the second
#: (rightmost) one. It flips the target when the control is ``1``:
#: ``|10> -> |11>`` and ``|11> -> |10>``, leaving ``|00>`` and ``|01>``
#: untouched.
#:
#: In the basis order ``|00>, |01>, |10>, |11>`` it is the matrix below.
#:
#: .. note::
#:    Qiskit uses the *opposite* (little-endian) bit order internally: in a
#:    ``Statevector`` label the rightmost character is qubit 0. To realise this
#:    control-first convention in a Qiskit circuit we therefore use
#:    ``qc.cx(1, 0)`` (control qubit 1, target qubit 0), not ``qc.cx(0, 1)``.
CNOT: np.ndarray = np.array(
    [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ],
    dtype=complex,
)


def ket(label: str) -> np.ndarray:
    """Return the two-qubit basis vector for ``label`` (one of :data:`BASIS_LABELS`)."""
    if label not in BASIS_LABELS:
        raise ValueError(f"label must be one of {BASIS_LABELS}, got {label!r}")
    vector = np.zeros(4, dtype=complex)
    vector[int(label, 2)] = 1.0
    return vector


def qubit_ket(bit: str) -> np.ndarray:
    """Return the single-qubit basis vector for ``"0"`` or ``"1"``."""
    if bit not in ("0", "1"):
        raise ValueError(f"bit must be '0' or '1', got {bit!r}")
    return np.array([1.0, 0.0] if bit == "0" else [0.0, 1.0], dtype=complex)


def tensor(*factors: np.ndarray) -> np.ndarray:
    """Return the tensor product of ``factors``.

    The first factor becomes the **leftmost** qubit in the label, so
    ``tensor(ket("0"), ket("1")) == ket("01")``. This is the standard
    ``A x B`` convention written ``|a>|b>``.
    """
    if not factors:
        raise ValueError("tensor needs at least one factor")
    result = np.array([1.0 + 0.0j])
    for factor in factors:
        result = np.kron(result, factor)
    return result


def bell_state(index: int = 0) -> np.ndarray:
    """Return one of the four Bell states as a 4-vector.

    ``index`` selects the state, mirroring the standard ``Phi+/Phi-/Psi+/Psi-``
    family:

    - ``0`` -> ``(|00> + |11>) / sqrt(2)`` (the ``H`` then ``CNOT`` state)
    - ``1`` -> ``(|00> - |11>) / sqrt(2)``
    - ``2`` -> ``(|01> + |10>) / sqrt(2)``
    - ``3`` -> ``(|01> - |10>) / sqrt(2)``
    """
    root = 1.0 / np.sqrt(2.0)
    signs = {
        0: (root, root),
        1: (root, -root),
        2: (root, root),
        3: (root, -root),
    }
    if index not in signs:
        raise ValueError("index must be 0, 1, 2 or 3")
    plus, minus = signs[index]
    if index < 2:
        return plus * ket("00") + minus * ket("11")
    return plus * ket("01") + minus * ket("10")


def amplitudes(state: np.ndarray) -> dict[str, complex]:
    """Return the four amplitudes of ``state`` keyed by basis label."""
    return {label: complex(state[int(label, 2)]) for label in BASIS_LABELS}


def probabilities(state: np.ndarray) -> dict[str, float]:
    """Return measurement probabilities keyed by basis label (the Born rule)."""
    return {label: float(abs(amplitude) ** 2) for label, amplitude in amplitudes(state).items()}


def schmidt_rank(state: np.ndarray, *, atol: float = 1e-9) -> int:
    """Return the Schmidt rank of a two-qubit state (1 = product, 2 = entangled).

    Reshaping the four amplitudes into a 2x2 matrix turns the question "can this
    state be written as ``|a>|b>``?" into "is this matrix rank 1?". A rank of 2
    means the state cannot be factored and is **entangled**.
    """
    matrix = np.asarray(state, dtype=complex).reshape(2, 2)
    return int(np.linalg.matrix_rank(matrix, tol=atol))


def is_entangled(state: np.ndarray) -> bool:
    """Return whether a two-qubit state is entangled (Schmidt rank 2)."""
    return schmidt_rank(state) > 1


def compose(matrices: Sequence[np.ndarray]) -> np.ndarray:
    """Multiply gate matrices in the order they are applied (last applied last)."""
    result = np.eye(4, dtype=complex)
    for matrix in matrices:
        result = matrix @ result
    return result
