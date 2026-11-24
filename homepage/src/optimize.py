# -*- coding: utf-8 -*-
"""Ship only the photos a page uses, as WebP sized to how large they appear. Called by both builders."""
import os, re
from PIL import Image

BIG = ("k_conf", "e2026", "cta", "globe", "fde_team", "k_summit", "cs_horizon", "cs_rac", "cs_mckesson")

def width_for(name):
    if name in BIG or name.startswith("cs_"):
        return 1600
    if name.startswith(("e1", "e2", "n1", "n2")):
        return 2200   # era photos fill the 48 numeral at about 1000 css px: 2400 keeps it sharp on retina screens
    return 1000

def optimize(html, src_dir, dst_dir, quality=70):
    os.makedirs(dst_dir, exist_ok=True)
    names = sorted(set(re.findall(r"assets/img/([\w-]+)\.jpg", html)))
    total = 0
    for n in names:
        im = Image.open(os.path.join(src_dir, n + ".jpg")).convert("RGB")
        w = width_for(n)
        if im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        out = os.path.join(dst_dir, n + ".webp")
        im.save(out, "WEBP", quality=76 if n.startswith(("e1", "e2", "n1", "n2")) else quality, method=6)
        total += os.path.getsize(out)
    return re.sub(r"assets/img/([\w-]+)\.jpg", r"assets/img/\1.webp", html), len(names), total
