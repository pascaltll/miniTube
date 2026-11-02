#!/usr/bin/env python3
"""Genera el arte de MiniTube para Steam (logo original, sin marcas de terceros).

Uso:  python tools/make_assets.py [carpeta_salida]      (por defecto: assets/)
Requiere Pillow (pip install pillow). Fuente: Poppins/Inter/DejaVu si existen; si no, la fuente por defecto de Pillow.
Salidas (tamaños recomendados por Steam para accesos directos que no son de Steam):
  capsule_portrait_600x900.png   cartel vertical de la biblioteca (Steam: "Portrait")
  capsule_wide_920x430.png       cápsula horizontal / "Wide Capsule"
  header_460x215.png             cabecera
  hero_1920x620.png              imagen grande del fondo (sin texto: el logo se superpone)
  logo_1280x720.png              logo con transparencia (se superpone sobre el hero)
  icon_512.png / icon.ico        icono (lanzador, escritorio, Steam)
"""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
BG0, BG1 = (13, 15, 30), (24, 22, 52)          # fondo azul noche
CY, VI = (34, 211, 238), (139, 92, 246)         # degradado cian -> violeta
SS = 4                                          # supersampling


def font(names, size):
    for n in names:
        for base in ("/usr/share/fonts/truetype/google-fonts/", "/usr/share/fonts/opentype/inter/", "/usr/share/fonts/truetype/dejavu/", ""):
            try:
                return ImageFont.truetype(base + n, size)
            except OSError:
                pass
    return ImageFont.load_default()


def grad(w, h, c0, c1, diag=True):
    g = Image.new("RGB", (w, h))
    px = g.load()
    for y in range(h):
        for x in range(w):
            t = (x / max(w - 1, 1) * 0.6 + y / max(h - 1, 1) * 0.4) if diag else y / max(h - 1, 1)
            px[x, y] = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
    return g


def rr_mask(w, h, r):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], r, fill=255)
    return m


def mark(size):
    """Marca: pantalla grande (borde en degradado) + tarjeta flotante con play + barrita de deslizar."""
    s = size * SS
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    # pantalla
    sw, sh = int(s * 0.80), int(s * 0.60)
    sx, sy = int(s * 0.06), int(s * 0.12)
    outer = rr_mask(sw, sh, int(s * 0.08))
    inner = Image.new("L", (sw, sh), 0)
    b = int(s * 0.025)
    ImageDraw.Draw(inner).rounded_rectangle([b, b, sw - 1 - b, sh - 1 - b], int(s * 0.06), fill=255)
    ring = Image.composite(Image.new("L", (sw, sh), 0), outer, inner)
    img.paste(grad(sw, sh, CY, VI), (sx, sy), ring)
    fill = Image.new("RGBA", (sw, sh), BG0 + (255,))
    img.paste(fill, (sx, sy), inner)
    ov = Image.new("RGBA", (s, s), (0, 0, 0, 0))   # capa de detalles semitransparentes (se compone, no se sobrescribe)
    d = ImageDraw.Draw(ov)
    # barrita de deslizar (gesto de minimizar)
    bw, bh = int(s * 0.16), int(s * 0.022)
    d.rounded_rectangle([sx + sw // 2 - bw // 2, sy + int(s * 0.05), sx + sw // 2 + bw // 2, sy + int(s * 0.05) + bh], bh // 2, fill=(255, 255, 255, 140))
    # filas de miniaturas dentro de la pantalla
    for i in range(3):
        x0 = sx + int(s * (0.10 + i * 0.20)); y0 = sy + int(s * 0.17)
        d.rounded_rectangle([x0, y0, x0 + int(s * 0.17), y0 + int(s * 0.10)], int(s * 0.015), fill=(255, 255, 255, 34))
    img = Image.alpha_composite(img, ov)
    # tarjeta mini flotante
    cw, ch = int(s * 0.46), int(s * 0.30)
    cx, cy = int(s * 0.46), int(s * 0.56)
    sh_img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    ImageDraw.Draw(sh_img).rounded_rectangle([cx + 6 * SS, cy + 10 * SS, cx + cw + 6 * SS, cy + ch + 10 * SS], int(s * 0.05), fill=(0, 0, 0, 150))
    img = Image.alpha_composite(img, sh_img.filter(ImageFilter.GaussianBlur(10 * SS)))
    img.paste(grad(cw, ch, CY, VI), (cx, cy), rr_mask(cw, ch, int(s * 0.05)))
    ov = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    tx, ty, tr = cx + cw // 2, cy + ch // 2, int(ch * 0.30)
    d.polygon([(tx - tr * 0.7, ty - tr), (tx - tr * 0.7, ty + tr), (tx + tr * 1.05, ty)], fill=(255, 255, 255, 245))
    img = Image.alpha_composite(img, ov)
    return img.resize((size, size), Image.LANCZOS)


def backdrop(w, h):
    bg = grad(w, h, BG0, BG1).convert("RGBA")
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse([w * 0.55, -h * 0.35, w * 1.25, h * 0.75], fill=CY + (46,))
    g.ellipse([-w * 0.25, h * 0.45, w * 0.50, h * 1.35], fill=VI + (52,))
    bg = Image.alpha_composite(bg, glow.filter(ImageFilter.GaussianBlur(min(w, h) // 5)))
    grid = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(grid)
    step = max(24, min(w, h) // 14)
    for x in range(0, w, step):
        d.line([(x, 0), (x, h)], fill=(255, 255, 255, 7))
    for y in range(0, h, step):
        d.line([(0, y), (w, y)], fill=(255, 255, 255, 7))
    return Image.alpha_composite(bg, grid)


def text_center(img, xy, txt, f, fill, anchor="mm"):
    ImageDraw.Draw(img).text(xy, txt, font=f, fill=fill, anchor=anchor)


def wordmark(size):
    f = font(["Poppins-Bold.ttf", "DejaVuSans-Bold.ttf"], size)
    f2 = font(["Poppins-Bold.ttf", "DejaVuSans-Bold.ttf"], size)
    return f, f2


def draw_title(img, cx, cy, size, with_tag=True, tag_size=None):
    f = font(["Poppins-Bold.ttf", "DejaVuSans-Bold.ttf"], size)
    d = ImageDraw.Draw(img)
    a, b = "Mini", "Tube"
    wa, wb = d.textlength(a, font=f), d.textlength(b, font=f)
    x0 = cx - (wa + wb) / 2
    d.text((x0, cy), a, font=f, fill=(255, 255, 255, 255), anchor="lm")
    tb = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(tb).text((x0 + wa, cy), b, font=f, fill=(255, 255, 255, 255), anchor="lm")
    bx = tb.getbbox()
    if bx:
        gm = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gm.paste(grad(bx[2] - bx[0], bx[3] - bx[1], CY, VI).crop((0, 0, bx[2] - bx[0], bx[3] - bx[1])), (bx[0], bx[1]), tb.split()[3].crop(bx))
        img.alpha_composite(gm)
    if with_tag:
        ft = font(["Poppins-Medium.ttf", "Inter-Medium.otf", "DejaVuSans.ttf"], tag_size or size // 3)
        ImageDraw.Draw(img).text((cx, cy + size * 0.82), "Mini reproductor para Steam", font=ft, fill=(200, 205, 225, 255), anchor="mm")


def save(img, name):
    p = os.path.join(OUT, name)
    img.save(p)
    print("→", p, img.size)


# icono
ic = mark(512)
base = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
plate = backdrop(512, 512)
base.paste(plate, (0, 0), rr_mask(512, 512, 110))
base.alpha_composite(ic.resize((440, 440), Image.LANCZOS), (36, 40))
save(base, "icon_512.png")
base.save(os.path.join(OUT, "icon.ico"), sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
# cartel vertical
w, h = 600, 900
im = backdrop(w, h)
im.alpha_composite(mark(460), (70, 150))
draw_title(im, w // 2, 700, 88, tag_size=30)
save(im, "capsule_portrait_600x900.png")
# cápsula horizontal y cabecera
for (w, h, name, ms, ts) in [(920, 430, "capsule_wide_920x430.png", 300, 92), (460, 215, "header_460x215.png", 150, 46)]:
    im = backdrop(w, h)
    im.alpha_composite(mark(ms), (int(w * 0.07), (h - ms) // 2))
    draw_title(im, int(w * 0.68), h // 2 - ts * 0.15, ts, tag_size=int(ts * 0.30))
    save(im, name)
# hero (sin texto)
w, h = 1920, 620
im = backdrop(w, h)
m = mark(560)
m.putalpha(m.split()[3].point(lambda a: int(a * 0.20)))
im.alpha_composite(m, (w - 700, 30))
im.alpha_composite(m.resize((380, 380), Image.LANCZOS), (120, 190))
save(im, "hero_1920x620.png")
# logo con transparencia
lg = Image.new("RGBA", (1280, 720), (0, 0, 0, 0))
lg.alpha_composite(mark(300), (150, 210))
draw_title(lg, 800, 360, 150, with_tag=False)
save(lg, "logo_1280x720.png")
