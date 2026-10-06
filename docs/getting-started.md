# Getting started

This page is only about **running the samples** and **regenerating the
diagrams**. For the quantum-computing concepts, start at
[Chapter 1](chapters/ch01-evolution-revolution-hype.md).

## Requirements

- [uv](https://docs.astral.sh/uv/) — manages Python and dependencies
- Python 3.14 (uv installs it automatically)

The samples rely on [Qiskit](https://www.ibm.com/quantum/qiskit) for the
circuits, [matplotlib](https://matplotlib.org/) for the figures, and
[Rich](https://github.com/Textualize/rich) for the console output.

## Setup

```bash
uv sync
```

## Run a chapter

Each chapter prints a short explanation, a step-by-step breakdown, the numeric
results, and the paths of the diagrams it saved.

```bash
# via the module
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03
uv run python -m quantum_computing_in_action ch04
uv run python -m quantum_computing_in_action ch05
uv run python -m quantum_computing_in_action ch06

# or via make
make ch01
make ch02
make ch03
make ch04
make ch05
make ch06
```

| Chapter | Command | Diagrams written to `build/` |
|---------|---------|------------------------------|
| 1 | `make ch01` | `ch01-time-complexity.png`, `ch01-time-complexity-classical.png` |
| 2 | `make ch02` | `ch02-random-bits-circuit.png`, `ch02-random-bits-counts.png`, `ch02-random-bits-bloch.png` |
| 3 | `make ch03` | `ch03-pauli-x.png`, `ch03-pauli-x2-circuit.png`, `ch03-pauli-x-bloch.png`, `ch03-pauli-x-counts.png`, `ch03-pauli-x2-counts.png` |
| 4 | `make ch04` | `ch04-hadamard-circuit.png`, `ch04-hadamard2-circuit.png`, `ch04-hadamard-bloch.png`, `ch04-hadamard-counts.png`, `ch04-hadamard2-counts.png`, `ch04-gate-matrices.png` |
| 5 | `make ch05` | `ch05-bell-circuit.png`, `ch05-cnot-circuit.png`, `ch05-bell-counts.png`, `ch05-independent-counts.png`, `ch05-bell-vs-independent.png`, `ch05-amplitude-matrices.png` |
| 6 | `make ch06` | `ch06-clone-attempt-circuit.png`, `ch06-clone-fidelity.png`, `ch06-clone-agreement.png`, `ch06-cz-circuit.png`, `ch06-cz-vs-bell.png`, `ch06-cz-matrices.png`, `ch06-teleport-circuit.png`, `ch06-teleport-outcomes.png`, `ch06-teleport-fidelity.png`, `ch06-repeater-circuit.png`, `ch06-repeater-consistency.png`, `ch06-repeater-counts.png` |

Chapter 6 has four samples and runs all of them; to run just one of them, invoke
it directly:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
```

## Development

```bash
make sync      # install dependencies
make lint      # ruff + ty
make format    # ruff formatter
make test      # pytest
make docs      # build this documentation site into site/
make docs-serve # live-preview the docs at http://127.0.0.1:8000
make clean     # remove caches and generated artifacts
```

## Project layout

```
.
├── Makefile
├── pyproject.toml
├── mkdocs.yml
├── build/                       # generated diagrams (committed)
├── docs/                        # this documentation site
│   └── assets/                  # diagrams copied here at docs build time
├── src/quantum_computing_in_action/
│   ├── __main__.py              # CLI: python -m quantum_computing_in_action <chapter>
│   ├── _console.py              # shared dark console theme
│   ├── _diagrams.py             # reusable circuit / counts / Bloch / matrix renderers
│   ├── ch01/time_complexity.py
│   ├── ch02/random_bits.py
│   ├── ch03/pauli_x.py
│   ├── ch04/                    # hadamard.py + matrices.py
│   ├── ch05/                    # entanglement.py + states.py
│   └── ch06/                    # networking, czmeasure, teleportation, repeater, protocol
└── tests/
```

## Documentation languages

These notes are available in **English** (default) and **Tiếng Việt**. Use the
language selector in the top bar; the Vietnamese pages live under `/vi/`.
