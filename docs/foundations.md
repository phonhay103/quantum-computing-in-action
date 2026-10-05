# Foundations

These notes assume you can read a little linear algebra and are new to quantum
mechanics. This page collects the small set of background ideas every chapter
leans on. Skim it once, then come back whenever a chapter uses a term you do not
recognise.

## Bits, qubits, and Dirac notation

A classical **bit** is `0` or `1`. A quantum bit — a **qubit** — can also be a
*combination* of both. We write its state as

$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle$$

The symbols `|0⟩` and `|1⟩` are the two **basis states**, read "ket zero" and
"ket one". A ket such as `|ψ⟩` is just a label for a state; the information lives
in the numbers placed in front of the basis states.

## Amplitudes, probabilities, and the Born rule

The numbers `α` and `β` are **amplitudes**, not probabilities. They can be
negative and even complex. To turn them into probabilities you square their
magnitudes — the **Born rule**:

$$P(0) = |\alpha|^2, \qquad P(1) = |\beta|^2$$

Because the two outcomes are exhaustive, the amplitudes satisfy

$$|\alpha|^2 + |\beta|^2 = 1$$

This is the **normalisation** condition: it says the state has "total weight" 1.

## Complex numbers and phase

Amplitudes are complex numbers, so each one carries a **magnitude** and a
**phase**. The phase of a single amplitude on its own is not observable —
multiplying the whole state by `e^{iθ}` describes the same physics. What *is*
observable is a **relative phase**: a difference between the phases of two parts
of the same state. Relative phases are what make amplitudes add up or cancel out
— the effect called **interference**.

## Vectors, matrices, and unitary gates

A one-qubit state is a two-entry **column vector**:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}$$

A **gate** is a matrix that multiplies the state:

$$|\psi'\rangle = U\,|\psi\rangle$$

Quantum gates are **unitary**: `U^† U = I`. Unitarity is the mathematical reason
a gate is reversible and preserves the normalisation of the state.

## Multiple qubits and the tensor product

Two qubits are not two separate vectors glued together — their joint state is the
**tensor product** of the individual states, written `|a⟩ ⊗ |b⟩` (or just
`|a⟩|b⟩`). The tensor product of two two-dimensional states has four basis
states:

$$|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle$$

The label is read left to right: `|01⟩` means the first character is `0` and the
second is `1`. As with one qubit, the state is a weighted sum of these four
amplitudes, and measurement probabilities are their squared magnitudes.

A state that *can* be written as a tensor product is called a **product state**;
a state that cannot is **entangled** (Chapter 5).

## The circuit model

A quantum circuit is read **left to right**. Each horizontal **wire** is a qubit,
each **box** on a wire is a gate, and a **meter** at the end is a measurement
that produces a classical bit. Running a circuit many times is called taking
**shots**; the resulting tallies are what the count charts show.

## The Bloch sphere

The **Bloch sphere** is a geometric picture of a single qubit. The **north pole**
is `|0⟩` and the **south pole** is `|1⟩`. The **equator** holds the states that
are an even 50/50 mix of the two. Any single-qubit state is a point on the
surface, described by two angles, `θ` and `φ`. The sphere only works for one
qubit — it does not extend to entangled states.

## Growth rates and Big-O

We describe how fast a computation grows using **Big-O notation**: `O(f)` means
"grows no faster than `f`, up to constant factors". Growth is called

- **polynomial** when it grows like `b`, `b²`, `b³`, … — doubling `b` multiplies
  the work by a small constant;
- **exponential** when it grows like `2^b`, `e^b`, … — adding one bit can double
  the work;
- **sub-exponential** when it sits between the two: faster than any polynomial
  but slower than a full exponential.
