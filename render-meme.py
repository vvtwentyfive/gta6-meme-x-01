#!/usr/bin/env python3
"""Render gta6-meme-x-01 v2: Leonida Department of Revenue NOTICE OF ASSESSMENT.
All text is code-rendered with PIL (never AI-drawn). Deterministic: same bytes
on every re-run (no timestamps, no randomness).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1200
PAPER = (247, 241, 220, 255)
INK = (18, 32, 62, 255)      # dark navy
RED = (178, 34, 34, 255)
MAGENTA = (226, 0, 122, 255)
GOLD = (176, 141, 45, 255)
GREY = (90, 90, 84, 255)
LIGHT_LINE = (120, 110, 88, 255)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_w, minimum=16):
    size = start
    while size > minimum:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, minimum)


def sparkle(draw, cx, cy, r, fill):
    # Four-pointed star: 8 vertices alternating outer/inner radius.
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rad = r if i % 2 == 0 else r * 0.28
        pts.append((cx + rad * math.cos(ang), cy - rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def star5(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy - rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def draw_ghost(draw, cx, cy, scale, outline=7):
    """make.fun ghost per press-kit description: white ghost, thick black
    outline, two black four-pointed sparkle eyes, a round little hand,
    holding a magenta coin with a white star."""
    s = scale  # body width
    top = cy - 0.62 * s
    bottom = cy + 0.55 * s
    left = cx - 0.5 * s
    right = cx + 0.5 * s
    black = (0, 0, 0, 255)
    white = (255, 255, 255, 255)
    # Body: dome top + straight sides + scalloped hem (3 waves).
    draw.pieslice([left, top, right, top + s], 180, 360, fill=white, outline=black, width=outline)
    draw.rectangle([left, cy - 0.12 * s, right, bottom - 0.18 * s], fill=white, outline=black, width=outline)
    # Scallops: white circles over the hem, outlined underneath by arcs.
    for i in range(3):
        sx0 = left + i * s / 3
        draw.ellipse([sx0, bottom - 0.36 * s, sx0 + s / 3, bottom], fill=white, outline=black, width=outline)
    # Cover the seam lines between dome and rectangle.
    draw.rectangle([left + outline, cy - 0.12 * s, right - outline, cy - 0.05 * s], fill=white)
    # Round little hand on the right, holding the coin.
    hx, hy = right + 0.06 * s, cy + 0.18 * s
    draw.ellipse([hx - 0.13 * s, hy - 0.13 * s, hx + 0.13 * s, hy + 0.13 * s],
                 fill=white, outline=black, width=outline)
    # Magenta coin with a white star, in the hand.
    coin_cx, coin_cy, coin_r = hx + 0.10 * s, hy - 0.02 * s, 0.24 * s
    draw.ellipse([coin_cx - coin_r, coin_cy - coin_r, coin_cx + coin_r, coin_cy + coin_r],
                 fill=MAGENTA, outline=black, width=max(3, outline - 2))
    star5(draw, coin_cx, coin_cy, coin_r * 0.62, white)
    # Sparkle eyes.
    sparkle(draw, cx - 0.20 * s, cy - 0.18 * s, 0.11 * s, black)
    sparkle(draw, cx + 0.20 * s, cy - 0.18 * s, 0.11 * s, black)


# The 15 itemised lines (research file, verbatim wording; amount in its own column).
LINES = [
    ("1", "TAX YEAR 2013 \u2014 RETURN FILED, REFUND STILL PENDING \u2014 13 YRS", "$0.00"),
    ("2", "INTEREST ON PATIENCE \u2014 COMPOUNDED DAILY SINCE 2013", "$0.00"),
    ("3", "RESCHEDULE FEE #1 \u2014 DATE MOVED, HYPE KEPT", "$0.00"),
    ("4", "RESCHEDULE FEE #2 \u2014 MOVED AGAIN, HYPE DOUBLED", "$0.00"),
    ("5", "PRE-ORDER DEPOSIT \u2014 HELD SINCE 2013, EARNED $0.00 INTEREST", "$79.99"),
    ("6", "DOWNLOAD LEVY \u2014 214 GB, PAID IN DELETED FAMILY PHOTOS", "$0.00"),
    ("7", "STORAGE TAX \u2014 2 TB SSD, BOUGHT FOR ONE CITY", "$129.99"),
    ("8", "LAUNCH-DAY QUEUE \u2014 POSITION 13,013, STILL IN LINE", "$0.00"),
    ("9", "SICK-DAY DEDUCTION \u2014 5 DAYS CLAIMED, 0 APPROVED", "$0.00"),
    ("10", "TRAILER 2 \u2014 VIEWED 96 TIMES, MEMORISED FRAME BY FRAME", "$0.00"),
    ("11", "VICE CITY RENT \u2014 $900/MO FOR A COUCH FACING THE LOADING SCREEN", "$900.00"),
    ("12", "WANTED LEVEL \u2014 5 STARS FOR LOITERING IN THE WAITING ZONE", "$0.00"),
    ("13", "REUNION FEE \u2014 JASON & LUCIA, 13 YEARS APART, 1 MEETING", "$0.00"),
    ("14", "LEONIDA SALES TAX \u2014 CHARGED ON 12 YEARS OF NO GAME", "$0.00"),
    ("15", "SLEEP \u2014 0 HRS BANKED SINCE TRAILER 1 DROPPED", "$0.00"),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Double outer border.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=5)
    d.rectangle([26, 26, W - 27, H - 27], outline=INK, width=2)

    x0, x1 = 48, W - 48
    y = 44
    # --- Header: small ghost seal at right, department name at left. ---
    draw_ghost(d, 1065, 108, 92, outline=5)
    d.text((x0, y), "LEONIDA DEPARTMENT", font=font(SERIF_B, 46), fill=INK)
    y += 50
    d.text((x0, y), "OF REVENUE", font=font(SERIF_B, 46), fill=INK)
    y += 52
    d.text((x0, y), "NOTICE OF ASSESSMENT", font=font(SANS_B, 40), fill=RED)
    y += 48
    d.text((x0, y), "STATE OF LEONIDA  \u00b7  TAXPAYER SERVICES  \u00b7  FORM VI-2013",
           font=font(SANS_B, 21), fill=GREY)
    y += 34
    d.line([x0, y, x1, y], fill=INK, width=3)
    y += 12
    # --- Taxpayer facts: 6 counted header facts, 2 columns x 3 rows. ---
    facts = [
        ("TAXPAYER:", "THE PATIENT GAMER"),
        ("ACCOUNT NO.:", "VI-2013"),
        ("TAX YEARS:", "2013\u20132026  (13 YEARS)"),
        ("DUE DATE:", "LAUNCH DAY, 19 NOV 2026"),
        ("ADDRESS:", "VICE CITY, LEONIDA"),
        ("NOTICE DATE:", "20 NOV 2026"),
    ]
    col2 = 640
    for i, (k, v) in enumerate(facts):
        fx = x0 if i % 2 == 0 else col2
        fy = y + (i // 2) * 34
        d.text((fx, fy), k, font=font(SANS_B, 22), fill=INK)
        d.text((fx + 168, fy), v, font=font(SANS_B, 22), fill=INK)
    y += 3 * 34 + 10
    d.line([x0, y, x1, y], fill=INK, width=3)
    y += 8
    # --- Table header. ---
    d.text((x0, y), "#", font=font(SANS_B, 22), fill=INK)
    d.text((x0 + 44, y), "ASSESSMENT ITEM", font=font(SANS_B, 22), fill=INK)
    amt = "AMOUNT"
    d.text((x1 - d.textlength(amt, font=font(SANS_B, 22)), y), amt,
           font=font(SANS_B, 22), fill=INK)
    y += 32
    d.line([x0, y, x1, y], fill=LIGHT_LINE, width=2)
    y += 4
    # --- The 15 lines. ---
    row_h = 32
    for num, text, amount in LINES:
        f = fit_font(d, num + ".  " + text, SANS_B, 23, x1 - 130 - (x0 + 44))
        d.text((x0, y), num + ".", font=f, fill=INK)
        d.text((x0 + 44, y), text, font=f, fill=INK)
        af = font(MONO_B, 22)
        d.text((x1 - d.textlength(amount, font=af), y), amount, font=af, fill=INK)
        y += row_h
        d.line([x0, y - 6, x1, y - 6], fill=(200, 190, 160, 255), width=1)
    # --- Totals. ---
    d.line([x0, y - 2, x1, y - 2], fill=INK, width=2)
    totals = [
        ("TOTAL ASSESSED", "$1,109.98"),
        ("PAID BY MY AI AGENT ON make.fun", "$1,109.98"),
        ("BALANCE DUE", "$0.00"),
    ]
    for label, amount in totals:
        f = font(SANS_B, 23)
        d.text((x0 + 44, y), label, font=f, fill=RED if label == "BALANCE DUE" else INK)
        af = font(MONO_B, 23)
        d.text((x1 - d.textlength(amount, font=af), y), amount, font=af,
               fill=RED if label == "BALANCE DUE" else INK)
        y += 30
    y += 4
    # --- Payment box: big ghost revenue seal + TAX CREDIT sell. ---
    box_top = y
    box_h = 150
    d.rectangle([x0, box_top, x1, box_top + box_h], outline=RED, width=4)
    d.rectangle([x0 + 6, box_top + 6, x1 - 6, box_top + box_h - 6], outline=RED, width=1)
    # Seal: magenta disc, ghost on it.
    seal_cx, seal_cy, seal_r = x0 + 108, box_top + box_h // 2, 72
    d.ellipse([seal_cx - seal_r, seal_cy - seal_r, seal_cx + seal_r, seal_cy + seal_r],
              fill=MAGENTA, outline=INK, width=5)
    d.ellipse([seal_cx - seal_r + 8, seal_cy - seal_r + 8, seal_cx + seal_r - 8, seal_cy + seal_r - 8],
              outline=(255, 255, 255, 255), width=2)
    draw_ghost(d, seal_cx, seal_cy + 4, 92, outline=5)
    tx = x0 + 210
    ty = box_top + 12
    d.text((tx, ty), "TAX CREDIT \u2014 PAID IN FULL", font=font(SANS_B, 30), fill=RED)
    ty += 34
    d.text((tx, ty), "BY MY AI AGENT ON make.fun", font=font(SANS_B, 30), fill=INK)
    ty += 34
    d.text((tx, ty), "$250.00 BOUNTY EARNED WHILE I WAITED", font=font(SANS_B, 24), fill=INK)
    ty += 30
    d.text((tx, ty), "BALANCE DUE: $0.00", font=font(SANS_B, 24), fill=RED)
    y = box_top + box_h + 14
    # --- Footer. ---
    footer = "KEEP THIS ASSESSMENT. THE 13-YEAR WAIT IS TAX-DEDUCTIBLE. THE HYPE IS NOT."
    ff = fit_font(d, footer, SANS_B, 22, x1 - x0)
    d.text(((W - d.textlength(footer, font=ff)) / 2, y), footer, font=ff, fill=INK)

    img.save("meme.png")
    img.resize((480, 480), Image.LANCZOS).save("thumb-480.png")
    print("wrote meme.png 1200x1200 and thumb-480.png 480x480")


if __name__ == "__main__":
    main()
