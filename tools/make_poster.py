#!/usr/bin/env python3
"""
tools/make_poster.py - Broadsheet front-page poster generator for 18 November 2026.
Draws a 1024x1024 newspaper poster using PIL primitives and DejaVu fonts.
"""

import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1024
HEIGHT = 1024

# Editorial Color Palette
COLOR_PAPER = (248, 244, 232)       # #f8f4e8 warm newsprint
COLOR_INK = (20, 24, 29)           # #14181d deep charcoal ink
COLOR_RED = (179, 35, 27)          # #b3231b editorial accent red
COLOR_SUB = (61, 70, 82)           # #3d4652 slate subhead text
COLOR_RULE = (50, 56, 64)          # crisp divider ink
COLOR_RULE_LIGHT = (195, 188, 172) # subtle secondary rule
COLOR_ICON_BG = (240, 235, 222)    # badge background for spot graphics
COLOR_ICON_BORDER = (185, 178, 162)# badge border
COLOR_SEA = (130, 168, 195)        # Persian Gulf blue water
COLOR_SEA_BORDER = (45, 75, 100)   # coastline definition
COLOR_LAND = (225, 218, 201)       # beige landmass
COLOR_LAND_LABEL = (120, 112, 98)  # muted land text
COLOR_WHITE = (255, 255, 255)

# Font paths
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)

def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: float) -> list[str]:
    """Wrap text to ensure it never exceeds max_width."""
    words = text.split()
    lines = []
    cur = []
    for w in words:
        candidate = " ".join(cur + [w])
        if font.getlength(candidate) <= max_width:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
                cur = [w]
            else:
                lines.append(w)
                cur = []
    if cur:
        lines.append(" ".join(cur))
    return lines

def draw_letterspaced_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    x: float,
    y: float,
    font: ImageFont.FreeTypeFont,
    fill,
    tracking: float = 4.0
):
    cur_x = x
    for ch in text:
        draw.text((cur_x, y), ch, font=font, fill=fill)
        cur_x += font.getlength(ch) + tracking

def measure_letterspaced_text(
    text: str,
    font: ImageFont.FreeTypeFont,
    tracking: float = 4.0
) -> float:
    total = 0.0
    for i, ch in enumerate(text):
        total += font.getlength(ch)
        if i < len(text) - 1:
            total += tracking
    return total

def draw_star(draw: ImageDraw.ImageDraw, cx: float, cy: float, r_out: float, r_in: float, fill):
    """Draw a 5-pointed star centered at (cx, cy)."""
    points = []
    for i in range(10):
        r = r_out if i % 2 == 0 else r_in
        ang = i * math.pi / 5 - math.pi / 2
        points.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(points, fill=fill)

def draw_bridge_icon(draw: ImageDraw.ImageDraw, bx: int, by: int, size: int = 68):
    """Icon (a): Bridge arc with a broken middle span (Kerch Bridge)."""
    # Background badge frame
    draw.rectangle([bx, by, bx + size, by + size], fill=COLOR_ICON_BG, outline=COLOR_ICON_BORDER, width=1)
    
    # Water at the bottom
    draw.rectangle([bx + 1, by + 46, bx + size - 1, by + size - 1], fill=COLOR_SEA)
    draw.line([(bx + 1, by + 46), (bx + size - 1, by + 46)], fill=COLOR_SEA_BORDER, width=1)
    
    # Bridge piers (concrete columns)
    draw.rectangle([bx + 16, by + 28, bx + 22, by + 50], fill=COLOR_INK)
    draw.rectangle([bx + 46, by + 28, bx + 52, by + 50], fill=COLOR_INK)
    
    # Left span & arch (intact)
    draw.line([(bx + 6, by + 32), (bx + 26, by + 32)], fill=COLOR_INK, width=3)
    draw.arc([bx + 6, by + 18, bx + 26, by + 46], start=180, end=360, fill=COLOR_INK, width=2)
    
    # Right span & arch (intact)
    draw.line([(bx + 42, by + 32), (bx + 62, by + 32)], fill=COLOR_INK, width=3)
    draw.arc([bx + 42, by + 18, bx + 62, by + 46], start=180, end=360, fill=COLOR_INK, width=2)
    
    # Broken middle span (road span collapsed into water at angle)
    draw.line([(bx + 26, by + 32), (bx + 33, by + 46)], fill=COLOR_RED, width=3)
    draw.line([(bx + 42, by + 32), (bx + 35, by + 46)], fill=COLOR_RED, width=3)
    
    # Break burst / smoke marks
    draw.line([(bx + 34, by + 24), (bx + 34, by + 34)], fill=COLOR_RED, width=2)
    draw.line([(bx + 30, by + 28), (bx + 38, by + 28)], fill=COLOR_RED, width=2)

def draw_diplomacy_icon(draw: ImageDraw.ImageDraw, bx: int, by: int, size: int = 68):
    """Icon (b): Three stars over two flag poles, abstract (Xi & Putin meet)."""
    # Background badge frame
    draw.rectangle([bx, by, bx + size, by + size], fill=COLOR_ICON_BG, outline=COLOR_ICON_BORDER, width=1)
    
    # Two flagpoles
    draw.line([(bx + 22, by + 26), (bx + 22, by + 58)], fill=COLOR_INK, width=2)
    draw.line([(bx + 46, by + 26), (bx + 46, by + 58)], fill=COLOR_INK, width=2)
    
    # Pole finials
    draw.ellipse([bx + 20, by + 23, bx + 24, by + 27], fill=COLOR_RED)
    draw.ellipse([bx + 44, by + 23, bx + 48, by + 27], fill=COLOR_RED)
    
    # Abstract waving flags
    draw.polygon([(bx + 22, by + 27), (bx + 36, by + 33), (bx + 22, by + 39)], fill=COLOR_RED)
    draw.polygon([(bx + 46, by + 27), (bx + 32, by + 33), (bx + 46, by + 39)], fill=COLOR_INK)
    
    # Three stars floating over flagpoles
    draw_star(draw, bx + 22, by + 14, 5.0, 2.2, COLOR_RED)
    draw_star(draw, bx + 34, by + 10, 6.0, 2.5, COLOR_RED)
    draw_star(draw, bx + 46, by + 14, 5.0, 2.2, COLOR_RED)

def draw_ballot_icon(draw: ImageDraw.ImageDraw, bx: int, by: int, size: int = 68):
    """Icon (c): A ballot box with a ballot sliding in (Peltola Senate race)."""
    # Background badge frame
    draw.rectangle([bx, by, bx + size, by + size], fill=COLOR_ICON_BG, outline=COLOR_ICON_BORDER, width=1)
    
    # Ballot box body
    draw.rectangle([bx + 14, by + 28, bx + 54, by + 58], fill=COLOR_PAPER, outline=COLOR_INK, width=2)
    # Box slot
    draw.rectangle([bx + 22, by + 26, bx + 46, by + 29], fill=COLOR_INK)
    # Ballot emblem stripe
    draw.line([(bx + 16, by + 44), (bx + 52, by + 44)], fill=COLOR_RULE_LIGHT, width=1)
    
    # Ballot paper sliding into the slot
    draw.polygon([(bx + 26, by + 10), (bx + 42, by + 10), (bx + 42, by + 27), (bx + 26, by + 27)],
                 fill=COLOR_WHITE, outline=COLOR_INK, width=1)
    
    # Red checkmark on ballot paper
    draw.line([(bx + 30, by + 18), (bx + 33, by + 22)], fill=COLOR_RED, width=2)
    draw.line([(bx + 33, by + 22), (bx + 38, by + 14)], fill=COLOR_RED, width=2)

def draw_virus_icon(draw: ImageDraw.ImageDraw, bx: int, by: int, size: int = 68):
    """Icon (d): A virus circle with spike proteins (Ebola outbreak)."""
    # Background badge frame
    draw.rectangle([bx, by, bx + size, by + size], fill=COLOR_ICON_BG, outline=COLOR_ICON_BORDER, width=1)
    
    cx = bx + size / 2
    cy = by + size / 2
    r_body = 13.0
    
    # Radial spike proteins
    num_spikes = 10
    for i in range(num_spikes):
        ang = i * 2 * math.pi / num_spikes
        sx0 = cx + r_body * math.cos(ang)
        sy0 = cy + r_body * math.sin(ang)
        sx1 = cx + (r_body + 8.0) * math.cos(ang)
        sy1 = cy + (r_body + 8.0) * math.sin(ang)
        draw.line([(sx0, sy0), (sx1, sy1)], fill=COLOR_RED, width=2)
        # Spike bulb
        draw.ellipse([sx1 - 2.5, sy1 - 2.5, sx1 + 2.5, sy1 + 2.5], fill=COLOR_RED)
    
    # Central virus body
    draw.ellipse([cx - r_body, cy - r_body, cx + r_body, cy + r_body],
                 fill=COLOR_INK, outline=COLOR_RED, width=2)
    # Inner viral core
    draw.ellipse([cx - 4.0, cy - 4.0, cx + 4.0, cy + 4.0], fill=COLOR_RED)

def draw_schematic_map(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int):
    """Draw a schematic map panel of the Persian Gulf & Strait of Hormuz with Kuwait, Bahrain, Qeshm."""
    # Outer frame & land background
    draw.rectangle([x0, y0, x1, y1], fill=COLOR_LAND, outline=COLOR_INK, width=2)
    
    # Header bar
    draw.rectangle([x0, y0, x1, y0 + 20], fill=COLOR_INK)
    f_map_hdr = get_font(FONT_BOLD_PATH, 10)
    draw.text((x0 + 10, y0 + 4), "PERSIAN GULF & STRAIT OF HORMUZ", font=f_map_hdr, fill=COLOR_PAPER)
    draw.text((x1 - 32, y0 + 4), "N ↑", font=f_map_hdr, fill=COLOR_PAPER)
    
    # Water body polygon (Persian Gulf through Strait of Hormuz)
    water_poly = [
        (x0 + 15, y0 + 35),
        (x0 + 75, y0 + 38),
        (x0 + 155, y0 + 65),
        (x0 + 240, y0 + 95),
        (x0 + 305, y0 + 98),
        (x1 - 10, y0 + 135),
        (x1 - 10, y1 - 35),
        (x1 - 65, y1 - 25),
        (x0 + 280, y0 + 150),
        (x0 + 240, y0 + 165),
        (x0 + 175, y0 + 155),
        (x0 + 120, y0 + 140),
        (x0 + 35, y0 + 85),
        (x0 + 15, y0 + 55),
    ]
    draw.polygon(water_poly, fill=COLOR_SEA, outline=COLOR_SEA_BORDER, width=2)
    
    # Landmass territory labels
    f_land = get_font(FONT_BOLD_PATH, 11)
    draw.text((x0 + 140, y0 + 32), "IRAN", font=f_land, fill=COLOR_LAND_LABEL)
    draw.text((x0 + 38, y1 - 38), "ARABIAN PENINSULA", font=f_land, fill=COLOR_LAND_LABEL)
    
    # Qeshm Island in the Strait of Hormuz
    q_cx, q_cy = x0 + 268, y0 + 102
    draw.ellipse([q_cx - 15, q_cy - 6, q_cx + 15, q_cy + 6], fill=COLOR_LAND, outline=COLOR_INK, width=1)
    
    # Waterway name label
    f_water = get_font(FONT_REGULAR_PATH, 9)
    draw.text((x0 + 260, y0 + 160), "Gulf of Oman", font=f_water, fill=COLOR_SEA_BORDER)
    
    # Three red dots and labels: KUWAIT, BAHRAIN, QESHM
    lbl_font = get_font(FONT_BOLD_PATH, 11)
    locations = [
        ("KUWAIT", x0 + 45, y0 + 55, 12, -7),
        ("BAHRAIN", x0 + 130, y0 + 115, 12, -7),
        ("QESHM", q_cx, q_cy, -62, -8),
    ]
    
    for name, dx, dy, tx_off, ty_off in locations:
        # Red marker dot with white border
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=COLOR_RED, outline=COLOR_WHITE, width=2)
        # Label with clear white box
        lx = dx + tx_off
        ly = dy + ty_off
        w = lbl_font.getlength(name)
        draw.rectangle([lx - 4, ly - 2, lx + w + 4, ly + 14], fill=COLOR_WHITE, outline=COLOR_INK, width=1)
        draw.text((lx, ly), name, font=lbl_font, fill=COLOR_INK)

def create_poster() -> Image.Image:
    # 1024x1024 canvas
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_PAPER)
    draw = ImageDraw.Draw(img)

    margin_x = 40
    right_x = WIDTH - margin_x  # 984px
    usable_width = right_x - margin_x  # 944px

    # ==========================================
    # 1. MASTHEAD BLOCK
    # ==========================================
    y = 38

    # Top thin rule
    draw.line([(margin_x, y), (right_x, y)], fill=COLOR_INK, width=2)
    y += 8

    # Small caps tracking title: "THE WORLD IN ONE DAY"
    f_mast_tag = get_font(FONT_BOLD_PATH, 13)
    tag_text = "THE WORLD IN ONE DAY"
    tag_tracking = 6.0
    tag_w = measure_letterspaced_text(tag_text, f_mast_tag, tag_tracking)
    tag_x = margin_x + (usable_width - tag_w) / 2
    draw_letterspaced_text(draw, tag_text, tag_x, y, f_mast_tag, COLOR_INK, tag_tracking)
    y += 24

    # Date in huge bold type on two lines: WEDNESDAY / 18 NOVEMBER 2026 (~80px bold)
    f_date = get_font(FONT_BOLD_PATH, 80)
    
    wed_text = "WEDNESDAY"
    wed_w = f_date.getlength(wed_text)
    wed_x = margin_x + (usable_width - wed_w) / 2
    draw.text((wed_x, y), wed_text, font=f_date, fill=COLOR_INK)
    y += 72

    date_text = "18 NOVEMBER 2026"
    date_w = f_date.getlength(date_text)
    date_x = margin_x + (usable_width - date_w) / 2
    draw.text((date_x, y), date_text, font=f_date, fill=COLOR_INK)
    y += 80

    # Bottom masthead double rules
    draw.line([(margin_x, y), (right_x, y)], fill=COLOR_INK, width=3)
    draw.line([(margin_x, y + 5), (right_x, y + 5)], fill=COLOR_INK, width=1)
    y += 16

    # ==========================================
    # 2. LEAD STORY BLOCK
    # ==========================================
    lead_start_y = y
    lead_text_width = 530
    map_x0 = margin_x + lead_text_width + 24
    map_x1 = right_x
    map_y0 = lead_start_y + 2
    map_y1 = lead_start_y + 236

    # Schematic map panel
    draw_schematic_map(draw, map_x0, map_y0, map_x1, map_y1)

    # Lead kicker
    f_lead_kicker = get_font(FONT_BOLD_PATH, 15)
    draw.text((margin_x, y), "MIDDLE EAST ESCALATION", font=f_lead_kicker, fill=COLOR_RED)
    y += 24

    # Headline bold ~50px: "IRAN STRIKES KUWAIT AND BAHRAIN"
    f_lead_head = get_font(FONT_BOLD_PATH, 48)
    lead_head_lines = wrap_text("IRAN STRIKES KUWAIT AND BAHRAIN", f_lead_head, lead_text_width)
    for line in lead_head_lines:
        draw.text((margin_x, y), line, font=f_lead_head, fill=COLOR_INK)
        y += 52
    y += 8

    # Sub ~22px: "Retaliation for US strikes on Qeshm Island in the Strait of Hormuz, as Gulf tensions spiral"
    f_lead_sub = get_font(FONT_REGULAR_PATH, 22)
    lead_sub_lines = wrap_text(
        "Retaliation for US strikes on Qeshm Island in the Strait of Hormuz, as Gulf tensions spiral",
        f_lead_sub,
        lead_text_width
    )
    for line in lead_sub_lines:
        draw.text((margin_x, y), line, font=f_lead_sub, fill=COLOR_SUB)
        y += 28

    # Divider rule below lead story
    y = max(y + 12, map_y1 + 14)
    draw.line([(margin_x, y), (right_x, y)], fill=COLOR_RULE, width=1)
    y += 12

    # ==========================================
    # 3. FOUR PANELS IN 2x2 GRID (WITH ICONS)
    # ==========================================
    col_gap = 26
    col_width = (usable_width - col_gap) // 2  # ~459px
    col0_x = margin_x
    col1_x = margin_x + col_width + col_gap
    row_height = 152

    panels_data = [
        # (row, col, kicker, headline, sub, icon_drawer)
        (0, 0, "EUROPE · WAR", "UKRAINE HITS KERCH BRIDGE AGAIN",
         "Road span collapses in a second day of attacks on the Crimea link", draw_bridge_icon),
        (0, 1, "ASIA · DIPLOMACY", "XI AND PUTIN MEET IN SHENZHEN",
         "Trump arrives in China for Thursday's three-way summit at APEC", draw_diplomacy_icon),
        (1, 0, "AMERICAS · POLITICS", "PELTOLA WINS ALASKA SENATE RACE",
         "Democrats take a 56-44 majority in the US Senate", draw_ballot_icon),
        (1, 1, "AFRICA · HEALTH", "EBOLA PASSES 11,000 CASES IN DR CONGO",
         "Children under five are hit hardest by the outbreak", draw_virus_icon),
    ]

    grid_start_y = y
    f_panel_kicker = get_font(FONT_BOLD_PATH, 13)
    f_panel_head = get_font(FONT_BOLD_PATH, 27)
    f_panel_sub = get_font(FONT_REGULAR_PATH, 18)

    icon_size = 68
    head_max_w = col_width - icon_size - 14  # ~377px

    for r, c, kicker, headline, sub, icon_func in panels_data:
        px = col0_x if c == 0 else col1_x
        py = grid_start_y + r * (row_height + 10)

        # Draw icon in top-right of panel
        icon_x = px + col_width - icon_size
        icon_y = py
        icon_func(draw, icon_x, icon_y, icon_size)

        # Draw kicker
        draw.text((px, py + 2), kicker, font=f_panel_kicker, fill=COLOR_RED)
        cur_y = py + 20

        # Draw headline (left of icon)
        head_lines = wrap_text(headline, f_panel_head, head_max_w)
        for hl in head_lines:
            draw.text((px, cur_y), hl, font=f_panel_head, fill=COLOR_INK)
            cur_y += 31
        cur_y += 6

        # Draw sub (spanning full width below headline and icon)
        sub_lines = wrap_text(sub, f_panel_sub, col_width - 8)
        for sl in sub_lines:
            draw.text((px, cur_y), sl, font=f_panel_sub, fill=COLOR_SUB)
            cur_y += 21

    # Vertical divider line between columns
    grid_end_y = grid_start_y + 2 * row_height + 10
    mid_x = margin_x + col_width + col_gap // 2
    draw.line([(mid_x, grid_start_y), (mid_x, grid_end_y)], fill=COLOR_RULE, width=1)

    # Horizontal divider between row 0 and row 1
    mid_row_y = grid_start_y + row_height + 5
    draw.line([(col0_x, mid_row_y), (col0_x + col_width, mid_row_y)], fill=COLOR_RULE, width=1)
    draw.line([(col1_x, mid_row_y), (col1_x + col_width, mid_row_y)], fill=COLOR_RULE, width=1)

    # Divider below grid
    y = grid_end_y + 8
    draw.line([(margin_x, y), (right_x, y)], fill=COLOR_RULE, width=1)
    y += 10

    # ==========================================
    # 4. FULL-WIDTH STRIP
    # ==========================================
    strip_y = y

    # Line 1: Kicker on its own line
    draw.text((margin_x, strip_y), "AMERICAS · HEALTH", font=f_panel_kicker, fill=COLOR_RED)
    strip_y += 20

    # Line 2: Headline on the next line
    f_strip_head = get_font(FONT_BOLD_PATH, 25)
    draw.text((margin_x, strip_y), "US LOSES MEASLES-FREE STATUS", font=f_strip_head, fill=COLOR_INK)
    strip_y += 30

    # Line 3: Sub on its own line BELOW the headline
    f_strip_sub = get_font(FONT_REGULAR_PATH, 17)
    strip_sub_text = "Elimination status ends after 26 years amid a record outbreak"
    draw.text((margin_x, strip_y), strip_sub_text, font=f_strip_sub, fill=COLOR_SUB)

    # Divider below strip (fully frames the strip before the ticker)
    y = strip_y + 24
    draw.line([(margin_x, y), (right_x, y)], fill=COLOR_RULE, width=1)
    y += 10

    # ==========================================
    # 5. BOTTOM TICKER (BLACK BAR, WHITE TEXT)
    # ==========================================
    ticker_top = y
    ticker_bottom = 984  # Leaves exactly 40px bottom margin (>= 36px)
    
    # Black ticker bar
    draw.rectangle([margin_x, ticker_top, right_x, ticker_bottom], fill=COLOR_INK)
    # Red accent left indicator
    draw.rectangle([margin_x, ticker_top, margin_x + 6, ticker_bottom], fill=COLOR_RED)

    # Ticker text on two lines
    f_ticker_bold = get_font(FONT_BOLD_PATH, 12)
    f_ticker_reg = get_font(FONT_REGULAR_PATH, 12)

    line1_bold_part = "IN BRIEF — "
    line1_body_part = "Israel's Knesset elects Matan Kahana as speaker · Russian military plane crash in Siberia kills 19"
    line2_text = "EU approves signing of Indonesia trade deal · Markets slide worldwide; gold at $3,775"

    tx = margin_x + 18
    t_y1 = ticker_top + 10
    t_y2 = ticker_top + 30

    # Line 1
    draw.text((tx, t_y1), line1_bold_part, font=f_ticker_bold, fill=COLOR_WHITE)
    bold_part_w = f_ticker_bold.getlength(line1_bold_part)
    draw.text((tx + bold_part_w + 2, t_y1), line1_body_part, font=f_ticker_reg, fill=COLOR_WHITE)

    # Line 2
    draw.text((tx, t_y2), line2_text, font=f_ticker_reg, fill=COLOR_WHITE)

    return img

def main():
    poster = create_poster()
    out_path = Path("entry.png")
    poster.save(out_path, format="PNG", optimize=True)
    print(f"Saved {out_path} ({poster.size[0]}x{poster.size[1]})")

if __name__ == "__main__":
    main()
