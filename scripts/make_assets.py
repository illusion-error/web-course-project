"""Generate favicon, app icon and OG cover (programmatic, soft lavender palette, English only)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)

VIOLET = (101, 86, 152)
ROSE = (189, 98, 138)
INK = (48, 52, 81)
MUTED = (98, 103, 129)
PAPER = (251, 250, 255)
MOON = (255, 244, 229)
STAR = (255, 246, 223)
BG_TOP = (238, 239, 248)
BG_BOT = (246, 233, 241)

SEGOE_BOLD = r'C:\Windows\Fonts\segoeuib.ttf'
SEGOE = r'C:\Windows\Fonts\segoeui.ttf'
SEGOE_LIGHT = r'C:\Windows\Fonts\segoeuil.ttf'
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


def make_og_cover():
    W, H = 1200, 630
    img = vgradient(W, H, BG_TOP, BG_BOT).convert('RGBA')

    # decorative moon on the right
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    mc = (930, 250)
    mr = 150
    gd.ellipse([mc[0] - mr * 1.5, mc[1] - mr * 1.5, mc[0] + mr * 1.5, mc[1] + mr * 1.5],
               fill=(101, 86, 152, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)
    d.ellipse([mc[0] - mr, mc[1] - mr, mc[0] + mr, mc[1] + mr], fill=MOON)

    # rolling hills below the copy block
    d.polygon([(0, H), (0, 520), (220, 450), (430, 520), (640, 440), (860, 520),
               (1080, 460), (W, 510), (W, H)], fill=(101, 86, 152, 38))
    d.polygon([(0, H), (0, 560), (260, 510), (520, 570), (780, 510), (1040, 570), (W, 530), (W, H)],
              fill=(69, 75, 119, 45))
    four_point_star(d, 820, 150, 26, VIOLET)
    four_point_star(d, 1040, 360, 18, ROSE)

    f_eyebrow = ImageFont.truetype(SEGOE_BOLD, 27)
    f_title = ImageFont.truetype(GEORGIA_BOLD, 72)
    f_desc = ImageFont.truetype(GEORGIA, 28)

    spaced_text(d, (96, 160), 'AN EVENING, A STORY', f_eyebrow, VIOLET, tracking=10)
    # short rose rule beneath the eyebrow
    d.rectangle([98, 212, 168, 218], fill=ROSE)
    d.text((94, 240), 'Anime Tonight', font=f_title, fill=INK)
    d.text((98, 360), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MUTED)
    d.text((98, 402), 'matched to your mood.', font=f_desc, fill=MUTED)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=88)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
