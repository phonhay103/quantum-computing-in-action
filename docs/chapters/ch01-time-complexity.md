# Chapter 1 — Factoring time complexity

!!! abstract "In one sentence"
    Quantum computers matter because **Shor's algorithm factors large numbers in
    polynomial time**, while the best known classical algorithm needs
    *exponential* time — and modern encryption assumes that fact is hard.

## Why factoring is the hook

Much of the internet's security, including **RSA**, rests on a simple
asymmetry: multiplying two large primes is easy, but *undoing* that
multiplication — factoring the product back into its primes — is believed to be
very hard. "Hard" here is measured in **time**: how the work grows as the number
gets bigger.

If factoring suddenly became fast, a lot of encryption would become fast to
break. This chapter is about *how much* faster a quantum computer can make it.

## Measuring difficulty: how cost grows with size

Let `b` be the number of bits in the number we want to factor. As `b` grows, we
care less about the exact seconds and more about the **shape** of the growth:

| Growth | Name | Intuition |
|--------|------|-----------|
| grows like `b`, `b²`, `b³` … | **polynomial** | Doubling `b` multiplies the work by a small constant factor — manageable |
| grows like `2^b`, `e^b` … | **exponential** | Adding *one* bit can roughly double the work — quickly hopeless |

The whole promise of quantum computing, in this chapter, is a jump from the
second row to the first.

## The classical cost

The best known classical method for factoring is the **general number field
sieve (GNFS)**. Its running time is roughly

$$e^{\left(\tfrac{64}{9}\,b\,(\ln b)^2\right)^{1/3}}$$

The key detail is the `(ln b)^2` inside the root: the exponent grows with `b`,
which makes the whole expression grow **super-polynomially**. Adding bits does
not just add work — it multiplies it, again and again.

Practical consequence: every few extra bits of key length make classical
factoring dramatically more expensive. That is why keys of 2048 bits are
considered safe today.

## Shor's cost

Shor's algorithm factors in **polynomial time**, about

$$b^3$$

Cubic growth is gentle by comparison. Going from a 1024-bit number to a
2048-bit one multiplies the work by roughly `2³ = 8`, whereas the classical
method explodes far more violently.

!!! warning "Reality check"
    "Polynomial" is not the same as "easy today". Shor still needs a large,
    error-corrected quantum computer. The chapter is about the *asymptotic
    promise*, not about breaking RSA on current hardware.

## The diagram

![Classical vs. Shor factoring time](../assets/ch01-time-complexity.png){ width="560" }

The chart plots both estimates against the number of bits:

- The **classical** curve (yellow) climbs steeply — it is the exponential wall.
- The **Shor** curve (green) stays low and almost flat by comparison — this is
  the polynomial path.

The widening gap between the two curves *is* the quantum speed-up.

## What the sample shows

When you run the chapter it prints a table of estimates for 4, 8, 16, 32 and
64 bits. Reading down the columns makes the two growth rates concrete: the
classical column balloons to enormous numbers while the Shor column stays
comparatively modest. The figure above is the same story as a picture.

## Key takeaways

- Factoring difficulty is where quantum computing's reputation begins.
- Classical GNFS is **super-polynomial**; Shor is **polynomial** (`b³`).
- The speed-up is about *asymptotic growth*, not present-day machines.
- This is exactly why post-quantum cryptography is an active field.

## The code behind this chapter

The sample that produces the table and the figure lives in
[`src/quantum_computing_in_action/ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py).
Run it with `make ch01`.
