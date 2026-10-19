# Chapter 8 — Secure communication using quantum computing

!!! abstract "In one sentence"
    Alice and Bob can agree on a **secret key** over a public line because a qubit
    only carries a bit *in a chosen base* — and an eavesdropper who does not know
    the base must disturb the state, which shows up as a ~25% error rate.

## A qubit carries a bit only in a base

Every qubit in this chapter is written in one of two **bases**:

- the **Z base**, whose states are `|0⟩` and `|1⟩` — the ordinary bit;
- the **X base**, whose states are `|+⟩` and `|−⟩`, a Hadamard away from the Z base.

A Hadamard rotates from one to the other, and — the small fact the whole chapter
leans on — **`H·H = I`**: rotate into a base and rotate back, and nothing has
changed.

![The Hadamard round trip](../assets/ch08-haha-circuit.png){ width="420" }

Apply an `X` to set a bit, then a Hadamard and another Hadamard, and the qubit
comes back exactly where it started:

$$|0\rangle \xrightarrow{X} |1\rangle \xrightarrow{H} |-\rangle \xrightarrow{H} |1\rangle$$

| Step | P(00) | P(01) | P(10) | P(11) |
|---|---|---|---|---|
| start: `\|00⟩` | 1.00 | 0.00 | 0.00 | 0.00 |
| `X(0)` | 0.00 | 1.00 | 0.00 | 0.00 |
| `H(0), H(1)` | 0.25 | 0.25 | 0.25 | 0.25 |
| `H(0), H(1)` again | 0.00 | 1.00 | 0.00 | 0.00 |

![Entering a base and leaving it](../assets/ch08-haha-bloch.png){ width="620" }

The detour through the X base (row 3) looks like a coin flip in the Z base — every
outcome equally likely — yet it leaves **no trace**: the last row is identical to
the `X` row. A base is something you can hide behind, because returning from it
costs nothing.

## Two attempts that do not work

Before BB84, the obvious designs fail, each for a different reason.

**No base at all.** Alice sends plain `|0⟩`/`|1⟩`, Bob measures in Z and reads
every bit back exactly. It looks perfect, and that is the failure: nothing about
the qubit is disturbed by being read, so **anything Bob can read, Eve can read
too**. There is no secret, only an unwatched conversation.

**A base nobody reconciles.** Alice flips a coin per qubit and prepares it in Z or
in X. Bob, who has no idea which, measures everything in Z. When Alice used Z he
is right; when she used X he gets a fair coin. Half the qubits are wrong, half of
those flip, and the raw error rate lands on a quarter:

| Attempt | Raw error rate | Verdict |
|---|---|---|
| Naive (no base) | 0.00 | Bob reads everything — so does Eve |
| Blind base (Z only) | ≈ 0.25 | one bit in four is wrong |

![Why bases must be reconciled](../assets/ch08-attempts-error.png){ width="560" }

The fix is not more qubits. It is a short **public conversation** about bases.

## BB84: keep the qubits whose bases agree

The protocol is a coin flip per qubit on each side, plus one public announcement.

1. **Alice** picks a random bit and a random base, and prepares the qubit in that
   base — one of `|0⟩`, `|1⟩`, `|+⟩`, `|−⟩`.
2. **Bob** picks a random base and measures.
3. They **sift**: they announce their **bases** — never their bits — and keep only
   the qubits where the bases matched. On a match Bob's bit is Alice's bit with
   certainty.

![One BB84 circuit](../assets/ch08-bb84-circuit.png){ width="620" }

Half the qubits match, so an `N`-qubit exchange yields about `N/2` key bits. In the
worked example, 8 qubits give 2 matching positions and both bits agree:

| # | Alice bit | Alice base | Bob base | Bob bit | |
|---|---|---|---|---|---|
| 0 | 1 | Z | X | 1 | discarded (bases differ) |
| 1 | 0 | X | Z | 0 | discarded (bases differ) |
| 2 | 0 | X | Z | 1 | discarded (bases differ) |
| 3 | 0 | X | X | 0 | kept |
| 4 | 0 | X | Z | 1 | discarded (bases differ) |
| 5 | 1 | Z | X | 1 | discarded (bases differ) |
| 6 | 0 | X | Z | 0 | discarded (bases differ) |
| 7 | 0 | Z | Z | 0 | kept |

## The wiretap cannot hide

Why does this detect an eavesdropper? Eve cannot **copy** a qubit — the
[no-cloning theorem](ch06-quantum-networking.md) forbids it — so the best she can
do is **intercept-resend**: measure each qubit in a base she guesses, then send on
whatever state she collapsed it to. She guesses right half the time.

When she is right, she forwards the correct state and Bob is none the wiser. When
she is wrong, her measurement has *already* destroyed Alice's state, and the state
she sends disagrees with Alice's about half the time. Averaged over her coin flips,
a quarter of Bob's sifted bits are wrong:

| Line | Mean sifted error rate |
|---|---|
| No eavesdropper | 0.000 |
| Intercept-resend | ≈ 0.25 |

![A clean line vs. a wiretap](../assets/ch08-eavesdropper-error.png){ width="620" }

Two exchanges of 8 qubits never look alike, but 200 of them separate cleanly: the
clean line piles up entirely at **0** errors, while a wiretap spreads out around a
quarter of the sifted bits. Alice and Bob compare a sample of their key; a handful
of disagreements is ordinary noise, but a quarter is a wiretap, and they throw the
key away and try again.

!!! note "A key, not a message"
    BB84 produces a shared random **key**, not the message itself. The key is then
    used with an ordinary cipher — a one-time pad, say — so the quantum part only
    has to solve the hard half: agreeing on a secret in public.

## The diagrams

### The Hadamard round trip

![The Hadamard round trip](../assets/ch08-haha-circuit.png){ width="420" }

![Entering a base and leaving it](../assets/ch08-haha-bloch.png){ width="620" }

`H·H = I`: the middle state is spread over all four outcomes, and the last state is
the `X` row again — a base entered and left for free.

### The failed attempts

![Why bases must be reconciled](../assets/ch08-attempts-error.png){ width="560" }

Zero errors out of a base-less channel is not success — it is the absence of a
secret.

### BB84 and its wiretap

![One BB84 circuit](../assets/ch08-bb84-circuit.png){ width="620" }

Alice's preparation (an `X` for a `1`, a Hadamard for the X base), Bob's base
rotation, and the measurement.

![A clean line vs. a wiretap](../assets/ch08-eavesdropper-error.png){ width="620" }

## Key takeaways

- A qubit carries a bit only relative to a **base**. The Z base holds `|0⟩`,`|1⟩`;
  the X base holds `|+⟩`,`|−⟩`; a Hadamard moves between them, and `H·H = I`.
- A plain bit channel is perfectly readable — by Bob **and** Eve. Zero errors is
  not secrecy.
- Prepending a random base does not help on its own: if Bob never learns it, a
  quarter of the bits come out wrong.
- **BB84** fixes this by sifting on **bases**: announce the bases, keep the qubits
  where they agree, and the kept bits are identical.
- **No-cloning** means any eavesdropper must disturb the state. An intercept-resend
  attack leaves a **~25%** error rate where a clean line leaves 0 — so the wiretap
  is detectable, and Alice and Bob can refuse a compromised key.

## The code behind this chapter

Three samples, one per book section, plus a small shared model:

- [`ch08/identity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/identity.py)
  — the ``haha`` sample: `X` then `H`, `H`, and the state comes back (8.2).
- [`ch08/attempts.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/attempts.py)
  — the ``naive`` and ``guess`` designs that fail.
- [`ch08/bb84.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/bb84.py)
  — the working protocol, with an intercept-resend eavesdropper and the error-rate
  separation.
- [`ch08/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/protocol.py)
  — the shared qubit model: the four states, the one measurement rule (same base =
  the bit, other base = a fair coin), the sift, and the circuit worth drawing.

Run them all with `make ch08`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch08.bb84
```
