# -*- coding: utf-8 -*-
"""Logo helpers: trim empty margins from PNG logos and give every logo an optically balanced size,
so wide wordmarks and square marks read at the same visual weight in a row."""
import os, re, shutil, math
from PIL import Image

def _svg_aspect(path):
    s = open(path, encoding="utf-8", errors="ignore").read(4000)
    m = re.search(r'viewBox="\s*[-\d.]+[\s,]+[-\d.]+[\s,]+([\d.]+)[\s,]+([\d.]+)', s)
    if m:
        return float(m.group(1)) / float(m.group(2))
    w, h = re.search(r'\bwidth="([\d.]+)', s), re.search(r'\bheight="([\d.]+)', s)
    return float(w.group(1)) / float(h.group(1)) if w and h else 3.0

def prep(src, dst):
    """Copy a logo; PNG and WebP files are trimmed to their visible pixels. Returns the aspect ratio."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if src.lower().endswith(".svg"):
        s = open(src, encoding="utf-8", errors="ignore").read()
        fills = set(re.findall(r'fill(?:=|:)\s*"?(#[0-9a-fA-F]{3,6}|white)', s))
        if fills and fills <= {"#fff", "#ffffff", "#FFF", "#FFFFFF", "white"}:
            # an all-white logo made for dark backgrounds: draw it dark so it shows on white
            s = re.sub(r'(fill(?:=|:)\s*"?)(#fff(?:fff)?|white)', r"\g<1>#1C2233", s, flags=re.I)
        open(dst, "w", encoding="utf-8").write(s)
        return _svg_aspect(src)
    im = Image.open(src).convert("RGBA")
    a = im.split()[-1]
    box = a.point(lambda v: 255 if v > 12 else 0).getbbox()
    if box is None or (box[2] - box[0]) * (box[3] - box[1]) > 0.98 * im.width * im.height:
        # no transparency to trim by: trim near-white margins instead
        rgb = Image.new("RGB", im.size, (255, 255, 255)); rgb.paste(im, mask=a)
        g = rgb.convert("L").point(lambda v: 255 if v < 245 else 0)
        box = g.getbbox() or (0, 0, im.width, im.height)
    pad = 2
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
    im = im.crop(box)
    if im.height > 200:   # logos show at most about 48px tall: 200px keeps them sharp on retina without heavy files
        im = im.resize((round(im.width * 200 / im.height), 200), Image.LANCZOS)
    im.save(dst, optimize=True)
    return im.width / im.height

def size(aspect, base=58, lo=20, hi=44, maxw=168):
    """Height in px so that area reads evenly: h = base / sqrt(aspect), capped by height range and max width."""
    h = max(lo, min(hi, base / math.sqrt(max(aspect, .2))))
    if h * aspect > maxw:
        h = maxw / aspect
    return round(h), round(h * aspect)
