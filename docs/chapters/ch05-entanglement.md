# Chapter 5 — Entanglement

!!! abstract "In one sentence"
    A single **CNOT** gate, applied to a suitable two-qubit superposition,
    converts it into a **Bell state** — a joint state whose two qubits always
    measure the *same* and which cannot be described one qubit at a time.

## Two qubits at once

Chapter 4 described a single qubit by means of two amplitudes; a pair of qubits
requires four:

$$|\psi\rangle = \alpha_{00}\,|00\rangle + \alpha_{01}\,|01\rangle
  + \alpha_{10}\,|10\rangle + \alpha_{11}\,|11\rangle$$

Formally, such a state lives in the **tensor product** of the two individual
one-qubit spaces, a construction treated in detail on the foundations page (see
[multiple qubits and the tensor product](../foundations.md#multiple-qubits-and-the-tensor-product)).
The four-character labels are read from left to right, so the ket `|01⟩`
signifies that the first qubit carries the value `0` while the second carries
the value `1`. As in the single-qubit case, the amplitudes are not themselves
probabilities — it is the Born rule that squares them into measurement
statistics.

For `n` qubits, the description of the state involves `2^n` amplitudes, so the
space grows very rapidly with every additional qubit. This is the same
exponential growth that Chapter 4 identified as the raw material on which the
power of quantum algorithms rests.

## The CNOT gate

The new ingredient of this chapter is a gate that acts on **two** qubits
simultaneously: the **controlled-NOT** gate (`CNOT`). The gate distinguishes a
**control** qubit from a **target** qubit, and it flips the target precisely
when the control carries the value `1`; whenever the control is `0`, the target
qubit is left completely untouched.

We write two-qubit states as `|c t⟩`, with the **control first** and the
**target second** — the usual textbook order. The truth table is then:

| Input <code>\|c t⟩</code> | Output <code>\|c t⟩</code> |
|-------|--------|
| <code>\|00⟩</code> | <code>\|00⟩</code> |
| <code>\|01⟩</code> | <code>\|01⟩</code> |
| <code>\|10⟩</code> | <code>\|11⟩</code> |
| <code>\|11⟩</code> | <code>\|10⟩</code> |

In the state `|10⟩` the control is `1`, so the target flips and the output
becomes `|11⟩`; in `|11⟩` the same action returns the pair to `|10⟩`. When the
control is `0` (`|00⟩`, `|01⟩`) nothing happens: the state passes through the
gate unchanged.

Like every quantum gate, `CNOT` is **reversible** and **unitary**. In the basis
order `|00⟩, |01⟩, |10⟩, |11⟩` its matrix is

$$CNOT = \begin{bmatrix}1&0&0&0\\ 0&1&0&0\\ 0&0&0&1\\ 0&0&1&0\end{bmatrix}$$

Applying the gate twice yields the identity, so `CNOT·CNOT = I`; in other
words, a second application undoes the effect of the first.

!!! note "A note on bit order (Qiskit)"
    Qiskit stores amplitudes in the *opposite* (little-endian) bit order: in a
    `Statevector` label the rightmost character is qubit 0, which is the reverse
    of the order in which the states are written above. For this reason the
    sample calls `cx(1, 0)` — control qubit 1, target qubit 0 — so as to realise
    the control-first convention used in this chapter. Because the printed
    `|q1 q0⟩` labels already place the control first, nothing else changes: the
    displayed results match the mathematics exactly.

## Bell states

Entanglement appears when `CNOT` acts on a superposition rather than on a
single basis state. Begin with both qubits in `|00⟩`, apply a Hadamard to the
**control**, and then apply `CNOT`:

$$H(\text{control}):\quad \frac{|00\rangle + |10\rangle}{\sqrt{2}}
  \quad\xrightarrow{\;CNOT\;}\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

The result of this two-step procedure is a **Bell state** (also called an EPR
pair). It cannot be written in the product form `|a⟩|b⟩` for any single-qubit
states `a` and `b`, and it is precisely this impossibility of factorising the
state that the word "entangled" refers to.

Four Bell states exist, and together they exhaust the "maximally entangled"
two-qubit states:

$$\frac{|00\rangle \pm |11\rangle}{\sqrt{2}}, \qquad
  \frac{|01\rangle \pm |10\rangle}{\sqrt{2}}$$

The state obtained above is the first of the four; the remaining three follow
from inserting a `Z` or an `X` gate before the `CNOT`, which reshapes the
Hadamard superposition that the CNOT subsequently correlates.

## Measuring an entangled pair

When the Bell state is measured, something remarkable happens. The only
possible outcomes are `00` and `11`, each with probability 50%; the outcomes
`01` and `10` **never** occur.

- Each qubit, considered on its own, behaves like a perfect coin: measuring
  only qubit 0 yields `0` or `1` in a 50/50 split, and the same holds for
  qubit 1.
- The two measurement results, however, are always **equal**. The randomness is
  real, but it is *shared* between the two qubits: the outcomes are correlated.

This correlation does not depend on the distance separating the qubits. If the
qubits are carried far apart, the first measurement still appears to "decide"
the second — the "spooky action at a distance" the chapter is named after.

!!! warning "Entanglement does not send messages"
    It is tempting to imagine that the first measurement *tells* the second
    qubit what to do, faster than light. It does not. No experimenter can
    choose the outcome obtained — it is genuinely random — and in order to
    compare the two results, the classical information must still be sent
    between the parties, at no more than the speed of light. Entanglement
    therefore provides *correlation*, not communication.

## Product states vs. entangled states

The contrast with ordinary randomness is the point of the chapter. Apply a
Hadamard to **each** qubit and no `CNOT` at all:

$$H(0), H(1):\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}$$

Now all four outcomes appear, about 25% each — exactly the pattern expected
from tossing two independent coins. Such a state is a **product state**:
knowing the value of qubit 0 conveys no information whatsoever about qubit 1.

A neat test separates the two cases. Reshape the four amplitudes into a 2×2
matrix. A product state has a **rank-1** matrix — every row is a multiple of
the other, so the state factors apart into its two components. A Bell state
has **rank 2** — the rows are independent, and consequently the state does not
factor.

Rank is the number of independent rows; for a 2×2 matrix it is simply 1 or 2.
This number is the state's **Schmidt rank**: 1 means product, 2 means
entangled. The [coefficient matrices](#coefficient-matrices) below show the two
cases side by side.

The table below pits the two states against each other, one question per row;
the last row is the test the diagrams at the end make visual:

| | Two `H` qubits (product) | Bell state (entangled) |
|---|---|---|
| Outcomes | all four | only `00`, `11` |
| Each qubit alone | 50/50 | 50/50 |
| Joint outcome | independent | perfectly correlated |
| Amplitude matrix | rank 1 | rank 2 |

Both systems look "random" when only a single qubit is inspected; the
difference lies in the **correlations** between the outcomes.

??? question "Check yourself — each qubit alone is 50/50 in both states. What single experiment tells them apart?"
    Count how often the two measurement outcomes *agree*. With two independent
    `H` qubits, all four joint outcomes are equally likely, so agreement occurs
    about half the time (`00` and `11` are 2 of the 4 outcomes). With the Bell
    state, agreement occurs 100% of the time — `00` and `11` are the *only*
    outcomes. That single count is the difference between two random coins and
    one shared coin.

## The diagrams

### The Bell circuit

![Bell-state circuit](../assets/ch05-bell-circuit.png){ width="460" }

The **control** qubit receives a Hadamard, `CNOT` then correlates it with the
**target**, and both qubits are measured. This small circuit is the standard
procedure for *creating* entanglement from an initially uncorrelated pair.

### The CNOT circuit

![CNOT circuit](../assets/ch05-cnot-circuit.png){ width="460" }

The bare `CNOT` gate in isolation. On its own it never creates a superposition
— it only correlates qubits that are already in one.

### What you measure (Bell state)

![1000 runs of the Bell state](../assets/ch05-bell-counts.png){ width="420" }

Only the bars for `00` and `11` have any height; the other two outcomes are
missing entirely. This absence is the visible signature of entanglement.

### What you measure (independent qubits)

![1000 runs of two independent H qubits](../assets/ch05-independent-counts.png){ width="420" }

Two independent Hadamards fill all four bars roughly equally. Each qubit is
individually random, yet the results are **uncorrelated**.

### Independent vs. entangled

![Independent vs. entangled qubits](../assets/ch05-bell-vs-independent.png){ width="640" }

The same four outcomes, side by side. The independent qubits spread out over
all possibilities, while the entangled pair collapses onto the two matching
outcomes.

### Coefficient matrices

![Product state vs. entangled state](../assets/ch05-amplitude-matrices.png){ width="640" }

Reshaping the amplitudes into a 2×2 matrix makes the difference visual. The
product state yields a rank-1 matrix (all entries `0.50`); the Bell state
yields a diagonal rank-2 matrix. Rank 1 signifies a state that factorises;
rank 2 signifies an entangled state.

## Key takeaways

- Two qubits live in a four-dimensional space spanned by `|00⟩, |01⟩, |10⟩, |11⟩`, with one amplitude for each basis state.
- `CNOT` flips the **target** exactly when the **control** is `1`; the gate is reversible and unitary.
- `H` followed by `CNOT` prepares the Bell state `(|00⟩ + |11⟩)/√2`.
- Measuring a Bell state yields only `00` or `11` — perfectly correlated outcomes.
- Each qubit alone is still 50/50, so the randomness resides in the *correlations* rather than in either qubit individually.
- Entanglement gives correlation, **not** faster-than-light communication: comparing the two results still requires classical messaging.
- Two independent `H` qubits give a **product state** (all four outcomes, rank 1); a Bell state is **entangled** (rank 2).

## The code behind this chapter

The sample that draws the circuits, the count charts, the comparison, and the
coefficient matrices lives in
[`src/quantum_computing_in_action/ch05/entanglement.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/entanglement.py),
with the tensor-product and CNOT helpers in
[`src/quantum_computing_in_action/ch05/states.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/states.py).
The whole presentation can be reproduced locally by running `make ch05`.
