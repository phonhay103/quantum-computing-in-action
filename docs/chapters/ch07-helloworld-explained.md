# Chapter 7 — Our HelloWorld, explained

!!! abstract "In one sentence"
    A quantum program is not a black box: it is an ordered list of **steps**, and
    the state it produces can be read after *every* one of them — which is all
    "running a circuit" ever means.

## The question this chapter answers

Chapter 2 asked the simulator for a random bit and got one, in a single call. This
chapter opens that call up and asks the two questions a programmer asks about any
piece of magic:

1. **What actually ran?** It was not a function call. It was a *program*: an
   ordered list of **steps**, where each step holds the gates that act at the
   same time. That is what "a quantum circuit" has meant all along.
2. **Can I look inside while it runs?** Yes. A simulator holds one object — the
   **state** — from the first gate to the last, so "debugging" is nothing more
   than reading that state after each step, exactly like printing a variable in
   the middle of a loop.

Having opened the box, the chapter uses it to do real work: **arithmetic**.
Adding numbers is the classic first test of any computing model, and a quantum
circuit can add — but under one strange rule that shapes everything from here on:
*a quantum gate is never allowed to erase information.*

After this chapter you will be able to:

- read a circuit diagram as a program: which gate touches which qubit, in which
  step;
- write down the state after each step **in numbers**, not just at the end;
- explain why `CNOT` adds "modulo 2" (`1 + 1 = 0`), and what gets lost;
- explain the **Toffoli** gate and how it recovers the loss, so that `1 + 1 = 2`.

You need three things from earlier chapters, each in one line: `H` puts a qubit
into an even 50/50 superposition ([Chapter 4](ch04-superposition.md));
`CNOT` flips a target qubit when its control is `1` ([Chapter 5](ch05-entanglement.md));
and an *unknown* value cannot be copied — only entangled ([Chapter 6](ch06-quantum-networking.md)).

!!! note "One bit of bookkeeping: bit order"
    A label such as `1001` in this chapter always reads **`q0` first**, left to
    right: `q0 q1 q2 q3`. So `1001` means `q0 = 1, q1 = 0, q2 = 0, q3 = 1` — the
    book's order, matching its `Qubit[0] … Qubit[3]`. (Qiskit itself prints the
    highest index on the left; every result shown here has already been flipped
    into the book's order.)

## A program is a list of steps

The book's ``randombit`` sample is a four-qubit program with exactly two steps:

```text
step 1:  H(0), X(3)
step 2:  CNOT(0, 1)
```

![The four-qubit program](../assets/ch07-randombit-circuit.png){ width="460" }

Read the circuit gate by gate, and after each one, ask "what is the state now?"

**Start.** Every qubit begins in `|0⟩`, so the four-qubit state is the single
basis state `|0000⟩` — certainty, probability 1.00.

**Step 1 — `H(0)` and `X(3)`.** Two gates act at the same time, on different
qubits:

- `H` on `q0` splits it into `( |0⟩ + |1⟩ )/√2` — the even 50/50 mix, the random
  bit from Chapter 2. It does not *decide* anything; it just makes both futures
  equally likely.
- `X` on `q3` flips that qubit to a definite `|1⟩`. The program is allowed to
  set values it already knows — `X` is just a controlled, reversible "set to 1".
- `q1` and `q2` are not in this step, so they do not move at all.

So after step 1 the whole register is

$$\frac{1}{\sqrt{2}}\,(|0001\rangle + |1001\rangle)$$

Two basis states, amplitude `1/√2` each, probability `1/2` each. Read the labels
in the book's order: `0001` is "`q0=0` and `q3=1`", `1001` is "`q0=1` and `q3=1`".
Only `q0` differs between them — exactly the qubit the `H` acted on.

**Step 2 — `CNOT(0, 1)`.** This gate looks at its control `q0` and flips its
target `q1` when that control is `1`. It acts on each branch separately, and it
is deterministic within each branch:

- branch `0001`: the control `q0` is `0`, so nothing happens;
- branch `1001`: the control `q0` is `1`, so `q1` flips `0 → 1`, giving `1101`.

$$\frac{1}{\sqrt{2}}\,(|0001\rangle + |1001\rangle)
\;\xrightarrow{\;\mathrm{CNOT}\;}
\frac{1}{\sqrt{2}}\,(|0001\rangle + |1101\rangle)$$

Still two branches, each still probability `1/2` — `CNOT` did not make anything
*more* random; it *correlated* `q1` with `q0`.

??? question "Check yourself — four qubits have sixteen possible outcomes. Why do only two appear?"
    `q3` is pinned to `1` by `X`, `q2` is never touched and stays `0`, and the
    only split in the whole program is the one `H` made on `q0` — two branches.
    `CNOT` then maps each branch to exactly one new branch; it never splits
    anything. Two branches in, two branches out: `0001` and `1101`.

## Reading the state after every step

A histogram at the *end* tells you what a program returns; it cannot tell you
*where* each qubit changed. The book's ``randombitdebug`` sample answers that by
drawing the probability vector after **every** step — and because the simulator's
state is a single object all the way through, this is not a trick: it is just
"print the variable" at three moments.

Here is the same program with a boundary drawn after each step:

![The program with step boundaries](../assets/ch07-debug-circuit.png){ width="460" }

First the full probability vector, keeping only the basis states that can occur:

| Step | Basis state `q0 q1 q2 q3` | Probability |
|---|---|---|
| start | `0000` | 1.00 |
| `H(0), X(3)` | `0001` | 0.50 |
| | `1001` | 0.50 |
| `CNOT(0, 1)` | `0001` | 0.50 |
| | `1101` | 0.50 |

![Basis-state probabilities after each step](../assets/ch07-debug-steps.png){ width="620" }

How to read it: the table is the whole state at three moments. At the start there
is one row, because the register is in one definite state. After step 1 there are
two rows — the `H` split the register into two futures, each as likely as the
other, and the trailing `1` in both labels is the `X` on `q3`. Step 2 keeps two
rows but *renames* one of them: `1001 → 1101`, which is the `CNOT` flipping `q1`
inside the branch where `q0 = 1`.

The same information, one column per qubit, is easier to scan:

| Step | P(q0=1) | P(q1=1) | P(q2=1) | P(q3=1) |
|---|---|---|---|---|
| start | 0.00 | 0.00 | 0.00 | 0.00 |
| `H(0), X(3)` | 0.50 | 0.00 | 0.00 | 1.00 |
| `CNOT(0, 1)` | 0.50 | 0.50 | 0.00 | 1.00 |

![P(qubit = 1) after each step](../assets/ch07-debug-marginals.png){ width="620" }

Read the table column by column, then row by row:

- `q0`: jumps to `0.50` in the **first** step (`H`) and never moves again.
- `q1`: sits at `0` until the `CNOT` in the **second** step pulls it up to `0.50`.
- `q2`: `0.00` throughout — nothing in the program touches it.
- `q3`: jumps to `1.00` in the first step (`X`) and stays there.

This is the debugging information a final histogram cannot give you: *which step
changed which qubit*.

??? question "Check yourself — after step 2, P(q1 = 1) is 0.50. Does that mean `q1` is a random coin on its own?"
    If you measured **only** `q1`, you would see a fair coin — 50/50. But it is
    not *independent*: the two rows `0001` and `1101` say `q1` **always equals**
    `q0`. Half-probability comes from sharing the two branches, not from `q1`
    having a mind of its own. That difference — marginal randomness versus joint
    correlation — is the whole point of [Chapter 5](ch05-entanglement.md).

So what does the program *return*? Measure all four qubits and only two strings
ever appear:

| Outcome `q0 q1 q2 q3` | Count (1000 shots) |
|---|---|
| `0001` | ≈ 500 |
| `1101` | ≈ 500 |

![Only two outcomes, and q1 follows q0](../assets/ch07-randombit-counts.png){ width="620" }

`q2` is always `0` and `q3` is always `1`; the randomness lives entirely in `q0`,
and `q1` **always agrees** with it. That agreement is a Bell pair on the pair
`(q0, q1)` — and it is the only honest way for a circuit to share an unknown
value. It is not a copy: [Chapter 6](ch06-quantum-networking.md) showed that
copying is impossible, and a `CNOT` "clone" of a superposition produces exactly
this entanglement instead.

## Adding two qubits

With the program open, the book turns to arithmetic — the classic first test of
any computing model. Watch how a familiar, everyday operation behaves under the
"never erase anything" rule.

A classical circuit adds with `AND` and `OR` gates. A quantum circuit cannot, and
the reason is worth saying slowly: every quantum gate must be **reversible** —
you must always be able to run it backwards and recover exactly what you had. A
gate that throws information away (three inputs, one output, like `AND`) cannot
be run backwards, so it is banned.

The smallest arithmetic a quantum circuit *can* do is a single `CNOT`, which
flips its target exactly when its control is `1`. With `a` loaded on `q0` and `b`
on `q1`, the `CNOT(0, 1)` output on `q1` answers the question *"are the two bits
different?"*:

| a | b | "different?" | a + b (mod 2) |
|---|---|---|---|
| 0 | 0 | no | 0 |
| 0 | 1 | yes | 1 |
| 1 | 0 | yes | 1 |
| 1 | 1 | **no** | **0** |

"Are they different" is exactly the **XOR** operation, and it is also addition
**modulo 2** — counting the 1s and keeping only odd-or-even, like flipping a light
switch twice and finding it off again. The first three rows are ordinary
addition. The fourth is not: `1 + 1 = 2`, and `2` does not fit in one bit, so the
answer wraps back to `0`.

And there is the rub: the circuit *knows* a carry happened (both inputs were 1),
but it has **nowhere to put it**. `CNOT` only flips its target between `0` and
`1`; nothing in the circuit remembers that it carried. This is a **half-adder**:
correct as long as every answer fits in one bit.

??? question "Check yourself — is `1 + 1 = 0` a bug?"
    No — it is a contract. `CNOT` computes `a XOR b`, which is `a + b` *modulo
    2*: the sum with the carry thrown away. For three of the four inputs that is
    the full answer; for `1 + 1` it silently drops the 2. The circuit never
    claimed to store the carry — that is precisely the flaw the next section
    fixes.

## The gate that gives you a carry

What is missing is a logical **AND**: a bit that is `1` only when *both* inputs
are `1`. A plain `AND` cannot be used — it destroys its inputs, as the reversibility
rule says. Its reversible stand-in is the **Toffoli** gate (also written `CCNOT`).
The easiest way to picture it: **a `CNOT` that needs two permissions.** The
target flips only when *both* controls are `1`.

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

Only two rows move, and only the third qubit moves in them — but that is exactly
`AND` being written onto `q2`. Because the inputs are still there afterwards,
nothing was erased, so the gate is reversible (its matrix is a permutation: run
the table backwards and you undo it). The price of reversibility is that the
result needs **its own qubit** — you cannot overwrite an input with it.

Now the adder is two gates, and the order is not a stylistic choice:

```text
Toffoli(0, 1, 2)   q2 = q0 AND q1   (the carry)   -- first
CNOT(0, 1)         q1 = q0 XOR q1    (the sum)     -- second
```

![The full adder for 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

Watch the hardest case, `1 + 1`, go through — start with `a = 1` on `q0`, `b = 1`
on `q1`, carry scratch `q2 = 0`, i.e. the state `|110⟩`:

1. **Toffoli(0, 1, 2)** — both controls are `1`, so the target flips:
   `|110⟩ → |111⟩`. The carry bit now exists: `q2 = 1`.
2. **CNOT(0, 1)** — the control `q0` is `1`, so the target flips:
   `|111⟩ → |101⟩`. The sum bit lands on `q1 = 0`.

Read the result: `q1 = 0` (sum), `q2 = 1` (carry) — and `10` in binary is `2`.
`1 + 1 = 2` at last.

??? question "Check yourself — why must the Toffoli run *before* the CNOT?"
    Because the `CNOT` overwrites one of the Toffoli's inputs. Run them the other
    way on `1 + 1`: `CNOT` first gives `|110⟩ → |100⟩` (the sum lands, `q1 = 0`).
    Now the Toffoli sees controls `1` and `0` — not both 1 — so it does nothing,
    and the carry is never written. `|100⟩` says "sum 0, carry 0": the `2`
    vanished. Order matters whenever one gate reads what another gate writes.

The full picture over all four inputs:

| a | b | sum | carry | a + b |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | **2** |

![Half-adder vs. full adder](../assets/ch07-adder-comparison.png){ width="620" }

The two circuits agree on three inputs and split on the fourth. The gap — the
carry — is the whole reason the Toffoli exists in the quantum toolbox, and it is
the pattern every larger quantum algorithm builds on: **one more qubit, one more
control, and a previously irreversible operation becomes reversible.**

![From X to CNOT to Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

The matrices make the family clear. A one-qubit `X` flips its single target
unconditionally; a `CNOT` flips the target on one control; a `Toffoli` on two.
Each member adds one control and one qubit, and this *reversible* family is what
quantum algorithms are written from — including the oracles of
[Chapter 9](ch09-deutsch-jozsa.md).

## The diagrams

### The program

![The four-qubit program](../assets/ch07-randombit-circuit.png){ width="460" }

`q0` at the top, then `q1`, `q2`, `q3` — the book's order, matching
`Qubit[0] … Qubit[3]`. `H` splits `q0`, `X` sets `q3`, and `CNOT(0, 1)` ties
`q1` to `q0`. `q2` is drawn but never touched.

### Debugging, step by step

![The program with step boundaries](../assets/ch07-debug-circuit.png){ width="460" }

The barriers mark where one step ends and the next begins — the job the book's
probability gates did in the picture.

![Basis-state probabilities after each step](../assets/ch07-debug-steps.png){ width="620" }

The probability vector at three points: a single state, then two, then two — and
the second one changes qubit `q1`'s membership.

![P(qubit = 1) after each step](../assets/ch07-debug-marginals.png){ width="620" }

The same fact, one column per qubit: `q0` moves in step 1, `q1` in step 2, `q2`
and `q3` never.

### The adders

![The half-adder for 1 + 1](../assets/ch07-add1-circuit.png){ width="420" }

The `1 + 1` case: both inputs set, and the sum reads `0` because there is nowhere
to put the carry.

![The full adder for 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

The `Toffoli` writes the carry onto `q2`, the `CNOT` writes the sum onto `q1`.

![Half-adder vs. full adder](../assets/ch07-adder-comparison.png){ width="620" }

![From X to CNOT to Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

## Key takeaways

- A quantum program is an ordered list of **steps**. Running it is one state
  evolving from `|0…0>` to a final measurement — nothing more.
- The state can be read after **every** step; that is all "debugging a circuit"
  means, and it is how you see *which* step changed *which* qubit.
- In the HelloWorld program, `q0` becomes random at the `H`, `q1` picks up its
  value at the `CNOT`, and `q2` and `q3` never move. A final histogram would hide
  all of that.
- `CNOT` computes `a XOR b`: addition **modulo 2**, with no carry. On its own it
  is a **half-adder**, and `1 + 1 = 0`.
- Every quantum gate is **reversible**, so the classical `AND` is banned. Its
  stand-in is the **Toffoli** (`CCNOT`) — "a `CNOT` that needs two permissions" —
  a reversible `AND` that keeps its inputs.
- `Toffoli` for the carry plus `CNOT` for the sum make a **full adder**, and
  `1 + 1 = 2`. Adding one qubit and one gate is all it took to make the operation
  reversible — and gate *order* matters, because the `CNOT` overwrites what the
  Toffoli needs to read.

## The code behind this chapter

Four samples, one per book section, plus a small shared helper:

- [`ch07/randombit.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/randombit.py)
  — the four-qubit program, its two steps, and the measured outcomes (7.5.1).
- [`ch07/debugging.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/debugging.py)
  — the same program with the state reported after every step (7.5.2).
- [`ch07/half_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/half_adder.py)
  — the `CNOT` half-adder, modulo 2, with no carry (7.6.2).
- [`ch07/full_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/full_adder.py)
  — the `Toffoli` + `CNOT` full adder, and the `Toffoli` matrix (7.6.3).
- [`ch07/circuits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/circuits.py)
  — the shared helpers: reading the state after a step, the probability vector,
  and the Qiskit ↔ book bit-order fix-up.

Run them all with `make ch07`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch07.full_adder
```
