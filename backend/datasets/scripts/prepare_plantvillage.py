"""
Preparação do dataset PlantVillage para o projeto Ceres Diagnóstico.

Execução:
    python datasets/scripts/prepare_plantvillage.py

Pré-requisito:
    Dataset baixado e descompactado em:
    backend/datasets/raw/plantvillage dataset/color/

Saída:
    backend/datasets/processed/train|val|test   (imagens organizadas por classe)
    backend/datasets/dataset_stats.md
    backend/datasets/edge_impulse_upload_guide.md
"""

import os
import shutil
import random
import math
import textwrap
from pathlib import Path
from datetime import date

try:
    from PIL import Image, ImageEnhance
except ImportError:
    raise SystemExit("Pillow não instalado. Execute: pip install Pillow")

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

SEED = 42
SPLIT = (0.70, 0.15, 0.15)  # train / val / test

RAW_DIR = Path(__file__).resolve().parents[2] / "datasets" / "raw" / "plantvillage dataset" / "color"
PROCESSED_DIR = Path(__file__).resolve().parents[2] / "datasets" / "processed"
STATS_FILE = Path(__file__).resolve().parents[2] / "datasets" / "dataset_stats.md"
GUIDE_FILE = Path(__file__).resolve().parents[2] / "datasets" / "edge_impulse_upload_guide.md"

MIN_IMAGES_ALERT = 200  # alerta se classe tiver menos que isso após split

# Mapeamento: pasta PlantVillage → nome legível Ceres
# Nomes reais usam triple underscore (___) como separador
TOMATO_CLASSES = {
    "Tomato___Bacterial_spot":                          "D09_mancha_bacteriana",
    "Tomato___Early_blight":                            "D03_pinta_preta",
    "Tomato___Late_blight":                             "D01_requeima",
    "Tomato___Leaf_Mold":                               "D05_mofo_foliar",
    "Tomato___Septoria_leaf_spot":                      "D02_septoriose",
    "Tomato___Spider_mites Two-spotted_spider_mite":    "D07_acaro_bronzeamento",
    "Tomato___Target_Spot":                             "D03b_mancha_alvo",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus":           "D06_vira_cabeca",
    "Tomato___Tomato_mosaic_virus":                     "D06b_mosaico",
    "Tomato___healthy":                                 "saudavel",
}

# Augmentations aplicadas apenas no treino
AUG_OPS = [
    ("flip_h",   lambda img: img.transpose(Image.FLIP_LEFT_RIGHT)),
    ("flip_v",   lambda img: img.transpose(Image.FLIP_TOP_BOTTOM)),
    ("rot_p15",  lambda img: img.rotate(15, expand=True)),
    ("rot_m15",  lambda img: img.rotate(-15, expand=True)),
    ("bright_p", lambda img: ImageEnhance.Brightness(img).enhance(1.20)),
    ("bright_m", lambda img: ImageEnhance.Brightness(img).enhance(0.80)),
]


# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------

def listar_imagens(pasta: Path) -> list[Path]:
    """Retorna lista de imagens JPG/PNG em uma pasta."""
    exts = {".jpg", ".jpeg", ".png"}
    return [f for f in pasta.iterdir() if f.suffix.lower() in exts]


def split_estratificado(imagens: list[Path], ratios: tuple) -> tuple[list, list, list]:
    """Divide lista em train/val/test mantendo proporção."""
    random.shuffle(imagens)
    n = len(imagens)
    n_train = math.floor(n * ratios[0])
    n_val   = math.floor(n * ratios[1])
    return imagens[:n_train], imagens[n_train:n_train + n_val], imagens[n_train + n_val:]


def copiar(src: Path, dst_dir: Path):
    """Copia arquivo garantindo que o diretório existe."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst_dir / src.name)


def aplicar_augmentation(src: Path, dst_dir: Path):
    """Aplica todas as operações de augmentation e salva as variações."""
    img = Image.open(src).convert("RGB")
    stem = src.stem
    for nome, op in AUG_OPS:
        aug = op(img)
        out_path = dst_dir / f"{stem}__aug_{nome}.jpg"
        aug.save(out_path, "JPEG", quality=92)


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def main():
    random.seed(SEED)

    if not RAW_DIR.exists():
        raise SystemExit(
            f"\n[ERRO] Dataset não encontrado em:\n  {RAW_DIR}\n\n"
            "Execute primeiro:\n"
            "  kaggle datasets download abdallahalidev/plantvillage-dataset "
            "-p backend/datasets/raw/ --unzip"
        )

    # Descobrir quais pastas de tomate realmente existem no raw
    pastas_disponiveis = {p.name: p for p in RAW_DIR.iterdir() if p.is_dir()}
    classes_encontradas = {k: v for k, v in TOMATO_CLASSES.items() if k in pastas_disponiveis}
    classes_ausentes = [k for k in TOMATO_CLASSES if k not in pastas_disponiveis]

    if classes_ausentes:
        print(f"[AVISO] Classes não encontradas no dataset raw: {classes_ausentes}")

    print(f"\n=== Ceres Diagnóstico — Preparação PlantVillage ===")
    print(f"Classes encontradas : {len(classes_encontradas)}")
    print(f"Split               : {int(SPLIT[0]*100)}% train / {int(SPLIT[1]*100)}% val / {int(SPLIT[2]*100)}% test")
    print(f"Augmentation        : {len(AUG_OPS)} operações (somente treino)\n")

    stats = {}  # classe_ceres → {train, val, test, aug, total_treino}
    alertas = []

    for nome_raw, nome_ceres in classes_encontradas.items():
        pasta_src = pastas_disponiveis[nome_raw]
        imagens = listar_imagens(pasta_src)

        if len(imagens) < MIN_IMAGES_ALERT:
            alertas.append(f"  ⚠  {nome_ceres}: apenas {len(imagens)} imagens (< {MIN_IMAGES_ALERT})")

        train_imgs, val_imgs, test_imgs = split_estratificado(imagens, SPLIT)

        # Copiar splits
        for img in train_imgs:
            copiar(img, PROCESSED_DIR / "train" / nome_ceres)
        for img in val_imgs:
            copiar(img, PROCESSED_DIR / "val" / nome_ceres)
        for img in test_imgs:
            copiar(img, PROCESSED_DIR / "test" / nome_ceres)

        # Augmentation no treino
        aug_dir = PROCESSED_DIR / "train" / nome_ceres
        for img in train_imgs:
            aplicar_augmentation(img, aug_dir)

        n_aug = len(train_imgs) * len(AUG_OPS)
        stats[nome_ceres] = {
            "original": len(imagens),
            "train": len(train_imgs),
            "val": len(val_imgs),
            "test": len(test_imgs),
            "aug": n_aug,
            "total_treino": len(train_imgs) + n_aug,
        }

        print(f"  {nome_ceres:<35} orig={len(imagens):>5}  "
              f"train={len(train_imgs):>4}(+{n_aug} aug)  val={len(val_imgs):>4}  test={len(test_imgs):>4}")

    # Totais
    total_orig   = sum(v["original"]     for v in stats.values())
    total_train  = sum(v["train"]        for v in stats.values())
    total_val    = sum(v["val"]          for v in stats.values())
    total_test   = sum(v["test"]         for v in stats.values())
    total_aug    = sum(v["aug"]          for v in stats.values())
    total_treino = sum(v["total_treino"] for v in stats.values())

    print(f"\n  {'TOTAL':<35} orig={total_orig:>5}  "
          f"train={total_train:>4}(+{total_aug} aug)  val={total_val:>4}  test={total_test:>4}")

    if alertas:
        print("\nALERTAS:")
        for a in alertas:
            print(a)

    gerar_stats_md(stats, total_orig, total_train, total_val, total_test, total_aug, total_treino, alertas)
    gerar_guide_md(stats)

    print(f"\n[OK] dataset_stats.md       -> {STATS_FILE}")
    print(f"[OK] edge_impulse_upload_guide.md -> {GUIDE_FILE}")
    print("\nDataset pronto. Proximo passo: upload no Edge Impulse (veja o guia acima).")


# ---------------------------------------------------------------------------
# Geração dos Markdown de saída
# ---------------------------------------------------------------------------

def gerar_stats_md(stats, total_orig, total_train, total_val, total_test, total_aug, total_treino, alertas):
    linhas_tabela = []
    for classe, v in sorted(stats.items()):
        linhas_tabela.append(
            f"| {classe:<35} | {v['original']:>8} | {v['train']:>7} | {v['aug']:>10} | "
            f"{v['total_treino']:>13} | {v['val']:>5} | {v['test']:>5} |"
        )

    alertas_md = "\n".join(alertas) if alertas else "_Nenhum alerta._"

    conteudo = textwrap.dedent(f"""\
        # Dataset Stats — PlantVillage (Tomate)
        **Gerado em:** {date.today()}
        **Projeto:** Ceres Diagnóstico — TCC IFMT Sorriso-MT

        ## Resumo

        | Métrica               | Valor       |
        |-----------------------|-------------|
        | Classes               | {len(stats)} |
        | Imagens originais     | {total_orig} |
        | Treino (originais)    | {total_train} |
        | Augmentações geradas  | {total_aug} |
        | Treino total          | {total_treino} |
        | Validação             | {total_val} |
        | Teste                 | {total_test} |
        | Split                 | 70 / 15 / 15 |
        | Seed                  | 42 |

        ## Por Classe

        | Classe                              | Original | Train   | Aug (+) | Train total  | Val   | Test  |
        |-------------------------------------|----------|---------|---------|--------------|-------|-------|
        {chr(10).join(linhas_tabela)}
        | **TOTAL**                           | **{total_orig}** | **{total_train}** | **{total_aug}** | **{total_treino}** | **{total_val}** | **{total_test}** |

        ## Alertas

        {alertas_md}

        ## Augmentations aplicadas (somente treino)

        | Operação     | Descrição                         |
        |--------------|-----------------------------------|
        | flip_h       | Espelhamento horizontal           |
        | flip_v       | Espelhamento vertical             |
        | rot_p15      | Rotação +15°                      |
        | rot_m15      | Rotação −15°                      |
        | bright_p     | Brilho +20%                       |
        | bright_m     | Brilho −20%                       |
    """)

    STATS_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATS_FILE.write_text(conteudo, encoding="utf-8")


def gerar_guide_md(stats):
    classes_lista = "\n".join(f"- `{c}`" for c in sorted(stats.keys()))

    conteudo = textwrap.dedent(f"""\
        # Edge Impulse — Guia de Upload
        **Projeto:** Ceres Diagnóstico — TCC IFMT Sorriso-MT
        **Gerado em:** {date.today()}

        ## Pré-requisitos

        1. Conta criada em [edgeimpulse.com](https://edgeimpulse.com)
        2. Projeto criado: `ceres-diagnostico`
        3. Edge Impulse CLI instalado:
           ```bash
           npm install -g edge-impulse-cli
           edge-impulse-daemon  # autentica e vincula ao projeto
           ```

        ## Estrutura esperada após prepare_plantvillage.py

        ```
        backend/datasets/processed/
        ├── train/
        │   ├── D01_requeima/
        │   ├── D02_septoriose/
        │   └── ...
        ├── val/
        │   └── ...
        └── test/
            └── ...
        ```

        ## Classes disponíveis ({len(stats)})

        {classes_lista}

        ## Upload via CLI

        ```bash
        # Treino
        edge-impulse-uploader --category training \\
            backend/datasets/processed/train/**/*

        # Validação
        edge-impulse-uploader --category validation \\
            backend/datasets/processed/val/**/*

        # Teste (mantido local para benchmark final)
        # NÃO fazer upload do test split — usar em benchmark_esp32s3.py
        ```

        ## Configuração do Impulse no Edge Impulse Studio

        | Campo              | Valor sugerido          |
        |--------------------|-------------------------|
        | Image width        | 96 px                   |
        | Image height       | 96 px                   |
        | Resize mode        | Fit shortest axis       |
        | Color depth        | RGB                     |
        | Architecture       | MobileNetV2 96x96 0.35  |
        | Quantização        | INT8                    |
        | Target device      | ESP32-S3 (Xtensa LX7)   |

        ## Treinamento recomendado

        | Parâmetro          | Valor     |
        |--------------------|-----------|
        | Epochs             | 50        |
        | Learning rate      | 0.0005    |
        | Batch size         | 32        |
        | Data augmentation  | Desligada (já feita offline) |
        | Min accuracy alvo  | 85%       |

        ## Exportação para ESP32-S3

        1. **Deployment** → Arduino Library → Download `.zip`
        2. Mover para `firmware/esp32s3_ceres/lib/ei_ceres/`
        3. Seguir `docs/tflite_integration.md` (Sprint 2)

        ## Verificação rápida pós-upload

        ```bash
        # Confirmar contagem de amostras por label
        edge-impulse-api-client dataset summary
        ```
    """)

    GUIDE_FILE.parent.mkdir(parents=True, exist_ok=True)
    GUIDE_FILE.write_text(conteudo, encoding="utf-8")


if __name__ == "__main__":
    main()
