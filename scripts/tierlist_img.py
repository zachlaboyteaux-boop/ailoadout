#!/usr/bin/env python3
"""Render a 1200x675 tier-list PNG for a loadout from tools.json.
Usage: python3 scripts/tierlist_img.py coding [agents ...]   (or: all)
Output: /workspace/x-images/<slug>.png  (override with OUT_DIR env var)
Requires Pillow (pip install pillow)."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
D = json.load(open(os.path.join(ROOT, "tools.json")))
SLUG = {"Coding / Vibe Coding":"coding","AI Agents":"agents","Chat / Assistants":"chat","Image":"image","Video":"video",
        "Voice / Audio":"voice","Writing":"writing","Research / Search":"research","Game Dev":"game-dev","Productivity":"productivity",
        "Crypto / Finance AI":"crypto-finance","3D":"3d","Music":"music","Education":"education","Streamers / Creators":"creators",
        "Open-Source & Local Models":"local-models","AI in Games":"ai-in-games"}
BY_SLUG = {v: k for k, v in SLUG.items()}
OUT = os.environ.get("OUT_DIR", "/workspace/x-images")
COL = {"S":"#ff5c5c","A":"#ffb347","B":"#7cff6b","C":"#5ac8ff"}
def font(size, bold=True):
    for p in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]):
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()
def render(slug):
    cat = BY_SLUG[slug]
    ts = sorted([t for t in D["tools"] if t["category"] == cat], key=lambda t: t["rank"])
    W, H = 1200, 675
    im = Image.new("RGB", (W, H), "#0b0d12"); d = ImageDraw.Draw(im)
    d.text((40, 28), f"{cat} — tier list", font=font(46), fill="#e7eaf2")
    d.text((40, 88), f"The AI Loadout · updated {D.get('updated','')}", font=font(22, False), fill="#8b93a7")
    tiers = [k for k in "SABC" if any(t["tier"] == k for t in ts)]
    top, bottom = 140, H - 60
    rowh = (bottom - top) // max(1, len(tiers))
    for i, k in enumerate(tiers):
        y = top + i * rowh
        d.rectangle((40, y + 4, 140, y + rowh - 4), fill=COL[k])
        d.text((90, y + rowh // 2), k, font=font(min(64, rowh - 20)), fill="#000", anchor="mm")
        d.rectangle((150, y + 4, W - 40, y + rowh - 4), fill="#141823")
        x = 166; names = [t["name"] for t in ts if t["tier"] == k]
        f = font(26 if rowh > 70 else 20)
        for n in names:
            w = d.textlength(n, font=f) + 28
            if x + w > W - 50:  # overflow: shrink to "+N more"
                d.text((x, y + rowh // 2), f"+{len(names) - names.index(n)} more", font=f, fill="#8b93a7", anchor="lm"); break
            d.rounded_rectangle((x, y + rowh // 2 - 22, x + w, y + rowh // 2 + 22), radius=10, fill="#232a3a")
            d.text((x + 14, y + rowh // 2), n, font=f, fill="#e7eaf2", anchor="lm"); x += w + 12
    d.text((40, H - 40), "zachlaboyteaux-boop.github.io/ailoadout", font=font(22, False), fill="#5ac8ff")
    d.text((W - 40, H - 40), "S = must-equip · A = strong · B = specific · C = situational", font=font(18, False), fill="#8b93a7", anchor="ra")
    os.makedirs(OUT, exist_ok=True); p = os.path.join(OUT, f"{slug}.png"); im.save(p, optimize=True); return p
if __name__ == "__main__":
    args = sys.argv[1:] or ["coding"]
    if args == ["all"]: args = list(BY_SLUG)
    for s in args: print(render(s))
