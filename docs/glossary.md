# Glossary

The table below collects every term used in the accompanying chapters, grouped
thematically and arranged in the order in which the concepts arise. The
Vietnamese version of this page contains exactly the same rows in the same
order, so switching language (the selector sits in the top bar) does not
disturb the reading position.

Terms marked **first use** in a chapter are also defined there, briefly, at
the point where the concept is needed. This page therefore serves as the
consolidated reference to return to whenever a definition has faded.

## The building blocks

The terms below describe a single qubit: the object from which every later
section is built.

| Term | What it means |
|---|---|
| **bit** | A classical unit of information taking one of two values, `0` or `1`. A bit holds exactly one value at a time, and reading it does not change that value — this persistence under repeated inspection is what distinguishes classical information from quantum information. |
| **qubit** | The quantum generalisation of a bit. A qubit can occupy `\|0⟩` or `\|1⟩`, but — unlike a bit — it can also occupy a *weighted combination* of both at the same time, a possibility whose consequences dominate the rest of this glossary. |
| **basis state** | One of the named states against which a system is described; for one qubit these are `\|0⟩` and `\|1⟩`. Every other state of the system is expressed as a weighted sum of these basis states, which is why a basis is chosen once and then kept fixed. |
| **ket** | The symbol `\|ψ⟩` used to name a state. The ket itself carries no information and is only a label; the physical content of the state resides in the numbers placed in front of it. |
| **amplitude** | The number multiplying a basis state within such a weighted sum. An amplitude is not itself a probability: it may be negative, and even complex, and it acquires a probabilistic meaning only through the Born rule below. |
| **Born rule** | The rule that converts amplitudes into probabilities: the probability of an outcome is given by the squared magnitude of the corresponding amplitude. It is the bridge between the signed, complex amplitudes and the non-negative probabilities that are actually observed. |
| **normalisation** | The requirement that the squared amplitudes of a state sum to exactly 1, so that the Born rule yields a valid probability distribution over all possible outcomes. |
| **superposition** | A state that is a weighted combination of basis states simultaneously; it is neither one basis state nor the other, but a coherent mixture of both whose weights are precisely the amplitudes defined above. |
| **phase** | The angle attached to an amplitude. The phase of a single amplitude in isolation is unobservable; only a *relative* phase between two parts of the same state has measurable consequences, which is why it is that relative phase the later sections track. |
| **interference** | The effect that occurs when two parts of a state are combined: depending on their relative phase, the parts reinforce one another or cancel out. Interference is the mechanism by which quantum algorithms extract a usable answer from a superposition. |

## Gates and circuits

The terms below concern how qubits are manipulated: the gates themselves, the
reversibility that underlies them, and the diagrams in which the manipulation
is drawn.

| Term | What it means |
|---|---|
| **gate** | A reversible operation applied to one or more qubits. Every gate in these chapters is written as a matrix, and applying the gate to a state amounts to multiplying that matrix into the vector of amplitudes. |
| **reversible** | The defining property of a quantum gate: it can always be undone by some other gate. Reversibility means that no information is discarded anywhere inside a circuit; only measurement (below) breaks this rule. |
| **unitary** | A matrix satisfying `U^† U = I`. Unitarity is *why* gates are reversible and preserve normalisation: the transformation conserves the total squared amplitude, and it follows that the output is still a valid state. |
| **Pauli-X** | The `X` gate — the quantum `NOT`. It flips `\|0⟩ ↔ \|1⟩`, which amounts to swapping the two amplitudes, and otherwise leaves the state unaltered. |
| **Hadamard** | The `H` gate — the standard way to create an even superposition, and equally the standard way to turn such a superposition back into a basis state. The gate is its own inverse, so applying it twice undoes it, a fact used repeatedly in the circuits of later chapters. |
| **Pauli-Z** | The `Z` gate. It flips the **phase** of `\|1⟩` without touching its bit value, and it is therefore contrasted throughout with `X`, which flips the bit value but not the phase. |
| **CNOT** | A two-qubit gate pairing a **control** qubit with a **target** qubit. The target is flipped exactly when the control is `1`, and left untouched otherwise; this conditional behaviour is what makes the state of one qubit depend on another. |
| **CZ** | Controlled-Z. It is laid out like `CNOT`, with a control and a target, but it flips the target's *phase* instead of its bit; the consequence of such a phase flip surfaces only after a change of basis. |
| **Toffoli** | A three-qubit gate (`CCNOT`) that flips its target only when **both** controls are `1`. It computes a reversible `AND`, and thereby connects the reversible gates of this section with the arithmetic circuits below. |
| **identity** | `I`, the matrix that does nothing to any state. Two `X` gates in a row compose to `I`, as do two `H` gates; identities of this kind are how circuits are checked and simplified. |
| **circuit** | A diagram read from left to right: each wire is a qubit, each box a gate acting at that point in time, and each meter at the right-hand end a measurement that finalises the classical output. |
| **shots** | Running one and the same circuit many times to build up a count of outcomes, so that probabilities are estimated from observed frequencies rather than read off directly. |

## Multiple qubits

The terms below describe what occurs when two qubits are treated together
rather than one at a time.

| Term | What it means |
|---|---|
| **tensor product** | `⊗`, the operation that combines two one-qubit states into a single joint state. The combination is not a simple concatenation of labels: amplitudes multiply pairwise, and the resulting joint state carries one amplitude for every pair of classical outcomes. |
| **product state** | A joint state that *can* be written as one qubit's state times the other's. The two qubits are then fully independent: measuring one reveals nothing about the other. |
| **entangled** | A joint state that *cannot* be written in that product form. Neither qubit then possesses a state of its own; the description lives entirely in the joint amplitudes, and the measurement outcomes of the two qubits become correlated. |
| **Bell state** | A maximally entangled pair, e.g. `(\|00⟩ + \|11⟩)/√2`. It is also called an EPR pair, and such pairs are the resource consumed in teleportation (see Networking). |
| **CNOT** (control/target) | The convention used here writes the **control first**, so `CNOT(c, t)`: the first position holds the qubit whose value is read, the second the qubit whose value is flipped. |
| **Schmidt rank** | Arrange the joint amplitudes as a 2×2 matrix and compute its rank. Rank 1 means product; rank 2 means entangled, so the distinction above becomes a matter of linear algebra rather than intuition. |

## Measurement

The terms below concern the step that ends a superposition and produces a
classical answer.

| Term | What it means |
|---|---|
| **measurement** | The act that collapses a state to one basis state — selected by the probabilities of the Born rule — and yields one classical bit. It is the only non-reversible step in a computation, and it thus marks the boundary between the quantum and the classical part of a circuit. |
| **basis** | The pair of states against which the measurement is carried out; `{\|0⟩, \|1⟩}` unless stated otherwise. The same qubit measured in a different basis yields different outcomes, and that dependence is what the Cryptography section exploits. |
| **coherence** | How long a superposition and the phase relationships within it survive before noise scrambles them. Once coherence is lost, the superposition reduces to a classical mixture, and interference can no longer be exploited. |
| **loss** | The situation in which a state never arrives at all, because it was absorbed or scattered on the way. Loss manifests itself as the absence of a detection, and is distinct from the loss of coherence described above. |

## Arithmetic

These terms show how the reversible gates introduced above are assembled into
classical-style addition.

| Term | What it means |
|---|---|
| **half-adder** | A circuit that adds two bits **modulo 2** — the value `a XOR b`, computed by a single `CNOT` — while keeping no carry. Consequently `1 + 1` reads `0`: the circuit is complete as a sum but incomplete as arithmetic. |
| **full adder** | A half-adder extended by one `Toffoli` that computes the **carry** onto a separate output, so that `1 + 1` yields `2` instead of wrapping to `0`. In other words, sum and carry become available at the same time. |
| **carry** | The bit that is `1` precisely when a sum overflows one bit: the logical `AND` of the two inputs, written onto a spare qubit. This is why a reversible `AND` gate — the `Toffoli` above — suffices to compute it. |

## Networking

These terms concern what the no-cloning theorem implies for sending quantum
states between nodes.

| Term | What it means |
|---|---|
| **no-cloning theorem** | The statement that no machine can copy an arbitrary unknown quantum state. It is this impossibility that prevents quantum networks from forwarding packets the classical way, since no copy of the payload can be made in transit. |
| **teleportation** | Moving a state by destroying the original and rebuilding it at the destination from shared entanglement plus two classical bits. It is information that travels, not matter: the state itself is never in transit between the two nodes. |
| **repeater** | A node that chains teleportation links together so that a state crosses a longer total distance. Crucially, it rebuilds; it does not amplify, because amplifying a travelling state would amount to the forbidden copy. |
| **link** | One connection between two adjacent nodes. A single teleportation crosses one link; a repeater chains several links into a longer path. |
| **fidelity** | A number from 0 to 1 measuring how close two states are. A value of 1.0 means "identical"; the quantity appears formally as `\|⟨a\|b⟩\|²` in the symbol table below. |

## Cryptography

These terms describe the first quantum key-distribution protocol and the way
its security is argued.

| Term | What it means |
|---|---|
| **base** | The pair of states a qubit is written in and read against. The **Z** base is `{\|0⟩, \|1⟩}`; the **X** base is `{\|+⟩, \|−⟩}`. A qubit carries a bit only relative to one base, and read in the other base the same qubit yields a random-looking outcome. |
| **BB84** | The first quantum key-distribution protocol. Alice and Bob each pick a random base per qubit; they then **sift** — keep only the qubits for which the bases agree — and the bits from those qubits constitute the shared secret key. |
| **sifting** | The step in which the *bases* (never the bits) are announced and the qubits measured in the other base are discarded. About half of the transmitted qubits survive, and those survivors form the raw shared key. |
| **eavesdropper** | Anyone reading the qubits in transit. Because copying is impossible, such an interception must measure and re-send, which introduces an error rate of about **25%** on the sifted key; this elevated error rate is precisely the detection. |

## Algorithms

These terms cover the algorithmic building blocks used by Deutsch–Jozsa,
Grover, and Shor.

| Term | What it means |
|---|---|
| **constant function** | A function that gives the same answer on every input, so that all outputs agree. It is one of the two categories distinguished by the first oracle algorithm. |
| **balanced function** | A function that gives `0` on exactly half its inputs and `1` on the other half. Together with the constant functions, it forms the second category against which the oracle is tested. |
| **phase kickback** | The trick that turns a function's value into a *sign*: with the spare register in `\|−⟩`, the oracle multiplies each branch of the superposition by `(-1)^f(x)`. Hadamards applied afterwards then turn that sign pattern into a readable bit. |
| **quantum parallelism** | Evaluating a function on all `2^n` inputs in one pass, by running the oracle on a uniform superposition of inputs. The parallel answers cannot all be read out at once; it is interference that extracts a single usable bit from them. |
| **amplitude amplification** | The general trick behind Grover: the state is reflected repeatedly so that the amplitude of the wanted entries grows while all other amplitudes shrink. The Grover iteration below is the concrete instance of this trick. |
| **diffusion** | Grover's second step, the operator `2\|s⟩⟨s\| − I`: it reflects every amplitude about the mean, lifting the marked one above the average and driving all others below it. |
| **Grover iteration** | One application of the oracle followed by one diffusion. About `(π/4)·√N` such iterations find the answer in an unstructured list of `N` items. |
| **unstructured search** | Searching a list with no order to exploit. A classical examination takes `N/2` checks on average, whereas Grover needs `(π/4)·√N` iterations — a **quadratic** speed-up rather than an exponential one. |
| **order finding** | Finding the smallest `r` with `a^r = 1 (mod N)` — the period of `a^x mod N`. It is the one step of Shor's algorithm for which the quantum computer is genuinely required. |
| **period** | The `r` in `a^(x+r) = a^x (mod N)`: the interval after which the sequence of powers of `a` repeats itself. |
| **quantum Fourier transform** | The discrete Fourier transform realised as a circuit. It turns a periodic superposition into a few sharp **peaks** at multiples of `N/r`, and the period is then read off those peaks. |
| **continued fractions** | The classical way to read a fraction out of a measured peak: the denominator of the best convergent is the period `r`. This post-processing step completes Shor's algorithm. |
| **trial division** | The naive classical factoring method: try every divisor up to `√N`. The method is correct, and hopeless for large `N`, since its running time grows as the square root of `N` itself. |

## Complexity and algorithms

These terms fix the vocabulary in which the running times of classical and
quantum methods are compared.

| Term | What it means |
|---|---|
| **Big-O** | `O(f)` means growth no faster than `f`, ignoring constant factors. It is the notation in which the cost of the classical and quantum methods above is stated in these chapters. |
| **polynomial** | Growth like `b`, `b²`, `b³`. Doubling the input multiplies the work by a small constant, and for that reason such growth is considered manageable. |
| **exponential** | Growth like `2^b`. Adding *one* bit to the input can double the work, and the cost accordingly becomes hopeless quickly. |
| **sub-exponential** | Between the two previous categories: faster than every polynomial, slower than a full exponential. It is in this regime that the GNFS below lives. |
| **super-polynomial** | Faster than every polynomial but *not* necessarily exponential. The category is a different one from sub-exponential, and the two must not be confused. |
| **quadratic** | Growth like `b²`. A speed-up of this square-root class is real and worthwhile, but it does not cross the polynomial/exponential divide. |
| **GNFS** | The general number field sieve — the best known *classical* way to factor an integer, and the benchmark against which the quantum result above is measured. |
| **NISQ** | Noisy Intermediate-Scale Quantum. The designation for the machines of the present era: a few hundred error-prone qubits, with no error correction available. |
| **oracle** | A black-box function applied inside a circuit, in the form of the unitary `U_f`. It is the query structure used in Deutsch–Jozsa and in Grover. |

## Symbols used throughout

The following notation recurs across the chapters; each symbol is listed
together with its established meaning.

| Symbol | Meaning |
|---|---|
| <code>\|0⟩</code>, <code>\|1⟩</code> | The two basis states of a qubit, against which every one-qubit state is written |
| <code>\|ψ⟩</code> | An arbitrary one-qubit state, written as a ket |
| <code>\|+⟩</code>, <code>\|−⟩</code> | The two even superpositions `(\|0⟩ ± \|1⟩)/√2`, which together form the X base |
| <code>\|00⟩</code> … <code>\|11⟩</code> | Two-qubit basis states, read left to right |
| `α`, `β` | Amplitudes; the corresponding probabilities are their squared magnitudes, by the Born rule |
| `H`, `X`, `Z`, `I`, `U` | The Hadamard, Pauli-X, Pauli-Z, identity, and generic gates |
| `CNOT(c,t)`, `CZ` | Two-qubit gates; here the control is written first |
| `Toffoli(c,c,t)` | Three-qubit gate — a reversible `AND`; it flips the target when both controls are `1` |
| `U_f` | A function oracle: <code>\|x⟩\|y⟩ → \|x⟩\|y ⊕ f(x)⟩</code> |
| `QFT` | The quantum Fourier transform, described under Algorithms |
| <code>\|s⟩</code> | The uniform superposition over all `N` basis states |
| `⊗` | The tensor product, the operation that joins qubits into a joint state |
| `P(0)`, `P(1)` | Measurement probabilities, obtained by applying the Born rule |
| <code>\|⟨a\|b⟩\|²</code> | The fidelity between two states |

The full symbol table, with the chapter each one is used in, is on the
[Reference](reference.md) page.
