"""Generate favicon, app icon and OG cover: soft lavender rooftop night (English only)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / 'site/assets/icons'
ICON_DIR.mkdir(parents=True, exist_ok=True)
BG_PATH = ROOT / 'scripts' / 'assets' / 'bg-moonbranch.png'

VIOLET = (117, 100, 163)
ROSE = (201, 122, 156)
INK = (54, 52, 84)
MUTED = (110, 108, 138)
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


def cover_fit(im, W, H):
    w, h = im.size
    target = W / H
    cur = w / h
    if cur > target:
        nw = int(h * target)
        left = (w - nw) // 2
        im = im.crop((left, 0, left + nw, h))
    else:
        nh = int(w / target)
        top = (h - nh) // 2
        im = im.crop((0, top, w, top + nh))
    return im.resize((W, H), Image.LANCZOS)


def make_og_cover():
    W, H = 1200, 630
    bg = Image.open(BG_PATH).convert('RGB')
    bg = cover_fit(bg, W, H)
    img = bg.convert('RGBA')

    # gentle left wash for copy legibility, keeping the illustration on the right
    wash = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(wash)
    wd.rectangle([0, 0, 500, H], fill=(251, 250, 255, 90))
    wash = wash.filter(ImageFilter.GaussianBlur(40))
    img.alpha_composite(wash)

    d = ImageDraw.Draw(img)
    f_eyebrow = ImageFont.truetype(SEGOE_BOLD, 24)
    f_title = ImageFont.truetype(GEORGIA_BOLD, 64)
    f_desc = ImageFont.truetype(GEORGIA, 28)

    spaced_text(d, (96, 136), 'AN EVENING, A STORY', f_eyebrow, VIOLET, tracking=4)
    d.ellipse([98, 192, 112, 206], fill=ROSE)
    d.ellipse([124, 192, 138, 206], fill=VIOLET)
    d.text((94, 224), 'Anime', font=f_title, fill=INK)
    d.text((94, 304), 'Tonight', font=f_title, fill=INK)
    d.text((98, 410), 'Twenty spoiler-free anime picks,', font=f_desc, fill=MUTED)
    d.text((98, 452), 'matched to your mood.', font=f_desc, fill=MUTED)

    return img.convert('RGB')


make_icon(32).save(ICON_DIR / 'favicon-32.png', 'PNG')
make_icon(180).save(ICON_DIR / 'apple-touch-icon.png', 'PNG')
make_og_cover().save(ICON_DIR / 'og-cover.jpg', 'JPEG', quality=90)
print('Generated icons:', [p.name for p in ICON_DIR.iterdir()])
