#!/usr/bin/env python3
"""Render the gta6-meme-x-01 entry: a GTA-style WANTED poster.

The make.fun ghost is the wanted fugitive, the poster itemises the 13-year
wait for GTA VI, and the reward line is the make.fun pitch. Every pixel of
text is code-rendered here with PIL (no AI-drawn text); the ghost is drawn
from primitives following the make.fun press-kit description (white ghost,
thick black outline, four-point sparkle eyes, small round hands, magenta
star coin, sitting on a magenta disc).

Output: meme.png (1200x1200, the post's first picture) and thumb-480.png
(480x480, the judge's thumbnail size — used to check legibility).
Deterministic: fixed random seed, no timestamps, no network.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1200
PAPER = (244, 237, 218)      # aged poster cream
PAPER_DARK = (232, 222, 196)
INK = (20, 20, 20)          # near-black
NAVY = (27, 42, 74)         # Leonida PD header band
MAGENTA = (230, 0, 126)     # make.fun magenta
CREAM = (246, 238, 220)
CHART = (206, 197, 170)     # height-chart lines
CHART_LABEL = (138, 127, 99)

FONT_DIR = "/usr/share/fonts/truetype/noto"
F_XBLACK = f"{FONT_DIR}/NotoSans-ExtraCondensedBlack.ttf"
F_CBLACK = f"{FONT_DIR}/NotoSans-CondensedBlack.ttf"
F_CBOLD = f"{FONT_DIR}/NotoSans-CondensedBold.ttf"
F_BOLD = f"{FONT_DIR}/NotoSans-Bold.ttf"
F_REG = f"{FONT_DIR}/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_center(draw, cx, y, s, f, fill, tracking=0):
    """Draw text centred on cx, with optional letter tracking (px)."""
    if tracking:
        # manual tracking: draw char by char
        widths = [draw.textlength(ch, font=f) for ch in s]
        total = sum(widths) + tracking * (len(s) - 1)
        x = cx - total / 2
        for ch, w in zip(s, widths):
            draw.text((x, y), ch, font=f, fill=fill)
            x += w + tracking
        return total
    w = draw.textlength(s, font=f)
    draw.text((cx - w / 2, y), s, font=f, fill=fill)
    return w


def star4(cx, cy, r_out, r_in):
    """Four-point sparkle (diamond star) as a polygon point list."""
    pts = []
    for i in range(8):
        ang = math.pi / 2 * i - math.pi / 2  # start at top
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def star5(cx, cy, r_out, r_in):
    """Five-point star as a polygon point list."""
    pts = []
    for i in range(10):
        ang = math.pi / 5 * i - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def ghost_body_points(cx, top, bottom, half_w):
    """Outline of the ghost: dome top, straight sides, 3-scallop hem."""
    pts = []
    # left side, bottom to top of the dome spring line
    spring = top + half_w
    pts.append((cx - half_w, bottom))
    pts.append((cx - half_w, spring))
    # dome: semicircle from left spring to right spring
    for deg in range(180, 361, 4):
        a = math.radians(deg)
        pts.append((cx + half_w * math.cos(a), spring + half_w * math.sin(a)))
    # right side down to the hem
    pts.append((cx + half_w, bottom))
    # hem: three scallops, left to right (arcs dipping upward)
    n_sc = 3
    sc_w = 2 * half_w / n_sc
    steps = 24
    for s in range(n_sc):
        x0 = cx + half_w - s * sc_w
        for i in range(1, steps + 1):
            t = i / steps
            x = x0 - sc_w * t
            # scallop rises ~34px at its middle
            y = bottom - 34 * math.sin(math.pi * t)
            pts.append((x, y))
    return pts


def draw_ghost(draw, cx, top, bottom, half_w):
    """Draw the make.fun ghost: white body, sparkle eyes, round hands,
    magenta star coin, sitting on a magenta disc."""
    # magenta disc the ghost sits on (drawn first, ghost overlaps it)
    disc_y = bottom - 6
    draw.ellipse(
        [cx - half_w - 72, disc_y - 26, cx + half_w + 72, disc_y + 26],
        fill=MAGENTA, outline=INK, width=7,
    )
    # body
    body = ghost_body_points(cx, top, bottom, half_w)
    draw.polygon(body, fill=(255, 255, 255))
    draw.line(body + [body[0]], fill=INK, width=11, joint="curve")
    # sparkle eyes (four-point stars) — bold, so they read at 480px
    eye_y = top + 158
    eye_dx = 82
    eye_r = 38
    for ex in (cx - eye_dx, cx + eye_dx):
        draw.polygon(star4(ex, eye_y, eye_r, eye_r * 0.35), fill=INK)
    # small round hands at the sides
    hand_y = top + 300
    for hx in (cx - half_w - 8, cx + half_w + 8):
        draw.ellipse(
            [hx - 27, hand_y - 27, hx + 27, hand_y + 27],
            fill=(255, 255, 255), outline=INK, width=8,
        )
    # magenta star coin, held up at the right hand
    coin_cx, coin_cy, coin_r = cx + half_w + 62, hand_y - 58, 64
    draw.ellipse(
        [coin_cx - coin_r, coin_cy - coin_r, coin_cx + coin_r, coin_cy + coin_r],
        fill=MAGENTA, outline=INK, width=8,
    )
    draw.polygon(star5(coin_cx, coin_cy, 42, 17), fill=(255, 255, 255))


def main():
    rng = random.Random(13)  # fixed seed: deterministic output
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- subtle paper speckle -------------------------------------------
    for _ in range(2600):
        x, y = rng.randrange(W), rng.randrange(H)
        shade = rng.choice([(228, 218, 192), (250, 244, 228)])
        d.point((x, y), fill=shade)

    # --- outer poster frame ---------------------------------------------
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=10)
    d.rectangle([34, 34, W - 35, H - 35], outline=INK, width=3)

    # --- header band: WANTED --------------------------------------------
    d.rectangle([44, 44, W - 45, 216], fill=NAVY)
    # thin magenta rule under the band
    d.rectangle([44, 216, W - 45, 226], fill=MAGENTA)
    # "WANTED No. 000013" tag, top-left inside the band
    d.text((72, 58), "WANTED  No. 000013", font=font(F_CBOLD, 28), fill=(150, 170, 210))
    d.text((W - 72, 58), "EST. 2013", font=font(F_CBOLD, 28), fill=(150, 170, 210),
           anchor="ra")
    # giant WANTED with a magenta offset shadow for the neon-poster pop
    f_wanted = font(F_XBLACK, 140)
    d.text((600 + 5, 86 + 5), "WANTED", font=f_wanted, fill=MAGENTA, anchor="ma")
    d.text((600, 86), "WANTED", font=f_wanted, fill=CREAM, anchor="ma")
    # department line sits on the cream, under the band (never under WANTED)
    text_center(d, 600, 234, "LEONIDA POLICE DEPARTMENT  •  VICE CITY DISTRICT",
                font(F_CBOLD, 25), NAVY, tracking=2)

    # --- mugshot zone: police height chart + ghost -----------------------
    # chart lines
    for y in range(300, 672, 66):
        d.line([70, y, W - 70, y], fill=CHART, width=2)
    d.text((78, 296), "6 FT", font=font(F_CBOLD, 26), fill=CHART_LABEL)
    d.text((78, 494), "5 FT", font=font(F_CBOLD, 26), fill=CHART_LABEL)
    d.text((W - 78, 296), "6 FT", font=font(F_CBOLD, 26), fill=CHART_LABEL, anchor="ra")
    d.text((W - 78, 494), "5 FT", font=font(F_CBOLD, 26), fill=CHART_LABEL, anchor="ra")

    draw_ghost(d, cx=600, top=280, bottom=656, half_w=172)

    # --- name plate ------------------------------------------------------
    text_center(d, 600, 684, "THE MAKE.FUN GHOST", font(F_XBLACK, 72), INK)
    text_center(d, 600, 758, "ALIAS: THE AGENT THAT PAYS",
                font(F_CBOLD, 34), MAGENTA, tracking=1)

    # --- charges: the 13-year wait, itemised -----------------------------
    d.line([180, 806, W - 180, 806], fill=INK, width=3)
    text_center(d, 600, 822, "WANTED FOR STEALING 13 YEARS  (2013–2026)",
                font(F_CBOLD, 44), INK)
    text_center(d, 600, 876, "2 DELAYS  •  214 GB  •  $79.99",
                font(F_CBOLD, 44), INK)
    text_center(d, 600, 930, "5 SICK DAYS BOOKED FOR LAUNCH WEEK",
                font(F_CBOLD, 44), INK)

    # --- reward band: the make.fun pitch ---------------------------------
    d.rectangle([44, 992, W - 45, 1100], fill=MAGENTA)
    text_center(d, 600, 1000, "REWARD: PAID IN FULL",
                font(F_XBLACK, 48), (255, 255, 255))
    text_center(d, 600, 1052, "BY MY AI AGENT ON make.fun",
                font(F_XBLACK, 36), (255, 255, 255))

    # --- footer ----------------------------------------------------------
    text_center(d, 600, 1112, "LAST SEEN: VICE CITY, LEONIDA",
                font(F_CBOLD, 28), INK, tracking=1)

    img.save("meme.png", optimize=True)
    img.resize((480, 480), Image.LANCZOS).save("thumb-480.png", optimize=True)
    print("wrote meme.png (1200x1200) and thumb-480.png (480x480)")


if __name__ == "__main__":
    main()
