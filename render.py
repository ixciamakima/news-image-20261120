#!/usr/bin/env python3
"""The World in One Day v3 - renderer for news-image-20261120 (Round 3).

Draws a single-page broadsheet summing up Friday 20 November 2026:
a markets-rout lead with a vector chart, a numbered world map, a
30-story pictogram grid, a closing-figures strip and a sources line.

Deterministic: no randomness, no timestamps; two runs of this file
produce a byte-identical entry.png. In-session only (uses Pillow);
the graded program main.py never imports this file.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1192
MARGIN = 20
CW = W - 2 * MARGIN  # content width = 984

PAPER = (247, 244, 236)
PANEL = (255, 253, 247)
INK = (22, 24, 28)
DARKGREY = (56, 58, 62)
GREY = (110, 113, 116)
RED = (178, 32, 44)
BLUE = (27, 74, 110)
GOLD = (169, 124, 26)
GREEN = (58, 110, 62)
CELL_LINE = (214, 208, 194)
DARK = (23, 26, 32)
DARK_LINE = (72, 78, 88)
PAPER_TXT = (244, 241, 233)
MUTED_DARK = (176, 182, 190)
CHART = (255, 96, 74)
OCEAN = (218, 227, 230)
LAND = (124, 146, 110)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SERIF_B, 44)
F_DATE = font(SANS_B, 42)
F_KICKER = font(SANS_B, 15)
F_LEAD_H = font(SANS_B, 24)
F_BODY = font(SANS, 15)
F_BODY_B = font(SANS_B, 15)
F_FIG = font(SANS_B, 15)
F_CHART_BIG = font(SANS_B, 21)
F_STRIP = font(SANS, 15)
F_STRIP_B = font(SANS_B, 15)
F_FOOT = font(SANS, 15)
F_MAP_T = font(SANS_B, 15)
F_NUM = font(SANS_B, 15)

MIN_FONT = 15  # no text on the page is smaller than this

# ---------------------------------------------------------------- lead

LEAD_HEADLINE = "GLOBAL MARKETS ROUT: WORST WEEK SINCE 2020"
LEAD_SUB = ("The AI bubble bursts: a Friday tech crash caps the worst week "
            "for world markets since March 2020 (AP \u00b7 CNN \u00b7 Reuters)")
LEAD_FIGS = [
    "NASDAQ 22,617.73 \u25bc 5.28%",
    "S&P 500 6,910.39 \u25bc 3.70% \u00b7 7th straight loss",
    "DOW 48,147.33 \u25bc 1.93%",
    "NVIDIA \u25bc 14% Fri \u00b7 \u221247.5% from Oct 6 peak",
    "SEC said to probe Nvidia accounting",
    "Huang out as CEO \u00b7 $2.7tn gone in a week",
    "ANTHROPIC \u25bc 8.5% \u2192 $88.91 (debut $97.17)",
    "GOLD $3,517.24 \u25bc 3.02% \u00b7 VIX 40 \u25b2 30%",
]
CHART_TITLE = "NASDAQ COMPOSITE \u2014 THE WEEK"
CHART_END = "22,617.73"
CHART_END_SUB = "\u25bc 5.28% FRIDAY"
CHART_CAPTION = "Nasdaq now negative for the year \u00b7 S&P 500 in correction"

# ------------------------------------------------------------- stories
# (number, icon, headline, detail) - every figure from the verified
# pool in DESIGN-BRIEF-V3.md; estimates flagged as estimates.

STORIES = [
    (1, "bridge", "Kyiv's Dnipro bridges hit",
     "3 bridges hit; 3 dead, 15 injured"),
    (2, "dove", "Trump, Xi, Putin sign pact",
     "Declaration signed in Shenzhen"),
    (3, "leaf", "COP31 runs into overtime",
     "Draft drops fossil-fuel wording"),
    (4, "cyclone", "Cyclone Akvan hits Odisha",
     "Gusts to 90 km/h at Gopalpur"),
    (5, "scales", "ICJ rules Myanmar genocide",
     "9\u20136: Rohingya genocide in 2017"),
    (6, "chartdown", "Asia's worst week since 2020",
     "Nikkei \u22124.1% \u00b7 Kospi \u22124.7% fall"),
    (7, "derrick", "Brent crude climbs to $92.22",
     "+0.3% on Riyadh, Hormuz fears"),
    (8, "tower", "Houthi strike damages tower",
     "PIF Tower hit 19 Nov; none hurt"),
    (9, "capitol", "Senate rejects Iran war vote",
     "War powers resolution fails 51\u201348"),
    (10, "bubbles", "Taiwan flags 2,700 accounts",
     "Meta told before 28 Nov vote"),
    (11, "flags", "Prabowo and Xi hold talks",
     "Economy and South China Sea talks"),
    (12, "globe", "Europe set for Russia talks",
     "Allies gather in Berlin (BBC, AP)"),
    (13, "shield", "11 nations drill in Poland",
     "Troops drill at Nowa Deba (AP)"),
    (14, "stars", "UK\u2013EU summit in Brussels",
     "Youth mobility, food, carbon link"),
    (15, "pin", "Iraq unit for Jurf al-Sakhar",
     "Kataib Hezbollah compromise deal"),
    (16, "boat", "Boat capsizes off Senegal",
     "8,200 reached Canaries in 12 days"),
    (17, "chain", "Nigeria acts on suicide law",
     "Tinubu bids to scrap jail terms"),
    (18, "ribbon", "S. Africa: 600 women killed",
     "Deaths within three months (BBC)"),
    (19, "cross", "Kenya clears last Ebola case",
     "Out 37 days after first case"),
    (20, "bomb", "Sydney man charged",
     "Car-bomb research, IS material"),
    (21, "rocket", "BepiColombo nears Mercury",
     "Orbit burn 21 Nov; 8-year voyage"),
    (22, "controller", "GTA VI launch-day estimate",
     "Estimate: 24.6m copies, $2.36bn"),
    (23, "checkered", "Norris on pole in Las Vegas",
     "1:47.934 wet lap; Hamilton 20th"),
    (24, "dollar", "Dollar tops April 2025 level",
     "Index 103.86 amid market rout"),
    (25, "chat", "Chen, Min Zin raised by US",
     "Aide raises detained Americans"),
    (26, "shieldx", "Russia: no guarantee plan",
     "Ryabkov rebuffs Ukraine pledges"),
    (27, "flagpole", "Israel completes Gaza op",
     "Beyond the Yellow Line (BBC)"),
    (28, "doc", "Venezuela signs US deal",
     "Army pact follows Maduro removal"),
    (29, "ballot", "Bukele seeks third term",
     "Launches third-term bid (AP)"),
    (30, "snowflake", "UK's coldest autumn night",
     "Forecast lows down to \u221210C (BBC)"),
]

# ----------------------------------------------------------------- map
# Land spans per row of a 98 x 30 dot grid.
# Longitude -170..190 across, latitude 82..-58 down.

MAP_COLS, MAP_ROWS = 98, 30
MAP_SPANS = [
    [(30, 36), (73, 75)],
    [(8, 12), (16, 22), (25, 28), (30, 38), (55, 60), (66, 72),
     (80, 86), (90, 95)],
    [(2, 10), (12, 28), (31, 37), (47, 50), (52, 95)],
    [(1, 11), (13, 30), (33, 36), (41, 41), (47, 52), (53, 96)],
    [(2, 10), (14, 31), (34, 35), (46, 53), (54, 96)],
    [(13, 30), (44, 46), (47, 55), (56, 93)],
    [(12, 29), (44, 45), (46, 56), (57, 85), (86, 87)],
    [(11, 27), (45, 54), (55, 87)],
    [(10, 26), (44, 52), (53, 84), (85, 86)],
    [(10, 25), (43, 52), (53, 83), (84, 85)],
    [(13, 27), (44, 80)],
    [(14, 25), (41, 70), (72, 78)],
    [(17, 23), (40, 61), (64, 71), (72, 79), (80, 81)],
    [(18, 24), (39, 56), (58, 61), (65, 70), (73, 76), (80, 80)],
    [(21, 25), (26, 35), (39, 57), (58, 61), (73, 76), (80, 81)],
    [(25, 36), (38, 58), (72, 76), (78, 84), (86, 89)],
    [(25, 36), (41, 58), (70, 76), (79, 85), (86, 90)],
    [(24, 36), (41, 57), (72, 78), (80, 84), (87, 90)],
    [(24, 36), (42, 56), (78, 86)],
    [(25, 36), (42, 55), (79, 86)],
    [(26, 35), (42, 47), (76, 87)],
    [(27, 35), (43, 48), (55, 56), (75, 87)],
    [(27, 35), (43, 48), (55, 55), (75, 87)],
    [(27, 33), (43, 47), (76, 87)],
    [(27, 31), (43, 46), (77, 87), (93, 94)],
    [(26, 29), (79, 86), (92, 94)],
    [(26, 28), (91, 93)],
    [(26, 28)],
    [(25, 28)],
    [(27, 28)],
]

MAP_X, MAP_Y, MAP_W, MAP_H = MARGIN, 480, CW, 144
LON0, LON1 = -170.0, 190.0
LAT0, LAT1 = 82.0, -58.0

# (story number, longitude, latitude)
MARKERS = [
    (1, 30.5, 50.4), (2, 114.1, 22.5), (3, 30.7, 36.9),
    (4, 84.9, 19.3), (5, 95.9, 21.9), (7, 51.5, 27.0),
    (8, 46.7, 24.6), (9, -77.0, 38.9), (10, 121.0, 23.7),
    (13, 21.8, 50.4), (16, -17.2, 14.7), (19, 37.9, -1.3),
    (20, 151.2, -33.9), (23, -115.1, 36.2), (27, 34.3, 31.4),
    (28, -66.9, 10.5), (29, -89.2, 13.8), (30, -1.5, 52.5),
]
MARKER_R = 12
MARKER_MIN_DIST = 25.0

STRIP_1 = ("NASDAQ 22,617.73 \u25bc5.28% \u00b7 S&P 500 6,910.39 "
          "\u25bc3.70% \u00b7 DOW 48,147.33 \u25bc1.93% \u00b7 GOLD $3,517.24 \u25bc3.02%")
STRIP_2 = ("BRENT $92.22 +0.3% \u00b7 VIX 40 \u25b230% \u00b7 DOLLAR INDEX 103.86 \u00b7 "
           "10-YEAR YIELD 4.91% \u00b7 NIKKEI \u22124.1% \u00b7 KOSPI \u22124.7%")
FOOTER = ("Sources: Reuters, BBC, AP, CNN, UN News, The Guardian, IMD, "
          "ESA. Figures as reported on the day; estimates flagged.")

# ---------------------------------------------------------------- icons
# Each icon draws inside a 30x30 box at (x, y) with stroke colour c.

def _l(d, pts, c, w=3):
    d.line(pts, fill=c, width=w, joint="curve")


def icon_bridge(d, x, y, c):
    _l(d, [(x + 2, y + 24), (x + 28, y + 24)], c)
    _l(d, [(x + 8, y + 24), (x + 8, y + 8), (x + 22, y + 8),
           (x + 22, y + 24)], c)
    d.arc([x + 1, y + 2, x + 29, y + 22], start=180, end=360, fill=c,
          width=3)
    _l(d, [(x + 15, y + 5), (x + 15, y + 24)], c, 2)


def icon_dove(d, x, y, c):
    d.polygon([(x + 2, y + 15), (x + 9, y + 19), (x + 3, y + 25)],
              fill=c)
    d.ellipse([x + 5, y + 12, x + 23, y + 24], fill=c)
    d.ellipse([x + 19, y + 5, x + 28, y + 14], fill=c)
    d.polygon([(x + 27, y + 9), (x + 30, y + 11), (x + 27, y + 13)],
              fill=GOLD)
    d.arc([x + 6, y + 3, x + 22, y + 17], start=195, end=325, fill=c,
          width=3)
    _l(d, [(x + 25, y + 14), (x + 29, y + 18)], GREEN, 2)
    d.ellipse([x + 27, y + 17, x + 30, y + 20], fill=GREEN)


def icon_leaf(d, x, y, c):
    d.polygon([(x + 15, y + 2), (x + 26, y + 10), (x + 24, y + 22),
               (x + 14, y + 27), (x + 6, y + 20), (x + 7, y + 9)],
              outline=c, width=3)
    _l(d, [(x + 10, y + 22), (x + 21, y + 9)], c, 2)
    _l(d, [(x + 9, y + 25), (x + 5, y + 29)], c, 2)


def icon_cyclone(d, x, y, c):
    pts = []
    for i in range(61):
        t = i / 60.0
        ang = t * 4.6 * math.pi
        r = 2 + 11 * t
        pts.append((x + 15 + r * math.cos(ang),
                    y + 15 + r * math.sin(ang)))
    _l(d, pts, c, 3)


def icon_scales(d, x, y, c):
    _l(d, [(x + 15, y + 4), (x + 15, y + 24)], c)
    _l(d, [(x + 4, y + 7), (x + 26, y + 7)], c)
    for px in (4, 26):
        _l(d, [(x + px, y + 7), (x + px - 3, y + 15),
               (x + px + 3, y + 15), (x + px, y + 7)], c, 2)
        d.arc([x + px - 4, y + 13, x + px + 4, y + 19], start=0,
              end=180, fill=c, width=2)
    _l(d, [(x + 9, y + 27), (x + 21, y + 27)], c)


def icon_chartdown(d, x, y, c):
    _l(d, [(x + 4, y + 3), (x + 4, y + 26), (x + 27, y + 26)], c, 2)
    _l(d, [(x + 7, y + 8), (x + 13, y + 13), (x + 17, y + 10),
           (x + 24, y + 19)], RED, 3)
    _l(d, [(x + 19, y + 19), (x + 25, y + 19), (x + 24, y + 13)],
       RED, 2)


def icon_derrick(d, x, y, c):
    _l(d, [(x + 9, y + 27), (x + 13, y + 4), (x + 17, y + 4),
           (x + 21, y + 27)], c)
    _l(d, [(x + 11, y + 18), (x + 19, y + 18)], c, 2)
    _l(d, [(x + 10, y + 22), (x + 20, y + 12)], c, 2)
    _l(d, [(x + 20, y + 22), (x + 10, y + 12)], c, 2)
    _l(d, [(x + 5, y + 27), (x + 25, y + 27)], c, 2)


def icon_tower(d, x, y, c):
    d.rectangle([x + 10, y + 5, x + 21, y + 27], outline=c, width=3)
    for wy in (10, 15, 20):
        _l(d, [(x + 13, y + wy), (x + 18, y + wy)], c, 2)
    for dx, dy in ((-4, -3), (0, -5), (4, -3), (-5, 1), (5, 1)):
        _l(d, [(x + 24 + dx, y + 6 + dy), (x + 24, y + 6)], RED, 2)


def icon_capitol(d, x, y, c):
    d.arc([x + 8, y + 2, x + 22, y + 14], start=180, end=360, fill=c,
          width=3)
    _l(d, [(x + 15, y + 2), (x + 15, y + 5)], c, 2)
    _l(d, [(x + 4, y + 14), (x + 26, y + 14)], c)
    for cx in (7, 12, 17, 22):
        _l(d, [(x + cx, y + 17), (x + cx, y + 23)], c, 2)
    _l(d, [(x + 4, y + 26), (x + 26, y + 26)], c)


def icon_bubbles(d, x, y, c):
    d.rounded_rectangle([x + 2, y + 4, x + 19, y + 17], radius=4,
                        outline=c, width=3)
    d.rounded_rectangle([x + 12, y + 13, x + 28, y + 25], radius=4,
                        outline=BLUE, width=3)
    _l(d, [(x + 6, y + 17), (x + 5, y + 22)], c, 2)
    _l(d, [(x + 23, y + 25), (x + 24, y + 29)], BLUE, 2)


def icon_flags(d, x, y, c):
    _l(d, [(x + 9, y + 27), (x + 12, y + 4)], c)
    _l(d, [(x + 21, y + 27), (x + 18, y + 4)], BLUE)
    d.polygon([(x + 12, y + 4), (x + 21, y + 6), (x + 12, y + 10)],
              outline=RED, width=2)
    d.polygon([(x + 18, y + 4), (x + 10, y + 7), (x + 17, y + 11)],
              outline=GOLD, width=2)


def icon_globe(d, x, y, c):
    d.ellipse([x + 4, y + 3, x + 26, y + 27], outline=c, width=3)
    d.ellipse([x + 10, y + 3, x + 20, y + 27], outline=c, width=2)
    _l(d, [(x + 4, y + 15), (x + 26, y + 15)], c, 2)


def icon_shield(d, x, y, c):
    d.polygon([(x + 15, y + 2), (x + 25, y + 5), (x + 25, y + 14),
               (x + 15, y + 28), (x + 5, y + 14), (x + 5, y + 5)],
              outline=c, width=3)
    for ang in (90, 162, 234, 306, 18):
        a = math.radians(ang)
        _l(d, [(x + 15, y + 15),
               (x + 15 + 6 * math.cos(a), y + 15 - 6 * math.sin(a))],
           GOLD, 2)


def icon_stars(d, x, y, c):
    for i in range(8):
        a = math.radians(i * 45)
        px, py = x + 15 + 10 * math.cos(a), y + 15 + 10 * math.sin(a)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)
    d.ellipse([x + 13, y + 13, x + 17, y + 17], fill=c)


def icon_pin(d, x, y, c):
    d.ellipse([x + 8, y + 3, x + 22, y + 17], outline=c, width=3)
    d.polygon([(x + 9, y + 14), (x + 21, y + 14), (x + 15, y + 28)],
              outline=c, width=3)
    d.ellipse([x + 12, y + 7, x + 18, y + 13], fill=RED)


def icon_boat(d, x, y, c):
    d.polygon([(x + 4, y + 19), (x + 26, y + 19), (x + 22, y + 25),
               (x + 8, y + 25)], outline=c, width=3)
    _l(d, [(x + 15, y + 19), (x + 15, y + 5)], c, 2)
    d.polygon([(x + 15, y + 5), (x + 23, y + 17), (x + 15, y + 17)],
              outline=BLUE, width=2)
    d.arc([x + 2, y + 24, x + 12, y + 30], start=0, end=180, fill=BLUE,
          width=2)
    d.arc([x + 16, y + 24, x + 26, y + 30], start=0, end=180,
          fill=BLUE, width=2)


def icon_chain(d, x, y, c):
    d.arc([x + 2, y + 8, x + 16, y + 22], start=90, end=330, fill=c,
          width=3)
    d.arc([x + 14, y + 8, x + 28, y + 22], start=270, end=150,
          fill=BLUE, width=3)
    _l(d, [(x + 13, y + 4), (x + 17, y + 9)], RED, 2)
    _l(d, [(x + 17, y + 26), (x + 13, y + 21)], RED, 2)


def icon_ribbon(d, x, y, c):
    d.arc([x + 7, y + 3, x + 23, y + 19], start=0, end=360, fill=c,
          width=3)
    d.polygon([(x + 10, y + 16), (x + 16, y + 16), (x + 19, y + 28),
               (x + 13, y + 24), (x + 9, y + 28)], outline=c, width=2)


def icon_cross(d, x, y, c):
    d.ellipse([x + 3, y + 3, x + 27, y + 27], outline=c, width=3)
    d.polygon([(x + 12, y + 8), (x + 18, y + 8), (x + 18, y + 12),
               (x + 22, y + 12), (x + 22, y + 18), (x + 18, y + 18),
               (x + 18, y + 22), (x + 12, y + 22), (x + 12, y + 18),
               (x + 8, y + 18), (x + 8, y + 12), (x + 12, y + 12)],
              fill=RED)


def icon_bomb(d, x, y, c):
    d.ellipse([x + 5, y + 10, x + 25, y + 29], outline=c, width=3)
    d.arc([x + 14, y + 2, x + 26, y + 12], start=270, end=360, fill=c,
          width=2)
    for dx, dy in ((26, 2), (28, 6), (24, 0)):
        _l(d, [(x + 24, y + 5), (x + dx, y + dy)], GOLD, 2)


def icon_rocket(d, x, y, c):
    d.polygon([(x + 15, y + 2), (x + 21, y + 10), (x + 21, y + 20),
               (x + 9, y + 20), (x + 9, y + 10)], outline=c, width=3)
    d.ellipse([x + 12, y + 8, x + 18, y + 14], outline=BLUE, width=2)
    d.polygon([(x + 9, y + 17), (x + 4, y + 24), (x + 9, y + 23)],
              outline=c, width=2)
    d.polygon([(x + 21, y + 17), (x + 26, y + 24), (x + 21, y + 23)],
              outline=c, width=2)
    d.polygon([(x + 12, y + 23), (x + 18, y + 23), (x + 15, y + 29)],
              outline=RED, width=2)


def icon_controller(d, x, y, c):
    d.rounded_rectangle([x + 2, y + 9, x + 28, y + 23], radius=7,
                        outline=c, width=3)
    _l(d, [(x + 9, y + 13), (x + 9, y + 19)], c, 2)
    _l(d, [(x + 6, y + 16), (x + 12, y + 16)], c, 2)
    d.ellipse([x + 19, y + 12, x + 22, y + 15], fill=RED)
    d.ellipse([x + 22, y + 16, x + 25, y + 19], fill=GOLD)


def icon_checkered(d, x, y, c):
    _l(d, [(x + 7, y + 28), (x + 7, y + 3)], c)
    for r in range(2):
        for col in range(3):
            if (r + col) % 2 == 0:
                d.rectangle([x + 7 + col * 6, y + 3 + r * 5,
                             x + 13 + col * 6, y + 8 + r * 5],
                            fill=c)
    d.rectangle([x + 7, y + 3, x + 25, y + 13], outline=c, width=2)


def icon_dollar(d, x, y, c):
    d.ellipse([x + 4, y + 3, x + 26, y + 27], outline=GOLD, width=3)
    d.text((x + 15, y + 14), "$", font=font(SANS_B, 17), fill=GOLD,
           anchor="mm")


def icon_chat(d, x, y, c):
    d.rounded_rectangle([x + 3, y + 5, x + 27, y + 21], radius=5,
                        outline=c, width=3)
    _l(d, [(x + 9, y + 21), (x + 8, y + 27), (x + 15, y + 21)], c, 2)
    for dx in (9, 15, 21):
        d.ellipse([x + dx - 1, y + 12, x + dx + 1, y + 14], fill=c)


def icon_shieldx(d, x, y, c):
    d.polygon([(x + 15, y + 2), (x + 25, y + 5), (x + 25, y + 14),
               (x + 15, y + 28), (x + 5, y + 14), (x + 5, y + 5)],
              outline=c, width=3)
    _l(d, [(x + 10, y + 10), (x + 20, y + 19)], RED, 3)
    _l(d, [(x + 20, y + 10), (x + 10, y + 19)], RED, 3)


def icon_flagpole(d, x, y, c):
    _l(d, [(x + 10, y + 28), (x + 10, y + 3)], c)
    d.polygon([(x + 10, y + 3), (x + 26, y + 7), (x + 10, y + 12)],
              outline=RED, width=3)


def icon_doc(d, x, y, c):
    d.rectangle([x + 7, y + 3, x + 24, y + 27], outline=c, width=3)
    _l(d, [(x + 11, y + 10), (x + 20, y + 10)], c, 2)
    _l(d, [(x + 11, y + 15), (x + 20, y + 15)], c, 2)
    _l(d, [(x + 11, y + 20), (x + 17, y + 20)], c, 2)
    d.ellipse([x + 18, y + 19, x + 22, y + 23], fill=GOLD)


def icon_ballot(d, x, y, c):
    d.rectangle([x + 8, y + 2, x + 22, y + 13], outline=c, width=2)
    _l(d, [(x + 11, y + 8), (x + 14, y + 11), (x + 19, y + 5)], GREEN,
       2)
    d.rectangle([x + 4, y + 16, x + 26, y + 27], outline=c, width=3)
    _l(d, [(x + 8, y + 20), (x + 22, y + 20)], c, 2)


def icon_snowflake(d, x, y, c):
    cx, cy = x + 15, y + 15
    for ang in (0, 60, 120):
        a = math.radians(ang)
        dx, dy = 11 * math.cos(a), 11 * math.sin(a)
        _l(d, [(cx - dx, cy - dy), (cx + dx, cy + dy)], BLUE, 3)
        for s in (-1, 1):
            bx, by = cx + s * dx * 0.55, cy + s * dy * 0.55
            for bang in (ang + 35, ang - 35):
                ba = math.radians(bang)
                _l(d, [(bx, by),
                       (bx + 4 * math.cos(ba), by + 4 * math.sin(ba))],
                   BLUE, 2)


ICONS = {
    "bridge": icon_bridge, "dove": icon_dove, "leaf": icon_leaf,
    "cyclone": icon_cyclone, "scales": icon_scales,
    "chartdown": icon_chartdown, "derrick": icon_derrick,
    "tower": icon_tower, "capitol": icon_capitol,
    "bubbles": icon_bubbles, "flags": icon_flags, "globe": icon_globe,
    "shield": icon_shield, "stars": icon_stars, "pin": icon_pin,
    "boat": icon_boat, "chain": icon_chain, "ribbon": icon_ribbon,
    "cross": icon_cross, "bomb": icon_bomb, "rocket": icon_rocket,
    "controller": icon_controller, "checkered": icon_checkered,
    "dollar": icon_dollar, "chat": icon_chat, "shieldx": icon_shieldx,
    "flagpole": icon_flagpole, "doc": icon_doc, "ballot": icon_ballot,
    "snowflake": icon_snowflake,
}

ICON_COLORS = {
    "bridge": BLUE, "dove": GREEN, "leaf": GREEN, "cyclone": BLUE,
    "scales": GOLD, "chartdown": INK, "derrick": INK, "tower": INK,
    "capitol": BLUE, "bubbles": INK, "flags": INK, "globe": BLUE,
    "shield": BLUE, "stars": BLUE, "pin": BLUE, "boat": INK,
    "chain": INK, "ribbon": RED, "cross": INK, "bomb": INK,
    "rocket": BLUE, "controller": INK, "checkered": INK,
    "dollar": GOLD, "chat": BLUE, "shieldx": INK, "flagpole": INK,
    "doc": INK, "ballot": INK, "snowflake": BLUE,
}

# -------------------------------------------------------------- checks

FIT = []  # (label, measured_width, max_width)


# -------------------------------------------------------------- layout

def draw_masthead(d):
    t = "THE WORLD IN ONE DAY"
    FIT.append(("title", d.textlength(t, font=F_TITLE), CW))
    d.text((W / 2, 14), t, font=F_TITLE, fill=INK, anchor="ma")
    t = "FRIDAY 20 NOVEMBER 2026"
    FIT.append(("date", d.textlength(t, font=F_DATE), CW))
    d.text((W / 2, 74), t, font=F_DATE, fill=RED, anchor="ma")
    t = "31 STORIES \u00b7 ONE PAGE \u00b7 EVERY FIGURE AS REPORTED ON THE DAY"
    FIT.append(("kicker", d.textlength(t, font=F_KICKER), CW))
    d.text((W / 2, 130), t, font=F_KICKER, fill=DARKGREY, anchor="ma")
    d.rectangle([MARGIN, 156, W - MARGIN, 159], fill=INK)
    d.rectangle([MARGIN, 162, W - MARGIN, 163], fill=INK)


def draw_lead(d):
    d.rectangle([MARGIN, 172, W - MARGIN, 444], fill=DARK)
    tag = "LEAD"
    tw = d.textlength(tag, font=F_BODY_B)
    d.rectangle([36, 186, 36 + tw + 16, 212], fill=RED)
    d.text((36 + 8, 190), tag, font=F_BODY_B, fill=(255, 255, 255))
    hx = 36 + tw + 16 + 12
    FIT.append(("lead headline",
                (hx - MARGIN) + d.textlength(LEAD_HEADLINE,
                                             font=F_LEAD_H), CW))
    d.text((hx, 184), LEAD_HEADLINE, font=F_LEAD_H, fill=PAPER_TXT)
    FIT.append(("lead sub", d.textlength(LEAD_SUB, font=F_BODY),
                CW - 32))
    d.text((36, 222), LEAD_SUB, font=F_BODY, fill=MUTED_DARK)
    # chart
    FIT.append(("chart title", d.textlength(CHART_TITLE,
                                            font=F_BODY_B), 520))
    d.text((36, 252), CHART_TITLE, font=F_BODY_B, fill=PAPER_TXT)
    gx0, gx1, gy0, gy1 = 40, 552, 286, 388
    for fr in (0.25, 0.5, 0.75):
        gy = gy0 + fr * (gy1 - gy0)
        d.line([(gx0, gy), (gx1, gy)], fill=DARK_LINE, width=1)
    frac = [0.15, 0.28, 0.45, 0.60, 0.95]
    xs = [64, 174, 284, 394, 516]
    pts = [(x, gy0 + f * (gy1 - gy0)) for x, f in zip(xs, frac)]
    d.line(pts, fill=CHART, width=4, joint="curve")
    for (px, py) in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=CHART)
    for x, lab in zip(xs, ["MON", "TUE", "WED", "THU", "FRI"]):
        d.text((x, 394), lab, font=F_BODY, fill=MUTED_DARK,
               anchor="ma")
    d.text((548, 292), CHART_END, font=F_CHART_BIG, fill=CHART,
           anchor="ra")
    d.text((548, 320), CHART_END_SUB, font=F_BODY_B, fill=CHART,
           anchor="ra")
    FIT.append(("chart caption",
                d.textlength(CHART_CAPTION, font=F_BODY), 500))
    d.text((36, 418), CHART_CAPTION, font=F_BODY, fill=MUTED_DARK)
    # figures column
    d.line([(568, 252), (568, 426)], fill=DARK_LINE, width=1)
    for i, line in enumerate(LEAD_FIGS):
        FIT.append((f"lead fig {i + 1}",
                    d.textlength(line, font=F_FIG), 404))
        d.text((584, 252 + i * 22), line, font=F_FIG, fill=PAPER_TXT)


def project(lon, lat):
    x = MAP_X + (lon - LON0) / (LON1 - LON0) * MAP_W
    y = MAP_Y + (LAT0 - lat) / (LAT0 - LAT1) * MAP_H
    return [x, y]


def relax_markers(pts):
    for _ in range(500):
        moved = False
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx = pts[j][0] - pts[i][0]
                dy = pts[j][1] - pts[i][1]
                dist = math.hypot(dx, dy)
                if dist < MARKER_MIN_DIST:
                    if dist == 0:
                        dx, dy, dist = 1.0, 0.0, 1.0
                    push = (MARKER_MIN_DIST - dist) / 2 + 0.05
                    ux, uy = dx / dist, dy / dist
                    pts[i][0] -= ux * push
                    pts[i][1] -= uy * push
                    pts[j][0] += ux * push
                    pts[j][1] += uy * push
                    moved = True
        for p in pts:
            p[0] = min(max(p[0], MAP_X + MARKER_R + 2),
                       MAP_X + MAP_W - MARKER_R - 2)
            p[1] = min(max(p[1], MAP_Y + MARKER_R + 2),
                       MAP_Y + MAP_H - MARKER_R - 2)
        if not moved:
            break
    return pts


def draw_map(d):
    t = "WHERE IT HAPPENED \u2014 FRIDAY'S STORIES ON THE MAP"
    FIT.append(("map title", d.textlength(t, font=F_MAP_T), 700))
    d.text((MARGIN, 458), t, font=F_MAP_T, fill=INK)
    t2 = "marker numbers match the grid below"
    FIT.append(("map note", d.textlength(t2, font=F_BODY), 400))
    d.text((W - MARGIN, 458), t2, font=F_BODY, fill=GREY, anchor="ra")
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                fill=OCEAN)
    cw = MAP_W / MAP_COLS
    ch = MAP_H / MAP_ROWS
    for r, spans in enumerate(MAP_SPANS):
        for (c0, c1) in spans:
            d.rectangle([MAP_X + c0 * cw, MAP_Y + r * ch,
                         MAP_X + (c1 + 1) * cw,
                         MAP_Y + (r + 1) * ch], fill=LAND)
    d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H],
                outline=INK, width=1)
    pts = relax_markers([project(lon, lat) for _, lon, lat in MARKERS])
    min_dist = min(
        math.hypot(pts[j][0] - pts[i][0], pts[j][1] - pts[i][1])
        for i in range(len(pts)) for j in range(i + 1, len(pts)))
    for (num, _, _), (px, py) in zip(MARKERS, pts):
        d.ellipse([px - MARKER_R, py - MARKER_R, px + MARKER_R,
                   py + MARKER_R], fill=RED, outline=(255, 255, 255),
                  width=2)
        d.text((px, py + 1), str(num), font=F_NUM,
               fill=(255, 255, 255), anchor="mm")
    return min_dist


def draw_grid(d):
    gx = [MARGIN, MARGIN + 331, MARGIN + 662]
    gy0, rh, cell_h, cell_w = 638, 46, 40, 321
    for idx, (num, icon, head, det) in enumerate(STORIES):
        cx = gx[idx % 3]
        cy = gy0 + (idx // 3) * rh
        d.rectangle([cx, cy, cx + cell_w, cy + cell_h], fill=PANEL,
                    outline=CELL_LINE, width=1)
        ICONS[icon](d, cx + 8, cy + 5, ICON_COLORS[icon])
        tx = cx + 46
        num_s = f"{num}."
        nw = d.textlength(num_s, font=F_BODY_B)
        d.text((tx, cy + 3), num_s, font=F_BODY_B, fill=RED)
        FIT.append((f"story {num} headline",
                    nw + 4 + d.textlength(head, font=F_BODY_B), 272))
        d.text((tx + nw + 4, cy + 3), head, font=F_BODY_B, fill=INK)
        FIT.append((f"story {num} detail",
                    d.textlength(det, font=F_BODY), 272))
        d.text((tx, cy + 22), det, font=F_BODY, fill=DARKGREY)


def draw_strip_footer(d):
    d.rectangle([MARGIN, 1106, W - MARGIN, 1154], fill=INK)
    for t, fnt, y in ((STRIP_1, F_STRIP_B, 1113),
                      (STRIP_2, F_STRIP, 1135)):
        FIT.append((f"strip y{y}", d.textlength(t, font=fnt), CW - 16))
        d.text((W / 2, y), t, font=fnt, fill=PAPER_TXT, anchor="ma")
    FIT.append(("footer", d.textlength(FOOTER, font=F_FOOT), CW))
    d.text((W / 2, 1166), FOOTER, font=F_FOOT, fill=GREY, anchor="ma")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_lead(d)
    min_dist = draw_map(d)
    draw_grid(d)
    draw_strip_footer(d)
    bad = [(lab, round(w, 1), m) for (lab, w, m) in FIT if w > m]
    worst = min(m - w for (_, w, m) in FIT)
    print(f"fit checks: {len(FIT)} strings, min font {MIN_FONT}px, "
          f"worst slack {worst:.1f}px, overflows: {bad}")
    assert not bad, f"text overflow: {bad}"
    print(f"markers: {len(MARKERS)}, min pairwise distance "
          f"{min_dist:.1f}px (required >= 24)")
    assert min_dist >= 24.0, "map markers overlap"
    print(f"stories: 1 lead + {len(STORIES)} grid = "
          f"{1 + len(STORIES)} total")
    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    import hashlib
    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()
    print(f"entry.png: {size} bytes, sha256 {digest}")
    assert size <= 1048576, "entry.png over the 1 MiB hard limit"


if __name__ == "__main__":
    main()
