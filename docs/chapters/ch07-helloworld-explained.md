# Chapter 7 — Our HelloWorld, explained

!!! abstract "In one sentence"
    A quantum program is not a black box: it is an ordered list of **steps**, and
    the state it produces can be read after *every* one of them — which is all
    "running a circuit" ever means.

## A program is a list of steps

Chapter 2 asked for a random bit and got one, without saying how. This chapter
opens the box. What it finds is not a function call but a **program**: an ordered
list of steps, each holding the gates that act at the same time.

The book's ``randombit`` sample is a four-qubit program with exactly two steps:

```text
step 1:  H(0), X(3)
step 2:  CNOT(0, 1)
```

![The four-qubit program](../assets/ch07-randombit-circuit.png){ width="460" }

Read it left to right:

- `H` on `q0` puts that qubit into an even superposition, `( |0⟩ + |1⟩ )/√2`. This
  is the random bit from Chapter 2.
- `X` on `q3` flips it to a definite `|1⟩` — the program is allowed to set values
  it already knows.
- `q2` is not touched at all.
- `CNOT(0, 1)` then flips `q1` exactly when `q0` is `1`.

Two steps, four qubits, and only one of them is actually random. But it is the
*combination* that matters, and to see why, you have to watch the state move.

## Reading the state after every step

A histogram at the end tells you *what* a program returns; it does not tell you
*where* each qubit changed. The book's ``randombitdebug`` sample answers that by
drawing the probability vector after **every** step. Its simulator holds one
object — the state — from start to finish, so "debugging" is nothing more than
looking at that object at each step.

Here is the same program with a boundary drawn after each step:

![The program with step boundaries](../assets/ch07-debug-circuit.png){ width="460" }

And here is what the state is at each of those points. The full probability
vector first, keeping only the basis states that can occur:

| Step | Basis state `q0 q1 q2 q3` | Probability |
|---|---|---|
| start | `0000` | 1.00 |
| `H(0), X(3)` | `0001` | 0.50 |
| | `1001` | 0.50 |
| `CNOT(0, 1)` | `0001` | 0.50 |
| | `1101` | 0.50 |

![Basis-state probabilities after each step](../assets/ch07-debug-steps.png){ width="620" }

Only ever two nonzero states, and the second column tells the whole story: the
`X` pins `q3` to `1` immediately (the leading `0001`), the `H` splits `q0`, and
the `CNOT` moves `q1` from `0` to `1` *in step with* `q0` (the `1001` becomes
`1101`).

The same information, one column per qubit, is easier to scan:

| Step | P(q0=1) | P(q1=1) | P(q2=1) | P(q3=1) |
|---|---|---|---|---|
| start | 0.00 | 0.00 | 0.00 | 0.00 |
| `H(0), X(3)` | 0.50 | 0.00 | 0.00 | 1.00 |
| `CNOT(0, 1)` | 0.50 | 0.50 | 0.00 | 1.00 |

![P(qubit = 1) after each step](../assets/ch07-debug-marginals.png){ width="620" }

Read the columns: `q0` alone jumps to `0.50` in the **first** step (`H`), `q1`
alone jumps in the **second** step (`CNOT`), and `q2` and `q3` hold their values
the whole way through. A histogram of the final state could not tell you that; the
intermediate state can.

So what does the program *return*? Measure all four qubits and only two strings
ever appear:

| Outcome `q0 q1 q2 q3` | Count (1000 shots) |
|---|---|
| `0001` | ≈ 500 |
| `1101` | ≈ 500 |

![Only two outcomes, and q1 follows q0](../assets/ch07-randombit-counts.png){ width="620" }

`q2` is always `0` and `q3` is always `1`; the randomness is entirely in `q0`, and
`q1` **always agrees** with it. That agreement is a Bell pair on the pair
`(q0, q1)` — the correlation of [Chapter 5](ch05-entanglement.md) — and it is the
only honest way for a circuit to share an unknown value. It is not a copy:
[Chapter 6](ch06-quantum-networking.md) showed that copying is impossible, and a
`CNOT` "clone" of a superposition produces exactly this entanglement instead.

## Adding two qubits

With the program open, the book turns to **arithmetic** — the classic first test
of any computing model. A classical circuit adds with `AND` and `OR` gates. A
quantum circuit cannot, because every quantum gate has to be **reversible**: you
are never allowed to erase a bit.

The smallest arithmetic a quantum circuit can do is therefore a `CNOT`, which
flips its target exactly when its control is `1`:

![The half-adder for 1 + 1](../assets/ch07-add1-circuit.png){ width="420" }

With `a` loaded on `q0` and `b` on `q1`, a single `CNOT(0, 1)` leaves the **sum**
on `q1`:

| a | b | a + b (mod 2) |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | **0** |

The first three lines are ordinary addition. The fourth is not: `1 + 1` wraps back
to `0`, because `CNOT` only ever flips the target *between* `0` and `1`. Nothing
in the circuit remembers that it carried. This is a **half-adder**: correct as
long as the answer fits in one bit.

## The gate that gives you a carry

What is missing is a logical **AND** — a bit that is `1` only when both inputs are
`1`. A plain `AND` destroys its inputs, so it is not allowed. Its reversible
stand-in is the **Toffoli** gate (also written `CCNOT`): a three-qubit gate that
flips its target only when **both** controls are `1`.

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
`AND`. Applied to `(a, b, 0)` the Toffoli leaves `a` and `b` untouched and writes
`a AND b` on top of the target. Nothing is erased, so the gate is reversible; the
price of that is that the inputs are still there afterwards, which is why the
result needs its own qubit.

```text
Toffoli(0, 1, 2)   q2 = q0 AND q1   (the carry)
CNOT(0, 1)         q1 = q0 XOR q1   (the sum)
```

The Toffoli must run **before** the `CNOT`, because the `CNOT` is about to
overwrite its second control.

![The full adder for 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

Now `1 + 1 = 2` at last: the sum bit still wraps to `0`, and the new qubit `q2`
holds the `1` the half-adder dropped.

| a | b | sum | carry | a + b |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | **2** |

![Half-adder vs. full adder](../assets/ch07-adder-comparison.png){ width="620" }

The two circuits agree on three inputs and split on the fourth. The gap — the
carry — is the whole reason the Toffoli exists in the quantum toolbox, and it is
the pattern every larger quantum algorithm builds on: one more qubit, one more
gate, and a previously irreversible operation becomes reversible.

![From X to CNOT to Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

The matrices make the family clear. A one-qubit `X` flips its single target
unconditionally; a `CNOT` flips the target on one control; a `Toffoli` on two.
Each adds a control and a qubit, and the set of *reversible* multi-qubit gates is
what an algorithm is written from.

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
  stand-in is the **Toffoli** (`CCNOT`), which flips a target only when two
  controls are `1` — a reversible `AND` that keeps its inputs.
- `Toffoli` for the carry plus `CNOT` for the sum make a **full adder**, and
  `1 + 1 = 2`. Adding one qubit and one gate is all it took to make the operation
  reversible.

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

!!! note "One bit of bookkeeping: bit order"
    Qiskit prints an outcome with the **highest** qubit index on the left — a
    four-qubit key reads `q3 q2 q1 q0`. The book writes `q0 q1 q2 q3`. Every
    result shown here has been flipped into the book's order, so a label in this
    chapter reads exactly as the book's `Qubit[0] … Qubit[3]`.
