# Chapter 7 — Our HelloWorld, explained

!!! abstract "In one sentence"
    A quantum program is not a black box: it is an ordered list of **steps**, and
    the state it produces can be read after *every* one of them — which is all
    "running a circuit" ever means. The chapters that follow only ever add steps
    to such a list; the picture of execution laid out here does not change.

## The question this chapter answers

Chapter 2 asked the simulator for a random bit and got one, in a single call:
one line of code returned a result without exposing anything about the machinery
that produced it. From the outside, the call looked like an indivisible act. This
chapter opens that call up and asks the two questions that a programmer
ultimately has to ask about any piece of apparent magic:

1. **What actually ran?** It was not a function call in the ordinary sense. It
   was a *program*: an ordered list of **steps**, where each step holds the
   gates that act at the same time. In other words, what the simulator executes
   is not a single indivisible operation but a structured schedule of
   concurrent operations, and that structure has a name that can be written
   down and inspected. This is what "a quantum circuit" has meant all along.
2. **Can the running process be looked into?** Yes. A simulator holds exactly
   one object — the **state** — from the first gate to the last, and that
   object remains available at every intermediate moment rather than being
   discarded as soon as a gate has been applied. Consequently, "debugging"
   amounts to nothing more than reading that state after each step, in the
   same way a variable is printed in the middle of an ordinary loop; no
   special instrumentation is required.

Having opened the box this far, the chapter puts it to real work:
**arithmetic**. Adding numbers is the classic first test of any computing
model, and the choice is deliberate: addition is familiar enough that a result
can be verified by hand, yet structured enough to expose what the model can and
cannot express. A quantum circuit can add — but under one strange rule that
shapes everything that follows: *a quantum gate is never allowed to erase
information.*

After this chapter, the following abilities will have been established:

- a circuit diagram can be read as a program: which gate touches which qubit,
  and in which step;
- the state after each step can be written down **in numbers**, not merely
  observed at the end;
- it can be explained why `CNOT` adds "modulo 2" (`1 + 1 = 0`), and precisely
  what gets lost in the process;
- the **Toffoli** gate can be explained, together with how it recovers that
  loss, so that `1 + 1 = 2` holds after all.

Three results from earlier chapters are required, and each is condensed into a
single line here: `H` puts a qubit into an even 50/50 superposition, which is
the subject of [Chapter 4](ch04-superposition.md); `CNOT` flips a target qubit
when its control is `1`, the gate examined in detail in
[Chapter 5](ch05-entanglement.md); and an *unknown* value cannot be copied — it
can only be entangled, as demonstrated in
[Chapter 6](ch06-quantum-networking.md).

!!! note "One bit of bookkeeping: bit order"
    A label such as `1001` in this chapter always reads **`q0` first**, left to
    right: `q0 q1 q2 q3`. So `1001` means `q0 = 1, q1 = 0, q2 = 0, q3 = 1` — the
    book's order, matching its `Qubit[0] … Qubit[3]`. It is worth noting that
    Qiskit itself prints the highest index on the left, the opposite
    convention; every result shown here has therefore already been flipped into
    the book's order, and no further adjustment is needed by the reader.

## A program is a list of steps

The book's ``randombit`` sample is a four-qubit program with exactly two steps
— small enough to be written out in full and checked by hand at every
intermediate moment, which is exactly what the following paragraphs do:

```text
step 1:  H(0), X(3)
step 2:  CNOT(0, 1)
```

![The four-qubit program](../assets/ch07-randombit-circuit.png){ width="460" }

The circuit should be read gate by gate, and after each gate the same question
asked: "what is the state now?" Nothing more is needed to follow the program
from beginning to end.

**Start.** Every qubit begins in `|0⟩`, so the four-qubit state is the single
basis state `|0000⟩` — certainty, probability 1.00. At this point the register
carries no randomness whatsoever; every possible outcome other than `0000` has
probability zero.

**Step 1 — `H(0)` and `X(3)`.** Two gates act at the same time, on different
qubits, and neither of them depends on the other's outcome:

- `H` on `q0` splits it into `( |0⟩ + |1⟩ )/√2` — the even 50/50 mix, the
  random bit that Chapter 2 obtained. It does not *decide* anything; it merely
  makes both futures equally likely, and the actual choice is left to the
  eventual measurement.
- `X` on `q3` flips that qubit to a definite `|1⟩`. The program is allowed to
  set values it already knows — `X` is just a controlled, reversible "set to
  1", and since it assigns no new information it violates no quantum rule.
- `q1` and `q2` are not in this step at all, so they do not move: their
  amplitudes remain exactly what they were at the start.

So after step 1 the whole register is

$$\frac{1}{\sqrt{2}}\,(|0001\rangle + |1001\rangle)$$

Two basis states, amplitude `1/√2` each, probability `1/2` each. Read the
labels in the book's order: `0001` is "`q0=0` and `q3=1`", `1001` is "`q0=1`
and `q3=1`". Only `q0` differs between them — exactly the qubit the `H`
acted on — while the trailing `1` in both labels records the `X` on `q3`.

**Step 2 — `CNOT(0, 1)`.** This gate looks at its control `q0` and flips its
target `q1` when that control is `1`. It acts on each branch separately, and it
is deterministic within each branch:

- branch `0001`: the control `q0` is `0`, so the condition is not met and
  nothing happens to the target;
- branch `1001`: the control `q0` is `1`, so the condition is met and `q1`
  flips `0 → 1`, giving `1101`.

$$\frac{1}{\sqrt{2}}\,(|0001\rangle + |1001\rangle)
\;\xrightarrow{\;\mathrm{CNOT}\;}
\frac{1}{\sqrt{2}}\,(|0001\rangle + |1101\rangle)$$

Still two branches, each still probability `1/2`. In other words, `CNOT` did
not make anything *more* random; what it did do is *correlate* `q1` with `q0`,
so that the value of one becomes a reliable indicator of the value of the
other.

??? question "Check yourself — four qubits have sixteen possible outcomes. Why do only two appear?"
    Sixteen is only the count of *possible* labels; a program reaches only the
    states its gates create. Here `q3` is pinned to `1` by `X`, `q2` is never
    touched and stays `0`, and the only split in the whole program is the one
    `H` made on `q0` — two branches. `CNOT` then maps each branch to exactly
    one new branch; it never splits anything. Two branches in, two branches
    out: `0001` and `1101`.

## Reading the state after every step

A histogram at the *end* tells what a program returns; it cannot tell *where*
each qubit changed along the way, and that is usually the interesting question
when a program misbehaves. The book's ``randombitdebug`` sample answers it by
drawing the probability vector after **every** step — and because the
simulator's state is a single object all the way through, this is not a
concession or a trick: it is just "print the variable" at three moments,
exactly as one would do while debugging classical code.

Here is the same program with a boundary drawn after each step:

![The program with step boundaries](../assets/ch07-debug-circuit.png){ width="460" }

First the full probability vector, keeping only the basis states that can
occur — states that never acquire a nonzero amplitude are omitted for brevity:

| Step | Basis state `q0 q1 q2 q3` | Probability |
|---|---|---|
| start | `0000` | 1.00 |
| `H(0), X(3)` | `0001` | 0.50 |
| | `1001` | 0.50 |
| `CNOT(0, 1)` | `0001` | 0.50 |
| | `1101` | 0.50 |

![Basis-state probabilities after each step](../assets/ch07-debug-steps.png){ width="620" }

How to read it: the table is the whole state at three moments, and each change
between moments is a change made by a specific step. At the start there is one
row, because the register is in one definite state. After step 1 there are two
rows — the `H` split the register into two futures, each as likely as the
other, and the trailing `1` in both labels is the `X` on `q3`. Step 2 keeps
two rows but *renames* one of them: `1001 → 1101`, which is the `CNOT`
flipping `q1` inside the branch where `q0 = 1`. Nothing else in the table
moves.

The same information, one column per qubit, is easier to scan:

| Step | P(q0=1) | P(q1=1) | P(q2=1) | P(q3=1) |
|---|---|---|---|---|
| start | 0.00 | 0.00 | 0.00 | 0.00 |
| `H(0), X(3)` | 0.50 | 0.00 | 0.00 | 1.00 |
| `CNOT(0, 1)` | 0.50 | 0.50 | 0.00 | 1.00 |

![P(qubit = 1) after each step](../assets/ch07-debug-marginals.png){ width="620" }

Read the table column by column, then row by row; every row is a different
qubit's history through the program:

- `q0`: jumps to `0.50` in the **first** step (`H`) and never moves again —
  the randomness assigned to `q0` is created once and then left untouched.
- `q1`: sits at `0` until the `CNOT` in the **second** step pulls it up to
  `0.50`, which means its randomness is inherited from `q0` rather than
  generated locally.
- `q2`: `0.00` throughout — nothing in the program touches it, so it plays no
  role in any outcome.
- `q3`: jumps to `1.00` in the first step (`X`) and stays there, behaving in
  effect as a classical constant the program set deliberately.

This is the debugging information a final histogram cannot give: *which step
changed which qubit*.

??? question "Check yourself — after step 2, P(q1 = 1) is 0.50. Does that mean `q1` is a random coin on its own?"
    If **only** `q1` were measured, a fair coin would be observed — 50/50,
    indistinguishable at that level from a genuinely random bit. But it is not
    *independent*: the two rows `0001` and `1101` say `q1` **always equals**
    `q0`. Half-probability comes from sharing the two branches, not from `q1`
    having a mind of its own. That difference — marginal randomness versus
    joint correlation — is the whole point of
    [Chapter 5](ch05-entanglement.md).

So what does the program *return*? When all four qubits are measured, only two
strings ever appear, regardless of how many times the run is repeated:

| Outcome `q0 q1 q2 q3` | Count (1000 shots) |
|---|---|
| `0001` | ≈ 500 |
| `1101` | ≈ 500 |

![Only two outcomes, and q1 follows q0](../assets/ch07-randombit-counts.png){ width="620" }

`q2` is always `0` and `q3` is always `1`; the randomness lives entirely in
`q0`, and `q1` **always agrees** with it. That agreement is a Bell pair on the
pair `(q0, q1)` — and it is the only honest way for a circuit to share an
unknown value. It is not a copy: [Chapter 6](ch06-quantum-networking.md)
showed that copying an unknown value is impossible in principle, and a `CNOT`
"clone" of a superposition produces exactly this entanglement instead.

## Adding two qubits

With the program open, the book turns to arithmetic — the classic first test
of any computing model, and the same one this chapter set out to pass. It is
worth watching closely how a familiar, everyday operation behaves once the
"never erase anything" rule is enforced.

A classical circuit adds with `AND` and `OR` gates. A quantum circuit cannot,
and the reason deserves to be stated carefully: every quantum gate must be
**reversible** — it must always be possible to run the gate backwards and
recover exactly the input that went in. A gate that throws information away
(three inputs, one output, like `AND`) cannot be run backwards, because two
different inputs produce the same output and the difference between them is
gone; for that reason it is banned outright.

The smallest arithmetic a quantum circuit *can* do is a single `CNOT`, which
flips its target exactly when its control is `1`. With `a` loaded on `q0` and
`b` on `q1`, the `CNOT(0, 1)` output on `q1` answers the question *"are the
two bits different?"*:

| a | b | "different?" | a + b (mod 2) |
|---|---|---|---|
| 0 | 0 | no | 0 |
| 0 | 1 | yes | 1 |
| 1 | 0 | yes | 1 |
| 1 | 1 | **no** | **0** |

"Are they different" is exactly the **XOR** operation, and it is also addition
**modulo 2** — counting the 1s and keeping only odd-or-even, like switching a
light off and on twice and finding it out again. The first three rows are
ordinary addition: the single `1` is small enough to fit in one bit. The
fourth is not: `1 + 1 = 2`, and `2` does not fit in one bit, so the answer
wraps back to `0`.

And there is the rub: the circuit *knows* a carry happened — both inputs were
`1`, so a genuine addition would have produced `10` in binary — but it has
**nowhere to put it**. `CNOT` only flips its target between `0` and `1`;
nothing in the circuit remembers that it carried. This is a **half-adder**: a
structure that is correct only as long as every answer fits in one bit, with
the overflow silently discarded.

??? question "Check yourself — is `1 + 1 = 0` a bug?"
    No — it is a contract. `CNOT` computes `a XOR b`, which is `a + b` *modulo
    2*: the sum with the carry thrown away. For three of the four inputs the
    carry is zero anyway, so that result is the full answer; for `1 + 1` the
    gate silently drops the `2`. The circuit never claimed to store the carry
    — that omission is precisely the flaw the next section fixes.

## The gate that gives you a carry

What is missing is a logical **AND**: a bit that is `1` only when *both*
inputs are `1`. A plain `AND` cannot be used — it destroys its inputs, as the
reversibility rule says. Its reversible stand-in is the **Toffoli** gate (also
written `CCNOT`). The easiest way to picture it: **a `CNOT` that needs two
permissions.** The target flips only when *both* controls are `1`.

| Body in `q0 q1 q2` | Out `q0 q1 q2` | |
|---|---|---|
| `000` | `000` | |
| `001` | `001` | |
| `010` | `010` | |
| `011` | `011` | |
| `100` | `100` | |
| `101` | `101` | |
| `110` | `111` | flipped |
| `111` | `110` | flipped |

Only two rows move, and in those two rows only the third qubit moves — but
that is exactly `AND` being written onto `q2`: whenever both controls are
`1`, the target becomes `1`, and whenever either control is `0`, the target
reverts to `0`. Because the inputs are still there afterwards, nothing was
erased, so the gate is reversible (its matrix is a permutation: running the
table backwards undoes it). The price of reversibility is that the result
needs **its own qubit** — it cannot be written over an input, because an
input that has been overwritten is an input that can no longer be recovered.

Now the adder is two gates, and the order is not a stylistic choice:

```text
Toffoli(0, 1, 2)   q2 = q0 AND q1   (the carry)   -- first
CNOT(0, 1)         q1 = q0 XOR q1    (the sum)     -- second
```

![The full adder for 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

The hardest case, `1 + 1`, is worth following through — it starts with
`a = 1` on `q0`, `b = 1` on `q1`, and a scratch qubit for the carry,
`q2 = 0`, i.e. the state `|110⟩`:

1. **Toffoli(0, 1, 2)** — both controls are `1`, so the target flips:
   `|110⟩ → |111⟩`. The carry bit now exists: `q2 = 1`.
2. **CNOT(0, 1)** — the control `q0` is `1`, so the target flips:
   `|111⟩ → |101⟩`. The sum bit lands on `q1 = 0`.

Read the result: `q1 = 0` (sum), `q2 = 1` (carry) — and `10` in binary is
`2`. `1 + 1 = 2` at last, and both parts of the answer are physically present
in the register.

??? question "Check yourself — why must the Toffoli run *before* the CNOT?"
    Because the `CNOT` overwrites one of the Toffoli's inputs. Run them the
    other way on `1 + 1`: `CNOT` first gives `|110⟩ → |100⟩` (the sum lands,
    `q1 = 0`). Now the Toffoli sees controls `1` and `0` — not both 1 — so it
    does nothing, and the carry is never written. `|100⟩` says "sum 0, carry
    0": the `2` vanished. In other words, order matters whenever one gate
    reads what another gate writes; here the CNOT destroys the very
    information the Toffoli needs before it can act.

The full picture over all four inputs:

| a | b | sum | carry | a + b |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | **2** |

![Half-adder vs. full adder](../assets/ch07-adder-comparison.png){ width="620" }

The two circuits agree on three inputs and split on the fourth. The gap — the
carry — is the whole reason the Toffoli exists in the quantum toolbox, and it
is the pattern every larger quantum algorithm builds on: **one more qubit,
one more control, and a previously irreversible operation becomes
reversible.**

![From X to CNOT to Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

The matrices make the family pattern explicit. A one-qubit `X` flips its
single target unconditionally; a `CNOT` flips the target on one control; a
`Toffoli` does so on two. Each member adds one control and one qubit to the
previous member, and it is this *reversible* family from which quantum
algorithms are constructed — including the oracles of
[Chapter 9](ch09-deutsch-jozsa.md), which are themselves built from exactly
such multi-controlled gates.

## The diagrams

### The program

![The four-qubit program](../assets/ch07-randombit-circuit.png){ width="460" }

`q0` at the top, then `q1`, `q2`, `q3` from top to bottom — the book's order,
matching `Qubit[0] … Qubit[3]`. `H` splits `q0`, `X` sets `q3`, and
`CNOT(0, 1)` ties `q1` to `q0`; the vertical connection between the two rules
is what makes the gate conditional. `q2` is drawn but never touched, and a
wire that no gate touches simply carries its starting value to the end.

### Debugging, step by step

![The program with step boundaries](../assets/ch07-debug-circuit.png){ width="460" }

The barriers mark where one step ends and the next begins — the same job the
book's probability gates performed in the printed diagram. Every region
between two barriers can therefore be interrogated independently, which is
what makes the state readable at each moment.

![Basis-state probabilities after each step](../assets/ch07-debug-steps.png){ width="620" }

The probability vector at three points: a single state first, then two, then
two — and the second transition changes qubit `q1`'s membership in the
branch that carries `q0 = 1`, without ever creating a new branch.

![P(qubit = 1) after each step](../assets/ch07-debug-marginals.png){ width="620" }

The same fact expressed one column per qubit: `q0` moves in step 1, `q1` in
step 2, `q2` and `q3` never. Reading the columns sequentially gives, in
effect, a per-qubit biography of the program.

### The adders

![The half-adder for 1 + 1](../assets/ch07-add1-circuit.png){ width="420" }

The `1 + 1` case: both inputs are set, and the sum reads `0` because the
one-bit output has nowhere to put the carry. What is missing from this
picture is not a gate but a place — a dedicated qubit for the overflow.

![The full adder for 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

The `Toffoli` writes the carry onto `q2` and the `CNOT` writes the sum onto
`q1`; between them, both halves of the two-bit total exist as ordinary qubit
values at the end of the program.

![Half-adder vs. full adder](../assets/ch07-adder-comparison.png){ width="620" }

![From X to CNOT to Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

## Key takeaways

- A quantum program is an ordered list of **steps**. Running it is nothing
  more than one state evolving from `|0…0>` under that list of steps until a
  final measurement is taken.
- The state can be read after **every** step; that is all "debugging a
  circuit" means, and it is how one determines *which* step changed *which*
  qubit — the question a final histogram cannot answer.
- In the HelloWorld program, `q0` becomes random at the `H`, `q1` picks up
  its value at the `CNOT`, and `q2` and `q3` never move. Every one of these
  facts is hidden by a final histogram, which only shows the end state.
- `CNOT` computes `a XOR b`: addition **modulo 2**, with no carry. On its own
  it is a **half-adder**, and on `1 + 1` it returns `0`.
- Every quantum gate is **reversible**, so the classical `AND` is banned. Its
  stand-in is the **Toffoli** (`CCNOT`) — "a `CNOT` that needs two
  permissions" — a reversible `AND` that keeps its inputs intact.
- `Toffoli` for the carry plus `CNOT` for the sum make a **full adder**, and
  `1 + 1 = 2`. Adding one qubit and one gate is all it took to make the
  operation reversible — and gate *order* matters, because the `CNOT`
  overwrites exactly the value the Toffoli needs to read.

## The code behind this chapter

Four samples, one per book section, plus a small shared helper:

- [`ch07/randombit.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/randombit.py)
  — the four-qubit program, its two steps, and the measured outcomes
  (7.5.1).
- [`ch07/debugging.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/debugging.py)
  — the same program with the state reported after every step (7.5.2).
- [`ch07/half_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/half_adder.py)
  — the `CNOT` half-adder, modulo 2, with no carry stored (7.6.2).
- [`ch07/full_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/full_adder.py)
  — the `Toffoli` + `CNOT` full adder, and the `Toffoli` matrix (7.6.3).
- [`ch07/circuits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/circuits.py)
  — the shared helpers: reading the state after a step, the probability
  vector, and the Qiskit ↔ book bit-order fix-up.

Run them all with `make ch07`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch07.full_adder
```
