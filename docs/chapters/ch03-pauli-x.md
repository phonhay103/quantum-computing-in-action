# Chapter 3 — The Pauli-X gate

!!! abstract "In one sentence"
    The **Pauli-X gate** flips a qubit — `|0⟩` becomes `|1⟩` and vice versa — so
    measuring after an `X` always gives the same answer. No randomness here.

## From superposition back to certainty

Chapter 2 used the Hadamard gate to create a 50/50 superposition. This chapter
uses a gate that does the opposite kind of thing: it moves a qubit **cleanly
from one basis state to the other**, with no superposition involved.

## A NOT gate for qubits

The **Pauli-X gate** is the quantum analogue of the classical `NOT`:

$$X\,|0\rangle = |1\rangle, \qquad X\,|1\rangle = |0\rangle$$

It swaps the roles of the two basis states while leaving everything else about
the qubit consistent. Start in `|0⟩`, apply `X`, and the qubit is now certainly
`|1⟩`. Measure it and you get `1` — every single time.

!!! note "Gates are reversible"
    Unlike some classical operations, quantum gates are **reversible**: applying
    `X` twice returns the qubit to where it started (`X·X = I`, the identity).
    This reversibility is a deep property of quantum evolution, not an accident
    of this particular gate.

## Why the result is deterministic

Contrast the two chapters directly:

| | Chapter 2 (Hadamard) | Chapter 3 (Pauli-X) |
|---|---|---|
| State after the gate | `(|0⟩ + |1⟩)/√2` | `\|1⟩` |
| Probability of `0` | 50 % | 0 % |
| Probability of `1` | 50 % | 100 % |
| Repeated measurements | mixed `0`s and `1`s | always `1` |

The difference is the state, not the measuring device. A definite state measures
definitely; a balanced superposition measures randomly.

## The diagrams

### The circuit

![Pauli-X circuit](../assets/ch03-pauli-x.png){ width="420" }

Left to right: the qubit `q` starts in `|0⟩`, the `X` box flips it, and the
measurement `M` records the outcome in the classical bit `c`. The small diagram
is the whole story of the chapter.

### Before and after, on the Bloch sphere

![Qubit before and after the X gate](../assets/ch03-pauli-x-bloch.png){ width="520" }

The **Bloch sphere** makes the flip visual:

- **Before** — the arrow points to the north pole, `|0⟩`.
- **After** — the arrow points to the south pole, `|1⟩`.

Geometrically, `X` is a **180° rotation about the X axis** of the sphere. Because
the state moves from pole to pole and never touches the equator, there is no
superposition and therefore no randomness in the outcome.

## Key takeaways

- The Pauli-X gate is the qubit equivalent of `NOT`.
- `X|0⟩ = |1⟩` and `X|1⟩ = |0⟩`; two `X` gates cancel out.
- Applying `X` to `|0⟩` and measuring always returns `1` — deterministic, not random.
- On the Bloch sphere, `X` is a 180° rotation about the X axis.

## The code behind this chapter

The sample that draws the circuit and the before/after Bloch spheres lives in
[`src/quantum_computing_in_action/ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py).
Run it with `make ch03`.
