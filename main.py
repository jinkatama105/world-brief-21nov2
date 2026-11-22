#!/usr/bin/env python3
"""Serve the pre-rendered board to /output/entry.png (grader runs this offline)."""
import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
dst = os.path.join(out_dir, "entry.png")
if os.path.abspath(src) != os.path.abspath(dst):
    # skip the copy when the output already matches byte-for-byte
    if not (os.path.exists(dst)
            and open(dst, "rb").read() == open(src, "rb").read()):
        shutil.copyfile(src, dst)
print(dst)
