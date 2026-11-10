"""Generate favicon, app icon and OG cover for the static site (stdlib + Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)

# Night palette
NIGHT_TOP = (36, 37, 64)
NIGHT_MID = (74, 58, 102)
NIGHT_BOT = (148, 84, 110)
CREAM = (255, 243, 220)
GOLD = (233, 202, 168)
ROSE_PINK = (242, 186, 206)
MIST = (217, 212, 232)
ICON_BG = (58, 51, 88)

YAHEI_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'
YAHEI = r'C:\Windows\Fonts\msyh.ttc'
GEORGIA_BOLD = r'C:\Windows\Fonts\georgiab.ttf'
GEORGIA = r'C:\Windows\Fonts\georgia.ttf'
SCRIPT = r'C:\Windows\Fonts\segoesc.ttf'
SEGOE_SEMI = r'C:\Windows\Fonts\seguisb.ttf'


def vgradient(w, h, top, bottom):
    img = Image.new('RGB', (w, h), top)
    px = img.load()
    for y in range(h):
        t = y / max(1, h - 1)
        row = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = row
    return img


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
    # crescent moon: cream circle, then offset background circle cuts a crescent
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
    img = vgradient(W, H, NIGHT_TOP, NIGHT_BOT).convert('RGBA')

    # moon glow + moon on the right
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    mc = (915, 232)
    mr = 132
    gd.ellipse([mc[0] - mr * 1.7, mc[1] - mr * 1.7, mc[0] + mr * 1.7, mc[1] + mr * 1.7],
               fill=(255, 236, 205, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(42))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.ellipse([mc[0] - mr, mc[1] - mr, mc[0] + mr, mc[1] + mr], fill=CREAM)

    # scattered stars (fixed positions)
    dots = [(150, 118, 3), (300, 92, 2), (520, 150, 3), (700, 96, 2), (1085, 150, 3),
            (1120, 280, 2), (860, 320, 2), (430, 236, 2), (250, 300, 2)]
    for x, y, r in dots:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 246, 228, 190))
    four_point_star(d, 790, 150, 24, GOLD)
    four_point_star(d, 1050, 350, 17, ROSE_PINK)

    # hill silhouettes
    d.polygon([(0, H), (0, 500), (220, 430), (430, 500), (640, 420), (860, 500),
               (1080, 440), (W, 490), (W, H)], fill=(70, 60, 100, 120))
    d.polygon([(0, H), (0, 556), (260, 505), (520, 566), (780, 505), (1040, 566), (W, 525), (W, H)],
              fill=(28, 28, 50, 200))

    f_eyebrow = ImageFont.truetype(SEGOE_SEMI, 28)
    f_title = ImageFont.truetype(YAHEI_BOLD, 90)
    f_script = ImageFont.truetype(SCRIPT, 60)
    f_desc = ImageFont.truetype(GEORGIA, 29)

    spaced_text(d, (100, 148), 'AN EVENING, A STORY', f_eyebrow, GOLD, tracking=10)
    d.text((96, 200), '今晚看什么', font=f_title, fill=CREAM)
    d.text((100, 312), 'Anime Tonight', font=f_script, fill=ROSE_PINK)
    d.text((100, 404), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MIST)
    d.text((100, 446), 'matched to your mood.', font=f_desc, fill=MIST)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=90)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
