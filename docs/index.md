# Quantum Computing in Action — companion notes

This site explains the **ideas** behind the book
[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)
by Johan Vos, for the chapters ported to Python with
[Qiskit](https://www.ibm.com/quantum/qiskit).

The book teaches quantum computing with the Java-based
[Strange](https://github.com/gluonhq/strange) simulator. This repository keeps the
same narrative but uses Qiskit, and renders the result of each sample as a
diagram so you can *see* what the maths describes. It draws on only two public
sources: the book's **source code** and its
[Manning page](https://www.manning.com/books/quantum-computing-in-action), which
includes the table of contents.

!!! note "What these notes are — and are not"
    These pages cover the **quantum-computing knowledge** of each chapter:
    what a qubit is, what a gate does, what a measurement returns, and why it
    matters. They deliberately do **not** walk through the source code. Each
    page links to the matching module if you want to read the implementation.

## The chapters covered

Chapter titles follow the book's table of contents.

| Chapter | Status | Idea in one line | Diagrams |
|---------|--------|------------------|----------|
| [1 — Evolution, revolution, or hype?](chapters/ch01-evolution-revolution-hype.md) | done | Quantum computing is an evolution with a revolutionary speed-up for a narrow set of problems, such as factoring | [classical vs. Shor, classical alone](chapters/ch01-evolution-revolution-hype.md#the-diagrams) |
| [2 — Hello World, quantum computing style](chapters/ch02-hello-world.md) | done | A qubit in superposition returns genuinely random `0`/`1` on measurement | [circuit, counts, Bloch](chapters/ch02-hello-world.md#the-diagrams) |
| [3 — Qubits and quantum gates](chapters/ch03-qubits-and-gates.md) | done | Qubits are the basic unit and gates are reversible operations; `X` flips <code>\|0⟩</code> to <code>\|1⟩</code> deterministically | [circuits, Bloch, counts](chapters/ch03-qubits-and-gates.md#the-diagrams) |
| [4 — Superposition](chapters/ch04-superposition.md) | done | A state is a vector and a gate is a matrix; `H` creates an even superposition and `H·H` cancels it | [circuits, Bloch, counts, matrices](chapters/ch04-superposition.md#the-diagrams) |
| [5 — Entanglement](chapters/ch05-entanglement.md) | done | Two qubits can share a joint state that cannot be described one qubit at a time | [circuits, counts, comparison, matrices](chapters/ch05-entanglement.md#the-diagrams) |
| [6 — Quantum networking: The basics](chapters/ch06-quantum-networking.md) | planned | Moving quantum information between nodes: teleportation, no-cloning, and repeaters | — |
| [7 — Our HelloWorld, explained](chapters/ch07-helloworld-explained.md) | planned | Rebuild the random-bit circuit gate by gate to see how it really works | — |
| [8 — Secure communication using quantum computing](chapters/ch08-secure-communication.md) | planned | Quantum key distribution (BB84) makes eavesdropping detectable | — |
| [9 — Deutsch–Jozsa algorithm](chapters/ch09-deutsch-jozsa.md) | planned | Decide whether a function is constant or balanced in a single query | — |
| [10 — Grover's search algorithm](chapters/ch10-grovers-search.md) | planned | A quadratic speed-up for unstructured search | — |
| [11 — Shor's algorithm](chapters/ch11-shors-algorithm.md) | planned | Polynomial-time factoring via order finding and the quantum Fourier transform | — |

## Diagram gallery

Every sample writes its figures to `build/`, prefixed with the chapter number so
a figure always tells you where it came from.

### Chapter 1 — classical vs. Shor

![Classical vs. Shor factoring time](assets/ch01-time-complexity.png){ width="460" }
![The classical curve on its own](assets/ch01-time-complexity-classical.png){ width="460" }

### Chapter 2 — random bits

![Random-bit circuit](assets/ch02-random-bits-circuit.png){ width="360" }
![Measurement counts](assets/ch02-random-bits-counts.png){ width="360" }
![Superposition on the Bloch sphere](assets/ch02-random-bits-bloch.png){ width="360" }

### Chapter 3 — qubits and gates

![Pauli-X circuit](assets/ch03-pauli-x.png){ width="360" }
![Two Pauli-X gates](assets/ch03-pauli-x2-circuit.png){ width="360" }
![Qubit before, after X, and after X·X](assets/ch03-pauli-x-bloch.png){ width="620" }

### Chapter 4 — superposition

![Single Hadamard circuit](assets/ch04-hadamard-circuit.png){ width="360" }
![Two Hadamard gates](assets/ch04-hadamard2-circuit.png){ width="360" }
![Superposition created and cancelled on the Bloch sphere](assets/ch04-hadamard-bloch.png){ width="560" }
![X, H, and H·H as matrices](assets/ch04-gate-matrices.png){ width="560" }

### Chapter 5 — entanglement

![Bell-state circuit](assets/ch05-bell-circuit.png){ width="360" }
![CNOT circuit](assets/ch05-cnot-circuit.png){ width="360" }
![Independent vs. entangled qubits](assets/ch05-bell-vs-independent.png){ width="560" }
![Coefficient matrices](assets/ch05-amplitude-matrices.png){ width="560" }

## Where to go next

- New here? Start with **[Getting started](getting-started.md)** to run the
  samples and regenerate the diagrams.
- New to the background ideas (bits, amplitudes, phases, the Bloch sphere)?
  Skim the **[Foundations](foundations.md)** page.
- Want the concepts only? Jump straight to
  **[Chapter 1](chapters/ch01-evolution-revolution-hype.md)**.
- Looking for the code that produces a figure? See the
  **[Reference](reference.md)** table, which maps each chapter to its module,
  CLI command, and diagrams.
