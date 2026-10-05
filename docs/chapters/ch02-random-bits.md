# Chapter 2 — Random bits

!!! abstract "In one sentence"
    Put a qubit into **superposition** with a Hadamard gate, then measure it, and
    you get `0` or `1` with equal probability — randomness that comes from
    physics, not from a hidden algorithm.

## Classical bits vs. qubits

A classical bit is always one of two values: `0` **or** `1`. A **qubit** can
additionally be in a *combination* of both. Written in the Dirac notation used
throughout the book:

- `|0⟩` — the state that always measures as `0`
- `|1⟩` — the state that always measures as `1`
- a **superposition**, e.g. `(|0⟩ + |1⟩) / √2` — an even mixture of the two

The symbols `|…⟩` are just a labelling convention; the physics is in the
coefficients.

## The Hadamard gate

The **Hadamard gate** (`H`) is the standard way to create an even superposition:

$$H\,|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

If the qubit starts in `|0⟩`, a single `H` puts it into a state that is exactly
half `|0⟩` and half `|1⟩`. The `1/√2` factors are what make the probabilities
add up to 1 (see the Born rule below).

## Measurement and the Born rule

You never *see* a superposition directly. The moment you **measure** the qubit,
it collapses to one of the basis states, and the probability of each outcome is
the square of that state's coefficient — the **Born rule**:

$$P(0) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}, \qquad
  P(1) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}$$

Run the experiment once and you get a single bit. Run it thousands of times and
the two outcomes appear in nearly equal numbers.

!!! info "Why this is *genuinely* random"
    A classical `random()` function is usually **pseudo-random**: it looks
    random but is fully determined by a hidden seed, and can be reproduced.
    A measured qubit has no hidden value waiting to be revealed — the outcome is
    not determined before the measurement. That is why this "hello world" is a
    fitting first example of a quantum program.

## The diagrams

### The circuit

![Random-bit circuit](../assets/ch02-random-bits-circuit.png){ width="420" }

Reading left to right: the qubit `q` starts in `|0⟩`, an `H` gate puts it into
superposition, and the measurement `M` writes the collapsed value into the
classical bit `c`.

### What you actually get

![Histogram of 10000 measured bits](../assets/ch02-random-bits-counts.png){ width="420" }

Measuring 10,000 times produces two bars of almost the same height. Slight
deviations from exactly 5,000/5,000 are expected — they are the same statistical
wobble you would get from 10,000 fair coin flips.

### The state on the Bloch sphere

![Superposition on the Bloch sphere](../assets/ch02-random-bits-bloch.png){ width="420" }

The **Bloch sphere** is a geometric picture of a single qubit's state. Its north
pole is `|0⟩` and its south pole is `|1⟩`. `H|0⟩` lands exactly on the equator,
pointing along the **+X** axis — the visual signature of an even 50/50
superposition. A state sitting on the equator is what guarantees balanced
measurements.

## Key takeaways

- A qubit can be in a superposition, not just `0` or `1`.
- `H` turns `|0⟩` into an even mix `(|0⟩ + |1⟩)/√2`.
- Measurement collapses the state; the **Born rule** gives the probabilities.
- The resulting bits are truly random, unlike pseudo-random software generators.
- On the Bloch sphere, an even superposition sits on the equator.

## The code behind this chapter

The sample that draws the circuit, the histogram, and the Bloch sphere lives in
[`src/quantum_computing_in_action/ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py).
Run it with `make ch02`.
