"""
Avalia o modelo ceres_mobilenetv2_int8.tflite no dataset Daffodil BD.
Validação independente em imagens de campo real — Bangladesh, Ásia do Sul.

Dataset: "Tomato leaf diseases" — Daffodil International University, Bangladesh
  Coleta: Khagan, Charabag (campo aberto, iPhone 11, luz natural)
  Referência: Mendeley Data — https://data.mendeley.com/datasets/93h9p62kg4/1
  Total: 2.627 imagens, 10 classes
  Avaliadas: 7 classes com mapeamento direto para Ceres (1.616 imagens)
  Ignoradas: Cercospora leaf mold, Insect Damage, Leaf Miner (sem equivalente Ceres)

Uso:
    python avaliar_daffodil.py

Saída:
    docs/daffodil_results.md
"""

import argparse
import numpy as np
import tensorflow as tf
from pathlib import Path
from datetime import datetime
from collections import Counter
from PIL import Image

# ---------------------------------------------------------------------------
# Argumentos
# ---------------------------------------------------------------------------

_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument("--modelo", type=str, default=None,
    help="Nome do .tflite em datasets/modelo/. Ex: --modelo ceres_expe_int8.tflite")
_args, _ = _parser.parse_known_args()

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

BASE_DIR    = Path(__file__).resolve().parents[2]
_modelo_nome = _args.modelo if _args.modelo else "ceres_mobilenetv2_int8.tflite"
MODELO_PATH = BASE_DIR / "datasets" / "modelo" / _modelo_nome
BD_DIR      = BASE_DIR / "datasets" / "raw" / "daffodil_bd" / "Tomato leaf diseases" / "Tomato Leaf"
RESULTADO   = BASE_DIR.parent / "docs" / "resultados" / "daffodil_results.md"

IMG_SIZE    = 96

# Mapeamento Daffodil → classe Ceres
# Tomato Leaf Curl Virus (TLCV) → D06_vira_cabeca (TYLCV)
#   Ambos são begomovirus transmitidos por mosca-branca (Bemisia tabaci)
#   com sintomas de enrolamento e amarelamento — mapeamento biologicamente válido.
#   Diferente do TSWV usado no Tomato-Village (mapeamento incorreto).
MAPA_CLASSES = {
    "Late Blight"             : "D01_requeima",
    "Leaf Mold"               : "D05_mofo_foliar",
    "Early Blight"            : "D03_pinta_preta",
    "Spider Mites"            : "D07_acaro_bronzeamento",
    "Tomato Leaf Curl Virus"  : "D06_vira_cabeca",
    "Bacterial Spot"          : "D09_mancha_bacteriana",
    "Healthy"                 : "saudavel",
    # Ignoradas — sem equivalente nas 10 classes Ceres:
    # "Cercospora leaf mold"  → fungo diferente do Leaf Mold (D05)
    # "Insect Damage"         → dano genérico por inseto, não classificado
    # "Leaf Miner"            → Liriomyza spp., não está no escopo
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
out_escala, out_zero = out["quantization"]

print(f"Input : {inp['shape']}  dtype={inp['dtype']}")
print(f"Output: {out['shape']}  dtype={out['dtype']}")
print(f"Classes Ceres: {CLASSES_CERES}")

# ---------------------------------------------------------------------------
# Função de inferência
# ---------------------------------------------------------------------------

def inferir(caminho_img: Path) -> str:
    """Retorna o nome da classe predita para uma imagem."""
    img = Image.open(caminho_img).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))
    arr = np.array(img, dtype=np.float32)
    arr_norm = arr / 127.5 - 1.0
    arr_int8 = np.round(arr_norm / escala + zero).clip(-128, 127).astype(np.int8)
    arr_int8 = arr_int8[np.newaxis, ...]
    interp.set_tensor(inp["index"], arr_int8)
    interp.invoke()
    saida_int8  = interp.get_tensor(out["index"])[0]
    saida_float = (saida_int8.astype(np.float32) - out_zero) * out_escala
    return CLASSES_CERES[int(np.argmax(saida_float))]

# ---------------------------------------------------------------------------
# Avaliar por classe
# ---------------------------------------------------------------------------

print(f"\nDataset: {BD_DIR}")
print(f"Classes avaliadas: {list(MAPA_CLASSES.keys())}\n")

resultados   = {}
erros_global = 0

for pasta_bd, classe_ceres in MAPA_CLASSES.items():
    pasta = BD_DIR / pasta_bd
    if not pasta.exists():
        print(f"  [AVISO] Pasta não encontrada: {pasta_bd}")
        continue

    imagens = (list(pasta.glob("*.jpg")) + list(pasta.glob("*.JPG")) +
               list(pasta.glob("*.jpeg")) + list(pasta.glob("*.png")))
    if not imagens:
        print(f"  [SKIP] Sem imagens: {pasta_bd}")
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

    resultados[classe_ceres] = {
        "corretas"  : corretas,
        "total"     : len(imagens),
        "bd_pasta"  : pasta_bd,
        "predicoes" : predicoes,
    }
    acc  = corretas / len(imagens) * 100
    top3 = Counter(predicoes).most_common(3)
    print(f"  {classe_ceres:<35} {corretas:>3}/{len(imagens):<3}  {acc:.1f}%")
    for cls, cnt in top3:
        print(f"    → {cls}: {cnt}")

# ---------------------------------------------------------------------------
# Acurácia geral
# ---------------------------------------------------------------------------

total_corretas = sum(v["corretas"] for v in resultados.values())
total_imgs     = sum(v["total"]    for v in resultados.values())
acc_geral      = total_corretas / total_imgs * 100 if total_imgs else 0

print(f"\n{'='*55}")
print(f"Acurácia geral Daffodil BD (campo real): {acc_geral:.2f}%")
print(f"Total imagens avaliadas: {total_imgs}")
print(f"Erros de leitura: {erros_global}")
print(f"{'='*55}")

# ---------------------------------------------------------------------------
# Salvar resultado em Markdown
# ---------------------------------------------------------------------------

RESULTADO.parent.mkdir(parents=True, exist_ok=True)

with open(RESULTADO, "w", encoding="utf-8") as f:
    f.write("# Avaliação Daffodil BD — 3ª Validação Independente em Campo Real\n\n")
    f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"**Modelo:** ceres_mobilenetv2_int8.tflite (639 KB) — Exp D\n")
    f.write(f"**Dataset:** Daffodil International University, Bangladesh (Mendeley, 2024)\n")
    f.write(f"**Captura:** iPhone 11, campo aberto, luz natural, Khagan/Charabag\n\n")

    f.write("## Mapeamento de Classes\n\n")
    f.write("| Classe Daffodil BD | Classe Ceres | Justificativa |\n|---|---|---|\n")
    mapas_just = {
        "Late Blight"            : "Phytophthora infestans — mesma doença",
        "Leaf Mold"              : "Passalora fulva — mesma doença",
        "Early Blight"           : "Alternaria solani — mesma doença",
        "Spider Mites"           : "Tetranychus urticae — mesma espécie",
        "Tomato Leaf Curl Virus" : "TLCV = begomovirus mesma família do TYLCV (D06) — sintomas equivalentes",
        "Bacterial Spot"         : "Xanthomonas spp. — mesma doença",
        "Healthy"                : "Folha saudável",
    }
    for bd, ceres in MAPA_CLASSES.items():
        f.write(f"| {bd} | {ceres} | {mapas_just.get(bd, '—')} |\n")

    f.write("\n*Ignoradas (sem mapeamento Ceres): Cercospora leaf mold, Insect Damage, Leaf Miner*\n\n")

    f.write("## Resultado por Classe\n\n")
    f.write("| Classe Ceres | Pasta BD | Corretas | Total | Acurácia | Top predição errada |\n")
    f.write("|---|---|---|---|---|---|\n")
    for classe, v in resultados.items():
        acc = v["corretas"] / v["total"] * 100 if v["total"] else 0
        erradas = [p for p in v["predicoes"] if p != classe]
        top_err = Counter(erradas).most_common(1)
        top_str = f"{top_err[0][0]} ({top_err[0][1]}x)" if top_err else "—"
        f.write(f"| {classe} | {v['bd_pasta']} | {v['corretas']} | "
                f"{v['total']} | {acc:.1f}% | {top_str} |\n")

    f.write("\n## Resultado Geral\n\n")
    f.write("| Métrica | Valor |\n|---|---|\n")
    f.write(f"| **Acurácia geral** | **{acc_geral:.2f}%** |\n")
    f.write(f"| Total imagens | {total_imgs} |\n")
    f.write(f"| Classes avaliadas | {len(resultados)} |\n")
    f.write(f"| Erros de leitura | {erros_global} |\n\n")

    f.write("## Comparativo — 3 Datasets Independentes\n\n")
    f.write("| Dataset | Região | Clima | Imagens | Classes | Resultado Exp D |\n")
    f.write("|---|---|---|---|---|---|\n")
    f.write("| PlantDoc (test) | EUA / Europa | Temperado | 69 | 4 | 30,43% |\n")
    f.write("| Tomato-Village (test) | Rajasthan, Índia | Árido tropical | 217 | 4* | 11,52% |\n")
    f.write(f"| **Daffodil BD** | **Bangladesh** | **Tropical úmido** | **{total_imgs}** | **{len(resultados)}** | **{acc_geral:.2f}%** |\n\n")
    f.write("*\\* D06 no Tomato-Village era TSWV (mapeamento incorreto — doença diferente do TYLCV)*\n\n")

    f.write("## Análise\n\n")
    f.write("`[Preencher após ver os resultados]`\n")

print(f"\nResultado salvo em: {RESULTADO}")
