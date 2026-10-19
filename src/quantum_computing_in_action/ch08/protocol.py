"""Chapter 8 — the quantum/bit model behind BB84.

Everything in this chapter is built on one qubit and two bases:

* the **Z basis** (``0``), whose states are ``|0>`` and ``|1>``;
* the **X basis** (``1``), whose states are ``|+>`` and ``|->``.

Alice prepares each qubit with a *bit* (which state) and a *base* (which pair).
Bob measures each qubit with a *base* of his own. The only fact the whole protocol
rests on is small enough to state once:

    if Bob measures in the base Alice prepared, he gets her bit;
    if he measures in the other base, he gets a fair coin.

That is the Born rule for two bases 45 degrees apart, and :func:`measure` is that
rule. :func:`state_probabilities` computes the same numbers with Qiskit so the
tests can check the rule against the simulator rather than against itself.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

#: The **Z** basis: ``|0>`` and ``|1>``.
Z = 0

#: The **X** basis: ``|+>`` and ``|->`` (a Hadamard away from the Z basis).
X = 1

#: The two bases by name, for printing.
BASES: tuple[str, ...] = ("Z", "X")


def base_name(base: int) -> str:
    """Return ``"Z"`` or ``"X"`` for the base index ``0`` or ``1``."""
    return BASES[base]


def prepare_circuit(bit: int, base: int) -> QuantumCircuit:
    """Return the one-qubit circuit that prepares ``bit`` in ``base``.

    An ``X`` sets the *bit* (``|0> -> |1>``) and a Hadamard sets the *base*
    (``|0> -> |+>``). Doing the ``X`` first means “prepare the bit, then rotate
    into the chosen base”, which is exactly how BB84 describes it.
    """
    circuit = QuantumCircuit(1)
    if bit:
        circuit.x(0)
    if base == X:
        circuit.h(0)
    return circuit


def prepare_state(bit: int, base: int) -> Statevector:
    """Return the one-qubit state Alice sends for ``bit`` in ``base``."""
    return Statevector.from_instruction(prepare_circuit(bit, base))


def measure(bit: int, *, prepared_base: int, measured_base: int, rng: np.random.Generator) -> int:
    """Measure a qubit that was prepared as ``bit`` in ``prepared_base``.

    Args:
        bit: the bit Alice encoded, ``0`` or ``1``.
        prepared_base: the base the state was prepared in.
        measured_base: the base Bob measures in.
        rng: the random source used for the “fair coin” case.

    Returns:
        The measured bit. If the bases agree that is ``bit`` with certainty; if
        they differ, it is an independent fair coin.
    """
    if prepared_base == measured_base:
        return bit
    return int(rng.integers(0, 2))


def state_probabilities(bit: int, base: int, measured_base: int) -> dict[str, float]:
    """Return Qiskit's measurement probabilities for the state in ``measured_base``.

    The reference the :func:`measure` rule is checked against.
    """
    circuit = prepare_circuit(bit, base)
    if measured_base == X:
        circuit.h(0)
    state = Statevector.from_instruction(circuit)
    return {label: float(value) for label, value in state.probabilities_dict().items()}


def _random_bits(rng: np.random.Generator, count: int) -> tuple[int, ...]:
    return tuple(int(value) for value in rng.integers(0, 2, size=count))


@dataclass(frozen=True)
class Run:
    """The complete record of one BB84 exchange.

    Attributes:
        alice_bits: the bits Alice chose.
        alice_bases: the bases Alice prepared them in.
        bob_bases: the bases Bob measured in.
        bob_bits: the bits Bob measured.
        eve_bases: the bases an eavesdropper measured in, or ``None``.
        eve_bits: the bits an eavesdropper measured, or ``None``.
    """

    alice_bits: tuple[int, ...]
    alice_bases: tuple[int, ...]
    bob_bases: tuple[int, ...]
    bob_bits: tuple[int, ...]
    eve_bases: tuple[int, ...] | None = None
    eve_bits: tuple[int, ...] | None = None

    @property
    def size(self) -> int:
        """The number of qubits exchanged."""
        return len(self.alice_bits)

    @property
    def sifted(self) -> tuple[int, ...]:
        """The indices where Alice's and Bob's bases agree — the kept positions."""
        return tuple(index for index in range(self.size) if self.alice_bases[index] == self.bob_bases[index])

    @property
    def alice_key(self) -> str:
        """Alice's key: her bits at the sifted positions."""
        return "".join(str(self.alice_bits[index]) for index in self.sifted)

    @property
    def bob_key(self) -> str:
        """Bob's key: his bits at the sifted positions."""
        return "".join(str(self.bob_bits[index]) for index in self.sifted)

    @property
    def errors(self) -> int:
        """How many sifted bits disagree — Bob's raw error count."""
        return sum(self.alice_bits[index] != self.bob_bits[index] for index in self.sifted)

    @property
    def error_rate(self) -> float:
        """The fraction of sifted bits that disagree.

        With no eavesdropper this is ``0.0``; with an intercept-resend
        eavesdropper it climbs to about ``0.25``, which is the detection.
        """
        if not self.sifted:
            return 0.0
        return self.errors / len(self.sifted)

    @property
    def raw_errors(self) -> int:
        """How many bits disagree over *every* position, sifting aside."""
        return sum(self.alice_bits[index] != self.bob_bits[index] for index in range(self.size))

    @property
    def raw_error_rate(self) -> float:
        """The fraction of *all* bits that disagree.

        For a protocol that does not reconcile bases this is around ``0.25``:
        half the qubits were measured in the wrong base, and half of those flip.
        """
        if self.size == 0:
            return 0.0
        return self.raw_errors / self.size


def run(size: int = 8, *, seed: int | None = None, eavesdropper: bool = False) -> Run:
    """Run one BB84 exchange of ``size`` qubits.

    Alice picks a random bit and base for each qubit and sends it. Bob picks a
    random base and measures. If ``eavesdropper`` is set, an Eve between them
    measures every qubit in a random base and re-sends the state she collapsed it
    to — the classic intercept-resend attack.

    The qubits never touch each other, so the protocol is simulated one qubit at
    a time with the :func:`measure` rule; the argument for that is at the top of
    this module.
    """
    if size < 1:
        raise ValueError("size must be at least 1")
    rng = np.random.default_rng(seed)

    alice_bits = _random_bits(rng, size)
    alice_bases = _random_bits(rng, size)
    bob_bases = _random_bits(rng, size)

    eve_bases: tuple[int, ...] | None = None
    eve_bits: tuple[int, ...] | None = None
    if eavesdropper:
        eve_bases = _random_bits(rng, size)
        eve_bits = tuple(
            measure(alice_bits[index], prepared_base=alice_bases[index], measured_base=eve_bases[index], rng=rng)
            for index in range(size)
        )

    # Bob measures the state that reaches him: Alice's original, or Eve's resend.
    source_bits = eve_bits if eve_bits is not None else alice_bits
    source_bases = eve_bases if eve_bases is not None else alice_bases
    bob_bits = tuple(
        measure(source_bits[index], prepared_base=source_bases[index], measured_base=bob_bases[index], rng=rng)
        for index in range(size)
    )

    return Run(
        alice_bits=alice_bits,
        alice_bases=alice_bases,
        bob_bases=bob_bases,
        bob_bits=bob_bits,
        eve_bases=eve_bases,
        eve_bits=eve_bits,
    )


def bb84_circuit(
    alice_bits: tuple[int, ...], alice_bases: tuple[int, ...], bob_bases: tuple[int, ...]
) -> QuantumCircuit:
    """Return the circuit Alice and Bob would run — the one worth drawing.

    Alice prepares every qubit, Bob rotates into his base, and every qubit is
    measured. (An eavesdropper is not drawn: her measurement in the middle cannot
    be expressed in a single plain circuit without mid-circuit control flow.)
    """
    size = len(alice_bits)
    circuit = QuantumCircuit(size, size)
    for index in range(size):
        if alice_bits[index]:
            circuit.x(index)
        if alice_bases[index] == X:
            circuit.h(index)
    for index in range(size):
        if bob_bases[index] == X:
            circuit.h(index)
        circuit.measure(index, index)
    return circuit
