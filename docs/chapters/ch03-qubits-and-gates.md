# Chapter 3 — Qubits and quantum gates

!!! abstract "In one sentence"
    A **qubit** is the basic unit of quantum information and a **gate** is a
    reversible operation on it; the first gate to meet is **Pauli-X**, which
    flips `|0⟩` to `|1⟩` deterministically — the quantum `NOT`.

## The basic units

Quantum programs are built from two very small pieces:

- a **qubit** — the carrier of quantum information, with basis states `|0⟩` and
  `|1⟩`;
- a **gate** — an operation applied to one or more qubits.

Everything later in the book (superposition, entanglement, whole algorithms) is
assembled from these two ideas. That is why this chapter is the "basic units"
chapter: before doing anything clever, we need to know what a qubit is and how a
gate changes it.

## Qubits

A classical bit is `0` or `1`. A qubit can be either of those, but it can also be
in a **superposition** — a weighted combination of both. Chapter 2 already used
that to make random bits. Here we focus on the simplest thing a gate can do: move
a qubit cleanly between the two basis states.

Keep a scale fact for later: `n` qubits are described by `2^n` amplitudes, so the
count doubles with every extra qubit. That growth is the raw material of
Chapter 4 and beyond.

## Gates are reversible

A defining property of quantum gates is that they are **reversible**: information
is never thrown away. Every gate has an inverse that restores the previous state.
This contrasts with familiar classical gates — `AND` takes two inputs and returns
one, so the inputs cannot be recovered from the output. Mathematically,
reversibility means a gate is a **unitary** matrix
(see [vectors, matrices, and unitary gates](../foundations.md#vectors-matrices-and-unitary-gates)),
which Chapter 4 spells out.

- The inverse of `X` is `X` itself: `X·X = I`.
- The inverse of `H` is `H` itself too (Chapter 4).

Here `I` is the **identity** operation — "do nothing". This reversibility is not
a detail; it is what lets quantum circuits be built up and undone.

!!! note "Measurement is the exception"
    Gates are reversible, but a **measurement** is not: it collapses the state
    and leaves a single classical result. That asymmetry is why a quantum
    algorithm is written as a reversible circuit followed by a measurement.

## A NOT gate for qubits

The **Pauli-X gate** is the quantum analogue of the classical `NOT`:

$$X\,|0\rangle = |1\rangle, \qquad X\,|1\rangle = |0\rangle$$

It swaps the roles of the two basis states while leaving everything else about
the qubit consistent. Start in `|0⟩`, apply `X`, and the qubit is now certainly
`|1⟩`. Measure it and you get `1` — every single time.

## The gates you will meet

`X` is the first gate, but it is one of a small family. `H` (Chapter 2) creates
superposition, and a **two-qubit** gate such as `CNOT` arrives with entanglement
in Chapter 5. For now the point is that every gate shares the same two rules: it
is reversible, and it moves the qubit to a definite point on the Bloch sphere.

## Why the result is deterministic

Contrast the two chapters directly:

| | Chapter 2 (Hadamard) | Chapter 3 (Pauli-X) |
|---|---|---|
| State after the gate | (\|0⟩ + \|1⟩)/√2 | \|1⟩ |
| Probability of `0` | 50 % | 0 % |
| Probability of `1` | 50 % | 100 % |
| Repeated measurements | mixed `0`s and `1`s | always `1` |

The difference is the state, not the measuring device. A definite state measures
definitely; a balanced superposition measures randomly. (Throughout, "measure"
means a measurement in the computational `{|0⟩, |1⟩}` basis — the same Z axis the
Bloch sphere's poles represent.)

## The diagrams

### The circuit

![Pauli-X circuit](../assets/ch03-pauli-x.png){ width="420" }

Left to right: the qubit `q` starts in `|0⟩`, the `X` box flips it, and the
measurement `M` records the outcome in the classical bit `c`. The small diagram
is the whole story of the chapter.

### Two `X` gates cancel

![Two Pauli-X gates](../assets/ch03-pauli-x2-circuit.png){ width="420" }

Because `X·X = I`, the second `X` undoes the first. A circuit is just gates in a
sequence, and the sequence `X, X` is equivalent to doing nothing.

### Before, after one `X`, after two

![Qubit before, after X, and after X·X](../assets/ch03-pauli-x-bloch.png){ width="720" }

The **Bloch sphere** makes the flip visual:

- **Before** — the arrow points to the north pole, `|0⟩`.
- **After one `X`** — the arrow points to the south pole, `|1⟩`.
- **After two `X`s** — back to the north pole, `|0⟩`.

Geometrically, `X` is a **180° rotation about the X axis** of the sphere. Because
the state moves from pole to pole and never touches the equator, there is no
superposition and therefore no randomness in the outcome.

### What you measure

![1000 runs of X](../assets/ch03-pauli-x-counts.png){ width="420" }
![1000 runs of X·X](../assets/ch03-pauli-x2-counts.png){ width="420" }

After one `X` all 1000 results are `1`; after two `X`s all 1000 results are `0`.
Deterministic in both cases — the only randomness in these chapters comes from
the Hadamard gate.

## Key takeaways

- Qubits and gates are the two **basic units** of quantum programs.
- Quantum gates are **reversible**; every gate has an inverse.
- The Pauli-X gate is the qubit equivalent of `NOT`.
- `X|0⟩ = |1⟩` and `X|1⟩ = |0⟩`; two `X` gates cancel out (`X·X = I`).
- Applying `X` to `|0⟩` and measuring always returns `1` — deterministic, not random.
- On the Bloch sphere, `X` is a 180° rotation about the X axis.

## The code behind this chapter

The sample that draws the circuits, the before/after Bloch spheres, and the count
charts lives in
[`src/quantum_computing_in_action/ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py).
Run it with `make ch03`.
