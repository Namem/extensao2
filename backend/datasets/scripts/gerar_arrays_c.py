"""
gerar_arrays_c.py — Gera model_data.h e test_images.h para TFLite Micro no ESP32-S3.

Uso:
    python gerar_arrays_c.py

Saída:
    firmware/esp32s3_ceres/include/model_data.h   — modelo TFLite como array C
    firmware/esp32s3_ceres/include/test_images.h  — 5 imagens de teste como arrays int8

O modelo INT8 do MobileNetV2 espera entrada int8 com:
    scale=0.0078125, zero_point=0  →  valor_int8 = pixel_uint8 - 128
    (equivale a normalizar [0,255] → [-128,127])
"""

from pathlib import Path
import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
BASE       = Path(__file__).resolve().parents[3]
MODELO     = BASE / "backend" / "datasets" / "modelo" / "ceres_mobilenetv2_int8.tflite"
TEST_DIR   = BASE / "backend" / "datasets" / "processed" / "test"
OUT_DIR    = BASE / "firmware" / "esp32s3_ceres" / "include"
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMG_SIZE   = 96

# 1 imagem representativa por classe (na ordem do modelo)
CLASSES = [
    "D01_requeima",
    "D02_septoriose",
    "D03_pinta_preta",
    "D03b_mancha_alvo",
    "D05_mofo_foliar",
    "D06_vira_cabeca",
    "D06b_mosaico",
    "D07_acaro_bronzeamento",
    "D09_mancha_bacteriana",
    "saudavel",
]

# ---------------------------------------------------------------------------
# Passo 1 — model_data.h
# ---------------------------------------------------------------------------
print("=" * 60)
print("PASSO 1 — Gerando model_data.h")
print("=" * 60)

if not MODELO.exists():
    raise FileNotFoundError(f"Modelo não encontrado: {MODELO}")

model_bytes = MODELO.read_bytes()
print(f"  Modelo: {MODELO.name} — {len(model_bytes)/1024:.1f} KB")

lines = ["// Modelo TFLite gerado automaticamente por gerar_arrays_c.py",
         "// NÃO editar manualmente.",
         "#pragma once",
         "#include <stdint.h>",
         "",
         f"// Tamanho: {len(model_bytes)} bytes ({len(model_bytes)/1024:.1f} KB)",
         f"const unsigned int g_model_len = {len(model_bytes)};",
         "alignas(8) const unsigned char g_model_data[] = {"]

HEX_PER_LINE = 12
for i in range(0, len(model_bytes), HEX_PER_LINE):
    chunk = model_bytes[i:i+HEX_PER_LINE]
    hex_vals = ", ".join(f"0x{b:02x}" for b in chunk)
    lines.append(f"  {hex_vals},")

lines.append("};")
lines.append("")

(OUT_DIR / "model_data.h").write_text("\n".join(lines), encoding="utf-8")
print(f"  Salvo: {OUT_DIR / 'model_data.h'}")

# ---------------------------------------------------------------------------
# Passo 2 — test_images.h
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("PASSO 2 — Gerando test_images.h")
print("=" * 60)

images_data = []
for label in CLASSES:
    class_dir = TEST_DIR / label
    if not class_dir.exists():
        print(f"  AVISO: classe não encontrada — {label}")
        continue
    imgs = sorted(class_dir.glob("*.jpg")) + sorted(class_dir.glob("*.png"))
    if not imgs:
        print(f"  AVISO: sem imagens em {label}")
        continue
    # Pega a 3ª imagem (evita possível imagem corrompida no início)
    src = imgs[min(2, len(imgs)-1)]
    img = Image.open(src).convert("RGB").resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
    arr = np.array(img, dtype=np.int32) - 128   # uint8 [0,255] → int8 [-128,127]
    arr = arr.astype(np.int8).flatten()
    images_data.append((label, arr, src.name))
    print(f"  OK  {label:30s} ← {src.name[:35]}")

# Gerar header
lines2 = ["// Imagens de teste geradas automaticamente por gerar_arrays_c.py",
          "// NÃO editar manualmente.",
          "#pragma once",
          "#include <stdint.h>",
          "",
          f"#define TEST_IMG_SIZE     {IMG_SIZE}",
          f"#define TEST_IMG_CHANNELS 3",
          f"#define TEST_IMG_BYTES    ({IMG_SIZE} * {IMG_SIZE} * 3)",
          f"#define TEST_IMG_COUNT    {len(images_data)}",
          ""]

# Nomes das classes
lines2.append("const char* const g_class_names[] = {")
for label, _, _ in images_data:
    lines2.append(f'  "{label}",')
lines2.append("};")
lines2.append("")

# Arrays de cada imagem
for idx, (label, arr, fname) in enumerate(images_data):
    lines2.append(f"// [{idx}] {label} — {fname}")
    lines2.append(f"const int8_t g_test_img_{idx}[TEST_IMG_BYTES] = {{")
    for i in range(0, len(arr), HEX_PER_LINE):
        chunk = arr[i:i+HEX_PER_LINE]
        vals = ", ".join(str(int(v)) for v in chunk)
        lines2.append(f"  {vals},")
    lines2.append("};")
    lines2.append("")

# Ponteiro array para iterar facilmente no firmware
lines2.append("const int8_t* const g_test_images[] = {")
for idx, (label, _, _) in enumerate(images_data):
    lines2.append(f"  g_test_img_{idx},  // {label}")
lines2.append("};")
lines2.append("")

(OUT_DIR / "test_images.h").write_text("\n".join(lines2), encoding="utf-8")
print(f"\n  Salvo: {OUT_DIR / 'test_images.h'}")

# ---------------------------------------------------------------------------
# Resumo
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("CONCLUÍDO")
print("=" * 60)
print(f"  model_data.h  — {len(model_bytes)/1024:.1f} KB")
print(f"  test_images.h — {len(images_data)} imagens x {IMG_SIZE}x{IMG_SIZE}x3 int8")
print(f"  Destino: {OUT_DIR}")
print("\nPróximo passo: criar o projeto PlatformIO em firmware/esp32s3_ceres/")
