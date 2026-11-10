"""Generate favicon, app icon and OG cover for the static site (stdlib + Pillow)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)

# High-contrast night palette
BG_TOP = (24, 21, 48)
BG_BOT = (40, 34, 74)
MOON = (255, 241, 216)
MOON_LOW = (246, 220, 176)
GOLD = (242, 184, 107)
CORAL = (233, 124, 146)
WHITE = (255, 255, 255)
MIST = (216, 212, 234)
HILL_FAR = (64, 54, 100, 170)
HILL_NEAR = (18, 15, 34, 238)
ICON_BG = (28, 25, 55)

YAHEI_BOLD = r'C:\Windows\Fonts\msyhbd.ttc'
GEORGIA_BOLD = r'C:\Windows\Fonts\georgiab.ttf'
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
    d.ellipse([c1[0] - r1, c1[1] - r1, c1[0] + r1, c1[1] + r1], fill=MOON)
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


def moon_ball(r):
    size = 2 * r
    ball = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    px = ball.load()
    for y in range(size):
        t = y / max(1, size - 1)
        row = tuple(int(MOON[i] + (MOON_LOW[i] - MOON[i]) * t) for i in range(3))
        for x in range(size):
            px[x, y] = row + (255,)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    ball.putalpha(mask)
    return ball


def make_og_cover():
    W, H = 1200, 630
    img = vgradient(W, H, BG_TOP, BG_BOT).convert('RGBA')

    # large moon with layered glow (focal point, right side)
    mc = (905, 248)
    mr = 150
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([mc[0] - mr * 2.1, mc[1] - mr * 2.1, mc[0] + mr * 2.1, mc[1] + mr * 2.1],
               fill=(242, 184, 107, 42))
    glow = glow.filter(ImageFilter.GaussianBlur(52))
    img.alpha_composite(glow)
    glow2 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(glow2)
    gd2.ellipse([mc[0] - mr * 1.35, mc[1] - mr * 1.35, mc[0] + mr * 1.35, mc[1] + mr * 1.35],
                fill=(255, 240, 214, 70))
    glow2 = glow2.filter(ImageFilter.GaussianBlur(22))
    img.alpha_composite(glow2)
    img.alpha_composite(moon_ball(mr), (mc[0] - mr, mc[1] - mr))
    d = ImageDraw.Draw(img)
    d.ellipse([mc[0] - mr * 0.55, mc[1] - mr * 0.22, mc[0] - mr * 0.18, mc[1] + mr * 0.12],
              fill=(228, 198, 150, 55))
    d.ellipse([mc[0] + mr * 0.08, mc[1] + mr * 0.28, mc[0] + mr * 0.34, mc[1] + mr * 0.52],
              fill=(228, 198, 150, 45))

    # stars with varied weight
    dots = [(150, 118, 3), (300, 92, 2), (520, 150, 3), (700, 96, 2), (1085, 150, 3),
            (1120, 300, 2), (860, 320, 2), (430, 236, 2), (250, 300, 2)]
    for x, y, r in dots:
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 246, 228, 200))
    four_point_star(d, 780, 150, 26, GOLD)
    four_point_star(d, 1055, 350, 18, CORAL)

    # dark hill silhouettes along the bottom
    round_hills(img, [(-150, 870, 340), (350, 890, 300), (800, 870, 360), (1250, 890, 320)],
                HILL_FAR)
    round_hills(img, [(100, 930, 360), (600, 940, 340), (1120, 930, 380)], HILL_NEAR)

    f_eyebrow = ImageFont.truetype(SEGOE_SEMI, 27)
    f_title = ImageFont.truetype(YAHEI_BOLD, 92)
    f_en = ImageFont.truetype(GEORGIA_BOLD, 44)
    f_desc = ImageFont.truetype(SEGOE_LIGHT, 28)

    spaced_text(d, (100, 146), 'AN EVENING, A STORY', f_eyebrow, GOLD, tracking=10)
    d.text((96, 198), '今晚看什么', font=f_title, fill=WHITE)
    d.text((102, 322), 'Anime Tonight', font=f_en, fill=CORAL)
    d.text((100, 404), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MIST)
    d.text((100, 446), 'matched to your mood.', font=f_desc, fill=MIST)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=90)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
