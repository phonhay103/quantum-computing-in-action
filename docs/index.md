# Quantum Computing in Action — companion notes

This site explains the **ideas** behind the book
[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)
by Johan Vos, for the chapters ported to Python with
[Qiskit](https://www.ibm.com/quantum/qiskit).

The book teaches quantum computing with the Java-based
[Strange](https://github.com/gluonhq/strange) simulator. This repository keeps the
same narrative but uses Qiskit, and renders the result of each sample as a
diagram so you can *see* what the maths describes.

!!! note "What these notes are — and are not"
    These pages cover the **quantum-computing knowledge** of each chapter:
    what a qubit is, what a gate does, what a measurement returns, and why it
    matters. They deliberately do **not** walk through the source code. Each
    page links to the matching module if you want to read the implementation.

## The chapters covered

| Chapter | Idea in one line | Diagrams |
|---------|------------------|----------|
| [1 — Factoring time complexity](chapters/ch01-time-complexity.md) | Quantum computers promise a speed-up because Shor's algorithm is polynomial while the best classical method is exponential | [classical vs. Shor](chapters/ch01-time-complexity.md#the-diagram) |
| [2 — Random bits](chapters/ch02-random-bits.md) | A qubit in superposition returns genuinely random `0`/`1` on measurement | [circuit, counts, Bloch](chapters/ch02-random-bits.md#the-diagrams) |
| [3 — The Pauli-X gate](chapters/ch03-pauli-x.md) | A single-qubit gate flips `\|0⟩` to `\|1⟩` deterministically | [circuit, Bloch](chapters/ch03-pauli-x.md#the-diagrams) |
| [4 — The Hadamard gate](chapters/ch04-hadamard.md) | `H` creates an even superposition, and `H` twice cancels it back to `\|0⟩` | [circuits, Bloch, counts](chapters/ch04-hadamard.md#the-diagrams) |

## Diagram gallery

Every sample writes its figures to `build/`, prefixed with the chapter number so
a figure always tells you where it came from.

### Chapter 1 — classical vs. Shor

![Classical vs. Shor factoring time](assets/ch01-time-complexity.png){ width="520" }

### Chapter 2 — random bits

![Random-bit circuit](assets/ch02-random-bits-circuit.png){ width="360" }
![Measurement counts](assets/ch02-random-bits-counts.png){ width="360" }
![Superposition on the Bloch sphere](assets/ch02-random-bits-bloch.png){ width="360" }

### Chapter 3 — the Pauli-X gate

![Pauli-X circuit](assets/ch03-pauli-x.png){ width="360" }
![Qubit before and after X](assets/ch03-pauli-x-bloch.png){ width="520" }

### Chapter 4 — the Hadamard gate

![Single Hadamard circuit](assets/ch04-hadamard-circuit.png){ width="360" }
![Two Hadamard gates](assets/ch04-hadamard2-circuit.png){ width="360" }
![Superposition created and cancelled on the Bloch sphere](assets/ch04-hadamard-bloch.png){ width="560" }

## Where to go next

- New here? Start with **[Getting started](getting-started.md)** to run the
  samples and regenerate the diagrams.
- Want the concepts only? Jump straight to **[Chapter 1](chapters/ch01-time-complexity.md)**.
- Looking for the code that produces a figure? See the
  **[Reference](reference.md)** table, which maps each chapter to its module,
  CLI command, and diagrams.
