#!/usr/bin/env python3
"""Entry program for news-image-20261127.

The image is rendered by build_image.py (same repository) into entry.png;
this program copies that image to /output/entry.png, as the competition
rules allow: the simplest program copies an image the repository holds.
Standard library only, no network, fully deterministic.
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = "/output"
    if not os.path.isdir(out_dir):
        out_dir = here
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    print("wrote %s" % dst)


if __name__ == "__main__":
    main()
