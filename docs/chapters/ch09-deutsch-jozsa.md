# Chapter 9 — Deutsch–Jozsa algorithm

!!! abstract "In one sentence"
    If a function is promised to be **constant** or **balanced**, one quantum query
    decides which — where a classical check may need `2^(n-1) + 1`.

## Every gate is reversible

A quantum circuit is built from **reversible** gates: apply one and you can always
apply its inverse to get back exactly what you had. The simplest example is an `X`
gate used twice.

![Two X gates](../assets/ch09-reversible-circuit.png){ width="360" }

$$|0\rangle \xrightarrow{X} |1\rangle \xrightarrow{X} |0\rangle$$

This is not a curiosity — it is the constraint that shapes the whole chapter. A
classical `AND` violates it:

| a | b | a AND b | |
|---|---|---|---|
| 0 | 0 | 0 | |
| 0 | 1 | 0 | three inputs, one output |
| 1 | 0 | 0 | |
| 1 | 1 | 1 | |

Three different inputs share the output `0`, so the input is gone and cannot be
recovered. Quantum circuits cannot use `AND` as a black box. They use the
**Toffoli** gate of [Chapter 7](ch07-helloworld-explained.md) instead, which writes
`a AND b` onto a *third* qubit and leaves `a` and `b` in place — reversible, at the
cost of one extra wire.

## Oracles: reversible black boxes

A quantum algorithm never sees a function; it sees an **oracle**, the reversible
circuit that evaluates it. For a function `f` of one bit, the oracle acts on two
registers:

$$U_f : |x\rangle|y\rangle \longrightarrow |x\rangle\,|y \oplus f(x)\rangle$$

The input `x` comes back untouched and the answer is XOR-ed onto the spare
register `y`. Set `y = 0` and the spare holds `f(x)`; set `y = 1` and it holds
`NOT f(x)`. Either way nothing is erased — which is exactly what reversibility
demands.

![A balanced oracle: one CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

## The four one-bit functions

There are only four functions of one bit, and they split into two families:

| Function | f(0) | f(1) | Kind | Oracle circuit |
|---|---|---|---|---|
| constant 0 | 0 | 0 | constant | nothing |
| constant 1 | 1 | 1 | constant | `X` on `y` |
| balanced: `f(x) = x` | 0 | 1 | balanced | `CNOT(x, y)` |
| balanced: `f(x) = NOT x` | 1 | 0 | balanced | `X` on `y`, then `CNOT(x, y)` |

![The four oracle matrices](../assets/ch09-oracle-matrices.png){ width="620" }

Each is a **permutation matrix**: one `1` in every row and column, so the
operation is invertible. The difference between the two families is exactly
whether the input `x` changes the answer — constant functions ignore `x` entirely,
balanced functions answer differently on `0` and `1`.

## The Deutsch algorithm

Deutsch's problem: you are handed one of these oracles and asked only *which
family* it belongs to. Classically you must query both inputs — two lookups.
Quantumly, **one** query is enough:

![The Deutsch circuit](../assets/ch09-deutsch-circuit.png){ width="460" }

1. `X(1)` — the spare register becomes `|1⟩`.
2. `H(0), H(1)` — both registers in superposition; `q1` is now `|−⟩`.
3. the oracle — one evaluation of `f`.
4. `H(0)` — interfere the two branches.
5. measure `q0`.

The mechanism is **phase kickback**. With `q1 = |−⟩`, the oracle leaves both
registers where they are but multiplies the state by `(-1)^f(x)`: it writes the
function's value into the **sign**. Now the two branches of `q0` carry
`(-1)^f(0)` and `(-1)^f(1)`.

- **Constant** — both signs are equal. Equal signs are a global phase and
  invisible, so the final Hadamard puts `q0` back to `|0⟩`. The measurement is `0`.
- **Balanced** — the signs differ. That relative minus sign is what interference
  sees, and the final Hadamard turns it into `|1⟩`. The measurement is `1`.

| Function | f(0) | f(1) | measured q0 | Verdict |
|---|---|---|---|---|
| const 0 | 0 | 0 | 0 | constant |
| const 1 | 1 | 1 | 0 | constant |
| f(x) = x | 0 | 1 | 1 | balanced |
| f(x) = NOT x | 1 | 0 | 1 | balanced |

![One query: constant measures 0, balanced measures 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

Both constant functions measure `0`, both balanced functions measure `1`, always
and with certainty, from a single evaluation.

## Deutsch–Jozsa: one query for any `n`

The generalisation replaces the one-bit input with an `n`-bit one,
`f: {0,1}^n → {0,1}`, promised to be **constant** (the same answer on every input)
or **balanced** (0 on exactly half the inputs, 1 on the other half). The circuit is
Deutsch's with more wires:

![Deutsch–Jozsa for n = 3](../assets/ch09-dj-circuit.png){ width="620" }

1. `X` the ancilla; Hadamard all `n + 1` qubits.
2. Run the oracle **once** — on all `2^n` inputs at the same time.
3. Hadamard the `n` input qubits.
4. Measure the input register.

The amplitude of `|0…0⟩` is the **sum** of the branch signs:

- **Constant** — every sign is the same, the amplitudes add, and `|0…0⟩` has
  probability 1.
- **Balanced** — half the signs are `-1`, the amplitudes cancel, and `|0…0⟩` has
  probability 0.

So one outcome settles it: **all zeros means constant; anything else means
balanced.**

| n | Oracle | P(0…0) | Verdict | Classical worst case |
|---|---|---|---|---|
| 1 | constant 0 | 1.00 | constant | 2 |
| 1 | constant 1 | 1.00 | constant | 2 |
| 1 | balanced | 0.00 | balanced | 2 |
| 2 | constant 0 | 1.00 | constant | 3 |
| 2 | balanced | 0.00 | balanced | 3 |
| 3 | constant 0 | 1.00 | constant | 5 |
| 3 | balanced | 0.00 | balanced | 5 |

![n = 2: a constant oracle returns 00, a balanced one never does](../assets/ch09-dj-outcomes.png){ width="620" }

The classical column is the point. To be *certain*, a classical check may have to
evaluate `2^(n-1) + 1` inputs — half the space plus one, past the point where a
balanced function could still be hiding. The quantum cost stays at **one** query
no matter how wide the input is.

!!! note "Quantum parallelism, and what it is not"
    The oracle really does evaluate `f` on all `2^n` inputs in a single pass — that
    is **quantum parallelism**. But you cannot read all those values out: a
    measurement returns one basis state. What the circuit extracts is not the
    answers but a single bit of **global** information about `f` (here, its
    constancy). Interference is what turns the parallel evaluation into that bit,
    and it is why quantum speed-ups are about *questions*, not about computing
    everything at once.

## The diagrams

### Reversibility

![Two X gates](../assets/ch09-reversible-circuit.png){ width="360" }

### Oracles

![A balanced oracle: one CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

![The four oracle matrices](../assets/ch09-oracle-matrices.png){ width="620" }

### Deutsch

![The Deutsch circuit](../assets/ch09-deutsch-circuit.png){ width="460" }

![One query: constant measures 0, balanced measures 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

### Deutsch–Jozsa

![Deutsch–Jozsa for n = 3](../assets/ch09-dj-circuit.png){ width="620" }

![n = 2: a constant oracle returns 00, a balanced one never does](../assets/ch09-dj-outcomes.png){ width="620" }

## Key takeaways

- Every quantum gate is **reversible**. Irreversible classical gates such as `AND`
  cannot be used directly; the reversible stand-in is the **Toffoli** gate.
- An **oracle** evaluates a function reversibly:
  `U_f : |x⟩|y⟩ → |x⟩|y ⊕ f(x)⟩`. It keeps the input and writes the answer onto a
  spare register.
- A one-bit function is **constant** (`f(0) = f(1)`) or **balanced**
  (`f(0) ≠ f(1)`); there are four such functions and each has a one-gate oracle.
- **Phase kickback** turns a function's value into a *sign*: with the spare
  register in `|−⟩`, the oracle multiplies each branch by `(-1)^f(x)`.
- **Deutsch** uses one query to classify a one-bit function; **Deutsch–Jozsa**
  does the same for `n` bits, still in **one** query, where a classical check
  needs up to `2^(n-1) + 1`.
- The algorithm does not read the `2^n` answers; it extracts one **global** bit —
  constancy — through interference.

## The code behind this chapter

Four samples, from the rule up to the algorithm:

- [`ch09/reversible.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/reversible.py)
  — the ``reversibleX`` sample: `X·X = I`, and why `AND` cannot be an oracle.
- [`ch09/oracles.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/oracles.py)
  — the four one-bit functions, their circuit oracles and matrices, plus the
  `n`-bit oracles for Deutsch–Jozsa.
- [`ch09/deutsch.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutsch.py)
  — the Deutsch circuit and its one-query classification.
- [`ch09/deutschjozsa.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutschjozsa.py)
  — the general algorithm, the all-zero test, and the classical comparison.

Run them all with `make ch09`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch09.deutschjozsa
```
