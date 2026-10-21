# Foundations

These notes presuppose a modest acquaintance with linear algebra and make no
assumption of prior knowledge in quantum mechanics. This page collects the small
set of background ideas on which every chapter relies: bits and qubits,
amplitudes and probabilities, complex phases, vectors and unitary gates, the
circuit model, measurement bases, and the arithmetic behind periodic functions.
It is best read once at the outset, and consulted again whenever a chapter uses
a term that is not immediately recognisable.

Every term introduced here has its own entry in the
**[Glossary](glossary.md)**, with the Vietnamese equivalent alongside; the
glossary can therefore serve both as a quick reference and as a bilingual index
of the vocabulary used throughout the book.

## Bits, qubits, and Dirac notation

A classical **bit** is a quantity that is always either `0` or `1`; at every
moment the bit holds exactly one of these two values, and nothing in between. A
quantum bit — a **qubit** — differs in precisely this respect: it can be prepared
in, or evolve into, a *combination* of both classical values at the same time.
The state of a qubit is written as

$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle$$

The symbols `|0⟩` and `|1⟩` denote the two **basis states** and are read "ket
zero" and "ket one". A ket such as `|ψ⟩` is nothing more than a label attached to
a state; the information lives in the numbers placed in front of the basis
states. In other words, all kets are merely names, and it is the coefficients
that distinguish one state from another.

## Amplitudes, probabilities, and the Born rule

The numbers `α` and `β` are **amplitudes**, not probabilities. This distinction
matters: amplitudes can be negative and even complex, whereas a probability must
always be a non-negative real number. To turn amplitudes into probabilities,
their magnitudes are squared — the **Born rule**:

$$P(0) = |\alpha|^2, \qquad P(1) = |\beta|^2$$

Because the two outcomes are exhaustive — a measurement must yield one of them —
the probabilities have to sum to one, and consequently the amplitudes satisfy

$$|\alpha|^2 + |\beta|^2 = 1$$

This is the **normalisation** condition: it says the state has "total weight" 1,
meaning that the probability is distributed entirely between the two possible
outcomes and none is lost.

## Complex numbers and phase

Amplitudes are complex numbers, so each one carries a **magnitude** and a
**phase**. The phase of a single amplitude on its own is not observable —
multiplying the whole state by `e^{iθ}` changes no measurement statistic and
therefore describes the same physics. What *is* observable is a **relative
phase**: a difference between the phases of two parts of the same state.
Relative phases determine whether amplitudes add up or cancel out when they are
combined — the effect called **interference**. It is interference, rather than
the absolute phase, that carries measurable consequences.

## Vectors, matrices, and unitary gates

In the vector picture of quantum mechanics, a one-qubit state is a two-entry
**column vector**:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}$$

A **gate** is represented by a matrix that multiplies the state; the
multiplication turns the initial state into the new state

$$|\psi'\rangle = U\,|\psi\rangle$$

Quantum gates are **unitary**: `U^† U = I`. Unitarity is the mathematical reason
a gate is reversible — applying the inverse gate undoes its effect exactly — and
it also guarantees that the gate preserves the normalisation of the state, so
the output remains a valid probability distribution.

## Multiple qubits and the tensor product

Two qubits are not two separate vectors glued together — their joint state is
the **tensor product** of the individual states, written `|a⟩ ⊗ |b⟩` (or just
`|a⟩|b⟩`). Since each factor contributes two basis states, the tensor product of
two two-dimensional states has four basis states in total:

$$|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle$$

The label is read left to right: `|01⟩` means the first character is `0` and the
second is `1`. Just as with one qubit, the joint state is a weighted sum of
these four basis states, and the probability of each measurement outcome is the
squared magnitude of the corresponding amplitude.

A state that *can* be written as a tensor product is called a **product state**;
states of this kind can be reasoned about one qubit at a time. A state that
cannot be written this way is **entangled** (Chapter 5), and entanglement gives
rise to behaviour that no product state can reproduce.

## The circuit model

A quantum circuit is read **left to right**, in the same direction in which time
flows during the computation. Each horizontal **wire** is a qubit, each **box**
on a wire is a gate applied to that qubit, and a **meter** at the end is a
measurement that produces a classical bit as its output. Running the same
circuit many times is called taking **shots**; the resulting tallies of outcomes
are what the count charts show.

## The Bloch sphere

The **Bloch sphere** is a geometric picture of a single qubit: every possible
state of one qubit corresponds to a point on the sphere's surface. The **north
pole** is `|0⟩` and the **south pole** is `|1⟩`. The **equator** holds the states
that are an even 50/50 mix of the two. Any single-qubit state is a point on the
surface, described by two angles, `θ` and `φ`. It is worth noting that the
sphere only works for one qubit — it does not extend to entangled states, which
cannot be located anywhere on it.

## Measurement bases

A measurement is always made **in a basis**, and a qubit carries a definite bit
only once the basis is fixed; asking what the qubit's bit is without specifying
a basis is not a well-posed question. The default is the **Z basis**, whose
states are `|0⟩` and `|1⟩` — the ordinary bit. Rotating both states by a
Hadamard gives the **X basis**, `|+⟩ = (|0⟩ + |1⟩)/√2` and
`|−⟩ = (|0⟩ − |1⟩)/√2`.

The rule that makes bases matter is short: **measuring a qubit in the basis in
which it was prepared yields a certain answer, whereas measuring it in the other
basis yields the outcome of a fair coin.** Formally, `|⟨+|0⟩|² = ½` — the two
bases are 45° apart on the Bloch sphere, so each basis state is an even mix of
the other basis's states. Consequently, a measurement in the "wrong" basis is
genuinely unpredictable. This is the fact behind
[Chapter 8](chapters/ch08-secure-communication.md) on secure communication: a
base is something a bit can be hidden behind, and an eavesdropper who guesses
the wrong base disturbs the state and can thereby be detected.

## Periodic functions and modular arithmetic

`a mod N` is the **remainder** when `a` is divided by `N`: for example,
`17 mod 15 = 2`, and by definition `a mod N` always lands between `0` and
`N − 1`. Two numbers are **coprime** when their only common divisor is 1, and
`gcd(a, N)` — the greatest common divisor — is computed by the Euclidean
algorithm in time `O(log N)`, that is, it grows only logarithmically with `N`.

The **sequence** `f(x) = a^x mod N` is what [Chapter 11](chapters/ch11-shors-algorithm.md)
on Shor's algorithm hunts. It is always **periodic** when `a` and `N` are
coprime: after some number of steps `r` the values repeat exactly, in the sense
that `a^(x+r) = a^x mod N`, and the smallest such `r` is the **order** of `a`
modulo `N`. For `a = 2`, `N = 15` the values run
`1, 2, 4, 8, 1, 2, 4, 8, …`, so the order is 4.

Finding that `r` is *order finding*, and it is as hard as factoring classically.
The trick that makes it easy quantumly is the **Fourier transform**: a periodic
list of values turns into a few sharp **peaks** when transformed, and the peaks
sit at multiples of `1/r`. Reading a peak back as a fraction recovers `r`, and
`r` turns into the factors of `N` with two `gcd` calls. In other words, the
quantum part of the computation reduces factoring to a period-finding problem,
which the Fourier transform solves efficiently.

## Growth rates and Big-O

How fast a computation grows as its input size increases is described using
**Big-O notation**: `O(f)` means "grows no faster than `f`, up to constant
factors". Growth is called

- **polynomial** when it grows like `b`, `b²`, `b³`, … — doubling `b` multiplies
  the work by a small constant, so the cost remains manageable as the input
  expands;
- **exponential** when it grows like `2^b`, `e^b`, … — adding one bit can double
  the work, which is why exponential costs quickly become prohibitive;
- **sub-exponential** when it sits between the two: faster than any polynomial
  but slower than a full exponential, an improvement over brute-force cost that
  still falls short of polynomial efficiency.
