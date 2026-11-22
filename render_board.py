#!/usr/bin/env python3
"""Render the World in Brief board (21 Nov 2026). Deterministic: no clock, no RNG."""
import os
from PIL import Image, ImageDraw, ImageFont

FD = "/usr/share/fonts/truetype/dejavu"
F = lambda n, s: ImageFont.truetype(f"{FD}/{n}", s)

W = H = 1024
BG = "#0e1420"
CARD = "#182233"
INK = "#e8edf5"
DIM = "#9aa7ba"
ACCENT = "#4cc2ff"

STORIES = [
    ("AMERICAS", "#e05c5c", "El Chapo Isidro captured", "Guasave, Mexico",
     "Mexican commandos seized fugitive boss Ismael 'El Chapo Isidro' Nava in Sinaloa; 11 killed, long on FBI most-wanted list."),
    ("MIDDLE EAST", "#e0a13c", "Tankers ablaze at Hormuz", "Strait of Hormuz",
     "Iran targeted ships transiting the strait; at least three commercial vessels set ablaze as Tehran unveils an underground 'missile city'."),
    ("MIDDLE EAST", "#e0a13c", "Aid workers killed in Gaza", "Gaza City",
     "Israeli strike on a World Central Kitchen truck killed 3; Israel says militants were aboard, WCK disputes."),
    ("EUROPE", "#5c8de0", "War spills into Baltic", "Gulf of Finland",
     "Ukrainian drones hit a Russian cargo freighter in the gulf; a Russian helicopter violated Finnish airspace for hours."),
    ("MIDDLE EAST", "#e0a13c", "Riyadh targets missiles", "Riyadh, Saudi Arabia",
     "Saudi Arabia says it deflected ballistic missiles on the capital as Houthi fire struck three straight nights."),
    ("GLOBAL", "#4cc2ff", "No treaty on killer robots", "Geneva, Switzerland",
     "UN talks on autonomous weapons ended with no legally binding rules on lethal AI systems."),
    ("CANADA", "#9b6de0", "Bains wins Ontario race", "Ontario, Canada",
     "Navdeep Bains takes the Liberal leadership - the party's third contest in six years."),
    ("CANADA", "#9b6de0", "Tumbler Ridge shooting probe", "Tumbler Ridge, B.C.",
     "Reports say the young killer had sought AI instructions on modifying weapons."),
    ("MARKETS", "#3cc98a", "Bitcoin slips under $60K", "Global markets",
     "Bitcoin drops below $60,000 for the first time since July on a broad risk-off day."),
]

COLS, ROWS = 3, 3
MX, MY = 40, 30
GAP = 16
HEAD_H = 118  # masthead block height
CARD_W = (W - 2 * MX - (COLS - 1) * GAP) // COLS   # 296
CARD_H = (H - HEAD_H - 2 * MY - (ROWS - 1) * GAP) // ROWS  # ~247
PAD = 14
INNER = CARD_W - 2 * PAD

f_title = F("DejaVuSans-Bold.ttf", 34)
f_sub = F("DejaVuSans.ttf", 16)
f_chip = F("DejaVuSans-Bold.ttf", 11)
f_head = F("DejaVuSans-Bold.ttf", 17)
f_place = F("DejaVuSans-Bold.ttf", 11)
f_fact = F("DejaVuSans.ttf", 12)

def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if not cur:
                raise SystemExit(f"word too wide: {word!r}")
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# masthead
d.text((MX, MY), "WORLD IN BRIEF", font=f_title, fill=INK)
sub = "SATURDAY 21 NOVEMBER 2026"
d.text((W - MX - d.textlength(sub, font=f_sub), MY + 14), sub, font=f_sub, fill=ACCENT)
d.line([(MX, MY + 56), (W - MX, MY + 56)], fill="#2a3850", width=2)
tag = "Nine stories, nine regions - compiled from AP, Reuters, AFP, Guardian, NPR, CBS, Global News"
d.text((MX, MY + 68), tag, font=F("DejaVuSans.ttf", 13), fill=DIM)

top0 = HEAD_H + MY
max_used = {}
for i, (region, color, headline, place, fact) in enumerate(STORIES):
    cx = MX + (i % COLS) * (CARD_W + GAP)
    cy = top0 + (i // COLS) * (CARD_H + GAP)
    d.rounded_rectangle([cx, cy, cx + CARD_W - 1, cy + CARD_H - 1], radius=10, fill=CARD)
    d.rectangle([cx, cy, cx + 4, cy + CARD_H - 1], fill=color)
    x, y = cx + PAD, cy + PAD
    # chip
    cw = d.textlength(region, font=f_chip) + 14
    d.rounded_rectangle([x, y, x + cw, y + 18], radius=9, fill=color)
    d.text((x + 7, y + 3), region, font=f_chip, fill="#0e1420")
    y += 26
    # headline (2 lines reserved)
    for ln in wrap(d, headline, f_head, INNER):
        d.text((x, y), ln, font=f_head, fill=INK)
        y += 21
    y += 3
    d.text((x, y), place.upper(), font=f_place, fill=color)
    y += 20
    fact_lines = wrap(d, fact, f_fact, INNER)
    for ln in fact_lines:
        d.text((x, y), ln, font=f_fact, fill=DIM)
        y += 16
    max_used[i] = (y, cy + CARD_H, len(fact_lines))

for i, (bot, limit, n) in max_used.items():
    if bot > limit - 6:
        raise SystemExit(f"card {i} overflows: {bot} > {limit-6} ({n} fact lines)")

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "entry.png")
img.save(out, "PNG")
print(out, os.path.getsize(out), "bytes")
