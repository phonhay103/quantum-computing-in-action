# Chapter 4 — Superposition

!!! abstract "In one sentence"
    **Superposition** is a qubit being in a weighted combination of `|0⟩` and
    `|1⟩` at once; the **Hadamard gate** creates it, and — because `H` is its own
    inverse — applying `H` a second time **cancels** it back to `|0⟩`.

## What is superposition?

A classical bit is definitely `0` or definitely `1`. A qubit can be in a
*combination* of both basis states at the same time:

$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle$$

The numbers `α` and `β` are called **amplitudes**. They are not probabilities —
they can be negative or even complex — but squaring them gives probabilities.

The reason this matters is scale. Two classical bits can hold one of four values
at a time; two *qubits* can hold a weighted combination of all four. Add more
qubits and the amount of data described grows **exponentially**, while the number
of qubits grows only linearly. That is the raw material every quantum algorithm
works with.

## The state as a vector

Because a single qubit has exactly two amplitudes, we can write its state as a
**column vector**:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}, \qquad
  |0\rangle = \begin{bmatrix}1\\ 0\end{bmatrix}, \qquad
  |1\rangle = \begin{bmatrix}0\\ 1\end{bmatrix}$$

This is the *probability vector* picture: the state is a point in a
two-dimensional space, and the **Born rule** turns the entries into measurement
probabilities:

$$P(0) = |\alpha|^2, \qquad P(1) = |\beta|^2, \qquad P(0) + P(1) = 1$$

## Gates as matrices

If the state is a vector, then a gate is a **matrix** that multiplies it. One
rule works for every single-qubit gate:

$$|\psi'\rangle = U\,|\psi\rangle$$

The **Pauli-X gate** from Chapter 3 becomes

$$X = \begin{bmatrix}0 & 1\\ 1 & 0\end{bmatrix}$$

so that

$$X\begin{bmatrix}\alpha\\ \beta\end{bmatrix} =
  \begin{bmatrix}\beta\\ \alpha\end{bmatrix}$$

X simply **swaps the two amplitudes** — which is exactly the "flip" we saw on the
Bloch sphere.

## Applying X to a superposition

The matrix picture makes a subtle point easy to see. Take the even superposition
from Chapter 2 and apply `X`:

$$X\,\frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix} =
  \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix}$$

The state is **unchanged**. An even superposition is symmetric, so swapping its
two amplitudes does nothing. `X` flips definite states, but it leaves this
particular superposition alone — a small preview of how the *same* gate can act
very differently depending on the state.

## The Hadamard gate

The **Hadamard gate** is the gate that *creates* superposition. Its matrix is

$$H = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}$$

Applied to `|0⟩`:

$$H\,|0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix}
  = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

an even mix, so measuring gives `0` or `1` with a 50% chance each.

## `H` is its own inverse

Every quantum gate is reversible, but `H` has a special property: it is its **own
inverse**, which in matrix form is

$$H \cdot H = \begin{bmatrix}1 & 0\\ 0 & 1\end{bmatrix} = I$$

where `I` is the identity (the "do nothing" operation). Two Hadamards in a row do
nothing at all: the second one *undoes* exactly what the first one did.

$$H\,H\,|0\rangle = |0\rangle$$

So the same gate both **creates** and **removes** superposition, depending on
whether it is applied an odd or an even number of times.

## One `H` versus two

| | One `H` | Two `H`s (`H·H`) |
|---|---|---|
| State | (\|0⟩ + \|1⟩)/√2 | \|0⟩ |
| Superposition? | yes | no |
| Probability of `0` | 50 % | 100 % |
| Probability of `1` | 50 % | 0 % |
| Repeated measurements | mixed `0`s and `1`s | always `0` |

The contrast is the whole point of the chapter: **applying a gate twice can bring
you back to where you started**, and the randomness that appeared after one `H`
vanishes after the second.

!!! info "Reading the diagrams together"
    The single-`H` and double-`H` results are two halves of one idea. `H` rotates
    the state by 90° on the Bloch sphere: one `H` lands on the equator (random),
    two `H`s rotate 180° in total and return to the pole (definite). In matrix
    language, that 180° is simply `H·H = I`.

## The diagrams

### The single-`H` circuit

![Single Hadamard circuit](../assets/ch04-hadamard-circuit.png){ width="420" }

A qubit `q` starts in `|0⟩`, passes through one `H`, and the measurement `M` writes
a random `0` or `1` into the classical bit `c`.

### The `H·H` circuit

![Two Hadamard gates](../assets/ch04-hadamard2-circuit.png){ width="420" }

The same circuit with a **second** `H`. The two gates cancel, so `M` now always
reads `0`.

### On the Bloch sphere

![|0>, after H, and after H·H](../assets/ch04-hadamard-bloch.png){ width="640" }

- **`|0⟩`** — north pole, the starting point.
- **after `H`** — on the equator: maximum superposition, 50/50 randomness.
- **after `H·H`** — back to the north pole: the superposition is gone.

### The gates as matrices

![X, H, and H·H as matrices](../assets/ch04-gate-matrices.png){ width="640" }

The `X` and `H` panels show the two gate matrices; the `H·H` panel is the identity
— the visual proof that two Hadamards cancel.

### What you measure

![1000 runs of H](../assets/ch04-hadamard-counts.png){ width="420" }
![1000 runs of H·H](../assets/ch04-hadamard2-counts.png){ width="420" }

After one `H`, the two bars are nearly equal. After two `H`s, one bar contains all
1000 results and the other is empty — no randomness left at all.

## Key takeaways

- A qubit state is a **vector** `[α, β]`; the Born rule turns it into probabilities.
- A gate is a **matrix** that multiplies the state vector.
- `X` swaps the two amplitudes; `H` maps `|0⟩` to an even superposition.
- `H` is its **own inverse**: `H·H = I`.
- One `H` gives random results; two `H`s give a deterministic `0`.
- Superposition lets a few qubits describe exponentially many amplitudes.

## The code behind this chapter

The sample that draws the circuits, the Bloch sphere, the count charts, and the
gate matrices lives in
[`src/quantum_computing_in_action/ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py),
with the matrix helpers in
[`src/quantum_computing_in_action/ch04/matrices.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/matrices.py).
Run it with `make ch04`.
