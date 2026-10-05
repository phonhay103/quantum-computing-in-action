# Reference

A quick map from each chapter to its source module, CLI command, and diagrams.
The module links point to the code; for the *concepts*, follow the chapter links.

## Chapters at a glance

| Chapter | Topic (book title) | Source module | Command |
|---------|--------------------|---------------|---------|
| [1](chapters/ch01-evolution-revolution-hype.md) | Evolution, revolution, or hype? | [`ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py) | `make ch01` |
| [2](chapters/ch02-hello-world.md) | Hello World, quantum computing style | [`ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py) | `make ch02` |
| [3](chapters/ch03-qubits-and-gates.md) | Qubits and quantum gates | [`ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py) | `make ch03` |
| [4](chapters/ch04-superposition.md) | Superposition | [`ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py), [`ch04/matrices.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/matrices.py) | `make ch04` |
| [5](chapters/ch05-entanglement.md) | Entanglement | — | planned |
| [6](chapters/ch06-quantum-networking.md) | Quantum networking: The basics | — | planned |
| [7](chapters/ch07-helloworld-explained.md) | Our HelloWorld, explained | — | planned |
| [8](chapters/ch08-secure-communication.md) | Secure communication using quantum computing | — | planned |
| [9](chapters/ch09-deutsch-jozsa.md) | Deutsch–Jozsa algorithm | — | planned |
| [10](chapters/ch10-grovers-search.md) | Grover's search algorithm | — | planned |
| [11](chapters/ch11-shors-algorithm.md) | Shor's algorithm | — | planned |

The CLI takes the chapter id:

```bash
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03
uv run python -m quantum_computing_in_action ch04
```

## Diagram files

All diagrams are written to `build/` and prefixed with the chapter so a figure
always shows where it came from.

| Diagram | Chapter | Shows |
|---------|---------|-------|
| `ch01-time-complexity.png` | 1 | Classical vs. Shor factoring-time curves |
| `ch01-time-complexity-classical.png` | 1 | The classical curve on its own |
| `ch02-random-bits-circuit.png` | 2 | Circuit: `H` then measurement |
| `ch02-random-bits-counts.png` | 2 | Histogram of 10,000 measured bits |
| `ch02-random-bits-bloch.png` | 2 | Superposition on the Bloch sphere |
| `ch03-pauli-x.png` | 3 | Circuit: `X` then measurement |
| `ch03-pauli-x2-circuit.png` | 3 | Circuit: `X`, `X`, then measurement |
| `ch03-pauli-x-bloch.png` | 3 | `\|0⟩` → after `X` → after `X·X` |
| `ch03-pauli-x-counts.png` | 3 | Histogram of 1000 runs of `X` (all `1`) |
| `ch03-pauli-x2-counts.png` | 3 | Histogram of 1000 runs of `X·X` (all `0`) |
| `ch04-hadamard-circuit.png` | 4 | Circuit: one `H` then measurement |
| `ch04-hadamard2-circuit.png` | 4 | Circuit: `H`, `H`, then measurement |
| `ch04-hadamard-bloch.png` | 4 | `\|0⟩` → after `H` → after `H·H` |
| `ch04-hadamard-counts.png` | 4 | Histogram of 1000 runs of `H` |
| `ch04-hadamard2-counts.png` | 4 | Histogram of 1000 runs of `H·H` (all `0`) |
| `ch04-gate-matrices.png` | 4 | The `X`, `H`, and `H·H` matrices as heatmaps |

## Notation used in these notes

| Symbol | Meaning |
|--------|---------|
| `\|0⟩`, `\|1⟩` | The two basis states of a qubit |
| `\|ψ⟩` | A general (arbitrary) single-qubit state |
| `\|+⟩`, `\|−⟩` | The two even superpositions `(\|0⟩ ± \|1⟩)/√2` |
| `(a\|0⟩ + b\|1⟩)` | A superposition with amplitudes `a` and `b` |
| `[α, β]` | The same state written as a column vector |
| `H` | Hadamard gate — creates an even superposition |
| `X` | Pauli-X gate — flips `\|0⟩ ↔ \|1⟩` |
| `I` | The identity operation — "do nothing" |
| `U` | A generic gate, written as a 2×2 matrix |
| `P(0)`, `P(1)` | Measurement probabilities (Born rule: amplitude squared) |
| Bloch sphere | Geometric picture of a single qubit's state |
