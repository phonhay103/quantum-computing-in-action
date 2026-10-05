# quantum-computing-in-action

Companion code for **[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)**
by Johan Vos (Manning, January 2022 · ISBN 9781617296321 · 264 pages).

Hands-on experiments in quantum computing with [Qiskit](https://www.ibm.com/quantum/qiskit).
The book teaches the concepts using the Java-based [Strange](https://github.com/gluonhq/strange)
simulator; this repository reimplements the same ideas in Python with Qiskit.

## About the book

A gentle introduction to quantum computing for working developers — no physics
degree or advanced math required. Topics covered:

- Core concepts of quantum computing
- Qubits and quantum gates
- Superposition, entanglement, and hybrid computing
- Quantum algorithms including Shor's, Deutsch–Jozsa, and Grover's search
- Quantum communication and quantum repeaters
- From hardware to high-level languages and simulators

See the full [table of contents](https://livebook.manning.com/book/quantum-computing-in-action/contents)
and the [author's page](https://www.manning.com/authors/johan-vos).

## Chapters

Python/Qiskit ports of the book's Java samples. Each chapter can be run with
`uv run python -m quantum_computing_in_action <chapter>` or the matching `make` target.

| Chapter | Topic | Module | Run |
|---------|-------|--------|-----|
| 1 | Factoring time complexity (classical vs. Shor) | `quantum_computing_in_action.ch01.time_complexity` | `make ch01` |
| 2 | "Hello World" — random bits | `quantum_computing_in_action.ch02.random_bits` | `make ch02` |
| 3 | Qubits and the Pauli-X gate | `quantum_computing_in_action.ch03.pauli_x` | `make ch03` |

Chapter 1 writes `build/time-complexity.png`; chapter 3 can render the circuit
with `quantum_computing_in_action.ch03.pauli_x.draw()`.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python 3.14 (installed automatically by uv)

## Setup

```bash
uv sync
```

## Usage

```bash
uv run python -c "import quantum_computing_in_action as q; print(q.__version__)"
```

## Development

```bash
make help      # list targets
make sync      # install dependencies
make lint      # ruff + ty
make format    # ruff formatter
make test      # pytest
make ch01      # run chapter 1
make ch02      # run chapter 2
make ch03      # run chapter 3
make clean     # remove caches/artifacts
```

## Layout

```
.
├── Makefile
├── pyproject.toml
├── src/quantum_computing_in_action/
│   ├── __main__.py
│   ├── ch01/time_complexity.py
│   ├── ch02/random_bits.py
│   └── ch03/pauli_x.py
└── tests/
```
