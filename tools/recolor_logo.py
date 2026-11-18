#!/usr/bin/env python3
"""
Recolor a (white) transparent logo PNG to any colour, keeping its transparency.

Usage:
    pip install pillow
    python tools/recolor_logo.py INPUT.png OUTPUT.png --color "#000000"
"""
import argparse

from PIL import Image


def recolor(src, dst, color):
    color = color.lstrip("#")
    r, g, b = (int(color[i:i + 2], 16) for i in (0, 2, 4))
    im = Image.open(src).convert("RGBA")
    alpha = im.getchannel("A")
    out = Image.new("RGBA", im.size, (r, g, b, 255))
    out.putalpha(alpha)
    out.save(dst, optimize=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("output")
    ap.add_argument("--color", default="#000000")
    a = ap.parse_args()
    recolor(a.input, a.output, a.color)
    print(f"wrote {a.output}")
