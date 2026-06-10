from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, random

W, H = 1080, 1350
FONT_DIR = "/home/user/pixellabweb/assets/fonts/"
OUT = "/home/user/pixellabweb/assets/carousel/"
os.makedirs(OUT, exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def f(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def spaced(draw, pos, text, fnt, fill, sp=3):
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += fnt.getlength(ch) + sp

def grain(img, strength=0.15):
    random.seed(7)
    g = img.copy(); px = g.load()
    for yy in range(H):
        for xx in range(W):
            v = random.randint(-8, 8)
            r, gb, b = img.getpixel((xx, yy))
            px[xx, yy] = (max(0,min(255,r+v)), max(0,min(255,gb+v)), max(0,min(255,b+v)))
    return Image.blend(img, g, strength)

def warm_glow(img, cx, cy, layers):
    g = Image.new("RGB", (W, H), img.getpixel((0,0)))
    d = ImageDraw.Draw(g)
    for rx, ry, col in layers:
        d.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=col)
    return Image.blend(img, g.filter(ImageFilter.GaussianBlur(90)), 0.88)

def footer(draw, y=H-72):
    fb = f("Montserrat-Bold-static.ttf", 14)
    fl = f("Montserrat-Light-static.ttf", 14)
    spaced(draw, (M, y), "PIXELLAB", fb, (61,79,53,200), sp=2)
    draw.text((M + fb.getlength("PIXELLAB") + 16, y), ".AR", font=fl, fill=(61,79,53,130))

def slide_num(draw, n, ambient, col=(255,255,255,60)):
    fn = f("Montserrat-Bold-static.ttf", 12)
    spaced(draw, (M, 72), f"0{n}  ·  {ambient}", fn, col, sp=2)

def divider(draw, y, color=(61,79,53,220), w=2, h=72):
    draw.rectangle([M, y, M+w, y+h], fill=color)

def save(img, name):
    img.convert("RGB").save(f"{OUT}{name}.jpg", "JPEG", quality=95, subsampling=0)
    print(f"  ✓ {name}")

M = 72  # left margin
WHITE     = (255,255,255,255)
WHITE_60  = (255,255,255,150)
WHITE_30  = (255,255,255,75)
GREEN     = (61,79,53,255)
TERRA     = (160,96,74,255)

# ── SLIDE 1 — PORTADA ────────────────────────────────────────────────────────
def s1():
    img = Image.new("RGB", (W, H), (26,26,26))
    img = warm_glow(img, W//2, int(H*0.74), [
        (750,580,(40,22,8)), (520,400,(85,44,14)),
        (320,245,(148,76,22)), (170,130,(210,115,36)),
        (72,55,(252,180,58)), (24,18,(255,228,120)),
    ])
    img = grain(img)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)

    # header
    fh = f("Montserrat-Bold-static.ttf", 14)
    spaced(d, (M, 72), "PIXELLAB.AR  ·  DISEÑO & FABRICACIÓN", fh, (61,79,53,200), sp=2)
    d.rectangle([M, 72+20, M+80, 72+21], fill=GREEN)

    # headline
    fblk = f("Montserrat-Black-static.ttf", 128)
    flgt = f("Montserrat-Light-static.ttf", 128)
    y0 = 165
    LH = 142
    d.text((M, y0),      "UNA",        font=fblk, fill=WHITE)
    d.text((M, y0+LH),   "LÁMPARA,",   font=fblk, fill=WHITE)
    d.text((M, y0+LH*2), "CINCO",      font=flgt, fill=WHITE_30)
    d.text((M, y0+LH*3), "AMBIENTES.", font=fblk, fill=WHITE)

    # product tag
    ty = y0 + LH*4 + 18
    divider(d, ty)
    fp = f("Montserrat-Light-static.ttf", 22)
    d.text((M+20, ty+6),  "Cáliz Blanco", font=fp, fill=WHITE_60)
    d.text((M+20, ty+38), "Diseñada y fabricada en Buenos Aires.", font=f("Montserrat-Light-static.ttf",16), fill=WHITE_30)

    footer(d)
    save(img, "slide-01-portada")

# ── SLIDE 2 — LIVING (AI photo placeholder) ──────────────────────────────────
def s2():
    # Atmospheric terracotta — will be replaced with real AI photo
    img = Image.new("RGB", (W, H), (42,18,8))
    glow = Image.new("RGB", (W, H), (42,18,8))
    gd = ImageDraw.Draw(glow)
    for rx, ry, col in [
        (680,520,(90,38,10)), (460,350,(165,80,18)),
        (260,200,(220,118,30)), (100,76,(255,175,60)),
        (34,26,(255,220,110)),
    ]:
        gd.ellipse([W//2-rx, int(H*0.62)-ry, W//2+rx, int(H*0.62)+ry], fill=col)
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(100)), 0.92)
    img = grain(img, 0.20)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)

    slide_num(d, 1, "LIVING NOCTURNO", (255,255,255,80))

    fblk = f("Montserrat-Black-static.ttf", 96)
    flgt = f("Montserrat-Light-static.ttf", 30)

    d.text((M, H-420), "LIVING", font=fblk, fill=WHITE)
    d.text((M, H-420+108), "NOCTURNO.", font=fblk, fill=WHITE)

    divider(d, H-280, (160,96,74,200))
    d.text((M+20, H-274), "Para los que disfrutan", font=flgt, fill=WHITE_60)
    d.text((M+20, H-236), "la noche en casa.", font=flgt, fill=WHITE_60)

    # placeholder note (small, hidden once photo is added)
    fn = f("Montserrat-Light-static.ttf", 13)
    d.text((M, H-120), "★ Reemplazar con foto AI del Living", font=fn, fill=(255,255,255,35))

    footer(d)
    save(img, "slide-02-living")

# ── SLIDES 3-6 — GRAPHIC ─────────────────────────────────────────────────────
AMBIENTES = [
    # (num, label, bg_color, accent, headline_l1, headline_l2, copy_l1, copy_l2)
    (2, "DORMITORIO",   (18,20,28),    (100,115,160,200),
     "DORMI-", "TORIO.", "Tu mesita de noche", "nunca tuvo tanto carácter."),
    (3, "ESCRITORIO",   (24,16,8),     (160,96,74,200),
     "ESCRI-",  "TORIO.", "Porque crear", "también se ilumina."),
    (4, "LECTURA",      (20,30,20),    (61,79,53,220),
     "RINCÓN", "LECTOR.", "Un rincón, una lámpara,", "mil historias."),
    (5, "TERRAZA",      (10,10,12),    (255,255,255,60),
     "TERRA-",  "ZA.", "La noche afuera.", "La luz, tuya."),
]

def make_graphic(n, label, bg, accent, h1, h2, c1, c2):
    img = Image.new("RGB", (W, H), bg)

    # subtle radial warmth in lower area
    glow = Image.new("RGB", (W, H), bg)
    gd = ImageDraw.Draw(glow)
    r, g, b = bg
    warm = (min(255,r+30), min(255,g+18), min(255,b+8))
    gd.ellipse([W//2-400, H-600, W//2+400, H+100], fill=warm)
    img = Image.blend(img, glow.filter(ImageFilter.GaussianBlur(120)), 0.6)
    img = grain(img, 0.12)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)

    slide_num(d, n, label, (255,255,255,65))

    fblk = f("Montserrat-Black-static.ttf", 112)
    flgt = f("Montserrat-Light-static.ttf", 28)

    d.text((M, H-450), h1, font=fblk, fill=WHITE)
    d.text((M, H-450+125), h2, font=fblk, fill=WHITE)

    divider(d, H-290, accent)
    d.text((M+20, H-283), c1, font=flgt, fill=WHITE_60)
    d.text((M+20, H-247), c2, font=flgt, fill=WHITE_60)

    footer(d)
    save(img, f"slide-0{n+2}-{label.lower()}")

# ── SLIDE 7 — CTA ────────────────────────────────────────────────────────────
def s7():
    img = Image.new("RGB", (W, H), (22,22,22))
    img = warm_glow(img, W//2, int(H*0.5), [
        (600,460,(50,24,8)), (380,290,(100,50,15)),
        (200,150,(155,80,22)), (80,60,(200,110,32)),
    ])
    img = grain(img, 0.18)
    img = img.convert("RGBA")
    d = ImageDraw.Draw(img)

    # header
    fh = f("Montserrat-Bold-static.ttf", 14)
    spaced(d, (M, 72), "PIXELLAB.AR  ·  OFERTA PRIMERA COMPRA", fh, (61,79,53,190), sp=2)
    d.rectangle([M, 72+20, M+80, 72+21], fill=GREEN)

    # Big CTA headline
    fblk = f("Montserrat-Black-static.ttf", 128)
    flgt = f("Montserrat-Light-static.ttf", 128)
    fbld = f("Montserrat-Bold-static.ttf", 32)
    flit = f("Montserrat-Light-static.ttf", 28)

    y0 = 200
    d.text((M, y0),      "PRIMERA", font=fblk, fill=WHITE)
    d.text((M, y0+142),  "COMPRA.", font=fblk, fill=WHITE)

    # Discount line
    d.text((M, y0+310), "Descuento especial.", font=fbld, fill=TERRA)

    # Divider + body
    divider(d, y0+380)
    d.text((M+20, y0+385), "Visitá pixellab.ar", font=flit, fill=WHITE_60)
    d.text((M+20, y0+423), "y elegí la tuya.", font=flit, fill=WHITE_60)

    # URL highlight
    fu = f("Montserrat-Bold-static.ttf", 26)
    uy = y0 + 510
    d.text((M, uy), "→ pixellab.ar", font=fu, fill=TERRA)

    footer(d)
    save(img, "slide-07-cta")

# ── RUN ALL ──────────────────────────────────────────────────────────────────
print(f"Generating carousel — {W}×{H}px (4:5)")
s1()
s2()
for args in AMBIENTES:
    make_graphic(*args)
s7()
print(f"\nAll slides saved to {OUT}")
