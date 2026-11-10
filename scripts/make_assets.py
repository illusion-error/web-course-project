"""Generate favicon, app icon and OG cover over the dark night background (English only)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)
BG_PATH = ROOT / 'scripts/assets/bg-night-dark.png'

# Dark-night brand palette
WHITE = (255, 255, 255)
CREAM = (255, 244, 229)
GOLD = (242, 201, 138)
ROSE = (232, 155, 180)
MIST = (216, 212, 234)
ICON_BG = (28, 25, 55)

GEORGIA = r'C:\Windows\Fonts\georgia.ttf'
GEORGIA_BOLD = r'C:\Windows\Fonts\georgiab.ttf'
SEGOE_SEMI = r'C:\Windows\Fonts\seguisb.ttf'
SEGOE_LIGHT = r'C:\Windows\Fonts\segoeuil.ttf'


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
    base = Image.new('RGBA', (size, size), ICON_BG + (255,))
    d = ImageDraw.Draw(base)
    c1 = (size * 0.64, size * 0.38)
    r1 = size * 0.30
    d.ellipse([c1[0] - r1, c1[1] - r1, c1[0] + r1, c1[1] + r1], fill=CREAM)
    c2 = (size * 0.74, size * 0.30)
    r2 = size * 0.27
    d.ellipse([c2[0] - r2, c2[1] - r2, c2[0] + r2, c2[1] + r2], fill=ICON_BG + (255,))
    four_point_star(d, size * 0.30, size * 0.68, size * 0.11, GOLD)
    return base


def make_og_cover():
    W, H = 1200, 630
    if BG_PATH.exists():
        img = Image.open(BG_PATH).convert('RGBA').resize((W, H), Image.LANCZOS)
    else:
        img = Image.new('RGBA', (W, H), (28, 25, 55, 255))

    # gentle left scrim to keep the light copy legible
    scrim = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(scrim)
    for x in range(W):
        a = int(90 * max(0, 1 - x / (W * 0.65)))
        sd.line([(x, 0), (x, H)], fill=(16, 13, 34, a))
    img.alpha_composite(scrim)

    d = ImageDraw.Draw(img)
    f_eyebrow = ImageFont.truetype(SEGOE_SEMI, 25)
    f_title = ImageFont.truetype(GEORGIA_BOLD, 74)
    f_desc = ImageFont.truetype(GEORGIA, 28)
    f_note = ImageFont.truetype(SEGOE_LIGHT, 19)

    spaced_text(d, (96, 168), 'AN EVENING, A STORY', f_eyebrow, GOLD, tracking=10)
    d.text((92, 218), 'Anime Tonight', font=f_title, fill=WHITE)
    d.text((98, 340), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MIST)
    d.text((98, 384), 'matched to your mood.', font=f_desc, fill=MIST)
    spaced_text(d, (98, 466), 'NO SPOILERS · JUST STORIES', f_note, GOLD, tracking=6)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=90)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
