# Reference

This reference provides a systematic map from each chapter of the book to its
corresponding source module, the command that executes that module, and the
diagrams generated in the process. It is intended to be consulted alongside the
chapter texts: the module links lead directly to the implementation code,
whereas the *concepts* behind each program are developed on the chapter pages,
which should be followed for the conceptual exposition.

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

The accompanying command-line interface accepts a chapter identifier as its
argument. Invoking the CLI with a given chapter id executes the sample program
of that chapter and produces the corresponding output and figures:

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

Every diagram produced by the sample programs is written to the `build/`
directory and is prefixed with the chapter number, so that any individual figure
can always be traced back to the chapter and the program that generated it. The
table below lists each generated file together with a description of the figure
it depicts.

| Diagram | Chapter | Shows |
|---------|---------|-------|
| `ch01-time-complexity.png` | 1 | The factoring-time curves of the classical and the Shor-based approaches, compared side by side |
| `ch01-time-complexity-classical.png` | 1 | The classical factoring-time curve, plotted in isolation |
| `ch02-random-bits-circuit.png` | 2 | Circuit diagram: a single `H` gate followed by a measurement |
| `ch02-random-bits-counts.png` | 2 | Histogram of 10,000 measured bits, showing the two outcomes at roughly equal frequency |
| `ch02-random-bits-bloch.png` | 2 | The resulting superposition displayed on the Bloch sphere |
| `ch03-pauli-x.png` | 3 | Circuit diagram: a single `X` gate followed by a measurement |
| `ch03-pauli-x2-circuit.png` | 3 | Circuit diagram: two consecutive `X` gates followed by a measurement |
| `ch03-pauli-x-bloch.png` | 3 | The evolution of <code>\|0⟩</code> → after `X` → after `X·X`, traced step by step |
| `ch03-pauli-x-counts.png` | 3 | Histogram of 1000 runs of `X` (every run yields `1`) |
| `ch03-pauli-x2-counts.png` | 3 | Histogram of 1000 runs of `X·X` (every run yields `0`) |
| `ch04-hadamard-circuit.png` | 4 | Circuit diagram: a single `H` gate followed by a measurement |
| `ch04-hadamard2-circuit.png` | 4 | Circuit diagram: two consecutive `H` gates followed by a measurement |
| `ch04-hadamard-bloch.png` | 4 | The evolution of <code>\|0⟩</code> → after `H` → after `H·H`, traced step by step |
| `ch04-hadamard-counts.png` | 4 | Histogram of 1000 runs of `H`, showing the two measurement outcomes |
| `ch04-hadamard2-counts.png` | 4 | Histogram of 1000 runs of `H·H` (every run yields `0`) |
| `ch04-gate-matrices.png` | 4 | The matrices of `X`, `H`, and `H·H`, rendered as heatmaps |
| `ch05-bell-circuit.png` | 5 | Circuit diagram: `H`, `CNOT`, followed by a measurement of both qubits |
| `ch05-cnot-circuit.png` | 5 | Circuit diagram: a bare `CNOT(0,1)` applied without any additional preparation |
| `ch05-bell-counts.png` | 5 | Histogram of 1000 runs of the Bell state (only the outcomes `00` and `11` appear) |
| `ch05-independent-counts.png` | 5 | Histogram of 1000 runs of two qubits, each passing through its own `H` gate |
| `ch05-bell-vs-independent.png` | 5 | Grouped bar chart: the outcomes of the independent case versus the entangled case |
| `ch05-amplitude-matrices.png` | 5 | Coefficient matrices: the product state (rank 1) compared with the Bell state (rank 2) |
| `ch06-clone-attempt-circuit.png` | 6 | Circuit diagram: `H` then `CNOT`, representing the clone attempt that fails |
| `ch06-clone-fidelity.png` | 6 | The fidelity of the `CNOT` copy, evaluated for each possible input state |
| `ch06-clone-agreement.png` | 6 | Cloning of `\|+⟩`: two independent copies compared with the correlated `CNOT` attempt |
| `ch06-cz-circuit.png` | 6 | Circuit diagram: `H`, then `CZ`, followed by a measurement |
| `ch06-cz-vs-bell.png` | 6 | Demonstration that `CZ` entangles the pair without changing any measurement probability |
| `ch06-cz-matrices.png` | 6 | Coefficient matrices: a single sign flip raising the rank from 1 to 2 |
| `ch06-teleport-circuit.png` | 6 | The teleportation protocol: a Bell pair, a Bell measurement, and the `If X` / `If Z` corrections |
| `ch06-teleport-outcomes.png` | 6 | Bob's measurement result for each state Alice sends, indexed by the classical message |
| `ch06-teleport-fidelity.png` | 6 | Demonstration that every message reconstructs the transmitted state exactly |
| `ch06-repeater-circuit.png` | 6 | Two chained repeater links, carried over five qubits and four classical bits |
| `ch06-repeater-consistency.png` | 6 | Alice's initial `P(1)` compared with the `P(0)` delivered to Bob |
| `ch06-repeater-counts.png` | 6 | The value `P(1) = 0.4` sent through the relay: the expected distribution compared with the measured one |
| `ch07-randombit-circuit.png` | 7 | Circuit diagram: the four-qubit program, composed of `H`, `X`, and `CNOT` |
| `ch07-randombit-counts.png` | 7 | Histogram of the measurement results, which collapse onto the two possible outcomes satisfying `q0 = q1` |
| `ch07-randombit-qubits.png` | 7 | The value of `P(1)` for each qubit: `q0`/`q1` at 0.50, `q2` at 0, and `q3` at 1 |
| `ch07-debug-circuit.png` | 7 | The same program, with a barrier inserted to mark each step |
| `ch07-debug-steps.png` | 7 | The distribution over basis states after each step |
| `ch07-debug-marginals.png` | 7 | The marginal `P(1)` for each qubit after each step, revealing which step moved which qubit |
| `ch07-add1-circuit.png` | 7 | The half-adder: `CNOT` applied to `1 + 1`, summing modulo 2 |
| `ch07-add2-circuit.png` | 7 | The full adder: `Toffoli` (computing the carry) followed by `CNOT` (computing the sum) |
| `ch07-toffoli-matrices.png` | 7 | The matrices of `X`, `CNOT`, and `Toffoli`: each successive gate adds one control |
| `ch07-adder-comparison.png` | 7 | Half-adder versus full adder: `1 + 1` results in 0 without a carry, and in 2 with one |
| `ch08-haha-circuit.png` | 8 | Circuit diagram: `X` then `H`, `H` — a basis entered and then left again |
| `ch08-haha-bloch.png` | 8 | The same evolution displayed on the Bloch sphere, illustrating `H·H = I` |
| `ch08-attempts-error.png` | 8 | The raw error rate: the case with no basis compared with an unreconciled one |
| `ch08-superposition-circuit.png` | 8 | The four-qubit circuit used to prepare a superposition |
| `ch08-superposition-states.png` | 8 | All sixteen states displayed at once, followed by the recovery of the prepared bits |
| `ch08-bb84-circuit.png` | 8 | A single BB84 exchange: state preparation, Bob's choice of basis, and measurement |
| `ch08-eavesdropper-error.png` | 8 | The sifted errors accumulated over 200 exchanges: the clean channel compared with the wiretap |
| `ch09-reversible-circuit.png` | 9 | Circuit diagram: `X`, `X` — demonstrating that every gate in the sequence is reversible |
| `ch09-oracle-matrices.png` | 9 | The four possible oracle matrices for a one-bit function |
| `ch09-oracle-circuit.png` | 9 | The balanced oracle `f(x) = x`, realisable with a single `CNOT` |
| `ch09-deutsch-circuit.png` | 9 | The Deutsch circuit, built from `X`, `H`, `H`, the oracle, and a final `H` |
| `ch09-deutsch-outcomes.png` | 9 | A single oracle query: a constant function measures 0, a balanced function measures 1 |
| `ch09-dj-circuit.png` | 9 | The Deutsch–Jozsa circuit for `n = 3` |
| `ch09-dj-outcomes.png` | 9 | For `n = 2`: a constant oracle returns `00`, whereas a balanced oracle never does |
| `ch10-classical-tries.png` | 10 | The classical linear scan: the number of tries required to locate the target |
| `ch10-oracle-matrix.png` | 10 | Grover's phase oracle, realised as a single sign flip |
| `ch10-step-by-step.png` | 10 | Grover's algorithm on 2 qubits: the probability of each basis state after each round |
| `ch10-grover-circuit.png` | 10 | A 3-qubit Grover circuit: an initial `H` layer, followed by alternating oracle/diffusion pairs |
| `ch10-grover-curve.png` | 10 | Grover's algorithm on 64 items: the success probability rises and then overshoots |
| `ch10-grover-outcomes.png` | 10 | The 64 possible outcomes after 6 rounds: the correct answer dominates the distribution |
| `ch11-classical-factor.png` | 11 | Trial division: the amount of work grows like `sqrt(n)` |
| `ch11-period-function.png` | 11 | The function `2^x mod 15`, which repeats with period 4 |
| `ch11-qft-circuit.png` | 11 | The quantum Fourier transform circuit for three qubits |
| `ch11-qft-phase.png` | 11 | The state `QFT\|1⟩`: uniform magnitudes combined with a linear phase ramp |
| `ch11-order-circuit.png` | 11 | A compact order-finding circuit for `2^x mod 15` |
| `ch11-order-peaks.png` | 11 | The output of the inverse QFT: four peaks, spaced 64 apart |

## Book samples and their Python ports

The book's Java samples are organised into one directory per program
(`quantumjava/chNN/sample`). The following table maps these directories to the
Python modules of this repository, chapter by chapter, so that each
demonstrative program from the book can be located directly in its ported form.

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

Some samples share a single module: the four chapter 9 oracle samples, for
instance, are all contained in `ch09.oracles`. In addition, a few modules
provide support code for which no Java counterpart exists (`ch07.circuits`,
`ch08.protocol`). It is worth noting that the `quantumjava/ch11/jshell` snippets
correspond to the book's hand calculations; the call
`ch11.classical.reduction_steps(6, 493)` reproduces them programmatically.

## Notation used in these notes

The notation below is used throughout these notes. Each symbol is introduced at
the point where it first becomes relevant, and the table collects the
definitions in one place for quick consultation while reading.

| Symbol | Meaning |
|--------|---------|
| <code>\|0⟩</code>, <code>\|1⟩</code> | The two computational basis states of a qubit, corresponding to the bit values 0 and 1 |
| <code>\|ψ⟩</code> | A general (arbitrary) single-qubit state, not restricted to a basis state |
| <code>\|+⟩</code>, <code>\|−⟩</code> | The two even superpositions <code>(\|0⟩ ± \|1⟩)/√2</code>, which differ from one another only in relative phase |
| <code>(a\|0⟩ + b\|1⟩)</code> | A superposition of <code>\|0⟩</code> and <code>\|1⟩</code> with amplitudes `a` and `b`, respectively |
| `[α, β]` | The same state written as a column vector, with components `α` and `β` |
| `H` | Hadamard gate — creates an even superposition from a basis state |
| `X` | Pauli-X gate — flips <code>\|0⟩ ↔ \|1⟩</code> |
| `CNOT` | Controlled-NOT — flips the target qubit when the control qubit is `1` |
| `Toffoli` | Controlled-controlled-NOT (`CCNOT`) — flips the target when **both** controls are `1`; a reversible implementation of `AND` |
| `XOR` | Exclusive-or — the sum bit of addition modulo 2 |
| `U_f` | A function oracle for `f`: `\|x⟩\|y⟩ → \|x⟩\|y ⊕ f(x)⟩` |
| `QFT` | The quantum Fourier transform — the discrete Fourier transform implemented as a circuit |
| `\|s⟩` | The uniform superposition over all `N` basis states, in which every basis state carries the same amplitude |
| `Z` | Pauli-Z gate — flips the **phase** without changing the bit |
| `CZ` | Controlled-Z — applies `Z` to the target qubit when the control qubit is `1` |
| `⊗` | Tensor product — combines single-qubit states into a joint multi-qubit state |
| Bell state | Maximally entangled pair, e.g. <code>(\|00⟩ + \|11⟩)/√2</code> |
| `I` | The identity operation — "do nothing", that is, the operation which leaves every state unchanged |
| `U` | A generic gate, written as a 2×2 matrix |
| `P(0)`, `P(1)` | Measurement probabilities (Born rule: amplitude squared) |
| Bloch sphere | Geometric picture of a single qubit's state |
| Fidelity | Overlap of two states, <code>\|⟨a\|b⟩\|²</code>; a value of 1 indicates identical states |
| Schmidt rank | 1 indicates a product state and 2 an entangled state (see the section on the [coefficient matrix](chapters/ch05-entanglement.md#product-states-vs-entangled-states)) |
