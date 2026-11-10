"""Generate favicon, app icon and OG cover over the AI night background."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)
BG_PATH = ROOT / 'scripts/assets/bg-night.png'

# Site brand palette
INK = (48, 52, 81)
MUTED = (98, 103, 129)
VIOLET = (101, 86, 152)
ROSE = (189, 98, 138)
PAPER = (251, 250, 255)

YAHEI_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'
GEORGIA = r'C:\Windows\Fonts\georgia.ttf'
GEORGIA_BOLD = r'C:\Windows\Fonts\georgiab.ttf'
SEGOE_SEMI = r'C:\Windows\Fonts\seguisb.ttf'


def four_point_star(draw, cx, cy, r, color):
    draw.polygon([(cx, cy - r), (cx + r * 0.28, cy - r * 0.28), (cx + r, cy),
                  (cx + r * 0.28, cy + r * 0.28), (cx, cy + r), (cx - r * 0.28, cy + r * 0.28),
                  (cx - r, cy), (cx - r * 0.28, cy - r * 0.28)], fill=color)


def spaced_text(draw, xy, text, font, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking


def make_icon(size):
    base = Image.new('RGBA', (size, size), PAPER + (255,))
    d = ImageDraw.Draw(base)
    c1 = (size * 0.64, size * 0.38)
    r1 = size * 0.30
    d.ellipse([c1[0] - r1, c1[1] - r1, c1[0] + r1, c1[1] + r1], fill=VIOLET)
    c2 = (size * 0.74, size * 0.30)
    r2 = size * 0.27
    d.ellipse([c2[0] - r2, c2[1] - r2, c2[0] + r2, c2[1] + r2], fill=PAPER + (255,))
    four_point_star(d, size * 0.30, size * 0.68, size * 0.11, ROSE)
    return base


def make_og_cover():
    W, H = 1200, 630
    if BG_PATH.exists():
        img = Image.open(BG_PATH).convert('RGBA').resize((W, H), Image.LANCZOS)
    else:
        img = Image.new('RGBA', (W, H), (156, 157, 201, 255))

    # light left scrim so the copy stays legible over the misty sky
    scrim = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = int(150 * max(0, 1 - x / (W * 0.7)))
        sd.line([(x, 0), (x, H)], fill=(247, 243, 252, a))
    img.alpha_composite(scrim)

    d = ImageDraw.Draw(img)
    f_eyebrow = ImageFont.truetype(SEGOE_SEMI, 26)
    f_title = ImageFont.truetype(YAHEI_BOLD, 86)
    f_en = ImageFont.truetype(GEORGIA_BOLD, 40)
    f_desc = ImageFont.truetype(GEORGIA, 27)

    spaced_text(d, (96, 146), 'AN EVENING, A STORY', f_eyebrow, VIOLET, tracking=10)
    d.text((92, 196), '今晚看什么', font=f_title, fill=INK)
    d.text((100, 316), 'Anime Tonight', font=f_en, fill=ROSE)
    d.text((98, 400), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MUTED)
    d.text((98, 442), 'matched to your mood.', font=f_desc, fill=MUTED)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=90)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
