"""
Bioluminescent Circuitry - Plant Light Sculpture
A visual expression of organic forms meeting electronic precision
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import random

# Canvas setup - high resolution
WIDTH, HEIGHT = 1200, 900
BACKGROUND = (5, 10, 18)  # Deep navy-black

# Color palette - bioluminescent
CYAN_GLOW = (56, 189, 248)
PURPLE_GLOW = (167, 139, 250)
MINT_GLOW = (52, 211, 153)
WARM_GLOW = (251, 191, 36)

def lerp_color(c1, c2, t):
    """Linear interpolation between two colors"""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def add_glow(draw, x, y, radius, color, intensity=0.3):
    """Add a soft glow effect at a point"""
    for r in range(radius, 0, -2):
        alpha = int(255 * intensity * (r / radius) ** 2)
        glow_color = (*color, alpha)
        # We'll composite this separately

def draw_glowing_circle(img, x, y, radius, color, glow_radius=None):
    """Draw a circle with glow effect"""
    if glow_radius is None:
        glow_radius = radius * 3

    # Create glow layer
    glow = Image.new('RGBA', (int(glow_radius*2), int(glow_radius*2)), (0,0,0,0))
    glow_draw = ImageDraw.Draw(glow)

    # Draw concentric circles for glow
    center = glow_radius
    for r in range(int(glow_radius), 0, -2):
        alpha = int(80 * (1 - r/glow_radius) ** 1.5)
        glow_draw.ellipse([center-r, center-r, center+r, center+r],
                         fill=(*color, alpha))

    # Draw core
    glow_draw.ellipse([center-radius, center-radius, center+radius, center+radius],
                      fill=(*color, 255))

    # Paste onto main image
    paste_x = int(x - glow_radius)
    paste_y = int(y - glow_radius)
    img.paste(glow, (paste_x, paste_y), glow)

def draw_glowing_line(img, x1, y1, x2, y2, color, width=2, glow_width=8):
    """Draw a line with glow effect"""
    # Create a larger canvas for the line segment
    padding = glow_width * 2
    min_x, max_x = min(x1, x2) - padding, max(x1, x2) + padding
    min_y, max_y = min(y1, y2) - padding, max(y1, y2) + padding

    line_width = int(max_x - min_x) + 1
    line_height = int(max_y - min_y) + 1

    if line_width <= 0 or line_height <= 0:
        return

    line_img = Image.new('RGBA', (line_width, line_height), (0,0,0,0))
    line_draw = ImageDraw.Draw(line_img)

    # Adjusted coordinates
    ax1, ay1 = x1 - min_x, y1 - min_y
    ax2, ay2 = x2 - min_x, y2 - min_y

    # Draw glow layers
    for w in range(glow_width, 0, -1):
        alpha = int(60 * (1 - w/glow_width))
        line_draw.line([(ax1, ay1), (ax2, ay2)], fill=(*color, alpha), width=w*2)

    # Draw core line
    line_draw.line([(ax1, ay1), (ax2, ay2)], fill=(*color, 200), width=width)

    img.paste(line_img, (int(min_x), int(min_y)), line_img)

def draw_organic_branch(img, start_x, start_y, length, angle, depth, color, width=3):
    """Recursively draw organic branching structure"""
    if depth <= 0 or length < 5:
        return

    # Calculate end point with slight organic curve
    curve = random.uniform(-0.1, 0.1)
    end_x = start_x + length * math.cos(angle + curve)
    end_y = start_y - length * math.sin(angle + curve)  # Negative because y increases downward

    # Draw the branch
    draw_glowing_line(img, start_x, start_y, end_x, end_y, color,
                      width=max(1, int(width)), glow_width=int(width*2))

    # Add node at end
    if depth > 1:
        draw_glowing_circle(img, end_x, end_y, int(width+1), color, glow_radius=int(width*4))

    # Branch out
    if depth > 1:
        # Main continuation
        new_angle = angle + random.uniform(-0.3, 0.3)
        draw_organic_branch(img, end_x, end_y, length * 0.75, new_angle,
                           depth-1, color, max(1, width*0.8))

        # Side branches
        if random.random() > 0.3:
            branch_angle = angle + random.uniform(0.4, 0.8) * random.choice([-1, 1])
            draw_organic_branch(img, end_x, end_y, length * 0.5, branch_angle,
                               depth-2, color, max(1, width*0.6))

def draw_led_strip(img, points, color):
    """Draw a strip of LED nodes along a path"""
    for i, (x, y) in enumerate(points):
        # Vary the brightness slightly
        brightness = 0.7 + 0.3 * math.sin(i * 0.5)
        adjusted_color = tuple(int(c * brightness) for c in color)
        draw_glowing_circle(img, x, y, 4, adjusted_color, glow_radius=15)

def draw_pot_base(draw, center_x, bottom_y, width, height, color):
    """Draw a geometric pot/base"""
    # Trapezoid shape
    top_width = width * 0.7
    points = [
        (center_x - width/2, bottom_y),
        (center_x + width/2, bottom_y),
        (center_x + top_width/2, bottom_y - height),
        (center_x - top_width/2, bottom_y - height),
    ]

    # Draw with subtle gradient effect
    for i in range(3):
        alpha = 150 - i * 40
        offset = i * 2
        adjusted_points = [
            (points[0][0] + offset, points[0][1] - offset),
            (points[1][0] - offset, points[1][1] - offset),
            (points[2][0] - offset, points[2][1] + offset),
            (points[3][0] + offset, points[3][1] + offset),
        ]
        draw.polygon(adjusted_points, fill=(*color, alpha), outline=(*CYAN_GLOW, 100))

def create_plant_sculpture():
    """Create the main plant light sculpture artwork"""

    # Create base image with alpha
    img = Image.new('RGBA', (WIDTH, HEIGHT), (*BACKGROUND, 255))
    draw = ImageDraw.Draw(img)

    # Add subtle grid pattern in background (circuit board aesthetic)
    grid_color = (20, 35, 55)
    for x in range(0, WIDTH, 50):
        draw.line([(x, 0), (x, HEIGHT)], fill=grid_color, width=1)
    for y in range(0, HEIGHT, 50):
        draw.line([(0, y), (WIDTH, y)], fill=grid_color, width=1)

    # Add corner nodes on grid
    for x in range(0, WIDTH, 100):
        for y in range(0, HEIGHT, 100):
            if random.random() > 0.7:
                draw_glowing_circle(img, x, y, 2, CYAN_GLOW, glow_radius=8)

    # Center of composition
    center_x = WIDTH // 2
    base_y = HEIGHT - 120

    # Draw the pot/base
    pot_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    pot_draw = ImageDraw.Draw(pot_layer)

    # Geometric pot with glow
    pot_width = 180
    pot_height = 80
    pot_top = base_y - pot_height

    # Pot outline with glow effect
    for i in range(10, 0, -1):
        alpha = int(30 * (1 - i/10))
        offset = i
        pot_draw.polygon([
            (center_x - pot_width/2 - offset, base_y + offset),
            (center_x + pot_width/2 + offset, base_y + offset),
            (center_x + pot_width*0.35 + offset, pot_top - offset),
            (center_x - pot_width*0.35 - offset, pot_top - offset),
        ], fill=(*CYAN_GLOW, alpha))

    # Solid pot interior
    pot_draw.polygon([
        (center_x - pot_width/2, base_y),
        (center_x + pot_width/2, base_y),
        (center_x + pot_width*0.35, pot_top),
        (center_x - pot_width*0.35, pot_top),
    ], fill=(15, 25, 40), outline=(*CYAN_GLOW, 180))

    # Add circuit traces on pot
    for i in range(5):
        y = pot_top + 15 + i * 12
        pot_draw.line([(center_x - pot_width*0.3, y), (center_x + pot_width*0.3, y)],
                      fill=(*CYAN_GLOW, 60), width=1)

    img.paste(pot_layer, (0, 0), pot_layer)

    # Main stem from center
    stem_base = (center_x, pot_top - 10)

    # Draw main organic structures
    random.seed(42)  # For reproducibility

    # Central main stem with cyan glow
    draw_organic_branch(img, stem_base[0], stem_base[1], 180, math.pi/2 + 0.1,
                       6, CYAN_GLOW, width=5)

    # Secondary stems - purple
    draw_organic_branch(img, stem_base[0] - 30, stem_base[1] + 20, 140,
                       math.pi/2 + 0.5, 5, PURPLE_GLOW, width=4)
    draw_organic_branch(img, stem_base[0] + 30, stem_base[1] + 20, 130,
                       math.pi/2 - 0.4, 5, PURPLE_GLOW, width=4)

    # Tertiary stems - mint
    draw_organic_branch(img, stem_base[0] - 50, stem_base[1] + 40, 100,
                       math.pi/2 + 0.8, 4, MINT_GLOW, width=3)
    draw_organic_branch(img, stem_base[0] + 50, stem_base[1] + 40, 90,
                       math.pi/2 - 0.7, 4, MINT_GLOW, width=3)

    # Add LED node clusters (like flowers/buds)
    led_positions = [
        (center_x, stem_base[1] - 200),  # Top
        (center_x - 80, stem_base[1] - 150),
        (center_x + 90, stem_base[1] - 140),
        (center_x - 120, stem_base[1] - 80),
        (center_x + 110, stem_base[1] - 90),
        (center_x - 60, stem_base[1] - 180),
        (center_x + 70, stem_base[1] - 170),
    ]

    # Draw larger glowing "flower" nodes
    for i, (x, y) in enumerate(led_positions):
        color = [CYAN_GLOW, PURPLE_GLOW, MINT_GLOW][i % 3]
        # Add slight position variation
        x += random.randint(-10, 10)
        y += random.randint(-10, 10)
        draw_glowing_circle(img, x, y, 8 + i % 3, color, glow_radius=40)

        # Add smaller satellite nodes
        for j in range(3):
            angle = (j / 3) * 2 * math.pi + i * 0.5
            sat_x = x + 20 * math.cos(angle)
            sat_y = y + 20 * math.sin(angle)
            draw_glowing_circle(img, sat_x, sat_y, 3, color, glow_radius=15)

    # Add floating particles/spores for atmosphere
    for _ in range(30):
        x = random.randint(100, WIDTH - 100)
        y = random.randint(100, HEIGHT - 200)
        color = random.choice([CYAN_GLOW, PURPLE_GLOW, MINT_GLOW])
        size = random.randint(1, 3)
        draw_glowing_circle(img, x, y, size, color, glow_radius=size*4)

    # Add Arduino board suggestion at base
    board_x = center_x + 120
    board_y = base_y - 40
    board_w, board_h = 60, 40

    # Board outline
    draw.rectangle([board_x, board_y, board_x + board_w, board_y + board_h],
                   fill=(20, 30, 45), outline=(*MINT_GLOW, 150))

    # Board details (chip, pins)
    draw.rectangle([board_x + 15, board_y + 10, board_x + 45, board_y + 30],
                   fill=(10, 15, 25), outline=(*CYAN_GLOW, 100))

    # Pin headers
    for i in range(8):
        px = board_x + 5 + i * 6
        draw.rectangle([px, board_y + 35, px + 3, board_y + 40],
                       fill=(*WARM_GLOW, 180))

    # Wire from board to plant
    draw_glowing_line(img, board_x, board_y + 20, center_x + 60, pot_top + 20,
                      MINT_GLOW, width=2, glow_width=6)

    # Load font for text
    try:
        font_path = "/sessions/optimistic-modest-curie/mnt/.skills/skills/canvas-design/canvas-fonts/Jura-Light.ttf"
        title_font = ImageFont.truetype(font_path, 28)
        label_font = ImageFont.truetype(font_path, 14)
        small_font = ImageFont.truetype(font_path, 11)
    except:
        title_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # Add minimal typography
    text_layer = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    text_draw = ImageDraw.Draw(text_layer)

    # Title - subtle, positioned thoughtfully
    title = "PLANT LIGHT SCULPTURE"
    text_draw.text((60, 50), title, font=title_font, fill=(*CYAN_GLOW, 200))

    # Subtitle
    subtitle = "Interactive Electronics · 3D Printed · Arduino + FastLED"
    text_draw.text((60, 85), subtitle, font=label_font, fill=(150, 170, 190, 180))

    # Technical labels (sparse, clinical)
    text_draw.text((board_x - 10, board_y - 20), "MCU", font=small_font, fill=(*MINT_GLOW, 150))
    text_draw.text((center_x - 15, base_y + 20), "5V", font=small_font, fill=(*CYAN_GLOW, 120))

    # Measurement markers
    text_draw.text((WIDTH - 100, HEIGHT - 40), "WS2812B", font=small_font, fill=(*PURPLE_GLOW, 120))

    img.paste(text_layer, (0, 0), text_layer)

    # Final subtle vignette
    vignette = Image.new('RGBA', (WIDTH, HEIGHT), (0,0,0,0))
    vignette_draw = ImageDraw.Draw(vignette)

    for i in range(50):
        alpha = int(2 * i)
        offset = i * 3
        vignette_draw.rectangle([offset, offset, WIDTH - offset, HEIGHT - offset],
                                fill=None, outline=(0, 0, 0, alpha))

    img = Image.alpha_composite(img, vignette)

    # Convert to RGB for final save
    final = Image.new('RGB', (WIDTH, HEIGHT), BACKGROUND)
    final.paste(img, (0, 0), img)

    return final

# Create and save
print("Creating plant light sculpture artwork...")
artwork = create_plant_sculpture()
output_path = "/sessions/optimistic-modest-curie/mnt/obsidianVault/elisava/slides/images/final_project_example.png"
artwork.save(output_path, "PNG", quality=95)
print(f"Saved to {output_path}")
