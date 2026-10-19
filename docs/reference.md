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
| [7](chapters/ch07-helloworld-explained.md) | Our HelloWorld, explained | [`ch07/randombit.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/randombit.py), [`ch07/debugging.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/debugging.py), [`ch07/half_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/half_adder.py), [`ch07/full_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/full_adder.py), [`ch07/circuits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/circuits.py) | `make ch07` |
| [8](chapters/ch08-secure-communication.md) | Secure communication using quantum computing | [`ch08/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/protocol.py), [`ch08/identity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/identity.py), [`ch08/attempts.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/attempts.py), [`ch08/superposition.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/superposition.py), [`ch08/bb84.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/bb84.py) | `make ch08` |
| [9](chapters/ch09-deutsch-jozsa.md) | Deutsch–Jozsa algorithm | [`ch09/reversible.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/reversible.py), [`ch09/oracles.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/oracles.py), [`ch09/deutsch.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutsch.py), [`ch09/deutschjozsa.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutschjozsa.py) | `make ch09` |
| [10](chapters/ch10-grovers-search.md) | Grover's search algorithm | [`ch10/search.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/search.py), [`ch10/oracle.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/oracle.py), [`ch10/step_by_step.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/step_by_step.py), [`ch10/grover.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/grover.py) | `make ch10` |
| [11](chapters/ch11-shors-algorithm.md) | Shor's algorithm | [`ch11/classical.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/classical.py), [`ch11/qft.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/qft.py), [`ch11/shor.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/shor.py) | `make ch11` |

The CLI takes the chapter id:

```bash
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
| `ch06-clone-agreement.png` | 6 | Clone of `\|+⟩`: independent copies vs. the correlated `CNOT` attempt |
| `ch06-cz-circuit.png` | 6 | Circuit: `H` then `CZ`, then measurement |
| `ch06-cz-vs-bell.png` | 6 | `CZ` entangles the pair without changing any probability |
| `ch06-cz-matrices.png` | 6 | Coefficient matrices: one sign flip takes rank 1 to rank 2 |
| `ch06-teleport-circuit.png` | 6 | Teleportation: Bell pair, Bell measurement, `If X` / `If Z` corrections |
| `ch06-teleport-outcomes.png` | 6 | Bob's result for each state Alice sends, keyed by message |
| `ch06-teleport-fidelity.png` | 6 | Every message reconstructs the state exactly |
| `ch06-repeater-circuit.png` | 6 | Two chained links over five qubits and four classical bits |
| `ch06-repeater-consistency.png` | 6 | Alice's starting `P(1)` vs. Bob's delivered `P(0)` |
| `ch06-repeater-counts.png` | 6 | `P(1) = 0.4` sent through the relay: expected vs. measured |
| `ch07-randombit-circuit.png` | 7 | Circuit: the four-qubit program (`H`, `X`, `CNOT`) |
| `ch07-randombit-counts.png` | 7 | Histogram of the two possible outcomes (`q0 = q1`) |
| `ch07-randombit-qubits.png` | 7 | `P(1)` for each qubit: `q0`/`q1` at 0.50, `q2` 0, `q3` 1 |
| `ch07-debug-circuit.png` | 7 | The program with a barrier marking each step |
| `ch07-debug-steps.png` | 7 | Basis-state probabilities after each step |
| `ch07-debug-marginals.png` | 7 | `P(1)` per qubit after each step: which step moved which qubit |
| `ch07-add1-circuit.png` | 7 | Half-adder: `CNOT` for `1 + 1`, summing modulo 2 |
| `ch07-add2-circuit.png` | 7 | Full adder: `Toffoli` (carry) then `CNOT` (sum) |
| `ch07-toffoli-matrices.png` | 7 | The `X`, `CNOT`, and `Toffoli` matrices: each adds a control |
| `ch07-adder-comparison.png` | 7 | Half-adder vs. full adder: `1 + 1` is 0 without a carry, 2 with one |
| `ch08-haha-circuit.png` | 8 | Circuit: `X` then `H`, `H` — a base entered and left |
| `ch08-haha-bloch.png` | 8 | The same on the Bloch sphere: `H·H = I` |
| `ch08-attempts-error.png` | 8 | Raw error rate: no base vs. an unreconciled one |
| `ch08-superposition-circuit.png` | 8 | The four-qubit superposition circuit |
| `ch08-superposition-states.png` | 8 | All sixteen states at once, then the prepared bits back |
| `ch08-bb84-circuit.png` | 8 | One BB84 exchange: prepare, Bob's base, measure |
| `ch08-eavesdropper-error.png` | 8 | Sifted errors over 200 exchanges: clean line vs. wiretap |
| `ch09-reversible-circuit.png` | 9 | Circuit: `X`, `X` — every gate is reversible |
| `ch09-oracle-matrices.png` | 9 | The four one-bit oracle matrices |
| `ch09-oracle-circuit.png` | 9 | The balanced `f(x) = x` oracle: one `CNOT` |
| `ch09-deutsch-circuit.png` | 9 | The Deutsch circuit (`X`, `H`, `H`, oracle, `H`) |
| `ch09-deutsch-outcomes.png` | 9 | One query: constant measures 0, balanced measures 1 |
| `ch09-dj-circuit.png` | 9 | Deutsch–Jozsa for `n = 3` |
| `ch09-dj-outcomes.png` | 9 | `n = 2`: a constant oracle returns `00`, a balanced one never does |
| `ch10-classical-tries.png` | 10 | Classical linear scan: tries to find the target |
| `ch10-oracle-matrix.png` | 10 | Grover's phase oracle: one sign flip |
| `ch10-step-by-step.png` | 10 | Grover on 2 qubits: probability per basis state per round |
| `ch10-grover-circuit.png` | 10 | A 3-qubit Grover circuit: `H`, then oracle/diffusion pairs |
| `ch10-grover-curve.png` | 10 | Grover on 64 items: probability rises then overshoots |
| `ch10-grover-outcomes.png` | 10 | 64 outcomes after 6 rounds: the answer dominates |
| `ch11-classical-factor.png` | 11 | Trial division: work grows like `sqrt(n)` |
| `ch11-period-function.png` | 11 | `2^x mod 15` repeats with period 4 |
| `ch11-qft-circuit.png` | 11 | The three-qubit QFT circuit |
| `ch11-qft-phase.png` | 11 | `QFT\|1⟩`: uniform magnitude, linear phase ramp |
| `ch11-order-circuit.png` | 11 | A compact order-finding circuit for `2^x mod 15` |
| `ch11-order-peaks.png` | 11 | The inverse QFT: four peaks, 64 apart |

## Book samples and their Python ports

The book's Java samples live in one directory per program (`quantumjava/chNN/sample`).
This table maps them to the Python modules here, chapter by chapter.

| Book chapter | Java samples (`quantumjava/chNN/`) | Python modules |
|---|---|---|
| 1 | `time` | `ch01.time_complexity` |
| 2 | `hellostrange` | `ch02.random_bits` |
| 3 | `paulix`, `paulixui` | `ch03.pauli_x` |
| 4 | `hadamard`, `hadamard2` | `ch04.hadamard`, `ch04.matrices` |
| 5 | `bellstate`, `classiccoin`, `cnot`, `maryqubit`, `quantumcoin` | `ch05.entanglement`, `ch05.states` |
| 6 | `classic`, `classiccopy`, `hczmeasure`, `teleport`, `repeater` | `ch06.networking`, `ch06.czmeasure`, `ch06.teleportation`, `ch06.repeater`, `ch06.protocol` |
| 7 | `randombit`, `randombitdebug`, `add1`, `add2` | `ch07.randombit`, `ch07.debugging`, `ch07.half_adder`, `ch07.full_adder`, `ch07.circuits` |
| 8 | `haha`, `naive`, `guess`, `superposition`, `bb84` | `ch08.identity`, `ch08.attempts`, `ch08.superposition`, `ch08.bb84`, `ch08.protocol` |
| 9 | `reversibleX`, `function`, `oracle`, `applyoracle`, `deutsch`, `deutschjozsa` | `ch09.reversible`, `ch09.oracles`, `ch09.deutsch`, `ch09.deutschjozsa` |
| 10 | `classicsearch`, `quantumsearch`, `groveroracle`, `stepbystepgrover`, `grover` | `ch10.search`, `ch10.oracle`, `ch10.step_by_step`, `ch10.grover` |
| 11 | `classicfactor`, `semiclassicfactor`, `quantumfactor`, `jshell` | `ch11.classical`, `ch11.qft`, `ch11.shor` |

Some samples share a module (the four chapter 9 oracle samples, for instance, are
all in `ch09.oracles`), and a few add support code with no Java counterpart
(`ch07.circuits`, `ch08.protocol`). The `quantumjava/ch11/jshell` snippets are the
book's hand calculations; `ch11.classical.reduction_steps(6, 493)` reproduces
them.

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
| `Toffoli` | Controlled-controlled-NOT (`CCNOT`) — flips the target when **both** controls are `1`; a reversible `AND` |
| `XOR` | Exclusive-or — the sum bit of addition modulo 2 |
| `U_f` | A function oracle: `\|x⟩\|y⟩ → \|x⟩\|y ⊕ f(x)⟩` |
| `QFT` | The quantum Fourier transform — the discrete Fourier transform as a circuit |
| `\|s⟩` | The uniform superposition over all `N` basis states |
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
