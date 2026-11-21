#!/usr/bin/env python3
"""Deliver the v2 front page for news-image-20261120.

Copies entry.png (the rendered 1024x1024 front page for Friday
20 November 2026, built by render.py) to the output location the
platform expects: the MAKEFUN_OUTPUT_DIR directory when that
variable is set, otherwise /output/entry.png. Standard library
only. Never writes into the repository or working directory.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        print("copy size mismatch", file=sys.stderr)
        return 1
    print("wrote", target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
