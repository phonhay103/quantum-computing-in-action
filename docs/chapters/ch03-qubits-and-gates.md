# Chapter 3 — Qubits and quantum gates

!!! abstract "In one sentence"
    A **qubit** is the basic unit of quantum information, and a **gate** is a
    reversible operation that acts on it; the first gate encountered is
    **Pauli-X**, which flips `|0⟩` to `|1⟩` deterministically — in other words,
    the quantum `NOT`.

## The basic units

Quantum programs are assembled from two very small pieces:

- a **qubit** — the carrier of quantum information, equipped with the two basis
  states `|0⟩` and `|1⟩`;
- a **gate** — an operation applied to one or more qubits.

Everything that appears later in the book — superposition, entanglement, and
complete algorithms alike — is constructed from these two ideas alone. It
follows that this chapter serves as the "basic units" chapter: before any more
elaborate construction can be attempted, it is necessary to establish precisely
what a qubit is and how a gate acts upon it.

## Qubits

A classical bit takes exactly one of two values: `0` or `1`. A qubit can occupy
either of those states, but it can also be placed in a **superposition** — a
weighted combination of both basis states at once. Chapter 2 already exploited
this property to generate random bits. The present chapter focuses on the
simplest operation a gate can perform: moving a qubit cleanly between the two
basis states.

It is worth recording a scale fact for later use: `n` qubits are described by
`2^n` amplitudes, so the number of amplitudes doubles with every additional
qubit. That exponential growth constitutes the raw material of Chapter 4 and the
chapters beyond it.

## Gates are reversible

A defining property of quantum gates is that they are **reversible**:
information is never thrown away. Every gate possesses an inverse that restores
the preceding state. This contrasts sharply with the familiar classical gates —
`AND` takes two inputs and returns a single output, so the inputs cannot be
recovered from the output alone. Mathematically, reversibility amounts to the
requirement that a gate be represented by a **unitary** matrix
(see [vectors, matrices, and unitary gates](../foundations.md#vectors-matrices-and-unitary-gates)),
which Chapter 4 develops in full detail.

- The inverse of `X` is `X` itself: `X·X = I`.
- The inverse of `H` is likewise `H` itself (Chapter 4).

Here `I` denotes the **identity** operation — "do nothing". This reversibility
is not a minor detail; it is precisely what allows quantum circuits to be built
up and, when required, undone.

!!! note "Measurement is the exception"
    Gates are reversible, but a **measurement** is not: a measurement collapses
    the state and leaves behind a single classical result. That asymmetry is the
    reason a quantum algorithm is written as a reversible circuit followed, at
    the very end, by a measurement.

## A NOT gate for qubits

The **Pauli-X gate** is the quantum analogue of the classical `NOT`:

$$X\,|0\rangle = |1\rangle, \qquad X\,|1\rangle = |0\rangle$$

The gate swaps the roles of the two basis states while leaving everything else
about the qubit consistent. If the computation starts in `|0⟩` and `X` is then
applied, the qubit is thereafter certainly in `|1⟩`; measuring it consequently
returns `1` — on every single repetition of the experiment.

## The gates you will meet

`X` is the first gate encountered, but it is only one member of a small family.
`H` (introduced in Chapter 2) creates superposition, and a **two-qubit** gate
such as `CNOT` arrives together with entanglement in Chapter 5. Each of these
gates is introduced formally at exactly the point where it becomes necessary, so
no familiarity with them is assumed at this stage. For the moment, the essential
point is that every gate in the family obeys the same two rules: it is
reversible, and it moves the qubit to a definite point on the Bloch sphere.

## Why the result is deterministic

Why does the same kind of experiment — one gate followed by a measurement —
yield randomness in one chapter and certainty in the other? The two chapters may
be contrasted directly, one fact per row:

| | Chapter 2 (Hadamard) | Chapter 3 (Pauli-X) |
|---|---|---|
| State after the gate | (\|0⟩ + \|1⟩)/√2 | \|1⟩ |
| Probability of `0` | 50 % | 0 % |
| Probability of `1` | 50 % | 100 % |
| Repeated measurements | mixed `0`s and `1`s | always `1` |

The difference lies in the state itself, not in the measuring device. A definite
state measures definitely; a balanced superposition measures randomly. In other
words, the statistics are fully determined by what the state is at the moment of
measurement.

!!! info "What "measurement basis" means"
    Throughout, "measure" means a measurement in the computational `{|0⟩, |1⟩}`
    basis — the same Z axis that the poles of the Bloch sphere represent. A
    different choice of basis yields different results; Chapter 6 encounters a
    case in which the state changes sign yet every measurement probability stays
    exactly the same.

??? question "Check yourself — Chapter 2's `H` is reversible too. Can its randomness be undone?"
    Yes — but only as long as the qubit has not yet been measured. Applying a
    second `H` before any measurement returns the qubit to `|0⟩`; measuring at
    that point yields `0` every time (Chapter 4 makes this its headline result).
    The randomness becomes permanent only at the measurement itself — precisely
    the exception described in the note above.

## The diagrams

### The circuit

![Pauli-X circuit](../assets/ch03-pauli-x.png){ width="420" }

Read from left to right: the qubit `q` starts in `|0⟩`, the `X` box flips it,
and the measurement `M` records the outcome in the classical bit `c`. This small
diagram encapsulates the entire story of the chapter.

### Two `X` gates cancel

![Two Pauli-X gates](../assets/ch03-pauli-x2-circuit.png){ width="420" }

Because `X·X = I`, the second `X` undoes the first. A circuit is nothing more
than gates arranged in a sequence, and the sequence `X, X` is equivalent to
doing nothing at all.

### Before, after one `X`, after two

![Qubit before, after X, and after X·X](../assets/ch03-pauli-x-bloch.png){ width="720" }

The **Bloch sphere** renders the flip visually:

- **Before** — the state arrow points to the north pole, `|0⟩`.
- **After one `X`** — the arrow points to the south pole, `|1⟩`.
- **After two `X`s** — the arrow has returned to the north pole, `|0⟩`.

Geometrically, `X` is a **180° rotation about the X axis** of the sphere.
Because the state travels from pole to pole and never touches the equator, no
superposition is produced and, consequently, no randomness appears in the
outcome.

### What you measure

![1000 runs of X](../assets/ch03-pauli-x-counts.png){ width="420" }
![1000 runs of X·X](../assets/ch03-pauli-x2-counts.png){ width="420" }

After one `X`, all 1000 results are `1`; after two `X`s, all 1000 results are
`0`. The outcome is deterministic in both cases — the only source of randomness
in these chapters is the Hadamard gate. It is worth noting that a sample of 1000
repetitions is large enough for even a small residual probability to have shown
up in the counts; the complete absence of deviation is therefore meaningful
evidence that the outcome is certain rather than merely likely.

## Key takeaways

- Qubits and gates are the two **basic units** of quantum programs.
- Quantum gates are **reversible**; every gate possesses an inverse.
- The Pauli-X gate is the qubit equivalent of `NOT`.
- `X|0⟩ = |1⟩` and `X|1⟩ = |0⟩`; two `X` gates cancel out (`X·X = I`).
- Applying `X` to `|0⟩` and measuring always returns `1` — deterministic, not
  random.
- On the Bloch sphere, `X` is a 180° rotation about the X axis.

## The code behind this chapter

The sample that draws the circuits, the before/after Bloch spheres, and the
count charts lives in
[`src/quantum_computing_in_action/ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py).
Run it with `make ch03`.
