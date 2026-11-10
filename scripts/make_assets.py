"""Generate favicon, app icon and OG cover for the static site (stdlib + Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)

# Soft fog-night palette (blue-grey violet, no muddy rose)
NIGHT_TOP = (43, 51, 80)
NIGHT_MID = (86, 94, 134)
NIGHT_BOT = (154, 143, 174)
CREAM = (255, 244, 228)
GOLD = (233, 201, 160)
ROSE_SOFT = (239, 199, 210)
MIST = (205, 208, 228)
ICON_BG = (43, 51, 80)

YAHEI_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'
YAHEI = r'C:\Windows\Fonts\msyh.ttc'
GEORGIA_ITALIC = r'C:\Windows\Fonts\georgiai.ttf'
SEGOE_LIGHT = r'C:\Windows\Fonts\segoeuil.ttf'
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
    c1 = (size * 0.64, size * 0.38)
    r1 = size * 0.30
    d.ellipse([c1[0] - r1, c1[1] - r1, c1[0] + r1, c1[1] + r1], fill=CREAM)
    c2 = (size * 0.74, size * 0.30)
    r2 = size * 0.27
    d.ellipse([c2[0] - r2, c2[1] - r2, c2[0] + r2, c2[1] + r2], fill=ICON_BG + (255,))
    four_point_star(d, size * 0.30, size * 0.68, size * 0.11, GOLD)
    return base


def round_hills(img, circles, color):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for cx, cy, r in circles:
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    img.alpha_composite(layer)


def make_og_cover():
    W, H = 1200, 630
    img = vgradient(W, H, NIGHT_TOP, NIGHT_BOT).convert('RGBA')

    # moon glow + moon on the right
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    mc = (912, 210)
    mr = 115
    gd.ellipse([mc[0] - mr * 1.7, mc[1] - mr * 1.7, mc[0] + mr * 1.7, mc[1] + mr * 1.7],
               fill=(255, 238, 210, 55))
    glow = glow.filter(ImageFilter.GaussianBlur(44))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.ellipse([mc[0] - mr, mc[1] - mr, mc[0] + mr, mc[1] + mr], fill=CREAM)

    # scattered stars
    dots = [(150, 118, 3), (300, 92, 2), (520, 150, 3), (700, 96, 2), (1085, 150, 3),
            (1120, 280, 2), (860, 300, 2), (430, 236, 2), (250, 300, 2)]
    for x, y, r in dots:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 246, 228, 190))
    four_point_star(d, 790, 150, 22, GOLD)
    four_point_star(d, 1050, 330, 16, ROSE_SOFT)

    # rounded hill silhouettes kept along the bottom edge, clear of the copy
    round_hills(img, [(-150, 870, 340), (350, 890, 300), (800, 870, 360), (1250, 890, 320)],
                (70, 80, 116, 150))
    round_hills(img, [(100, 930, 360), (600, 940, 340), (1120, 930, 380)],
                (35, 42, 66, 220))

    f_eyebrow = ImageFont.truetype(SEGOE_SEMI, 27)
    f_title = ImageFont.truetype(YAHEI_BOLD, 88)
    f_en = ImageFont.truetype(GEORGIA_ITALIC, 46)
    f_desc = ImageFont.truetype(SEGOE_LIGHT, 28)

    spaced_text(d, (100, 140), 'AN EVENING, A STORY', f_eyebrow, GOLD, tracking=10)
    d.text((96, 192), '今晚看什么', font=f_title, fill=CREAM)
    d.text((102, 308), 'Anime Tonight', font=f_en, fill=ROSE_SOFT)
    d.text((100, 388), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MIST)
    d.text((100, 430), 'matched to your mood.', font=f_desc, fill=MIST)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=90)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
