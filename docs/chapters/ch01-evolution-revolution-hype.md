# Chapter 1 — Evolution, revolution, or hype?

!!! abstract "In one sentence"
    Quantum computing is a genuine **evolution** of computing, but it is not a
    drop-in replacement: it matters because **Shor's algorithm factors large
    numbers in polynomial time**, while the best known classical algorithm needs
    *super-polynomial* (sub-exponential) time — and modern encryption assumes
    that fact is hard.

## The evolution of computing

Classical computing has grown for decades by making transistors smaller: more
switches, faster clocks, cheaper work. That run is slowing down. Transistors are
now a few atoms wide, and shrinking further runs into heat and quantum effects.

Quantum computing is the next step in that evolution, but it changes the *kind*
of machine we build. Instead of more classical switches, it uses **qubits** and
the rules of quantum mechanics — superposition, interference, and entanglement —
to compute in ways a classical computer cannot imitate efficiently.

## Revolution or hype?

Both words get used, so it helps to separate the two:

| Claim | Verdict |
|-------|---------|
| "Quantum computers are faster at everything" | **Hype** — for most everyday tasks they are not |
| "Some specific problems get a dramatic speed-up" | **Revolution** — factoring, search, simulation |
| "You can use one today for production" | **Hype** — today's machines are small and noisy |
| "The theory is sound and improving fast" | **Revolution** — the algorithms are real |

The honest summary: a **revolution for a narrow set of problems**, not a
universal speed-up. Knowing *which* problems is the whole point of this book.

## Where quantum computers help

The applications that motivate the field fall into a few families:

- **Cryptography** — Shor's algorithm breaks RSA-style public-key encryption;
  quantum key distribution and post-quantum crypto respond to that threat.
- **Simulation** — molecules and materials are quantum systems; a quantum
  computer can model them natively (chemistry, drug discovery, materials). A
  quantum system with `n` qubits lives in a space of `2^n` amplitudes, which is
  what makes exact classical simulation so expensive.
- **Search and optimisation** — Grover's algorithm speeds up unstructured
  search and many optimisation problems.
- **Sampling and machine learning** — still early, but an active area.

The first three are the ones with the clearest algorithmic advantage, and they
are exactly the algorithms this book walks through.

A related idea the book uses is **hybrid computing**: a small quantum device
handles the part where quantum rules win, and a classical computer drives the
rest. Speed-ups are not all equal either — Shor's is **exponential**, while
Grover's search is only **quadratic** — so "faster" always needs a qualifier.

## Why factoring is the hook

Much of the internet's security, including **RSA**, rests on a simple
asymmetry: multiplying two large primes is easy, but *undoing* that
multiplication — factoring the product back into its primes — is believed to be
very hard. "Hard" here is measured in **time**: how the work grows as the number
gets bigger.

!!! note "What RSA relies on"
    In RSA, your public key contains a number `N = p · q` that is the product of
    two large primes. Anyone can encrypt a message using `N`, but decrypting it
    needs `p` and `q` — that is, it needs the factors of `N`. As long as
    factoring `N` is hard, the key stays safe. Shor's algorithm threatens exactly
    this assumption.

If factoring suddenly became fast, a lot of encryption would become fast to
break. This is the most dramatic example of the evolution/revolution question, so
the chapter starts here.

## Measuring difficulty: how cost grows with size

Let `b` be the number of bits in the number we want to factor. As `b` grows, we
care less about the exact seconds and more about the **shape** of the growth
(see [growth rates and Big-O](../foundations.md#growth-rates-and-big-o) in the
foundations):

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

This is the book's simplified estimate of GNFS. The key detail is the
`(ln b)^2` inside the root: the exponent grows with `b`, which makes the whole
expression grow **super-polynomially**. Adding bits does not just add work — it
multiplies it, again and again. Strictly speaking, GNFS is **sub-exponential** —
faster than a full exponential but still far beyond any polynomial.

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
    error-corrected quantum computer. Today's machines are **NISQ** — noisy,
    intermediate-scale, and not error-corrected — so they use many *physical*
    qubits to encode one reliable **logical** qubit. The chapter is about the
    *asymptotic promise*, not about breaking RSA on current hardware.

## The diagrams

The book draws **two** charts: one comparing both algorithms, and one showing the
classical curve on its own so its shape is not hidden by the much lower Shor
curve.

![Classical vs. Shor factoring time](../assets/ch01-time-complexity.png){ width="520" }

![The classical curve on its own](../assets/ch01-time-complexity-classical.png){ width="520" }

- The **classical** curve (yellow) climbs steeply — it is the super-polynomial wall.
- The **Shor** curve (green) stays low and almost flat by comparison — this is
  the polynomial path.

The widening gap between the two curves *is* the quantum speed-up.

## What the sample shows

When you run the chapter it prints a table of estimates for 4, 8, 16, 32 and
64 bits. Reading down the columns makes the two growth rates concrete: the
classical column balloons to enormous numbers while the Shor column stays
comparatively modest. The figures above tell the same story as a picture.

## Key takeaways

- Quantum computing is an **evolution** with a **revolutionary** speed-up for a
  narrow set of problems — not a universal faster computer.
- The clearest wins are cryptography, quantum simulation, and search.
- Classical GNFS is **super-polynomial**; Shor is **polynomial** (`b³`).
- The speed-up is about *asymptotic growth*, not present-day machines.
- This is exactly why post-quantum cryptography is an active field.

## The code behind this chapter

The sample that produces the table and the figures lives in
[`src/quantum_computing_in_action/ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py).
Run it with `make ch01`.
