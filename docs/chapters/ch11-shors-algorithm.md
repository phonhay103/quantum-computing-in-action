# Chapter 11 — Shor's algorithm

!!! abstract "In one sentence"
    Factoring is hard only because **order finding** is hard; a periodic
    superposition plus the **quantum Fourier transform** finds the order in
    polynomial time, and a couple of `gcd`s turn the order into the factors.

## The question this chapter answers

Multiplying two primes is instant: `3 × 5 = 15`, done. Going backwards — given
`15`, recover `3` and `5` — is believed to be hopeless for large numbers, and
RSA-style public-key cryptography rests exactly on that gap. Shor's algorithm
is the famous quantum crack in it, and this chapter asks the three questions
you need in order to understand it honestly:

1. **Why is factoring the problem everyone cares about, and what makes it
   hard?** The honest baseline is the trial division you learned in school —
   try `2`, then `3`, then `5`, … It works, and it dies by the square root:
   work grows with `√N`, so a number twice as long costs astronomically more.
2. **What does factoring have to do with periods?** Shor's reduction: do not
   hunt for a factor directly. Find the period `r` of the sequence
   `a^x mod N`, and the factors fall out of two `gcd` calls. We work it fully
   for `N = 15`, then on the book's larger example `N = 493`.
3. **How does a quantum computer find a period?** A superposition evaluates
   `a^x mod N` for *every* `x` at once, and the quantum Fourier transform is
   the piece that turns that hidden repetition into a few sharp, measurable
   peaks. Reading one peak recovers `r` — and `r` cracks `N`.

After this chapter you will be able to:

- factor `15` by trial division and say exactly *when* that method dies;
- turn a period into factors with two `gcd` calls, and explain why an odd
  period means "unlucky, pick another `a`";
- explain the QFT as "counting how often a pattern repeats", with worked
  numbers showing where the peaks land;
- walk through the whole algorithm for `N = 15`, naming which steps are
  classical and which are genuinely quantum.

You need four things from earlier chapters, each in one line: `H` puts a
register into an even superposition of all its values at once, and
measurement picks one outcome with probability = amplitude²
([Chapter 4](ch04-superposition.md)); a controlled gate acts on its target
only when its control is `1` ([Chapter 3](ch03-qubits-and-gates.md)); a
circuit is a program — an ordered list of steps you can read gate by gate
([Chapter 7](ch07-helloworld-explained.md)); and an oracle computes `f` on
every input at once inside one superposition ([Chapter 9](ch09-deutsch-jozsa.md)).

!!! note "One bit of bookkeeping: the words and the notation"
    - `x mod N` is the *remainder* after dividing `x` by `N`: `16 mod 15 = 1`.
      "Multiply mod N" just means "keep only the remainder".
    - `gcd(u, v)` is the largest number dividing both: `gcd(12, 15) = 3`.
      If `gcd(a, N) = 1`, then `a` and `N` are **coprime** — they share no
      factor.
    - The **period** of `a` modulo `N` — also called the **order** — is the
      smallest `r ≥ 1` with `a^r mod N = 1`. The whole chapter hunts this one
      number.
    - Two registers throughout: the **counting** register holds the exponent
      `x`; the **work** register holds the value `a^x mod N`. A measured
      counting-register value `s` is always read as the fraction
      `s / 2^m ≈ k / r`.

## Factoring, and why it is hard

Every number is a product of primes. For small numbers you can see the factors;
for a 600-digit number, nobody knows how to find them. The best classical
method — the **general number field sieve** — is still *sub-exponential*: its
cost grows almost like `2^bits`. Shor's algorithm is *polynomial*, which is the
whole fame of quantum computing in one sentence.

But before admiring the quantum answer, build the classical one and watch it
fail. That is what the chapter (and the `ch11.classical` module) does first —
because Shor's algorithm *is* the classical method with one step swapped out,
and you cannot see which step until you have the classical method in hand.

## Trial division: the honest classical baseline

The naive method is easy to trust because you can check every move. To factor
`N`: try `2`, then every odd number `3, 5, 7, …`, and stop at the first one
that divides `N`.

**Worked: `N = 15`.**

- try `2`: `15 = 2 × 7 + 1` — remainder `1`, not a divisor;
- try `3`: `15 = 3 × 5` — remainder `0`. Factor found: `3`, and its partner
  is `15 / 3 = 5`.

Two divisions, answer `15 = 3 × 5`. The module reports exactly this:
`trial_division(15) = 3` after `steps_to_factor(15) = 2` divisions.

**Worked: `N = 91`.**

- `2`: `91 = 2 × 45 + 1` — no;
- `3`: `91 = 3 × 30 + 1` — no;
- `5`: `91 = 5 × 18 + 1` — no;
- `7`: `91 = 7 × 13` — yes.

Four divisions, answer `91 = 7 × 13`.

![Classical trial division: work grows like sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

**The general rule, and why it dies.** You only ever need to try divisors up to
`√N`, because divisors come in pairs: if `d` divides `N`, so does `N / d`, and
the smaller of the pair is never above `√N`. (For `91`: `√91 ≈ 9.5`, and the
smallest factor `7` is below it; had nothing divided `91` by then, `91` would
be prime.) That is the good news — and it is also the death sentence, because
the loop still runs about `√N` times:

| `N` | digits | trial divisions (`steps_to_factor`) |
|---|---|---|
| `15` | 2 | 2 |
| `91` | 2 | 4 |
| `999983` (prime) | 6 | 500 |
| `999999999989` (prime) | 12 | 500 000 |

Doubling the number of digits multiplies the work by about `1000`, because
`√10^6 ≈ 10^3` becomes `√10^12 = 10^6`. The worst case below `200` in the
module's `steps_curve` is `N = 169 = 13²` at 7 divisions — the curve is almost
flat at this scale, and a 600-digit RSA modulus would need about `10^300`.
Trial division is not the best classical method, but *every* known classical
method explodes like this; only the exponent differs.

## The reduction: factoring becomes order finding

Shor's insight is that you do not hunt for a factor directly. You hunt for a
hidden rhythm in a sequence, and the factors fall out of it.

Pick any `a` coprime to `N` — say `a = 2`, `N = 15` — and look at the sequence

$$f(x) = a^x \bmod N = 2^x \bmod 15$$

Computed one step at a time (each entry is the previous one times `2`, keep
the remainder):

| `x` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| `2^x mod 15` | 1 | 2 | 4 | 8 | 1 | 2 | 4 | 8 | 1 |

`1, 2, 4, 8`, then `1` again. The sequence is **periodic** with period
`r = 4`: the smallest `r` with `2^r mod 15 = 1` (indeed `2^4 = 16 = 1 × 15 + 1`).

![The period of 2^x mod 15 is 4](../assets/ch11-period-function.png){ width="620" }

**Why the period gives the factors — worked.** We need one algebraic identity:
difference of two squares.

$$a^r - 1 = \left(a^{r/2} - 1\right)\left(a^{r/2} + 1\right)$$

Since `a^r mod N = 1`, the number `N` divides `a^r − 1`, so `N` divides the
product of the two brackets. For `a = 2`, `r = 4`, `N = 15`:

- `a^(r/2) = 2^(4/2) = 2^2 = 4`;
- `a^r − 1 = 16 − 1 = 15 = (4 − 1)(4 + 1) = 3 × 5` — the brackets *are* the
  factors here;
- `gcd(4 − 1, 15) = gcd(3, 15) = 3` and `gcd(4 + 1, 15) = gcd(5, 15) = 5`.

**The general rule.** Given the period `r` of `a` mod `N`:

1. if `r` is odd, or `a^(r/2) ≡ −1 (mod N)`, this `a` was unlucky — pick
   another `a` and retry;
2. otherwise the two factors of `N` are `gcd(a^(r/2) − 1, N)` and
   `gcd(a^(r/2) + 1, N)`.

Both guards exist because `N` must split *between* the two brackets. If `N`
divided one bracket entirely, that bracket is `≡ 0` or `≡ −1` and its `gcd`
gives the trivial answer (`1` or `N`) — no information. The unlucky cases are
real: for `a = 2`, `N = 7` the sequence is `2, 4, 1` with `r = 3` (odd —
`a^(r/2)` is not even an integer power); and for `a = 2`, `N = 5` the period
`r = 4` is even but `2^2 = 4 ≡ −1 (mod 5)`, so `gcd(3, 5) = 1` and
`gcd(5, 5) = 5` — nothing learned. Retry with another `a`.

**The book's larger example, fully worked.** `a = 6`, `N = 493` (the numbers
the book's `jshell` snippets check; `reduction_steps(6, 493)` reproduces them):

- the period of `6 mod 493` is `r = 112`;
- `6^(r/2) = 6^56 mod 493 = 407`;
- `gcd(407 − 1, 493) = gcd(406, 493) = 29`;
- `gcd(407 + 1, 493) = gcd(408, 493) = 17`;
- and indeed `493 = 17 × 29`.

**The catch.** Finding `r` by brute force — multiplying `a` by itself until the
remainder comes back to `1` — costs up to `r` multiplications, and `r` can be
as large as `N`. It is *as hard as factoring*, so the reduction by itself buys
nothing. What it does is isolate the one step a quantum computer can do well:
**order finding**. Everything else in Shor's algorithm is the classical
arithmetic you just read.

??? question "Check yourself — why must `a` be coprime to `N`?"
    If `gcd(a, N) = d > 1` then `d` **already is a factor** — e.g. `a = 5`,
    `N = 15`: `gcd(5, 15) = 5`, done, no quantum computer needed. Worse, the
    sequence `a^x mod N` would never return to `1` (every power of `a` still
    shares the factor `d`), so there would be no period to find. That is why
    Shor's first step computes `gcd(a, N)`: it either finishes the job
    instantly or proves that `a` is usable.

??? question "Check yourself — the period of `4 mod 21` is `r = 3`, odd. Why is that 'unlucky', and what does Shor do?"
    The whole trick factors `a^r − 1` into the two brackets `a^(r/2) ± 1`, and
    with `r = 3` the exponent `r/2 = 1.5` is not a whole number — the
    brackets never exist. Shor simply picks another `a`. For `N = 21`, retrying
    with `a = 2` gives the even period `r = 6`, `2^3 mod 21 = 8`, and
    `gcd(7, 21) = 7`, `gcd(9, 21) = 3` — so `21 = 3 × 7`. (Check the
    unlucky case by hand: `4, 16, 64 = 3 × 21 + 1` — three steps back to `1`.)

## The quantum Fourier transform

The plain-language goal of this section: **counting how often a pattern
repeats**. A Fourier transform — the same mathematics that tells you a guitar
string vibrates 440 times a second — takes a signal and answers "how often
does this repeat?". The **quantum Fourier transform** (QFT) is the discrete
Fourier transform written as a circuit, so a quantum register can ask that
question about its own amplitudes.

![The three-qubit QFT circuit](../assets/ch11-qft-circuit.png){ width="620" }

**Worked: a list repeating every 4.** Take `m = 4` qubits, i.e. a list of
`2^4 = 16` amplitudes. Put amplitude `1/2` at positions `0, 4, 8, 12` and `0`
everywhere else — a pattern that repeats every `r = 4` positions. (This is
exactly the shape the counting register will have in the next section.) Apply
`qft_matrix(4)` and look at the probabilities of the 16 outcomes:

| outcome `s` | 0 | 4 | 8 | 12 | every other `s` |
|---|---|---|---|---|---|
| probability | 0.25 | 0.25 | 0.25 | 0.25 | 0 |

All the weight landed on **four sharp peaks**, and their positions read as
fractions of the whole range:

$$\frac{0}{16} = 0,\qquad \frac{4}{16} = \frac{1}{4},\qquad
\frac{8}{16} = \frac{1}{2},\qquad \frac{12}{16} = \frac{3}{4}$$

Multiples of `1/4` — and `4` was the period. That is the entire trick: **the
period moved from the *spacing* of the pattern into the *positions* of the
peaks**, and peak positions are things you can measure.

**Why it works.** Each output amplitude is a sum of phase-stepped copies of the
input, one copy per nonzero entry. At output `s`, consecutive copies (which
live 4 positions apart) differ by a phase step of `e^{2πi·4·s/16} = e^{πis/2}`.
When `s` is a multiple of `16/4 = 4` — at `s = 0, 4, 8, 12` — that step is a
whole number of turns, all copies point the same way, and they add up. At every
other `s` the copies rotate around the circle and cancel: e.g. at `s = 1` the
four copies point at `0°, 90°, 180°, 270°` — a full set of compass
directions that sums to zero. The peaks are constructive interference; the
silence everywhere else is destructive interference.

![QFT|1>: a uniform magnitude, a linear phase ramp](../assets/ch11-qft-phase.png){ width="620" }

**On a single basis state, the same circuit does something you can write in a
table.** The QFT of `|k⟩` spreads a **phase ramp** across all outputs:

$$\mathrm{QFT}\,|k\rangle = \frac{1}{\sqrt{N}}\sum_j e^{2\pi i j k / N} |j\rangle$$

Feed the three-qubit circuit `|1⟩` (`k = 1`, `N = 8`) and every output gets the
same magnitude `1/√8 ≈ 0.354`, while the phase climbs by `2π/8 = π/4` per step
— measured by `phase_ramp(3)`:

| `j` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| phase (in units of π) | 0 | 0.25 | 0.50 | 0.75 | 1.00 | −0.75 | −0.50 | −0.25 |

The last three entries have passed `π` and are printed wrapped into
`(−π, π]`: the phase `−0.75π` is the same point on the circle as `1.25π`. The
ramp climbs steadily; only the label wraps.

The matrix behind all of this is the familiar Fourier matrix
`F[j, k] = e^(2πi j k / N)/√N` — symmetric, **unitary**, and invertible by
running the same circuit backwards (`qft_circuit(n, inverse=True)`). The
unitarity is not decoration: it is why the (inverse) QFT can sit inside a
quantum algorithm at all, and it is the (inverse) QFT that Shor applies — a
*periodic* register is what it turns into the sharp peaks above.

## Order finding: the period as peaks

Now assemble the period-finder. The circuit uses **two registers**, and each
has one plain-language job:

- the **counting register** — `m` qubits — *counts* `x = 0, 1, 2, …`. Hadamards
  put it into an even superposition of **every exponent at once** (`2^m` of
  them);
- the **work register** — enough qubits to hold `N` — *holds the value*
  `f(x) = a^x mod N`. It starts at `|1⟩`, and controlled modular
  multiplications `|y⟩ → |a^(2^j)·y mod N⟩` write `f` into it: counting-qubit
  `j` multiplies the work register by `a^(2^j)` when it is `1`.

This is the Deutsch–Jozsa pattern again ([Chapter 9](ch09-deutsch-jozsa.md)):
one circuit evaluates `f` on every input at once. For `a = 2`, `N = 15`,
`m = 8`: the counting register holds all `256` exponents, and the work register
holds `2^x mod 15` next to each one — the periodic sequence
`1, 2, 4, 8, 1, 2, 4, 8, …` written across a superposition.

![A compact order-finding circuit](../assets/ch11-order-circuit.png){ width="620" }

Measuring the work register would collapse it to one value — useless. Instead
the circuit applies the **inverse QFT** to the counting register, and the
period hidden in it becomes readable peaks:

![Inverse QFT of the periodic register: four peaks](../assets/ch11-order-peaks.png){ width="620" }

`order_distribution(2, 15)` gives the exact numbers. The counting register
(`m = 8`, so `2^m = 256` outcomes) shows **four peaks**, each with probability
`0.25`, at

$$0,\quad 64,\quad 128,\quad 192 \qquad\text{— spaced } \frac{2^m}{r} = \frac{256}{4} = 64 \text{ apart.}$$

Read a peak as the fraction `k/r = outcome / 2^m` and run it through a
**continued-fraction** expansion (Euclid's algorithm on `outcome` and `2^m`;
each quotient peels off one digit of the fraction):

| Measured | `k/r = outcome / 2^m` | Convergents | Period found |
|---|---|---|---|
| 0 | 0 | `0/1` | — (`k = 0`, no information) |
| 64 | `64/256 = 1/4` | `0/1 → 1/4` | **4** |
| 128 | `128/256 = 1/2` | `0/1 → 1/2` | — (`2^2 = 4 ≠ 1`, check fails) |
| 192 | `192/256 = 3/4` | `0/1 → 1/1 → 3/4` | **4** |

Worked, for `outcome = 64`: `64/256 = 0.25`, and Euclid on `(64, 256)` gives
`256 = 4 × 64`, so `64/256 = 1/4` — denominator `4`. The check `2^4 mod 15 = 16
mod 15 = 1` confirms it: `r = 4`. The two peaks whose numerator `k` shares a
factor with `r` (`k = 0` and `k = 2`) give a *divisor* of `r` or nothing, and
the `a^r ≡ 1` check rejects them.

**One run gives one peak.** A measurement returns a *single* outcome, sampled
from the four at probability `0.25` each. You might get `64` — done in one
shot. You might get `128`, whose candidate `r = 2` fails the check, or `0`,
which says nothing. That is why Shor repeats the quantum part a few times:
each shot is a lottery ticket on a peak, and only the peaks with `k` coprime
to `r` pay out the period.

??? question "Check yourself — the QFT peaks *encode* the period, so why does one measurement not simply hand it over?"
    Because a measurement does not show you the distribution — it samples it.
    All four peaks sit in the register with probability `0.25` each, and
    measuring collapses the register to **one** of them, at random. Reading
    `outcome/2^m` only helps when that outcome landed on a peak with `k`
    coprime to `r` (`64` or `192` here). The other outcomes give nothing
    (`0`) or a divisor that fails the `a^r ≡ 1` check (`128`). Repeat the run
    and combine with the classical check, and the period emerges after a
    couple of shots.

## Assembling Shor

End to end for the demo target `N = 15` — exactly what the `ch11.shor` module
runs, with every number one you have already met:

1. **Even check (classical).** `15` is odd, so the free shortcut does not
   apply — an even `N` is factored on the spot: `shor(14) → 2 × 7`.
2. **Preprocess (classical).** Pick `a = 2`; `gcd(2, 15) = 1` — no free factor,
   and `2` is usable.
3. **Build the order-finding circuit (quantum).** Counting register
   `m = counting_width(15) = 8` qubits, work register `4` qubits. Hadamards
   spread all `256` exponents; the work register starts at `|1⟩`; controlled
   multiplications by `2^(2^j) mod 15` write `f(x)` in — only `j = 0` (× 2)
   and `j = 1` (× 4) exist, since `2^(2^2) = 16 ≡ 1` makes the rest the
   identity.
4. **Inverse QFT (quantum).** The periodic counting register collapses to the
   four peaks `0, 64, 128, 192`.
5. **Measure and read the period (quantum + classical).** One outcome, say
   `64`. Continued fractions: `64/256 = 1/4`, check `2^4 mod 15 = 1` — the
   period is `r = 4`. (Outcome `0` or `128`? Measure again.)
6. **Guards (classical).** `r = 4` is even, and `2^(r/2) mod 15 = 4`, not
   `≡ −1 = 14` — this `a` works.
7. **Extract (classical).** `gcd(4 − 1, 15) = 3`, `gcd(4 + 1, 15) = 5`.
   Factors: **3 and 5**.

| Step | What it does | Classical or quantum |
|---|---|---|
| Preprocess | pick `a`; `gcd(a, N) > 1` would already be a factor | classical |
| Hadamards | every exponent at once | quantum |
| Controlled modular multiplication | record `a^x mod N` in the work register | quantum |
| Inverse QFT | turn the period into peaks | quantum |
| Measure | read a peak | quantum |
| Continued fractions | recover `r` from the peak | classical |
| Guard and `gcd` | turn `r` into the factors | classical |

The same code then factors `21`: `a = 2` has period `r = 6`, `2^3 mod 21 = 8`,
and `gcd(7, 21) = 7`, `gcd(9, 21) = 3` → `21 = 3 × 7`. One honest wrinkle
shows up there: `2^m / r = 1024/6 ≈ 170.7` is not a whole number, so the peaks
smear over neighboring outcomes (`171`, `341`, `683`, `853` instead of exact
multiples) — close enough that continued fractions still recover `1/6`, hence
`r = 6`.

!!! warning "Cost, honestly stated"
    The demo stops at `15` and `21`, and that is a limit of *this simulation*,
    not the algorithm. Each extra bit of `N` widens both registers, and the
    simulated modular-multiplication unitary has `(2^width)²` entries: `15` is
    instant, `21` takes a few seconds, and a 30-bit `N` would already be out
    of reach. On real hardware Shor is **polynomial** in the number of bits,
    but the constants are enormous: a 2048-bit number needs thousands of
    *logical* qubits and millions of gates, and each logical qubit needs error
    correction (thousands of physical qubits). The algorithm breaks current
    public-key cryptography *in principle*; building the machine is the hard
    part, and these pages do not overpromise it.

??? question "Check yourself — the semiclassic sample factors 15 and 21 without any quantum circuit. Is that cheating?"
    No — it is the point. Shor's algorithm is *mostly classical*: the
    reduction, the guards, the `gcd`s, even the continued fractions are
    ordinary arithmetic. The only quantum step is the period **search**.
    `semiclassic_factor` does everything classically and gets the same factors
    — it just replaces the quantum period-finder with brute force, which is
    why it would take forever on a large `N`. The demo pair
    (`semiclassic_factor` and `shor`) exists precisely to show which step the
    quantum computer replaces, and nothing else.

## The diagrams

### The classical baseline

![Classical trial division: work grows like sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

Trial divisions per `n` up to 120 — the `steps_curve` of the module. Nearly
flat here; at 600 digits the same curve needs about `10^300` divisions.

![The period of 2^x mod 15 is 4](../assets/ch11-period-function.png){ width="620" }

`2^x mod 15` for `x = 0 … 15`: the four-step rhythm `1, 2, 4, 8` — the number
the whole algorithm is built to find.

### The quantum Fourier transform

![The three-qubit QFT circuit](../assets/ch11-qft-circuit.png){ width="620" }

One Hadamard per qubit plus a controlled phase gate for every pair — a small
circuit for the amount of mathematics it carries.

![QFT|1>: a uniform magnitude, a linear phase ramp](../assets/ch11-qft-phase.png){ width="620" }

`QFT|1⟩` on three qubits: every output magnitude `1/√8`, phase climbing `π/4`
per step (wrapped past `π`).

### Order finding

![A compact order-finding circuit](../assets/ch11-order-circuit.png){ width="620" }

Counting register on top, work register below: Hadamards, two controlled
modular multiplications (× 2 and × 4), then the inverse QFT.

![Inverse QFT of the periodic register: four peaks](../assets/ch11-order-peaks.png){ width="620" }

The counting register after the inverse QFT: four peaks at `0, 64, 128, 192`,
each probability `0.25` — the period `4` in peak form.

## Key takeaways

- Factoring matters because RSA-style cryptography rests on it being hard.
  Trial division costs about `√N`: 500 divisions for the 6-digit prime
  `999983`, 500 000 for the 12-digit `999999999989` — twice the digits, a
  thousand times the work.
- Shor's reduction: the period `r` of `a^x mod N` gives the factors through
  `gcd(a^(r/2) − 1, N)` and `gcd(a^(r/2) + 1, N)`, because `N` divides
  `a^r − 1 = (a^(r/2) − 1)(a^(r/2) + 1)` and splits between the brackets.
  Retry with another `a` if `r` is odd or `a^(r/2) ≡ −1`.
- The **QFT** is "counting how often a pattern repeats": a register periodic
  with period `r` transforms into sharp **peaks** at multiples of
  `2^m / r` — constructive interference on the peaks, cancellation elsewhere.
- **Order finding** prepares every exponent at once with Hadamards, records
  `a^x mod N` in a work register with controlled multiplications, then reads
  the period off the inverse-QFT peaks. One measurement gives one peak, so a
  few repeats are part of the design, not a failure.
- Recovering `r` from a peak is classical: continued fractions of
  `outcome / 2^m`, checked with `a^r ≡ 1 (mod N)`. The guards and `gcd`s are
  classical too — only the period *search* is quantum.
- The demo stays at `15` and `21` because simulating modular-exponentiation
  circuits explodes; real Shor is polynomial but needs error-corrected
  hardware measured in thousands of logical qubits.

## The code behind this chapter

Three samples, from the classical baseline to the algorithm:

- [`ch11/classical.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/classical.py)
  — the ``classicfactor`` and ``semiclassicfactor`` samples: trial division,
  the reduction, `gcd(a^(r/2) ± 1, N)`, and the classical period search.
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
