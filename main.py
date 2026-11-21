#!/usr/bin/env python3
"""news-image-20261121: draw "The World in One Day - 21 November 2026".

Pure-stdlib Python (zlib + struct PNG encoder, no PIL, no network, no
external assets). Writes one deterministic 1024x1024 PNG to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font
# 5x7 bitmap font. Each glyph is 7 strings of 5 chars ('#' = ink).
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01110", "00001", "01111", "10001", "01111"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01110", "10000", "10000", "10001", "01110"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01111"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "01111", "10001", "10001", "01111", "00001", "01110"),
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "10010", "01100"),
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "11110", "10000", "10000"),
    'q': ("00000", "00000", "01111", "10001", "01111", "00001", "00001"),
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11100", "01000", "01000", "01001", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "10101", "01010"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "01111", "00001", "01110"),
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '\u2013': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '\u2014': ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '\u00b7': ("00000", "00000", "00000", "01100", "01100", "00000", "00000"),
    '$': ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    '#': ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    '@': ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    '_': ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    '*': ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    '<': ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    '>': ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
}

ADV = 6  # advance per char in font units (5 glyph + 1 space)


def text_width(s, scale):
    return len(s) * (5 * scale + 1) - 1 if s else 0


def wrap_text(s, max_width, scale):
    """Greedy word wrap; returns a list of lines fitting max_width px."""
    unit = 5 * scale + 1
    max_chars = max(1, (max_width + 1) // unit)
    words = s.split(' ')
    lines, cur = [], ''
    for w in words:
        trial = w if not cur else cur + ' ' + w
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            while len(cur) > max_chars:  # over-long single word: hard split
                lines.append(cur[:max_chars])
                cur = cur[max_chars:]
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bytes(bg) * (w * h))

    def rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(color) * (x1 - x0)
        for yy in range(y0, y1):
            off = (yy * self.w + x0) * 3
            self.px[off:off + (x1 - x0) * 3] = row

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            off = (y * self.w + x) * 3
            self.px[off:off + 3] = bytes(color)

    def line(self, x0, y0, x1, y1, color, thick=1):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if thick <= 1:
                self.set(x0, y0, color)
            else:
                self.rect(x0 - thick // 2, y0 - thick // 2, thick, thick, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, color, fill=True):
        if fill:
            for yy in range(cy - r, cy + r + 1):
                dx = int((r * r - (yy - cy) ** 2) ** 0.5) if abs(yy - cy) <= r else 0
                self.rect(cx - dx, yy, 2 * dx + 1, 1, color)
        else:
            steps = max(8, r * 6)
            for i in range(steps):
                import math
                a = 2 * math.pi * i / steps
                self.set(int(cx + r * math.cos(a)), int(cy + r * math.sin(a)), color)

    def poly(self, pts, color):
        """Filled polygon (scanline). pts: list of (x, y)."""
        if len(pts) < 3:
            return
        ys = [p[1] for p in pts]
        for y in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                self.rect(int(xs[j]), y, int(xs[j + 1]) - int(xs[j]) + 1, 1, color)

    def text(self, x, y, s, scale, color, bold=False):
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT[' '])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == '1':
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
                        if bold:
                            self.rect(cx + col * scale + 1, y + row * scale,
                                      scale, scale, color)
            cx += 5 * scale + 1
        return cx

    def text_lines(self, x, y, lines, scale, color, lh=None, bold=False):
        if lh is None:
            lh = 7 * scale + 2
        for ln in lines:
            self.text(x, y, ln, scale, color, bold=bold)
            y += lh
        return y


# ---------------------------------------------------------------- PNG out
def write_png(canvas, path):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)  # filter: none
        raw += canvas.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', struct.pack('>IIBBBBB', canvas.w, canvas.h, 8, 2, 0, 0, 0))
    png += chunk(b'IDAT', comp)
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- palette
PAPER = (246, 241, 230)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
NAVY2 = (28, 52, 96)
RED = (176, 42, 30)
GOLD = (192, 138, 26)
TEAL = (14, 107, 107)
GREY = (110, 108, 100)
LIGHT = (255, 255, 255)
CARD = (255, 253, 247)
RULE = (200, 192, 172)
SKY = (16, 24, 48)
SKY2 = (38, 52, 92)
ORANGE = (240, 140, 40)
YELLOW = (250, 200, 60)
LAND = (216, 205, 178)
LAND2 = (196, 182, 148)

# ---------------------------------------------------------------- stories
# Lead + 39 numbered stories + 10 "Also Today" = 50 stories, every one
# happened or first reported on Saturday 21 November 2026 (any time zone).
LEAD_KICKER = "LEAD  ·  EUROPE  ·  KYIV / POLAND"
LEAD_HEAD = ["RUSSIA'S BIGGEST", "BARRAGE HITS KYIV", "\u2014 MISSILES IN POLAND"]
LEAD_SUB = ("400+ drones and 110 missiles overnight. Bridges, rail and "
            "power hit in 10 regions; at least eight killed in Kyiv. "
            "Three projectiles fell in Poland \u2014 Tusk calls it a "
            "deliberate provocation. (BBC \u00b7 France 24)")

STORIES = [
    "HORMUZ: two tankers hit; US-Iran talks stall, AFP",
    "ICJ: Myanmar guilty of Rohingya genocide, ICJ",
    "MARKETS: AI rout drags S&P into correction, AP",
    "FBI database, USDA systems hacked, reports say, AP",
    "COP31 talks pass deadline over fossil fuels, UN",
    "UK-EU sign 3 post-Brexit deals, Reuters",
    "Cost-of-living protests spread in 25 nations, AP",
    "Denmark expels Russian envoy in 'kill plot', AFP",
    "Houthis fire on Riyadh; coalition hits back, AFP",
    "Israeli fire kills Palestinians in Gaza, AFP",
    "Cartel boss 'Chapo Isidro' captured in Mexico, AFP",
    "M6.7 quake shakes central Peru, USGS",
    "Basra plant fire kills 4, injures 30, Reuters",
    "Man convicted over deadly LA Palisades fire, AFP",
    "Three Salvadoran soldiers killed in Haiti blast, AFP",
    "Phumzile Mlambo-Ngcuka dies at 71, AFP",
    "Man gets 19 yrs in Sikh-leader kill plot, AP",
    "Spain heads to 29 Nov election, AP",
    "China sidelines Japan as ties hit record low, AP",
    "Nigeria boat capsizes; four dead, Al Jazeera",
    "Paris police sentenced over racist beating, AFP",
    "Bolsonaro in hospital with bowel obstruction, AP",
    "Trump defends Putin ties; Zelenskyy: 'killer', AP",
    "US loses measles elimination status, AP",
    "Uganda limits gatherings as Ebola spreads, AP",
    "Cancer pill makes tumours vanish in 1 in 12, Trial",
    "Riemann proof claimed with AI help, CLAIM",
    "CERN finds first sign of ultra-rare decay, CERN",
    "BepiColombo reaches Mercury orbit, ESA/JAXA",
    "Voyager 1: 24 light-hours from Earth, NASA",
    "Pilotless air taxi carries passenger in Japan, AP",
    "US sells deep-sea mining leases off Samoa, AP",
    "Argentina country risk tops 1,000 points, AP",
    "Kenya starts onshore crude drilling in Turkana, AP",
    "Saudi Arabia, Japan agree oil stockpile deal, AP",
    "Nepal PM Balendra Shah to visit India, AP",
    "Vietnam speeds land seizures, Reuters",
    "Wildberries CEO quits over EU sanctions, Reuters",
    "Ex-Italian police chief dies at 78, Reuters",
]

ALSO = [
    "CRICKET \u2014 KL Rahul first Indian opener with Test 100s in all SENA nations",
    "F1 \u2014 Verstappen on pole for Las Vegas GP after Antonelli penalty",
    "TENNIS \u2014 Alcaraz beats Cobolli at ATP Finals despite thigh worry",
    "NBA \u2014 Harden passes Kobe on 50-point games list",
    "NFL \u2014 Texans beat Colts 26-3 behind C.J. Stroud",
    "K-POP \u2014 BTS win five MAMA awards in Osaka",
    "AFLW \u2014 North Melbourne into fourth straight grand final",
    "SPEED SKATING \u2014 Choi Min-jeong wins third straight World Tour 1,000m",
    "FOOTBALL \u2014 Kane out for months with ankle injury",
    "CRICKET \u2014 India A crush Nepal by 306 runs; Nepal 26 all out",
]

TIMELINE = [
    ("00:09", "M6.7 quake", "shakes Peru"),
    ("OVERNIGHT", "Russia's barrage", "hits Kyiv"),
    ("MORNING", "Two tankers hit", "in Hormuz"),
    ("MIDDAY", "ICJ genocide", "ruling: Myanmar"),
    ("AFTERNOON", "UK-EU sign three", "post-Brexit deals"),
    ("EVENING", "US stocks close", "in correction"),
]

# World-map pins: (lon, lat, label)
PINS = [
    (30, 50, "L"), (19, 52, "1"), (56, 26, "1"), (4, 52, "2"),
    (-74, 40, "3"), (30, 36, "5"), (4, 50, "6"), (46, 24, "9"),
    (34, 31, "10"), (-99, 19, "11"), (-77, -12, "12"), (47, 30, "13"),
    (-118, 34, "14"), (18, -34, "16"), (-3, 40, "18"), (139, 35, "19"),
    (3, 6, "20"), (2, 48, "21"), (-47, -15, "22"),
]

CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 68), (-105, 68),
     (-95, 69), (-88, 66), (-82, 66), (-78, 71), (-72, 62), (-65, 60),
     (-60, 55), (-55, 52), (-59, 47), (-65, 44), (-70, 42), (-74, 39),
     (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 29), (-94, 29),
     (-97, 26), (-97, 19), (-94, 17), (-90, 14), (-86, 12), (-83, 9),
     (-80, 8), (-77, 7), (-79, 9), (-82, 9), (-86, 13), (-88, 13),
     (-90, 14), (-92, 15), (-96, 16), (-97, 19), (-102, 18), (-106, 22),
     (-110, 24), (-114, 28), (-117, 32), (-122, 37), (-124, 42),
     (-125, 48), (-130, 54), (-135, 58), (-145, 60), (-155, 58),
     (-162, 55), (-168, 60)],
    # South America
    [(-80, 8), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
     (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50),
     (-70, -55), (-66, -55), (-68, -50), (-65, -45), (-62, -40),
     (-58, -35), (-52, -32), (-48, -28), (-41, -23), (-38, -15),
     (-35, -8), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4),
     (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10)],
    # Europe
    [(-10, 36), (-9, 43), (-1, 46), (-4, 48), (0, 50), (3, 51), (7, 54),
     (8, 57), (10, 58), (6, 62), (12, 66), (20, 70), (28, 71), (32, 70),
     (30, 66), (28, 62), (24, 59), (21, 55), (24, 58), (28, 60),
     (30, 59), (24, 57), (19, 54), (15, 55), (12, 54), (8, 54),
     (5, 53), (2, 51), (-2, 50), (-5, 48), (-2, 47), (-1, 44),
     (-3, 43), (-9, 43), (-9, 37), (-6, 36), (-2, 37), (0, 38),
     (3, 42), (7, 44), (10, 44), (12, 42), (16, 40), (18, 40),
     (15, 38), (12, 38), (10, 37), (8, 39), (3, 38), (-1, 37)],
    # Africa
    [(-17, 15), (-17, 21), (-15, 27), (-10, 31), (-5, 35), (0, 36),
     (10, 37), (11, 34), (20, 32), (25, 31), (32, 31), (34, 28),
     (37, 22), (39, 18), (43, 12), (48, 11), (51, 12), (46, 5),
     (42, 0), (40, -5), (40, -10), (38, -15), (36, -20), (33, -26),
     (28, -33), (20, -35), (17, -32), (15, -27), (12, -18), (12, -10),
     (13, -5), (9, 4), (4, 6), (-8, 5), (-13, 8), (-17, 12)],
    # Asia
    [(30, 70), (40, 72), (60, 73), (75, 73), (90, 75), (110, 76),
     (130, 72), (150, 70), (160, 69), (178, 66), (170, 60), (162, 60),
     (158, 52), (142, 50), (140, 45), (135, 43), (130, 42), (127, 40),
     (122, 38), (120, 32), (122, 28), (118, 25), (110, 20), (108, 18),
     (105, 10), (103, 5), (100, 7), (98, 12), (95, 16), (92, 21),
     (88, 22), (85, 19), (80, 15), (77, 8), (75, 12), (72, 20),
     (68, 23), (65, 25), (61, 25), (57, 26), (54, 27), (51, 29),
     (48, 30), (44, 29), (40, 31), (38, 36), (35, 36), (32, 36),
     (30, 41), (28, 45), (30, 50), (30, 60), (28, 65)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
     (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
     (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
     (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # Greenland
    [(-45, 60), (-40, 64), (-32, 68), (-25, 70), (-20, 74), (-25, 76),
     (-35, 77), (-45, 76), (-55, 74), (-58, 70), (-55, 64), (-50, 60)],
]


# ---------------------------------------------------------------- drawing
def draw_burst(c, cx, cy, r, color, core):
    for i in range(8):
        ang = i * 3.14159 / 4
        c.line(cx, cy, int(cx + r * 1.5 * (1 if i % 2 == 0 else 0.45) * _cos(ang)),
               int(cy + r * 1.5 * (1 if i % 2 == 0 else 0.45) * _sin(ang)),
               color, thick=2)
    c.circle(cx, cy, r, color)
    c.circle(cx, cy, max(2, r // 2), core)


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


def draw_lead_graphic(c, x, y, w, h):
    """Night sky over a city under attack: skyline, missile streaks, bursts."""
    c.rect(x, y, w, h, SKY)
    c.rect(x, y, w, h // 3, SKY2)
    # stars
    for sx, sy in [(12, 8), (40, 20), (70, 6), (105, 16), (140, 9), (170, 22),
                   (200, 7), (230, 18), (255, 10), (285, 20), (310, 8),
                   (25, 32), (90, 30), (160, 34), (215, 30), (295, 34)]:
        c.set(x + sx, y + sy, (200, 200, 220))
    # missile streaks
    c.line(x + 30, y + 10, x + 150, y + 95, ORANGE, thick=2)
    c.line(x + 200, y + 6, x + 260, y + 70, YELLOW, thick=2)
    c.line(x + 90, y + 2, x + 60, y + 80, ORANGE, thick=2)
    c.circle(x + 150, y + 95, 3, YELLOW)
    c.circle(x + 260, y + 70, 3, YELLOW)
    c.circle(x + 60, y + 80, 3, YELLOW)
    # bursts
    draw_burst(c, x + 150, y + 105, 7, ORANGE, YELLOW)
    draw_burst(c, x + 265, y + 80, 5, ORANGE, YELLOW)
    draw_burst(c, x + 60, y + 92, 5, ORANGE, YELLOW)
    # skyline silhouette
    base = y + h - 6
    heights = [46, 70, 38, 84, 56, 96, 44, 66, 36, 78, 52, 88, 40, 62, 48]
    bw = w // len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw
        c.rect(bx, base - hh, bw - 2, hh, (8, 10, 22))
        # lit windows
        for wy in range(base - hh + 8, base - 6, 12):
            for wx in range(bx + 4, bx + bw - 6, 9):
                if (wx * 7 + wy * 3) % 5 == 0:
                    c.rect(wx, wy, 3, 4, YELLOW)
    c.rect(x, base, w, 6, (8, 10, 22))
    c.text(x + 8, y + h - 18, "KYIV \u2014 OVERNIGHT", 1, LIGHT, bold=True)


def draw_map(c, x, y, w, h):
    c.rect(x, y, w, h, (232, 226, 208))
    c.rect(x, y, w, 1, RULE)
    c.rect(x, y + h - 1, w, 1, RULE)

    def proj(lon, lat):
        px = x + int((lon + 180) / 360.0 * w)
        py = y + int((78 - lat) / 136.0 * h)
        return (px, py)

    for poly in CONTINENTS:
        c.poly([proj(lon, lat) for lon, lat in poly], LAND)
    # pin dots with numbers
    for lon, lat, label in PINS:
        px, py = proj(lon, lat)
        c.circle(px, py, 7, RED)
        c.circle(px, py, 7, RED, fill=False)
        c.text(px - 2, py - 3, label, 1, LIGHT, bold=True)
    c.text(x + 6, y + 4, "WHERE IT HAPPENED", 1, NAVY, bold=True)
    c.text(x + w - 118, y + 4, "RED DOT = A STORY", 1, RED, bold=True)




def build():
    c = Canvas(W, H, PAPER)

    # ---- masthead ------------------------------------------------------
    c.rect(0, 0, W, 80, NAVY)
    c.rect(0, 80, W, 4, GOLD)
    c.text(16, 8, "THE WORLD IN ONE DAY", 6, LIGHT, bold=True)
    c.text(16, 58, "SATURDAY \u00b7 21 NOVEMBER 2026", 2, GOLD, bold=True)
    right = "50 STORIES \u00b7 VERIFIED TO 21 NOV 2026"
    c.text(W - 16 - text_width(right, 2), 58, right, 2, LIGHT, bold=True)

    # ---- lead story ----------------------------------------------------
    c.rect(16, 88, 992, 200, CARD)
    c.rect(16, 88, 992, 1, RULE)
    c.rect(16, 287, 992, 1, RULE)
    c.rect(16, 88, 6, 200, RED)
    c.text(30, 98, LEAD_KICKER, 1, RED, bold=True)
    y = 114
    for ln in LEAD_HEAD:
        c.text(30, y, ln, 4, INK, bold=True)
        y += 31
    sub = wrap_text(LEAD_SUB, 600, 2)
    c.text_lines(30, 212, sub, 2, INK, lh=16)
    draw_lead_graphic(c, 664, 92, 340, 192)

    # ---- UTC timeline --------------------------------------------------
    c.text(16, 296, "THE DAY IN UTC", 1, NAVY, bold=True)
    c.line(170, 312, 1008, 312, RULE, thick=2)
    for i, (t, a, b) in enumerate(TIMELINE):
        cx = 200 + i * 158
        c.circle(cx, 312, 4, RED)
        for yy, s, col in ((298, t, RED), (320, a, INK), (330, b, INK)):
            tx = cx - text_width(s, 1) // 2
            tx = max(8, min(W - 8 - text_width(s, 1), tx))
            c.text(tx, yy, s, 1, col, bold=(col is RED))

    # ---- world map -----------------------------------------------------
    draw_map(c, 16, 344, 992, 82)

    # ---- numbered stories ---------------------------------------------
    c.text(16, 434, "39 MORE STORIES", 2, NAVY, bold=True)
    c.text(1008 - text_width("EACH VERIFIED TO 21 NOV 2026", 1), 437,
           "EACH VERIFIED TO 21 NOV 2026", 1, GREY, bold=True)
    c.rect(16, 452, 992, 2, NAVY)
    for i, s in enumerate(STORIES):
        col, row = divmod(i, 13)
        x = 16 + col * 336
        y = 460 + row * 34
        c.rect(x, y, 24, 24, RED)
        num = str(i + 1)
        c.text(x + (24 - text_width(num, 2)) // 2, y + 5, num, 2, LIGHT,
               bold=True)
        lines = wrap_text(s, 290, 2)
        c.text_lines(x + 30, y + 1, lines, 2, INK, lh=15)

    # ---- also today ----------------------------------------------------
    c.text(16, 908, "ALSO TODAY", 2, NAVY, bold=True)
    c.rect(16, 926, 992, 2, NAVY)
    for i, a in enumerate(ALSO):
        col, row = divmod(i, 5)
        x = 16 + col * 504
        y = 936 + row * 11
        c.text(x, y, "\u00b7", 1, RED, bold=True)
        c.text(x + 10, y, a, 1, INK)

    # ---- footer: date check + sources ----------------------------------
    c.rect(16, 996, 624, 2, NAVY)
    c.rect(656, 996, 352, 2, NAVY)
    c.text(16, 1004, "DATE CHECK \u2014 NOT 21 NOV, SO LEFT OUT:", 1, RED,
           bold=True)
    c.text(656, 1004, "SOURCES: AP \u00b7 REUTERS \u00b7 AFP \u00b7 BBC \u00b7 "
           "FRANCE 24", 1, NAVY, bold=True)
    c.text(16, 1014, "Anthropic IPO (19 Nov) \u00b7 Shenzhen summit "
           "(19 Nov) \u00b7 Vietnam (20 Nov) \u00b7 Kerch (earlier)", 1, INK)
    c.text(656, 1014, "USGS \u00b7 ICJ \u00b7 ESA \u00b7 NASA \u00b7 CLAIM = "
           "unconfirmed", 1, INK)
    return c


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    c = build()
    path = os.path.join(outdir, "entry.png")
    n = write_png(c, path)
    print("wrote %s (%d bytes)" % (path, n))


if __name__ == "__main__":
    main()
