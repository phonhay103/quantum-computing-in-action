# Chapter 11 — Shor's algorithm

!!! abstract "In one sentence"
    Factoring is hard only because **order finding** is hard; a periodic
    superposition plus the **quantum Fourier transform** finds the order in
    polynomial time, and a couple of `gcd`s turn the order into the factors.

## Factoring, and why it is hard

Factoring a large number is the problem that made quantum computing famous. The
best classical methods — the **general number field sieve** — are
*sub-exponential*; Shor's algorithm is *polynomial*. The whole chapter is about
one reduction and one quantum circuit.

## Trial division: the honest classical baseline

The book starts with the naive method, because it is easy to trust: try 2, then
every odd number up to `√N`, and stop at the first divisor.

![Classical trial division: work grows like sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

It works, and it is hopeless: the loop runs about `√N` times, so a number with a
few hundred digits is already out of reach. Its value here is as the thing to beat.

## The reduction: factoring becomes order finding

Shor's insight is that you do not hunt for a factor directly. Pick `a` coprime to
`N` and look at the sequence

$$f(x) = a^x \bmod N$$

It is **periodic**. Call its period `r`. For `N = 15` and `a = 2` the values run
`1, 2, 4, 8, 1, 2, 4, 8, …` — the period is 4.

![The period of 2^x mod 15 is 4](../assets/ch11-period-function.png){ width="620" }

Once you know `r`, the factoring is a few `gcd` calls away:

1. if `r` is odd, or `a^(r/2) ≡ −1 (mod N)`, this `a` was unlucky — pick another
   and retry;
2. otherwise the two factors are `gcd(a^(r/2) − 1, N)` and `gcd(a^(r/2) + 1, N)`.

For `a = 2`, `r = 4`: `a^(r/2) = 4`, `gcd(4 − 1, 15) = 3`, and `15/3 = 5`. Done.

The book then checks the same arithmetic on a larger example by hand:

$$a = 6,\quad N = 493,\quad r = 112,\quad 6^{56} \bmod 493 = 407$$

so `gcd(407 − 1, 493) = 29` and `gcd(407 + 1, 493) = 17` — and indeed
`493 = 17 × 29`. The `jshell` snippets in the book's chapter 11 directory are those
two checks; `ch11.classical.reduction_steps(6, 493)` reproduces them in one call.

The catch: finding `r` classically is as hard as factoring, so this reduction buys
nothing *by itself*. What it does is isolate the one step a quantum computer can
do well — **order finding** — which is the rest of the chapter.

## The quantum Fourier transform

The period-finder is the **quantum Fourier transform** (QFT): the discrete Fourier
transform written as a circuit. On a basis state it spreads a phase ramp:

$$\mathrm{QFT}\,|k\rangle = \frac{1}{\sqrt{N}}\sum_j e^{2\pi i j k / N} |j\rangle$$

![The three-qubit QFT circuit](../assets/ch11-qft-circuit.png){ width="620" }

Feed it `|1⟩` and every output has the same magnitude, with a phase that sweeps
linearly from 0 to `2π`:

![QFT|1>: a uniform magnitude, a linear phase ramp](../assets/ch11-qft-phase.png){ width="620" }

The matrix is the familiar Fourier matrix `F[j, k] = e^(2πi j k / N)/√N` —
symmetric, **unitary**, and invertible by running the same circuit backwards. That
invertibility is the point: a *periodic* input is what the (inverse) QFT turns into
sharp peaks.

## Order finding: the period as peaks

Put the pieces together. Two registers:

- a **counting** register of `m` qubits, put into a uniform superposition with
  Hadamards — every exponent `x` at once;
- a **work** register, started at `|1⟩`, that records `a^x mod N` through
  controlled modular multiplications `|y⟩ → |a^(2^j)·y mod N⟩`.

The counting register now holds a **periodic** superposition, and the inverse QFT
turns that period into a handful of measurable peaks:

![A compact order-finding circuit](../assets/ch11-order-circuit.png){ width="620" }

![Inverse QFT of the periodic register: four peaks](../assets/ch11-order-peaks.png){ width="620" }

For `N = 15`, `a = 2` the peaks sit at `0, 64, 128, 192` — every `2^m / r = 256/4 =
64` apart. Read a peak as `k/r = outcome / 2^m` and run it through a
**continued-fraction** expansion:

| Measured | k/r = outcome / 2^m | Convergents | Period found |
|---|---|---|---|
| 0 | 0 | `0/1` | — (k = 0) |
| 64 | 1/4 | `0/1 → 1/4` | **4** |
| 128 | 1/2 | `0/1 → 1/2` | — (k not coprime to r) |
| 192 | 3/4 | `0/1 → 1/1 → 3/4` | **4** |

Two peaks give the answer directly. The other two have a numerator that shares a
factor with `r`, so the convergent gives a *divisor* of `r` — and the check
`a^r ≡ 1 (mod N)` rejects it. Shor simply looks at another peak. That is why the
algorithm repeats a measured run or two.

## Assembling Shor

| Step | What it does | Classical or quantum |
|---|---|---|
| Preprocess | pick `a`; `gcd(a, N) > 1` would already be a factor | classical |
| Hadamards | every exponent at once | quantum |
| Controlled modular multiplication | record `a^x mod N` in the work register | quantum |
| Inverse QFT | turn the period into peaks | quantum |
| Measure | read a peak | quantum |
| Continued fractions | recover `r` from the peak | classical |
| Guard and `gcd` | turn `r` into the factors | classical |

The quantum part is only in the middle. Everything before and after is arithmetic
that a laptop does instantly — which is why the chapter spent a whole module on the
classical reduction first.

!!! warning "Cost, honestly stated"
    Shor is **polynomial** in the number of bits, but the constant and the qubit
    count are large: factoring a 2048-bit number needs thousands of *logical*
    qubits and millions of gates, and those logical qubits need error correction
    (thousands of physical qubits each). The algorithm breaks our current public-key
    cryptography *in principle*; building the machine is the hard part, and this
    simulation only reaches `N` with a few bits before the register widths make it
    impractical.

## The diagrams

### The classical baseline

![Classical trial division: work grows like sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

![The period of 2^x mod 15 is 4](../assets/ch11-period-function.png){ width="620" }

### The quantum Fourier transform

![The three-qubit QFT circuit](../assets/ch11-qft-circuit.png){ width="620" }

![QFT|1>: a uniform magnitude, a linear phase ramp](../assets/ch11-qft-phase.png){ width="620" }

### Order finding

![A compact order-finding circuit](../assets/ch11-order-circuit.png){ width="620" }

![Inverse QFT of the periodic register: four peaks](../assets/ch11-order-peaks.png){ width="620" }

## Key takeaways

- Classical factoring costs about `√N` by trial division, and sub-exponential by the
  number field sieve; Shor's algorithm is **polynomial**.
- Factoring reduces to **order finding**: the period `r` of `a^x mod N` gives the
  factors through `gcd(a^(r/2) ± 1, N)`, retrying if `r` is odd or `a^(r/2) ≡ −1`.
- The **QFT** is the Fourier transform as a circuit: unitary, invertible, and it
  turns a *periodic* register into a few sharp **peaks** at multiples of `2^m / r`.
- **Order finding** prepares a periodic superposition with controlled modular
  multiplications and reads the period off the peaks of the inverse QFT.
- Recovering `r` is classical: **continued fractions** of `outcome / 2^m`, checked
  against `a^r ≡ 1 (mod N)`.
- Shor is polynomial, but the resource counts are enormous; the algorithm matters
  because of *what* it makes cheap, and error correction is what makes it real.

## The code behind this chapter

Three samples, from the classical baseline to the algorithm:

- [`ch11/classical.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/classical.py)
  — the ``classicfactor`` and ``semiclassicfactor`` samples: trial division, the
  reduction, `gcd(a^(r/2) ± 1, N)`, and the classical period search.
- [`ch11/qft.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/qft.py)
  — the quantum Fourier transform, its circuit, its matrix, and the phase ramp it
  puts on `|1⟩`.
- [`ch11/shor.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/shor.py)
  — the ``quantumfactor`` sample: modular multiplication, the order-finding
  circuit, the inverse QFT, continued fractions, and the factors of 15 and 21.

Run them all with `make ch11`, or one at a time:

```bash
uv run python -m quantum_computing_in_action.ch11.shor
```
