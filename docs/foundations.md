# Foundations

These notes assume you can read a little linear algebra and are new to quantum
mechanics. This page collects the small set of background ideas every chapter
leans on. Skim it once, then come back whenever a chapter uses a term you do not
recognise.

Every term here has its own entry in the **[Glossary](glossary.md)**, with the
Vietnamese equivalent alongside.

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

## Measurement bases

A measurement is always made **in a basis**, and a qubit carries a definite bit
only once the basis is fixed. The default is the **Z basis**, whose states are
`|0⟩` and `|1⟩` — the ordinary bit. Rotating both states by a Hadamard gives the
**X basis**, `|+⟩ = (|0⟩ + |1⟩)/√2` and `|−⟩ = (|0⟩ − |1⟩)/√2`.

The rule that makes bases matter is short: **measure in the basis a state was
prepared in and you get a certain answer; measure in the other basis and you get a
fair coin.** Formally, `|⟨+|0⟩|² = ½` — the two bases are 45° apart on the Bloch
sphere, so each basis state is an even mix of the other basis's states. This is
the fact behind [Chapter 8](chapters/ch08-secure-communication.md): a base is
something you can hide a bit behind, and an eavesdropper who guesses the wrong
base disturbs the state.

## Periodic functions and modular arithmetic

`a mod N` is the **remainder** when `a` is divided by `N`: `17 mod 15 = 2`, and
`a mod N` always lands between `0` and `N − 1`. Two numbers are **coprime** when
their only common divisor is 1, and `gcd(a, N)` — the greatest common divisor —
is computed by the Euclidean algorithm in time `O(log N)`.

The **sequence** `f(x) = a^x mod N` is what [Chapter 11](chapters/ch11-shors-algorithm.md)
hunts. It is always **periodic** when `a` and `N` are coprime: after some number of
steps `r` the values repeat exactly (`a^(x+r) = a^x mod N`), and the smallest such
`r` is the **order** of `a` modulo `N`. For `a = 2`, `N = 15` the values run
`1, 2, 4, 8, 1, 2, 4, 8, …`, so the order is 4.

Finding that `r` is *order finding*, and it is as hard as factoring classically.
The trick that makes it easy quantumly is the **Fourier transform**: a periodic
list of values turns into a few sharp **peaks** when you transform it, and the
peaks sit at multiples of `1/r`. Reading a peak back as a fraction recovers `r`,
and `r` turns into the factors of `N` with two `gcd` calls.

## Growth rates and Big-O

We describe how fast a computation grows using **Big-O notation**: `O(f)` means
"grows no faster than `f`, up to constant factors". Growth is called

- **polynomial** when it grows like `b`, `b²`, `b³`, … — doubling `b` multiplies
  the work by a small constant;
- **exponential** when it grows like `2^b`, `e^b`, … — adding one bit can double
  the work;
- **sub-exponential** when it sits between the two: faster than any polynomial
  but slower than a full exponential.
