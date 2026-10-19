"""Chapter 11 — Shor's algorithm: factoring through order finding.

The chapter follows the book's samples, from the classical baseline to the quantum
algorithm:

* :mod:`...ch11.classical` — the ``classicfactor`` and ``semiclassicfactor``
  samples: trial division, and the reduction of factoring to **order finding**.
* :mod:`...ch11.qft` — the quantum Fourier transform, the circuit that turns a
  periodic register into a few measurable peaks.
* :mod:`...ch11.shor` — the ``quantumfactor`` sample: controlled modular
  multiplication, the inverse QFT, continued fractions, and the factors.

:func:`main` runs all three in that order, which is what ``make ch11`` does. Run an
individual sample with, for example, ``python -m
quantum_computing_in_action.ch11.shor``.

The thread running through all three is that factoring is hard only because
*order finding* is hard, and that a periodic superposition plus a Fourier
transform makes the order cheap to read.
"""

from __future__ import annotations

from quantum_computing_in_action.ch11 import classical, qft, shor
from quantum_computing_in_action.ch11.classical import (
    classical_period,
    factor_from_order,
    period_function,
    reduction_steps,
    semiclassic_factor,
    trial_division,
)
from quantum_computing_in_action.ch11.qft import phase_ramp, qft_circuit, qft_matrix
from quantum_computing_in_action.ch11.shor import (
    convergents,
    counting_width,
    modular_multiplier,
    order_distribution,
    order_finding_circuit,
    period_from_outcome,
    quantum_order,
)

#: The samples in the order the chapter builds them up.
SAMPLES = (classical, qft, shor)


def main() -> None:
    """Run every Chapter 11 sample in order, as ``make ch11`` does."""
    for sample in SAMPLES:
        sample.main()


__all__ = [
    "SAMPLES",
    "classical",
    "classical_period",
    "convergents",
    "counting_width",
    "factor_from_order",
    "main",
    "modular_multiplier",
    "order_distribution",
    "order_finding_circuit",
    "period_from_outcome",
    "period_function",
    "phase_ramp",
    "qft",
    "qft_circuit",
    "qft_matrix",
    "quantum_order",
    "random_semiclassic_factor",
    "reduction_steps",
    "semiclassic_factor",
    "shor",
    "trial_division",
]
