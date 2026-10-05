# Chapter 5 — Entanglement

!!! abstract "In one sentence"
    Two qubits can share a joint state that **cannot** be described one qubit at
    a time: the **CNOT** gate turns a superposition into a **Bell state**, whose
    two qubits always measure the *same* — perfectly correlated, yet each random.

## Two qubits at once

Chapter 4 described one qubit with two amplitudes. Two qubits need four:

$$|\psi\rangle = \alpha_{00}\,|00\rangle + \alpha_{01}\,|01\rangle
  + \alpha_{10}\,|10\rangle + \alpha_{11}\,|11\rangle$$

This is the **tensor product** of two single-qubit spaces (see
[multiple qubits and the tensor product](../foundations.md#multiple-qubits-and-the-tensor-product)).
The labels are read left to right, so `|01⟩` means the first qubit is `0` and the
second is `1`. As before, the amplitudes are not probabilities — the Born rule
squares them.

`n` qubits have `2^n` amplitudes, so the space grows very fast. That is the same
growth Chapter 4 flagged as the raw material of quantum algorithms.

## The CNOT gate

The new ingredient is a gate that acts on **two** qubits: the **controlled-NOT**
(`CNOT`). It has a **control** qubit and a **target** qubit, and it flips the
target exactly when the control is `1`.

We write two-qubit states as `|c t⟩` with the **control first** and the **target
second** — the usual textbook order. The truth table is then:

| Input <code>\|c t⟩</code> | Output <code>\|c t⟩</code> |
|-------|--------|
| <code>\|00⟩</code> | <code>\|00⟩</code> |
| <code>\|01⟩</code> | <code>\|01⟩</code> |
| <code>\|10⟩</code> | <code>\|11⟩</code> |
| <code>\|11⟩</code> | <code>\|10⟩</code> |

In `|10⟩` the control is `1`, so the target flips and the state becomes `|11⟩`;
when the control is `0` (`|00⟩`, `|01⟩`) nothing happens.

Like every quantum gate, `CNOT` is **reversible** and **unitary**. In the basis
order `|00⟩, |01⟩, |10⟩, |11⟩` its matrix is

$$CNOT = \begin{bmatrix}1&0&0&0\\ 0&1&0&0\\ 0&0&0&1\\ 0&0&1&0\end{bmatrix}$$

Applying it twice gives the identity, so `CNOT·CNOT = I`.

!!! note "A note on bit order (Qiskit)"
    Qiskit stores amplitudes in the *opposite* (little-endian) bit order: in a
    `Statevector` label the rightmost character is qubit 0. The sample therefore
    calls `cx(1, 0)` — control qubit 1, target qubit 0 — to realise the
    control-first convention used here. The printed `|q1 q0⟩` labels already put
    the control first, so nothing else changes.

## Bell states

Entanglement appears when `CNOT` acts on a superposition. Start with both qubits
in `|00⟩`, apply a Hadamard to the **control**, then `CNOT`:

$$H(\text{control}):\quad \frac{|00\rangle + |10\rangle}{\sqrt{2}}
  \quad\xrightarrow{\;CNOT\;}\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

The result is a **Bell state** (also called an EPR pair). It cannot be written as
`|a⟩|b⟩` for any single-qubit states `a` and `b` — that is exactly what
"entangled" means.

There are four Bell states, the "maximally entangled" two-qubit states:

$$\frac{|00\rangle \pm |11\rangle}{\sqrt{2}}, \qquad
  \frac{|01\rangle \pm |10\rangle}{\sqrt{2}}$$

The one above is the first; the others follow from adding a `Z` or an `X` before
the `CNOT`.

## Measuring an entangled pair

Measure the Bell state and something strange happens. The only possible outcomes
are `00` and `11`, each with probability 50%; `01` and `10` **never** occur.

- Each qubit on its own is a perfect coin: measure only qubit 0 and you get `0`
  or `1` 50/50; the same for qubit 1.
- But the two outcomes are always **equal**. The randomness is real, yet it is
  *shared*: the qubits are correlated.

This correlation does not depend on distance. If the qubits are separated, the
first measurement still seems to "decide" the second — the "spooky action at a
distance" the chapter is named after.

!!! warning "Entanglement does not send messages"
    It is tempting to think the first measurement *tells* the second qubit what
    to do, faster than light. It does not. You cannot choose the outcome you get
    — it is random — and to compare the two results you still have to send the
    classical information between the parties, at most at the speed of light.
    Entanglement gives *correlation*, not communication.

## Product states vs. entangled states

The contrast with ordinary randomness is the point of the chapter. Apply a
Hadamard to **each** qubit and no `CNOT`:

$$H(0), H(1):\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}$$

Now all four outcomes appear, about 25% each — exactly like tossing two
independent coins. This is a **product state**: knowing qubit 0 tells you nothing
about qubit 1.

A neat test separates the two cases. Reshape the four amplitudes into a 2×2
matrix. A product state has a **rank-1** matrix (every row is a multiple of the
other); a Bell state has **rank 2**. The [coefficient matrices](#coefficient-matrices)
below show the two side by side.

| | Two `H` qubits (product) | Bell state (entangled) |
|---|---|---|
| Outcomes | all four | only `00`, `11` |
| Each qubit alone | 50/50 | 50/50 |
| Joint outcome | independent | perfectly correlated |
| Amplitude matrix | rank 1 | rank 2 |

Both systems look "random" if you glance at a single qubit. The difference is in
the **correlations**.

## The diagrams

### The Bell circuit

![Bell-state circuit](../assets/ch05-bell-circuit.png){ width="460" }

The **control** qubit gets a Hadamard, then `CNOT` correlates it with the
**target**, and both are measured. This little circuit is the standard way to
*create* entanglement.

### The CNOT circuit

![CNOT circuit](../assets/ch05-cnot-circuit.png){ width="460" }

The bare `CNOT`. On its own it never creates a superposition — it only
correlates qubits that are already in one.

### What you measure (Bell state)

![1000 runs of the Bell state](../assets/ch05-bell-counts.png){ width="420" }

Only the bars for `00` and `11` have any height. The other two outcomes are
missing entirely — the visible signature of entanglement.

### What you measure (independent qubits)

![1000 runs of two independent H qubits](../assets/ch05-independent-counts.png){ width="420" }

Two independent Hadamards fill all four bars roughly equally. Each qubit is
random, but the results are **uncorrelated**.

### Independent vs. entangled

![Independent vs. entangled qubits](../assets/ch05-bell-vs-independent.png){ width="640" }

The same four outcomes, side by side. The independent qubits spread out; the
entangled pair collapses onto the two matching outcomes.

### Coefficient matrices

![Product state vs. entangled state](../assets/ch05-amplitude-matrices.png){ width="640" }

Reshaping the amplitudes into a 2×2 matrix makes the difference visual. The
product state gives a rank-1 matrix (all entries `0.50`); the Bell state gives a
diagonal rank-2 matrix. Rank 1 means "factorises"; rank 2 means "entangled".

## Key takeaways

- Two qubits live in a four-dimensional space spanned by `|00⟩, |01⟩, |10⟩, |11⟩`.
- `CNOT` flips the **target** when the **control** is `1`; it is reversible and unitary.
- `H` followed by `CNOT` prepares the Bell state `(|00⟩ + |11⟩)/√2`.
- Measuring a Bell state yields only `00` or `11` — perfectly correlated outcomes.
- Each qubit alone is still 50/50, so the randomness is in the *correlations*.
- Entanglement gives correlation, **not** faster-than-light communication.
- Two independent `H` qubits give a **product state** (all four outcomes, rank 1);
  a Bell state is **entangled** (rank 2).

## The code behind this chapter

The sample that draws the circuits, the count charts, the comparison, and the
coefficient matrices lives in
[`src/quantum_computing_in_action/ch05/entanglement.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/entanglement.py),
with the tensor-product and CNOT helpers in
[`src/quantum_computing_in_action/ch05/states.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/states.py).
Run it with `make ch05`.
