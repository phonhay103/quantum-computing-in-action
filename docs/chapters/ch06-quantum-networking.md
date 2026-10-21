# Chapter 6 — Quantum networking: The basics

!!! abstract "In one sentence"
    A qubit **cannot** be copied, so a quantum network cannot forward a packet the
    way ordinary networking does — it has to *rebuild* the state at each node,
    which is what **teleportation** does with shared entanglement and two
    classical bits. The chapter establishes the prohibition first, then develops
    the protocol that circumvents it by moving the state's information rather
    than the state itself.

## A byte over a socket

The chapter opens with the humblest network that can be constructed, and this
minimalism is deliberate: the contrast between what such a network does and what
a quantum network can never do is the organizing idea of everything that
follows. A receiver process binds a specific port and then simply waits for a
connection to arrive; a sender process connects to that port and writes a single
byte of payload:

```
[Receiver] Starting to listen for incoming data at port 9753
[Sender] Create a connection to port 9753
[Sender] Write a byte: 8
[Sender] Wrote a byte: 8
[Receiver] Got a byte 8
```

The sample in
[`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py)
performs exactly this exchange with the Python `socket` module, and nothing
about its machinery is exotic — indeed, that absence of exotica is precisely the
point. Every classical network carries out essentially this same service, and it
does so by applying one rule over and over again: **read a packet, copy it,
forward the copy.** The next section establishes that this fundamental rule has
no quantum analogue, and that the prohibition behind its absence is a theorem
rather than an engineering difficulty.

## Why a qubit cannot be copied

The book's `classiccopy` sample copies a single classical bit, and the
procedure succeeds because classical information permits duplication without
any penalty:

```python
source = True
copy = classic_copy(source)      # both now exist and work
copy = not copy                  # changing the copy leaves the source alone
```

This construction works because the act of reading a classical bit does not
disturb it: a classical bit already occupies one of two definite values, and
inspecting which value it holds leaves that value itself unchanged. The same
claim is **not** true of a qubit, and this is not for want of trying — the
**no-cloning theorem** states that no physical device, however sophisticated,
can copy an arbitrary unknown quantum state.

The argument is short, and it proceeds by contradiction. Suppose a machine could
copy any state `|ψ⟩` while leaving the original untouched.

1. Supplying it with the basis states `|0⟩` and `|1⟩` produces correct copies,
   and at this stage the hypothetical device is fully consistent with its
   own definition.
2. Supplying it with `|+⟩ = ( |0⟩ + |1⟩ ) / √2` instead exposes the
   difficulty: because copying must be a *linear* operation on amplitudes, the
   output is then forced to be
   `( |00⟩ + |11⟩ ) / √2` — an entangled pair, not two independent copies
   of `|+⟩`.
3. Measuring **one** qubit of `( |00⟩ + |11⟩ ) / √2`, however, yields a
   definite `0` or `1`, collapsing the other qubit to `|0⟩` or `|1⟩`.
4. Consequently the "copy" is either `|0⟩` or `|1⟩` — never `|+⟩`. This is a
   contradiction.

### What a failed attempt looks like

The most obvious attempt is a `CNOT`: a `|+⟩` state is prepared on `q0`, and the
`CNOT` is then applied into `q1`. Qiskit builds and runs this circuit without
complaint, which makes the failure instructive rather than immediate — the
result is quietly wrong:

![The clone attempt](../assets/ch06-clone-attempt-circuit.png){ width="420" }

The control qubit is never touched by the operation, so `q0` *does* keep the
original state. But `q1` ends up entangled with it rather than standing as an
independent copy:

$$H(0),\; CNOT(0,1) \quad\longrightarrow\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

What has been produced is a **Bell state**, not two `|+⟩` states. Measuring the
pair yields outcomes that are perfectly *correlated* — `01` and `10` never
occur — whereas two genuine copies would be independent and give all four
outcomes at 25% each:

![A perfect clone vs. the CNOT attempt](../assets/ch06-clone-agreement.png){ width="620" }

The sample also tries the mirror-image strategy: abandoning the copy itself and
simply preparing a fresh `|+⟩` on the copy register with `H`. As the table
demonstrates, neither strategy covers every input.

| Input | `CNOT` clone: copy | `CNOT` clone: source | Fresh `H` on the copy | A real copy |
|---|---|---|---|---|
| <code>\|0⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|1⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|+⟩</code> | 0.50 | 0.50 | 1.00 | 1.00 |
| <code>\|−⟩</code> | 0.50 | 0.50 | 0.00 | 1.00 |

Reading down the `CNOT` columns shows a strategy that clones basis states and
fails on superpositions. Reading the `H` column shows the opposite pattern.
**No single row of either strategy is right for all four inputs.** That
measurable gap — between what each strategy achieves and what a genuine copy
requires — is the no-cloning theorem presented as data rather than as proof.

![Fidelity of the CNOT copy](../assets/ch06-clone-fidelity.png){ width="420" }

!!! note "What this costs a real network"
    Classical networks make a copy of every packet so that the original can be
    safely retransmitted if the link drops mid-transfer. A quantum network
    cannot do that, because the no-cloning theorem removes this safety net at
    the fundamental level. It therefore has to re-*create* the state at every
    link from whatever resources remain available, which is precisely what the
    rest of this chapter is about.

## A phase you cannot see

The book's Chapter 6 exercise ("Pauli-Z gate and Measurement") asks what the
*other* two-qubit gate does. `CZ`, the controlled-Z gate, is `CNOT` with a
single difference: when the control is `1` it flips the target's **phase**
instead of its bit. The change acts entirely on the sign structure of the
amplitudes and leaves every magnitude untouched, which will matter below.

![The H + CZ circuit](../assets/ch06-cz-circuit.png){ width="420" }

The demonstration proceeds by placing both qubits in an equal superposition
first, then applying `CZ`:

$$H(0),\, H(1) \quad\longrightarrow\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}
\qquad\text{(a product state)}$$
$$\xrightarrow{\;CZ\;}\quad \frac{|00\rangle + |01\rangle + |10\rangle - |11\rangle}{2}
\qquad\text{(entangled)}$$

One sign flip has changed the character of the state completely: the
coefficient matrix goes from rank 1 to rank 2, and it follows that the qubits
are no longer independent. (See
[product vs. entangled states](ch05-entanglement.md#product-states-vs-entangled-states),
which explains the rank test in detail.)

Measuring both qubits at this point yields **all four outcomes at 25% each** —
the identical histogram to the state without the `CZ`:

![CZ versus the Bell state](../assets/ch06-cz-vs-bell.png){ width="620" }

The Born rule *squares* amplitudes when it converts them into probabilities, so
`|−½|² = |+½|²`. The sign is there in the state, the entanglement is real, and
a computational-basis measurement reports nothing that distinguishes the two
situations. Telling the two states apart therefore needs a **different
measurement basis** — and this is exactly the trick teleportation relies on in
the next section.

![Coefficient matrices](../assets/ch06-cz-matrices.png){ width="620" }

Two contrast cases round the picture out. `CZ` after a *lone* `H` does nothing
at all, because qubit 1 stays `|0⟩` and the control consequently never fires.
And `CZ` on the Bell state flips the same single sign while leaving the outcome
set `{00, 11}` unchanged, because `CNOT` had already performed the correlating
that the phase flip would have modified.

## Teleportation: moving a state, not a particle

The chapter now reaches its main result. Alice cannot read her qubit, and she
cannot send a copy, because the previous section established that no such copy
can exist. But she can *destroy* the original deliberately and rebuild an
identical state at Bob's end, using correlations the two parties already share:

| Qubit | Whose |
|---|---|
| `q0` | Alice — the state to send |
| `q1` | Alice's half of a Bell pair she shares with Bob |
| `q2` | Bob's half of that pair — the state ends up here |

![The teleportation circuit](../assets/ch06-teleport-circuit.png){ width="620" }

The protocol proceeds in five steps:

1. **Share a Bell pair.** `H(2)`, `CNOT(2,1)` — this is Chapter 5 again, since
   it builds the entangled resource the whole protocol rests on.
2. **Spread the state.** `CNOT(0,1)`, `H(0)`. Alice's state is now spread
   across both her qubits in the form of correlations, rather than remaining
   localized in one register.
3. **Bell-measure.** Alice measures `q0` and `q1`. This destroys `q0` — and
   that destruction is exactly what allows the state to reappear at Bob's end,
   because a quantum state cannot be in two qubits at once.
4. **Send two classical bits.** Over an ordinary channel, at light speed — an
   ordinary message carrying nothing but Alice's two measurement results.
5. **Correct.** Bob applies `X` to `q2` if his bit for `q1` is `1`, and `Z` if
   his bit for `q0` is `1`, undoing whichever of the four possible errors the
   measurement inflicted.

| Alice's message | Bob applies | Bob's qubit when Alice sent <code>\|0⟩</code> | Fidelity |
|---|---|---|---|
| `00` | nothing | <code>\|0⟩</code> | 1.000 |
| `01` | `X` | <code>\|0⟩</code> | 1.000 |
| `10` | `Z` | <code>\|0⟩</code> | 1.000 |
| `11` | `X` then `Z` | <code>\|0⟩</code> | 1.000 |

All four messages occur with probability ¼, and **all four rebuild the state
exactly**. That is the protocol's whole claim, and it holds for every input.

The **fidelity** column below measures how close two states are to one another,
on a scale from 0 to 1. A fidelity of 1.0 means the two states are identical
for every measurable purpose:

| Alice sends | Bob measures | Fidelity |
|---|---|---|
| <code>\|0⟩</code> | P(0) = 1.00 | 1.000 |
| <code>\|1⟩</code> | P(1) = 1.00 | 1.000 |
| <code>\|+⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |
| <code>\|−⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |

![Every message reconstructs the state](../assets/ch06-teleport-fidelity.png){ width="620" }

It is worth noting what fidelity 1.0 does *not* mean here: Bob cannot prepare
`|+⟩` from `|0⟩` by himself, and he cannot prepare `|0⟩` from `|+⟩`. He only
*rebuilds* a state that already existed at Alice's end. Teleportation moves the
**information**, not the particle — Alice's `q0` is gone either way, in every
branch of the protocol.

![Bob's result for each state Alice sends](../assets/ch06-teleport-outcomes.png){ width="620" }

!!! warning "No faster-than-light signalling"
    Step 4 is an ordinary classical message, and it is limited by the speed of
    light in exactly the way any network traffic is. Without those two bits,
    Bob holds a state with a random phase error and no way to identify or fix
    it. That is the "2 classical bits" in the protocol's name, and it is why
    teleportation is *not* superluminal: the quantum part of the transfer does
    nothing useful until the classical message catches up.

??? question "Check yourself — step 3 says Alice's measurement *destroys* `q0`. Isn't the state gone before Bob can rebuild it?"
    `q0` is gone, but the state's information is not: step 2 had already spread
    it across the correlations between all three qubits. After Alice measures,
    Bob's `q2` therefore already holds the sent state with one of four known
    errors — possibly flipped (`X`), possibly phase-flipped (`Z`), possibly
    both. Each of Alice's four equally likely messages names exactly which
    error it is, which is why two bits are enough to repair the state — and
    why they are needed, since without them the error remains unknown and
    uncorrectable.

## From circuits to networks: the repeater

Teleportation moves a state across **one** link. A **repeater** chains links
together so that a state can cross a much longer distance, with a node in the
middle acting as both receiver and sender of successive links:

```
Alice (q0)  ---  link 1  ---  relay (q2)  ---  link 2  ---  Bob (q4)
                        with q1                     with q3
```

![Two chained links across a relay](../assets/ch06-repeater-circuit.png){ width="620" }

The relay is the interesting part of the chain. It **measures** its qubits on
the first link, exactly as Alice does, so it never holds the state cleanly in
between the two links. What travels from end to end is not the state itself: it
is the chain of **correlations** plus *four* classical bits — two sent by
Alice, two sent by the relay.

To show that the state really arrives, Alice starts with a qubit that is
neither `|0⟩` nor `|1⟩`: a rotation with `P(1) = 0.4`. If the relay were only
forwarding classical bits, Bob could observe nothing but 0s and 1s. Instead,
his statistics match hers, for every input:

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

A genuine mixture arrived at Bob, having been rebuilt twice along the way. It
is also worth noting that the relay had to *measure* in order to forward the
state — the state was never in transit as a copy, which is precisely why the
procedure works even though copying is impossible.

!!! note "Where this leads"
    Distance in a quantum network is limited by loss, not by the speed of
    light. Two distinct mechanisms are at work:

    - **Loss** — the state is absorbed or scattered on the way and never
      arrives at the receiving node at all.
    - **Decoherence** — the state arrives, but noise has scrambled its
      superposition and its phase along the way.

    Neither can be repaired, because there is no copy to fall back on. That is
    why a repeater does not amplify a weak signal the way a classical repeater
    does — instead, it *rebuilds* the state at each node from shared
    entanglement plus a classical message. [Chapter 8](ch08-secure-communication.md)
    turns the same idea into secure communication.

## The diagrams

### No-cloning

![The failed clone attempt](../assets/ch06-clone-attempt-circuit.png){ width="420" }

A `CNOT` does not clone: it entangles. The control qubit passes through the
gate untouched, and the target ends up holding a Bell partner rather than a
copy — the visual signature of the no-cloning theorem.

![A perfect clone vs. the CNOT attempt](../assets/ch06-clone-agreement.png){ width="620" }

Two real copies of `|+⟩` would be independent, giving 25% for each outcome; the
attempt is instead perfectly correlated, and the combinations `01`/`10` vanish
from the histogram entirely.

![Fidelity of the CNOT copy](../assets/ch06-clone-fidelity.png){ width="420" }

The attempt is exactly right for the basis states and exactly wrong for
superpositions, which summarizes the theorem in a single plot.

### Controlled-Z

![The H + CZ circuit](../assets/ch06-cz-circuit.png){ width="420" }

![CZ versus the Bell state](../assets/ch06-cz-vs-bell.png){ width="620" }

The first two series are indistinguishable by measurement, even though one is a
product state and the other is entangled — a direct illustration of how much
the computational basis hides.

![Coefficient matrices](../assets/ch06-cz-matrices.png){ width="620" }

The single sign flip is the only change between the two matrices, and it is
sufficient to take the coefficient matrix's rank from 1 to 2.

### Teleportation

![The teleportation circuit](../assets/ch06-teleport-circuit.png){ width="620" }

The `If X` and `If Z` boxes are the classical corrections, driven by Alice's
measurement results and applied to Bob's qubit only where the message calls
for them.

![Every message reconstructs the state](../assets/ch06-teleport-fidelity.png){ width="620" }

![Bob's result for each state Alice sends](../assets/ch06-teleport-outcomes.png){ width="620" }

### Repeater

![Two chained links across a relay](../assets/ch06-repeater-circuit.png){ width="620" }

Two Bell pairs are consumed, two Bell measurements are performed, and four
classical corrections drive the full trip across the relay.

![The statistics survive the trip](../assets/ch06-repeater-consistency.png){ width="620" }

![Expected vs. measured at Bob](../assets/ch06-repeater-counts.png){ width="620" }

## Key takeaways

- A classical network forwards packets by **copying** them; a quantum network
  cannot do the same, because the **no-cloning theorem** forbids copying an
  unknown quantum state.
- A `CNOT` does not clone: it entangles. The copy attempt succeeds on basis
  states and fails on superpositions, and no variant of it covers both.
- `CZ` flips a phase, and the Born rule squares amplitudes — so `CZ` can turn
  a product state into an entangled one **without changing a single
  measurement probability**.
- **Teleportation** moves a state by destroying the original and rebuilding it
  from shared entanglement plus **two classical bits**. It moves information,
  not a particle, and it is not faster than light.
- A **repeater** chains teleportation links; a relay that measures can still
  pass a state on, and the delivered qubit keeps the statistics it started
  with.
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
  — the two-link chain across a relay.
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
    blocks, exactly as one would write them by hand. The numbers come from the
    frame simulator, which computes the same distribution without executing
    control flow. Qubits are addressed by plain index (`q0`, `q1`, ...),
    matching the book's Java samples, so `q0` is the qubit at `q[0]`.
