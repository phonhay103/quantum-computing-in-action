# Getting started

This page is only about **running the samples** and **regenerating the
diagrams**. For the quantum-computing concepts, start at
[Chapter 1](chapters/ch01-time-complexity.md).

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

# or via make
make ch01
make ch02
make ch03
```

| Chapter | Command | Diagrams written to `build/` |
|---------|---------|------------------------------|
| 1 | `make ch01` | `ch01-time-complexity.png` |
| 2 | `make ch02` | `ch02-random-bits-circuit.png`, `ch02-random-bits-counts.png`, `ch02-random-bits-bloch.png` |
| 3 | `make ch03` | `ch03-pauli-x.png`, `ch03-pauli-x-bloch.png` |

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
│   ├── _diagrams.py             # reusable circuit / counts / Bloch renderers
│   ├── ch01/time_complexity.py
│   ├── ch02/random_bits.py
│   └── ch03/pauli_x.py
└── tests/
```

## Documentation languages

These notes are available in **English** (default) and **Tiếng Việt**. Use the
language selector in the top bar; the Vietnamese pages live under `/vi/`.
