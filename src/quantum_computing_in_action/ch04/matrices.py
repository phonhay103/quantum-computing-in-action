"""Chapter 4 — gates as matrices (book sections 4.2-4.4).

The book describes a single qubit as a **state vector** ``[alpha, beta]`` and
every gate as a **2x2 matrix** that multiplies it. These helpers expose the
matrices for the Pauli-X and Hadamard gates so the idea can be printed and
tested, instead of hiding behind the simulator.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

#: The identity ("do nothing") operation.
IDENTITY: np.ndarray = np.eye(2, dtype=complex)

#: The Pauli-X gate as a matrix: it swaps the two basis states.
X: np.ndarray = np.array([[0, 1], [1, 0]], dtype=complex)

#: The Hadamard gate as a matrix: it maps ``|0>`` to an even superposition.
H: np.ndarray = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


def state_vector(alpha: complex, beta: complex) -> np.ndarray:
    """Return the state vector ``alpha|0> + beta|1>``."""
    return np.array([alpha, beta], dtype=complex)


def apply(matrix: np.ndarray, state: np.ndarray) -> np.ndarray:
    """Apply a gate matrix to a state vector (matrix-vector product)."""
    return matrix @ state


def probabilities(state: np.ndarray) -> tuple[float, float]:
    """Return ``(P(0), P(1))`` for a state vector, using the Born rule."""
    return float(abs(state[0]) ** 2), float(abs(state[1]) ** 2)


def is_identity(matrix: np.ndarray, *, atol: float = 1e-9) -> bool:
    """Return whether ``matrix`` is (numerically) the identity."""
    return bool(np.allclose(matrix, IDENTITY, atol=atol))


def compose(matrices: Sequence[np.ndarray]) -> np.ndarray:
    """Multiply a sequence of gate matrices in the order they are applied."""
    result = IDENTITY
    for matrix in matrices:
        result = matrix @ result
    return result
