# Chapter 9 — Deutsch and Deutsch–Jozsa

!!! abstract "In one sentence"
    If a function is promised to be **constant** or **balanced**, a quantum circuit
    needs only **one** call to its oracle to tell which — where a classical check
    that must be certain can need `2^(n-1) + 1` calls.

## The question this chapter answers

Imagine a black box that computes a function `f`, handed over under one strict
condition: the box may not be opened or examined in any way. The only permitted
interaction is to feed it inputs and read off the outputs it returns. This chapter
asks — and answers — three questions about that box:

1. **How can a quantum circuit "call" a function at all?** The rule established
   in Chapter 7 states that every quantum gate is reversible and that nothing may
   be erased — yet a function such as `AND` discards its inputs, since several
   distinct input pairs collapse onto the same output. The resolution is the
   **oracle**: a reversible circuit that *keeps* the input intact and writes the
   answer onto a spare qubit.
2. **How many calls does it take to learn one *global* fact about `f`?** If `f` is
   promised to be **constant** (the same answer everywhere) or **balanced** (two
   different answers, half each), a classical check may need `2^(n-1) + 1` calls
   before it is *certain* of the verdict. In other words, the classical cost grows
   with the width of the input. The quantum circuit of this chapter needs **one**
   call, whatever the width of the input.
3. **What does that single quantum call actually deliver — and what does it not?**
   Not the `2^n` answers themselves: a measurement returns exactly one outcome.
   It delivers one bit of global information about `f`, and **interference** is
   the mechanism that distills that bit out of the surrounding superposition.

Working through this chapter builds four abilities:

- read the oracle rule `U_f : |x⟩|y⟩ → |x⟩|y ⊕ f(x)⟩` and explain `⊕` as
  *"are the two bits different?"*;
- trace the whole Deutsch circuit **in amplitudes**, for a balanced and for a
  constant function, and see where each sign comes from;
- explain **phase kickback**: why the spare qubit must start in `|−⟩`, and how the
  value `f(x)` moves into a *sign* on each branch;
- state the Deutsch–Jozsa verdict — all zeros means constant — and the classical
  `2^(n-1) + 1` bound it beats.

Three results from earlier chapters are used throughout, and each can be stated
in a single line: `H` puts a qubit into an even 50/50 superposition
([Chapter 4](ch04-superposition.md)); `CNOT` flips its target whenever its
control is `1` ([Chapter 5](ch05-entanglement.md)); and every quantum gate is
reversible, with the **Toffoli** as the reversible `AND`
([Chapter 7](ch07-helloworld-explained.md)).

!!! note "One bit of bookkeeping: notation and bit order"
    A label such as `01` always reads **`q0` first**, left to right — the book's
    order, as in [Chapter 7](ch07-helloworld-explained.md). Because every circuit
    below is read in exactly this convention, it is worth fixing before any wire
    is examined. Three symbols are used all chapter:

    - `⊕` is **XOR**: *are the two bits different?* `0⊕0 = 0`, `0⊕1 = 1`,
      `1⊕0 = 1`, `1⊕1 = 0` — addition modulo 2.
    - `|−⟩ = (|0⟩ − |1⟩)/√2` is the *minus* superposition: same 50/50 chances as
      `|+⟩ = (|0⟩ + |1⟩)/√2`, but the two branches carry opposite **signs**.
    - `(-1)^f(x)` is `+1` when `f(x) = 0` and `-1` when `f(x) = 1` — a sign that
      each branch of a superposition can carry.

## Every gate is reversible

A quantum circuit is built from **reversible** gates: apply one, and it can always
be run backwards, recovering exactly what was there before. In this setting
reversibility is not a stylistic preference but a mechanical property — a
reversible gate carries all of its input information through to the output, so the
input can be reconstructed from the output alone. The constraint was stated in
Chapter 7; here it becomes the design rule for the whole chapter, so it is worth
seeing once more with numbers.

The simplest reversible operation is an `X` gate applied twice:

![Two X gates](../assets/ch09-reversible-circuit.png){ width="360" }

$$|0\rangle \xrightarrow{\;X\;} |1\rangle \xrightarrow{\;X\;} |0\rangle$$

One flip, then another to undo it. The two flips cancel exactly because `X` erases
nothing: knowing that the qubit now holds `1` reveals precisely what it held
before, namely `0`. Run the circuit and measure: the outcome is `0` with
certainty, on every repetition. Nothing about the outcome depends on how many
times the pair is applied — the two gates cancel as a unit — and this ability
to undo an operation is exactly the guarantee that every oracle later in the
chapter must provide.

Classical logic is not so careful. An `AND` gate takes two bits in and returns
one:

| a | b | a AND b | |
|---|---|---|---|
| 0 | 0 | 0 | |
| 0 | 1 | 0 | three inputs, one output |
| 1 | 0 | 0 | |
| 1 | 1 | 1 | |

Reading the first three rows shows the difficulty: three *different* inputs share
the same output `0`. After the gate has run, the output does not say which input
went in — the information is gone, and no circuit can bring it back. It follows
that `AND` cannot be run in reverse, and consequently that a quantum circuit
cannot use it. The culprit is erasure, not the particular table: any operation
whose output no longer determines its input discards information in the same
way.

??? question "Check yourself — `AND` is banned, yet Chapter 7 computed `a AND b` with a Toffoli gate. Why is that allowed?"
    The permission follows because the Toffoli never throws anything away. It
    writes `a AND b` onto a *third* qubit and leaves `a` and `b` exactly where
    they were: `Toffoli(a, b, 0)` gives `(a, b, a AND b)`. Given the output, the
    inputs can be read straight off it, so the operation runs backwards. The rule
    is not "no `AND` ever" — it is "no *erasing*". Pay one extra qubit, keep
    everything, and even `AND` becomes a legal quantum gate.

## Oracles: reversible black boxes

A quantum algorithm never sees the function it works on — it sees an **oracle**:
the reversible circuit that evaluates it. The oracle is the interface between an
ordinary function and the reversible world of quantum gates: inside it the
function is computed as usual, while at the boundary every trace of the
computation is preserved. What does a *callable* function look like when it has
to obey the "nothing is erased" rule? The answer is worked out here on the one
function whose oracle is a single gate.

Take `f(x) = x` (one of the two balanced one-bit functions). Its oracle is one
`CNOT`, with the input `x` on `q0` and a spare register `y` on `q1`:

![A balanced oracle: one CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

Run it on all four input pairs and watch the spare register: the record obtained
is the table below. The rule is `y ⊕ f(x)`, and `⊕` answers one plain question:
*are the two bits different?*

| x | y | y ⊕ f(x) | what happened |
|---|---|---|---|
| 0 | 0 | 0 | `f(0) = 0`: the spare stays |
| 0 | 1 | 1 | `f(0) = 0`: the spare stays |
| 1 | 0 | 1 | `f(1) = 1`: the spare flips |
| 1 | 1 | 0 | `f(1) = 1`: the spare flips back |

The input `x` comes back untouched in every row; the answer is folded into the
spare register. Only *now* is the general rule stated:

$$U_f : |x\rangle\,|y\rangle \longrightarrow |x\rangle\,|y \oplus f(x)\rangle$$

Set `y = 0` and the spare register holds `f(x)`; set `y = 1` and it holds
`NOT f(x)`. In either configuration nothing is erased — the function has been
evaluated and, at the same time, every input has been preserved, which is
precisely the double bookkeeping the quantum rule demands.

Why is this reversible? Because XOR undoes itself: `y ⊕ f(x) ⊕ f(x) = y`. Run the
same oracle twice and the spare register is back to its original value — the
oracle is its own inverse. That is exactly what the reversibility rule demands,
and it is why `U_f` is a legal quantum gate. This self-inverse quality is not an
accident of the function chosen here: it follows from the XOR construction
itself, and every oracle built on the same rule inherits it.

## The four one-bit functions

There are only four functions of one bit — two answers through two inputs — and
they split into two families. Enumerating them takes one short table, and it is
worth doing, because every argument in the rest of this chapter runs on exactly
this list:

| Function | f(0) | f(1) | Kind | Oracle circuit |
|---|---|---|---|---|
| constant 0 | 0 | 0 | constant | nothing |
| constant 1 | 1 | 1 | constant | `X` on `y` |
| balanced: `f(x) = x` | 0 | 1 | balanced | `CNOT(x, y)` |
| balanced: `f(x) = NOT x` | 1 | 0 | balanced | `X` on `y`, then `CNOT(x, y)` |

![The four oracle matrices](../assets/ch09-oracle-matrices.png){ width="620" }

Each matrix is a **permutation matrix**: exactly one `1` in every row and every
column, every other entry `0`. That is what reversibility looks like as a matrix —
a reshuffling of the basis states with nothing lost, so it can always be shuffled
back.

The two families differ in exactly one way: does the input change the answer? A
**constant** function ignores `x` completely (`f(0) = f(1)`); a **balanced**
function answers differently on `0` and on `1` (`f(0) ≠ f(1)`). That question —
*"does the input matter?"* — is worth keeping in mind throughout, because it is
the entire thing the algorithms below manage to ask with a single query. That question is notably a *global* one: it
does not ask for the value of `f` at either input, only whether the two values
move together.

## The trick: phase kickback

The oracle writes its answer onto the spare register — but a caution is in order:
if the spare sits in a plain `|0⟩` or `|1⟩` while the input is in superposition,
*measuring* the spare to read the answer would destroy the superposition.
Deutsch's circuit needs the answer to show up somewhere that does not collapse
the branches. The trick is to prepare the spare qubit in `|−⟩`, so that the
oracle's flip turns into a *sign*.

Start with the smallest fact, verified by direct multiplication. `X` swaps
`|0⟩` and `|1⟩`, so applied to `|−⟩`:

$$X\,|-\rangle = X\,\frac{|0\rangle - |1\rangle}{\sqrt{2}}
= \frac{|1\rangle - |0\rangle}{\sqrt{2}} = -\,\frac{|0\rangle - |1\rangle}{\sqrt{2}} = -\,|-\rangle$$

Flip both branches of `|−⟩` and the result is `|−⟩` back again, **times minus
one**. Nothing visible changed — the 50/50 chances are the same — but the state
picked up a sign. In other words, the flip did not leave the quantum system; it
was recorded in the only place a measurement cannot destroy it, the relative
phase.

Now apply the oracle to `|x⟩|−⟩` for a definite `x`. The oracle flips the spare
register exactly when `f(x) = 1`, and a flip on `|−⟩` is a multiplication by
`-1`:

- `f(x) = 0`: no flip, `|x⟩|−⟩ → |x⟩|−⟩` — sign `(-1)^0 = +1`;
- `f(x) = 1`: one flip, `|x⟩|−⟩ → |x⟩·(-|−⟩) = -|x⟩|−⟩` — sign `(-1)^1 = -1`.

$$U_f\,|x\rangle|-\rangle = (-1)^{f(x)}\,|x\rangle|-\rangle$$

Worked on the balanced oracle `f(x) = x` with input `1`: the `CNOT` sees
`x = 1`, flips the spare register, and `|1⟩|−⟩` comes out as `-|1⟩|−⟩`. The value
`f(1) = 1` is no longer a bit sitting on a wire — it has *moved into the sign* of
the branch. That is **phase kickback**: the answer kicks back up into the phase
of the input register, where the superposition survives. The information is
relocated rather than destroyed — placed exactly where the final Hadamard can
still convert it into a readable bit.

??? question "Check yourself — why must the spare qubit start in `|−⟩` and not `|+⟩`?"
    Because `X` does different things to the two. On `|−⟩` a flip shows up as a
    sign: `X|−⟩ = -|−⟩`, so `f(x) = 1` leaves a visible `(-1)^f(x)` on the
    branch. On `|+⟩` the flip is invisible: `X|+⟩ = |+⟩` — swapping `|0⟩` and
    `|1⟩` in `(|0⟩ + |1⟩)/√2` returns the same state, plus nothing. With the
    spare in `|+⟩`, the oracle's action is `|x⟩|+⟩ → |x⟩|+⟩` whether `f(x)` is
    `0` or `1`, and no later gate can tell the two cases apart. The entire
    algorithm lives in that one minus sign, and `|−⟩` is the only state that
    carries it.

## The Deutsch algorithm

Deutsch's problem takes the following form: one of the four oracles above is
handed over, sealed, and the only question asked is *which family* it belongs to
— **constant** or **balanced**. Neither `f(0)` nor `f(1)` is requested; only
whether the two are equal matters. Nothing more specific is at stake, and this
restriction is what makes a single query meaningful: the question has been
trimmed to the size of one bit. Only the oracle's internals vary from one
problem instance to another; the surrounding operations — preparation,
superposition, interference, measurement — remain fixed.

Classically this needs both inputs looked at: query `f(0)`, query `f(1)`,
compare — two lookups, and there is no way around them, because one classical
call reveals nothing about the other input. Quantumly, **one** query is enough, and the bulk of this chapter is spent on
explaining why: the mechanism is interference, funnelled through a single
final Hadamard.

![The Deutsch circuit](../assets/ch09-deutsch-circuit.png){ width="460" }

The circuit, gate by gate, with `q0` the input register and `q1` the spare
register:

1. `X(1)` — the spare register becomes `|1⟩`;
2. `H(0), H(1)` — both registers enter superposition, `q1` landing in `|−⟩`;
3. the oracle — **one** evaluation of `f`, on both inputs at the same time;
4. `H(0)` — the two branches are brought together to interfere;
5. measure `q0`.

### The balanced case, `f(x) = x`, in amplitudes

Every register starts at `|0⟩`, so the two-qubit state is `|00⟩`. Each step can
now be followed in detail — these are the exact amplitudes the simulator
reports:

**Step 1 — `X(1)`.** The spare register flips: `q1 = 1`, the input is untouched.

$$|00\rangle \;\xrightarrow{\;X(1)\;}\; |0\rangle|1\rangle$$

**Step 2 — `H(0), H(1)`.** `q0` becomes `|+⟩`, and `q1` — a `|1⟩` under a
Hadamard — becomes `|−⟩`:

$$|0\rangle|1\rangle \;\xrightarrow{\;H,H\;}\;
\frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes \frac{|0\rangle - |1\rangle}{\sqrt{2}}
\;=\; \tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)$$

Four basis states, amplitude `±1/2` each, probability `1/4` each. The two
branches of `q0` are the `|0…⟩` pair and the `|1…⟩` pair. At this point the
oracle has not yet acted: both input values are present at once, waiting for
step 3 to mark them.

**Step 3 — the oracle (a `CNOT` here).** It acts on each branch separately,
XOR-ing `f(x)` onto the spare register: `|00⟩→|00⟩`, `|01⟩→|01⟩`, `|10⟩→|11⟩`,
`|11⟩→|10⟩`:

$$\tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)
\;\xrightarrow{\;U_f\;}\;
\tfrac{1}{2}\left(|00\rangle - |01\rangle - |10\rangle + |11\rangle\right)$$

Collect the terms and the kickback is plain to see: the state is now

$$\frac{|0\rangle - |1\rangle}{\sqrt{2}} \otimes |-\rangle$$

The `q0` register — which was `|+⟩` — is now `|−⟩`. The branch `x = 0` carries
`(-1)^f(0) = +1` and the branch `x = 1` carries `(-1)^f(1) = -1`; the input
register's *sign* is now the function's answer.

**Step 4 — `H(0)`.** The Hadamard turns the sign difference into a bit
difference: `H|+⟩ = |0⟩` and `H|−⟩ = |1⟩`:

$$\frac{|0\rangle - |1\rangle}{\sqrt{2}} \otimes |-\rangle
\;\xrightarrow{\;H(0)\;}\; |1\rangle \otimes |-\rangle$$

**Step 5 — measure `q0`:** it reads `1` with probability 1.00. Verdict:
**balanced**, after one query.

### The constant-0 case, in amplitudes

Same start, same first two steps — the state after step 2 is identical. But the
constant-0 oracle is the empty circuit, so step 3 changes nothing:

$$\tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)
\;\xrightarrow{\;U_f\;}\;
\tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)$$

Both branches of `q0` still carry `+1 = (-1)^f(0) = (-1)^f(1)` — the signs
agree. Step 4 gives `H|+⟩ = |0⟩`, so the state becomes `|0⟩ ⊗ |−⟩`, and the
measurement reads `0` with probability 1.00. Verdict: **constant**. The
preparation is identical in the two runs, so whatever separates the families
must be contributed by the oracle in step 3 — and for constant 0 that
contribution is nothing at all.

The other two functions behave the same way through their family:

- **constant 1** — the oracle is an `X` on the spare register, which turns
  `|−⟩` into `-|−⟩`. Every branch flips sign, so the whole state is multiplied
  by `-1`. That is a *global* phase — invisible to any measurement — and after
  the final `H(0)` the qubit reads `0` all the same.
- **`f(x) = NOT x`** — the branch `x = 0` flips sign (since `f(0) = 1`), the
  branch `x = 1` does not. The state after the oracle is
  `-|−⟩ ⊗ |−⟩` — the same as the balanced case up to an invisible global sign —
  and the measurement reads `1`.

| Function | f(0) | f(1) | Branch signs | measured q0 | Verdict |
|---|---|---|---|---|---|
| const 0 | 0 | 0 | `+1, +1` | 0 | constant |
| const 1 | 1 | 1 | `-1, -1` | 0 | constant |
| f(x) = x | 0 | 1 | `+1, -1` | 1 | balanced |
| f(x) = NOT x | 1 | 0 | `-1, +1` | 1 | balanced |

![One query: constant measures 0, balanced measures 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

**Why it works, in words.** The oracle does not hand over `f`'s values — it hands
over their *signs*, one per branch, thanks to the `|−⟩` spare register. Equal
signs (constant) mean the two branches still interfere the way `|+⟩` does, and
`q0` returns to `|0⟩`. Opposite signs (balanced) mean the branches interfere
*the other way*, exactly as `|−⟩` does, and `q0` ends at `|1⟩`. The final
Hadamard is the translator: it converts a difference of signs — which no
measurement can read directly — into a difference of bits, which one measurement
settles with certainty. The verdict is thus a property of the whole interference
pattern, not of any single amplitude; nothing in the outcome says anything
beyond which family the sealed oracle belongs to.

??? question "Check yourself — constant 1 multiplies the *whole* state by `-1`. Why doesn't the measurement notice?"
    A sign in front of the entire state is a **global phase**: every possible
    measurement outcome gets multiplied by the same `-1`, and probabilities use
    `|amplitude|²`, which erases it. `|-0⟩` and `|0⟩` measure identically. What a
    measurement *can* notice is a *relative* sign — one branch negative, the
    other positive — because then the branches cancel or reinforce each other
    when they meet at the final Hadamard. Constant functions only ever produce
    global signs; only a balanced function can put `+1` on one branch and `-1`
    on the other. That is precisely the line the algorithm draws.

## Deutsch–Jozsa: one query for any `n`

The generalisation widens the input: `f : {0,1}^n → {0,1}`, still sealed in an
oracle, still with a promise — **constant** (the same answer on every one of the
`2^n` inputs) or **balanced** (`0` on exactly half of them, `1` on the other
half). The promise is broader in scale but not in kind: constant still means one
answer everywhere, and balanced still means a 50/50 split — now over the
`2^n` inputs instead of two. The circuit is Deutsch's with more wires:

![Deutsch–Jozsa for n = 3](../assets/ch09-dj-circuit.png){ width="620" }

1. `X` on the ancilla (the spare register, index `n`); `H` on all `n + 1` qubits;
2. the oracle is run **once** — on all `2^n` inputs at the same time;
3. `H` on the `n` input qubits;
4. measure the input register.

### A worked case: `n = 2`, constant versus balanced

Take `n = 2`, so the input register holds `q0 q1` and the ancilla is `q2`. This
case is small enough to track by hand, and the hand computation matches the
simulator exactly. After step 1 the input register is an even superposition of
all four inputs and the ancilla is in `|−⟩`; factored out, the state is

$$\frac{1}{2}\left(|00\rangle + |01\rangle + |10\rangle + |11\rangle\right) \otimes |-\rangle$$

Each input branch has amplitude `1/2`. For a balanced function the signs come in
equal measure — exactly half `+1`, exactly half `-1` — a restatement of the
promise that will matter directly once the signs are summed. Now comes the
oracle, and the answer lands in the branch signs `(-1)^f(x)`:

- **constant 0** — nothing happens; all four signs stay `+1`:

  $$\frac{1}{2}\left(|00\rangle + |01\rangle + |10\rangle + |11\rangle\right) \otimes |-\rangle$$

- **balanced, the parity** `f(x) = q0 ⊕ q1` — with `f(00) = 0`, `f(01) = 1`,
  `f(10) = 1`, `f(11) = 0` the signs become `+1, -1, -1, +1`:

  $$\frac{1}{2}\left(|00\rangle - |01\rangle - |10\rangle + |11\rangle\right) \otimes |-\rangle$$

Step 3 applies `H` to both input qubits, and every branch contributes to every
outcome with a sign. The amplitude of the all-zero outcome `|00⟩` is the **sum
of the branch signs**, scaled:

$$\text{amplitude of } |00\rangle \;=\; \frac{1}{2^n} \sum_x (-1)^{f(x)}$$

Evaluate it with the numbers above:

- **constant**: `(1/4)(+1 +1 +1 +1) = 4/4 = 1` → `P(00) = 1`. (Constant 1 gives
  `(1/4)(-1 -1 -1 -1) = -1` — amplitude `-1`, probability still 1.)
- **balanced**: `(1/4)(+1 -1 -1 +1) = 0` → `P(00) = 0`.

And the simulator agrees: the constant oracle measures `00` with probability
1.00, while the parity oracle measures `11` with probability 1.00 and **never**
`00`. The verdict rule, for any `n`:

> **All zeros means constant; anything else means balanced.**

| n | Oracle | P(0…0) | Verdict | Classical worst case |
|---|---|---|---|---|
| 1 | constant 0 | 1.00 | constant | 2 |
| 1 | constant 1 | 1.00 | constant | 2 |
| 1 | balanced | 0.00 | balanced | 2 |
| 2 | constant 0 | 1.00 | constant | 3 |
| 2 | constant 1 | 1.00 | constant | 3 |
| 2 | balanced | 0.00 | balanced | 3 |
| 3 | constant 0 | 1.00 | constant | 5 |
| 3 | constant 1 | 1.00 | constant | 5 |
| 3 | balanced | 0.00 | balanced | 5 |

![n = 2: a constant oracle returns 00, a balanced one never does](../assets/ch09-dj-outcomes.png){ width="620" }

### The classical cost, in words

Why might a classical check need `2^(n-1) + 1` calls? Because a balanced function
is allowed to agree with a constant one for a *long* time: it answers `0` on
exactly half of its inputs, so it can keep saying the same thing for
`2^(n-1)` calls in a row and still be balanced. The moment two *different*
answers appear, the case is settled — the function is balanced. But to conclude
**constant**, the queries must continue until more than half of the inputs have
agreed: after `2^(n-1) + 1` identical answers, a balanced function has no places
left to hide, because its agreeing half is only `2^(n-1)` inputs. Half, then one
more: either that one extra query finds the disagreement, or it rules balanced
out. For `n = 1, 2, 3` that is `2, 3, 5` calls — and for `n = 10` it is already
`513`. The quantum cost stays at **one** query no matter how wide the input is. In
other words, the classical bound is not a penalty for carelessness; it is the
exact price of demanding a *certain* verdict under the promise.

!!! note "Quantum parallelism, and what it is not"
    The oracle really does evaluate `f` on all `2^n` inputs in a single pass —
    that is **quantum parallelism**. But those values cannot all be read out: a
    measurement returns one basis state. What the circuit extracts is not the
    answers but a single bit of **global** information about `f` (here, its
    constancy). Interference is what turns the parallel evaluation into that bit,
    and it is why quantum speed-ups are about *questions*, not about computing
    everything at once.

??? question "Check yourself — the oracle evaluated `f` on all `2^n` inputs. Why doesn't the measurement hand you all `2^n` answers?"
    Because a measurement returns **one** basis state, sampled according to the
    probabilities — reading the register destroys the superposition, and the
    other branches' information dies with it. The algorithm never tries to read
    the answers individually. Instead the final Hadamards make all `2^n` branches
    *vote* on one outcome — `|0…0⟩` — and the vote's tally (`2^n` for constant,
    `0` for balanced) is a property of `f` as a whole. One query buys one global
    bit, not `2^n` local ones; the speed-up works because the question only ever
    needed that one bit.

## The diagrams

### Reversibility

![Two X gates](../assets/ch09-reversible-circuit.png){ width="360" }

`X` applied twice returns the qubit to `|0⟩` with certainty: the smallest circuit
that undoes itself, and the rule every oracle must obey.

### Oracles

![A balanced oracle: one CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

The oracle for `f(x) = x`: input `x` on `q0`, spare register `y` on `q1`, one
`CNOT`.

![The four oracle matrices](../assets/ch09-oracle-matrices.png){ width="620" }

Four permutation matrices — one `1` per row and column. Constant oracles shuffle
nothing (or swap within the spare register); balanced oracles swap across the
input's value.

### Deutsch

![The Deutsch circuit](../assets/ch09-deutsch-circuit.png){ width="460" }

`X(1)` prepares the spare register, the Hadamards make `|+⟩|−⟩`, the oracle kicks
the sign back onto `q0`, and the final `H(0)` reads it out.

![One query: constant measures 0, balanced measures 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

P(q0 = 1) for the four one-bit functions: exactly 0 for both constant ones,
exactly 1 for both balanced ones.

### Deutsch–Jozsa

![Deutsch–Jozsa for n = 3](../assets/ch09-dj-circuit.png){ width="620" }

The same circuit, three input wires wide: Hadamards, one oracle pass, Hadamards
on the input register.

![n = 2: a constant oracle returns 00, a balanced one never does](../assets/ch09-dj-outcomes.png){ width="620" }

The `n = 2` measurement distributions: the constant oracle returns `00`, while
the balanced parity oracle returns `11` — and `00` is impossible. The all-zero
outcome is the linchpin of the verdict, which is why the entire test can be
phrased about it alone.

## Key takeaways

- Every quantum gate is **reversible**; `AND`, which erases its inputs, is
  banned. The reversible stand-in is the **Toffoli** gate: pay one extra qubit,
  keep the inputs, and the operation runs backwards.
- An **oracle** evaluates a function without erasing:
  `U_f : |x⟩|y⟩ → |x⟩|y ⊕ f(x)⟩`, with `⊕` meaning *are the two bits different?*.
  It is its own inverse, so it is a legal quantum gate.
- A one-bit function is **constant** (`f(0) = f(1)`) or **balanced**
  (`f(0) ≠ f(1)`); there are four of them, each with a one-gate oracle.
- **Phase kickback**: with the spare in `|−⟩`, the oracle's flip becomes a sign,
  `U_f|x⟩|−⟩ = (-1)^f(x)|x⟩|−⟩` — the value of `f` moves into the phase. With the
  spare in `|+⟩` the flip is invisible, and nothing can be extracted.
- **Deutsch** reads that sign with one final Hadamard: equal signs (constant)
  measure `0`, opposite signs (balanced) measure `1` — one query, with
  certainty.
- **Deutsch–Jozsa** scales it to `n` bits: the amplitude of `|0…0⟩` is
  `(1/2^n) Σ_x (-1)^f(x)` — `±1` for constant, `0` for balanced — so *all zeros
  means constant*, and one query settles it where a classical check may need
  `2^(n-1) + 1`.
- The algorithm does not read the `2^n` answers; it extracts one **global** bit —
  *does the input matter at all?* — through interference.

## The code behind this chapter

Four samples, extending from the underlying rule up to the full algorithm:

- [`ch09/reversible.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/reversible.py)
  — the ``reversibleX`` sample: `X·X = I`, and why `AND` cannot be an oracle.
- [`ch09/oracles.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/oracles.py)
  — the four one-bit functions, their circuit oracles and matrices, plus the
  `n`-bit oracles for Deutsch–Jozsa.
- [`ch09/deutsch.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutsch.py)
  — the Deutsch circuit, traced in amplitudes, and its one-query classification.
- [`ch09/deutschjozsa.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutschjozsa.py)
  — the general algorithm, the all-zero test, and the classical comparison.

Run them all with `make ch09`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch09.deutschjozsa
```
