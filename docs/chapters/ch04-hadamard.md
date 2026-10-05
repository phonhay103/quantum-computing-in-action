# Chapter 4 — The Hadamard gate

!!! abstract "In one sentence"
    The **Hadamard gate** turns a definite qubit into an even superposition, and —
    because it is its own inverse — applying it a second time **cancels the
    superposition** and returns the qubit to `|0⟩`.

## The gate that creates superposition

Chapter 3 used the Pauli-X gate, which only ever moves a qubit between the two
poles `|0⟩` and `|1⟩`. The **Hadamard gate** (`H`) is different: it takes a
definite state and puts it exactly *between* the poles.

$$H\,|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}, \qquad
  H\,|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$$

Applied to `|0⟩`, the qubit becomes an even mixture: measure it and you get `0` or
`1` with equal probability. This is the same superposition Chapter 2 used for its
random bits — Chapter 4 looks at the gate itself in more detail.

## `H` is its own inverse

Every quantum gate is reversible, but `H` has a special property: it is its **own
inverse**,

$$H \cdot H = I$$

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

!!! info "Reading the two diagrams together"
    The single-`H` and double-`H` results are two halves of one idea. If `H`
    rotated the state by 90° on the Bloch sphere, then one `H` lands on the
    equator (random) and two `H`s rotate 180° in total, returning to the pole
    (definite).

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

### What you measure

![1000 runs of H](../assets/ch04-hadamard-counts.png){ width="420" }
![1000 runs of H·H](../assets/ch04-hadamard2-counts.png){ width="420" }

After one `H`, the two bars are nearly equal. After two `H`s, one bar contains all
1000 results and the other is empty — no randomness left at all.

## Key takeaways

- The Hadamard gate **creates** an even superposition from `|0⟩`.
- `H` is its **own inverse**: `H·H = I`.
- One `H` gives random results; two `H`s give a deterministic `0`.
- On the Bloch sphere, `H` rotates the state toward the equator (and back).

## The code behind this chapter

The sample that draws the circuits, the Bloch sphere, and the count charts lives in
[`src/quantum_computing_in_action/ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py).
Run it with `make ch04`.
