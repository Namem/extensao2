"""
gen_icon.py — Gera ícone do app Ceres Diagnóstico (1024x1024)
Paleta Taxonomia Viva: forest_deep #1B5E20 / white
"""
import os, math
from PIL import Image, ImageDraw

SIZE  = 1024
OUT   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
SPLASH_OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "splash.png")

# ── Ícone principal ───────────────────────────────────────────────────────────
img  = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
draw = ImageDraw.Draw(img)

BG_DEEP  = (27,  94,  32)   # #1B5E20
BG_MID   = (46, 125,  50)   # #2E7D32
WHITE    = (255,255,255)
GREEN_LT = (200,230,201)

# Fundo circular
draw.ellipse([0,0,SIZE,SIZE], fill=BG_DEEP)

# Anel interno sutil
draw.ellipse([32,32,SIZE-32,SIZE-32], outline=BG_MID, width=8)

# ── Folha central ─────────────────────────────────────────────────────────────
cx, cy = SIZE//2, SIZE//2

def leaf(d, cx, cy, w, h, angle_deg, fill, vein_color, vein_w=4):
    """Desenha uma folha elíptica com nervura central."""
    import math
    a = math.radians(angle_deg)
    # Bounding box da folha (rotacionar manualmente é complexo; usar elipse simples)
    # Para rotação, desenhamos numa sub-imagem e colamos
    sub = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    sd  = ImageDraw.Draw(sub)
    # Elipse da folha
    sd.ellipse([cx-w//2, cy-h//2, cx+w//2, cy+h//2], fill=fill)
    # Nervura central
    sd.line([cx, cy-h//2+10, cx, cy+h//2-10], fill=vein_color, width=vein_w)
    # Nervuras laterais
    for i in range(-3, 4):
        oy = i*(h//2//4)
        sd.line([cx, cy+oy, cx+w//2-20, cy+oy-h//8], fill=vein_color, width=2)
        sd.line([cx, cy+oy, cx-w//2+20, cy+oy-h//8], fill=vein_color, width=2)
    # Rotacionar
    rotated = sub.rotate(-angle_deg, center=(cx,cy), expand=False)
    d._image.paste(rotated, mask=rotated)

# Sombra suave da folha principal
shadow = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
sd = ImageDraw.Draw(shadow)
sd.ellipse([cx-155, cy-255, cx+155, cy+255], fill=(0,0,0,60))
img.paste(Image.new("RGBA",(SIZE,SIZE),(0,0,0,0)), mask=shadow)

# Folha principal (vertical, levemente inclinada)
leaf(draw, cx, cy, 300, 510, 8, WHITE, GREEN_LT, 6)

# Pequena folha secundária (esquerda, inclinada)
leaf(draw, cx-95, cy+40, 160, 270, -28, GREEN_LT, BG_MID, 3)

# Haste
draw.line([cx+8, cy+240, cx+8, cy+340], fill=WHITE, width=10)
draw.ellipse([cx, cy+330, cx+16, cy+346], fill=WHITE)

# ── Salvar ícone ──────────────────────────────────────────────────────────────
# Converter para RGB com fundo sólido (launcher icons precisa de PNG RGBA ou RGB)
final = Image.new("RGB", (SIZE, SIZE), BG_DEEP)
final.paste(img, mask=img.split()[3])
final.save(OUT, "PNG")
print(f"Icon -> {OUT}")

# ── Splash (fundo simples verde com folha menor e centrada) ────────────────────
sp = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
sd2 = ImageDraw.Draw(sp)
leaf(sd2, SIZE//2, SIZE//2, 220, 370, 8, WHITE, GREEN_LT, 4)

sp_final = Image.new("RGB", (SIZE, SIZE), BG_DEEP)
sp_final.paste(sp, mask=sp.split()[3])
sp_final.save(SPLASH_OUT, "PNG")
print(f"Splash -> {SPLASH_OUT}")
