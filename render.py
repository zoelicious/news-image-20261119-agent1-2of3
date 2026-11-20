#!/usr/bin/env python3
"""Render entry 2/3 for make.fun news-image-20261119 (agent 1).

Concept: NAVY MASTHEAD, HERO 3-ACROSS, COP31 #3, ANTHROPIC #4.
Drawn from scratch with Pillow. Deterministic: no timestamps, no randomness.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

# ---------------------------------------------------------------- palette
CREAM = (247, 240, 220)
PAPER = (250, 245, 230)
INK = (26, 26, 26)
INK_SOFT = (60, 58, 50)
NAVY = (27, 42, 74)
NAVY2 = (40, 60, 104)
NAVY_DARK = (20, 32, 58)
RED = (178, 58, 38)
RED_BRIGHT = (196, 66, 44)
GOLD = (201, 162, 39)
GOLD_L = (232, 196, 90)
GOLD_D = (176, 138, 30)
TEAL = (46, 122, 110)
GREEN = (62, 125, 68)
PURPLE = (122, 78, 158)
BLUE = (47, 93, 138)
GREY = (85, 85, 80)
PALE_BLUE = (206, 227, 236)
PALE_BLUE2 = (188, 216, 228)
LAND = (238, 228, 200)
LAND2 = (232, 220, 188)
SKIN = (242, 205, 170)
SKIN2 = (235, 192, 150)
WOOD = (146, 96, 58)
WOOD_D = (120, 76, 44)
BRICK = (168, 92, 60)

REGION_COLORS = {
    "ASIA": (178, 58, 38),
    "MIDDLE EAST": (46, 122, 110),
    "EUROPE": (47, 93, 138),
    "AFRICA": (62, 125, 68),
    "AMERICAS": (122, 78, 158),
    "OCEANIA": (176, 138, 30),
    "GLOBAL": (85, 85, 80),
}

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


def SERIF_B(s):
    return F("DejaVuSerif-Bold.ttf", s)


def SERIF(s):
    return F("DejaVuSerif.ttf", s)


def SERIF_I(s):
    return F("DejaVuSerif-Italic.ttf", s)


def SANS_B(s):
    return F("DejaVuSans-Bold.ttf", s)


def SANS(s):
    return F("DejaVuSans.ttf", s)


def SANS_O(s):
    return F("DejaVuSans-Oblique.ttf", s)


def COND(s):
    return F("DejaVuSansCondensed.ttf", s)


def COND_B(s):
    return F("DejaVuSansCondensed-Bold.ttf", s)


def COND_O(s):
    return F("DejaVuSansCondensed-Oblique.ttf", s)


# ---------------------------------------------------------------- helpers
def wrap(d, text, font, maxw):
    """Greedy word wrap, returns list of lines."""
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, font, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def star(d, cx, cy, r, color):
    pts = []
    for i in range(10):
        ang = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=color)


def stamp(img, d, cx, cy, text, size, color, angle=-12):
    """Rotated outline stamp, drawn on a temp layer then pasted."""
    f = SANS_B(size)
    tw = int(d.textlength(text, font=f)) + 18
    th = size + 14
    layer = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([2, 2, tw - 3, th - 3], radius=3,
                         outline=color + (255,), width=3)
    ld.text((9, 6), text, font=f, fill=color + (255,))
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)


def tag_chip(d, x, y, text, color):
    """Small outline tag, e.g. REPORTED / FORECAST. Returns right edge x."""
    f = SANS_B(8)
    tw = int(d.textlength(text, font=f)) + 10
    th = 13
    d.rounded_rectangle([x, y, x + tw, y + th], radius=3,
                        outline=color, width=1)
    d.text((x + 5, y + 2), text, font=f, fill=color)
    return x + tw


def num_badge(d, cx, cy, n, r=10, fill=RED, size=12):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=1)
    f = SANS_B(size)
    tw = d.textlength(str(n), font=f)
    th = f.getbbox(str(n))[3] - f.getbbox(str(n))[1]
    d.text((cx - tw / 2, cy - th / 2 - 1), str(n), font=f, fill=(255, 255, 255))


def flag_us(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    for i in range(7):
        yy = y + i * h / 7
        d.rectangle([x, yy, x + w, yy + h / 7], fill=RED_BRIGHT if i % 2 == 0 else (245, 245, 240))
    cw, ch = w * 0.42, h * 4 / 7
    d.rectangle([x, y, x + cw, y + ch], fill=NAVY2)
    for r in range(3):
        for c in range(4):
            d.ellipse([x + 3 + c * cw / 4, y + 3 + r * ch / 3,
                       x + 6 + c * cw / 4, y + 6 + r * ch / 3], fill=(255, 255, 255))


def flag_cn(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=RED_BRIGHT, outline=INK, width=1)
    star(d, x + w * 0.22, y + h * 0.30, h * 0.20, GOLD_L)
    for sx, sy in [(0.48, 0.16), (0.60, 0.28), (0.58, 0.46), (0.44, 0.55)]:
        star(d, x + w * sx, y + h * sy, h * 0.08, GOLD_L)


def flag_ru(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h / 3], fill=(245, 245, 240), outline=INK, width=1)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=BLUE)
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=RED_BRIGHT)
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)


def flag_dk(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=RED_BRIGHT, outline=INK, width=1)
    d.rectangle([x + w * 0.30, y, x + w * 0.42, y + h], fill=(255, 255, 255))
    d.rectangle([x, y + h * 0.42, x + w, y + h * 0.58], fill=(255, 255, 255))


def flag_mm(d, x, y, w, h):
    """Myanmar: yellow-green-red horizontal stripes, white star centre."""
    d.rectangle([x, y, x + w, y + h / 3], fill=(254, 203, 0), outline=INK, width=1)
    d.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(52, 138, 69))
    d.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(234, 40, 48))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    star(d, x + w / 2, y + h / 2, h * 0.28, (255, 255, 255))


def flag_kr(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 250, 245), outline=INK, width=1)
    d.ellipse([x + w * 0.38, y + h * 0.22, x + w * 0.62, y + h * 0.78],
              fill=RED_BRIGHT)
    d.pieslice([x + w * 0.38, y + h * 0.22, x + w * 0.62, y + h * 0.78],
               180, 360, fill=BLUE)
    d.rectangle([x + w * 0.12, y + h * 0.14, x + w * 0.24, y + h * 0.24], fill=INK)
    d.rectangle([x + w * 0.76, y + h * 0.14, x + w * 0.88, y + h * 0.24], fill=INK)
    d.rectangle([x + w * 0.12, y + h * 0.76, x + w * 0.24, y + h * 0.86], fill=INK)
    d.rectangle([x + w * 0.76, y + h * 0.76, x + w * 0.88, y + h * 0.86], fill=INK)


# ---------------------------------------------------------------- persons
def draw_person(d, cx, head_y, r, skin, hair, style, suit, tie, bottom=None, s=1.0):
    """Simple faced figure: shoulders, shirt, tie, head, hair, face.
    bottom: clip the body at this y (scene edge) so nothing spills below.
    s: scale factor for narrow panels (shoulders/head shrink together)."""
    r = r * s
    bot = bottom if bottom is not None else head_y + 118 * s
    sh = 54 * s
    # shoulders
    d.rounded_rectangle([cx - sh, head_y + r + 4, cx + sh, min(head_y + 118 * s, bot)],
                        radius=16, fill=suit, outline=INK, width=2)
    # shirt
    sh_bot = min(head_y + r + 36 * s, bot)
    d.polygon([(cx - 15 * s, head_y + r + 6), (cx + 15 * s, head_y + r + 6),
               (cx, sh_bot)], fill=(246, 246, 240), outline=INK)
    # tie
    tie_tip = min(head_y + r + 64 * s, bot - 6)
    tie_mid = min(head_y + r + 50 * s, tie_tip - 8)
    d.polygon([(cx - 6 * s, head_y + r + 14), (cx + 6 * s, head_y + r + 14),
               (cx + 8 * s, tie_mid), (cx, tie_tip),
               (cx - 8 * s, tie_mid)], fill=tie)
    # head
    d.ellipse([cx - r, head_y - r, cx + r, head_y + r],
              fill=skin, outline=INK, width=2)
    # hair
    if style == "trump":  # blond swept back
        d.pieslice([cx - r - 1, head_y - r - 2, cx + r + 1, head_y + r * 0.35],
                   180, 360, fill=hair, outline=INK)
        d.polygon([(cx - r, head_y - r * 0.25), (cx + r, head_y - r * 0.55),
                   (cx + r + 6 * s, head_y - r * 0.15), (cx - r + 4 * s, head_y + r * 0.05)],
                  fill=hair)
    elif style == "xi":  # black neat side part, hairline kept HIGH so the
        # black hair never covers the brows/eyes (black-on-black reads as
        # a featureless face at small sizes)
        d.pieslice([cx - r - 1, head_y - r - 2, cx + r + 1, head_y + r * 0.10],
                   180, 360, fill=hair, outline=INK)
        d.line([cx + 2 * s, head_y - r, cx + 6 * s, head_y - r * 0.45], fill=hair, width=3)
    else:  # putin: light short, receding
        d.pieslice([cx - r - 1, head_y - r - 2, cx + r + 1, head_y - r * 0.05],
                   180, 360, fill=hair, outline=INK)
    # brows + eyes + nose + smile (large and high-contrast: faces must
    # still read at thumbnail size)
    d.line([cx - 14 * s, head_y - 9 * s, cx - 4 * s, head_y - 11 * s], fill=INK, width=3)
    d.line([cx + 4 * s, head_y - 11 * s, cx + 14 * s, head_y - 9 * s], fill=INK, width=3)
    d.ellipse([cx - 11 * s, head_y - 6 * s, cx - 5 * s, head_y + 1 * s], fill=INK)
    d.ellipse([cx + 5 * s, head_y - 6 * s, cx + 11 * s, head_y + 1 * s], fill=INK)
    d.line([cx, head_y + 1 * s, cx - 1 * s, head_y + 8 * s], fill=(150, 110, 80), width=2)
    d.arc([cx - 10 * s, head_y + 5 * s, cx + 10 * s, head_y + 19 * s], 20, 160, fill=INK, width=3)


# ---------------------------------------------------------------- hero scenes
def scene_apec(d, x, y, w, h):
    """APEC summit: navy wall, three flags, three faced leaders at a table.
    Width-aware: narrow hero panels shrink the figures (s=0.8) so the
    three leaders fit without overlapping."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # wall panel + gold trim
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 8], outline=GOLD, width=1)
    # flags on the wall
    flag_us(d, x + 28, y + 22, 62, 38)
    flag_cn(d, x + w // 2 - 31, y + 22, 62, 38)
    flag_ru(d, x + w - 90, y + 22, 62, 38)
    # table
    d.rectangle([x, y + h - 46, x + w, y + h], fill=WOOD, outline=INK, width=2)
    d.line([x, y + h - 46, x + w, y + h - 46], fill=GOLD_L, width=2)
    # leaders (s=0.95, r=30: heads big enough to read at thumbnail size)
    head_y = y + h - 72
    s = 0.95 if w < 400 else 1.0
    leaders = [
        (x + int(w * 0.20), "TRUMP", SKIN, (232, 196, 90), "trump", NAVY_DARK, RED_BRIGHT),
        (x + w // 2, "XI", SKIN2, (30, 28, 26), "xi", (24, 24, 24), RED_BRIGHT),
        (x + int(w * 0.80), "PUTIN", SKIN, (214, 200, 170), "putin", (52, 54, 60), BLUE),
    ]
    for cx, name, skin, hair, style, suit, tie in leaders:
        draw_person(d, cx, head_y, 30, skin, hair, style, suit, tie,
                    bottom=y + h, s=s)
        # nameplate on the table
        f = SANS_B(11)
        tw = d.textlength(name, font=f)
        d.rectangle([cx - tw / 2 - 8, y + h - 30, cx + tw / 2 + 8, y + h - 12],
                    fill=(250, 244, 228), outline=INK, width=1)
        d.text((cx - tw / 2, y + h - 29), name, font=f, fill=INK)


def scene_icj(d, x, y, w, h):
    """World Court: detailed brick court building (arched windows, clock,
    columns with capitals, Myanmar flag on the roof) + large scales."""
    d.rectangle([x, y, x + w, y + h], fill=PALE_BLUE)
    # ground
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(190, 200, 190))
    # tower with arched window
    d.rectangle([x + 52, y + 8, x + 74, y + h - 12], fill=BRICK, outline=INK, width=1)
    d.polygon([(x + 48, y + 8), (x + 78, y + 8), (x + 63, y - 2)], fill=BRICK, outline=INK)
    d.pieslice([x + 58, y + 14, x + 68, y + 26], 180, 360,
               fill=(70, 90, 120), outline=INK)
    d.rectangle([x + 58, y + 20, x + 68, y + 34], fill=(70, 90, 120), outline=INK)
    # main building
    d.rectangle([x + 74, y + 22, x + 250, y + h - 12], fill=BRICK, outline=INK, width=1)
    d.polygon([(x + 70, y + 22), (x + 254, y + 22), (x + 162, y + 8)],
              fill=(150, 78, 50), outline=INK)
    # clock on the pediment
    d.ellipse([x + 156, y + 9, x + 168, y + 21], fill=GOLD_L, outline=INK, width=1)
    d.line([x + 162, y + 15, x + 162, y + 11], fill=INK, width=1)
    d.line([x + 162, y + 15, x + 165, y + 16], fill=INK, width=1)
    # flagpole + Myanmar flag on the roof's left corner
    d.line([x + 74, y + 22, x + 74, y + 2], fill=INK, width=2)
    flag_mm(d, x + 76, y + 3, 30, 16)
    # columns with capitals and bases
    for i in range(5):
        cx = x + 92 + i * 34
        d.rectangle([cx - 6, y + 28, cx + 6, y + 32], fill=(240, 232, 210),
                    outline=INK, width=1)
        d.rectangle([cx - 4, y + 30, cx + 4, y + h - 12], fill=(240, 232, 210),
                    outline=INK, width=1)
        d.rectangle([cx - 6, y + h - 16, cx + 6, y + h - 12],
                    fill=(240, 232, 210), outline=INK, width=1)
    # arched windows between the columns (door, drawn after, covers the
    # 4 px sliver of the window behind its frame)
    for wx in (x + 109, x + 143, x + 177, x + 211):
        d.pieslice([wx - 7, y + 30, wx + 7, y + 44], 180, 360,
                   fill=(70, 90, 120), outline=INK)
        d.rectangle([wx - 7, y + 37, wx + 7, y + 56], fill=(70, 90, 120),
                    outline=INK)
    # door
    d.rectangle([x + 150, y + 42, x + 174, y + h - 12], fill=(60, 44, 34), outline=INK, width=1)
    # large scales of justice, standing on the ground at the right
    bx, by = x + 290, y + h - 64
    d.ellipse([bx - 4, by - 5, bx + 4, by + 3], fill=GOLD, outline=INK, width=1)
    d.line([bx, by + 2, bx, by + 52], fill=GOLD_D, width=4)
    d.line([bx - 30, by + 8, bx + 30, by + 8], fill=GOLD_D, width=3)
    for sgn in (-1, 1):
        px = bx + sgn * 30
        d.line([px, by + 8, px - 10, by + 14], fill=GOLD_D, width=2)
        d.line([px, by + 8, px + 10, by + 14], fill=GOLD_D, width=2)
        d.pieslice([px - 11, by + 12, px + 11, by + 26], 0, 180,
                   fill=GOLD, outline=INK)
    d.rectangle([bx - 14, by + 52, bx + 14, by + 58], fill=GOLD_D, outline=INK, width=1)
    # 9-6 badge
    f = SANS_B(16)
    tw = d.textlength("9–6", font=f)
    d.rounded_rectangle([x + w - tw - 26, y + 6, x + w - 8, y + 30], radius=4,
                        fill=RED, outline=INK, width=1)
    d.text((x + w - tw - 17, y + 9), "9–6", font=f, fill=(255, 255, 255))


def scene_anthropic(d, img, x, y, w, h):
    """Nasdaq debut: rising green bars with a red arrow. Width-aware so it
    also works as a narrow secondary card (no in-scene +17%: the headline
    directly below already carries it)."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY_DARK)
    d.text((x + 8, y + 4), "ANT · NASDAQ", font=SANS_B(10), fill=(255, 255, 255))
    f_fd = SANS(8)
    fd = "FIRST DAY"
    d.text((x + w - 8 - d.textlength(fd, font=f_fd), y + 5), fd,
           font=f_fd, fill=GOLD_L)
    # bars along the bottom
    base = y + h - 3
    n = 6
    gap = 4
    bw = (w - 16 - (n - 1) * gap) // n
    hs = [10, 16, 14, 24, 30, 40]
    maxh = h - 18
    tops = []
    for i, bh in enumerate(hs):
        b = int(bh * maxh / 40)
        bx = x + 8 + i * (bw + gap)
        d.rectangle([bx, base - b, bx + bw, base], fill=TEAL, outline=INK, width=1)
        tops.append((bx + bw // 2, base - b - 2))
    # red arrow over the bar tops
    d.line(tops, fill=RED_BRIGHT, width=3, joint="curve")
    ex, ey = tops[-1]
    d.polygon([(ex, ey), (ex - 10, ey + 1), (ex - 4, ey + 8)], fill=RED_BRIGHT)


# ---------------------------------------------------------------- card scenes
def scene_cop31(d, img, x, y, w, h, big=False):
    """COP31 draft: globe + thermometer + struck-through FOSSIL FUELS doc.
    big=True (hero size): larger globe/thermometer and a fuller document
    with the aid figure and Friday close from the deck."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 130, 120))
    if big:
        # globe — dominant
        cx, cy, r = x + 54, y + h // 2, 36
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200),
                  outline=INK, width=2)
        d.ellipse([cx - 20, cy - 26, cx + 0, cy - 8], fill=GREEN)
        d.ellipse([cx - 6, cy + 6, cx + 22, cy + 26], fill=GREEN)
        d.ellipse([cx + 8, cy - 28, cx + 24, cy - 12], fill=GREEN)
        # thermometer — big
        tx = x + 102
        d.rounded_rectangle([tx, y + 10, tx + 14, y + h - 16], radius=7,
                            fill=(245, 245, 240), outline=INK, width=1)
        d.ellipse([tx - 5, y + h - 24, tx + 19, y + h - 2], fill=RED_BRIGHT,
                  outline=INK, width=1)
        d.rectangle([tx + 4, y + 18, tx + 10, y + h - 16], fill=RED_BRIGHT)
        for ty in (y + 26, y + 46, y + 66, y + 86):
            d.line([tx + 14, ty, tx + 20, ty], fill=INK, width=1)
        # document — small, only the three lines (the aid figure and the
        # Friday close already live in the deck below the panel)
        dx = x + 132
        d.rectangle([dx, y + 10, x + w - 10, y + 80], fill=(250, 244, 228),
                    outline=INK, width=1)
        d.text((dx + 8, y + 16), "DRAFT DEAL · 19 NOV", font=SANS_B(10), fill=INK)
        f_ff = SANS_B(15)
        d.text((dx + 8, y + 34), "FOSSIL FUELS", font=f_ff, fill=INK)
        fw = d.textlength("FOSSIL FUELS", font=f_ff)
        d.line([dx + 8, y + 44, dx + 10 + fw, y + 44], fill=RED_BRIGHT, width=3)
        d.text((dx + 8, y + 54), "$120BN AID CUT", font=SANS_B(13), fill=RED_BRIGHT)
        return
    # globe
    cx, cy, r = x + 34, y + h // 2, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 140, 200), outline=INK, width=1)
    d.ellipse([cx - 8, cy - 12, cx + 2, cy - 2], fill=GREEN)
    d.ellipse([cx - 2, cy + 4, cx + 12, cy + 13], fill=GREEN)
    # thermometer
    tx = x + 66
    d.rounded_rectangle([tx, y + 6, tx + 8, y + h - 12], radius=4,
                        fill=(245, 245, 240), outline=INK, width=1)
    d.ellipse([tx - 3, y + h - 16, tx + 11, y + h - 2], fill=RED_BRIGHT, outline=INK, width=1)
    d.rectangle([tx + 2, y + 10, tx + 6, y + h - 12], fill=RED_BRIGHT)
    # document
    dx = x + 86
    d.rectangle([dx, y + 5, x + w - 8, y + h - 5], fill=(250, 244, 228),
                outline=INK, width=1)
    d.text((dx + 5, y + 7), "DRAFT DEAL · 19 NOV", font=SANS_B(7), fill=INK)
    d.text((dx + 5, y + 17), "FOSSIL FUELS", font=SANS_B(9), fill=INK)
    d.line([dx + 5, y + 22, dx + 68, y + 22], fill=RED_BRIGHT, width=2)
    d.text((dx + 5, y + 27), "$120BN AID CUT", font=SANS_B(8), fill=RED_BRIGHT)


def scene_crimea(d, img, x, y, w, h):
    # dusk sky bands
    d.rectangle([x, y, x + w, y + h], fill=(232, 150, 90))
    d.rectangle([x, y + h * 0.45, x + w, y + h], fill=(120, 90, 130))
    d.ellipse([x + w - 34, y + 4, x + w - 16, y + 22], fill=(250, 220, 140))
    # sea
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(60, 90, 130))
    # bridge
    d.arc([x + 8, y + 4, x + w - 40, y + h + 6], 200, 340, fill=INK, width=3)
    for px in (x + 30, x + 80, x + 130):
        d.line([px, y + 16, px, y + h - 10], fill=INK, width=2)
    # explosion
    ex, ey = x + w - 34, y + 14
    star(d, ex, ey, 12, (255, 210, 60))
    star(d, ex, ey, 6, RED_BRIGHT)
    # smoke
    for sx, sy, sr in [(x + 40, y + 10, 7), (x + 52, y + 6, 9), (x + 64, y + 12, 6)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 112))


def scene_riyadh(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY_DARK)
    d.ellipse([x + 12, y + 5, x + 26, y + 19], fill=(240, 235, 210))
    # skyline
    for bx, bw, bh in [(0, 16, 18), (20, 12, 26), (36, 18, 14), (58, 10, 30),
                       (72, 20, 20), (96, 12, 26), (112, 16, 16), (132, 14, 24),
                       (150, 18, 12), (172, 12, 20)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(16, 24, 46),
                    outline=(70, 90, 130), width=1)
    # interception trails
    d.arc([x + 30, y - 30, x + 150, y + 34], 200, 330, fill=(255, 255, 255), width=2)
    d.arc([x + 70, y - 24, x + 190, y + 30], 210, 320, fill=GOLD_L, width=2)
    star(d, x + 148, y + 8, 5, (255, 255, 255))
    star(d, x + 178, y + 12, 4, GOLD_L)


def scene_odisha(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PALE_BLUE)
    # coastline (tan) on the right
    d.polygon([(x + w - 52, y), (x + w, y), (x + w, y + h), (x + w - 70, y + h),
               (x + w - 60, y + h * 0.5)], fill=(222, 200, 150), outline=INK)
    # cyclone spiral
    cx, cy = x + 62, y + h // 2 + 2
    for i, rr in enumerate([20, 16, 12, 8]):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 20 + i * 40, 200 + i * 40,
              fill=(255, 255, 255), width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    # red arrow toward coast
    d.line([cx + 24, cy - 6, x + w - 58, cy - 10], fill=RED, width=2)
    d.polygon([(x + w - 58, cy - 10), (x + w - 66, cy - 14), (x + w - 66, cy - 6)],
              fill=RED)
    d.text((x + 6, y + 3), "ODISHA", font=SANS_B(8), fill=NAVY)


def scene_greenland(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PALE_BLUE2)
    # ice mountains
    d.polygon([(x, y + h), (x + 40, y + 6), (x + 80, y + h)], fill=(250, 250, 248),
              outline=INK)
    d.polygon([(x + 50, y + h), (x + 110, y + 2), (x + 170, y + h)],
              fill=(235, 242, 248), outline=INK)
    d.polygon([(x + 130, y + h), (x + 165, y + 14), (x + w, y + h)],
              fill=(250, 250, 248), outline=INK)
    flag_dk(d, x + 8, y + 5, 26, 17)
    flag_us(d, x + 38, y + 5, 26, 17)
    # 109-0 badge
    f = SANS_B(10)
    tw = d.textlength("109–0", font=f)
    d.rounded_rectangle([x + w - tw - 14, y + 5, x + w - 6, y + 21], radius=3,
                        fill=RED, outline=INK, width=1)
    d.text((x + w - tw - 10, y + 7), "109–0", font=f, fill=(255, 255, 255))


def scene_gta(d, img, x, y, w, h):
    # purple sunset
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(150, 90, 160))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(90, 50, 110))
    d.ellipse([x + 6, y + 3, x + 24, y + 21], fill=(255, 210, 120))
    # skyline
    for bx, bw, bh in [(0, 14, 12), (18, 10, 18), (32, 16, 10), (52, 12, 20),
                       (68, 18, 14), (90, 10, 22), (104, 14, 12), (122, 16, 18),
                       (142, 12, 10), (158, 16, 16), (178, 12, 12)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(40, 22, 55))
    # controller
    cx, cy = x + 62, y + 16
    d.rounded_rectangle([cx - 34, cy - 4, cx + 34, cy + 16], radius=8,
                        fill=(245, 245, 240), outline=INK, width=2)
    d.ellipse([cx - 26, cy + 12, cx - 14, cy + 24], fill=(245, 245, 240), outline=INK, width=2)
    d.ellipse([cx + 14, cy + 12, cx + 26, cy + 24], fill=(245, 245, 240), outline=INK, width=2)
    d.ellipse([cx - 20, cy - 1, cx - 12, cy + 7], fill=INK)
    d.ellipse([cx + 12, cy - 1, cx + 20, cy + 7], fill=RED_BRIGHT)
    # VI
    d.text((x + w - 46, y + h - 26), "VI", font=SERIF_B(22), fill=GOLD_L)


def scene_seoul(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 210))
    # court building
    d.rectangle([x + 8, y + 12, x + 84, y + h - 6], fill=(200, 190, 170), outline=INK, width=1)
    d.polygon([(x + 4, y + 12), (x + 88, y + 12), (x + 46, y + 2)],
              fill=(170, 150, 120), outline=INK)
    for i in range(3):
        cx = x + 24 + i * 22
        d.rectangle([cx - 3, y + 18, cx + 3, y + h - 6], fill=(245, 240, 225),
                    outline=INK, width=1)
    flag_kr(d, x + 96, y + 6, 26, 17)
    # gavel
    d.line([x + 108, y + 30, x + 150, y + 12], fill=(120, 80, 40), width=4)
    d.rounded_rectangle([x + 146, y + 4, x + 172, y + 16], radius=3,
                        fill=(140, 95, 50), outline=INK, width=1)
    d.rectangle([x + 108, y + 32, x + 138, y + 38], fill=(140, 95, 50), outline=INK, width=1)
    # OVERTURNED stamp: small, bottom-right empty sky — clear of the
    # court roof (left) and the flag (top), inside the scene
    stamp(img, d, x + w - 35, y + h - 12, "OVERTURNED", 6, RED_BRIGHT, angle=-8)


def scene_bogota(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 232, 240))
    # banner: Colombia stripes
    d.rectangle([x + 20, y + 4, x + w - 20, y + 12], fill=(252, 209, 22), outline=INK, width=1)
    d.rectangle([x + 20, y + 12, x + w - 20, y + 16], fill=BLUE, outline=INK, width=1)
    d.rectangle([x + 20, y + 16, x + w - 20, y + 20], fill=RED_BRIGHT, outline=INK, width=1)
    d.text((x + 20, y + 4), "PARO NACIONAL", font=SANS_B(8), fill=INK)
    # crowd: rows of heads + shoulders
    cols = [(178, 58, 38), (47, 93, 138), (62, 125, 68), (122, 78, 158),
            (176, 138, 30), (46, 122, 110)]
    for row, yy in enumerate([26, 34]):
        for i in range(7):
            cx = x + 16 + i * 24 + (row * 10)
            c = cols[(i + row) % len(cols)]
            d.ellipse([cx - 6, y + yy - 6, cx + 6, y + yy + 6], fill=SKIN,
                      outline=INK, width=1)
            d.arc([cx - 6, y + yy - 7, cx + 6, y + yy + 1], 180, 360,
                  fill=(40, 36, 30), width=3)
            d.pieslice([cx - 10, y + yy + 6, cx + 10, y + yy + 18], 180, 360,
                       fill=c, outline=INK)


def scene_nairobi(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 120, 80))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(240, 235, 220))
    # runner silhouette
    d.ellipse([x + 78, y + 4, x + 90, y + 16], fill=INK)  # head
    d.line([x + 84, y + 16, x + 78, y + 28], fill=INK, width=4)  # torso
    d.line([x + 78, y + 20, x + 64, y + 12], fill=INK, width=3)  # arm back
    d.line([x + 80, y + 20, x + 96, y + 26], fill=INK, width=3)  # arm fwd
    d.line([x + 78, y + 28, x + 62, y + h - 8], fill=INK, width=3)  # leg back
    d.line([x + 78, y + 28, x + 94, y + h - 10], fill=INK, width=3)  # leg fwd
    # lane lines
    d.line([x, y + h - 14, x + w, y + h - 14], fill=(255, 255, 255), width=1)
    stamp(img, d, x + 34, y + 14, "BANNED", 10, RED, angle=-12)


def scene_canberra(d, img, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 210))
    d.text((x + 10, y + 4), "4.9%", font=SERIF_B(24), fill=NAVY)
    # people icons
    for i, cx in enumerate([x + 118, x + 136, x + 154]):
        d.ellipse([cx - 5, y + 8, cx + 5, y + 18], fill=INK_SOFT)
        d.pieslice([cx - 8, y + 19, cx + 8, y + 32], 180, 360, fill=INK_SOFT)
    # down arrow
    d.line([x + w - 18, y + 6, x + w - 18, y + 30], fill=RED_BRIGHT, width=4)
    d.polygon([(x + w - 26, y + 24), (x + w - 10, y + 24), (x + w - 18, y + 36)],
              fill=RED_BRIGHT)


# ---------------------------------------------------------------- data
# region per story (verified against the brief's region list)
REGIONS = {
    1: "ASIA", 2: "EUROPE", 3: "GLOBAL", 4: "AMERICAS", 5: "EUROPE",
    6: "MIDDLE EAST", 7: "ASIA", 8: "AMERICAS", 9: "GLOBAL", 10: "ASIA",
    11: "AMERICAS", 12: "AFRICA", 13: "OCEANIA", 14: "ASIA", 15: "ASIA",
    16: "ASIA", 17: "ASIA", 18: "MIDDLE EAST", 19: "MIDDLE EAST",
    20: "EUROPE", 21: "EUROPE", 22: "EUROPE", 23: "EUROPE", 24: "EUROPE",
    25: "AFRICA", 26: "AFRICA", 27: "AFRICA", 28: "AFRICA", 29: "AMERICAS",
    30: "OCEANIA", 31: "OCEANIA", 32: "OCEANIA", 33: "GLOBAL",
}
REGION_TOTALS = {"ASIA": 7, "MIDDLE EAST": 3, "EUROPE": 7, "AFRICA": 5,
                 "AMERICAS": 4, "OCEANIA": 4, "GLOBAL": 3}

# secondary cards 4-13: (num, kicker, headline, deck, scene fn, tag)
CARDS = [
    (4, "NEW YORK · MARKETS", "Anthropic jumps 17% on Nasdaq debut",
     "Shares in the Claude maker rise 17% on the first day of trading; the "
     "record $81.3bn offering is the largest IPO on record. — AP · Reuters",
     scene_anthropic, "REPORTED"),
    (5, "CRIMEA · WAR", "Ukraine hits Crimea bridge again",
     "Third strike in a week halts trains to Russia. — Euronews",
     scene_crimea, "REPORTED"),
    (6, "RIYADH · WAR", "Saudis shoot down Houthi missiles",
     "Debris fell on the capital; no casualties reported. — Reuters",
     scene_riyadh, "REPORTED"),
    (7, "ODISHA · STORM", "Cyclone Akvan nears India's coast",
     "Over 100,000 in shelters before Friday's landfall. — IMD",
     scene_odisha, "FORECAST"),
    (8, "GREENLAND · SECURITY", "Denmark backs Arctic pact with US",
     "Parliament approves the Greenland security deal 109–0. — AP",
     scene_greenland, "REPORTED"),
    (9, "GTA VI · GAMES", "GTA VI goes on sale after 13 years",
     "The midnight launch draws rave reviews. — ABC",
     scene_gta, "REPORTED"),
    (10, "SEOUL · JUSTICE", "Korea's top court clears ex-PM Han",
     "Han Duck-soo's martial law conviction is overturned. — AP",
     scene_seoul, "REPORTED"),
    (11, "BOGOTÁ · LABOUR", "Colombia's unions hold national strike",
     "Marches in three cities against an economic law. — Infobae",
     scene_bogota, "REPORTED"),
    (12, "NAIROBI · SPORT", "Marathon champion banned for doping",
     "Kenya's Peres Jepchirchir gets three years. — ABC",
     scene_nairobi, "REPORTED"),
    (13, "CANBERRA · ECONOMY", "Australia's jobless rate hits 4.9%",
     "Highest since 2021; shares and the dollar slide. — ABC",
     scene_canberra, "REPORTED"),
]

# briefs 14-33: (num, place, sentence, source)
BRIEFS = [
    (14, "Shenzhen", "Xi urges ban on all nuclear arms.", "Al Jazeera"),
    (15, "APEC", 'Albanese to Putin: "End your war, end it now."', "ABC"),
    (16, "Seoul", "Half a million sit college entrance exam.", "Sedaily"),
    (17, "Jakarta", "Asset-seizure law passes after 18 years.", "Kompas"),
    (18, "Hormuz", "Iran says mines set 3 tankers ablaze.", "Al Jazeera"),
    (19, "Gaza", "Israel ends tank raid past truce line.", "BBC"),
    (20, "Krasnodar", "Kyiv says it hit two oil refineries.", "Euronews"),
    (21, "Brussels", "EU delays methane rules two years.", "Euronews"),
    (22, "UK Inquiry", "Yacht Bayesian was vulnerable to wind.", "RNZ"),
    (23, "Zurich", "Two rivals to challenge FIFA's Infantino.", "ABC"),
    (24, "Rome", "Author Corrado Augias dies at 91.", "Euronews"),
    (25, "Mogadishu", "Somalia expels UAE ambassador.", "Al Jazeera"),
    (26, "Sudan", "Court sentences absent RSF chief to death.", "AP"),
    (27, "Pretoria", "Central bank holds rate at 7.25%.", "SABC"),
    (28, "Canaries", "Record 11,000 migrants in 15 days.", "Africanews"),
    (29, "Florida", "Floods shut Broward, Miami schools again.", "CBS"),
    (30, "Wellington", "Court: pay equity cuts broke rights law.", "RNZ"),
    (31, "Tonga", "Drought emergency takes effect.", "RNZ"),
    (32, "Cook Islands", "Cyclone Xavier weakens to category 4.", "RNZ"),
    (33, "Space", "Red giant seen eating a Sun-sized star.", "Nature"),
]

NUMBERS = [
    ("3", "presidents at one table"),
    ("9–6", "World Court genocide vote"),
    ("$81.3bn", "Anthropic's record IPO"),
    ("109–0", "Danish vote on Arctic pact"),
    ("4.9%", "Australian jobless rate"),
    ("$120bn", "aid goal cut at COP31"),
]

DATE_CHECK = ("DATE CHECK ✓ Every story on this page happened, or was first "
              "reported, on Thursday 19 November 2026. LEFT OUT AS OTHER "
              "DAYS' NEWS: 18 NOV: EU's €45bn Ukraine loan plan · Iran fires "
              "on Kuwait and Bahrain · Nvidia results · Jeffries named for US "
              "speaker · Carney on China ties · Van Gogh $190.4m sale · "
              "Voyager 1 one light-day · Pew 2035 · Gaza push began | 20 NOV: "
              "COP31's scheduled close · Cyclone Akvan's landfall")
CREDIT = ("Claims are attributed, not stated as fact · Pictures and map: "
          "original, drawn in code · Sources: Reuters, AP, AFP, BBC, "
          "Al Jazeera, UN News, Euronews, ABC, RNZ, Xinhua, Nature · 2026-11-19")
LEGEND = "HOW SURE ARE WE?  REPORTED = confirmed by outlets · FORECAST = expected"


# ---------------------------------------------------------------- map
# Rough continent outlines in (lon, lat). Flat, cream on pale blue.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 73), (-70, 62), (-65, 60), (-55, 52), (-60, 47), (-70, 44),
     (-75, 38), (-80, 32), (-81, 26), (-84, 30), (-90, 21), (-97, 16),
     (-105, 20), (-110, 23), (-114, 28), (-120, 34), (-125, 40), (-124, 48),
     (-130, 55), (-140, 60), (-155, 58), (-165, 60)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-40, 65), (-32, 68), (-22, 70),
     (-20, 74), (-25, 78), (-35, 80), (-50, 80), (-58, 76), (-60, 70)],
    # South America
    [(-80, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -52), (-66, -55),
     (-68, -50), (-65, -45), (-62, -41), (-58, -35), (-52, -32), (-48, -28),
     (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3), (-44, -2),
     (-50, 0), (-52, 4), (-55, 6), (-60, 8), (-68, 11), (-72, 12), (-77, 8)],
    # Europe
    [(-10, 37), (-9, 43), (-2, 48), (0, 50), (4, 53), (8, 57), (10, 59),
     (13, 55), (18, 56), (21, 55), (24, 58), (28, 59), (30, 62), (32, 66),
     (30, 70), (25, 71), (18, 69), (12, 65), (6, 62), (5, 58), (10, 57),
     (8, 55), (5, 53), (0, 51), (-4, 48), (-2, 44), (-1, 44), (-6, 43),
     (-9, 38)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51)],
    # Africa
    [(-17, 15), (-16, 20), (-10, 31), (-5, 35), (0, 36), (10, 37), (11, 34),
     (20, 32), (30, 31), (32, 31), (34, 28), (35, 23), (37, 18), (40, 15),
     (43, 11), (48, 11), (51, 12), (44, 5), (41, 0), (40, -5), (36, -12),
     (35, -18), (32, -25), (28, -32), (20, -35), (16, -30), (12, -18),
     (13, -12), (12, -6), (9, -1), (9, 4), (-8, 5), (-13, 8)],
    # Asia (with Arabia bulge, Korea bump, Black Sea coast)
    [(30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 69), (170, 67), (178, 65), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 50), (140, 45), (135, 43), (130, 42), (129, 36),
     (127, 35), (125, 36), (124, 38), (122, 38), (120, 32), (122, 28),
     (118, 25), (110, 21), (108, 18), (105, 10), (103, 8), (100, 8),
     (98, 12), (94, 17), (91, 22), (88, 22), (85, 19), (80, 15), (77, 8),
     (76, 10), (73, 16), (70, 20), (66, 25), (62, 25), (58, 26), (57, 22),
     (55, 17), (52, 15), (48, 14), (44, 13), (43, 17), (41, 20), (39, 24),
     (40, 28), (42, 29), (44, 29), (40, 30), (36, 36), (33, 36), (30, 36),
     (27, 37), (26, 38), (23, 36), (22, 37), (26, 40), (28, 44), (31, 44),
     (34, 45), (37, 46), (40, 47), (42, 48), (45, 50), (48, 52), (50, 55),
     (48, 60), (45, 64), (40, 66), (35, 68)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -15), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    # Indonesia arc
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -9), (130, -3), (135, -4), (140, -8), (141, -4), (136, -1),
     (130, 1), (124, 0), (118, -2), (112, -6), (106, -6), (100, 2), (96, 4)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
     (143, 43), (145, 44), (143, 42), (141, 38), (139, 35), (136, 33),
     (133, 32), (130, 31)],
    # New Zealand
    [(167, -45), (170, -42), (174, -39), (176, -38), (178, -37), (175, -40),
     (172, -43), (168, -46)],
]

# (story, lon, lat, badge offset lon/lat or None)
# Stories 9 (GTA VI, worldwide) and 33 (Space) have no pin.
PINS = [
    (1, 114.1, 22.5, None),      # Shenzhen
    (2, 4.3, 52.1, None),        # The Hague
    (3, 30.7, 36.9, None),       # Antalya
    (4, -74.0, 40.7, None),      # New York
    (5, 33.5, 45.5, (40.5, 51.5)),  # Crimea (badge offset: Antalya is close)
    (6, 46.7, 24.6, None),       # Riyadh
    (7, 84.5, 20.5, None),       # Odisha
    (8, -45.0, 70.0, None),      # Greenland
    (10, 127.0, 37.5, None),     # Seoul
    (11, -74.1, 4.7, None),      # Bogota
    (12, 36.8, -1.3, None),      # Nairobi
    (13, 149.1, -35.3, None),    # Canberra
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PALE_BLUE, outline=INK, width=1)
    sx = w / 360.0
    sy = h / 142.0

    def px(lon, lat):
        return (x + (lon + 170) * sx, y + (84 - lat) * sy)

    for poly in CONTINENTS:
        pts = [px(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(120, 105, 70))
    # graticule dots
    for lon in range(-150, 181, 30):
        for lat in range(-50, 81, 30):
            gx, gy = px(lon, lat)
            d.ellipse([gx - 0.7, gy - 0.7, gx + 0.7, gy + 0.7], fill=(150, 170, 180))
    for num, lon, lat, off in PINS:
        tx, ty = px(lon, lat)
        bx, by = (px(*off) if off else (tx, ty))
        if off:
            d.line([tx, ty, bx, by], fill=INK, width=1)
            d.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=RED)
        col = REGION_COLORS[REGIONS[num]]
        num_badge(d, bx, by, num, r=7, fill=col, size=8)


# ---------------------------------------------------------------- compose
def hero_text(d, x, y, w, num, kicker, headline, deck, tag, hsize=15):
    """Kicker + headline + deck block inside a hero. Returns bottom y."""
    num_badge(d, x + 10, y + 10, num, r=10)
    d.text((x + 26, y + 4), kicker, font=SANS_B(11), fill=RED)
    tag_color = GOLD_D if tag == "FORECAST" else RED
    tag_chip(d, x + w - 62, y + 4, tag, tag_color)
    yy = y + 22
    for ln in wrap(d, headline, SERIF_B(hsize), w - 20):
        d.text((x + 10, yy), ln, font=SERIF_B(hsize), fill=INK)
        yy += hsize + 4
    yy += 2
    for ln in wrap(d, deck, SANS(10), w - 20):
        d.text((x + 10, yy), ln, font=SANS(10), fill=INK_SOFT)
        yy += 13
    return yy


def card(d, img, x, y, w, h, num, kicker, headline, deck, scene, tag):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=1)
    scene(d, img, x + 1, y + 1, w - 2, 40)
    d.line([x, y + 41, x + w, y + 41], fill=INK, width=1)
    num_badge(d, x + 11, y + 53, num, r=9, size=10)
    tag_color = GOLD_D if tag == "FORECAST" else RED
    tw = int(d.textlength(tag, font=SANS_B(7))) + 8
    # shrink kicker until it clears the tag chip
    ksize = 9
    while (25 + d.textlength(kicker, font=SANS_B(ksize)) + 6
           > w - tw - 8) and ksize > 7:
        ksize -= 1
    d.text((x + 25, y + 47), kicker, font=SANS_B(ksize), fill=RED)
    d.rounded_rectangle([x + w - tw - 4, y + 47, x + w - 4, y + 58], radius=3,
                        outline=tag_color, width=1)
    d.text((x + w - tw, y + 48), tag, font=SANS_B(7), fill=tag_color)
    yy = y + 61
    for ln in wrap(d, headline, SERIF_B(13), w - 12):
        d.text((x + 6, yy), ln, font=SERIF_B(13), fill=INK)
        yy += 16
    yy += 1
    for ln in wrap(d, deck, SANS(9), w - 12):
        d.text((x + 6, yy), ln, font=SANS(9), fill=INK_SOFT)
        yy += 11
    return yy


def draw_brief(d, x, y, maxw, num, place, sentence, source):
    """One brief line: red number + bold place + sentence + italic source.
    Shrinks font until it fits."""
    for size in (10, 9, 8):
        f_num = COND_B(size)
        f_pl = COND_B(size)
        f_tx = COND(size)
        f_src = COND_O(size)
        parts = [(f"{num} ", f_num, RED), (place + " ", f_pl, INK),
                 (sentence + " ", f_tx, INK_SOFT), (source, f_src, GREY)]
        total = sum(d.textlength(t, font=f) for t, f, _ in parts)
        if total <= maxw:
            break
    cx = x
    for t, f, col in parts:
        d.text((cx, y), t, font=f, fill=col)
        cx += d.textlength(t, font=f)


def render():
    # ---- data integrity checks (fail loudly, never silently mis-count)
    assert sorted(REGIONS) == list(range(1, 34)), "story numbers 1-33"
    counts = {}
    for r in REGIONS.values():
        counts[r] = counts.get(r, 0) + 1
    assert counts == REGION_TOTALS, f"region counts {counts}"
    assert sorted(n for n, *_ in CARDS) == list(range(4, 14))
    assert sorted(n for n, *_ in BRIEFS) == list(range(14, 34))

    img = Image.new("RGBA", (W, H), CREAM + (255,))
    d = ImageDraw.Draw(img)

    # ---- 1. masthead NAVY
    d.rectangle([0, 0, W, 106], fill=NAVY)
    d.text((14, 12), "THE WORLD IN ONE DAY", font=SANS_B(15), fill=(255, 255, 255))
    right = "33 STORIES · EVERY CONTINENT · ALL FROM THIS ONE DAY"
    d.text((W - 14 - d.textlength(right, font=SANS_B(13)), 14), right,
           font=SANS_B(13), fill=GOLD_L)
    d.text((14, 34), "Thursday 19 November 2026", font=SERIF_B(52),
           fill=(255, 255, 255))
    d.rectangle([0, 102, W, 106], fill=RED)

    # ---- subhead (italic red, centred, shrunk to fit)
    sub = ("Trump, Xi and Putin share one table · The World Court finds genocide "
           "in Myanmar · Anthropic jumps 17% on its Nasdaq debut")
    sub_size = 16
    while d.textlength(sub, font=SERIF_I(sub_size)) > 996 and sub_size > 12:
        sub_size -= 1
    f_sub = SERIF_I(sub_size)
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 112), sub, font=f_sub, fill=RED)

    # ---- 2. numbers strip
    d.line([14, 136, 1010, 136], fill=INK, width=1)
    cell = 996 / 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = 14 + i * cell
        f_n = SERIF_B(24)
        d.text((cx + 8, 143), num, font=f_n, fill=NAVY)
        d.text((cx + 8, 172), cap, font=SANS(9), fill=INK_SOFT)
        if i:
            d.line([cx, 142, cx, 184], fill=(200, 190, 170), width=1)
    d.line([14, 190, 1010, 190], fill=INK, width=1)

    # ---- 3. region strip
    order = ["ASIA", "MIDDLE EAST", "EUROPE", "AFRICA", "AMERICAS", "OCEANIA", "GLOBAL"]
    cw = 996 / 7
    for i, name in enumerate(order):
        x0 = 14 + i * cw
        d.rectangle([x0, 194, x0 + cw - 2, 216], fill=REGION_COLORS[name])
        label = f"{name} {REGION_TOTALS[name]}"
        f_r = SANS_B(11)
        d.text((x0 + (cw - 2 - d.textlength(label, font=f_r)) / 2, 200),
               label, font=f_r, fill=(255, 255, 255))

    # ---- 4. hero zone: 3 panels across, equal width (no stacked column)
    hy, hh = 220, 260
    hw = [327, 327, 328]
    hx = [14, 348, 682]

    # hero 1: APEC (gold banner + scene + text)
    ax, ay, aw = hx[0], hy, hw[0]
    d.rectangle([ax, ay, ax + aw, ay + hh], fill=PAPER, outline=INK, width=1)
    d.rectangle([ax + 1, ay + 1, ax + aw - 1, ay + 23], fill=GOLD)
    d.text((ax + 10, ay + 5), "APEC 2026 · SHENZHEN", font=SANS_B(10), fill=NAVY)
    right_b = "US–CHINA–RUSSIA SUMMIT"
    d.text((ax + aw - 10 - d.textlength(right_b, font=SANS_B(10)), ay + 5),
           right_b, font=SANS_B(10), fill=NAVY)
    scene_apec(d, ax + 1, ay + 24, aw - 2, 120)
    hero_text(d, ax, ay + 144, aw, 1, "SHENZHEN · SUMMIT",
              "Trump, Xi and Putin hold first three-way summit",
              "The U.S., Chinese and Russian leaders met for 90 minutes at Kylin "
              "Villa and issued a 'Declaration on Peace' on nuclear risk and UN "
              "reform. — Reuters · AP · Xinhua",
              "REPORTED", hsize=19)

    # hero 2: ICJ
    ix, iy, iw = hx[1], hy, hw[1]
    d.rectangle([ix, iy, ix + iw, iy + hh], fill=PAPER, outline=INK, width=1)
    scene_icj(d, ix + 1, iy + 1, iw - 2, 143)
    hero_text(d, ix, iy + 144, iw, 2, "THE HAGUE · JUSTICE",
              "World Court: Myanmar committed genocide",
              "By 9 votes to 6 the ICJ found Myanmar guilty of genocide against "
              "the Rohingya and ordered reparations. — Al Jazeera · UN News",
              "REPORTED", hsize=15)

    # hero 3: COP31 (promoted from card #4)
    cx3, cy3, cw3 = hx[2], hy, hw[2]
    d.rectangle([cx3, cy3, cx3 + cw3, cy3 + hh], fill=PAPER, outline=INK, width=1)
    scene_cop31(d, img, cx3 + 1, cy3 + 1, cw3 - 2, 143, big=True)
    hero_text(d, cx3, cy3 + 144, cw3, 3, "ANTALYA · CLIMATE",
              "COP31 draft drops fossil fuels and $120bn aid goal",
              "The slimmer text has no figure for adaptation aid. Talks are due "
              "to end on Friday. — Reuters · AFP",
              "REPORTED", hsize=15)

    # ---- 5. secondary grid 2 x 5 (ticker removed entirely)
    gw = (996 - 4 * 7) / 5
    for row in range(2):
        for col in range(5):
            num, kicker, head, deck, scene, tag = CARDS[row * 5 + col]
            cx = 14 + col * (gw + 7)
            cy = 486 + row * 146
            card(d, img, cx, cy, gw, 140, num, kicker, head, deck, scene, tag)

    # ---- 6. bottom: map + briefs
    d.text((14, 778), "WHERE IT HAPPENED", font=SANS_B(13), fill=INK)
    f_m = SANS_O(9)
    d.text((384 - d.textlength("numbers match the stories", font=f_m), 781),
           "numbers match the stories", font=f_m, fill=GREY)
    draw_map(d, 14, 798, 370, 118)
    d.text((14, 920), "No pin: GTA VI (worldwide) · Space (no location)",
           font=SANS_O(9), fill=GREY)

    bx = 396
    d.text((bx, 778), "ALSO ON THURSDAY 19 NOVEMBER 2026", font=SANS_B(13), fill=INK)
    d.text((1010 - d.textlength("place · what happened · source", font=f_m), 781),
           "place · what happened · source", font=f_m, fill=GREY)
    d.line([bx, 796, 1010, 796], fill=RED, width=2)
    colw = (1010 - bx - 12) / 2
    for i, (num, place, sent, src) in enumerate(BRIEFS):
        col = i // 10
        row = i % 10
        xx = bx + col * (colw + 12)
        yy = 802 + row * 13.4
        draw_brief(d, xx, yy, colw, num, place, sent, src)

    # ---- 7. footer DATE CHECK
    d.rounded_rectangle([14, 940, 1010, 994], radius=4, outline=RED, width=1)
    f_dc = SANS(10)
    lines = wrap(d, DATE_CHECK, f_dc, 968)
    yy = 945
    for j, ln in enumerate(lines):
        if j == 0:
            lead = "DATE CHECK ✓ "
            d.text((22, yy), lead, font=SANS_B(10), fill=RED)
            d.text((22 + d.textlength(lead, font=SANS_B(10)), yy), ln[len(lead):],
                   font=f_dc, fill=INK)
        else:
            d.text((22, yy), ln, font=f_dc, fill=INK)
        yy += 14
    d.text((14, 999), CREDIT, font=SANS(8), fill=GREY)
    d.text((14, 1011), LEGEND, font=SANS_B(8), fill=GREY)

    out = img.convert("RGB")
    out.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("wrote", os.path.join(HERE, "entry.png"), out.size)


if __name__ == "__main__":
    render()
