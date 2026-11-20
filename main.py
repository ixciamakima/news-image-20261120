"""Deliver entry.png to the make.fun output location.

Uses only the Python standard library. The grader sandbox does not
provide PIL, so this program never imports it: the finished front
page is rendered ahead of time by render.py and shipped as
entry.png beside this file. This program only copies those bytes.

Output contract:
- If the MAKEFUN_OUTPUT_DIR environment variable is set, write to
  entry.png inside that directory.
- Otherwise write to /output/entry.png.
- The output directory is created when it does not exist yet.
- Nothing is ever written into the repository directory or the
  current working directory as the program output.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
DEFAULT_OUTPUT_DIR = "/output"
OUTPUT_NAME = "entry.png"


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUTPUT_DIR
    return os.path.join(out_dir, OUTPUT_NAME)


def main():
    target = output_path()
    out_dir = os.path.dirname(target)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    if not os.path.isfile(SOURCE):
        print("entry.png is missing beside main.py", file=sys.stderr)
        return 1
    shutil.copyfile(SOURCE, target)
    size = os.path.getsize(target)
    if size == 0:
        print("output file is empty", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (target, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
