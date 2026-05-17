from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

SIZE = 1024
OFF = -80  # shift cat up to give it more space

img = Image.new("RGB", (SIZE, SIZE))
draw = ImageDraw.Draw(img)

# Background gradient — deep navy to purple
for y in range(SIZE):
    ratio = y / SIZE
    r = int(18  + (45  - 18)  * ratio)
    g = int(18  + (10  - 18)  * ratio)
    b = int(60  + (90  - 60)  * ratio)
    draw.line([(0, y), (SIZE, y)], fill=(r, g, b))

# Soft glow circle behind cat
glow = Image.new("RGB", (SIZE, SIZE), (0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([180, 100 + OFF, 840, 780 + OFF], fill=(80, 50, 160))
glow = glow.filter(ImageFilter.GaussianBlur(radius=100))
img = Image.blend(img, glow, alpha=0.5)
draw = ImageDraw.Draw(img)

def o(y): return y + OFF  # offset helper

# ── CAT BODY ──────────────────────────────────────────────
draw.ellipse([280, o(530), 740, o(870)], fill=(255, 200, 120))
draw.ellipse([350, o(600), 670, o(840)], fill=(255, 230, 180))

# ── TAIL ──────────────────────────────────────────────────
for i in range(60):
    t = i / 60
    angle = math.pi * (0.1 + t * 0.7)
    cx = 700 + int(140 * math.cos(angle) * (1 - t * 0.3))
    cy = o(840) - int(120 * math.sin(angle) * (1 - t * 0.2))
    r = max(4, 20 - int(t * 15))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(230, 160, 60))

# ── HEAD ──────────────────────────────────────────────────
draw.ellipse([310, o(300), 710, o(580)], fill=(255, 200, 120))
draw.ellipse([295, o(460), 400, o(550)], fill=(255, 215, 140))
draw.ellipse([620, o(460), 725, o(550)], fill=(255, 215, 140))

# ── EARS ──────────────────────────────────────────────────
draw.polygon([(330, o(350)), (270, o(230)), (420, o(330))], fill=(255, 190, 100))
draw.polygon([(340, o(345)), (295, o(260)), (410, o(335))], fill=(255, 140, 140))
draw.polygon([(690, o(350)), (750, o(230)), (600, o(330))], fill=(255, 190, 100))
draw.polygon([(680, o(345)), (725, o(260)), (610, o(335))], fill=(255, 140, 140))

# ── FACE ──────────────────────────────────────────────────
# Eyes
draw.ellipse([368, o(390), 448, o(470)], fill=(60, 40, 20))
draw.ellipse([570, o(390), 650, o(470)], fill=(60, 40, 20))
draw.ellipse([370, o(392), 446, o(468)], fill=(80, 200, 180))
draw.ellipse([572, o(392), 648, o(468)], fill=(80, 200, 180))
draw.ellipse([390, o(408), 428, o(452)], fill=(10, 10, 10))
draw.ellipse([592, o(408), 630, o(452)], fill=(10, 10, 10))
draw.ellipse([396, o(411), 408, o(423)], fill=(255, 255, 255))
draw.ellipse([598, o(411), 610, o(423)], fill=(255, 255, 255))

# Nose
draw.polygon([(510, o(490)), (495, o(510)), (525, o(510))], fill=(255, 120, 140))
# Mouth
draw.arc([486, o(504), 516, o(524)], start=0, end=180, fill=(180, 80, 100), width=3)
draw.arc([516, o(504), 546, o(524)], start=0, end=180, fill=(180, 80, 100), width=3)

# Whiskers
for side in [-1, 1]:
    bx = 510 + side * 10
    for wy in [o(492), o(505), o(518)]:
        ex = bx + side * 130
        draw.line([(bx, wy), (ex, wy - side * 5)], fill=(255, 240, 200), width=2)

# ── STRIPES ───────────────────────────────────────────────
for sx, sy, ex, ey in [
    (400, o(320), 430, o(360)), (450, o(308), 470, o(348)), (500, o(304), 515, o(344)),
]:
    draw.line([(sx, sy), (ex, ey)], fill=(220, 160, 80), width=5)

# ── BOOK ──────────────────────────────────────────────────
bx, by = 320, o(700)
bw, bh = 380, 220

draw.rectangle([bx + 10, by + 10, bx + bw + 10, by + bh + 10], fill=(20, 10, 50))
draw.rectangle([bx, by, bx + bw // 2, by + bh], fill=(245, 235, 210))
draw.rectangle([bx + bw // 2, by, bx + bw, by + bh], fill=(255, 248, 230))
draw.rectangle([bx + bw // 2 - 6, by, bx + bw // 2 + 6, by + bh], fill=(180, 100, 60))
draw.rectangle([bx - 8, by - 10, bx + bw + 8, by + 12], fill=(180, 100, 60))
draw.rectangle([bx - 8, by + bh - 12, bx + bw + 8, by + bh + 10], fill=(180, 100, 60))

for i in range(5):
    ly = by + 35 + i * 30
    draw.rectangle([bx + 18, ly, bx + bw // 2 - 18, ly + 9], fill=(180, 160, 130))
    draw.rectangle([bx + bw // 2 + 18, ly, bx + bw - 18, ly + 9], fill=(180, 160, 130))

# Paws
draw.ellipse([278, o(760), 358, o(830)], fill=(255, 200, 120))
draw.ellipse([660, o(760), 740, o(830)], fill=(255, 200, 120))

# ── APP NAME ──────────────────────────────────────────────
win_fonts = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
font_path = os.path.join(win_fonts, "arialbd.ttf")
try:
    font_name = ImageFont.truetype(font_path, 100)
except:
    font_name = ImageFont.load_default()

draw.text((SIZE // 2 + 4, 968), "NUMPER", font=font_name, fill=(0, 0, 0), anchor="mm")
draw.text((SIZE // 2, 964), "NUMPER", font=font_name, fill=(255, 220, 100), anchor="mm")

img.save("app_icon.png", format="PNG")
print("Saved: app_icon.png  (1024x1024)")
