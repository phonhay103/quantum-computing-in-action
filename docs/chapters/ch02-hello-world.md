# Chapter 2 — Hello World, quantum computing style

!!! abstract "In one sentence"
    Applying a Hadamard gate to a qubit places it into **superposition**, and a
    subsequent measurement then yields `0` or `1` with equal probability — a form
    of randomness that originates in physics itself, not in a hidden algorithm.

## Why "Hello World"?

Every programming language tradition begins with a program that prints
`Hello, World!`. The program is small enough to type in a few seconds, yet it
serves an important purpose: it demonstrates that the entire toolchain —
compiler, runtime, and output path — is functioning correctly. Quantum
computing requires the same kind of first program, one that confirms the
environment before any deeper material is attempted.

The distinctive feature is that the smallest *interesting* quantum program
accomplishes something a classical program cannot: it produces a **truly
random bit**. That is the quantum "Hello World" — one qubit, one gate, and one
measurement. In other words, the whole demonstration fits on a single circuit
line, yet nothing classical can replicate its outcome deterministically.

## Classical bits vs. qubits

A classical bit is always exactly one of two values: `0` **or** `1`. The value
is well-defined at every moment, and reading the bit simply reports what is
already there. A **qubit**, by contrast, can additionally occupy a
*combination* of both values at once. Written in the Dirac notation used
throughout the book, the relevant states are:

- `|0⟩` — the state that always measures as `0`
- `|1⟩` — the state that always measures as `1`
- a **superposition**, e.g. `(|0⟩ + |1⟩) / √2` — an even mixture of the two

The symbols `|…⟩` are merely a labelling convention for naming states; the
physical content resides in the coefficients attached to each term, since those
coefficients determine what a measurement will reveal. A fuller treatment of
bits, qubits, and Dirac notation is provided in
[bits, qubits, and Dirac notation](../foundations.md#bits-qubits-and-dirac-notation).

## The Hadamard gate

The **Hadamard gate** (`H`) is the standard mechanism for creating an even
superposition. Applied to the initial state, it acts as follows:

$$H\,|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

If the qubit starts in `|0⟩`, a single `H` places it into a state consisting of
exactly half `|0⟩` and half `|1⟩`. The `1/√2` factors are **amplitudes**, not
probabilities (see [amplitudes and the Born rule](../foundations.md#amplitudes-probabilities-and-the-born-rule)).
It is worth noting that squaring the amplitudes is what produces the
probabilities, and it is precisely this operation that ensures the
probabilities of all outcomes add up to 1. Consequently, the gate does not
*select* an outcome; it only prepares the state from which an outcome will
later be drawn by measurement.

## Measurement and the Born rule

A superposition is never *observed* directly. At the moment the qubit is
**measured**, it collapses to one of the basis states, and the probability of
each outcome is the square of that state's coefficient — this prescription is
the **Born rule**:

$$P(0) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}, \qquad
  P(1) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}$$

A single run of the experiment yields a single bit, and nothing more can be
inferred from that one trial. When the experiment is repeated many times — by
taking many **shots** — the two outcomes appear in nearly equal numbers, which
is exactly what the Born rule predicts statistically.

!!! info "Why this is *genuinely* random"
    A classical `random()` function is usually **pseudo-random**: its output
    appears random, yet the entire sequence is fully determined by a hidden
    seed, so it can be reproduced given the same starting conditions. A
    measured qubit has no hidden value waiting to be revealed — the outcome is
    not determined before the measurement takes place. For this reason, the
    randomness produced here cannot be reduced to any underlying deterministic
    mechanism, which is why this "hello world" is a fitting first example of a
    quantum program.

## The diagrams

### The circuit

![Random-bit circuit](../assets/ch02-random-bits-circuit.png){ width="420" }

A circuit is read from left to right (see [the circuit model](../foundations.md#the-circuit-model)).
In the diagram above, the qubit `q` starts in `|0⟩`, an `H` gate places it into
superposition, and the measurement `M` writes the collapsed value into the
classical bit `c`. It follows that only the classical bit `c` carries a
definite value after execution; the qubit's role is to generate that value
through the measurement step.

### What you actually get

![Histogram of 10000 measured bits](../assets/ch02-random-bits-counts.png){ width="420" }

Measuring 10,000 times produces two bars of almost the same height. Slight
deviations from exactly 5,000/5,000 are expected and are not a sign of error —
they are the same statistical wobble that would be obtained from 10,000 fair
coin flips; moreover, such deviations are expected to shrink as the number of
shots grows.

### The state on the Bloch sphere

![Superposition on the Bloch sphere](../assets/ch02-random-bits-bloch.png){ width="420" }

The **Bloch sphere** is a geometric picture of a single qubit's state,
described by two angles `θ` and `φ` (see [the Bloch sphere](../foundations.md#the-bloch-sphere)).
Its north pole represents `|0⟩` and its south pole represents `|1⟩`. The state
`H|0⟩` lands exactly on the equator, pointing along the **+X** axis — the
visual signature of an even 50/50 superposition. It follows that a state
sitting on the equator is what guarantees balanced measurements, since neither
hemisphere is favoured; the distance from the poles encodes how strongly the
outcome is biased toward `0` or `1`.

## Key takeaways

- A qubit can be in a superposition, not just `0` or `1`.
- `H` turns `|0⟩` into an even mix `(|0⟩ + |1⟩)/√2`.
- Measurement collapses the state; the **Born rule** gives the probabilities.
- The resulting bits are truly random, unlike pseudo-random software generators.
- On the Bloch sphere, an even superposition sits on the equator.

## The code behind this chapter

The book's sample relies on the high-level `Classic.randomBit()` call; the
Python port opens up that call into the explicit `H`-then-measure circuit so
that the underlying mechanism becomes visible rather than hidden inside a
library routine. The code lives in
[`src/quantum_computing_in_action/ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py).
It can be executed with `make ch02`.
