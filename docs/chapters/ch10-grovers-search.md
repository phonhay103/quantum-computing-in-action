# Chapter 10 — Grover's search algorithm

!!! abstract "In one sentence"
    Given a list with no structure and only a test that recognises the answer,
    Grover finds it in about `(π/4)·√N` steps instead of the classical `N/2` — a
    **quadratic** speed-up, and the best an unordered list allows.

## Unstructured search

The book's example is a small address book and one question — *who is 29 and lives
in Mexico?* There is no sorted key to binary-search, so a classical program can
only look, entry after entry:

| Entry | Name | Age | Country |
|---|---|---|---|
| 0 | Alice | 42 | Nigeria |
| 1 | Bob | 36 | Australia |
| 2 | Eve | 85 | USA |
| 3 | Niels | 18 | Greece |
| **4** | **Albert** | **29** | **Mexico** |
| 5 | Roger | 29 | Belgium |
| 6 | Marie | 15 | Russia |
| 7 | Janice | 52 | China |

The match is at position 4, so the scan takes 5 tries. Shuffle the list and the
target lands at each position equally often, giving an average of
`(1 + 2 + … + 8)/8 = 4.5` tries. That flat 4.5 is the bar Grover has to beat.

![Classical scan: how many tries to find the target](../assets/ch10-classical-tries.png){ width="560" }

## The oracle: a sign, and nothing else

Grover never sees the list. All it gets is an **oracle** that recognises the
answer, and the only thing the oracle may do is *mark* the wanted state with a
**phase flip**:

$$U_w : |x\rangle \longrightarrow (-1)^{[x = w]}\,|x\rangle$$

For two qubits with `|11⟩` marked, that is a diagonal matrix with a single `-1`:

![Grover's oracle: one sign flip, nothing measurable](../assets/ch10-oracle-matrix.png){ width="420" }

A sign on its own is invisible. A global phase means nothing, and measuring `|x⟩`
before and after the oracle returns the same histogram. The whole of Grover's
work is turning this one hidden sign into a large probability.

## Diffusion: reflecting about the mean

The second move is the **diffusion** operator, a reflection of every amplitude
about the average:

$$D = H^{\otimes n}\bigl(2|0\rangle\langle 0| - I\bigr)H^{\otimes n} = 2|s\rangle\langle s| - I$$

Applied after the oracle, it sets each amplitude `a → 2·mean − a`. The marked
state, which the oracle pushed *below* the mean, is the one that flips back up
*above* it; the others sink. Repeat the pair and the marked amplitude grows a
little each round.

## Step by step on two qubits

Two qubits give four states — few enough to print every amplitude after every
round. Mark `|11⟩` and start uniform, every amplitude `1/2`:

| Round | `00` | `01` | `10` | marked `11` |
|---|---|---|---|---|
| after 0 rounds | +0.50 | +0.50 | +0.50 | +0.50 |
| after 1 round | 0.00 | 0.00 | 0.00 | **+1.00** |
| after 2 rounds | −0.50 | −0.50 | −0.50 | +0.50 |

Read it in three moves:

1. **Oracle** flips the sign of the marked amplitude: `+0.50 → −0.50`. The average
   of the four amplitudes drops from `0.50` to `0.25`.
2. **Diffusion** reflects about that average: `0.50 → 2(0.25) − 0.50 = 0` and
   `−0.50 → 2(0.25) + 0.50 = 1`. One round and the marked state holds **all** the
   probability.
3. A **second round** rotates past the answer — back to `1/4` — which is the
   overshoot. Running Grover too long makes it worse.

![Grover on 2 qubits: the marked state takes all the probability](../assets/ch10-step-by-step.png){ width="620" }

## Grover on 64 items

Scale up to six qubits (`N = 64`), mark one state, and each round is a small
rotation of the whole amplitude vector. The probability of the answer follows
`sin²((2k+1)θ)` with `sin θ = 1/√N`:

| Rounds | 0 | 1 | 2 | 3 | 4 | 5 | **6** | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| P(answer) | 0.02 | 0.13 | 0.34 | 0.59 | 0.82 | 0.96 | **1.00** | 0.91 | 0.72 | 0.47 |

![Grover on 64 items: probability rises, then overshoots](../assets/ch10-grover-curve.png){ width="620" }

The peak sits at 6 rounds — `floor((π/4)·√64)` — and a classical scan would take
`32` tries on average. Measured 2000 times, the answer comes back overwhelmingly:

![64 outcomes after 6 rounds: the answer dominates](../assets/ch10-grover-outcomes.png){ width="620" }

![A small Grover circuit](../assets/ch10-grover-circuit.png){ width="620" }

The circuit is the whole loop, repeated: `H` on every qubit once, then an
**oracle / diffusion** pair per round. The `H, X, MCZ, X, H` block at each round
is the reflection about the mean; the single phase flip is the oracle.

## How big is the speed-up?

| Items `N` | Classical (average) | Grover rounds |
|---|---|---|
| 8 | 4.5 | 2 |
| 64 | 32 | 6 |
| 1 000 000 | 500 000 | 785 |

The pattern is `N/2` against `(π/4)·√N`: **quadratic**, not exponential. Doubling
the list multiplies the classical work by four but the quantum work by only about
`√2`. That is the honest size of Grover's gift — real, useful, and modest — and it
is provably the best possible for a list with no structure to exploit.

!!! note "Where the speed-up comes from"
    Grover does not test items in parallel and read out the answers — a measurement
    returns one basis state. It runs the oracle **once per round** on the whole
    superposition and lets *interference* concentrate the probability. The gain is
    a square root because each round is one more rotation of the amplitude vector,
    and the vector only has to rotate a quarter turn to point at the answer.

## The diagrams

### The classical baseline

![Classical scan: how many tries to find the target](../assets/ch10-classical-tries.png){ width="560" }

### The oracle

![Grover's oracle: one sign flip, nothing measurable](../assets/ch10-oracle-matrix.png){ width="420" }

### Step by step

![Grover on 2 qubits: the marked state takes all the probability](../assets/ch10-step-by-step.png){ width="620" }

### Grover on 64 items

![A small Grover circuit](../assets/ch10-grover-circuit.png){ width="620" }

![Grover on 64 items: probability rises, then overshoots](../assets/ch10-grover-curve.png){ width="620" }

![64 outcomes after 6 rounds: the answer dominates](../assets/ch10-grover-outcomes.png){ width="620" }

## Key takeaways

- **Unstructured search** has no sorted key to exploit: classically it costs `N/2`
  tests on average, and there is no better classical way.
- The **oracle** marks the answer with a **phase flip** — `(-1)^[x = w]` — and does
  nothing else. On its own a sign is unmeasurable.
- **Diffusion** (`2|s⟩⟨s| − I`) reflects every amplitude about the mean. Applied
  after the oracle, it lifts the marked amplitude above the mean and pushes the
  others down.
- Each **oracle + diffusion** round rotates the amplitude vector; the answer's
  probability follows `sin²((2k+1)θ)`, `sin θ = 1/√N`.
- The **iteration count matters**: too few rounds leave the probability small, too
  many rotate past the answer. The optimum is about `(π/4)·√N`.
- The speed-up is **quadratic** — `(π/4)·√N` against `N/2` — and no quantum
  algorithm can beat it for an unordered list.

## The code behind this chapter

Four samples, from the classical baseline to the full algorithm:

- [`ch10/search.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/search.py)
  — the ``classicsearch`` and ``quantumsearch`` samples: the address book, the
  linear scan, and a Grover search over the same entries.
- [`ch10/oracle.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/oracle.py)
  — the ``groveroracle`` sample: the phase oracle, built from an explicit
  multi-controlled `Z`, and its matrix.
- [`ch10/step_by_step.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/step_by_step.py)
  — the ``stepbystepgrover`` sample: two qubits, amplitudes after every round.
- [`ch10/grover.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/grover.py)
  — the ``grover`` sample: the diffusion operator, the iteration count, the
  success curve, and the measured outcomes.

Run them all with `make ch10`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch10.grover
```
