#!/usr/bin/env python
"""CLI interface for orgstats - Org-mode archive file analysis."""

import sys
from typing import Any

import orgparse

from core import BODY, HEADING, TAGS, analyze, clean


def main() -> None:
    """Main CLI entry point."""
    nodes: list[Any] = []

    for name in sys.argv[1:]:
        with open(name, encoding="utf-8") as f:
            print("Processing " + name + "...")

            # NOTE Making the file parseable.
            contents = f.read().replace("24:00", "00:00")

            ns = orgparse.loads(contents)
            if ns is not None:
                nodes = nodes + list(ns[1:])

    (total, done, tags, heading, body) = analyze(nodes)

    # Top skills
    max_results = 100

    def order_by_frequency(item: tuple[str, int]) -> int:
        """Sort by frequency (descending)."""
        return -item[1]

    print("\nTotal tasks: ", total)
    print("\nDone tasks: ", done)
    print("\nTop tags:\n", sorted(clean(TAGS, tags).items(), key=order_by_frequency)[0:max_results])
    print(
        "\nTop words in headline:\n",
        sorted(clean(HEADING, heading).items(), key=order_by_frequency)[0:max_results],
    )
    print(
        "\nTop words in body:\n",
        sorted(clean(BODY, body).items(), key=order_by_frequency)[0:max_results],
    )


if __name__ == "__main__":
    main()
