"""Render 'The World in One Day' front page for Friday 20 November 2026.

Draws a 1024 x 1024 newspaper-style PNG at entry.png using only PIL.
All text is rendered programmatically with DejaVu fonts.
Stories are verified reports from Reuters, BBC, AP, UN News and
Formula 1, gathered on 20 November 2026 up to about 19:00 Jakarta.
"""
import math
import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

INK = (18, 18, 20)
PAPER = (246, 242, 232)
RED = (178, 24, 32)
BLUE = (24, 62, 120)
TEAL = (18, 110, 110)
GOLD = (176, 128, 24)
GREY = (92, 92, 92)
LIGHT = (226, 220, 204)
OCEAN = (168, 198, 214)
LAND = (216, 204, 164)
LAND_EDGE = (120, 108, 74)

FDIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FDIR + name, size)


def serif(size):
    return font("DejaVuSerif-Bold.ttf", size)


def bold(size):
    return font("DejaVuSans-Bold.ttf", size)


def reg(size):
    return font("DejaVuSans.ttf", size)


# Each story: (number, headline, detail, lon, lat, region colour key)
STORIES = [
    (1, "KYIV BRIDGES HIT BY BALLISTIC MISSILES",
     "Russian missiles hit three Dnipro bridges. Mayor Klitschko: "
     "3 killed, 15 injured, bridges closed.", 30.5, 50.4, "EUR"),
    (2, "TRUMP, XI AND PUTIN ISSUE PEACE DECLARATION",
     "First three-way summit in Shenzhen ends with a joint peace "
     "declaration, no arms-control deal.", 114.1, 22.5, "ASI"),
    (3, "COP31 FINAL DAY: DEADLOCK IN ANTALYA",
     "21 issues unresolved on finance, adaptation and just "
     "transition as the scheduled close arrives.", 30.7, 36.9, "EUR"),
    (4, "CYCLONE AKVAN MAKES LANDFALL AT GOPALPUR",
     "Third cyclone in a month crosses the Odisha coast at "
     "70-80 km/h, gusting 90. No major damage yet.", 84.9, 19.3, "ASI"),
    (5, "WORLD COURT: MYANMAR COMMITTED GENOCIDE",
     "ICJ rules 9-6 that Myanmar committed genocide against the "
     "Rohingya in 2017. About 10,000 killed.", 4.3, 52.1, "EUR"),
    (6, "MYANMAR CALLS GENOCIDE RULING UNFAIR",
     "A government spokesperson in Naypyidaw says the ICJ ruling "
     "was not unanimous and was unjust.", 96.2, 21.9, "ASI"),
    (7, "ANTHROPIC IPO: BIGGEST DEBUT IN HISTORY",
     "Priced at $83, shares closed at $97.17, up 17 percent, for "
     "a valuation near $1.5 trillion.", -74.0, 40.7, "AME"),
    (8, "ANTHROPIC SLIPS IN POST-DEBUT REALITY CHECK",
     "Shares eased to $91.24 on Friday as investors questioned "
     "lofty AI valuations and spending.", -122.4, 37.8, "AME"),
    (9, "ASIAN SHARES FACE WORST WEEK SINCE 2020",
     "MSCI Asia-Pacific fell 2.5 percent. Nikkei tumbled 4.1 "
     "percent and Kospi fell 4.7 percent.", 139.7, 35.7, "ASI"),
    (10, "US STOCKS SLUMP ABOUT 2 PERCENT AGAIN",
     "The S and P 500 fell for a fifth straight session and hit "
     "fresh seven-month lows on Thursday.", -87.6, 41.8, "AME"),
    (11, "OIL EDGES UP ON RIYADH AND HORMUZ FEARS",
     "Brent rose 0.3 percent to $92.22 as Houthi attacks and "
     "tanker disruption reports raised concern.", 51.5, 35.7, "MEA"),
    (12, "GOLD SLIDES TOWARD A HEAVY WEEKLY LOSS",
     "Gold dipped 0.6 percent to $3,601 an ounce, heading for a "
     "7.3 percent weekly loss as dollar rose.", -0.1, 51.5, "EUR"),
    (13, "DOLLAR RALLY REACHES STRONGEST SINCE 2025",
     "The dollar index held at 103.86, its strongest level since "
     "April 2025, on safe-haven flows.", -77.0, 38.9, "AME"),
    (14, "HOUTHI STRIKE DAMAGES RIYADH PIF TOWER",
     "Riyadh's tallest skyscraper, home to the Saudi wealth fund, "
     "was struck. No injuries were reported.", 46.7, 24.6, "MEA"),
    (15, "HOUTHIS SAY THEY TARGETED RIYADH AIRPORT",
     "The group said it aimed cruise missiles at King Khalid "
     "Airport and the capital's financial centre.", 44.0, 15.5, "MEA"),
    (16, "SENATE REJECTS IRAN WAR POWERS MOVE 51-48",
     "Senate Republicans blocked a resolution to end the Iran war "
     "or require Congress approval for it.", -95.0, 39.0, "AME"),
    (17, "TRUMP: AIDE RAISED DETAINED AMERICANS",
     "Trump says an aide raised two wrongfully detained Americans, "
     "Chen and Zin, with Chinese officials.", 116.4, 39.9, "ASI"),
    (18, "PRABOWO AND XI DISCUSS SOUTH CHINA SEA",
     "Indonesia and China discussed economic partnership and "
     "future South China Sea cooperation.", 106.8, -6.2, "ASI"),
    (19, "TAIWAN FLAGS 2,700 CHINA-LINKED ACCOUNTS",
     "Taipei told Meta the accounts seek to influence the island's "
     "28 November local elections.", 121.0, 23.7, "ASI"),
    (20, "RUSSIA REJECTS NATO-STYLE GUARANTEES",
     "Deputy minister Ryabkov pushed back on NATO-style security "
     "guarantees proposed for Ukraine.", 37.6, 55.8, "EUR"),
    (21, "EUROPE READY TO TALK TO RUSSIA, LEADERS SAY",
     "Ukraine's allies meeting in Berlin said Europe is ready for "
     "talks with Russia on ending the war.", 13.4, 52.5, "EUR"),
    (22, "EUROPEAN TROOPS DRILL IN POLAND",
     "Thousands of troops from 11 countries exercised at Nowa Deba "
     "for a possible postwar Ukraine mission.", 21.8, 50.4, "EUR"),
    (23, "UK-EU SUMMIT: YOUTH MOBILITY DEAL NEARS",
     "Burnham in Brussels for deals on youth mobility, food trade "
     "and linked carbon emissions schemes.", 4.4, 50.8, "EUR"),
    (24, "UK FACES COLDEST AUTUMN NIGHT, MINUS 10C",
     "Friday night is forecast to be the coldest of the autumn so "
     "far, with minus 10C possible in places.", -3.7, 55.4, "EUR"),
    (25, "IRAQ FORCES TO DEPLOY IN MILITIA STRONGHOLD",
     "Security forces will deploy in Jurf al-Sakhar under a deal "
     "to ease tension with Kataib Hezbollah.", 44.4, 33.3, "MEA"),
    (26, "DOZENS MISSING AS BOAT CAPSIZES OFF SENEGAL",
     "A migrant boat bound for Europe capsized off Yenne. About "
     "8,200 reached the Canaries in 12 days.", -17.4, 14.7, "AFR"),
    (27, "NIGERIA MOVES TO END JAIL FOR SUICIDE BID",
     "President Tinubu backs reform to end jail terms for attempted "
     "suicide after years of medical calls.", 7.5, 9.1, "AFR"),
    (28, "NEARLY 600 WOMEN KILLED IN SOUTH AFRICA",
     "BBC reports nearly 600 women were killed in South Africa "
     "within a three-month period.", 24.7, -29.0, "AFR"),
    (29, "KENYA DISCHARGES ITS LAST EBOLA PATIENT",
     "Kenya discharged its last Ebola patient 37 days after the "
     "country's first case was confirmed.", 36.8, -1.3, "AFR"),
    (30, "BUKELE LAUNCHES BID FOR A THIRD TERM",
     "El Salvador's president launched his candidacy for a third "
     "term while campaigning on gang crackdowns.", -89.2, 13.7, "AME"),
    (31, "SYDNEY MAN CHARGED OVER CAR BOMB PLOT",
     "Australian police arrested a man accused of researching a "
     "car bomb and holding Islamic State material.", 151.2, -33.9, "OCE"),
    (32, "DAYCARE PRINCIPAL JAILED IN INDONESIA",
     "An Indonesian daycare principal was jailed for five years "
     "over a child abuse case, BBC reports.", 112.7, -7.2, "ASI"),
    (33, "CHINA ISSUES MOUNT FUJI CLIMB WARNING",
     "A $75,000 reward by a missing climber's family sparked fears "
     "of reckless attempts on Mount Fuji.", 138.7, 35.4, "ASI"),
    (34, "BEPICOLOMBO NEARS MERCURY AFTER 8 YEARS",
     "The ESA-JAXA probe is due to enter Mercury orbit on 21 "
     "November after an eight-year journey.", 8.7, 50.1, "EUR"),
    (35, "GTA VI SMASHES LAUNCH-DAY SALES RECORDS",
     "Sensor Tower estimates 24.6 million copies and $2.36 billion "
     "on launch day. Not yet official.", -80.2, 25.8, "AME"),
    (36, "RUSSELL FASTEST IN WET LAS VEGAS PRACTICE",
     "George Russell topped FP2 in 1:47.272, just 0.071 seconds "
     "ahead of Gasly, with Leclerc third.", -115.2, 36.1, "AME"),
    (37, "ISRAELI ARMY ENDS GAZA GROUND OPERATION",
     "The Israeli military said it completed a ground operation in "
     "Gaza beyond the Yellow Line, BBC reports.", 34.3, 31.5, "MEA"),
    (38, "VENEZUELA SIGNS MILITARY DEAL WITH US",
     "Venezuela signed a military deal with the United States less "
     "than a year after Maduro's removal.", -66.9, 10.5, "AME"),
]

SHORT = {
    2: "Shenzhen summit joint declaration.",
    3: "21 issues unresolved at close.",
    4: "70-80 km/h at Gopalpur, no damage.",
    5: "ICJ 9-6: genocide vs Rohingya, 2017.",
    6: "Naypyidaw calls the ruling unjust.",
    7: "Closed $97.17, +17%, near $1.5tn.",
    8: "Shares eased to $91.24 on Friday.",
    9: "MSCI -2.5%, Nikkei -4.1%, Kospi -4.7%.",
    10: "S and P 500: fifth straight loss.",
    11: "Brent rose to $92.22 a barrel.",
    12: "Gold $3,601/oz, set for -7.3% week.",
    13: "Dollar index held at 103.86.",
    14: "Riyadh PIF Tower hit, no injuries.",
    15: "Claims airport, finance centre aim.",
    16: "War powers move blocked 51-48.",
    17: "Chen and Zin cases raised in China.",
    18: "Economy, sea cooperation discussed.",
    19: "Influence bid before 28 Nov vote.",
    20: "Ryabkov rejects guarantee proposal.",
    21: "Berlin allies signal talks readiness.",
    22: "11 nations drill at Nowa Deba.",
    23: "Burnham in Brussels, reset deals.",
    24: "Minus 10C forecast Friday night.",
    25: "Jurf al-Sakhar deal eases tension.",
    26: "Migrant boat capsizes off Yenne.",
    27: "Tinubu backs reform, medics' call.",
    28: "Nearly 600 killed in three months.",
    29: "Last patient out, day 37 of outbreak.",
    30: "Third-term bid on gang crackdown.",
    31: "Car bomb research, IS material claim.",
    32: "Five years jail, child abuse case.",
    33: "$75,000 reward sparks climb fears.",
    34: "Mercury orbit insertion due 21 Nov.",
    35: "Est. 24.6m copies, $2.36bn day one.",
    36: "1:47.272, Gasly +0.071, Leclerc 3rd.",
    37: "Operation beyond Yellow Line ends.",
    38: "Signed a year after Maduro's exit.",
}

# Short grid headlines, each sized to fit one bold line of a column.
HEAD = {
    2: "TRUMP, XI, PUTIN: PEACE DEAL",
    3: "COP31 DEADLOCK IN ANTALYA",
    4: "CYCLONE AKVAN HITS GOPALPUR",
    5: "WORLD COURT: MYANMAR GENOCIDE",
    6: "MYANMAR: RULING IS UNFAIR",
    7: "ANTHROPIC IPO BIGGEST EVER",
    8: "ANTHROPIC SLIPS AFTER DEBUT",
    9: "ASIA STOCKS: WORST WEEK 2020",
    10: "US STOCKS SLUMP 2 PERCENT",
    11: "OIL UP ON RIYADH FEARS",
    12: "GOLD SLIDES, WEAK WEEK",
    13: "DOLLAR AT 2025 HIGH",
    14: "HOUTHI HIT ON PIF TOWER",
    15: "HOUTHIS AIM AT AIRPORT",
    16: "SENATE BLOCKS IRAN MOVE",
    17: "TRUMP: DETAINED DUO RAISED",
    18: "PRABOWO, XI TALK SEA DEAL",
    19: "TAIWAN FLAGS 2,700 ACCOUNTS",
    20: "RUSSIA REJECTS GUARANTEES",
    21: "EUROPE READY FOR TALKS",
    22: "EUROPE TROOPS DRILL POLAND",
    23: "UK-EU: YOUTH MOBILITY DEAL",
    24: "UK COLDEST NIGHT: -10C",
    25: "IRAQ DEPLOYS IN STRONGHOLD",
    26: "DOZENS MISSING OFF SENEGAL",
    27: "NIGERIA ENDS SUICIDE JAIL",
    28: "600 WOMEN KILLED, S. AFRICA",
    29: "KENYA: LAST EBOLA CASE OUT",
    30: "BUKELE SEEKS THIRD TERM",
    31: "SYDNEY BOMB PLOT CHARGE",
    32: "DAYCARE CHIEF JAILED, JAVA",
    33: "CHINA WARNS FUJI CLIMBERS",
    34: "BEPICOLOMBO NEARS MERCURY",
    35: "GTA VI SMASHES RECORDS",
    36: "RUSSELL FASTEST, LAS VEGAS",
    37: "ISRAEL ENDS GAZA OPERATION",
    38: "VENEZUELA-US MILITARY DEAL",
}

# Pixel nudges so markers in crowded regions stay separately readable.
NUDGE = {
    1: (20, -14), 3: (-22, 26), 5: (-4, -28), 12: (-26, 26),
    20: (28, -24), 21: (-20, 28), 22: (28, 20), 23: (-30, 16),
    24: (-32, -26), 34: (20, 28), 37: (-26, 18), 25: (24, 26),
    11: (0, -26), 14: (20, 16), 15: (-24, 22), 2: (-10, 8),
    19: (14, 12), 33: (16, -8), 9: (-14, -12), 17: (-6, -14),
    18: (-12, 6), 32: (14, 10), 4: (-12, -6), 6: (-16, 10),
    8: (-14, -8), 36: (12, 12), 35: (20, -20), 7: (12, -10),
    10: (-12, -12), 13: (26, 20), 16: (-8, 12),
}

REGION_COLOURS = {
    "AME": (178, 24, 32),
    "EUR": (24, 62, 120),
    "MEA": (176, 128, 24),
    "AFR": (30, 128, 76),
    "ASI": (128, 42, 140),
    "OCE": (18, 110, 110),
}
REGION_NAMES = {
    "AME": "Americas",
    "EUR": "Europe",
    "MEA": "Middle East",
    "AFR": "Africa",
    "ASI": "Asia-Pacific",
    "OCE": "Oceania",
}

# Simplified continent outlines as (lon, lat) polygon points, drawn in
# equirectangular projection. Shapes are approximate by design: the map
# is a locator, and every marker is placed by true lon/lat.
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69),
     (-85, 66), (-80, 73), (-78, 62), (-85, 60), (-92, 57), (-95, 50),
     (-89, 48), (-84, 46), (-76, 44), (-70, 42), (-74, 39), (-76, 35),
     (-80, 32), (-81, 26), (-84, 30), (-89, 30), (-94, 29), (-97, 26),
     (-97, 22), (-94, 19), (-90, 21), (-87, 21), (-90, 14), (-83, 9),
     (-79, 9), (-83, 15), (-88, 16), (-92, 15), (-97, 16), (-105, 20),
     (-110, 23), (-114, 28), (-117, 33), (-122, 37), (-124, 46),
     (-130, 55), (-145, 60), (-158, 58), (-168, 66)],
    [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-71, -38), (-73, -44), (-74, -50),
     (-69, -54), (-66, -55), (-68, -50), (-65, -45), (-62, -41),
     (-58, -34), (-48, -28), (-41, -23), (-39, -15), (-35, -8),
     (-44, -3), (-50, 0), (-54, 5), (-61, 8), (-68, 11), (-72, 12),
     (-77, 8), (-79, 9)],
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-5, 48), (0, 50),
     (5, 53), (8, 55), (8, 57), (18, 56), (21, 60), (25, 60),
     (30, 62), (30, 70), (45, 68), (60, 69), (45, 66), (32, 60),
     (28, 55), (24, 58), (20, 54), (14, 54), (18, 50), (23, 50),
     (28, 48), (30, 46), (28, 41), (23, 40), (22, 37), (15, 38),
     (12, 44), (8, 44), (3, 43), (3, 39), (-2, 37), (-10, 36)],
    [(-6, 35), (-10, 31), (-16, 24), (-17, 15), (-12, 8), (-8, 5),
     (2, 6), (6, 4), (9, -1), (13, -12), (12, -18), (14, -22),
     (16, -29), (19, -34), (27, -34), (32, -29), (35, -24),
     (36, -20), (40, -15), (40, -10), (42, -2), (48, 5), (51, 11),
     (44, 11), (43, 12), (38, 20), (35, 24), (33, 27), (32, 31),
     (22, 33), (11, 34), (10, 37), (5, 37), (-2, 35), (-6, 35)],
    [(32, 36), (36, 36), (42, 38), (44, 38), (48, 40), (50, 44),
     (54, 46), (60, 50), (70, 52), (85, 55), (100, 55), (115, 52),
     (128, 50), (140, 48), (142, 52), (156, 52), (162, 60), (170, 66),
     (178, 65), (170, 60), (158, 52), (142, 45), (135, 35), (130, 33),
     (122, 30), (120, 25), (110, 20), (108, 15), (106, 9), (103, 5),
     (100, 8), (98, 14), (95, 16), (92, 21), (88, 22), (86, 20),
     (80, 15), (77, 8), (73, 16), (68, 23), (66, 25), (61, 25),
     (57, 26), (52, 28), (50, 29), (48, 30), (44, 29), (42, 32),
     (36, 36), (32, 36)],
    [(95, 5), (100, 0), (105, -3), (110, -4), (115, -2), (120, 0),
     (125, -1), (131, -1), (136, -2), (141, -3), (146, -6), (150, -9),
     (147, -9), (142, -8), (136, -7), (130, -4), (122, -3), (115, -5),
     (108, -6), (100, -3), (95, 2), (95, 5)],
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (147, -39), (150, -37), (153, -30), (153, -25),
     (151, -20), (149, -15), (146, -11), (142, -11), (141, -17),
     (140, -22), (136, -15), (135, -12), (132, -11), (129, -15),
     (126, -14), (122, -17), (118, -20), (113, -22)],
    [(-45, 60), (-42, 65), (-40, 70), (-32, 68), (-22, 70), (-20, 76),
     (-30, 82), (-45, 80), (-55, 76), (-58, 68), (-53, 64), (-45, 60)],
    [(130, 32), (133, 34), (137, 35), (140, 36), (141, 40), (141, 44),
     (140, 44), (138, 38), (135, 34), (131, 32), (130, 32)],
    [(-3, 50), (-5, 53), (-3, 56), (-5, 58), (-8, 55), (-10, 52),
     (-6, 50), (-3, 50)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (90.0 - lat) / 180.0 * (y1 - y0)
    return (x, y)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_map(draw, img, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=OCEAN, outline=INK, width=2)
    # graticule every 30 degrees
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, box)
        draw.line([(gx, y0), (gx, y1)], fill=(190, 212, 226), width=1)
    for lat in range(-60, 91, 30):
        _, gy = project(0, lat, box)
        draw.line([(x0, gy), (x1, gy)], fill=(190, 212, 226), width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # markers, nudged apart when stories share a city
    seen = {}
    for num, _h, _d, lon, lat, region in STORIES:
        key = (round(lon), round(lat))
        n = seen.get(key, 0)
        seen[key] = n + 1
        mx, my = project(lon, lat, box)
        mx += (n % 3 - 1) * 13
        my += (n // 3) * 13 - (4 if n else 0)
        dx, dy = NUDGE.get(num, (0, 0))
        mx += dx
        my += dy
        colour = REGION_COLOURS[region]
        r = 10
        draw.ellipse([mx - r, my - r, mx + r, my + r], fill=colour,
                     outline=(255, 255, 255), width=2)
        label = str(num)
        fnt = bold(11 if num < 10 else 10)
        tw = draw.textlength(label, font=fnt)
        draw.text((mx - tw / 2, my - 7), label, fill=(255, 255, 255),
                  font=fnt)
    draw.text((x0 + 8, y0 + 6), "WHERE IT HAPPENED - NUMBERED MARKERS",
              fill=INK, font=bold(13))


def texture(img):
    """Add a fine printed-paper grain so the page reads rich, not flat."""
    rng = random.Random(20261120)
    px = img.load()
    for _ in range(260000):
        x = rng.randrange(W)
        y = rng.randrange(H)
        r, g, b = px[x, y]
        d = rng.choice((-7, -4, 4, 7))
        px[x, y] = (max(0, min(255, r + d)), max(0, min(255, g + d)),
                    max(0, min(255, b + d)))
    return img


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw.rectangle([0, 0, W, 86], fill=INK)
    title = "THE WORLD IN ONE DAY"
    tf = serif(52)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 10), title, fill=(250, 246, 235), font=tf)
    draw.rectangle([0, 86, W, 90], fill=RED)
    sub = "38 verified stories  -  Reuters  -  BBC  -  AP  -  UN News"
    sf = bold(14)
    sw = draw.textlength(sub, font=sf)
    draw.text(((W - sw) / 2, 96), sub, fill=INK, font=sf)
    date = "FRIDAY  20  NOVEMBER  2026"
    df = serif(34)
    dw = draw.textlength(date, font=df)
    draw.text(((W - dw) / 2, 118), date, fill=RED, font=df)
    draw.line([(14, 162), (W - 14, 162)], fill=INK, width=3)

    # Giant lead story (story 1)
    lead = STORIES[0]
    draw.rectangle([14, 168, W - 14, 292], fill=(252, 248, 238),
                   outline=INK, width=2)
    draw.rectangle([14, 168, 64, 292], fill=RED)
    draw.text((26, 196), "1", fill=(255, 255, 255), font=serif(44))
    draw.text((76, 174), "LEAD STORY - KYIV, UKRAINE", fill=RED,
              font=bold(14))
    lf = serif(27)
    for i, line in enumerate(wrap(draw, lead[1], lf, 920)):
        draw.text((76, 194 + i * 32), line, fill=INK, font=lf)
    bf = reg(15)
    body = ("Russian ballistic missiles struck three bridges over the "
            "Dnipro River - Podilsko-Voskresenskyi, Darnytskyi and "
            "Pivdennyi - in the biggest attack on the capital's river "
            "crossings of the war. Mayor Vitali Klitschko said three "
            "people were killed and 15 injured, and the bridges were "
            "closed or restricted for the city of three million.")
    for i, line in enumerate(wrap(draw, body, bf, 920)):
        draw.text((76, 232 + i * 19), line, fill=INK, font=bf)

    # World map
    draw_map(draw, img, (14, 300, W - 14, 512))

    # Region legend
    lx = 14
    draw.text((lx, 518), "REGIONS:", fill=INK, font=bold(13))
    lx += 78
    for key in ("AME", "EUR", "MEA", "AFR", "ASI", "OCE"):
        draw.rectangle([lx, 519, lx + 14, 533], fill=REGION_COLOURS[key])
        label = REGION_NAMES[key]
        draw.text((lx + 18, 518), label, fill=INK, font=bold(13))
        lx += 22 + int(draw.textlength(label, font=bold(13))) + 16
    draw.line([(14, 540), (W - 14, 540)], fill=INK, width=2)

    # Dense grid of the remaining stories, three columns
    rest = STORIES[1:]
    cols = 3
    col_w = (W - 28 - (cols - 1) * 10) // cols
    rows = math.ceil(len(rest) / cols)
    grid_y = 548
    grid_h = 958 - grid_y
    cell_h = grid_h // rows
    gf = reg(13)
    hf = bold(13)
    for idx, story in enumerate(rest):
        num, head, detail, _lon, _lat, region = story
        cx = 14 + (idx % cols) * (col_w + 10)
        cy = grid_y + (idx // cols) * cell_h
        if idx % cols == 0 and idx > 0:
            pass
        draw.rectangle([cx, cy + 2, cx + 5, cy + cell_h - 4],
                       fill=REGION_COLOURS[region])
        head_line = "%d. %s" % (num, HEAD.get(num, head))
        draw.text((cx + 10, cy + 2), head_line, fill=INK, font=hf)
        draw.text((cx + 10, cy + 18), SHORT.get(num, detail), fill=INK,
                  font=gf)
        if (idx // cols) < rows - 1:
            draw.line([(cx, cy + cell_h - 1), (cx + col_w, cy + cell_h - 1)],
                      fill=LIGHT, width=1)

    # Markets strip
    draw.rectangle([0, 962, W, H], fill=INK)
    draw.text((14, 968), "MARKETS", fill=GOLD, font=bold(16))
    markets = ("Brent $92.22 +0.3%   WTI $83.40   Gold $3,601 -0.6%   "
               "S&P 500 -2% (5th loss)   Nikkei -4.1%   Kospi -4.7%")
    draw.text((14, 990), markets, fill=(250, 246, 235), font=bold(15))
    draw.text((14, 1008 - 0), "", fill=(250, 246, 235), font=reg(13))

    img = texture(img)
    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()

