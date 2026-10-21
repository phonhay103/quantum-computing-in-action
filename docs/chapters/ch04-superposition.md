# Chapter 4 — Superposition

!!! abstract "In one sentence"
    **Superposition** is a qubit being in a weighted combination of `|0⟩` and
    `|1⟩` at once; the **Hadamard gate** creates it, and — because `H` is its own
    inverse — applying `H` a second time **cancels** it back to `|0⟩`.

## What is superposition?

A classical bit is, at every moment, definitely `0` or definitely `1`: its state
is a single value that is known with complete certainty. A qubit, by contrast,
can occupy a *combination* of both basis states at the same time — a
mathematical object written as

$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle$$

The numbers `α` and `β` are called **amplitudes**. It is worth noting that they
are not probabilities, even though they determine probabilities: an amplitude
may be negative, or indeed complex, whereas a probability can only be a
non-negative real number. The connection is established by squaring — taking
the squared magnitude of each amplitude yields the probability of observing the
corresponding basis state (see [complex numbers and phase](../foundations.md#complex-numbers-and-phase),
which develops the arithmetic of magnitudes and phases).

The reason this matters is scale. Two classical bits can hold one of four
values at a time; two *qubits* can hold a weighted combination of all four at
once (their joint state is built from the **tensor product** of the two
single-qubit states). Add more qubits and the number of amplitudes grows
**exponentially** — a register of n qubits is described by 2^n amplitudes —
while the number of qubits itself grows only linearly. For this reason, a
modest number of qubits spans an enormous amplitude space, and that space is
the raw material every quantum algorithm works with.

!!! note "You cannot read them all"
    Having `2^n` amplitudes does **not** mean that `2^n` values can be read out
    at once. A measurement returns a single outcome, and the rest of the
    amplitude information is not accessible in that step. Superposition gives
    the algorithm many amplitudes to work with, but the task of the algorithm is
    to steer the probabilities — through interference — so that the outcome that
    *is* measured turns out to be the answer.

Superposition is also relative to a **basis**: the same state can be "definite"
in one basis and "superposed" in another, so calling a state superposed is only
meaningful once a basis has been fixed. Throughout these notes the basis is
`{|0⟩, |1⟩}` unless stated otherwise.

## The state as a vector

Because a single qubit has exactly two amplitudes, its state can be written as
a **column vector**, with one entry per basis state:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}, \qquad
  |0\rangle = \begin{bmatrix}1\\ 0\end{bmatrix}, \qquad
  |1\rangle = \begin{bmatrix}0\\ 1\end{bmatrix}$$

This is the *state vector* picture: the state is represented as a point in a
two-dimensional space, and the **Born rule** turns the entries of that vector
into measurement probabilities:

$$P(0) = |\alpha|^2, \qquad P(1) = |\beta|^2, \qquad |\alpha|^2 + |\beta|^2 = 1$$

The last equation is **normalisation**: the total probability must equal 1,
since one of the two outcomes must occur at every measurement. It follows that
the amplitudes are constrained — in squared magnitude they add up to exactly 1,
so fixing one of them already restricts the value the other may take.

## Gates as matrices

If the state is a vector, then a gate is a **matrix** that multiplies it; the
action of the gate is thereby reduced to ordinary linear algebra. One rule
works for every single-qubit gate:

$$|\psi'\rangle = U\,|\psi\rangle$$

The **Pauli-X gate** from Chapter 3 becomes

$$X = \begin{bmatrix}0 & 1\\ 1 & 0\end{bmatrix}$$

so that

$$X\begin{bmatrix}\alpha\\ \beta\end{bmatrix} =
  \begin{bmatrix}\beta\\ \alpha\end{bmatrix}$$

X simply **swaps the two amplitudes** — the first entry becomes the second and
the second becomes the first — which is exactly the "flip" observed on the
Bloch sphere in Chapter 3.

## Applying X to a superposition

The matrix picture makes a subtle point easy to see. Take the even
superposition from Chapter 2 and apply `X`:

$$X\,\frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix} =
  \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix}$$

The state is **unchanged**. The reason is symmetry: an even superposition
assigns the same amplitude to both basis states, so exchanging the two entries
reproduces the very same vector. `X` flips definite states, but it leaves this
particular superposition alone — a small preview of how the *same* gate can act
very differently depending on the state it is applied to.

## The Hadamard gate

The **Hadamard gate** is the gate that *creates* superposition from a definite
state. Its matrix is

$$H = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}$$

Applied to `|0⟩`:

$$H\,|0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix}
  = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

an even mix, so a measurement gives `0` or `1` with a 50% chance each. Applied
to `|1⟩` it yields the *other* even mix, distinguished only by a minus sign in
front of the `|1⟩` term:

$$H\,|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle$$

That minus sign is a **relative phase** (see [complex numbers and phase](../foundations.md#complex-numbers-and-phase),
where relative phase is defined formally). Both states measure 50/50, yet they
are genuinely different states — and the difference is exactly what makes
interference possible.

??? question "Check yourself — if `|+⟩` and `|−⟩` both measure 50/50, how can a minus sign ever matter?"
    It matters as soon as the amplitudes are made to meet again within one and
    the same state. Apply one more `H`: `H|+⟩ = |0⟩` with certainty, while
    `H|−⟩ = |1⟩` with certainty. A measurement squares amplitudes, so on its own
    it discards the sign; the extra `H`, however, converts the sign back into a
    visible difference in measurement outcomes. That is **interference**, the
    mechanism behind every algorithm in this book.

## `H` is its own inverse

Every quantum gate is reversible, but `H` has a special property: it is its
**own inverse**, which in matrix form is

$$H \cdot H = \begin{bmatrix}1 & 0\\ 0 & 1\end{bmatrix} = I$$

where `I` is the identity (the "do nothing" operation). Two Hadamards in a row
therefore do nothing at all: the second one *undoes* exactly what the first one
did, and the state is left precisely as it was found.

$$H\,H\,|0\rangle = |0\rangle$$

Consequently, the same gate both **creates** and **removes** superposition,
depending on whether it is applied an odd or an even number of times.

## One `H` versus two

Both circuits of this chapter are placed side by side — each row of the table
is one question that can be put to the finished circuit:

| | One `H` | Two `H`s (`H·H`) |
|---|---|---|
| State | (\|0⟩ + \|1⟩)/√2 | \|0⟩ |
| Superposition? | yes | no |
| Probability of `0` | 50 % | 100 % |
| Probability of `1` | 50 % | 0 % |
| Repeated measurements | mixed `0`s and `1`s | always `0` |

The contrast is the whole point of the chapter: **applying a gate twice can
bring the system back to where it started**, and the randomness that appeared
after one `H` vanishes completely after the second.

!!! info "Where the cancellation comes from — interference"
    The single-`H` and double-`H` results are two halves of one idea. The second
    `H` gives the state two ways to reach each outcome, and the minus sign in
    `H|1⟩` makes some of those ways point in opposite directions. For `|1⟩` the
    two contributions cancel, and for `|0⟩` they reinforce — so `H·H|0⟩ = |0⟩`.
    On the Bloch sphere, one `H` moves the state from the pole to the equator
    (random); the second `H` moves it back to the pole (definite). In matrix
    language that round trip is simply `H·H = I`.

## The diagrams

### The single-`H` circuit

![Single Hadamard circuit](../assets/ch04-hadamard-circuit.png){ width="420" }

A qubit `q` starts in `|0⟩`, passes through one `H`, and the measurement `M`
writes a random `0` or `1` into the classical bit `c`. Running this circuit
repeatedly therefore produces a mixture of both outcomes rather than one fixed
answer.

### The `H·H` circuit

![Two Hadamard gates](../assets/ch04-hadamard2-circuit.png){ width="420" }

The same circuit with a **second** `H`. The two gates cancel each other, so
`M` now always reads `0`, no matter how often the experiment is repeated.

### On the Bloch sphere

![|0⟩, after H, and after H·H](../assets/ch04-hadamard-bloch.png){ width="640" }

- **`|0⟩`** — the north pole, the starting point of the experiment.
- **after `H`** — on the equator: maximum superposition, with 50/50
  randomness between the two outcomes.
- **after `H·H`** — back at the north pole: the superposition has been removed
  and the state is definite again.

### The gates as matrices

![X, H, and H·H as matrices](../assets/ch04-gate-matrices.png){ width="640" }

The `X` and `H` panels show the two gate matrices; the `H·H` panel collapses to
the identity matrix — the visual proof that two Hadamards cancel.

### What you measure

![1000 runs of H](../assets/ch04-hadamard-counts.png){ width="420" }
![1000 runs of H·H](../assets/ch04-hadamard2-counts.png){ width="420" }

After one `H`, the two bars are nearly equal, reflecting the 50/50 balance of
the superposition. After two `H`s, one bar contains all 1000 results and the
other is empty — no randomness is left at all.

## Key takeaways

- A qubit state is a **vector** `[α, β]`; the Born rule turns its entries into
  measurement probabilities.
- A gate is a **matrix** that multiplies the state vector, so every gate action
  is a matrix multiplication.
- `X` swaps the two amplitudes; `H` maps `|0⟩` to an even superposition.
- `H` is its **own inverse**: `H·H = I`, so two consecutive Hadamards cancel.
- One `H` gives random results; two `H`s return the state to `|0⟩`, giving a
  deterministic answer.
- Superposition lets a few qubits describe exponentially many amplitudes.

## The code behind this chapter

The sample that draws the circuits, the Bloch sphere, the count charts, and the
gate matrices lives in
[`src/quantum_computing_in_action/ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py),
with the matrix helpers in
[`src/quantum_computing_in_action/ch04/matrices.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/matrices.py).
Running the sample reproduces every figure of this chapter, and it is invoked
with `make ch04`.
