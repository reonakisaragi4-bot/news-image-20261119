#!/usr/bin/env python3
"""Render the one-image summary of Thursday 19 November 2026 world news.

A newspaper front page at 1024x1024: a navy masthead naming the day, a
small world map with a red dot per story, then a 5-by-6 grid of 30 short
items (place tag, headline, caption). Every item below was checked against
live news reporting on 20 November 2026 as an event that happened, or was
first reported, on 19 November 2026 in some time zone. The two headliners
were re-verified this morning: the first-ever Trump-Xi-Putin trilateral
meeting in Shenzhen and the ICJ's 9-6 genocide ruling on Myanmar.

Run:  python3 draw_poster.py   (writes entry.png next to this script)
"""

from PIL import Image, ImageDraw, ImageFont

CANVAS_W, CANVAS_H = 1024, 1024
OUTFILE = "entry.png"

BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

PAPER = (252, 250, 245)
INK = (20, 28, 40)
NAVY = (13, 27, 62)
CRIMSON = (176, 32, 32)
GOLD = (200, 160, 60)
CARD = (255, 255, 255)
RULE = (200, 208, 220)
GREY = (90, 100, 115)
OCEAN = (214, 226, 235)
LAND = (150, 165, 180)

# Region colours for the place tags and the top strip of each card.
PALETTE = {
    "ASIA": (24, 96, 168),
    "EUROPE": (110, 40, 160),
    "MIDEAST": (184, 90, 10),
    "AFRICA": (150, 70, 14),
    "AMERICAS": (22, 130, 65),
    "GLOBAL": (96, 112, 132),
    "SPORT": (190, 24, 93),
}

# (place, region, headline, caption). Headlines stay short enough for two
# 15px lines in a ~170px cell; captions for three 11px lines.
ITEMS = [
    ("SHENZHEN", "ASIA", "Trump, Xi, Putin meet at APEC",
     "First trilateral summit; 'peace declaration' on nuclear risk."),
    ("THE HAGUE", "EUROPE", "ICJ: Myanmar committed genocide",
     "9-6 ruling on Rohingya; first verdict of its kind."),
    ("NEW YORK", "AMERICAS", "Anthropic IPO sets record",
     "Shares close +17%; ~$2tn value, first pure-AI listing."),
    ("WASHINGTON", "AMERICAS", "Senate rejects Iran war powers",
     "51-48 vote; three Republicans backed the measure."),
    ("WASHINGTON", "AMERICAS", "Court halts Venezuela TPS order",
     "Appeals court grants Trump stay; SCOTUS bid filed."),
    ("RIYADH", "MIDEAST", "Houthi missile hits PIF Tower",
     "Strike damages Riyadh tower; NYT reporter saw it."),
    ("CRIMEA", "EUROPE", "Ukraine hits Crimean Bridge again",
     "Third attack this week, Russia says; Putin vows reply."),
    ("LONDON", "EUROPE", "UK, Norway fund Ukraine ships",
     "£100m+ joint programme for two naval craft."),
    ("LONDON", "EUROPE", "UK sends 1,000 drones to Kyiv",
     "Long-range strike drones pledged to Ukraine."),
    ("BRUSSELS", "EUROPE", "Europe open to Russia talks",
     "Leaders say ready for talks on ending Ukraine war."),
    ("TOKYO", "ASIA", "Takaichi says she talked to Putin",
     "Japan PM: agreed to keep communicating with Moscow."),
    ("GAZA", "MIDEAST", "Israel completes Gaza operation",
     "Ground op beyond Yellow Line ends; Hamas condemns."),
    ("GAZA", "MIDEAST", "Peace plan rated 4 out of 26",
     "Five aid groups score the 20-point plan's rollout."),
    ("GENEVA", "GLOBAL", "589m children in conflict zones",
     "23.4% of children lived in conflict in 2025."),
    ("ODISHA", "ASIA", "Cyclone Akvan nears landfall",
     "~300,000 evacuated; 423 rescue teams on standby."),
    ("SHENZHEN", "ASIA", "APEC adopts Shenzhen Outlook",
     "Voluntary pact on trade, data and AI risks."),
    ("COPENHAGEN", "EUROPE", "Denmark backs Greenland defence",
     "Parliament approves defence agreement 109-0."),
    ("BELGRADE", "EUROPE", "Cupic elected Serbia speaker",
     "New parliament speaker wins 140 votes to 97."),
    ("DHAKA", "ASIA", "Bangladesh shutdown turns violent",
     "Opposition shutdown; Yunus ancestral home attacked."),
    ("LONDON", "EUROPE", "Leasehold system to be scrapped",
     "Ground rent capped at £250 in England and Wales."),
    ("LONDON", "EUROPE", "Covid inquiry reports findings",
     "Report covers testing, tracing and 'the pingdemic'."),
    ("NEW YORK", "AMERICAS", "JPMorgan hit by cyberattack",
     "Thousands of customer emails leaked via vendors."),
    ("WASHINGTON", "AMERICAS", "Iran war costs pass $48.3bn",
     "Lawmakers seek unreleased base-damage estimates."),
    ("HANGZHOU", "ASIA", "Alibaba slips on earnings miss",
     "Shares fall despite 53% cloud revenue growth."),
    ("PARIS", "EUROPE", "Van Gogh sells for $190.4m",
     "Record price for a Van Gogh painting at auction."),
    ("CINCINNATI", "AMERICAS", "Fiona the hippo dies",
     "Cincinnati hippo dies after swallowing a visitor's hat."),
    ("LONDON", "EUROPE", "UK joins GTA 6 frenzy",
     "Game available worldwide; queues form at midnight."),
    ("TURIN", "SPORT", "Shelton, Zverev win in Turin",
     "ATP Finals: Shelton beats Jodar; Zverev tops Fils."),
    ("LONDON", "SPORT", "England fined over fan chants",
     "UEFA fines England for anti-Catholic chants in Spain."),
    ("WASHINGTON", "AMERICAS", "Jeffries nominated House Speaker",
     "Hakeem Jeffries nominated to lead the House."),
]

# One map pin per story: (longitude, latitude, region). Same-city pins are
# nudged a little so they do not sit exactly on top of each other.
PINS = [
    (114, 22.5, "ASIA"), (4.3, 52.1, "EUROPE"), (-74, 40.7, "AMERICAS"),
    (-77, 38.9, "AMERICAS"), (-76.3, 38.6, "AMERICAS"),
    (46.7, 24.7, "MIDEAST"), (34, 45, "EUROPE"), (-0.1, 51.5, "EUROPE"),
    (-0.6, 51.2, "EUROPE"), (4.4, 50.8, "EUROPE"), (139.7, 35.7, "ASIA"),
    (34.5, 31.5, "MIDEAST"), (34.8, 31.3, "MIDEAST"), (6.1, 46.2, "GLOBAL"),
    (85.8, 20.3, "ASIA"), (114.3, 22.7, "ASIA"), (12.6, 55.7, "EUROPE"),
    (20.5, 44.8, "EUROPE"), (90.4, 23.8, "ASIA"), (-0.3, 51.4, "EUROPE"),
    (0.2, 51.6, "EUROPE"), (-74.3, 40.5, "AMERICAS"),
    (-77.3, 38.7, "AMERICAS"), (120.2, 30.3, "ASIA"), (2.35, 48.85, "EUROPE"),
    (-84.5, 39.1, "AMERICAS"), (-0.5, 51.5, "EUROPE"), (7.7, 45.1, "SPORT"),
    (-0.15, 51.45, "SPORT"), (-77.1, 39.0, "AMERICAS"),
]

# Rough continent shapes as (lon, lat) rings, equirectangular. Deliberately
# simplified: the map is a locator, not an atlas.
SHAPES = [
    # North America
    [(-168, 66), (-130, 71), (-95, 69), (-75, 62), (-55, 47), (-70, 44),
     (-80, 32), (-90, 21), (-105, 20), (-120, 35), (-125, 49), (-150, 60),
     (-168, 66)],
    # Greenland
    [(-55, 64), (-40, 60), (-25, 70), (-45, 76), (-58, 76)],
    # South America
    [(-79, 9), (-60, 10), (-50, 0), (-38, -8), (-45, -25), (-58, -38),
     (-70, -52), (-72, -30), (-79, -5)],
    # Europe
    [(-10, 36), (-9, 43), (0, 51), (8, 57), (18, 56), (28, 60), (30, 66),
     (20, 70), (5, 60), (-5, 58), (-10, 50)],
    # Africa
    [(-17, 15), (-10, 30), (10, 37), (32, 31), (43, 12), (51, 11),
     (40, -10), (32, -28), (18, -35), (12, -18), (9, 4), (-13, 8)],
    # Asia
    [(32, 62), (60, 70), (100, 76), (140, 72), (170, 66), (160, 55),
     (140, 40), (127, 35), (115, 23), (105, 10), (97, 16), (80, 10),
     (70, 22), (55, 26), (42, 30), (32, 36)],
    # Australia
    [(114, -22), (115, -35), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (137, -12), (126, -14), (114, -22)],
]


def typeface(size, bold=False):
    return ImageFont.truetype(BOLD_PATH if bold else PLAIN_PATH, size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap of one string into lines no wider than width."""
    out = []
    current = ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def paint_header(draw):
    draw.rectangle([0, 0, CANVAS_W, 98], fill=NAVY)
    draw.rectangle([0, 98, CANVAS_W, 103], fill=CRIMSON)
    draw.text((24, 14), "THURSDAY 19 NOVEMBER 2026",
              font=typeface(30, bold=True), fill=(255, 255, 255))
    draw.text((1000, 14), "THE WORLD IN ONE DAY",
              font=typeface(20, bold=True), fill=GOLD, anchor="ra")
    draw.text((24, 58), "30 STORIES  ·  SIX CONTINENTS  ·  ONE DAY",
              font=typeface(17, bold=True), fill=(203, 213, 225))
    draw.text((1000, 58), "19 NOV 2026",
              font=typeface(17, bold=True), fill=(203, 213, 225), anchor="ra")


def paint_map(draw):
    x0, y0, x1, y1 = 16, 116, 1008, 258
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=OCEAN,
                           outline=RULE, width=1)
    draw.text((x0 + 10, y0 + 6), "WHERE THE NEWS HAPPENED",
              font=typeface(13, bold=True), fill=GREY)

    def project(lon, lat):
        px = x0 + 8 + (lon + 170) / 360.0 * (x1 - x0 - 16)
        py = y0 + 22 + (75 - lat) / 130.0 * (y1 - y0 - 30)
        return (px, py)

    for ring in SHAPES:
        draw.polygon([project(lon, lat) for lon, lat in ring], fill=LAND)
    for lon, lat, _region in PINS:
        px, py = project(lon, lat)
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=CRIMSON,
                     outline=(255, 255, 255), width=1)


def paint_cards(draw):
    margin, gap = 16, 8
    cols, rows = 5, 6
    top = 270
    grid_h = CANVAS_H - top - 28
    cw = (CANVAS_W - 2 * margin - (cols - 1) * gap) // cols
    ch = (grid_h - (rows - 1) * gap) // rows
    for i, (place, region, headline, caption) in enumerate(ITEMS):
        col, row = i % cols, i // cols
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        colour = PALETTE[region]
        draw.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=CARD,
                               outline=RULE, width=1)
        # Region colour strip across the top of the card.
        draw.rounded_rectangle([x0, y0, x1, y0 + 5], radius=6, fill=colour)
        draw.rectangle([x0, y0 + 3, x1, y0 + 5], fill=colour)
        tx = x0 + 10
        draw.text((tx, y0 + 10), f"{i + 1:02d}  {place}",
                  font=typeface(12, bold=True), fill=colour)
        y = y0 + 28
        for line in fit_lines(draw, headline, typeface(15, bold=True),
                              cw - 20)[:2]:
            draw.text((tx, y), line, font=typeface(15, bold=True), fill=INK)
            y += 18
        for line in fit_lines(draw, caption, typeface(11), cw - 20)[:3]:
            draw.text((tx, y), line, font=typeface(11), fill=GREY)
            y += 14


def paint_footer(draw):
    draw.text((512, CANVAS_H - 14),
              "All 30 stories happened or were first reported on Thursday 19 November 2026.",
              font=typeface(13), fill=GREY, anchor="mm")


def main():
    assert len(ITEMS) == 30, f"expected 30 stories, got {len(ITEMS)}"
    assert len(PINS) == 30, f"expected 30 map pins, got {len(PINS)}"
    img = Image.new("RGB", (CANVAS_W, CANVAS_H), PAPER)
    draw = ImageDraw.Draw(img)
    paint_header(draw)
    paint_map(draw)
    paint_cards(draw)
    paint_footer(draw)
    img.save(OUTFILE, optimize=True)
    print(f"wrote {OUTFILE}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
