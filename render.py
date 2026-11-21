#!/usr/bin/env python3
"""Render the v2 front page for Friday 20 November 2026.

Draws a 1024x1024 broadsheet front page with PIL: masthead, date,
one giant lead story (the Wall Street rout that closed the day),
a numbered equirectangular world map, a 24-story grid and a
markets strip. All text is rendered programmatically; every figure
was verified against Reuters / AP / BBC / UN News / Formula 1 /
ESA reporting on 20 November 2026. Deterministic output.
"""

import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28

PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (176, 30, 36)
DARK_RED = (140, 20, 26)
BLUE = (31, 78, 121)
RULE = (26, 26, 26)
LIGHT_LINE = (120, 110, 90)
LAND = (216, 205, 180)
LAND_EDGE = (90, 80, 60)
CHIP_BG = (255, 255, 255)

REGION_COLORS = {
    "North America": (37, 99, 235),
    "Europe": (180, 83, 9),
    "Asia": (219, 39, 119),
    "Africa": (220, 38, 38),
    "Middle East": (124, 58, 237),
    "Oceania": (8, 145, 178),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    try:
        return ImageFont.truetype(FONT_DIR + name, size)
    except OSError:
        return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731


# ---------------------------------------------------------------- stories
# (number, region, headline, detail, lon, lat, dx, dy)
STORIES = [
    (1, "Europe", "Kyiv bridges hit by ballistic missiles",
     "Three Dnipro bridges hit; mayor: 3 killed, 15 injured.",
     30.5, 50.4, 0, -6),
    (2, "Europe", "COP31 runs past deadline in Antalya",
     "Draft drops fossil fuels, $120bn finance goal.",
     30.7, 36.9, 4, 12),
    (3, "Europe", "World Court: Myanmar committed genocide",
     "ICJ rules 9-6; about 10,000 Rohingya killed in 2017.",
     4.3, 52.1, -16, -12),
    (4, "Asia", "Trump, Xi and Putin issue peace declaration",
     "First three-way summit ends with no arms-control deal.",
     114.1, 22.5, 0, 0),
    (5, "Asia", "Cyclone Akvan strikes India's east coast",
     "Lands at Gopalpur at 70-80 km/h, gusting to 90.",
     84.9, 19.3, 0, 6),
    (6, "North America", "Nvidia crashes 14% on SEC probe report",
     "Worst day in two years; 47.5% below October peak.",
     -122.0, 37.4, -10, -8),
    (7, "North America", "Anthropic slides 8.5% after record IPO",
     "Closes at $88.91, close to its $83 offer price.",
     -122.4, 37.8, 8, 10),
    (8, "North America", "Norris takes pole in wet Las Vegas qualifying",
     "McLaren star beats Verstappen by 0.323s; Hamilton last.",
     -115.1, 36.2, 10, -6),
    (9, "Europe", "BepiColombo set for Mercury orbit insertion",
     "Fires thrusters Sat 19:24 CET after an 8-year voyage.",
     8.6, 49.9, 8, 14),
    (10, "Middle East", "Houthi strike damages Riyadh's tallest tower",
     "PIF Tower hit on 19 Nov; no injuries reported.",
     46.7, 24.7, 0, 0),
    (11, "North America", "US Senate rejects Iran war powers bid 51-48",
     "Republicans block bid to curb Trump's Iran war powers.",
     -77.0, 38.9, -14, 2),
    (12, "Asia", "Prabowo and Xi talk economy, South China Sea",
     "Leaders discuss partnership and sea cooperation.",
     106.8, -6.2, 0, 0),
    (13, "Asia", "Taiwan flags 2,700 China-linked accounts",
     "Taipei warns Meta before 28 Nov local elections.",
     121.6, 25.0, 0, 0),
    (14, "Europe", "Russia rejects NATO-style guarantees for Kyiv",
     "Deputy minister Ryabkov pushes back on pledges.",
     37.6, 55.8, 12, -6),
    (15, "Europe", "Europe ready for talks with Russia, allies say",
     "Berlin allies back talks to end the Ukraine war.",
     13.4, 52.5, 14, -12),
    (16, "Europe", "UK-EU summit nears youth mobility deal",
     "PM Burnham in Brussels for trade and carbon-link talks.",
     4.4, 50.9, -14, 12),
    (17, "Middle East", "Iraqi forces to deploy in militia stronghold",
     "Jurf al-Sakhar deal struck with Kataib Hezbollah.",
     44.4, 32.5, 8, 8),
    (18, "Africa", "Dozens missing as migrant boat capsizes",
     "Boat sinks off Yenne; 8,200 reached Canaries in 12 days.",
     -17.4, 14.7, 0, 0),
    (19, "Africa", "Nigeria moves to end jail for suicide bids",
     "Tinubu backs reform after years of psychiatrists' calls.",
     7.5, 9.1, 0, 0),
    (20, "Africa", "Nearly 600 women killed in South Africa",
     "Nearly 600 killed within three months, figures show.",
     28.2, -25.7, 0, 0),
    (21, "Africa", "Kenya discharges its last Ebola patient",
     "Outbreak ends 37 days after the first case.",
     36.8, -1.3, 0, 0),
    (22, "North America", "Bukele launches bid for a third term",
     "El Salvador president campaigns on gang crackdowns.",
     -89.2, 13.7, 0, 0),
    (23, "Oceania", "Sydney man charged over car bomb research",
     "Police allege Islamic State material downloaded.",
     151.2, -33.9, 0, 0),
    (24, "North America", "GTA VI: 24.6m copies on launch day, estimate",
     "Sensor Tower estimate; no official Take-Two figure.",
     -80.2, 25.8, 10, 10),
]

# Simplified continent outlines (lon, lat), equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-165, 60), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
     (-130, 54), (-125, 49), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
     (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-83, 9), (-79, 9),
     (-83, 15), (-87, 21), (-90, 21), (-91, 19), (-97, 26), (-93, 30),
     (-89, 30), (-84, 30), (-81, 25), (-80, 32), (-76, 35), (-74, 40),
     (-70, 42), (-68, 45), (-65, 44), (-60, 47), (-55, 52), (-60, 55),
     (-65, 60), (-68, 58), (-72, 62), (-78, 62), (-85, 66), (-92, 66),
     (-95, 69), (-110, 68), (-125, 70), (-140, 70), (-155, 71), (-165, 68)],
    # Greenland
    [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68), (-22, 70),
     (-20, 74), (-25, 78), (-35, 80), (-50, 80), (-58, 76), (-60, 70)],
    # South America
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50), (-68, -55),
     (-65, -55), (-68, -50), (-65, -45), (-62, -40), (-58, -35), (-52, -32),
     (-48, -28), (-41, -23), (-39, -17), (-35, -9), (-35, -6), (-40, -3),
     (-44, -2), (-50, 0), (-53, 4), (-58, 6), (-62, 9), (-68, 11),
     (-72, 12), (-77, 8)],
    # Africa
    [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (25, 32), (32, 31), (34, 28),
     (35, 24), (37, 20), (39, 18), (43, 12), (48, 11), (51, 10),
     (46, 5), (41, 0), (40, -5), (40, -10), (36, -18), (35, -23),
     (32, -28), (28, -33), (20, -35), (17, -32), (15, -27), (13, -20),
     (12, -15), (13, -10), (9, -1), (9, 4), (4, 6), (-3, 5), (-8, 5),
     (-13, 8), (-17, 12)],
    # Eurasia
    [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
     (-2, 49), (0, 51), (3, 53), (8, 55), (8, 57), (10, 59),
     (5, 60), (5, 62), (12, 65), (18, 69), (25, 71), (30, 70),
     (35, 68), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
     (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
     (150, 70), (160, 70), (170, 67), (178, 65), (178, 62), (170, 60),
     (162, 58), (158, 52), (156, 51), (150, 59), (142, 55), (142, 50),
     (140, 45), (135, 43), (130, 42), (127, 40), (126, 38), (122, 38),
     (120, 35), (122, 30), (120, 25), (115, 22), (110, 20), (108, 15),
     (105, 10), (103, 8), (100, 7), (98, 10), (95, 15), (92, 20),
     (90, 22), (88, 22), (86, 20), (82, 17), (80, 15), (77, 8),
     (75, 12), (72, 20), (68, 23), (66, 25), (62, 25), (58, 26),
     (56, 27), (52, 28), (50, 29), (48, 30), (44, 29), (40, 28),
     (38, 24), (35, 28), (34, 31), (33, 36), (30, 36), (27, 37),
     (26, 40), (23, 36), (22, 37), (19, 40), (16, 38), (15, 40),
     (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
     (137, -12), (135, -12), (132, -12), (130, -13), (126, -14), (122, -17),
     (118, -20)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8), (146, -8),
     (141, -8), (136, -6), (131, -4)],
    # Borneo
    [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -4),
     (110, -3), (109, 0)],
    # Sumatra
    [(95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5),
     (100, -1), (97, 2)],
    # Java
    [(105, -6), (110, -7), (114, -7), (114, -9), (108, -8), (105, -7)],
    # Japan
    [(130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (140, 39),
     (141, 41), (142, 43), (144, 44), (142, 42), (140, 39), (138, 36),
     (135, 34), (132, 33), (130, 32)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
     (1, 51), (-2, 50)],
    # New Zealand
    [(167, -45), (170, -43), (173, -41), (175, -38), (177, -38),
     (175, -40), (172, -42), (168, -46)],
    # Madagascar
    [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (44, -25),
     (43, -21), (44, -17)],
]


def project(lon, lat, mx, my, mw, mh):
    """Equirectangular: lon -180..180, lat 75..-58."""
    x = mx + (lon + 180.0) / 360.0 * mw
    y = my + (75.0 - lat) / 133.0 * mh
    return x, y


def star_points(cx, cy, r_out, r_in, n=5):
    import math

    pts = []
    for i in range(2 * n):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_map(d, mx, my, mw, mh):
    d.rectangle([mx, my, mx + mw, my + mh], fill=(233, 228, 214),
                outline=INK, width=1)
    # graticule
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 75, mx, my, mw, mh)
        d.line([(x, my), (x, my + mh)], fill=(200, 192, 172), width=1)
    for lat in (60, 30, 0, -30):
        _, y = project(0, lat, mx, my, mw, mh)
        d.line([(mx, y), (mx + mw, y)], fill=(200, 192, 172), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # lead star: New York, the market story
    sx, sy = project(-74.0, 40.7, mx, my, mw, mh)
    sx += 6
    sy -= 6
    d.polygon(star_points(sx, sy, 13, 5.5), fill=(212, 175, 55),
              outline=INK)
    d.text((sx + 15, sy - 7), "LEAD", font=SANS_B(11), fill=DARK_RED)
    for n, region, _h, _dt, lon, lat, dx, dy in STORIES:
        x, y = project(lon, lat, mx, my, mw, mh)
        x += dx
        y += dy
        color = REGION_COLORS[region]
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=color,
                  outline=(255, 255, 255), width=1)
        label = str(n)
        tw = d.textlength(label, font=SANS_B(12))
        d.text((x - tw / 2, y - 6), label, font=SANS_B(12),
               fill=(255, 255, 255))


def draw_chart(d, x0, y0, w, h):
    """Plunging Nasdaq line chart, vector-drawn."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=CHIP_BG, outline=INK, width=2)
    d.text((x0 + 12, y0 + 8), "NASDAQ COMPOSITE — FRIDAY",
           font=SANS_B(13), fill=INK)
    d.text((x0 + 12, y0 + 26),
           "22,617.73  -5.28% — worst week since Mar 2020",
           font=SANS(13), fill=DARK_RED)
    px0, py0, px1, py1 = x0 + 16, y0 + 52, x0 + w - 16, y0 + h - 26
    # gridlines
    for i in range(4):
        gy = py0 + (py1 - py0) * i / 3
        d.line([(px0, gy), (px1, gy)], fill=(220, 220, 220), width=1)
    # falling line: week-long slide, Friday cliff
    pts = [(px0, py0 + 6), (px0 + 55, py0 + 16), (px0 + 110, py0 + 12),
           (px0 + 165, py0 + 30), (px0 + 215, py0 + 44), (px0 + 255, py0 + 52),
           (px1 - 8, py1 - 4)]
    d.polygon(pts + [(px1 - 8, py1), (px0, py1)], fill=(232, 180, 180))
    d.line(pts, fill=DARK_RED, width=4, joint="curve")
    d.ellipse([pts[-1][0] - 5, pts[-1][1] - 5, pts[-1][0] + 5, pts[-1][1] + 5],
              fill=DARK_RED, outline=(255, 255, 255), width=1)
    d.text((px0, py1 + 6), "MON 16 NOV", font=SANS(11), fill=(90, 90, 90))
    tw = d.textlength("FRI 20 NOV", font=SANS_B(11))
    d.text((px1 - tw, py1 + 6), "FRI 20 NOV", font=SANS_B(11), fill=DARK_RED)


def check_fits(d, stories, col_w):
    """Warn (and fail loudly in the log) if any line overflows."""
    bad = []
    for n, _r, head, detail, *_ in stories:
        if d.textlength(head, font=SERIF_B(16)) > col_w:
            bad.append((n, "headline", head))
        if d.textlength(detail, font=SANS(15)) > col_w:
            bad.append((n, "detail", detail))
    return bad


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    rng = random.Random(20261120)

    # subtle paper grain (deterministic)
    grain = Image.new("RGB", (W, H), PAPER)
    gd = ImageDraw.Draw(grain)
    for _ in range(60000):
        x = rng.randrange(W)
        y = rng.randrange(H)
        v = rng.choice([(238, 233, 220), (252, 248, 238)])
        gd.point((x, y), fill=v)
    img = Image.blend(img, grain, 0.6)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    d.line([(MARGIN, 10), (W - MARGIN, 10)], fill=INK, width=3)
    title = "THE WORLD IN ONE DAY"
    tf = SERIF_B(56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 16), title, font=tf, fill=INK)
    d.line([(MARGIN, 84), (W - MARGIN, 84)], fill=INK, width=2)
    date = "FRIDAY  20  NOVEMBER  2026"
    df = SANS_B(32)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 92), date, font=df, fill=RED)
    sub = "25 STORIES  ·  6 REGIONS  ·  ONE DAY OF WORLD NEWS"
    sf = SANS(15)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 130), sub, font=sf, fill=INK)
    d.line([(MARGIN, 152), (W - MARGIN, 152)], fill=INK, width=2)

    # ---- lead story ----------------------------------------------------
    lx, ly = MARGIN, 164
    lw, lh = 600, 168
    d.rectangle([lx, ly, lx + lw, ly + lh], outline=INK, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 30], fill=INK)
    d.text((lx + 12, ly + 6), "MARKETS IN TURMOIL — THE LEAD STORY",
           font=SANS_B(16), fill=(255, 255, 255))
    d.text((lx + 12, ly + 40), "Wall Street rout wipes out",
           font=SERIF_B(34), fill=INK)
    d.text((lx + 12, ly + 78), "Nasdaq's gains for 2026",
           font=SERIF_B(34), fill=INK)
    d.text((lx + 12, ly + 118),
           "S&P 500 falls 3.7% to 6,910, its 7th straight loss, into correction;",
           font=SANS(15), fill=INK)
    d.text((lx + 12, ly + 138),
           "the Dow drops 949 points and the VIX fear gauge spikes to 40.",
           font=SANS(15), fill=INK)
    draw_chart(d, lx + lw + 16, ly, W - MARGIN - (lx + lw + 16), lh)

    # ---- map -----------------------------------------------------------
    map_y = 346
    map_h = 160
    d.text((MARGIN, map_y - 2), "THE WORLD TODAY — EVERY STORY NUMBERED",
           font=SANS_B(16), fill=INK)
    legend = "6 North America  ·  7 Europe  ·  4 Asia  ·  4 Africa  ·  2 Middle East  ·  1 Oceania"
    lw_ = d.textlength(legend, font=SANS(13))
    d.text((W - MARGIN - lw_, map_y), legend, font=SANS(13), fill=(70, 70, 70))
    draw_map(d, MARGIN, map_y + 22, W - 2 * MARGIN, map_h - 22)
    # region colour chips under the map
    chip_y = map_y + map_h + 6
    cx = MARGIN
    for region, color in REGION_COLORS.items():
        d.rectangle([cx, chip_y, cx + 12, chip_y + 12], fill=color,
                    outline=INK, width=1)
        d.text((cx + 16, chip_y - 1), region, font=SANS(13), fill=INK)
        cx += 16 + d.textlength(region, font=SANS(13)) + 18
    d.text((W - MARGIN - d.textlength("★ = lead story: New York markets",
                                     font=SANS(13)), chip_y - 1),
           "★ = lead story: New York markets", font=SANS(13), fill=INK)

    # ---- grid ----------------------------------------------------------
    grid_y = 540
    d.text((MARGIN, grid_y), "THE DAY IN FULL", font=SANS_B(16), fill=INK)
    d.line([(MARGIN, grid_y + 24), (W - MARGIN, grid_y + 24)], fill=INK, width=2)
    col_w = (W - 2 * MARGIN - 28) // 2
    text_w = col_w - 34
    bad = check_fits(d, STORIES, text_w)
    for b in bad:
        print("OVERFLOW:", b)
    row_h = 32
    top = grid_y + 34
    for i, (n, region, head, detail, *_rest) in enumerate(STORIES):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 28)
        y = top + row * row_h
        color = REGION_COLORS[region]
        d.ellipse([x, y + 1, x + 17, y + 18], fill=color, outline=INK, width=1)
        label = str(n)
        lw2 = d.textlength(label, font=SANS_B(11))
        d.text((x + (17 - lw2) / 2, y + 3), label, font=SANS_B(11),
               fill=(255, 255, 255))
        d.text((x + 24, y), head, font=SERIF_B(16), fill=INK)
        d.text((x + 24, y + 18), detail, font=SANS(15), fill=(60, 60, 60))

    # ---- markets strip -------------------------------------------------
    strip_y = 968
    d.line([(MARGIN, strip_y), (W - MARGIN, strip_y)], fill=INK, width=2)
    strip = ("MARKETS AT THE CLOSE — S&P 500 6,910.39 −3.70% · "
             "Nasdaq 22,617.73 −5.28% · Dow 48,147.33 −1.93% · "
             "Gold $3,517 −3.02%")
    sf2 = SANS_B(15)
    sw2 = d.textlength(strip, font=sf2)
    if sw2 > W - 2 * MARGIN:
        sf2 = SANS_B(14)
        sw2 = d.textlength(strip, font=sf2)
    if sw2 > W - 2 * MARGIN:
        sf2 = SANS_B(13)
        sw2 = d.textlength(strip, font=sf2)
    if sw2 > W - 2 * MARGIN:
        print("OVERFLOW: markets strip still too wide:", sw2)
    d.text(((W - sw2) / 2, strip_y + 8), strip, font=sf2, fill=DARK_RED)
    d.line([(MARGIN, strip_y + 32), (W - MARGIN, strip_y + 32)], fill=INK, width=1)
    foot = "Sources: Reuters, AP, BBC, UN News, Formula 1, ESA — all figures as reported on 20 November 2026."
    ff = SANS(14)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, strip_y + 38), foot, font=ff, fill=(70, 70, 70))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
