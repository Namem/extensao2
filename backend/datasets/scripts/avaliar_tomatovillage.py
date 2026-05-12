"""
Avalia o modelo ceres_mobilenetv2_int8.tflite no dataset Tomato-Village.
Validação independente do gap lab-campo usando dataset completamente
separado dos experimentos de treinamento (A, B, C e D).

Dataset: Tomato-Village (Rajasthan, Índia, 2022)
  Referência: Girase et al., Frontiers in Plant Science, 2024
  4.525 imagens, 8 classes, condições de campo real
  Apenas classes com mapeamento Ceres são avaliadas (4 classes):
    Late_blight        → D01_requeima
    Early_blight       → D03_pinta_preta
    Spotted Wilt Virus → D06_vira_cabeca
    Healthy            → saudavel

Uso:
    python avaliar_tomatovillage.py              # apenas split test (padrão)
    python avaliar_tomatovillage.py --split all  # train + val + test

Saída:
    docs/resultados/tomatovillage_results.md
"""

import argparse
import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from PIL import Image

# ---------------------------------------------------------------------------
# Argumentos
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument(
    "--split",
    choices=["test", "all"],
    default="test",
    help="Split(s) a avaliar. 'test' = apenas test (padrão, métrica justa). "
         "'all' = train+val+test (para diagnóstico).",
)
parser.add_argument("--modelo", type=str, default=None,
    help="Nome do .tflite em datasets/modelo/. Ex: --modelo ceres_expe_int8.tflite")
args = parser.parse_args()

SPLITS = ["test"] if args.split == "test" else ["train", "val", "test"]

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

BASE_DIR    = Path(__file__).resolve().parents[2]
_modelo_nome = args.modelo if args.modelo else "ceres_mobilenetv2_int8.tflite"
MODELO_PATH = BASE_DIR / "datasets" / "modelo" / _modelo_nome
TV_DIR      = BASE_DIR / "datasets" / "raw" / "tomato_village"
RESULTADO   = BASE_DIR.parent / "docs" / "resultados" / "tomatovillage_results.md"

IMG_SIZE    = 96

# Mapeamento Tomato-Village → classe Ceres
# Apenas as 4 classes com correspondência direta são avaliadas.
# As outras 4 classes do dataset (Yellow_Leaf_Curl, Mosaic, Leaf_Miner,
# Spider_mite) não têm correspondência exata e são ignoradas.
MAPA_CLASSES = {
    "Late_blight"        : "D01_requeima",
    "Early_blight"       : "D03_pinta_preta",
    "Spotted Wilt Virus" : "D06_vira_cabeca",
    "Healthy"            : "saudavel",
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
print(f"Classes Ceres: {CLASSES_CERES}")
print(f"Splits a avaliar: {SPLITS}")

# ---------------------------------------------------------------------------
# Função de inferência
# ---------------------------------------------------------------------------

def inferir(caminho_img: Path) -> str:
    """Retorna o nome da classe predita para uma imagem."""
    img = Image.open(caminho_img).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img, dtype=np.float32)

    # Normalizar para [-1, 1] — igual ao treinamento (Rescaling 1/127.5 - 1)
    arr_norm = arr / 127.5 - 1.0

    # Quantizar float → INT8 usando parâmetros do tensor de entrada
    arr_int8 = np.round(arr_norm / escala + zero).clip(-128, 127).astype(np.int8)
    arr_int8 = arr_int8[np.newaxis, ...]  # adiciona batch dimension

    interp.set_tensor(inp["index"], arr_int8)
    interp.invoke()

    # Dequantizar saída INT8 → float antes do argmax
    out_escala, out_zero = out["quantization"]
    saida_int8  = interp.get_tensor(out["index"])[0]  # shape: (10,) INT8
    saida_float = (saida_int8.astype(np.float32) - out_zero) * out_escala
    idx = int(np.argmax(saida_float))
    return CLASSES_CERES[idx]

# ---------------------------------------------------------------------------
# Avaliar por classe
# ---------------------------------------------------------------------------

print(f"\nDataset Tomato-Village: {TV_DIR}")

resultados  = {}  # classe_ceres → {"corretas": int, "total": int, "tv_pasta": str}
erros_global = 0

for pasta_tv, classe_ceres in MAPA_CLASSES.items():
    imagens = []
    for split in SPLITS:
        pasta = TV_DIR / split / pasta_tv
        if pasta.exists():
            imagens += (
                list(pasta.glob("*.jpg")) +
                list(pasta.glob("*.JPG")) +
                list(pasta.glob("*.jpeg")) +
                list(pasta.glob("*.png"))
            )
        else:
            print(f"  [AVISO] Não encontrado: {pasta}")

    if not imagens:
        print(f"  [SKIP] Nenhuma imagem para: {pasta_tv}")
        continue

    corretas  = 0
    predicoes = []
    for img_path in imagens:
        try:
            pred = inferir(img_path)
            predicoes.append(pred)
            if pred == classe_ceres:
                corretas += 1
        except Exception as e:
            erros_global += 1
            print(f"  [ERRO] {img_path.name}: {e}")

    resultados[classe_ceres] = {
        "corretas"   : corretas,
        "total"      : len(imagens),
        "tv_pasta"   : pasta_tv,
        "predicoes"  : predicoes,
    }
    acc = corretas / len(imagens) * 100
    print(f"  {classe_ceres:<35} {corretas:>3}/{len(imagens):<3}  {acc:.1f}%")
    # Top-3 predições mais frequentes
    from collections import Counter
    top3 = Counter(predicoes).most_common(3)
    for cls, cnt in top3:
        print(f"    → {cls}: {cnt}")

# ---------------------------------------------------------------------------
# Calcular acurácia geral
# ---------------------------------------------------------------------------

total_corretas = sum(v["corretas"] for v in resultados.values())
total_imgs     = sum(v["total"]    for v in resultados.values())
acc_geral      = total_corretas / total_imgs * 100 if total_imgs else 0

print(f"\n{'='*55}")
print(f"Acurácia geral Tomato-Village (campo real): {acc_geral:.2f}%")
print(f"Total imagens avaliadas: {total_imgs}")
print(f"Erros de leitura: {erros_global}")
print(f"Splits avaliados: {SPLITS}")
print(f"{'='*55}")

# ---------------------------------------------------------------------------
# Salvar resultado em Markdown
# ---------------------------------------------------------------------------

with open(RESULTADO, "w", encoding="utf-8") as f:
    f.write("# Avaliação Tomato-Village — Validação Independente em Campo Real\n\n")
    f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Modelo:** ceres_mobilenetv2_int8.tflite (639 KB) — Exp D\n")
    f.write(f"**Dataset:** Tomato-Village (Rajasthan, Índia, 2022 — Girase et al., 2024)\n")
    f.write(f"**Splits avaliados:** {', '.join(SPLITS)}\n\n")
    f.write("## Mapeamento de Classes\n\n")
    f.write("| Classe Tomato-Village | Classe Ceres |\n|---|---|\n")
    for tv, ceres in MAPA_CLASSES.items():
        f.write(f"| {tv} | {ceres} |\n")
    f.write("\n*Nota: 4 das 8 classes do dataset não têm correspondência "
            "direta no Ceres e foram ignoradas.*\n\n")
    f.write("## Resultado por Classe\n\n")
    f.write("| Classe Ceres | Pasta TV | Corretas | Total | Acurácia | Top predição errada |\n")
    f.write("|---|---|---|---|---|---|\n")
    from collections import Counter
    for classe, v in resultados.items():
        acc = v["corretas"] / v["total"] * 100 if v["total"] else 0
        erradas = [p for p in v["predicoes"] if p != classe]
        top_errada = Counter(erradas).most_common(1)
        top_str = f"{top_errada[0][0]} ({top_errada[0][1]}x)" if top_errada else "—"
        f.write(f"| {classe} | {v['tv_pasta']} | {v['corretas']} | "
                f"{v['total']} | {acc:.1f}% | {top_str} |\n")
    f.write("\n## Resultado Geral\n\n")
    f.write("| Métrica | Valor |\n|---|---|\n")
    f.write(f"| **Acurácia geral** | **{acc_geral:.2f}%** |\n")
    f.write(f"| Total imagens | {total_imgs} |\n")
    f.write(f"| Erros de leitura | {erros_global} |\n")
    f.write(f"| Splits | {', '.join(SPLITS)} |\n\n")
    f.write("## Comparativo com PlantDoc\n\n")
    f.write("| Dataset | Imgs | Modelo | Acurácia | Nota |\n")
    f.write("|---|---|---|---|---|\n")
    f.write("| PlantDoc (train+test) | 746 | Exp B | 20,24% | Linha base |\n")
    f.write("| PlantDoc (test only) | 69 | Exp D | 30,43% | Após fine-tuning |\n")
    f.write(f"| **Tomato-Village (test)** | **{total_imgs}** | **Exp D** | "
            f"**{acc_geral:.2f}%** | **Validação independente** |\n\n")
    f.write("## Análise\n\n")
    f.write("`[Preencher após ver os resultados]`\n")

print(f"\nResultado salvo em: {RESULTADO}")
