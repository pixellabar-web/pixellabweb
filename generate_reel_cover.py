from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os, random

W, H = 1080, 1920
FONT_DIR = "/home/user/pixellabweb/assets/fonts/"

def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

def spaced(draw, pos, text, f, fill, spacing=4):
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += f.getlength(ch) + spacing

# ────────────────────────────────────────────────────────────────
# 1. BACKGROUND — deep charcoal
# ────────────────────────────────────────────────────────────────
img = Image.new("RGB", (W, H), (26, 26, 26))

# ────────────────────────────────────────────────────────────────
# 2. WARM GLOW — simulates the amber lamp
#    Center placed in lower-half so the upper text area stays dark
# ────────────────────────────────────────────────────────────────
GX, GY = W // 2, 1310   # glow center

glow = Image.new("RGB", (W, H), (26, 26, 26))
gd = ImageDraw.Draw(glow)

for (rx, ry, col) in [
    (980, 740, (38, 22, 8)),
    (750, 560, (72, 38, 12)),
    (530, 390, (130, 66, 18)),
    (350, 255, (190, 100, 28)),
    (200, 148, (230, 148, 50)),
    (100, 76, (252, 198, 80)),
    (42, 32, (255, 228, 140)),
    (14, 11, (255, 248, 210)),
]:
    gd.ellipse([GX-rx, GY-ry, GX+rx, GY+ry], fill=col)

glow = glow.filter(ImageFilter.GaussianBlur(radius=120))
img = Image.blend(img, glow, 0.94)

# Core bright point
core = Image.new("RGB", (W, H), (26, 26, 26))
cd = ImageDraw.Draw(core)
cd.ellipse([GX-28, GY-22, GX+28, GY+22], fill=(255, 248, 200))
core = core.filter(ImageFilter.GaussianBlur(radius=16))
img = Image.blend(img, core, 0.6)

# Subtle warm spill upward — creates depth
spill = Image.new("RGB", (W, H), (26, 26, 26))
sd = ImageDraw.Draw(spill)
sd.ellipse([GX-320, GY-700, GX+320, GY+200], fill=(55, 28, 8))
spill = spill.filter(ImageFilter.GaussianBlur(radius=160))
img = Image.blend(img, spill, 0.55)

# ────────────────────────────────────────────────────────────────
# 3. GRAIN — brand texture
# ────────────────────────────────────────────────────────────────
random.seed(99)
grn = img.copy()
grn_px = grn.load()
for yy in range(H):
    for xx in range(W):
        v = random.randint(-7, 7)
        r, g, b = img.getpixel((xx, yy))
        grn_px[xx, yy] = (
            max(0, min(255, r + v)),
            max(0, min(255, g + v)),
            max(0, min(255, b + v)),
        )
img = Image.blend(img, grn, 0.18)

# ────────────────────────────────────────────────────────────────
# 4. TYPE
# ────────────────────────────────────────────────────────────────
img = img.convert("RGBA")
draw = ImageDraw.Draw(img)

WHITE     = (255, 255, 255, 255)
WHITE_DIM = (255, 255, 255, 82)
GREEN     = (61, 79, 53, 255)
TERRA     = (160, 96, 74, 255)
AMBER     = (220, 148, 55, 255)

M = 80   # left margin

# — HEADER LABEL —
f_hdr = font("Montserrat-Bold-static.ttf", 17)
f_sub = font("Montserrat-Light-static.ttf", 12)
spaced(draw, (M, 88), "PIXELLAB.AR", f_hdr, GREEN, spacing=3)
draw.rectangle([M, 88+26, M+88, 88+27], fill=GREEN)
spaced(draw, (M, 88+40), "ILUMINACIÓN · DISEÑO 3D · BUENOS AIRES",
       f_sub, (255, 255, 255, 50), spacing=1.5)

# — HEADLINE —
f_blk = font("Montserrat-Black-static.ttf", 162)
f_lgt = font("Montserrat-Light-static.ttf", 162)

y0 = 220
LH = 178   # line-height

draw.text((M, y0),        "UNA",        font=f_blk, fill=WHITE)
draw.text((M, y0+LH),     "LUZ",        font=f_blk, fill=WHITE)
draw.text((M, y0+LH*2),   "PARA",       font=f_lgt, fill=WHITE_DIM)
draw.text((M, y0+LH*3),   "CADA",       font=f_lgt, fill=WHITE_DIM)
draw.text((M, y0+LH*4),   "AMBIENTE.",  font=f_blk, fill=WHITE)

# — VERTICAL RULE + TAGLINE —
ty = y0 + LH*5 + 20    # ≈ 1130
draw.rectangle([M, ty, M+2, ty+88], fill=GREEN)

f_tag = font("Montserrat-Light-static.ttf", 27)
draw.text((M+20, ty+8),  "Cada espacio tiene su luz.",           font=f_tag, fill=(255,255,255,145))
draw.text((M+20, ty+46), "Diseñadas y fabricadas en Argentina.", font=f_tag, fill=(255,255,255,145))

# — GLOW LABEL (floats near the light source) —
f_glo = font("Montserrat-Light-static.ttf", 20)
draw.text((M, GY - 80), "una luz.", font=f_glo, fill=(220, 168, 80, 90))

# — CTA (placeholder — reemplazar cuando el usuario confirme) —
f_cta  = font("Montserrat-Bold-static.ttf", 26)
f_ctax = font("Montserrat-Light-static.ttf", 18)
cy_cta = H - 195
draw.text((M, cy_cta),      "→ Ver colección",  font=f_cta,  fill=TERRA)
draw.text((M, cy_cta + 42), "pixellab.ar",       font=f_ctax, fill=(255,255,255,50))

# ────────────────────────────────────────────────────────────────
# 5. EXPORT
# ────────────────────────────────────────────────────────────────
out = img.convert("RGB")
path = "/home/user/pixellabweb/assets/reel-cover.jpg"
out.save(path, "JPEG", quality=96, subsampling=0)
print(f"✓ {path}  {W}×{H}px")
