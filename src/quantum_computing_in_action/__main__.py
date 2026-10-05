"""Command-line entry point: ``python -m quantum_computing_in_action <chapter>``."""

from __future__ import annotations

import argparse
import importlib
from typing import Protocol, cast


class _ChapterModule(Protocol):
    def main(self) -> None: ...


_MODULES: dict[str, str] = {
    "ch01": "quantum_computing_in_action.ch01.time_complexity",
    "ch02": "quantum_computing_in_action.ch02.random_bits",
    "ch03": "quantum_computing_in_action.ch03.pauli_x",
}


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="quantum_computing_in_action",
        description="Run a chapter sample from 'Quantum Computing in Action'.",
    )
    parser.add_argument("chapter", choices=sorted(_MODULES), help="chapter to run")
    args = parser.parse_args()
    module = cast(_ChapterModule, importlib.import_module(_MODULES[args.chapter]))
    module.main()


if __name__ == "__main__":
    main()
