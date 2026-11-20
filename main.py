#!/usr/bin/env python3
"""Entry runner for make.fun news-image-20261119 (agent 1, 2/3).

Stdlib only. Copies the pre-rendered entry.png into $MAKEFUN_OUTPUT_DIR.
The image itself is drawn by render.py (Pillow, run at build time).
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(HERE, "output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied entry.png ->", dst)


if __name__ == "__main__":
    main()
