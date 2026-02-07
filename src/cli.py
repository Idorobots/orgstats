#!/usr/bin/env python
"""CLI interface for orgstats - Org-mode archive file analysis."""

import sys
import orgparse
from core import analyze, clean, TAGS, HEADING, BODY


def main() -> None:
    """Main CLI entry point."""
    nodes = []

    for name in sys.argv[1:]:
        contents = ""
        with open(name) as f:
            print("Processing " + name + "...")

            # NOTE Making the file parseable.
            contents = f.read().replace("24:00", "00:00")

            ns = orgparse.loads(contents)
            if ns != None:
                nodes = nodes + list(ns[1:])

    (total, done, tags, heading, body) = analyze(nodes)

    # Top skills
    N = 100
    order = lambda item: -item[1]

    print("\nTotal tasks: ", total)
    print("\nDone tasks: ", done)
    print("\nTop tags:\n", list(sorted(clean(TAGS, tags).items(), key=order))[0:N])
    print("\nTop words in headline:\n", list(sorted(clean(HEADING, heading).items(), key=order))[0:N])
    print("\nTop words in body:\n", list(sorted(clean(BODY, body).items(), key=order))[0:N])


if __name__ == "__main__":
    main()
