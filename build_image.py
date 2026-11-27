#!/usr/bin/env python3
"""News image for Friday 27 November 2026.

Draws a 1024x1024 broadsheet-style summary of the day's world news:
a stylised world map with numbered story markers above a 40-story list.
The map outlines are simplified hand-drawn polygons; the stories were
researched and verified from Reuters, AP, AFP, Bloomberg, Xinhua, AAP,
ANSA and Bangkok Post reporting on 26-27 November 2026.

Run:  python3 build_image.py   -> writes entry.png next to this file.
Deterministic: no network, no clock, no randomness.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 239)
INK = (20, 33, 61)
RED = (193, 39, 45)
GOLD = (201, 162, 74)
SEA = (214, 230, 240)
LAND = (235, 224, 198)
LAND_EDGE = (122, 106, 79)
GREY = (98, 106, 120)
BOX = (238, 231, 213)
RULE = (178, 170, 148)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(bold, size):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = os.path.join(FONT_DIR, name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    try:
        return ImageFont.load_default(size)
    except Exception:
        return ImageFont.load_default()


def fit(text, font, max_w, draw):
    """Shorten text with an ellipsis until it fits max_w pixels."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "...", font=font) > max_w:
        text = text[:-1]
    return text + "..."


# (number, headline, latitude, longitude, badge dx, badge dy)
STORIES = [
    (1, "Kuwait drone strike kills 2 Italians", 29.30, 47.50, -10, -10),
    (2, "Houthis claim Ras Tanura refinery hit", 26.60, 50.20, 12, 8),
    (3, "Riyadh tower strike wounds 11", 24.70, 46.70, -12, 10),
    (4, "Gaza truce frays: 1,600+ dead since Oct 2025", 31.50, 34.45, -14, -2),
    (5, "Trump presses Kyiv on 28-point peace plan", 50.45, 30.52, -6, -20),
    (6, "Tehran denies Kuwait role, offers probe", 35.70, 51.40, 12, -12),
    (7, "Houthis claim Jeddah and Jazan port strikes", 15.35, 44.20, 0, 12),
    (8, "Cairo tanker fire kills 31", 30.00, 31.20, 0, 16),
    (9, "De Cos to succeed Lagarde at ECB", 50.11, 8.68, 4, 20),
    (10, "EU 1.6tn budget talks end with no deal", 50.85, 4.35, 0, -20),
    (11, "Ibiza tanker capsizes; 1 dead, 7,000t diesel", 38.98, 1.43, -14, 12),
    (12, "Dutch resist US curbs on ASML China sales", 52.07, 4.30, 20, -14),
    (13, "Germany arrests 2 over synagogue plots", 52.52, 13.40, 20, -12),
    (14, "Serbia calls presidential vote for 27 Dec", 44.80, 20.50, 14, 12),
    (15, "Heathrow third runway faces MPs' challenge", 51.47, -0.47, -22, 10),
    (16, "AFP hit by cyberattack; platform shut", 48.85, 2.35, -8, 18),
    (17, "Bangkok refinery blast injures 9", 13.75, 100.50, -12, -6),
    (18, "US proposes 18% tariffs on Thai goods", 13.75, 100.50, 12, 8),
    (19, "China closes golf courses in crackdown", 39.90, 116.40, 16, -16),
    (20, "South Korea births surge 14.3%, a record", 37.57, 126.98, 14, 10),
    (21, "North Korea expels Swiss diplomat", 39.03, 125.75, -18, 6),
    (22, "Hong Kong ferry crash injures 25", 22.32, 114.17, -14, -10),
    (23, "HK fire reforms: 163 held in bid-rigging", 22.32, 114.17, 16, 10),
    (24, "Taipei mayor holds pre-election rally", 25.03, 121.56, -14, -2),
    (25, "NZ coalition falls one seat short", -41.29, 174.78, 0, 0),
    (26, "Australia sanctions 2 alleged Iran agents", -33.87, 151.21, 0, 0),
    (27, "Hasina return stirs Dhaka-Delhi tension", 23.81, 90.41, 10, 8),
    (28, "India holds drills with Malaysia, Lanka", 28.61, 77.21, 0, 0),
    (29, "Black Friday: $12.9bn online sales forecast", 40.71, -74.00, -16, -4),
    (30, "Thanksgiving storm cuts power to 900,000+", 38.90, -77.04, -16, 12),
    (31, "FCC clears SpaceX 1m orbital data centres", 28.39, -80.61, 6, 10),
    (32, "Boehly-led group to buy Lukoil's assets", 38.90, -77.04, 16, 2),
    (33, "Detroit to become drone-manufacturing hub", 42.33, -83.05, -6, -16),
    (34, "Argentina bans central-bank funding of govt", -34.60, -58.38, 0, 0),
    (35, "Nvidia halts server shipments to 4 nations", 37.35, -121.95, 0, 0),
    (36, "4,200 AI attack frameworks exposed online", 25.03, 121.56, 12, 0),
    (37, "Brent near $96.60, month high; weekly gain", 51.50, -0.12, -18, -12),
    (38, "Nepal mourns citizen killed in Saudi strike", 27.72, 85.32, 0, 0),
    (39, "Thai F-16s scramble to intercept aircraft", 16.87, 99.13, 14, -12),
    (40, "Zelensky warns of major Russian air attack", 50.45, 30.52, 16, 10),
]

TOP3 = [
    ("Kuwait drone strike kills 2 Italians",
     "Kuwait blames Iran; Tehran denies role"),
    ("Trump presses Kyiv on 28-point plan",
     "Deadline passes; Zelensky warns of air attack"),
    ("Black Friday: $12.9bn online forecast",
     "US online spend $82.5bn since 1 Nov, +9.1%"),
]

# Simplified hand-drawn continent outlines, (longitude, latitude).
# Coarse on purpose: a stylised map, not a survey chart.
NORTH_AMERICA = [
    (-168, 66), (-161, 58), (-153, 58), (-147, 60), (-140, 60), (-134, 57),
    (-130, 54), (-127, 50), (-124, 46), (-124, 40), (-121, 35), (-117, 32),
    (-112, 29), (-108, 25), (-105, 21), (-100, 18), (-96, 16), (-93, 15),
    (-90, 14), (-87, 13), (-83, 9), (-80, 8), (-77, 7), (-79, 9), (-82, 10),
    (-85, 11), (-88, 13), (-89, 15), (-91, 16), (-93, 17), (-96, 18),
    (-97, 21), (-97, 24), (-96, 27), (-93, 29), (-89, 30), (-85, 30),
    (-82, 28), (-80, 26), (-81, 30), (-80, 32), (-76, 34), (-75, 38),
    (-73, 41), (-70, 42), (-68, 44), (-66, 45), (-63, 46), (-60, 47),
    (-64, 50), (-60, 52), (-64, 55), (-65, 58), (-68, 58), (-72, 62),
    (-77, 63), (-82, 66), (-87, 66), (-93, 66), (-96, 69), (-105, 68),
    (-115, 69), (-125, 70), (-135, 69), (-145, 70), (-155, 71), (-162, 70),
    (-166, 68),
]
GREENLAND = [
    (-58, 64), (-52, 60), (-44, 60), (-40, 64), (-32, 68), (-22, 70),
    (-20, 74), (-25, 78), (-32, 80), (-45, 81), (-58, 80), (-62, 76),
    (-65, 72), (-60, 68),
]
SOUTH_AMERICA = [
    (-77, 7), (-75, 10), (-72, 12), (-68, 11), (-64, 10), (-60, 8),
    (-55, 6), (-52, 5), (-50, 0), (-48, -3), (-42, -5), (-38, -6),
    (-35, -9), (-38, -13), (-40, -20), (-42, -23), (-48, -27), (-52, -32),
    (-57, -38), (-62, -41), (-65, -45), (-68, -50), (-68, -54), (-71, -54),
    (-73, -50), (-73, -44), (-73, -37), (-71, -30), (-70, -22), (-75, -15),
    (-78, -8), (-81, -4), (-80, 0), (-80, 4),
]
AFRICA = [
    (-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
    (-12, 8), (-8, 5), (-4, 5), (0, 6), (6, 4), (9, 4), (13, 0), (12, -4),
    (13, -10), (12, -17), (15, -22), (18, -29), (20, -35), (26, -34),
    (32, -29), (35, -24), (38, -18), (40, -12), (40, -8), (42, -4),
    (44, 0), (46, 2), (48, 5), (51, 10), (48, 11), (44, 12), (42, 15),
    (40, 18), (38, 20), (37, 22), (35, 28), (33, 31), (30, 32), (25, 32),
    (20, 33), (15, 33), (10, 34), (5, 35), (0, 36),
]
MADAGASCAR = [
    (44, -16), (47, -15), (50, -17), (49, -21), (46, -25), (43, -22),
]
EUROPE = [
    (28, 41), (27, 39), (26, 38), (24, 37), (23, 36), (22, 36), (21, 38),
    (20, 40), (19, 42), (18, 44), (16, 44), (14, 45), (13, 45), (12, 44),
    (10, 44), (8, 44), (6, 43), (4, 43), (3, 42), (2, 41), (0, 39),
    (-1, 38), (-3, 37), (-5, 36), (-7, 37), (-9, 38), (-9, 40), (-9, 42),
    (-8, 44), (-6, 45), (-4, 46), (-2, 47), (-1, 48), (-2, 49), (-1, 50),
    (0, 50), (2, 51), (3, 52), (5, 53), (7, 54), (8, 55), (8, 57),
    (10, 58), (12, 58), (14, 59), (16, 59), (18, 59), (20, 60), (22, 61),
    (24, 62), (26, 63), (28, 64), (30, 65), (32, 66), (34, 67), (36, 68),
    (38, 68), (40, 68), (42, 67), (44, 66), (46, 65), (48, 64), (50, 63),
    (52, 62), (54, 61), (56, 60), (58, 59), (60, 58), (60, 56), (58, 55),
    (56, 54), (54, 53), (52, 52), (50, 51), (48, 50), (46, 49), (44, 48),
    (42, 47), (40, 46), (38, 45), (36, 44), (34, 44), (32, 44), (30, 45),
    (28, 45),
]
ASIA = [
    (28, 41), (30, 44), (32, 46), (35, 48), (38, 50), (41, 52), (44, 54),
    (47, 56), (50, 58), (53, 60), (56, 62), (58, 64), (60, 66), (62, 68),
    (64, 68), (68, 69), (72, 70), (76, 71), (80, 72), (84, 73), (88, 73),
    (92, 74), (96, 75), (100, 75), (104, 76), (108, 76), (112, 75),
    (116, 74), (120, 73), (124, 72), (128, 72), (132, 71), (136, 71),
    (140, 71), (144, 71), (148, 70), (152, 70), (156, 69), (160, 68),
    (164, 67), (168, 67), (172, 66), (176, 65), (178, 65), (178, 62),
    (172, 60), (166, 59), (162, 56), (158, 52), (155, 50), (150, 48),
    (146, 45), (142, 42), (140, 39), (138, 36), (135, 34), (132, 32),
    (129, 31), (127, 34), (126, 38), (124, 40), (122, 39), (120, 36),
    (119, 32), (121, 28), (118, 24), (113, 22), (110, 20), (108, 18),
    (106, 15), (105, 10), (104, 8), (103, 5), (101, 3), (100, 6),
    (98, 10), (97, 14), (94, 17), (92, 20), (90, 22), (88, 22), (86, 20),
    (84, 18), (82, 16), (80, 13), (78, 9), (77, 8), (75, 11), (73, 16),
    (71, 20), (69, 22), (67, 24), (65, 25), (63, 25), (61, 25), (59, 25),
    (57, 26), (56, 27), (54, 26), (52, 27), (50, 28), (49, 29), (50, 26),
    (51, 25), (52, 24), (54, 24), (56, 24), (58, 23), (59, 22), (58, 19),
    (56, 17), (54, 15), (52, 14), (49, 14), (46, 13), (44, 12), (43, 13),
    (42, 15), (41, 17), (40, 19), (39, 21), (38, 24), (37, 26), (36, 28),
    (35, 29), (34, 30), (34, 32), (35, 33), (36, 36), (34, 36), (32, 36),
    (30, 36), (28, 37), (27, 38), (27, 40),
]
AUSTRALIA = [
    (113, -22), (114, -28), (115, -33), (118, -35), (124, -33), (129, -32),
    (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
    (153, -32), (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
    (140, -13), (136, -15), (135, -12), (132, -11), (130, -12), (127, -14),
    (124, -16), (121, -19), (117, -20),
]
NEW_ZEALAND = [
    (167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (174, -41),
    (172, -43), (168, -46),
]
UNITED_KINGDOM = [
    (-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
]
JAPAN = [
    (130, 31), (132, 33), (135, 34), (137, 35), (139, 37), (141, 39),
    (141, 41), (143, 43), (145, 44), (142, 45), (140, 43), (139, 40),
    (137, 37), (135, 34), (133, 34), (131, 33),
]
BORNEO = [
    (109, 0), (112, 1), (116, 2), (118, -1), (117, -4), (114, -4), (111, -3),
]
SUMATRA = [
    (95, 5), (98, 3), (101, 0), (104, -3), (106, -6), (103, -5), (100, -1),
    (97, 2),
]
NEW_GUINEA = [
    (131, -1), (136, -2), (141, -3), (146, -6), (147, -8), (142, -8),
    (138, -7), (134, -4), (131, -2),
]
JAVA = [
    (105, -6), (108, -7), (111, -7), (114, -8), (112, -8), (108, -7),
]
ICELAND = [
    (-22, 64), (-18, 63), (-14, 64), (-16, 66), (-20, 66),
]
CUBA = [
    (-84, 22), (-80, 23), (-76, 21), (-74, 20), (-78, 21), (-82, 22),
]
SRI_LANKA = [
    (80, 9), (81, 7), (80, 6),
]

LAND_POLYS = [
    NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, MADAGASCAR, EUROPE,
    ASIA, AUSTRALIA, NEW_ZEALAND, UNITED_KINGDOM, JAPAN, BORNEO, SUMATRA,
    NEW_GUINEA, JAVA, ICELAND, CUBA, SRI_LANKA,
]

# ---- layout ----
MAP_X0, MAP_Y0, MAP_W, MAP_H = 8, 182, 1008, 374
LAT_TOP, LAT_BOT = 84.0, -58.0
LIST_Y0, LIST_ROW_H = 584, 27
COL_X = [16, 352, 688]
COL_W = 320


def project(lon, lat):
    x = MAP_X0 + (lon + 180.0) / 360.0 * MAP_W
    y = MAP_Y0 + (LAT_TOP - lat) / (LAT_TOP - LAT_BOT) * MAP_H
    return (x, y)


def draw_header(d):
    d.rectangle([0, 0, W, 84], fill=INK)
    d.rectangle([0, 84, W, 87], fill=GOLD)
    title = load_font(True, 34)
    d.text((16, 42), "THE WORLD IN ONE DAY", font=title, fill=(255, 255, 255),
           anchor="lm")
    date_f = load_font(True, 19)
    d.text((1008, 34), "FRIDAY, 27 NOVEMBER 2026", font=date_f, fill=GOLD,
           anchor="rm")
    sub_f = load_font(False, 12)
    d.text((1008, 60), "40 STORIES  ·  EVERY CONTINENT", font=sub_f,
           fill=(255, 255, 255), anchor="rm")


def draw_top3(d):
    for i, (head, sub) in enumerate(TOP3):
        x = 16 + i * 336
        d.rectangle([x, 96, x + 320, 170], fill=BOX, outline=RULE)
        d.rectangle([x, 96, x + 5, 170], fill=RED)
        head_f = load_font(True, 14)
        sub_f = load_font(False, 11)
        h = fit(head, head_f, 320 - 24, d)
        d.text((x + 14, 112), h, font=head_f, fill=INK, anchor="lm")
        s = fit(sub, sub_f, 320 - 24, d)
        d.text((x + 14, 140), s, font=sub_f, fill=GREY, anchor="lm")
        num_f = load_font(True, 11)
        d.text((x + 14, 158), "TOP STORY %d" % (i + 1), font=num_f, fill=RED,
               anchor="lm")


def draw_map(d):
    d.rectangle([MAP_X0, MAP_Y0, MAP_X0 + MAP_W, MAP_Y0 + MAP_H], fill=SEA,
                outline=RULE)
    # faint graticule
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0)
        d.line([(x, MAP_Y0), (x, MAP_Y0 + MAP_H)], fill=(255, 255, 255))
    for lat in range(-60, 91, 30):
        _, y = project(0, lat)
        d.line([(MAP_X0, y), (MAP_X0 + MAP_W, y)], fill=(255, 255, 255))
    # land
    for poly in LAND_POLYS:
        pts = [project(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # markers
    num_f = load_font(True, 10)
    for num, _head, lat, lon, dx, dy in STORIES:
        px, py = project(lon, lat)
        bx, by = px + dx, py + dy
        if dx or dy:
            d.line([(px, py), (bx, by)], fill=GREY, width=1)
            d.ellipse([px - 2.5, py - 2.5, px + 2.5, py + 2.5], fill=INK)
        d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((bx, by - 0.5), str(num), font=num_f, fill=(255, 255, 255),
               anchor="mm")


def draw_legend(d):
    f = load_font(False, 11)
    d.text((16, 566), "Numbers match the story list below  ·  Marker positions "
           "approximate  ·  Map: stylised equirectangular projection",
           font=f, fill=GREY, anchor="lm")


def draw_list(d):
    num_f = load_font(True, 12)
    head_f = load_font(False, 12)
    per_col = [14, 13, 13]
    idx = 0
    for col, count in enumerate(per_col):
        x = COL_X[col]
        for row in range(count):
            num, headline, _lat, _lon, _dx, _dy = STORIES[idx]
            idx += 1
            y = LIST_Y0 + row * LIST_ROW_H
            d.text((x, y), "%d." % num, font=num_f, fill=RED, anchor="la")
            h = fit(headline, head_f, COL_W - 30, d)
            d.text((x + 30, y), h, font=head_f, fill=INK, anchor="la")


def draw_footer(d):
    d.line([(16, 978), (1008, 978)], fill=RULE, width=1)
    f = load_font(False, 11)
    d.text((16, 994), "Sources: Reuters · AP · AFP · Bloomberg · Xinhua · "
           "AAP · ANSA · Bangkok Post", font=f, fill=GREY, anchor="la")
    d.text((1008, 994), "All events reported 26–27 Nov 2026", font=f,
           fill=GREY, anchor="ra")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    draw_top3(d)
    draw_map(d)
    draw_legend(d)
    draw_list(d)
    draw_footer(d)
    d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=2)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, format="PNG")
    print("wrote %s (%d bytes)" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
