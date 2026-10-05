# Reference

A quick map from each chapter to its source module, CLI command, and diagrams.
The module links point to the code; for the *concepts*, follow the chapter links.

## Chapters at a glance

| Chapter | Topic | Source module | Command |
|---------|-------|---------------|---------|
| [1](chapters/ch01-time-complexity.md) | Factoring time complexity | [`ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py) | `make ch01` |
| [2](chapters/ch02-random-bits.md) | Random bits from superposition | [`ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py) | `make ch02` |
| [3](chapters/ch03-pauli-x.md) | The Pauli-X gate | [`ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py) | `make ch03` |
| [4](chapters/ch04-hadamard.md) | The Hadamard gate | [`ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py) | `make ch04` |

The CLI takes the chapter id:

```bash
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03
```

## Diagram files

All diagrams are written to `build/` and prefixed with the chapter so a figure
always shows where it came from.

| Diagram | Chapter | Shows |
|---------|---------|-------|
| `ch01-time-complexity.png` | 1 | Classical vs. Shor factoring-time curves |
| `ch02-random-bits-circuit.png` | 2 | Circuit: `H` then measurement |
| `ch02-random-bits-counts.png` | 2 | Histogram of 10,000 measured bits |
| `ch02-random-bits-bloch.png` | 2 | Superposition on the Bloch sphere |
| `ch03-pauli-x.png` | 3 | Circuit: `X` then measurement |
| `ch03-pauli-x-bloch.png` | 3 | Qubit before and after the flip |
| `ch04-hadamard-circuit.png` | 4 | Circuit: one `H` then measurement |
| `ch04-hadamard2-circuit.png` | 4 | Circuit: `H`, `H`, then measurement |
| `ch04-hadamard-bloch.png` | 4 | `\|0⟩` → after `H` → after `H·H` |
| `ch04-hadamard-counts.png` | 4 | Histogram of 1000 runs of `H` |
| `ch04-hadamard2-counts.png` | 4 | Histogram of 1000 runs of `H·H` (all `0`) |

## Notation used in these notes

| Symbol | Meaning |
|--------|---------|
| `\|0⟩`, `\|1⟩` | The two basis states of a qubit |
| `(a\|0⟩ + b\|1⟩)` | A superposition with amplitudes `a` and `b` |
| `H` | Hadamard gate — creates an even superposition |
| `X` | Pauli-X gate — flips `\|0⟩ ↔ \|1⟩` |
| `P(0)`, `P(1)` | Measurement probabilities (Born rule: amplitude squared) |
| Bloch sphere | Geometric picture of a single qubit's state |
