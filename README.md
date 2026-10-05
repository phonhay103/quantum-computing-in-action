# quantum-computing-in-action

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-2ea44f.svg)](https://phonhay103.github.io/quantum-computing-in-action/)

Companion code for **[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)**
by Johan Vos (Manning, January 2022 · ISBN 9781617296321 · 264 pages).

Hands-on experiments in quantum computing with [Qiskit](https://www.ibm.com/quantum/qiskit).
The book teaches the concepts using the Java-based [Strange](https://github.com/gluonhq/strange)
simulator; this repository reimplements the same ideas in Python with Qiskit.
Console output is formatted with [Rich](https://github.com/Textualize/rich).

**Scope.** This repository is built from only three public sources: the book's
**source code** (the Java samples ported to Python/Qiskit), its **table of contents**
(which the chapter list follows), and the information on the book's
[Manning page](https://www.manning.com/books/quantum-computing-in-action).

## 📖 Buy the book

This repository is **companion material — not a replacement for the book**. The full
explanations, exercises, and narrative live in the original work:

> **[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)**
> by **Johan Vos** — Manning, January 2022.
> ISBN 9781617296321 · 264 pages.
> Available from [Manning](https://www.manning.com/books/quantum-computing-in-action)
> and on [LiveBook](https://livebook.manning.com/book/quantum-computing-in-action/).

If these samples help you, **please buy a copy**. Purchasing the book is the best way
to support the author and the publisher, and it gives you the context that this code
only illustrates.

## About the book

A gentle, practical introduction to quantum computing for developers — no physics
degree or advanced math required. Using the Java-based Strange simulator, the book
walks from core concepts to real algorithms. Per its
[Manning page](https://www.manning.com/books/quantum-computing-in-action), it covers:

- An introduction to the core concepts of quantum computing
- Qubits and quantum gates
- Superposition, entanglement, and hybrid computing
- Quantum algorithms including Shor's, Deutsch–Jozsa, and Grover's search

### Resources

- [Table of contents](https://livebook.manning.com/book/quantum-computing-in-action/contents)
- [Source code](https://github.com/johanvos/quantumjava) — the Java samples this repository ports
- [Manning product page](https://www.manning.com/books/quantum-computing-in-action)
- [Author's page](https://www.manning.com/authors/johan-vos)

## Chapters

Python/Qiskit ports of the book's Java samples. Each sample prints a short
explanation of the concept before showing results, and multi-step samples also
print a numbered, step-by-step breakdown (including the state after each
operation). Run a chapter with
`uv run python -m quantum_computing_in_action <chapter>` or the matching `make` target.

| Chapter | Topic (book title) | Module | Run |
|---------|--------------------|--------|-----|
| 1 | Evolution, revolution, or hype? | `quantum_computing_in_action.ch01.time_complexity` | `make ch01` |
| 2 | Hello World, quantum computing style | `quantum_computing_in_action.ch02.random_bits` | `make ch02` |
| 3 | Qubits and quantum gates | `quantum_computing_in_action.ch03.pauli_x` | `make ch03` |
| 4 | Superposition | `quantum_computing_in_action.ch04.hadamard` (+ `ch04.matrices`) | `make ch04` |
| 5 | Entanglement | — | planned |
| 6 | Quantum networking: The basics | — | planned |
| 7 | Our HelloWorld, explained | — | planned |
| 8 | Secure communication using quantum computing | — | planned |
| 9 | Deutsch–Jozsa algorithm | — | planned |
| 10 | Grover's search algorithm | — | planned |
| 11 | Shor's algorithm | — | planned |

Each sample also renders diagrams to `build/`:

| Chapter | Diagrams |
|---------|----------|
| 1 | `ch01-time-complexity.png` (classical vs. Shor), `ch01-time-complexity-classical.png` |
| 2 | `ch02-random-bits-circuit.png`, `ch02-random-bits-counts.png`, `ch02-random-bits-bloch.png` |
| 3 | `ch03-pauli-x.png`, `ch03-pauli-x2-circuit.png`, `ch03-pauli-x-bloch.png`, `ch03-pauli-x-counts.png`, `ch03-pauli-x2-counts.png` |
| 4 | `ch04-hadamard-circuit.png`, `ch04-hadamard2-circuit.png`, `ch04-hadamard-bloch.png`, `ch04-hadamard-counts.png`, `ch04-hadamard2-counts.png`, `ch04-gate-matrices.png` |

## Documentation

Bilingual (English / Tiếng Việt) notes explaining the **quantum-computing
concepts** of each chapter, illustrated with the generated diagrams and linked to
the matching source modules, are published with MkDocs Material to GitHub Pages:

**<https://phonhay103.github.io/quantum-computing-in-action/>**

Build or preview them locally:

```bash
make docs        # build the site into site/
make docs-serve  # live preview at http://127.0.0.1:8000
```

The sources live in `docs/` (`*.md` for English, `*.vi.md` for Vietnamese) and the
site is configured in `mkdocs.yml`; deployment runs via
`.github/workflows/docs.yml`.

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
make ch04      # run chapter 4
make docs      # build the documentation site
make clean     # remove caches/artifacts
```

## Layout

```
.
├── Makefile
├── pyproject.toml
├── mkdocs.yml
├── build/                    # generated diagrams (committed)
├── docs/                     # MkDocs site sources (en + vi)
├── src/quantum_computing_in_action/
│   ├── __main__.py
│   ├── _console.py
│   ├── _diagrams.py
│   ├── ch01/time_complexity.py
│   ├── ch02/random_bits.py
│   ├── ch03/pauli_x.py
│   └── ch04/                 # hadamard.py + matrices.py
└── tests/
```

## Disclaimer

- **Unofficial and independent.** This project is **not affiliated with, authorized,
  endorsed by, or sponsored by** Johan Vos, Manning Publications, IBM, or the Qiskit
  and Strange projects. It is a personal, educational companion project.
- **Sources.** This repository is derived from only three public sources: the book's
  **source code** (the Java samples, published by the author), its **table of
  contents**, and the information on the book's
  [Manning page](https://www.manning.com/books/quantum-computing-in-action). The
  Python/Qiskit ports, explanations, diagrams, and prose here are original companion
  material.
- **Educational use only.** The code ports chapters 1–4 and outlines the remaining
  chapters in the docs. It covers a *subset* of the book's material and may contain
  mistakes or simplifications; always treat the book as the authoritative source.
- **No warranty.** The code and notes are provided **"AS IS"**, without warranty of any
  kind. You are responsible for how you use them; the maintainers accept no liability
  for any loss or damage arising from their use.
- **Trademarks.** "Qiskit" and "IBM" are trademarks of IBM; "Strange" belongs to its
  authors (Gluon); "Manning" is a trademark of Manning Publications. The title
  *Quantum Computing in Action* and all other marks belong to their respective owners
  and are used for identification only.

## Acknowledgements

This repository was **created by [OpenCode](https://opencode.ai) and
[DeepSeek V4.1 Flash](https://www.deepseek.com)**:

- **[OpenCode](https://opencode.ai)** — the open-source AI coding agent that
  generated the code, the bilingual documentation, and the diagrams.
- **[DeepSeek V4.1 Flash](https://www.deepseek.com)** — the model driving OpenCode.

## License

The original code, documentation, and diagrams in this repository are released under the
**Apache License 2.0** — see [LICENSE](LICENSE) for the full text.

```text
Copyright 2026 the quantum-computing-in-action contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

> **Note:** the license applies **only** to the material created in this repository.

