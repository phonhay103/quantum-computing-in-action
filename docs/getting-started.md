# Getting started

This page is concerned solely with **running the samples** and
**regenerating the diagrams**. The quantum-computing concepts themselves
are introduced step by step in the chapters; to study them, begin at
[Chapter 1](chapters/ch01-evolution-revolution-hype.md), which lays the
foundations on which the later chapters build.

## Requirements

- [uv](https://docs.astral.sh/uv/) — manages both the Python interpreter
  and the project's dependencies, and is consequently the only tool that
  must be available beforehand
- Python 3.14 (uv installs it automatically, so no separate installation
  step is required)

The samples rely on [Qiskit](https://www.ibm.com/quantum/qiskit) to
construct and simulate the quantum circuits, on
[matplotlib](https://matplotlib.org/) to render the figures they
produce, and on [Rich](https://github.com/Textualize/rich) to format the
output printed to the console.

## Setup

A single command prepares the environment:

```bash
uv sync
```

Specifically, this command creates an isolated environment, installs
Python 3.14 when it is not already present, and downloads every
dependency declared by the project.

## Run a chapter

Each chapter corresponds to a self-contained sample program. When such a
program is executed, it prints a short explanation of the concept being
demonstrated, a step-by-step breakdown of the circuit construction, the
numeric results of the simulation, and the paths of the diagram files it
has written. The program can be invoked either through the module
interface or through the matching Makefile target:

```bash
# via the module
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03
uv run python -m quantum_computing_in_action ch04
uv run python -m quantum_computing_in_action ch05
uv run python -m quantum_computing_in_action ch06
uv run python -m quantum_computing_in_action ch07
uv run python -m quantum_computing_in_action ch08
uv run python -m quantum_computing_in_action ch09
uv run python -m quantum_computing_in_action ch10
uv run python -m quantum_computing_in_action ch11

# or via make
make ch01
make ch02
make ch03
make ch04
make ch05
make ch06
make ch07
make ch08
make ch09
make ch10
make ch11
```

| Chapter | Command | Diagrams written to `build/` |
|---------|---------|------------------------------|
| 1 | `make ch01` | `ch01-time-complexity.png`, `ch01-time-complexity-classical.png` |
| 2 | `make ch02` | `ch02-random-bits-circuit.png`, `ch02-random-bits-counts.png`, `ch02-random-bits-bloch.png` |
| 3 | `make ch03` | `ch03-pauli-x.png`, `ch03-pauli-x2-circuit.png`, `ch03-pauli-x-bloch.png`, `ch03-pauli-x-counts.png`, `ch03-pauli-x2-counts.png` |
| 4 | `make ch04` | `ch04-hadamard-circuit.png`, `ch04-hadamard2-circuit.png`, `ch04-hadamard-bloch.png`, `ch04-hadamard-counts.png`, `ch04-hadamard2-counts.png`, `ch04-gate-matrices.png` |
| 5 | `make ch05` | `ch05-bell-circuit.png`, `ch05-cnot-circuit.png`, `ch05-bell-counts.png`, `ch05-independent-counts.png`, `ch05-bell-vs-independent.png`, `ch05-amplitude-matrices.png` |
| 6 | `make ch06` | `ch06-clone-attempt-circuit.png`, `ch06-clone-fidelity.png`, `ch06-clone-agreement.png`, `ch06-cz-circuit.png`, `ch06-cz-vs-bell.png`, `ch06-cz-matrices.png`, `ch06-teleport-circuit.png`, `ch06-teleport-outcomes.png`, `ch06-teleport-fidelity.png`, `ch06-repeater-circuit.png`, `ch06-repeater-consistency.png`, `ch06-repeater-counts.png` |
| 7 | `make ch07` | `ch07-randombit-circuit.png`, `ch07-randombit-counts.png`, `ch07-randombit-qubits.png`, `ch07-debug-circuit.png`, `ch07-debug-steps.png`, `ch07-debug-marginals.png`, `ch07-add1-circuit.png`, `ch07-add2-circuit.png`, `ch07-toffoli-matrices.png`, `ch07-adder-comparison.png` |
| 8 | `make ch08` | `ch08-haha-circuit.png`, `ch08-haha-bloch.png`, `ch08-attempts-error.png`, `ch08-superposition-circuit.png`, `ch08-superposition-states.png`, `ch08-bb84-circuit.png`, `ch08-eavesdropper-error.png` |
| 9 | `make ch09` | `ch09-reversible-circuit.png`, `ch09-oracle-matrices.png`, `ch09-oracle-circuit.png`, `ch09-deutsch-circuit.png`, `ch09-deutsch-outcomes.png`, `ch09-dj-circuit.png`, `ch09-dj-outcomes.png` |
| 10 | `make ch10` | `ch10-classical-tries.png`, `ch10-oracle-matrix.png`, `ch10-step-by-step.png`, `ch10-grover-circuit.png`, `ch10-grover-curve.png`, `ch10-grover-outcomes.png` |
| 11 | `make ch11` | `ch11-classical-factor.png`, `ch11-period-function.png`, `ch11-qft-circuit.png`, `ch11-qft-phase.png`, `ch11-order-circuit.png`, `ch11-order-peaks.png` |

Chapters 6 through 11 each consist of several samples, and running the
chapter executes all of them in sequence; consequently, a single sample
can be examined in isolation by invoking its module directly:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
uv run python -m quantum_computing_in_action.ch07.full_adder
uv run python -m quantum_computing_in_action.ch08.bb84
uv run python -m quantum_computing_in_action.ch09.deutschjozsa
uv run python -m quantum_computing_in_action.ch10.grover
uv run python -m quantum_computing_in_action.ch11.shor
```

## Development

The Makefile exposes the routine development tasks; each target wraps a
single tool so that the task is performed consistently:

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

The repository follows a conventional Python project structure; the tree
below maps each directory and file to the role it plays:

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
│   ├── ch06/                    # networking, czmeasure, teleportation, repeater, protocol
│   ├── ch07/                    # randombit, debugging, half_adder, full_adder, circuits
│   ├── ch08/                    # protocol, identity, attempts, superposition, bb84
│   ├── ch09/                    # reversible, oracles, deutsch, deutschjozsa
│   ├── ch10/                    # search, oracle, step_by_step, grover
│   └── ch11/                    # classical, qft, shor
└── tests/
```

## Documentation languages

These notes are maintained in **English** (the default) and
**Tiếng Việt**. The language selector in the top bar switches between
them; the Vietnamese pages are served under the `/vi/` path, and each
page in one language corresponds to exactly one page in the other.
