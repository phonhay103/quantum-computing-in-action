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
| [5](chapters/ch05-entanglement.md) | Entanglement | [`ch05/entanglement.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/entanglement.py), [`ch05/states.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/states.py) | `make ch05` |
| [6](chapters/ch06-quantum-networking.md) | Quantum networking: The basics | [`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py), [`ch06/czmeasure.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/czmeasure.py), [`ch06/teleportation.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/teleportation.py), [`ch06/repeater.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/repeater.py), [`ch06/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/protocol.py) | `make ch06` |
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
uv run python -m quantum_computing_in_action ch05
uv run python -m quantum_computing_in_action ch06
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
| `ch03-pauli-x-bloch.png` | 3 | <code>\|0⟩</code> → after `X` → after `X·X` |
| `ch03-pauli-x-counts.png` | 3 | Histogram of 1000 runs of `X` (all `1`) |
| `ch03-pauli-x2-counts.png` | 3 | Histogram of 1000 runs of `X·X` (all `0`) |
| `ch04-hadamard-circuit.png` | 4 | Circuit: one `H` then measurement |
| `ch04-hadamard2-circuit.png` | 4 | Circuit: `H`, `H`, then measurement |
| `ch04-hadamard-bloch.png` | 4 | <code>\|0⟩</code> → after `H` → after `H·H` |
| `ch04-hadamard-counts.png` | 4 | Histogram of 1000 runs of `H` |
| `ch04-hadamard2-counts.png` | 4 | Histogram of 1000 runs of `H·H` (all `0`) |
| `ch04-gate-matrices.png` | 4 | The `X`, `H`, and `H·H` matrices as heatmaps |
| `ch05-bell-circuit.png` | 5 | Circuit: `H`, `CNOT`, then measurement of both qubits |
| `ch05-cnot-circuit.png` | 5 | Circuit: a bare `CNOT(0,1)` |
| `ch05-bell-counts.png` | 5 | Histogram of 1000 runs of the Bell state (only `00`, `11`) |
| `ch05-independent-counts.png` | 5 | Histogram of 1000 runs of two independent `H` qubits |
| `ch05-bell-vs-independent.png` | 5 | Grouped bars: independent vs. entangled outcomes |
| `ch05-amplitude-matrices.png` | 5 | Coefficient matrices: product state (rank 1) vs. Bell state (rank 2) |
| `ch06-clone-attempt-circuit.png` | 6 | Circuit: `H` then `CNOT`, the failed clone attempt |
| `ch06-clone-fidelity.png` | 6 | Fidelity of the `CNOT` copy for each input state |
| `ch06-clone-agreement.png` | 6 | Clone of `\|+>`: independent copies vs. the correlated `CNOT` attempt |
| `ch06-cz-circuit.png` | 6 | Circuit: `H` then `CZ`, then measurement |
| `ch06-cz-vs-bell.png` | 6 | `CZ` entangles the pair without changing any probability |
| `ch06-cz-matrices.png` | 6 | Coefficient matrices: one sign flip takes rank 1 to rank 2 |
| `ch06-teleport-circuit.png` | 6 | Teleportation: Bell pair, Bell measurement, `If X` / `If Z` corrections |
| `ch06-teleport-outcomes.png` | 6 | Bob's result for each state Alice sends, keyed by message |
| `ch06-teleport-fidelity.png` | 6 | Every message reconstructs the state exactly |
| `ch06-repeater-circuit.png` | 6 | Two chained hops over five qubits and four classical bits |
| `ch06-repeater-consistency.png` | 6 | Alice's starting `P(1)` vs. Bob's delivered `P(0)` |
| `ch06-repeater-counts.png` | 6 | `P(1) = 0.4` sent through the relay: expected vs. measured |

## Notation used in these notes

| Symbol | Meaning |
|--------|---------|
| <code>\|0⟩</code>, <code>\|1⟩</code> | The two basis states of a qubit |
| <code>\|ψ⟩</code> | A general (arbitrary) single-qubit state |
| <code>\|+⟩</code>, <code>\|−⟩</code> | The two even superpositions <code>(\|0⟩ ± \|1⟩)/√2</code> |
| <code>(a\|0⟩ + b\|1⟩)</code> | A superposition with amplitudes `a` and `b` |
| `[α, β]` | The same state written as a column vector |
| `H` | Hadamard gate — creates an even superposition |
| `X` | Pauli-X gate — flips <code>\|0⟩ ↔ \|1⟩</code> |
| `CNOT` | Controlled-NOT — flips the target when the control is `1` |
| `Z` | Pauli-Z gate — flips the **phase** without changing the bit |
| `CZ` | Controlled-Z — applies `Z` to the target when the control is `1` |
| `⊗` | Tensor product — combines qubits into a joint state |
| Bell state | Maximally entangled pair, e.g. <code>(\|00⟩ + \|11⟩)/√2</code> |
| `I` | The identity operation — "do nothing" |
| `U` | A generic gate, written as a 2×2 matrix |
| `P(0)`, `P(1)` | Measurement probabilities (Born rule: amplitude squared) |
| Bloch sphere | Geometric picture of a single qubit's state |
| Fidelity | Overlap of two states, <code>\|⟨a\|b⟩\|²</code>; 1 means identical |
| Schmidt rank | 1 = product state, 2 = entangled (see the [coefficient matrix](chapters/ch05-entanglement.md#product-states-vs-entangled-states)) |
