# Glossary

Every term the chapters use, in one table. The Vietnamese version has the same
rows in the same order, so you can switch languages without losing your place
(use the language selector in the top bar).

Terms marked **first use** in a chapter are defined there too, briefly. This page
is the place to come back when a definition has faded.

## The building blocks

| Term | What it means |
|---|---|
| **bit** | A classical `0` or `1`. It holds one value at a time, and reading it does not change it. |
| **qubit** | The quantum version of a bit. Besides `\|0⟩` and `\|1⟩` it can sit in a *combination* of both. |
| **basis state** | One of the named states a system can be in, here `\|0⟩` and `\|1⟩`. Everything else is a weighted sum of these. |
| **ket** | The symbol `\|ψ⟩` naming a state. The ket itself is only a label; the information sits in the numbers in front of it. |
| **amplitude** | The number multiplying a basis state. Not a probability: it can be negative, and even complex. |
| **Born rule** | The rule that turns amplitudes into probabilities: square their magnitudes. |
| **normalisation** | The requirement that squared amplitudes sum to 1, so probabilities are a valid distribution. |
| **superposition** | A state that is a weighted combination of basis states at the same time. |
| **phase** | The angle attached to an amplitude. A single amplitude's phase is unobservable; only a *relative* phase between two parts of a state matters. |
| **interference** | What happens when two parts of a state add up or cancel out, driven by their relative phase. |

## Gates and circuits

| Term | What it means |
|---|---|
| **gate** | A reversible operation applied to one or more qubits. Written as a matrix. |
| **reversible** | The defining property of a quantum gate: you can always undo it, so no information is thrown away. |
| **unitary** | A matrix satisfying `U^† U = I`. Unitarity is *why* gates are reversible and preserve normalisation. |
| **Pauli-X** | The `X` gate — the quantum `NOT`. Flips `\|0⟩ ↔ \|1⟩` and leaves anything else untouched. |
| **Hadamard** | The `H` gate — the standard way to create an even superposition. It is its own inverse, so applying it twice undoes it. |
| **Pauli-Z** | The `Z` gate. Flips the **phase** of `\|1⟩` without touching its bit value. |
| **CNOT** | A two-qubit gate with a **control** and a **target**. It flips the target exactly when the control is `1`. |
| **CZ** | Controlled-Z. Like `CNOT`, but it flips the target's *phase* instead of its bit. |
| **Toffoli** | A three-qubit gate (`CCNOT`) that flips its target only when **both** controls are `1`. A reversible `AND`. |
| **identity** | `I`, the matrix that does nothing. Two `X` gates in a row give `I`, as do two `H` gates. |
| **circuit** | A diagram read left to right: each wire is a qubit, each box is a gate, each meter at the end is a measurement. |
| **shots** | Running a circuit many times to build up a count of outcomes. |

## Multiple qubits

| Term | What it means |
|---|---|
| **tensor product** | `⊗`, how two qubits are glued into one joint state. Not simple concatenation. |
| **product state** | A joint state that *can* be written as one qubit's state times another's. The two qubits are independent. |
| **entangled** | A joint state that *cannot* be written that way. Neither qubit has a state of its own. |
| **Bell state** | A maximally entangled pair, e.g. `(\|00⟩ + \|11⟩)/√2`. Also called an EPR pair. |
| **CNOT** (control/target) | The convention used here writes the **control first**, so `CNOT(c, t)`. |
| **Schmidt rank** | Arrange the amplitudes as a 2×2 matrix. Rank 1 means product; rank 2 means entangled. |

## Measurement

| Term | What it means |
|---|---|
| **measurement** | Collapses a state to one basis state and yields one classical bit. The only non-reversible step. |
| **basis** | Which pair of states you measure against. `{\|0⟩, \|1⟩}` unless stated otherwise. |
| **coherence** | How long a superposition and its phase relationship survive before noise scrambles them. |
| **loss** | A state that never arrives at all, because it was absorbed or scattered on the way. |

## Arithmetic

| Term | What it means |
|---|---|
| **half-adder** | A circuit that adds two bits **modulo 2** (`a XOR b`) and keeps no carry, so `1 + 1` reads `0`. One `CNOT`. |
| **full adder** | A half-adder plus a `Toffoli` that computes the **carry**, so `1 + 1 = 2` instead of wrapping to `0`. |
| **carry** | The bit that is `1` when a sum overflows one bit: the logical `AND` of the two inputs, written onto a spare qubit. |

## Networking

| Term | What it means |
|---|---|
| **no-cloning theorem** | No machine can copy an arbitrary unknown quantum state. This is why quantum networks cannot forward packets the classical way. |
| **teleportation** | Moving a state by destroying the original and rebuilding it from shared entanglement plus two classical bits. Moves information, not matter. |
| **repeater** | A node that chains teleportation links together so a state crosses a longer distance. It rebuilds, it does not amplify. |
| **link** | One connection between two nodes. Teleportation crosses one link; a repeater chains several. |
| **fidelity** | A number from 0 to 1 measuring how close two states are. 1.0 means "identical". |

## Cryptography

| Term | What it means |
|---|---|
| **base** | The pair of states a qubit is written in. The **Z** base is `{\|0⟩, \|1⟩}`; the **X** base is `{\|+⟩, \|−⟩}`. A qubit carries a bit only relative to a base. |
| **BB84** | The first quantum key-distribution protocol: Alice and Bob each pick a random base per qubit, then **sift** — keep only the qubits where the bases agree, and those bits are the shared key. |
| **sifting** | Announcing the *bases* (never the bits) and discarding the qubits measured in the other base. About half survive. |
| **eavesdropper** | Anyone reading the qubits in transit. Because copying is impossible, she must measure and re-send, which introduces about a **25%** error rate on the sifted key — the detection. |

## Algorithms

| Term | What it means |
|---|---|
| **constant function** | A function that gives the same answer on every input. |
| **balanced function** | A function that gives `0` on exactly half its inputs and `1` on the other half. |
| **phase kickback** | The trick that turns a function's value into a *sign*: with the spare register in `\|−⟩`, the oracle multiplies each branch by `(-1)^f(x)`. Hadamards then turn that sign into a bit. |
| **quantum parallelism** | Evaluating a function on all `2^n` inputs in one pass, by running the oracle on a superposition. The answers cannot all be read out — interference is what extracts a usable bit. |
| **amplitude amplification** | The general trick behind Grover: reflect the state so the wanted amplitude grows. |
| **diffusion** | Grover's second step, `2\|s⟩⟨s\| − I`: reflect every amplitude about the mean, lifting the marked one. |
| **Grover iteration** | One oracle plus one diffusion. About `(π/4)·√N` of them find the answer in an unstructured list. |
| **unstructured search** | Searching a list with no order to exploit. Classically `N/2` checks on average; Grover needs `(π/4)·√N` — a **quadratic** speed-up. |
| **order finding** | Finding the smallest `r` with `a^r = 1 (mod N)` — the period of `a^x mod N`. The one step Shor gets from a quantum computer. |
| **period** | The `r` in `a^(x+r) = a^x (mod N)`. |
| **quantum Fourier transform** | The discrete Fourier transform as a circuit. It turns a periodic superposition into a few sharp **peaks** at multiples of `N/r`. |
| **continued fractions** | The classical way to read a fraction out of a measured peak: the denominator of the best convergent is the period `r`. |
| **trial division** | The naive classical factoring method: try every divisor up to `√N`. Correct, and hopeless for large `N`. |

## Complexity and algorithms

| Term | What it means |
|---|---|
| **Big-O** | `O(f)` means growth no faster than `f`, ignoring constant factors. |
| **polynomial** | Growth like `b`, `b²`, `b³`. Doubling the input multiplies the work by a small constant — manageable. |
| **exponential** | Growth like `2^b`. Adding *one* bit can double the work — quickly hopeless. |
| **sub-exponential** | Between the two: faster than every polynomial, slower than a full exponential. GNFS lives here. |
| **super-polynomial** | Faster than every polynomial but *not* necessarily exponential. A different class from sub-exponential — do not confuse the two. |
| **quadratic** | Growth like `b²`. A square-root-class speed-up: real, but not exponential. |
| **GNFS** | The general number field sieve — the best known *classical* way to factor an integer. |
| **NISQ** | Noisy Intermediate-Scale Quantum. Today's machines: a few hundred error-prone qubits, no error correction. |
| **oracle** | A black-box function applied inside a circuit. Used in Deutsch–Jozsa and Grover. |

## Symbols used throughout

| Symbol | Meaning |
|---|---|
| <code>\|0⟩</code>, <code>\|1⟩</code> | The two basis states of a qubit |
| <code>\|ψ⟩</code> | An arbitrary one-qubit state |
| <code>\|+⟩</code>, <code>\|−⟩</code> | The two even superpositions `(\|0⟩ ± \|1⟩)/√2` |
| <code>\|00⟩</code> … <code>\|11⟩</code> | Two-qubit basis states, read left to right |
| `α`, `β` | Amplitudes — probabilities are their squared magnitudes |
| `H`, `X`, `Z`, `I`, `U` | The Hadamard, Pauli-X, Pauli-Z, identity, and generic gates |
| `CNOT(c,t)`, `CZ` | Two-qubit gates; here the control is written first |
| `Toffoli(c,c,t)` | Three-qubit gate — a reversible `AND`; flips the target when both controls are `1` |
| `U_f` | A function oracle: <code>\|x⟩\|y⟩ → \|x⟩\|y ⊕ f(x)⟩</code> |
| `QFT` | The quantum Fourier transform |
| <code>\|s⟩</code> | The uniform superposition over all `N` basis states |
| `⊗` | Tensor product |
| `P(0)`, `P(1)` | Measurement probabilities, by the Born rule |
| <code>\|⟨a\|b⟩\|²</code> | Fidelity between two states |

The full symbol table, with the chapter each one is used in, is on the
[Reference](reference.md) page.