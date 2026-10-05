# quantum-computing-in-action

Companion code for **[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)**
by Johan Vos (Manning, January 2022 · ISBN 9781617296321 · 264 pages).

Hands-on experiments in quantum computing with [Qiskit](https://www.ibm.com/quantum/qiskit).
The book teaches the concepts using the Java-based [Strange](https://github.com/gluonhq/strange)
simulator; this repository reimplements the same ideas in Python with Qiskit.
Console output is formatted with [Rich](https://github.com/Textualize/rich).

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

Python/Qiskit ports of the book's Java samples. Each sample prints a short
explanation of the concept before showing results, and multi-step samples also
print a numbered, step-by-step breakdown (including the state after each
operation). Run a chapter with
`uv run python -m quantum_computing_in_action <chapter>` or the matching `make` target.

| Chapter | Topic | Module | Run |
|---------|-------|--------|-----|
| 1 | Factoring time complexity (classical vs. Shor) | `quantum_computing_in_action.ch01.time_complexity` | `make ch01` |
| 2 | "Hello World" — random bits | `quantum_computing_in_action.ch02.random_bits` | `make ch02` |
| 3 | Qubits and the Pauli-X gate | `quantum_computing_in_action.ch03.pauli_x` | `make ch03` |

Each sample also renders diagrams to `build/`:

| Chapter | Diagrams |
|---------|----------|
| 1 | `time-complexity.png` — classical vs. Shor curves |
| 2 | `random-bits-circuit.png`, `random-bits-counts.png`, `random-bits-bloch.png` |
| 3 | `pauli-x.png`, `pauli-x-bloch.png` (before/after the flip) |

## Dark mode

Output is designed for dark terminals. Console text uses a dark-friendly
[Rich](https://github.com/Textualize/rich) theme (defined in
`quantum_computing_in_action._console`), and every diagram is rendered on a dark
background (matplotlib's `dark_background` style and Qiskit's `iqp-dark` circuit
style), via the helpers in `quantum_computing_in_action._diagrams`.

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
│   ├── _console.py
│   ├── _diagrams.py
│   ├── ch01/time_complexity.py
│   ├── ch02/random_bits.py
│   └── ch03/pauli_x.py
└── tests/
```
