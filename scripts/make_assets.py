"""Generate favicon, app icon and OG cover: soft lavender, cute and gentle (English only)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)

VIOLET = (117, 100, 163)
ROSE = (201, 122, 156)
INK = (54, 52, 84)
MUTED = (110, 108, 138)
PAPER = (251, 250, 255)
MOON = (255, 246, 232)
STAR = (255, 246, 223)
BG_TOP = (237, 235, 248)
BG_BOT = (251, 231, 239)

SEGOE_BOLD = r'C:\Windows\Fonts\segoeuib.ttf'
GEORGIA_BOLD = r'C:\Windows\Fonts\georgiab.ttf'
GEORGIA = r'C:\Windows\Fonts\georgia.ttf'


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
    base = vgradient(size, size, VIOLET, ROSE).convert('RGBA')
    d = ImageDraw.Draw(base)
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    mc = (size * 0.62, size * 0.38)
    mr = size * 0.26
    gd.ellipse([mc[0] - mr * 1.5, mc[1] - mr * 1.5, mc[0] + mr * 1.5, mc[1] + mr * 1.5],
               fill=(255, 244, 229, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.06))
    base.alpha_composite(glow)
    d = ImageDraw.Draw(base)
    d.ellipse([mc[0] - mr, mc[1] - mr, mc[0] + mr, mc[1] + mr], fill=MOON)
    four_point_star(d, size * 0.3, size * 0.66, size * 0.1, STAR)
    return base


def smooth_hills(img, circles, color):
    layer = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for cx, cy, r in circles:
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    img.alpha_composite(layer)


def make_og_cover():
    W, H = 1200, 630
    img = vgradient(W, H, BG_TOP, BG_BOT).convert('RGBA')

    # soft clouds, kept away from the copy block
    clouds = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(clouds)
    cd.ellipse([720, 330, 1180, 395], fill=(255, 255, 255, 50))
    clouds = clouds.filter(ImageFilter.GaussianBlur(18))
    img.alpha_composite(clouds)

    # cute moon with layered glow and blush
    mc = (930, 238)
    mr = 138
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([mc[0] - mr * 1.7, mc[1] - mr * 1.7, mc[0] + mr * 1.7, mc[1] + mr * 1.7],
               fill=(226, 196, 220, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(36))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.ellipse([mc[0] - mr, mc[1] - mr, mc[0] + mr, mc[1] + mr], fill=MOON)

    # rounded hills along the bottom
    smooth_hills(img, [(-150, 860, 320), (350, 880, 290), (820, 860, 340), (1260, 880, 310)],
                 (150, 138, 190, 120))
    smooth_hills(img, [(100, 930, 340), (600, 940, 320), (1120, 930, 360)],
                 (110, 100, 155, 150))

    # sparkles: dots plus four-point stars
    for x, y, r in [(180, 120, 3), (360, 96, 2), (700, 110, 2), (1060, 130, 3), (1120, 300, 2)]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=STAR + (220,))
    four_point_star(d, 815, 150, 24, VIOLET)
    four_point_star(d, 1045, 350, 16, ROSE)

    f_eyebrow = ImageFont.truetype(SEGOE_BOLD, 27)
    f_title = ImageFont.truetype(GEORGIA_BOLD, 72)
    f_desc = ImageFont.truetype(GEORGIA, 28)

    spaced_text(d, (96, 158), 'AN EVENING, A STORY', f_eyebrow, VIOLET, tracking=10)
    d.ellipse([98, 214, 112, 228], fill=ROSE)
    d.ellipse([124, 214, 138, 228], fill=VIOLET)
    d.text((94, 240), 'Anime Tonight', font=f_title, fill=INK)
    d.text((98, 360), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MUTED)
    d.text((98, 402), 'matched to your mood.', font=f_desc, fill=MUTED)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=90)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
