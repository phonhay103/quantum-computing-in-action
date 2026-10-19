# Chapter 8 — Secure communication using quantum computing

!!! abstract "In one sentence"
    Alice and Bob can agree on a **secret key** over a public line because a qubit
    only carries a bit *in a chosen base* — and an eavesdropper who does not know
    the base must disturb the state, which shows up as a ~25% error rate.

## The question this chapter answers

Alice and Bob have never met in private, yet they want a secret. Every wire between
them is public: anything Alice sends, a third party — call her **Eve** — can look
at. Classically this is hopeless in a specific, interesting way: reading a copy
of a message leaves the original untouched, so Eve can copy quietly and nobody
ever knows. The chapter asks four questions about that setup:

1. **How do you even write a bit so that reading it is a *choice*?** A qubit
   carries a bit only relative to a **base**, and a reader who uses the wrong
   base gets a coin flip instead of the bit.
2. **Why do the obvious designs fail?** Sending plain bits, hiding them in a
   random base, or spreading them over a superposition each look promising — and
   each fails for a reason worth knowing before the fix makes sense.
3. **How does a public conversation create a private key?** BB84: announce the
   **bases** (never the bits), keep the qubits where both sides chose the same
   base, and the kept bits are identical.
4. **Why can't Eve hide?** She cannot copy a qubit, so she must measure it, in a
   base she can only guess — and her wrong guesses leave a fingerprint of about
   **25%** in the sifted key, where a clean line leaves exactly **0**.

After this chapter you will be able to:

- say what a **base** is (the Z base `|0⟩`, `|1⟩` vs. the X base `|+⟩`, `|−⟩`) and
  compute, with numbers, what a measurement returns in each base;
- explain `H·H = I` as "the right base cancels, the wrong base doesn't", using
  the Hadamard round trip;
- say precisely why plain bits, an unreconciled base, and a superposition each
  fail to make a secret;
- walk a full 8-qubit BB84 exchange row by row: which positions survive sifting
  and what key they produce;
- compute the eavesdropper's error rate as `1/2 × 1/2 = 1/4`, and explain why a
  clean line sits at exactly 0.

You need three things from earlier chapters, each in one line: `H` puts a qubit
into an even 50/50 superposition ([Chapter 4](ch04-superposition.md));
measuring a superposition collapses it, and an *unknown* state cannot be copied —
only entangled ([Chapter 6](ch06-quantum-networking.md)); and a circuit's state
can be read after every step ([Chapter 7](ch07-helloworld-explained.md)).

!!! note "How to read the tables in this chapter"
    - A **base** is the pair of states a measurement compares against. This
      chapter uses two: the **Z base** (`|0⟩`, `|1⟩` — the ordinary bit) and the
      **X base** (`|+⟩`, `|−⟩` — a Hadamard away). `Z` and `X` name bases;
      `0` and `1` name bits.
    - The two-qubit round-trip table uses Qiskit's label order `q1 q0`: the
      *right-hand* character is `q0`, the qubit carrying the bit.
    - Four-qubit register labels (e.g. `0110`) use the book's order, `q0` first —
      same convention as [Chapter 7](ch07-helloworld-explained.md).
    - Bit/base tables have one row per qubit position, position `0` first.

## A qubit carries a bit only in a base

A classical bit has exactly one alphabet: `0` and `1`, and every reader uses it.
A qubit has (at least) two alphabets, and *which one you read in is a choice*.
That choice is the whole chapter, so start concrete.

The four states Alice can send, written as vectors:

| Base | bit `0` | bit `1` |
|---|---|---|
| Z | `|0⟩` = (1, 0) | `|1⟩` = (0, 1) |
| X | `|+⟩` = (1, 1)/√2 | `|−⟩` = (1, −1)/√2 |

**A worked measurement.** Alice sends `|0⟩` — the *bit* is `0`, the *base* is Z.

- Bob measures in **Z**: the probability of reading `0` is `|⟨0|0⟩|² = 1`.
  Certain. This is the ordinary bit you already know.
- Bob measures in **X**: the possible outcomes are now `|+⟩` (bit `0`) and
  `|−⟩` (bit `1`). The probability of reading bit `0` is

$$|\langle +|0\rangle|^2 = \left(\tfrac{1}{\sqrt{2}}\right)^2 = \tfrac{1}{2}$$

  A 50/50 coin flip — about a perfectly definite state.

**The general rule, now that the example is on the table.** Measuring in the
base the qubit was prepared in returns the bit *with certainty* — all four
states, both bits. Measuring in the other base returns a fair coin *no matter
what the bit was*: `|⟨+|1⟩|² = 1/2` just as above, and
`|⟨0|−⟩|² = |⟨1|−⟩|² = 1/2` too. Verified against the simulator
(`protocol.state_probabilities`): every same-base measurement is certain, every
cross-base measurement is `0.5 / 0.5`.

**Why the round trip matters: `H·H = I`.** The Hadamard gate moves a qubit from
one base to the other (`H|0⟩ = |+⟩`, `H|1⟩ = |−⟩`), and it is its own inverse:
apply it twice and nothing happened. The book's `haha` sample watches this gate
by gate on two qubits — `q0` carries a bit, `q1` sits in the X base beside it:

$$|0\rangle \xrightarrow{X} |1\rangle \xrightarrow{H} |-\rangle \xrightarrow{H} |1\rangle
\qquad
|0\rangle \xrightarrow{H} |+\rangle \xrightarrow{H} |0\rangle$$

![The Hadamard round trip](../assets/ch08-haha-circuit.png){ width="420" }

The joint state, read after each step (labels `q1 q0`, so `01` means
`q0 = 1, q1 = 0`):

| Step | P(00) | P(01) | P(10) | P(11) |
|---|---|---|---|---|
| start: `\|00⟩` | 1.00 | 0.00 | 0.00 | 0.00 |
| `X(0)` | 0.00 | 1.00 | 0.00 | 0.00 |
| `H(0), H(1)` | 0.25 | 0.25 | 0.25 | 0.25 |
| `H(0), H(1)` again | 0.00 | 1.00 | 0.00 | 0.00 |

![Entering a base and leaving it](../assets/ch08-haha-bloch.png){ width="620" }

Row 3 deserves the arithmetic. The register is `q1` in `|+⟩` and `q0` in `|−⟩`,
i.e. `|+−⟩`:

$$|+\rangle \otimes |-\rangle = \tfrac{1}{2}\,(|00\rangle - |01\rangle + |10\rangle - |11\rangle)$$

Four basis states, amplitude `±1/2` each, probability `1/4` each. The *signs*
are invisible to a measurement — it only sees `|amplitude|²` — but they are not
lost: a Hadamard sees them. Apply `H` to both qubits again and the terms
recombine into exactly `q0 = 1, q1 = 0`, label `01`, probability 1.00. Row 4 is
row 2 again, digit for digit: **the detour through the X base left no trace.**

That is the "why it works". Read it as a rule about bases: if Bob measures in
Alice's base, his Hadamard (into the Z alphabet, right before the measurement)
undoes her Hadamard — `H·H = I`, the bit passes through untouched. If he
measures in the *other* base, only one Hadamard acts: `H` alone, and the state
he measures is a superposition *in his alphabet* — a coin flip. **Right base =
`H·H`; wrong base = `H` alone.** A base is something you can hide behind,
because leaving it costs the owner nothing and costs a stranger all certainty.

??? question "Check yourself — Alice sends `|−⟩` (bit `1`, X base). Bob measures in Z and gets `0`. Can he conclude the bit was `0`?"
    No — and worse, he has learned *nothing*. Whatever Alice sends, a Z
    measurement of an X-base state is a fair coin: `|⟨0|−⟩|² = 1/2` and
    `|⟨1|−⟩|² = 1/2`. Bob's `0` was as likely if Alice sent `|+⟩` (bit `0`) as
    if she sent `|−⟩` (bit `1`), so it carries zero information. And his
    measurement has already collapsed the qubit to `|0⟩` — nobody can re-read
    it in the right base afterwards. A wrong-base answer is not a noisy
    version of the bit; it is a coin flip that destroys the original.

## Two attempts that do not work

Before BB84, the book tries the obvious designs and watches each fail for a
different reason. The numbers below are real runs of the chapter's modules.

**Attempt 1 — no base at all.** Alice encodes each bit in Z (`|0⟩`/`|1⟩`) and
sends. Bob measures in Z. A 64-qubit run: the raw error rate is **0.00** —
every bit arrives intact. It looks perfect, and that is exactly the failure: a
measurement of a plain bit disturbs nothing, so there is nothing to stop Eve
from reading the same bits. **Anything Bob can read, Eve can read too.** Zero
errors here means zero secrecy — an unwatched conversation, not a private one.

**Attempt 2 — a base nobody reconciles.** Alice now flips a coin per qubit and
prepares it in Z or X. Bob, never told which, measures everything in Z. When
Alice used Z he is right; when she used X he gets a fair coin, and half the
coins land on the wrong bit. The arithmetic:

$$\underbrace{\tfrac{1}{2}}_{\text{wrong base}} \times \underbrace{\tfrac{1}{2}}_{\text{coin lands wrong}} = \tfrac{1}{4}$$

Real runs: a 64-qubit exchange came out at **0.36** (23 of 64 bits wrong — small
samples bounce around), and an 800-qubit exchange at **0.235**, closing in on
the predicted quarter.

| Attempt | Raw error rate (observed) | Verdict |
|---|---|---|
| Naive (no base) | 0.00 (64 qubits) | Bob reads everything — so does Eve |
| Blind base (Z only) | 0.36 in a 64-qubit run, 0.235 over 800 | one bit in four is wrong |

![Why bases must be reconciled](../assets/ch08-attempts-error.png){ width="560" }

Attempt 2 is interesting because it fails in the *opposite* direction from
Attempt 1: there is now something Eve does not know (the base), but Bob doesn't
know it either, and a key that is wrong one bit in four is unusable. The fix is
not more qubits. It is a short **public conversation about bases** — which is
precisely what BB84 adds.

## Using superposition is not enough either

The third obvious idea: if a plain bit is readable and a hidden base is not
enough, send the bits **in superposition** — Hadamard every qubit so the
register holds all `2^n` states at once. Eve surely cannot read a state that is
still "in flux"?

It really does spread the register — and then it spreads right back, because of
`H·H = I`. Watch the arithmetic on the sample's four qubits, prepared with bits
`0110` (an `X` on each qubit whose bit is `1`):

**Prepared.** One definite basis state, `|0110⟩`, probability 1.00.

**After one `H` round.** Each qubit splits with amplitude `1/√2` per term, so
each of the `2⁴ = 16` register states carries amplitude
`(1/√2)⁴ = 1/4`:

$$\underbrace{\left(\tfrac{1}{\sqrt{2}}\right)^4}_{\text{amplitude}} = \tfrac{1}{4},
\qquad
\text{probability per state} = \left(\tfrac{1}{4}\right)^2 = \tfrac{1}{16} = 0.0625$$

Sixteen states at `0.0625` each, and `16 × 0.0625 = 1`: the whole probability
mass, evenly spread. This is what "the register is in all states at once"
*means in numbers*.

**After the second `H` round.** The second round is the inverse of the first
(`H·H = I` on every qubit), so the amplitudes recombine into the prepared state
exactly: `|0110⟩` with probability 1.00, and `0` everywhere else.

![A register in superposition, and the same register recovered](../assets/ch08-superposition-states.png){ width="620" }

![The four-qubit superposition circuit](../assets/ch08-superposition-circuit.png){ width="620" }

| Stage | Distribution (verified) |
|---|---|
| prepared | one state: `0110`, probability 1.00 |
| after one `H` on every qubit | all 16 states, each with probability `1/16 = 0.0625` |
| after two `H` on every qubit | `0110` again, probability 1.00 |

So Bob — who knows the recipe, since Alice just applies `H` twice — reads the
bits perfectly. The chapter's sample run: Alice sent `1000`, Bob received
`1000`, four qubits, zero errors. Eve could do the same: the "spread" state is
not hidden, it is *rotated*, and anyone who knows the rotation reads it.

A superposition is a genuine capability (Chapter 9 will use it hard), but it is
not secrecy. Secrecy needs the one ingredient none of these attempts has: a
base that Alice chooses at random and reveals **only after the qubits are
gone**.

## BB84: keep the qubits whose bases agree

The protocol is a coin flip per qubit on each side, plus one public
announcement:

1. **Alice** picks a random bit *and* a random base, and prepares the qubit in
   that base — one of `|0⟩`, `|1⟩`, `|+⟩`, `|−⟩`.
2. **Bob** picks a random base and measures.
3. They **sift**: they announce their **bases** — never their bits — and keep
   only the qubits where the bases matched. On a match, Bob's measurement `H`
   undoes Alice's preparation `H` (`H·H = I`), so Bob's bit *is* Alice's bit
   with certainty.

![One BB84 circuit](../assets/ch08-bb84-circuit.png){ width="620" }

**A full worked exchange** — 8 qubits, produced with a fixed seed by the
chapter's own code (`bb84.exchange(seed=2)`), so you can reproduce every cell:

| # | Alice bit | Alice base | Bob base | Bob bit | verdict |
|---|---|---|---|---|---|
| 0 | 1 | Z | X | 1 | discarded (bases differ) |
| 1 | 0 | X | Z | 0 | discarded (bases differ) |
| 2 | 0 | X | Z | 1 | discarded (bases differ) |
| 3 | 0 | X | X | 0 | **kept** |
| 4 | 0 | X | Z | 1 | discarded (bases differ) |
| 5 | 1 | Z | X | 1 | discarded (bases differ) |
| 6 | 0 | X | Z | 0 | discarded (bases differ) |
| 7 | 0 | Z | Z | 0 | **kept** |

Walk it row by row:

- **Row 0:** Alice sends bit `1` in Z (`|1⟩`). Bob chose X. His `1` is a coin
  flip (`|⟨−|1⟩|² = 1/2`) — it *happened* to agree, but it is not information,
  so the position goes.
- **Rows 1, 2, 4, 6:** Alice used X, Bob used Z. Note row 2: Bob's bit is `1`
  where Alice's is `0` — exactly the coin-flip behaviour, and exactly why these
  positions must go.
- **Row 3:** both chose X. Alice's preparation `H` and Bob's measurement `H`
  cancel: Bob reads her `0` with certainty. Kept.
- **Row 5:** Alice in Z, Bob in X — differ, discard.
- **Row 7:** both chose Z, no Hadamards anywhere: the plain bit passes through.
  Kept.

The sifted positions are `3` and `7`, so the key is Alice's bits there: `0` and
`0`. Both keys read **`00`** — and on a clean line they always agree
(over 200 exchanges, the average sifted error rate was exactly `0.000`). Two
kept out of eight is a small-sample fluke of this seed; the long-run average is
about half — measured at `4.0` kept per 8-qubit exchange over 200 runs — so an
`N`-qubit exchange yields about `N/2` key bits.

??? question "Check yourself — Bob's wrong-base bits are sometimes right by luck (rows 0, 1, 6). Why throw them away instead of correcting them?"
    Because "wrong" is not a *fixable* kind of wrong. A discarded bit is a coin
    flip — it agrees with Alice's bit with probability 1/2 *whatever she sent*,
    so it contains no information to correct it *with*. To fix it, Bob would
    have to know Alice's bit — which is the very thing they are trying to
    share. And he cannot re-measure the qubit in the right base: the wrong-base
    measurement already collapsed it. Discarding costs half the qubits and
    keeps certainty; "correcting" would keep all the qubits and zero certainty.

!!! note "A key, not a message"
    BB84 produces a shared random **key**, not the message itself. The key is
    then used with an ordinary cipher — a one-time pad, say — so the quantum
    part only has to solve the hard half: agreeing on a secret in public.

## The wiretap cannot hide

Now the reason this is *secure* and not just a cute exchange. Classically, Eve
copies the message and passes the original along; nobody notices. Quantum
mechanics closes that door: the [no-cloning theorem](ch06-quantum-networking.md)
says an unknown state **cannot be duplicated** — and every state Alice sends is
unknown to Eve, because she does not know the base. To learn anything at all,
Eve must *measure*, and a measurement in a guessed base *disturbs* the qubit.
Her best strategy is **intercept-resend**: measure each qubit in a base she
guesses, then send on whatever state her measurement collapsed it to.

**A worked wiretapped exchange** — same fixed-seed machinery, now with Eve in
the middle (`bb84.exchange(seed=0, eavesdropper=True)`):

| # | Alice bit | Alice base | Eve base | Eve bit | Bob base | Bob bit | verdict |
|---|---|---|---|---|---|---|---|
| 0 | 1 | Z | Z | 1 | X | 0 | discarded (bases differ) |
| 1 | 1 | X | X | 1 | X | 1 | kept |
| 2 | 1 | X | X | 1 | X | 1 | kept |
| 3 | 0 | X | Z | 0 | X | 1 | kept — **disagrees** |
| 4 | 0 | X | X | 0 | Z | 0 | discarded (bases differ) |
| 5 | 0 | X | X | 0 | X | 0 | kept |
| 6 | 0 | X | X | 0 | X | 0 | kept |
| 7 | 0 | X | Z | 1 | Z | 1 | discarded (bases differ) |

Eve guessed wrong twice — rows 3 and 7. Follow row 3 in state arithmetic,
because it shows the whole detection in one qubit:

1. Alice sends bit `0` in the X base: `|−⟩`.
2. Eve guesses Z and measures. `|⟨0|−⟩|² = 1/2`: she reads `0` (this run),
   and her measurement **collapses the qubit to `|0⟩`** — Alice's `|−⟩` no
   longer exists anywhere. She resends `|0⟩`.
3. Bob measures in X (his base matches Alice's, so this position survives
   sifting). The qubit is now `|0⟩`, not `|−⟩`: he reads `1` with probability
   `|⟨−|0⟩|² = 1/2` — and does. Alice has `0`, Bob has `1`: **a key error.**

Row 7 shows the flip side: Eve guessed wrong there too (read `1`, resent `|1⟩`)
— but Bob's base (Z) differed from Alice's (X), so the position was discarded.
A corrupted bit in a discarded position is harmless.

The verdict: sifted positions `(1, 2, 3, 5, 6)`, so Alice's key is `11000` and
Bob's is `11100` — **1 of 5 bits wrong (20% this run)**.

**The 25% in general.** Take a kept bit — its position survived, so Alice and
Bob used the same base. That bit was tapped. Eve guesses the wrong base with
probability `1/2`. Given a wrong base (row-3 situation), Bob's outcome is a
coin flip, so his bit is wrong with probability `1/2`:

$$\underbrace{\tfrac{1}{2}}_{\text{Eve's base wrong}} \times \underbrace{\tfrac{1}{2}}_{\text{Bob's coin lands wrong}} = \tfrac{1}{4}$$

And a clean line is *exactly* 0: with nobody touching the qubits, every kept
bit passes through `H·H = I` untouched. Verified with the module's own
statistics over 200 exchanges of 8 qubits (`bb84.mean_error_rate`,
`bb84.error_distribution`, seed 10):

| Line | Mean sifted error rate | Error distribution (200 runs) |
|---|---|---|
| No eavesdropper | 0.000 | every run at 0 errors |
| Intercept-resend | 0.237 | 0 errors × 73, 1 × 74, 2 × 38, 3 × 13, 4 × 2 |

![A clean line vs. a wiretap](../assets/ch08-eavesdropper-error.png){ width="620" }

Two honest remarks about that distribution. First, 8 qubits is deliberately
tiny: in 73 of the 200 tapped runs Eve happened to leave 0 errors, so a single
short exchange does not *guarantee* catching her — it is the average that
separates (`0.000` vs `0.237`, about `0.96` errors on `4.0` kept bits per
exchange), and real keys are thousands of bits long, where a quarter is
unmissable. Second, the two distributions have different shapes, not just
different means: the clean line *piles up* at 0 and never moves; the tapped
line spreads around a quarter.

Alice and Bob finish by comparing a sample of their sifted bits over a public
channel. A few disagreements might be ordinary channel noise; a quarter is a
wiretap, so they throw the key away and try again.

??? question "Check yourself — why can't Eve copy the qubit, pass the original to Bob, and analyze her copy later?"
    The [no-cloning theorem](ch06-quantum-networking.md): an unknown quantum
    state cannot be duplicated. "Copy first, read later" needs Eve to know
    *what* to copy — but the copy operation would have to preserve the
    amplitudes of all four possible states without knowing which one was sent,
    and [Chapter 7](ch07-helloworld-explained.md) showed what a `CNOT` "copy"
    of a superposition really does: it entangles, it does not duplicate. So
    Eve's only route to information is to measure — and measuring in a guessed
    base collapses the qubit she must then resend. Disturbance is not a
    side-effect she can avoid; it is the only move she has.

??? question "Check yourself — could the 25% just be bad luck? Why can't Eve (or noise) explain a quarter of the key being wrong?"
    Noise cannot sit at 25%. Realistic channel noise is a few percent at
    worst, and the binomial arithmetic makes "noise produced a quarter"
    astronomically unlikely: even granting a generous 1% noise floor, the
    chance that ≥ 25 of 100 sifted bits flip by luck is about `10⁻²⁷` — and
    for 250 of 1000 bits it is too small for floating point to represent.
    Eve cannot average her way out either: the 25% comes from `1/2 × 1/2`,
    and every strategy that reads *more* of the key disturbs *more* of it.
    Alice and Bob compare a sample, see the rate, and refuse the key. The
    attack is not just detectable — it is unprofitable.

## The diagrams

### The Hadamard round trip

![The Hadamard round trip](../assets/ch08-haha-circuit.png){ width="420" }

![Entering a base and leaving it](../assets/ch08-haha-bloch.png){ width="620" }

`H·H = I`: the middle state is spread over all four outcomes (amplitude `±1/2`
each), and the last state is the `X` row again — a base entered and left for
free.

### The failed attempts

![Why bases must be reconciled](../assets/ch08-attempts-error.png){ width="560" }

Zero errors out of a base-less channel is not success — it is the absence of a
secret. The blind base lands near a quarter — a key that is wrong one bit in
four.

### Superposition: all sixteen states, then the same register back

![The four-qubit superposition circuit](../assets/ch08-superposition-circuit.png){ width="620" }

![A register in superposition, and the same register recovered](../assets/ch08-superposition-states.png){ width="620" }

Sixteen states at `1/16 = 0.0625` in the middle, the prepared `0110` at
probability 1.00 at both ends.

### BB84 and its wiretap

![One BB84 circuit](../assets/ch08-bb84-circuit.png){ width="620" }

Alice's preparation (an `X` for a `1`, a Hadamard for the X base), Bob's base
rotation, and the measurement.

![A clean line vs. a wiretap](../assets/ch08-eavesdropper-error.png){ width="620" }

The clean line piles up at 0 errors; the tapped line spreads around a quarter
of the sifted bits.

## Key takeaways

- A qubit carries a bit only relative to a **base**: the Z base holds
  `|0⟩`, `|1⟩`; the X base holds `|+⟩`, `|−⟩`. Same base = the bit with
  certainty (`|⟨0|0⟩|² = 1`); other base = a fair coin (`|⟨+|0⟩|² = 1/2`).
- `H·H = I` is the whole mechanics: the right base cancels (`H·H`), the wrong
  base leaves a lone `H` and a coin flip. A base is free to enter and leave —
  for the owner.
- A plain bit channel reads perfectly — by Bob **and** Eve. Zero errors is not
  secrecy; it is an unwatched conversation.
- A random base that is never reconciled gives Bob a quarter of bits wrong
  (`1/2 × 1/2`), and a superposition is a *rotation*, not a secret: the register
  truly spans all `2^n` states (amplitude `1/4`, probability `1/16` each for
  four qubits), but `H·H = I` returns it — and anyone who knows the rotation
  reads it.
- **BB84**: announce bases, never bits; keep the matches (about half — `4.0` of
  8 on average). Kept bits are identical with certainty, so an `N`-qubit
  exchange yields a shared key of about `N/2` bits.
- **No-cloning** forces Eve to measure, and a wrong-base measurement collapses
  the qubit she must resend. Her wrong half × their coin half = **~25%** of the
  sifted key wrong, where a clean line is exactly **0** — so the wiretap is
  detectable (and unprofitable), and Alice and Bob can refuse a compromised
  key.

## The code behind this chapter

Four samples, one per book section, plus a small shared model. Each prints a
tutorial panel and then the numbers to watch:

- [`ch08/identity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/identity.py)
  — the ``haha`` sample: `X` then `H`, `H`, and the state comes back (8.2).
  Watch the probability table: row 2 and row 4 are identical, row 3 is all
  `0.25`.
- [`ch08/attempts.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/attempts.py)
  — the ``naive`` and ``guess`` designs that fail. Watch the raw error rates:
  `0.00` for naive, `0.36` (64 qubits) for the blind base, with the long run
  closing in on `1/4`.
- [`ch08/superposition.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/superposition.py)
  — the ``superposition`` sample: all 16 states at `0.0625` after one `H` round,
  the prepared `0110` recovered after the second.
- [`ch08/bb84.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/bb84.py)
  — the working protocol: the 8-qubit sifting table, then the error-rate
  separation, `0.000` clean vs `0.237` tapped over 200 exchanges.
- [`ch08/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/protocol.py)
  — the shared qubit model: the four states, the one measurement rule (same
  base = the bit, other base = a fair coin), the sift, and the circuit worth
  drawing.

Run them all with `make ch08`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch08.bb84
```
