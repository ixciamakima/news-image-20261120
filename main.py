#!/usr/bin/env python3
"""news-image-20261120 entry program.

Copies the committed entry.png (the front page rendered in-session
by render.py) to the grading destination:

  1. the first command-line argument, if one is given;
  2. else the MAKEFUN_OUTPUT_DIR environment variable;
  3. else /output.

The destination is treated as a directory and the image lands at
<destination>/entry.png. Exits 0 on success, 1 on any failure.
Standard library only: no rendering happens here.
"""

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def destination():
    if len(sys.argv) > 1 and sys.argv[1]:
        return sys.argv[1]
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    return "/output"


def main():
    dest_dir = destination()
    try:
        os.makedirs(dest_dir, exist_ok=True)
        target = os.path.join(dest_dir, "entry.png")
        shutil.copyfile(SOURCE, target)
    except OSError as exc:
        print(f"entry copy failed: {exc}", file=sys.stderr)
        return 1
    if not os.path.isfile(target):
        print("entry copy failed: target missing", file=sys.stderr)
        return 1
    if os.path.getsize(target) != os.path.getsize(SOURCE):
        print("entry copy failed: size mismatch after copy",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
