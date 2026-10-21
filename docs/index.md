# Quantum Computing in Action — companion notes

This site presents a systematic account of the **ideas** behind the book
[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)
by Johan Vos, prepared for the chapters that have been ported to Python with
[Qiskit](https://www.ibm.com/quantum/qiskit). Its purpose is not to replace the
book itself but to accompany it: each page sets out the concepts a chapter
introduces and demonstrates how those concepts behave within an executable
simulation.

The book teaches quantum computing with the Java-based
[Strange](https://github.com/gluonhq/strange) simulator. This repository
preserves the same narrative while substituting Qiskit as the simulation engine,
and it renders the result of each sample as a diagram so that what the maths
describes can be inspected visually as well as symbolically. It is worth noting
that the material draws on exactly two public sources: the book's **source
code** and its
[Manning page](https://www.manning.com/books/quantum-computing-in-action), the
latter of which also includes the table of contents on which the chapter titles
below are based.

!!! note "What these notes are — and are not"
    These pages cover the **quantum-computing knowledge** developed in each
    chapter: what a qubit is, what a gate does, what a measurement returns, and
    why each of these matters for the argument of the book as a whole. They
    deliberately do **not** walk through the source code; the implementation is
    treated as a separate concern. Each page nevertheless links to the matching
    module, so that the implementation can be consulted whenever reading it is
    of interest.

## The chapters covered

Chapter titles follow the book's table of contents, so that the position of a
chapter in these notes corresponds exactly to its position in the book. Each
row of the table condenses the central idea of a chapter into a single sentence
and lists the diagrams that were generated for it.

| Chapter | Status | Idea in one line | Diagrams |
|---------|--------|------------------|----------|
| [1 — Evolution, revolution, or hype?](chapters/ch01-evolution-revolution-hype.md) | done | Quantum computing is an evolution with a revolutionary speed-up for a narrow set of problems, such as factoring | [classical vs. Shor, classical alone](chapters/ch01-evolution-revolution-hype.md#the-diagrams) |
| [2 — Hello World, quantum computing style](chapters/ch02-hello-world.md) | done | A qubit in superposition returns genuinely random `0`/`1` on measurement | [circuit, counts, Bloch](chapters/ch02-hello-world.md#the-diagrams) |
| [3 — Qubits and quantum gates](chapters/ch03-qubits-and-gates.md) | done | Qubits are the basic unit and gates are reversible operations; `X` flips <code>\|0⟩</code> to <code>\|1⟩</code> deterministically | [circuits, Bloch, counts](chapters/ch03-qubits-and-gates.md#the-diagrams) |
| [4 — Superposition](chapters/ch04-superposition.md) | done | A state is a vector and a gate is a matrix; `H` creates an even superposition and `H·H` cancels it | [circuits, Bloch, counts, matrices](chapters/ch04-superposition.md#the-diagrams) |
| [5 — Entanglement](chapters/ch05-entanglement.md) | done | Two qubits can share a joint state that cannot be described one qubit at a time | [circuits, counts, comparison, matrices](chapters/ch05-entanglement.md#the-diagrams) |
| [6 — Quantum networking: The basics](chapters/ch06-quantum-networking.md) | done | A qubit cannot be copied, so it has to be *moved*: teleportation rebuilds a state from shared entanglement plus two classical bits, and repeaters chain the links | [no-cloning, CZ, teleport, repeater](chapters/ch06-quantum-networking.md#the-diagrams) |
| [7 — Our HelloWorld, explained](chapters/ch07-helloworld-explained.md) | done | A circuit is an ordered list of steps, and the state can be read after every one — the same idea makes a reversible adder from `CNOT` and `Toffoli` | [circuit, step-by-step, adders, Toffoli](chapters/ch07-helloworld-explained.md#the-diagrams) |
| [8 — Secure communication using quantum computing](chapters/ch08-secure-communication.md) | done | A qubit only carries a bit in a chosen **base**, so Alice and Bob can sift matching bases into a secret key — and an eavesdropper's measurement leaves a ~25% error rate | [round trip, attempts, superposition, BB84, wiretap](chapters/ch08-secure-communication.md#the-diagrams) |
| [9 — Deutsch–Jozsa algorithm](chapters/ch09-deutsch-jozsa.md) | done | One quantum query decides whether a promised function is constant or balanced, where a classical check may need `2^(n-1) + 1` | [reversibility, oracles, Deutsch, DJ](chapters/ch09-deutsch-jozsa.md#the-diagrams) |
| [10 — Grover's search algorithm](chapters/ch10-grovers-search.md) | done | An oracle flips one sign; diffusion reflects about the mean; `(π/4)√N` rounds find the item — a quadratic speed-up | [classical, oracle, step by step, 64 items](chapters/ch10-grovers-search.md#the-diagrams) |
| [11 — Shor's algorithm](chapters/ch11-shors-algorithm.md) | done | Factoring reduces to order finding, and the quantum Fourier transform reads the period off a few peaks — polynomial time | [classical, QFT, order finding](chapters/ch11-shors-algorithm.md#the-diagrams) |

## Diagram gallery

Every sample writes its figures to `build/`, prefixed with the chapter number
from which the figure originates; it follows that a figure always reveals its
own provenance without any further labelling. The figures are collected below
in chapter order, so the gallery can also be read as a compressed visual
summary of the book as a whole.

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

### Chapter 6 — quantum networking

![The failed clone attempt](assets/ch06-clone-attempt-circuit.png){ width="360" }
![A perfect clone vs. the CNOT attempt](assets/ch06-clone-agreement.png){ width="560" }
![Teleportation circuit](assets/ch06-teleport-circuit.png){ width="620" }
![Two chained links across a relay](assets/ch06-repeater-circuit.png){ width="620" }

### Chapter 7 — our HelloWorld, explained

![The four-qubit program](assets/ch07-randombit-circuit.png){ width="360" }
![Basis-state probabilities after each step](assets/ch07-debug-steps.png){ width="560" }
![The half-adder for 1 + 1](assets/ch07-add1-circuit.png){ width="360" }
![The full adder for 1 + 1](assets/ch07-add2-circuit.png){ width="420" }
![From X to CNOT to Toffoli](assets/ch07-toffoli-matrices.png){ width="560" }
![Half-adder vs. full adder](assets/ch07-adder-comparison.png){ width="560" }

### Chapter 8 — secure communication

![The Hadamard round trip](assets/ch08-haha-circuit.png){ width="360" }
![A clean line vs. a wiretap](assets/ch08-eavesdropper-error.png){ width="560" }
![A register in superposition, and the same register recovered](assets/ch08-superposition-states.png){ width="560" }
![One BB84 circuit](assets/ch08-bb84-circuit.png){ width="620" }

### Chapter 9 — Deutsch–Jozsa

![The four oracle matrices](assets/ch09-oracle-matrices.png){ width="560" }
![The Deutsch circuit](assets/ch09-deutsch-circuit.png){ width="360" }
![One query: constant measures 0, balanced measures 1](assets/ch09-deutsch-outcomes.png){ width="560" }
![Deutsch–Jozsa for n = 3](assets/ch09-dj-circuit.png){ width="620" }

### Chapter 10 — Grover's search

![Grover's oracle](assets/ch10-oracle-matrix.png){ width="360" }
![Grover on 2 qubits](assets/ch10-step-by-step.png){ width="560" }
![Grover on 64 items: probability rises, then overshoots](assets/ch10-grover-curve.png){ width="560" }

### Chapter 11 — Shor's algorithm

![Classical trial division](assets/ch11-classical-factor.png){ width="560" }
![QFT|1>: a linear phase ramp](assets/ch11-qft-phase.png){ width="560" }
![A compact order-finding circuit](assets/ch11-order-circuit.png){ width="620" }
![Inverse QFT of the periodic register: four peaks](assets/ch11-order-peaks.png){ width="560" }

## Where to go next

- Someone starting here for the first time may begin with the
  **[Getting started](getting-started.md)** page, which explains how to run the
  samples and regenerate the diagrams from them.
- For readers who are new to the background ideas (bits, amplitudes, phases,
  the Bloch sphere), the **[Foundations](foundations.md)** page supplies the
  necessary groundwork in condensed form.
- When an unfamiliar term such as *fidelity*, *Schmidt rank*, or
  *sub-exponential* occurs, its definition can be looked up in the
  **[Glossary](glossary.md)**.
- Anyone interested in the concepts alone may proceed directly to
  **[Chapter 1](chapters/ch01-evolution-revolution-hype.md)**.
- To locate the code that produces a given figure, the
  **[Reference](reference.md)** table maps each chapter to its module, CLI
  command, and diagrams.
