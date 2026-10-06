# Chapter 6 — Quantum networking: The basics

!!! abstract "In one sentence"
    A qubit **cannot** be copied, so a quantum network cannot forward a packet the
    way ordinary networking does. It has to *rebuild* the state at each node —
    which is what **teleportation** does with shared entanglement and two
    classical bits, and what a **repeater** chains across a long link.

## A byte over a socket

The chapter opens with the humblest network that exists. A receiver process binds
a port and waits; a sender connects and writes one byte:

```
[Receiver] Starting to listen for incoming data at port 9753
[Sender] Create a connection to port 9753
[Sender] Write a byte: 8
[Sender] Wrote a byte: 8
[Receiver] Got a byte 8
```

The sample in
[`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py)
does exactly this with the Python `socket` module. Nothing about it is exotic —
and that is the point. Every classical network does this, and it does it by the
same trick over and over: **read a packet, copy it, forward the copy.**

## Why a qubit cannot be copied

The book's `classiccopy` sample copies a classical bit. Trivially:

```python
source = True
copy = classic_copy(source)      # both now exist and work
copy = not copy                  # changing the copy leaves the source alone
```

That works because reading a classical bit does not disturb it. The same is
**not** true of a qubit, and not for want of trying — the **no-cloning
theorem** says no machine can copy an arbitrary unknown state.

The argument is short. Suppose a machine could copy any state `|ψ>` while
leaving the original untouched.

1. Feed it `|+>`. The copy comes out as `|+>`, and nothing is wrong yet.
2. Feed it `( |0> + |1> ) / √2` instead. Since copying must be a *linear*
   operation on amplitudes, the copy is then forced to be
   `( |00> + |11> ) / √2`.
3. But measuring **one** qubit of `( |00> + |11> ) / √2` gives 0 or 1 with
   certainty, collapsing the other qubit to `|0>` or `|1>`.
4. So the "copy" is either `|0>` or `|1>` — never `|+>`. Contradiction.

### What a failed attempt looks like

The obvious attempt is a `CNOT`: prepare `|+>` on `q0`, then `CNOT` into `q1`.
Qiskit will happily build and run it. The result is quietly wrong:

![The clone attempt](../assets/ch06-clone-attempt-circuit.png){ width="420" }

The control qubit is never touched, so `q0` *does* keep the original state. But
`q1` ends up entangled with it rather than a copy:

$$H(0),\; CNOT(0,1) \quad\longrightarrow\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

That is a **Bell state**, not two `|+>` states. Measure the pair and the outcomes
come out perfectly *correlated* — `01` and `10` never occur — where two genuine
copies would be independent and give all four outcomes at 25% each:

![A perfect clone vs. the CNOT attempt](../assets/ch06-clone-agreement.png){ width="620" }

The sample also tries the mirror-image trick: forget about copying, just prepare
a fresh `|+>` on the copy with `H`. Neither strategy covers every input.

| Input | `CNOT` clone: copy | `CNOT` clone: source | Fresh `H` on the copy | A real copy |
|---|---|---|---|---|
| <code>\|0⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|1⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|+⟩</code> | 0.50 | 0.50 | 1.00 | 1.00 |
| <code>\|−⟩</code> | 0.50 | 0.50 | 0.00 | 1.00 |

Read the `CNOT` columns: it clones basis states and fails on superpositions.
Read the `H` column: the opposite. **No single row of either strategy is right
for all four inputs.** That gap is the no-cloning theorem, measured.

![Fidelity of the CNOT copy](../assets/ch06-clone-fidelity.png){ width="420" }

!!! note "What this costs a real network"
    Classical networks make a copy of every packet so the original can be
    retransmitted if the link drops. A quantum network cannot do that. It has to
    re-*create* the state at every hop, which is what the rest of this chapter
    is about.

## A phase you cannot see

The book's Chapter 6 exercise ("Pauli-Z gate and Measurement") asks what the
*other* two-qubit gate does. `CZ`, the controlled-Z gate, is `CNOT` with one
difference: when the control is `1` it flips the target's **phase** instead of
its bit.

![The H + CZ circuit](../assets/ch06-cz-circuit.png){ width="420" }

Put both qubits in a superposition first, then apply `CZ`:

$$H(0),\, H(1) \quad\longrightarrow\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}
\qquad\text{(a product state)}$$
$$\xrightarrow{\;CZ\;}\quad \frac{|00\rangle + |01\rangle + |10\rangle - |11\rangle}{2}
\qquad\text{(entangled)}$$

One sign flip changed the state completely: the coefficient matrix goes from rank
1 to rank 2, so the qubits are no longer independent. (See
[product vs. entangled states](ch05-entanglement.md#product-states-vs-entangled-states)
for the rank test.)

And now measure both qubits. You get **all four outcomes at 25% each** — the
identical histogram to the state without the `CZ`:

![CZ versus the Bell state](../assets/ch06-cz-vs-bell.png){ width="620" }

The Born rule *squares* amplitudes, so `|−½|² = |+½|²`. The sign is there, the
entanglement is real, and a computational-basis measurement reports nothing.
Telling the two states apart needs a **different measurement basis** — which is
exactly the trick teleportation uses.

![Coefficient matrices](../assets/ch06-cz-matrices.png){ width="620" }

Two contrast cases round this out. `CZ` after a *lone* `H` does nothing at all,
because qubit 1 stays `|0>` and the control never fires. And `CZ` on the Bell
state flips the same single sign while leaving the outcome set `{00, 11}`
unchanged, because `CNOT` had already done the correlating.

## Teleportation: moving a state, not a particle

Now the main event. Alice cannot read her qubit, and she cannot send a copy. But
she can *destroy* the original and rebuild an identical state at Bob's end, using
correlations they already share.

| Qubit | Whose |
|---|---|
| `q0` | Alice — the state to send |
| `q1` | Alice's half of a Bell pair she shares with Bob |
| `q2` | Bob's half of that pair — the state ends up here |

![The teleportation circuit](../assets/ch06-teleport-circuit.png){ width="620" }

The protocol:

1. **Share a Bell pair.** `H(2)`, `CNOT(2,1)` — Chapter 5 again.
2. **Spread the state.** `CNOT(0,1)`, `H(0)`. Alice's state is now spread across
   both her qubits.
3. **Bell-measure.** Alice measures `q0` and `q1`. This destroys `q0` — and that
   destruction is exactly what lets the state reappear at Bob's end.
4. **Send two classical bits.** Over an ordinary channel, at light speed.
5. **Correct.** Bob applies `X` to `q2` if his bit for `q1` is `1`, and `Z` if
   his bit for `q0` is `1`.

| Alice's message | Bob applies | Bob's qubit when Alice sent <code>\|0⟩</code> | Fidelity |
|---|---|---|---|
| `00` | nothing | <code>\|0⟩</code> | 1.000 |
| `01` | `X` | <code>\|0⟩</code> | 1.000 |
| `10` | `Z` | <code>\|0⟩</code> | 1.000 |
| `11` | `X` then `Z` | <code>\|0⟩</code> | 1.000 |

All four messages occur with probability ¼, and **all four rebuild the state
exactly**. That is the protocol's whole claim, and it holds for every input:

| Alice sends | Bob measures | Fidelity |
|---|---|---|
| <code>\|0⟩</code> | P(0) = 1.00 | 1.000 |
| <code>\|1⟩</code> | P(1) = 1.00 | 1.000 |
| <code>\|+⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |
| <code>\|−⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |

![Every message reconstructs the state](../assets/ch06-teleport-fidelity.png){ width="620" }

Note what fidelity 1.0 does *not* mean: Bob cannot prepare `|+>` from `|0>` by
himself, and he cannot prepare `|0>` from `|+>`. He only *rebuilds* a state that
already existed at Alice's end. Teleportation moves the **information**, not the
particle — Alice's `q0` is gone either way.

![Bob's result for each state Alice sends](../assets/ch06-teleport-outcomes.png){ width="620" }

!!! warning "No faster-than-light signalling"
    Step 4 is an ordinary classical message, limited by the speed of light.
    Without those two bits Bob has a state with a random phase error and no way
    to fix it. That is the "2 classical bits" in the protocol's name, and it is
    why teleportation is *not* superluminal.

## From circuits to networks: the repeater

Teleportation moves a state across one link. A **repeater** chains links together
so a state can cross a much longer distance, with a node in the middle acting as
both receiver and sender:

```
Alice (q0)  ---  link 1  ---  relay (q2)  ---  link 2  ---  Bob (q4)
                        with q1                     with q3
```

![Two chained hops across a relay](../assets/ch06-repeater-circuit.png){ width="620" }

The relay is the interesting part. It **measures** its qubits in the first hop,
exactly as Alice does, so it never holds the state cleanly in between. What
travels is not the state: it is the chain of **correlations** plus *four*
classical bits — two from Alice, two from the relay.

To show the state really arrives, Alice starts with a qubit that is neither
`|0>` nor `|1>`: a rotation with `P(1) = 0.4`. If the relay were only forwarding
classical bits, Bob could see nothing but 0s and 1s. Instead his statistics match
hers, for every input:

| Alice's qubit | P(1) at Alice | P(1) at Bob |
|---|---|---|
| P(1) = 0.0 | 0.00 | 0.00 |
| P(1) = 0.2 | 0.20 | 0.20 |
| P(1) = 0.4 | 0.40 | 0.40 |
| P(1) = 0.6 | 0.60 | 0.60 |
| P(1) = 0.8 | 0.80 | 0.80 |
| P(1) = 1.0 | 1.00 | 1.00 |

![The statistics survive the trip](../assets/ch06-repeater-consistency.png){ width="620" }

![Expected vs. measured at Bob](../assets/ch06-repeater-counts.png){ width="620" }

A genuine mixture arrived at Bob, having been rebuilt twice on the way. And note
that the relay had to *measure* to forward it — the state was never in transit as
a copy, which is precisely why this works even though copying is impossible.

!!! note "Where this leads"
    Distance in a quantum network is limited by **loss**, not by the speed of
    light: a state that decoheres cannot be repaired, because there is no copy to
    fall back on. A repeater does not amplify a weak signal the way a classical
    repeater does — it *recreates* the state at each node from shared
    entanglement plus a classical message. [Chapter 8](ch08-secure-communication.md)
    turns the same idea into secure communication.

## The diagrams

### No-cloning

![The failed clone attempt](../assets/ch06-clone-attempt-circuit.png){ width="420" }

A `CNOT` does not clone: it entangles. The control qubit is untouched, and the
target holds a Bell partner rather than a copy.

![A perfect clone vs. the CNOT attempt](../assets/ch06-clone-agreement.png){ width="620" }

Two real copies of `|+>` would be independent (25% each outcome); the attempt is
perfectly correlated, and `01`/`10` vanish.

![Fidelity of the CNOT copy](../assets/ch06-clone-fidelity.png){ width="420" }

Right for the basis states, exactly wrong for superpositions.

### Controlled-Z

![The H + CZ circuit](../assets/ch06-cz-circuit.png){ width="420" }

![CZ versus the Bell state](../assets/ch06-cz-vs-bell.png){ width="620" }

The first two series are indistinguishable by measurement even though one is a
product state and the other is entangled.

![Coefficient matrices](../assets/ch06-cz-matrices.png){ width="620" }

The single sign flip that takes rank 1 to rank 2.

### Teleportation

![The teleportation circuit](../assets/ch06-teleport-circuit.png){ width="620" }

The `If X` and `If Z` boxes are the classical corrections, driven by Alice's
measurement results.

![Every message reconstructs the state](../assets/ch06-teleport-fidelity.png){ width="620" }

![Bob's result for each state Alice sends](../assets/ch06-teleport-outcomes.png){ width="620" }

### Repeater

![Two chained hops across a relay](../assets/ch06-repeater-circuit.png){ width="620" }

Two Bell pairs, two Bell measurements, four classical corrections.

![The statistics survive the trip](../assets/ch06-repeater-consistency.png){ width="620" }

![Expected vs. measured at Bob](../assets/ch06-repeater-counts.png){ width="620" }

## Key takeaways

- A classical network forwards packets by **copying** them; a quantum network
  cannot, because the **no-cloning theorem** forbids copying an unknown state.
- A `CNOT` does not clone: it entangles. The attempt succeeds on basis states and
  fails on superpositions, and no variant covers both.
- `CZ` flips a phase, and the Born rule squares amplitudes — so `CZ` can turn a
  product state into an entangled one **without changing a single measurement
  probability**.
- **Teleportation** moves a state by destroying the original and rebuilding it
  from shared entanglement plus **two classical bits**. It moves information, not
  a particle, and it is not faster than light.
- A **repeater** chains teleportation hops; a relay that measures can still pass
  a state on, and the delivered qubit keeps the statistics it started with.
- Because loss cannot be repaired from a spare copy, real quantum networks are
  limited by decoherence — the price of the no-copy trick.

## The code behind this chapter

Four samples, one per book section, plus a small shared simulator:

- [`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py)
  — the TCP byte (6.2.1) and the no-cloning demonstration (6.2.2).
- [`ch06/czmeasure.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/czmeasure.py)
  — the Chapter 6 exercise on `CZ` and measurement.
- [`ch06/teleportation.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/teleportation.py)
  — the teleportation circuit and its correction table.
- [`ch06/repeater.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/repeater.py)
  — the two-hop chain across a relay.
- [`ch06/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/protocol.py)
  — the branch simulator they share. Teleportation needs a **mid-circuit
  measurement** whose result drives classical gates, and Qiskit's `Statevector`
  refuses circuits containing control flow. This module keeps one *frame* per
  measurement outcome instead, applying the gates to every frame and branching
  when a qubit is measured.

Run them all with `make ch06`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
```

!!! note "How to read the circuit labels"
    The circuits that get *drawn* are ordinary Qiskit circuits with `if_test`
    blocks, exactly as you would write them. The numbers come from the frame
    simulator, which computes the same distribution without executing control
    flow. Qubits are addressed by plain index (`q0`, `q1`, ...), matching the
    book's Java samples, so `q0` is the qubit at `q[0]`.
