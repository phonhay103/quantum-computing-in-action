# Chapter 10 — Grover's search algorithm

!!! abstract "In one sentence"
    Given a list with no structure and only a test that recognises the answer,
    Grover finds it in about `(π/4)·√N` steps instead of the classical `N/2` — a
    **quadratic** speed-up, and the best an unordered list allows.

## The question this chapter answers

Chapter 9 ended with an oracle that could be asked one global question about a
function — constant or balanced — in a single query. This chapter asks the
question every database user actually has, in three steps:

1. **How do you find one wanted item in a list with no structure?** No sorted
   key, nothing to exploit — just a pile of entries and a test that says "yes"
   for exactly one of them. Classically the only plan is to look, entry after
   entry, and that costs `N/2` tries on average.
2. **How can a hidden minus sign become a found item?** On a quantum register
   the test becomes an oracle that may only flip the **sign** of the wanted
   state — and a sign changes no probability at all, so it is invisible to any
   measurement. Grover's answer is a **two-step dance**, oracle then diffusion,
   repeated a counted number of times.
3. **Why must the dance stop on time?** Each round rotates the amplitude vector
   one fixed step toward the answer; past the answer, the same rotation points
   *away* again, so over-rotating *reduces* the success probability.

After this chapter you will be able to:

- say what an **unstructured search** costs classically, and justify the
  `N/2`-on-average baseline;
- explain the oracle as "flip the sign of the marked state — and nothing else",
  and why a sign flip is a **reflection**;
- work Grover's round **by hand on four states**: amplitudes `0.5` each →
  oracle → mean `0.25` → the marked state at `1.0` after a single round;
- explain **diffusion** as "reflect every amplitude about the mean"
  (`a → 2·mean − a`), and why it pushes amplitude *into* the state the oracle
  marked;
- choose the round count — about `(π/4)·√N` — and explain why more rounds
  eventually *hurt*.

You need three things from earlier chapters, each in one line: `H` on every
qubit makes the uniform superposition, every state amplitude `1/√N`
([Chapter 4](ch04-superposition.md)); an oracle is a **reversible** circuit,
and **phase kickback** turns its answer into a sign
([Chapter 9](ch09-deutsch-jozsa.md)); and a program's state can be read after
every step ([Chapter 7](ch07-helloworld-explained.md)) — which is how this
chapter watches every amplitude move.

!!! note "One bit of bookkeeping: amplitudes, signs, labels"
    This chapter prints **amplitudes**, which may be negative, and
    **probabilities**, which are the amplitude squared — so
    `(−1/2)² = 1/4 = (1/2)²`. Basis-state labels read **`q0` first**, left to
    right, the book's order: the marked index `7` on six qubits means
    `q0 = q1 = q2 = 1` and prints as `111000`. And `N` always counts the list:
    `N = 2^n` items for `n` qubits.

## Unstructured search

The book's example is a small address book and one question — *who is 29 and
lives in Mexico?* The frustrating part is not the question but the list: age is
not sorted, country is not sorted, so there is no key to binary-search. A
classical program can only look, entry after entry:

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

Work the scan by hand: Alice — miss. Bob — miss. Eve — miss. Niels — miss.
Albert — hit. The match sits at position 4, so the scan takes **5 tries**.

But 5 is luck, not cost. Shuffle the same list and the target lands at each of
the 8 positions equally often, so the honest classical price is the average
`(1 + 2 + … + 8)/8 = 36/8 = 4.5` tries.

![Classical scan: how many tries to find the target](../assets/ch10-classical-tries.png){ width="560" }

That flat histogram *is* the general rule. With `N` entries the target sits at
position `1, 2, …, N` with equal probability `1/N`, so the expected number of
tries is

$$(1 + 2 + \dots + N)\,/\,N = (N+1)/2 \;\approx\; N/2,$$

and no classical trick beats it, because on an unstructured list each check
rules out exactly one entry. That `N/2` is the bar Grover has to beat.

??? question "Check yourself — the target never moves: it is always Albert at index 4. So where does the 4.5 come from?"
    From the *shuffling*, not the data. In one fixed order you always take
    5 tries — but you might equally have been handed any other order. Averaging
    over all orders puts the target at each position equally often:
    `(1 + 2 + … + 8)/8 = 4.5`. The 4.5 is the price of *not knowing where to
    look*, which is exactly what "unstructured" means.

## The oracle: a sign, and nothing else

Grover never sees the list. All it gets is an **oracle** — Chapter 9's
reversible black box — that recognises the answer, and the only thing it is
allowed to do is mark it:

$$U_w : |x\rangle \longrightarrow (-1)^{[x = w]}\,|x\rangle$$

Read that as a promise made to a clerk: *you may not point at the record; you
may only write a small minus sign on it.* Every state keeps its amplitude; the
marked state alone gets its sign flipped.

Concrete example: two qubits, four states, `|11⟩` marked. The oracle is a
diagonal matrix with a single `-1`:

| Basis state | Sign |
|---|---|
| `00` | +1 |
| `01` | +1 |
| `10` | +1 |
| `11` (marked) | **−1** |

![Grover's oracle: one sign flip, nothing measurable](../assets/ch10-oracle-matrix.png){ width="420" }

Apply it to the uniform state — amplitudes `(0.5, 0.5, 0.5, 0.5)` — and you get
`(0.5, 0.5, 0.5, −0.5)`. Nothing changed size; one direction reversed. That is
why a sign flip is a **reflection**: multiplying one coordinate by `-1` mirrors
that coordinate about zero, the same way a mirror reverses a drawing — same
distance, other side.

And that is the catch: the sign is invisible on its own. Probability is
amplitude squared, and `(−0.5)² = 0.25 = (0.5)²`, so measuring before and after
the oracle returns the *same* histogram. The whole of Grover's remaining work
is turning this one hidden sign into a large probability.

Two remarks on how such an oracle is actually built:

- It must be a **circuit of reversible gates** — Chapter 9's rule; a lookup
  that swallows its input is not allowed. The samples here bracket the marked
  state with `X` gates (mapping it to the all-ones state), flip its phase with
  a multi-controlled `Z`, then undo the brackets — reversible from end to end.
- You will sometimes meet a phase oracle with **one extra qubit**, prepared in
  `|−⟩` so the sign arrives by Chapter 9's phase kickback as `(-1)^f(x)`. Same
  matrix, same promise; the bracketed multi-controlled `Z` used here does the
  job with no extra qubit.

??? question "Check yourself — the oracle recognises the answer. Why can't it just tell us which state is marked?"
    Because "telling" would mean changing amplitudes, and the oracle only
    changes a sign. The sign lives in the amplitude, and every measurement
    reads probability — the amplitude *squared* — where `(−0.5)² = (0.5)²`:
    the minus vanishes. Read the state after the oracle and the chances are
    exactly what they were before it. The sign is real information, but it is
    stored in a form no single measurement can see; Grover's trick is to make
    the *other* states interfere with it until it surfaces.

## Diffusion: reflecting about the mean

The oracle's minus sign would stay hidden forever if Grover did not add a
second move: the **diffusion** operator, whose idea is easier than its formula.
Think of a class where the average score is 7:

- you scored **5** — two points *below* the mean;
- reflecting your score about the mean gives `2·7 − 5 = 9` — two points
  *above* it.

That rule, `a → 2·mean − a`, applied to *every* amplitude at once, is the
diffusion: compute the average of all the amplitudes, then move every amplitude
to the point the same distance on the *other side* of that average. Whatever sat
below the mean is pushed up; whatever sat above it is pulled down.

$$D = H^{\otimes n}\bigl(2|0\rangle\langle 0| - I\bigr)H^{\otimes n} = 2|s\rangle\langle s| - I$$

(The formula says the same thing in fancier clothes: reflect about the uniform
superposition `|s⟩`, which for amplitudes is exactly "reflect about the mean".)

Watch it work on the oracle's output. After the oracle the four amplitudes are
`(0.5, 0.5, 0.5, −0.5)` and the mean is `(0.5 + 0.5 + 0.5 − 0.5)/4 = 0.25`:

| Amplitude | Reflect: `2·mean − a` | Result |
|---|---|---|
| unmarked `+0.5` | `2(0.25) − 0.5` | `0.0` |
| unmarked `+0.5` | `2(0.25) − 0.5` | `0.0` |
| unmarked `+0.5` | `2(0.25) − 0.5` | `0.0` |
| marked `−0.5` | `2(0.25) − (−0.5)` | `1.0` |

Why it works: the reflection pushes amplitude **into** exactly the states that
sit *below* the mean. After the oracle there is only one such state — the
marked one — so it is the only one that rises, and it rises past all the
others. The unmarked states, all *above* the mean, sink together.

The two moves are a pair, and neither does the job alone — see the check below.

??? question "Check yourself — what would the diffusion do if you ran it *first*, before any oracle, on the fresh uniform state?"
    Nothing at all. The amplitudes are `(0.5, 0.5, 0.5, 0.5)` and the mean is
    `0.5`, so every reflection gives `2(0.5) − 0.5 = 0.5`: the uniform state is
    a fixed point of the diffusion. The reflection only amplifies a state that
    sits *away* from the mean — and it is the oracle that puts the marked state
    below it. Neither move alone finds anything; the dance needs both steps.

## Step by step on two qubits

Two qubits give four states — few enough to print every amplitude after every
move, so let us do the whole algorithm by hand, with numbers. Mark `|11⟩` and
start uniform.

**Move 0 — prepare.** `H` on both qubits:

$$|s\rangle = \tfrac{1}{2}\bigl(|00\rangle + |01\rangle + |10\rangle + |11\rangle\bigr)$$

Amplitudes `(0.5, 0.5, 0.5, 0.5)`, mean `0.5`, and `P(11) = 0.25` — the same
chance as guessing.

**Move 1 — the oracle flips one sign.**

$$(0.5,\; 0.5,\; 0.5,\; 0.5) \;\longrightarrow\; (0.5,\; 0.5,\; 0.5,\; -0.5)$$

Still nothing measurable — but the mean has quietly dropped to
`(0.5 + 0.5 + 0.5 − 0.5)/4 = 0.25`, and the marked amplitude now sits *below*
it.

**Move 2 — the diffusion reflects about that mean**, `a → 2(0.25) − a`:

- unmarked: `2(0.25) − 0.5 = 0`;
- marked: `2(0.25) − (−0.5) = 1.0`.

The state is now exactly `|11⟩` — probability `1.00`, measured with certainty.
One round of the dance — one oracle, one diffusion — turned a 1-in-4 guess into
a sure thing:

| Round | `00` | `01` | `10` | marked `11` |
|---|---|---|---|---|
| after 0 rounds | +0.50 | +0.50 | +0.50 | +0.50 |
| after 1 round | 0.00 | 0.00 | 0.00 | **+1.00** |
| after 2 rounds | −0.50 | −0.50 | −0.50 | +0.50 |

![Grover on 2 qubits: the marked state takes all the probability](../assets/ch10-step-by-step.png){ width="620" }

**Why one round sufficed here.** Each round is a small rotation of the whole
amplitude vector by a fixed angle `2θ`, where `sin θ = 1/√N` (here
`sin θ = 1/2`, so `θ = 30°` and a round turns `60°`). The answer's probability
after `k` rounds is `sin²((2k+1)θ)`, and with `N = 4` the arithmetic lands
exactly on `sin²(90°) = 1` after one round — a perfect hit that only the
smallest case allows.

**And a second round overshoots.** Run the same dance again from `(0, 0, 0, 1)`:

1. **Oracle:** the marked amplitude flips, `1.0 → −1.0`, so the vector is
   `(0, 0, 0, −1)` and the mean drops to `(0 + 0 + 0 − 1)/4 = −0.25`.
2. **Diffusion:** unmarked `2(−0.25) − 0 = −0.5`; marked
   `2(−0.25) − (−1.0) = +0.5`.

The marked probability falls from `1` back to `0.25`. The rotation never knew
it had arrived — it just carried on turning, straight past the answer. Running
Grover too long makes it worse.

??? question "Check yourself — one round gives probability 1.00, a certain answer. Why does repeating the *same* round make it worse?"
    Because a round is a fixed rotation, not a homing missile. It turns the
    amplitude vector by the same `60°` every time, and nothing tells it to stop
    once the vector points at the answer. The second round turns *past* the
    answer, and the arithmetic shows where it lands: `(−0.5, −0.5, −0.5, +0.5)`,
    probability `0.25`. More rounds are not more effort spent finding — they
    are more rotation, in a direction that now points away.

## Grover on 64 items

Now the chapter's real experiment: six qubits, `N = 64` states, and state
`index 7` — label `111000`, since `q0 = q1 = q2 = 1` — marked by the oracle.

The dance is the same but the angle is smaller: `sin θ = 1/√64 = 1/8` gives
`θ ≈ 7.18°`, so each round rotates the amplitude vector by about
`2θ ≈ 14.36°`. To point at the answer the vector must turn roughly a quarter
turn — about `90° − θ ≈ 82.8°` — and `82.8 / 14.36 ≈ 5.8`, so the best count is

$$\left\lfloor \tfrac{\pi}{4}\sqrt{N} \right\rfloor
= \left\lfloor \tfrac{\pi}{4}\sqrt{64} \right\rfloor = 6 \text{ rounds}.$$

The simulator confirms it probability by probability (the answer follows
`sin²((2k+1)θ)`):

| Rounds | 0 | 1 | 2 | 3 | 4 | 5 | **6** | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| P(answer) | 0.02 | 0.13 | 0.34 | 0.59 | 0.82 | 0.96 | **1.00** | 0.91 | 0.72 | 0.47 |

![Grover on 64 items: probability rises, then overshoots](../assets/ch10-grover-curve.png){ width="620" }

Two numbers to take away from the experiment:

- after **6 rounds**, `P(answer) = 0.997` — the search is effectively finished,
  against the classical average of **32** checks for the same list;
- run too long and it *un*-finishes: 7 rounds drop to `0.907`, 9 rounds to
  `0.475`. The rotation overshoots, so more rounds are not better rounds.

Measured 2000 times after 6 rounds, the answer comes back overwhelmingly —
`1995` of the `2000` shots returned `111000`:

![64 outcomes after 6 rounds: the answer dominates](../assets/ch10-grover-outcomes.png){ width="620" }

![A small Grover circuit](../assets/ch10-grover-circuit.png){ width="620" }

The circuit is the whole loop made visible: `H` on every qubit once, then one
**oracle / diffusion** pair per round. The `H, X, MCZ, X, H` block at each round
is the reflection about the mean — the same reflection, written with reversible
gates; the single phase flip inside is the oracle.

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

- **Unstructured search** has no sorted key to exploit: classically it costs
  `(N+1)/2 ≈ N/2` checks on average, and no classical method does better.
- The **oracle** marks the answer with a **phase flip** — `(-1)^[x = w]` — and
  does nothing else. A sign flip is a reflection, and it is invisible on its
  own because probability squares the sign away.
- **Diffusion** (`2|s⟩⟨s| − I`) reflects every amplitude about the mean,
  `a → 2·mean − a`. It pushes amplitude into the below-mean states — and after
  the oracle, the marked state is the only one there.
- Each **oracle + diffusion** round is a fixed rotation `2θ` of the amplitude
  vector (`sin θ = 1/√N`); the answer's probability follows
  `sin²((2k+1)θ)`. On four states, `0.5 → 1.0` in a single round.
- The **round count matters**: too few rounds leave the probability small, too
  many rotate past the answer — on 64 items, 6 rounds give `0.997` but 9 give
  `0.475`. The optimum is about `(π/4)·√N`.
- The speed-up is **quadratic** — `(π/4)·√N` against `N/2`, so about `785`
  rounds for a million items against `500 000` checks — and no quantum
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
