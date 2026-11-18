#!/usr/bin/env python3
"""
tools/make_poster.py - Broadsheet front-page poster generator for 18 November 2026.
Draws a 1024x1024 newspaper poster using PIL primitives and DejaVu fonts.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Canvas dimensions
WIDTH = 1024
HEIGHT = 1024

# Editorial Color Palette
COLOR_PAPER = (248, 244, 232)      # #f8f4e8 warm newsprint
COLOR_INK = (20, 24, 29)          # #14181d deep charcoal ink
COLOR_RED = (179, 35, 27)         # #b3231b editorial accent red
COLOR_SUB = (61, 70, 82)          # #3d4652 slate subhead text
COLOR_RULE = (40, 45, 52)         # subtle divider ink
COLOR_MAP_BG = (235, 228, 214)     # warm map background
COLOR_SEA = (145, 178, 202)        # Persian Gulf blue water
COLOR_LAND = (226, 217, 196)       # beige landmass

# Font paths
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REGULAR_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(path: str, size: int):
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

def draw_letterspaced_text(draw: ImageDraw.ImageDraw, text: str, x: float, y: float, font: ImageFont.FreeTypeFont, fill, tracking: float = 4.0):
    cur_x = x
    for ch in text:
        draw.text((cur_x, y), ch, font=font, fill=fill)
        cur_x += font.getlength(ch) + tracking

def measure_letterspaced_text(text: str, font: ImageFont.FreeTypeFont, tracking: float = 4.0) -> float:
    total = 0.0
    for i, ch in enumerate(text):
        total += font.getlength(ch)
        if i < len(text) - 1:
            total += tracking
    return total

def draw_schematic_map(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int):
    """Draw a schematic map of the Persian Gulf & Strait of Hormuz with Kuwait, Bahrain, Qeshm."""
    # Outer map frame
    draw.rectangle([x0, y0, x1, y1], fill=COLOR_LAND, outline=COLOR_INK, width=2)

    # Water body (Persian Gulf & Strait of Hormuz)
    # A curved water corridor from upper-left to bottom-right
    water_poly = [
        (x0 + 10, y0 + 15),
        (x0 + 90, y0 + 20),
        (x0 + 180, y0 + 65),
        (x0 + 260, y0 + 120),
        (x1 - 25, y0 + 155),
        (x1 - 10, y1 - 20),
        (x1 - 70, y1 - 15),
        (x0 + 240, y1 - 45),
        (x0 + 170, y0 + 150),
        (x0 + 110, y0 + 130),
        (x0 + 20, y0 + 80),
        (x0 + 10, y0 + 40),
    ]
    draw.polygon(water_poly, fill=COLOR_SEA, outline=COLOR_INK)

    # Qeshm Island inside Strait of Hormuz (narrow opening near right)
    qeshm_x = x0 + 270
    qeshm_y = y0 + 138
    draw.ellipse([qeshm_x - 14, qeshm_y - 6, qeshm_x + 14, qeshm_y + 6], fill=COLOR_LAND, outline=COLOR_INK, width=1)

    # Label font
    lbl_font = get_font(FONT_BOLD_PATH, 11)
    sub_lbl_font = get_font(FONT_REGULAR_PATH, 9)

    # Map header label inside map box
    draw.rectangle([x0, y0, x0 + 160, y0 + 18], fill=COLOR_INK)
    draw.text((x0 + 8, y0 + 3), "STRAIT OF HORMUZ / GULF", font=get_font(FONT_BOLD_PATH, 9), fill=COLOR_PAPER)

    # The 3 dots: Kuwait, Bahrain, Qeshm
    locations = [
        ("KUWAIT", x0 + 38, y0 + 35, 10, -5),
        ("BAHRAIN", x0 + 130, y0 + 115, 12, 0),
        ("QESHM", qeshm_x, qeshm_y - 2, 10, -14),
    ]

    for name, dx, dy, tx_off, ty_off in locations:
        # Red marker dot with white border
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=COLOR_RED, outline=(255, 255, 255), width=2)
        # Background box for label readability
        w = lbl_font.getlength(name)
        lx = dx + tx_off
        ly = dy + ty_off
        draw.rectangle([lx - 3, ly - 2, lx + w + 3, ly + 14], fill=(248, 244, 232, 230), outline=COLOR_INK, width=1)
        draw.text((lx, ly), name, font=lbl_font, fill=COLOR_INK)

def create_poster() -> Image.Image:
    # 1024x1024 canvas
    img = Image.new("RGB", (WIDTH, HEIGHT), COLOR_PAPER)
    draw = ImageDraw.Draw(img)

    margin_x = 36
    usable_width = WIDTH - 2 * margin_x  # 952px

    # ==========================================
    # 1. MASTHEAD
    # ==========================================
    y = 36

    # Top thin rule
    draw.line([(margin_x, y), (WIDTH - margin_x, y)], fill=COLOR_INK, width=2)
    y += 8

    # Small caps tracking title: "THE WORLD IN ONE DAY"
    f_lead_tag = get_font(FONT_BOLD_PATH, 13)
    tag_text = "THE WORLD IN ONE DAY"
    tag_tracking = 5.0
    tag_w = measure_letterspaced_text(tag_text, f_lead_tag, tag_tracking)
    tag_x = margin_x + (usable_width - tag_w) / 2
    draw_letterspaced_text(draw, tag_text, tag_x, y, f_lead_tag, COLOR_INK, tag_tracking)
    y += 24

    # Date in very large bold type on two lines: WEDNESDAY / 18 NOVEMBER 2026
    f_date = get_font(FONT_BOLD_PATH, 78)
    
    wed_text = "WEDNESDAY"
    wed_w = f_date.getlength(wed_text)
    wed_x = margin_x + (usable_width - wed_w) / 2
    draw.text((wed_x, y), wed_text, font=f_date, fill=COLOR_INK)
    y += 72

    date_text = "18 NOVEMBER 2026"
    date_w = f_date.getlength(date_text)
    date_x = margin_x + (usable_width - date_w) / 2
    draw.text((date_x, y), date_text, font=f_date, fill=COLOR_INK)
    y += 84

    # Bottom masthead rule
    draw.line([(margin_x, y), (WIDTH - margin_x, y)], fill=COLOR_INK, width=3)
    draw.line([(margin_x, y + 4), (WIDTH - margin_x, y + 4)], fill=COLOR_INK, width=1)
    y += 16

    # ==========================================
    # 2. LEAD STORY BLOCK
    # ==========================================
    lead_start_y = y
    lead_text_width = 540
    map_x0 = margin_x + lead_text_width + 24
    map_x1 = WIDTH - margin_x
    map_y0 = lead_start_y + 4
    map_y1 = lead_start_y + 240

    # Draw schematic map panel beside lead story
    draw_schematic_map(draw, map_x0, map_y0, map_x1, map_y1)

    # Lead kicker
    f_kicker = get_font(FONT_BOLD_PATH, 15)
    draw.text((margin_x, y), "MIDDLE EAST ESCALATION", font=f_kicker, fill=COLOR_RED)
    y += 24

    # Lead headline bold ~50px: "IRAN STRIKES KUWAIT AND BAHRAIN"
    f_lead_head = get_font(FONT_BOLD_PATH, 48)
    lead_head_lines = wrap_text("IRAN STRIKES KUWAIT AND BAHRAIN", f_lead_head, lead_text_width)
    for line in lead_head_lines:
        draw.text((margin_x, y), line, font=f_lead_head, fill=COLOR_INK)
        y += 52
    y += 8

    # Lead sub ~24px: "Retaliation for US strikes on Qeshm Island in the Strait of Hormuz, as Gulf tensions spiral"
    f_lead_sub = get_font(FONT_REGULAR_PATH, 22)
    lead_sub_lines = wrap_text(
        "Retaliation for US strikes on Qeshm Island in the Strait of Hormuz, as Gulf tensions spiral",
        f_lead_sub,
        lead_text_width
    )
    for line in lead_sub_lines:
        draw.text((margin_x, y), line, font=f_lead_sub, fill=COLOR_SUB)
        y += 28

    # Divider below lead story
    y = max(y + 12, map_y1 + 14)
    draw.line([(margin_x, y), (WIDTH - margin_x, y)], fill=COLOR_RULE, width=1)
    y += 12

    # ==========================================
    # 3. FOUR PANELS IN 2x2 GRID
    # ==========================================
    col_gap = 28
    col_width = (usable_width - col_gap) // 2  # ~462px
    col0_x = margin_x
    col1_x = margin_x + col_width + col_gap
    row_height = 168

    panels_data = [
        # (row, col, kicker, headline, sub)
        (0, 0, "EUROPE · WAR", "UKRAINE HITS KERCH BRIDGE AGAIN",
         "Road span collapses in a second day of attacks on the Crimea link"),
        (0, 1, "ASIA · DIPLOMACY", "XI AND PUTIN MEET IN SHENZHEN",
         "Trump arrives in China for Thursday's three-way summit at APEC"),
        (1, 0, "AMERICAS · POLITICS", "PELTOLA WINS ALASKA SENATE RACE",
         "Democrats take a 56-44 majority in the US Senate"),
        (1, 1, "AFRICA · HEALTH", "EBOLA PASSES 11,000 CASES IN DR CONGO",
         "Children under five are hit hardest by the outbreak"),
    ]

    grid_start_y = y
    f_panel_kicker = get_font(FONT_BOLD_PATH, 13)
    f_panel_head = get_font(FONT_BOLD_PATH, 27)
    f_panel_sub = get_font(FONT_REGULAR_PATH, 18)

    for r, c, kicker, headline, sub in panels_data:
        px = col0_x if c == 0 else col1_x
        py = grid_start_y + r * (row_height + 12)

        # Draw kicker
        draw.text((px, py), kicker, font=f_panel_kicker, fill=COLOR_RED)
        cur_y = py + 20

        # Draw headline
        head_lines = wrap_text(headline, f_panel_head, col_width)
        for hl in head_lines:
            draw.text((px, cur_y), hl, font=f_panel_head, fill=COLOR_INK)
            cur_y += 31
        cur_y += 6

        # Draw sub
        sub_lines = wrap_text(sub, f_panel_sub, col_width)
        for sl in sub_lines:
            draw.text((px, cur_y), sl, font=f_panel_sub, fill=COLOR_SUB)
            cur_y += 22

    # Vertical divider line between columns
    grid_end_y = grid_start_y + 2 * row_height + 8
    mid_x = margin_x + col_width + col_gap // 2
    draw.line([(mid_x, grid_start_y), (mid_x, grid_end_y)], fill=COLOR_RULE, width=1)

    # Horizontal divider between row 0 and row 1
    mid_row_y = grid_start_y + row_height + 4
    draw.line([(col0_x, mid_row_y), (col0_x + col_width, mid_row_y)], fill=COLOR_RULE, width=1)
    draw.line([(col1_x, mid_row_y), (col1_x + col_width, mid_row_y)], fill=COLOR_RULE, width=1)

    # Divider below grid
    y = grid_end_y + 12
    draw.line([(margin_x, y), (WIDTH - margin_x, y)], fill=COLOR_RULE, width=1)
    y += 10

    # ==========================================
    # 4. FULL-WIDTH STRIP
    # ==========================================
    strip_y = y
    draw.text((margin_x, strip_y), "AMERICAS · HEALTH", font=f_panel_kicker, fill=COLOR_RED)
    strip_y += 20
    f_strip_head = get_font(FONT_BOLD_PATH, 26)
    draw.text((margin_x, strip_y), "US LOSES MEASLES-FREE STATUS", font=f_strip_head, fill=COLOR_INK)
    
    # Sub placed on the right side of the strip
    f_strip_sub = get_font(FONT_REGULAR_PATH, 18)
    strip_sub_text = "Elimination status ends after 26 years amid a record outbreak"
    sub_w = f_strip_sub.getlength(strip_sub_text)
    draw.text((WIDTH - margin_x - sub_w, strip_y + 5), strip_sub_text, font=f_strip_sub, fill=COLOR_SUB)

    return img

def main():
    poster = create_poster()
    out_path = Path("entry.png")
    poster.save(out_path, format="PNG", optimize=True)
    print(f"Saved {out_path} ({poster.size[0]}x{poster.size[1]})")

if __name__ == "__main__":
    main()
