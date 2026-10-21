# Chapter 1 — Evolution, revolution, or hype?

!!! abstract "In one sentence"
    Quantum computing matters for one reason: **Shor's algorithm factors large
    numbers in polynomial time**, while the best classical algorithm needs
    sub-exponential time — and modern encryption relies on factoring being
    hard. In other words, the security of widely deployed cryptosystems
    currently rests on a computational difficulty assumption that a quantum
    algorithm undermines, at least in principle.

## The evolution of computing

Classical computing has advanced for decades along a single dominant
strategy: making transistors ever smaller. Smaller transistors mean more
switches per chip, faster clock rates, and cheaper computation per operation,
and it is this combination that has produced the steady performance growth
familiar from the history of the field. That run, however, is slowing down.
Transistor features are now only a few atoms wide, and pushing them further
runs into two obstacles at once: the heat generated per unit area becomes
difficult to dissipate, and at atomic scales quantum effects begin to
interfere with the reliable operation of a switch that is supposed to behave
purely classically.

Quantum computing is the next step in that evolution, but it changes the
*kind* of machine being built rather than merely its size. Instead of adding
more classical switches, it employs **qubits** together with the rules of
quantum mechanics — superposition, interference, and entanglement — to
compute in ways that a classical computer cannot imitate efficiently. It is
worth noting that these three notions are not decorative extras: each one is
a computational resource, and each is unpacked in its own right in a later
chapter, namely Chapters 2, 4, and 5.

## Revolution or hype?

Both labels circulate freely in public discussion of the field, so it helps
to separate the two before using either. The table below presents each claim
in the form in which it is typically heard, together with the verdict that a
fair reading of the available evidence supports:

| Claim | Verdict |
|-------|---------|
| "Quantum computers are faster at everything" | **Hype** — for most everyday tasks a quantum machine offers no advantage |
| "Some specific problems get a dramatic speed-up" | **Revolution** — factoring, search, and simulation genuinely accelerate |
| "You can use one today for production" | **Hype** — today's machines are small, noisy, and unsuited to production workloads |
| "The theory is sound and improving fast" | **Revolution** — the algorithms are mathematically rigorous and well established |

The honest summary is that quantum computing constitutes a **revolution for
a narrow set of problems**, not a universal speed-up for computation in
general. Identifying precisely *which* problems belong to that narrow set
is, in fact, the central purpose of this book.

## Where quantum computers help

The applications that originally motivated the field fall into a small
number of families, each of which is anchored by a concrete algorithmic
result:

- **Cryptography** — Shor's algorithm breaks RSA-style public-key encryption
  once a sufficiently large quantum computer is available; quantum key
  distribution and post-quantum cryptography are the two main responses
  developed to counter that threat.
- **Simulation** — molecules and materials are themselves quantum systems,
  and a quantum computer can therefore model them natively (this covers
  chemistry, drug discovery, and materials science). A quantum system with
  `n` qubits lives in a space of `2^n` amplitudes, and it is precisely this
  exponential state space that makes exact classical simulation so
  expensive.
- **Search and optimisation** — Grover's algorithm speeds up unstructured
  search, along with many related optimisation problems.
- **Sampling and machine learning** — this family is still at an early
  stage, but it remains an active area of research.

The first three families exhibit the clearest algorithmic advantage, and
they correspond exactly to the algorithms this book develops and walks
through in detail.

A related idea that the book uses throughout is **hybrid computing**: a
small quantum device handles only the part of the computation where the
quantum rules confer an advantage, while a classical computer drives
everything else — typically pre-processing, control, and post-processing.

Speed-ups, moreover, are not all of the same magnitude. Shor's advantage is
**exponential**. Grover's, by contrast, is only **quadratic** — it cuts an
`N`-step search down to about `√N` steps, which is a square-root improvement
rather than an exponential one. For this reason, every statement that a
quantum computer is "faster" requires a qualifier specifying how much faster,
and for which problem.

## Why factoring is the hook

Much of the internet's security, including **RSA**, rests on a simple
asymmetry: multiplying two large primes is easy, but *undoing* that
multiplication — factoring the product back into its primes — is believed to
be very hard. "Hard" is to be understood here in a specific sense: it is
measured in **time**, that is, by how the required work grows as the number
to be factored gets bigger.

!!! note "What RSA relies on"
    In RSA, the public key contains a number `N = p · q` that is the product
    of two large primes. Anyone can encrypt a message using `N`, but
    decrypting it requires `p` and `q` — that is, decryption requires the
    factors of `N`. As long as factoring `N` remains hard, the key remains
    safe. Shor's algorithm threatens exactly this assumption.

If factoring were to become fast, a great deal of deployed encryption would
consequently become fast to break. This is the most dramatic embodiment of
the evolution/revolution question, which is why the chapter starts here.

## Measuring difficulty: how cost grows with size

Let `b` denote the number of bits of the number to be factored. As `b`
grows, the exact number of seconds involved matters less than the **shape**
of the growth (see
[growth rates and Big-O](../foundations.md#growth-rates-and-big-o) in the
foundations, where these notions are defined more formally):

| Growth | Name | Intuition |
|--------|------|-----------|
| grows like `b`, `b²`, `b³` … | **polynomial** | Doubling `b` multiplies the total work by a small constant factor — the growth stays manageable |
| grows like `2^b`, `e^b` … | **exponential** | Adding *one* bit can roughly double the work — the difficulty quickly becomes hopeless |
| sits between the two | **sub-exponential** | Faster than any polynomial, yet slower than a true exponential |

The entire promise of quantum computing, as this chapter frames it, is a
jump from the bottom rows of this table to the top one.

## The classical cost

The best known classical method for factoring is the **general number field
sieve (GNFS)**. Its running time is roughly

$$e^{\left(\tfrac{64}{9}\,b\,(\ln b)^2\right)^{1/3}}$$

This is the book's simplified estimate of GNFS. The decisive detail is the
`(ln b)^2` factor inside the root: the exponent itself grows with `b`, and
it is this feature that makes the whole expression grow **sub-exponentially**.

"Sub-exponential" is a precise term, and it is *not* synonymous with
"super-polynomial". *Super-polynomial* states only that the work grows
faster than every polynomial. *Sub-exponential* states that **and** that it
still grows more slowly than a true exponential such as `2^b` — the growth
sits between the two regimes. Both descriptions hold for GNFS, and the
second is the stronger (more informative) claim, because it supplies an
upper bound in addition to a lower one. The practical effect is that adding
bits does not merely add work; it *multiplies* the work — again and again.

The practical consequence is that every few additional bits of key length
make classical factoring dramatically more expensive. For this reason, keys
of 2048 bits are considered safe today.

## Shor's cost

Shor's algorithm factors in **polynomial time**, about

$$b^3$$

Cubic growth is gentle by comparison. Going from a 1024-bit number to a
2048-bit one multiplies the work by roughly `2³ = 8`, whereas the classical
method explodes far more violently over the same doubling.

!!! warning "Reality check"
    "Polynomial" is not the same as "easy today". Shor still requires a
    large, error-corrected quantum computer. Today's machines are **NISQ** —
    *Noisy Intermediate-Scale Quantum*: a few hundred error-prone qubits with
    no error correction at all. Such devices spend many *physical* qubits to
    encode one reliable **logical** qubit. This chapter is therefore about
    the *asymptotic promise*, not about breaking RSA on current hardware.

## The diagrams

The book draws **two** charts: one comparing both algorithms on the same
axes, and one showing the classical curve on its own, so that its shape is
not visually dominated by the much lower Shor curve.

![Classical vs. Shor factoring time](../assets/ch01-time-complexity.png){ width="520" }

![The classical curve on its own](../assets/ch01-time-complexity-classical.png){ width="520" }

- The **classical** curve (yellow) climbs steeply — that is the
  sub-exponential wall.
- The **Shor** curve (green) stays low and almost flat by comparison — this
  is the polynomial path.

It is precisely the widening gap between the two curves that *is* the
quantum speed-up.

## What the sample shows

When the chapter's program is executed, it prints a table of estimates for
4, 8, 16, 32 and 64 bits. Reading down the columns makes the two growth
rates concrete: the classical column balloons to enormous numbers, while the
Shor column stays comparatively modest. The figures above tell the same
story in pictorial form.

## Key takeaways

- Quantum computing is an **evolution** in hardware terms combined with a
  **revolutionary** speed-up for a narrow set of problems — it is not a
  universally faster computer.
- The clearest advantages lie in cryptography, quantum simulation, and
  search.
- Classical GNFS is **sub-exponential**; Shor's algorithm is **polynomial**
  (`b³`).
- The speed-up concerns *asymptotic growth*, not present-day machines.
- This is exactly why post-quantum cryptography is an active field of
  research.

## The code behind this chapter

The sample that produces the table and the figures lives in
[`src/quantum_computing_in_action/ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py).
It can be run with `make ch01`.
