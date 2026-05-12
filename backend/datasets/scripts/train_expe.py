"""
Experimento E — Focal Loss + Augmentação Agressiva + Backbone Completo.

Melhorias sobre o Exp D (fine-tuning PlantDoc):
  1. Focal Loss (Lin et al. 2017, RetinaNet) + label smoothing 0.1
     → combate colapso para D02_septoriose sob shift de domínio
  2. Augmentação de cor agressiva: brilho, contraste, saturação, hue
     → simula variação de iluminação campo real (luz solar, câmeras distintas)
  3. Backbone completamente descongelado na Fase 2 com LR=1e-5
     → ajuste fino de todas as features, não só as últimas 30 camadas
  4. Macro F1 por epoch no terminal
     → detecta colapso de classe que val_accuracy esconde
  5. 60 epochs Fase 2 com EarlyStopping(patience=10)
     → permite convergência mais longa sem risco de overfitting

Uso:
    source ~/venv_ceres/bin/activate
    python3 .../train_expe.py --data-dir datasets/processed_mixed

Saídas:
    datasets/modelo/ceres_expe_int8.tflite   ← não sobrescreve o Exp D
    datasets/modelo/ceres_expe.h5
    datasets/modelo/historico_expe.csv
    datasets/modelo/relatorio_expe.txt
"""

import os
import csv
import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.applications import MobileNetV2
from sklearn.metrics import f1_score, classification_report

print(f"TensorFlow: {tf.__version__}")
gpus = tf.config.list_physical_devices("GPU")
print(f"GPUs: {gpus}")
if not gpus:
    print("[AVISO] GPU nao detectada — treinando na CPU (muito mais lento)")

# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

SEED        = 42
IMG_SIZE    = 96
BATCH_SIZE  = 32
EPOCHS_1    = 10    # Fase 1: cabeça (head) com backbone congelado
EPOCHS_2    = 60    # Fase 2: backbone completo, LR baixíssimo
LR_1        = 1e-3
LR_2        = 1e-5  # 50x menor que Exp D — backbone completo é sensível
NUM_CLASSES = 10

random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

import argparse
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument("--data-dir", type=str, default=None)
_args, _ = _parser.parse_known_args()

BASE_DIR   = Path("/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend")
_data_root = Path(_args.data_dir) if _args.data_dir else BASE_DIR / "datasets" / "processed_mixed"
TRAIN_DIR  = _data_root / "train"
VAL_DIR    = _data_root / "val"
TEST_DIR   = _data_root / "test"
MODELO_DIR = BASE_DIR / "datasets" / "modelo"
MODELO_DIR.mkdir(parents=True, exist_ok=True)

print(f"Dataset      : {_data_root}")
print(f"Saídas em    : {MODELO_DIR}")

# ---------------------------------------------------------------------------
# 1. Carregar datasets
# ---------------------------------------------------------------------------

print("\n[1/6] Carregando datasets...")

def carregar_dataset(pasta: Path, shuffle: bool = True) -> tf.data.Dataset:
    """Carrega imagens de pasta organizada por subpastas de classe."""
    ds = tf.keras.utils.image_dataset_from_directory(
        str(pasta),
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
        seed=SEED,
        label_mode="categorical",
    )
    return ds

ds_train_raw = carregar_dataset(TRAIN_DIR, shuffle=True)
ds_val_raw   = carregar_dataset(VAL_DIR,   shuffle=False)
ds_test_raw  = carregar_dataset(TEST_DIR,  shuffle=False)

CLASSES = ds_train_raw.class_names
print(f"Classes ({len(CLASSES)}): {CLASSES}")

# ---------------------------------------------------------------------------
# 2. Pipeline de pré-processamento e augmentação
# ---------------------------------------------------------------------------

# Normalização [-1, 1] — obrigatório para MobileNetV2
normalizacao = layers.Rescaling(scale=1.0 / 127.5, offset=-1.0)


def augmentar_agressivo(x: tf.Tensor) -> tf.Tensor:
    """
    Augmentação forte de geometria + cor.

    Opera em [-1, 1]: converte para [0, 1] para operações de cor do tf.image
    (que esperam esse range), aplica, clipa, e volta para [-1, 1].
    Simula variações de campo: sol, sombra, câmeras diferentes, cultivares.
    """
    # Geometria
    x = tf.image.random_flip_left_right(x)
    x = tf.image.random_flip_up_down(x)
    # Rotação por múltiplos de 90° (sem distorção)
    k = tf.random.uniform(shape=[], minval=0, maxval=4, dtype=tf.int32)
    x = tf.image.rot90(x, k=k)

    # Cor — converte [-1,1] → [0,1] para usar tf.image.*
    x01 = (x + 1.0) / 2.0
    x01 = tf.image.random_brightness(x01, max_delta=0.30)   # simula sol/nuvem
    x01 = tf.image.random_contrast(x01, lower=0.70, upper=1.40)  # câmeras distintas
    x01 = tf.image.random_saturation(x01, lower=0.50, upper=1.60)  # saturação variável
    x01 = tf.image.random_hue(x01, max_delta=0.08)           # leve variação de matiz
    x01 = tf.clip_by_value(x01, 0.0, 1.0)

    # Volta para [-1, 1]
    return x01 * 2.0 - 1.0


def preparar(ds: tf.data.Dataset, treino: bool = False) -> tf.data.Dataset:
    ds = ds.map(lambda x, y: (normalizacao(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    if treino:
        ds = ds.map(
            lambda x, y: (augmentar_agressivo(x), y),
            num_parallel_calls=tf.data.AUTOTUNE,
        )
    return ds.prefetch(tf.data.AUTOTUNE)


ds_train = preparar(ds_train_raw, treino=True)
ds_val   = preparar(ds_val_raw,   treino=False)
ds_test  = preparar(ds_test_raw,  treino=False)

# ---------------------------------------------------------------------------
# 3. Callback: Macro F1 por epoch
# ---------------------------------------------------------------------------


class MacroF1Callback(tf.keras.callbacks.Callback):
    """
    Calcula Macro F1 no val set ao fim de cada epoch.

    Macro F1 é crucial aqui: val_accuracy de 95% pode esconder colapso
    para uma única classe (D02_septoriose) que o modelo aprende como
    'resposta segura' sob shift de domínio.
    """

    def __init__(self, ds_val, classes):
        super().__init__()
        self.ds_val  = ds_val
        self.classes = classes

    def on_epoch_end(self, epoch, logs=None):
        y_true, y_pred = [], []
        for x_batch, y_batch in self.ds_val:
            preds = self.model.predict(x_batch, verbose=0)
            y_true.extend(np.argmax(y_batch.numpy(), axis=1))
            y_pred.extend(np.argmax(preds, axis=1))

        macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
        if logs is not None:
            logs["macro_f1"] = macro_f1

        # Detectar colapso: se uma classe recebe > 50% das predições
        contagem = np.bincount(y_pred, minlength=len(self.classes))
        dominante_idx  = int(np.argmax(contagem))
        dominante_pct  = contagem[dominante_idx] / len(y_pred) * 100
        alerta = " ⚠ COLAPSO" if dominante_pct > 50 else ""
        print(
            f"  macro_F1={macro_f1:.4f} | "
            f"classe dominante: {self.classes[dominante_idx]} ({dominante_pct:.0f}%){alerta}"
        )


# ---------------------------------------------------------------------------
# 4. Construir modelo (igual ao Exp D — mesmo tamanho de saída)
# ---------------------------------------------------------------------------

print("\n[2/6] Construindo modelo MobileNetV2 96x96 0.35...")

base = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    alpha=0.35,
    include_top=False,
    weights="imagenet",
)
base.trainable = False

entradas = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base(entradas, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)       # Dropout maior (0.2→0.3) para regularizar mais
saidas = layers.Dense(NUM_CLASSES, activation="softmax")(x)

modelo = models.Model(entradas, saidas)
print(f"Parâmetros totais    : {modelo.count_params():,}")
print(f"Parâmetros treináveis: {sum(p.numpy().size for p in modelo.trainable_weights):,}")

# ---------------------------------------------------------------------------
# 5. Fase 1 — aquecer cabeça com CE normal (backbone congelado)
# ---------------------------------------------------------------------------

print(f"\n[3/6] Fase 1: cabeça ({EPOCHS_1} epochs, LR={LR_1}) com CE normal...")

modelo.compile(
    optimizer=optimizers.Adam(LR_1),
    loss="categorical_crossentropy",   # CE normal na fase 1 — backbone frozen = estável
    metrics=["accuracy"],
)

cbs_fase1 = [
    callbacks.EarlyStopping(patience=5, restore_best_weights=True, monitor="val_accuracy"),
    callbacks.ModelCheckpoint(str(MODELO_DIR / "expe_best_fase1.keras"), save_best_only=True),
    MacroF1Callback(ds_val, CLASSES),
]

t0 = time.time()
hist1 = modelo.fit(
    ds_train,
    epochs=EPOCHS_1,
    validation_data=ds_val,
    callbacks=cbs_fase1,
    verbose=1,
)
print(f"Fase 1 concluída em {(time.time()-t0)/60:.1f} min")

# ---------------------------------------------------------------------------
# 6. Fase 2 — Focal Loss + backbone completo + LR baixíssimo
# ---------------------------------------------------------------------------

print(f"\n[4/6] Fase 2: backbone completo ({EPOCHS_2} epochs, LR={LR_2}) com Focal Loss...")

# Descongela TODO o backbone — LR extremamente baixo para não destruir features
base.trainable = True

# CategoricalFocalCrossentropy: disponível desde TF 2.11
# gamma=2.0: exemplos difíceis (erros confiantes) recebem 4x mais gradiente
# label_smoothing=0.1: evita overconfidence no D02 (0.9 em vez de 1.0 no target)
try:
    focal_loss = tf.keras.losses.CategoricalFocalCrossentropy(
        gamma=2.0,
        label_smoothing=0.1,
        from_logits=False,
    )
    print("  Focal Loss carregada (TF nativo)")
except AttributeError:
    # Fallback: CE com label smoothing se TF < 2.11
    focal_loss = tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.1)
    print("  [AVISO] CategoricalFocalCrossentropy não disponível — usando CE + label_smoothing")

modelo.compile(
    optimizer=optimizers.Adam(LR_2),
    loss=focal_loss,
    metrics=["accuracy"],
)

cbs_fase2 = [
    callbacks.EarlyStopping(patience=10, restore_best_weights=True, monitor="val_accuracy"),
    callbacks.ModelCheckpoint(str(MODELO_DIR / "expe_best_fase2.keras"), save_best_only=True),
    callbacks.ReduceLROnPlateau(factor=0.5, patience=5, monitor="val_accuracy", verbose=1, min_lr=1e-7),
    MacroF1Callback(ds_val, CLASSES),
]

t0 = time.time()
hist2 = modelo.fit(
    ds_train,
    epochs=EPOCHS_2,
    validation_data=ds_val,
    callbacks=cbs_fase2,
    verbose=1,
)
print(f"Fase 2 concluída em {(time.time()-t0)/60:.1f} min")

# ---------------------------------------------------------------------------
# 7. Salvar modelo e histórico
# ---------------------------------------------------------------------------

print("\n[5/6] Salvando modelo e histórico...")

modelo.save(str(MODELO_DIR / "ceres_expe.h5"))

csv_path = MODELO_DIR / "historico_expe.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["fase", "epoch", "loss", "accuracy", "val_loss", "val_accuracy"])
    for i, (l, a, vl, va) in enumerate(zip(
        hist1.history["loss"], hist1.history["accuracy"],
        hist1.history["val_loss"], hist1.history["val_accuracy"],
    )):
        writer.writerow([1, i + 1, f"{l:.4f}", f"{a:.4f}", f"{vl:.4f}", f"{va:.4f}"])
    for i, (l, a, vl, va) in enumerate(zip(
        hist2.history["loss"], hist2.history["accuracy"],
        hist2.history["val_loss"], hist2.history["val_accuracy"],
    )):
        writer.writerow([2, i + 1, f"{l:.4f}", f"{a:.4f}", f"{vl:.4f}", f"{va:.4f}"])

print(f"Histórico salvo: {csv_path}")

# ---------------------------------------------------------------------------
# 8. Exportar TFLite INT8 (mesmo processo calibrado do Exp B/D)
# ---------------------------------------------------------------------------

print("\n[6/6] Exportando TFLite INT8 calibrado...")

# FP32
converter_fp32 = tf.lite.TFLiteConverter.from_keras_model(modelo)
tflite_fp32    = converter_fp32.convert()
path_fp32      = MODELO_DIR / "ceres_expe.tflite"
path_fp32.write_bytes(tflite_fp32)

# INT8 com representative_dataset do val set (50 batches — mesma estratégia do Exp B)
def gerador_calibracao():
    for imgs, _ in ds_val.take(50):
        for img in imgs:
            yield [img[tf.newaxis, ...].numpy()]

converter_int8 = tf.lite.TFLiteConverter.from_keras_model(modelo)
converter_int8.optimizations                     = [tf.lite.Optimize.DEFAULT]
converter_int8.representative_dataset            = gerador_calibracao
converter_int8.target_spec.supported_ops         = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter_int8.inference_input_type              = tf.int8
converter_int8.inference_output_type             = tf.int8

tflite_int8 = converter_int8.convert()
path_int8   = MODELO_DIR / "ceres_expe_int8.tflite"
path_int8.write_bytes(tflite_int8)

print(f"FP32 : {len(tflite_fp32)/1024:.1f} KB → {path_fp32}")
print(f"INT8 : {len(tflite_int8)/1024:.1f} KB → {path_int8}")

# ---------------------------------------------------------------------------
# 9. Relatório final com per-class F1 e matriz de confusão
# ---------------------------------------------------------------------------

print("\nAvaliando no test set...")
loss_test, acc_test = modelo.evaluate(ds_test, verbose=0)

y_true, y_pred = [], []
for imgs, labels in ds_test:
    preds  = modelo.predict(imgs, verbose=0)
    y_true.extend(np.argmax(labels.numpy(), axis=1))
    y_pred.extend(np.argmax(preds, axis=1))

y_true = np.array(y_true)
y_pred = np.array(y_pred)

macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
relatorio = classification_report(y_true, y_pred, target_names=CLASSES, zero_division=0)

relatorio_path = MODELO_DIR / "relatorio_expe.txt"
with open(relatorio_path, "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("RELATÓRIO EXPERIMENTO E — Focal Loss + Aug Agressiva\n")
    f.write(f"Data     : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Hardware : RTX 3060 Ti (WSL2), TF {tf.__version__}\n")
    f.write(f"Dataset  : {_data_root}\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Acurácia test set : {acc_test*100:.2f}%\n")
    f.write(f"Macro F1 test set : {macro_f1:.4f}\n")
    f.write(f"Loss test set     : {loss_test:.4f}\n")
    f.write(f"Tamanho FP32      : {len(tflite_fp32)/1024:.1f} KB\n")
    f.write(f"Tamanho INT8      : {len(tflite_int8)/1024:.1f} KB\n\n")
    f.write("Relatório por classe (precision / recall / f1):\n")
    f.write("-" * 60 + "\n")
    f.write(relatorio + "\n")
    f.write("\nMatriz de Confusão (linhas=real, colunas=predito):\n")
    n = NUM_CLASSES
    matriz = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred):
        matriz[t][p] += 1
    header = "".join(f"{c[:6]:>8}" for c in CLASSES)
    f.write(f"{'':>12}{header}\n")
    for i, row in enumerate(matriz):
        linha = "".join(f"{v:>8}" for v in row)
        f.write(f"{CLASSES[i][:12]:>12}{linha}\n")

print(f"\n{'='*55}")
print(f"RESULTADO FINAL — Experimento E")
print(f"Acurácia test set : {acc_test*100:.2f}%")
print(f"Macro F1 test set : {macro_f1:.4f}")
print(f"INT8              : {len(tflite_int8)/1024:.1f} KB → {path_int8}")
print(f"Relatório         : {relatorio_path}")
print(f"{'='*55}")
print("\nPróximo passo: rodar os 3 avaliadores de campo sequencialmente.")
print("  python3 datasets/scripts/avaliar_plantdoc.py")
print("  python3 datasets/scripts/avaliar_tomatovillage.py")
print("  python3 datasets/scripts/avaliar_daffodil.py")
