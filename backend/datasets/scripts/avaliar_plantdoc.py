"""
Avalia o modelo ceres_mobilenetv2_int8.tflite no dataset PlantDoc.
Valida a generalização do modelo para imagens de campo real.

Uso:
    python avaliar_plantdoc.py

Saída:
    docs/plantdoc_results.md
"""

import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from PIL import Image

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

BASE_DIR    = Path(__file__).resolve().parents[2]
MODELO_PATH = BASE_DIR / "datasets" / "modelo" / "ceres_mobilenetv2_int8.tflite"
PLANTDOC    = BASE_DIR / "datasets" / "raw" / "plantdoc" / "train"
RESULTADO   = BASE_DIR.parent / "docs" / "plantdoc_results.md"

IMG_SIZE    = 96

# Mapeamento PlantDoc → classe Ceres
MAPA_CLASSES = {
    "Tomato leaf late blight"                  : "D01_requeima",
    "Tomato Septoria leaf spot"                : "D02_septoriose",
    "Tomato Early blight leaf"                 : "D03_pinta_preta",
    "Tomato mold leaf"                         : "D05_mofo_foliar",
    "Tomato leaf yellow virus"                 : "D06_vira_cabeca",
    "Tomato leaf mosaic virus"                 : "D06b_mosaico",
    "Tomato two spotted spider mites leaf"     : "D07_acaro_bronzeamento",
    "Tomato leaf bacterial spot"               : "D09_mancha_bacteriana",
    "Tomato leaf"                              : "saudavel",
}

# Ordem das classes — DEVE ser idêntica à ordem do treino (alfabética)
CLASSES_CERES = sorted([
    "D01_requeima", "D02_septoriose", "D03_pinta_preta",
    "D03b_mancha_alvo", "D05_mofo_foliar", "D06_vira_cabeca",
    "D06b_mosaico", "D07_acaro_bronzeamento", "D09_mancha_bacteriana",
    "saudavel"
])

# ---------------------------------------------------------------------------
# Carregar modelo TFLite INT8
# ---------------------------------------------------------------------------

print(f"Carregando modelo: {MODELO_PATH}")
interp = tf.lite.Interpreter(model_path=str(MODELO_PATH))
interp.allocate_tensors()

inp  = interp.get_input_details()[0]
out  = interp.get_output_details()[0]
escala, zero = inp["quantization"]

print(f"Input shape : {inp['shape']}  dtype: {inp['dtype']}")
print(f"Output shape: {out['shape']}  dtype: {out['dtype']}")
print(f"Escala: {escala}  Zero-point: {zero}")
print(f"Classes: {CLASSES_CERES}")

# ---------------------------------------------------------------------------
# Função de inferência
# ---------------------------------------------------------------------------

def inferir(caminho_img: Path) -> str:
    """Retorna o nome da classe predita para uma imagem."""
    img = Image.open(caminho_img).convert("RGB").resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img, dtype=np.float32)

    # Passo 1: normalizar para [-1, 1] igual ao treinamento (Rescaling 1/127.5 - 1)
    arr_norm = arr / 127.5 - 1.0

    # Passo 2: quantizar float [-1,1] → INT8 usando params do tensor de entrada
    arr_int8 = np.round(arr_norm / escala + zero).clip(-128, 127).astype(np.int8)
    arr_int8 = arr_int8[np.newaxis, ...]  # adiciona batch dimension

    interp.set_tensor(inp["index"], arr_int8)
    interp.invoke()

    # Passo 3: saída INT8 — dequantizar para float antes do argmax
    out_escala, out_zero = out["quantization"]
    saida_int8 = interp.get_tensor(out["index"])[0]  # shape: (10,) INT8
    saida_float = (saida_int8.astype(np.float32) - out_zero) * out_escala
    idx = int(np.argmax(saida_float))
    return CLASSES_CERES[idx]

# ---------------------------------------------------------------------------
# Avaliar por classe
# ---------------------------------------------------------------------------

print(f"\nAvaliando imagens em: {PLANTDOC}")

resultados = {}   # classe_ceres → {"corretas": int, "total": int}
erros_global = 0

for pasta_plantdoc, classe_ceres in MAPA_CLASSES.items():
    pasta = PLANTDOC / pasta_plantdoc
    if not pasta.exists():
        print(f"  [AVISO] Pasta não encontrada: {pasta_plantdoc}")
        continue

    imagens = list(pasta.glob("*.jpg")) + list(pasta.glob("*.JPG")) + \
              list(pasta.glob("*.png")) + list(pasta.glob("*.jpeg"))

    corretas = 0
    for img_path in imagens:
        try:
            pred = inferir(img_path)
            if pred == classe_ceres:
                corretas += 1
        except Exception as e:
            erros_global += 1

    resultados[classe_ceres] = {"corretas": corretas, "total": len(imagens)}
    acc = corretas / len(imagens) * 100 if imagens else 0
    print(f"  {classe_ceres:<35} {corretas:>3}/{len(imagens):<3}  {acc:.1f}%")

# ---------------------------------------------------------------------------
# Calcular acurácia geral
# ---------------------------------------------------------------------------

total_corretas = sum(v["corretas"] for v in resultados.values())
total_imgs     = sum(v["total"]    for v in resultados.values())
acc_geral      = total_corretas / total_imgs * 100 if total_imgs else 0

print(f"\n{'='*50}")
print(f"Acuracia geral PlantDoc (campo real): {acc_geral:.2f}%")
print(f"Total imagens avaliadas: {total_imgs}")
print(f"Erros de leitura: {erros_global}")
print(f"{'='*50}")

# ---------------------------------------------------------------------------
# Salvar resultado em Markdown
# ---------------------------------------------------------------------------

with open(RESULTADO, "w", encoding="utf-8") as f:
    f.write("# Avaliacao PlantDoc — Validacao em Campo Real\n\n")
    f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Modelo:** ceres_mobilenetv2_int8.tflite (639 KB)\n")
    f.write(f"**Dataset:** PlantDoc (imagens de campo real, fundo natural)\n\n")
    f.write("## Resultado por Classe\n\n")
    f.write("| Classe Ceres | Corretas | Total | Acuracia |\n")
    f.write("|---|---|---|---|\n")
    for classe, v in resultados.items():
        acc = v["corretas"] / v["total"] * 100 if v["total"] else 0
        f.write(f"| {classe} | {v['corretas']} | {v['total']} | {acc:.1f}% |\n")
    f.write(f"\n## Resultado Geral\n\n")
    f.write(f"| Metrica | Valor |\n|---|---|\n")
    f.write(f"| **Acuracia geral** | **{acc_geral:.2f}%** |\n")
    f.write(f"| Total imagens | {total_imgs} |\n")
    f.write(f"| Meta TCC | > 70% |\n")
    f.write(f"| Atingiu a meta? | {'Sim' if acc_geral >= 70 else 'Nao — analisar causas'} |\n\n")
    f.write("## Analise\n\n")
    f.write("`[Preencher apos ver os resultados]`\n")

print(f"\nResultado salvo em: {RESULTADO}")