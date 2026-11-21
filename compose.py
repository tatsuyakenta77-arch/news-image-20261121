#!/usr/bin/env python3
"""Compose the news-image-20261121 front page: masthead + 6-panel grid + footer strip.
Base artwork: AI-generated photo collage (media-generation-news-20261121-collage-0-*.png).
All text is drawn here with PIL so every label is crisp and legible."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, os

BASE = "/home/hatch/workspace/makefun/news-image-20261121-bot/media-generation-news-20261121-collage-0-0e64fff5-67f4-4779-88dc-f4c9899ea03d.png"
OUT = "/home/hatch/workspace/makefun/news-image-20261121-bot/entry.png"

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (18, 38, 74)
RED = (178, 34, 34)
GREY = (90, 88, 82)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

img = Image.open(BASE).convert("RGB")
bw, bh = img.size  # square collage, 2x3 grid
# panel crops: equal thirds/halves; top-right (Wall Street) cropped 12% from top
# to cut the garbled screen text at the very top of that panel.
panels = [
    # (col, row, top_crop_frac)
    (0, 0, 0.00), (1, 0, 0.00), (2, 0, 0.12),
    (0, 1, 0.00), (1, 1, 0.00), (2, 1, 0.00),
]
cw, ch = bw // 3, bh // 2
crops = []
for col, row, top in panels:
    x0, y0 = col * cw, row * ch
    y0 = int(y0 + top * ch)
    crops.append(img.crop((x0, y0, x0 + cw, row * ch + ch)))

page = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(page)

# ---- Masthead ----
d.rectangle([0, 0, W, 116], fill=NAVY)
f_title = font(SERIF_B, 58)
d.text((W // 2, 8), "THE WORLD IN ONE DAY", font=f_title, fill=(255, 255, 255), anchor="ma")
f_date = font(SANS_B, 34)
d.text((W // 2, 72), "SATURDAY  21  NOVEMBER  2026", font=f_date, fill=(255, 214, 64), anchor="ma")

# ---- Grid ----
MX, GX, GY = 10, 8, 8
PW = (W - 2 * MX - 2 * GX) // 3   # 329
PH_IMG, PH_TXT = 220, 185
ROW_H = PH_IMG + PH_TXT
TOP = 124

stories = [
    ("THE HAGUE", "MYANMAR GUILTY OF ROHINGYA GENOCIDE",
     "World Court rules 9\u20136: genocide in 2017. Myanmar must investigate and pay up."),
    ("POLAND", "RUSSIAN MISSILE CRASHES IN POLAND",
     "A Kh-101 falls in a snowy field amid a huge attack on Ukraine. NATO jets scramble."),
    ("WALL STREET", "AI SELL-OFF SINKS MARKETS",
     "Nasdaq \u22125.3%, S&P 500 \u22123.7% as AI shares slide. The SEC examines Nvidia\u2019s accounting."),
    ("ANTALYA", "COP31 TALKS MISS DEADLINE",
     "Climate summit runs into overtime after its draft drops any mention of fossil fuels."),
    ("BRUSSELS", "UK AND EU SEAL NEW DEAL",
     "Most food and farm checks scrapped from 2028; youth mobility for 100,000 a year."),
    ("PERU", "6.8 QUAKE SHAKES PERU",
     "Strong tremor strikes Jun\u00edn in the Andes; shaking felt 320 km away in Lima."),
]

f_kick = font(SANS_B, 21)
f_head = font(SERIF_B, 25)
f_cap = font(SANS, 18)

for i, (kick, head, cap) in enumerate(stories):
    col, row = i % 3, i // 3
    x = MX + col * (PW + GX)
    y = TOP + row * (ROW_H + GY)
    # photo
    ph = crops[i].resize((PW, PH_IMG), Image.LANCZOS)
    page.paste(ph, (x, y))
    d.rectangle([x, y, x + PW - 1, y + PH_IMG - 1], outline=(0, 0, 0), width=2)
    # text block
    ty = y + PH_IMG + 8
    d.text((x, ty), kick, font=f_kick, fill=RED)
    ty += 30
    for ln in wrap(d, head, f_head, PW):
        d.text((x, ty), ln, font=f_head, fill=INK)
        ty += 30
    ty += 2
    for ln in wrap(d, cap, f_cap, PW):
        d.text((x, ty), ln, font=f_cap, fill=(52, 52, 48))
        ty += 24

# ---- Footer strip ----
fy = TOP + 2 * ROW_H + GY + 4
d.rectangle([0, fy, W, fy + 54], fill=NAVY)
f_foot = font(SANS_B, 15)
foot = "ALSO:  Gen Z protests in 25 European countries  \u00b7  KL Rahul\u2019s SENA centuries  \u00b7  NYC sets 2032 to close Rikers Island"
d.text((W // 2, fy + 27), foot, font=f_foot, fill=(255, 255, 255), anchor="mm")

page.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes", page.size)
