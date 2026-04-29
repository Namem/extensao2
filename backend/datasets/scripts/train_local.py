"""
Experimento B — Treinamento local MobileNetV2 com RTX 3060 Ti (WSL2).

Uso (dentro do WSL2 com venv ativa):
    python3 /mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend/datasets/scripts/train_local.py

Pre-requisitos:
    source ~/venv_ceres/bin/activate
    Dataset processado em backend/datasets/processed/train|val|test

Saidas:
    backend/datasets/modelo/ceres_mobilenetv2.h5        modelo Keras
    backend/datasets/modelo/ceres_mobilenetv2.tflite    modelo TFLite FP32
    backend/datasets/modelo/ceres_mobilenetv2_int8.tflite modelo TFLite INT8
    backend/datasets/modelo/historico_treino.csv        metricas por epoch
    backend/datasets/modelo/relatorio_final.txt         acuracia + matriz confusao
"""

import os
import csv
import time
import random
import numpy as np
from pathlib import Path
from datetime import datetime

# Suprimir warnings do TF antes do import
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers, callbacks
from tensorflow.keras.applications import MobileNetV2

print(f"TensorFlow: {tf.__version__}")
gpus = tf.config.list_physical_devices("GPU")
print(f"GPUs: {gpus}")
if not gpus:
    print("[AVISO] GPU nao detectada — treinando na CPU (muito mais lento)")

# ---------------------------------------------------------------------------
# Configuracoes
# ---------------------------------------------------------------------------

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

IMG_SIZE    = 96          # MobileNetV2 96x96 (mesmo do Edge Impulse)
BATCH_SIZE  = 32
EPOCHS_1    = 10          # Fase 1: cabeca congelada
EPOCHS_2    = 40          # Fase 2: fine-tuning
LR_1        = 1e-3        # Learning rate fase 1
LR_2        = 5e-4        # Learning rate fase 2 (menor para fine-tuning)
NUM_CLASSES = 10

BASE_DIR      = Path("/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend")
TRAIN_DIR     = BASE_DIR / "datasets" / "processed" / "train"
VAL_DIR       = BASE_DIR / "datasets" / "processed" / "val"
TEST_DIR      = BASE_DIR / "datasets" / "processed" / "test"
MODELO_DIR    = BASE_DIR / "datasets" / "modelo"
MODELO_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Carregar datasets
# ---------------------------------------------------------------------------

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

print("\n[1/6] Carregando datasets...")
ds_train = carregar_dataset(TRAIN_DIR, shuffle=True)
ds_val   = carregar_dataset(VAL_DIR,   shuffle=False)
ds_test  = carregar_dataset(TEST_DIR,  shuffle=False)

# Nomes das classes (ordem alfabetica — igual ao treinamento)
CLASSES = ds_train.class_names
print(f"Classes ({len(CLASSES)}): {CLASSES}")

# Normalizacao [-1, 1] igual ao MobileNetV2 original
normalizacao = layers.Rescaling(scale=1.0/127.5, offset=-1.0)

def preparar(ds, treino=False):
    ds = ds.map(lambda x, y: (normalizacao(x), y), num_parallel_calls=tf.data.AUTOTUNE)
    if treino:
        # Augmentation online leve (complementa o offline ja feito)
        aug = tf.keras.Sequential([
            layers.RandomFlip("horizontal"),
            layers.RandomRotation(0.05),
        ])
        ds = ds.map(lambda x, y: (aug(x, training=True), y), num_parallel_calls=tf.data.AUTOTUNE)
    return ds.prefetch(tf.data.AUTOTUNE)

ds_train = preparar(ds_train, treino=True)
ds_val   = preparar(ds_val,   treino=False)
ds_test  = preparar(ds_test,  treino=False)

# ---------------------------------------------------------------------------
# 2. Construir modelo
# ---------------------------------------------------------------------------

print("\n[2/6] Construindo modelo MobileNetV2 96x96...")

base = MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    alpha=0.35,          # variante leve (mesmo do Edge Impulse)
    include_top=False,
    weights="imagenet",
)
base.trainable = False   # congela na fase 1

entradas = tf.keras.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = base(entradas, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.2)(x)
saidas = layers.Dense(NUM_CLASSES, activation="softmax")(x)

modelo = models.Model(entradas, saidas)
modelo.summary()

# ---------------------------------------------------------------------------
# 3. Fase 1 — treinar cabeca
# ---------------------------------------------------------------------------

print(f"\n[3/6] Fase 1: treinando cabeca ({EPOCHS_1} epochs, LR={LR_1})...")

modelo.compile(
    optimizer=optimizers.Adam(LR_1),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

cbs_fase1 = [
    callbacks.EarlyStopping(patience=5, restore_best_weights=True, monitor="val_accuracy"),
    callbacks.ModelCheckpoint(str(MODELO_DIR / "best_fase1.keras"), save_best_only=True),
]

hist1 = modelo.fit(
    ds_train,
    epochs=EPOCHS_1,
    validation_data=ds_val,
    callbacks=cbs_fase1,
    verbose=1,
)

# ---------------------------------------------------------------------------
# 4. Fase 2 — fine-tuning
# ---------------------------------------------------------------------------

print(f"\n[4/6] Fase 2: fine-tuning ({EPOCHS_2} epochs, LR={LR_2})...")

# Descongela as ultimas 30 camadas do backbone
base.trainable = True
for layer in base.layers[:-30]:
    layer.trainable = False

modelo.compile(
    optimizer=optimizers.Adam(LR_2),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

cbs_fase2 = [
    callbacks.EarlyStopping(patience=8, restore_best_weights=True, monitor="val_accuracy"),
    callbacks.ModelCheckpoint(str(MODELO_DIR / "best_fase2.keras"), save_best_only=True),
    callbacks.ReduceLROnPlateau(factor=0.5, patience=4, monitor="val_accuracy", verbose=1),
]

hist2 = modelo.fit(
    ds_train,
    epochs=EPOCHS_2,
    validation_data=ds_val,
    callbacks=cbs_fase2,
    verbose=1,
)

# ---------------------------------------------------------------------------
# 5. Salvar modelo e metricas
# ---------------------------------------------------------------------------

print("\n[5/6] Salvando modelo e metricas...")

# Modelo Keras completo
modelo.save(str(MODELO_DIR / "ceres_mobilenetv2.h5"))

# Historico de treino em CSV (fase1 + fase2 concatenados)
csv_path = MODELO_DIR / "historico_treino.csv"
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["fase", "epoch", "loss", "accuracy", "val_loss", "val_accuracy"])
    for i, (l, a, vl, va) in enumerate(zip(
        hist1.history["loss"], hist1.history["accuracy"],
        hist1.history["val_loss"], hist1.history["val_accuracy"]
    )):
        writer.writerow([1, i+1, f"{l:.4f}", f"{a:.4f}", f"{vl:.4f}", f"{va:.4f}"])
    for i, (l, a, vl, va) in enumerate(zip(
        hist2.history["loss"], hist2.history["accuracy"],
        hist2.history["val_loss"], hist2.history["val_accuracy"]
    )):
        writer.writerow([2, i+1, f"{l:.4f}", f"{a:.4f}", f"{vl:.4f}", f"{va:.4f}"])

print(f"Historico salvo: {csv_path}")

# ---------------------------------------------------------------------------
# 6. Exportar TFLite FP32 e INT8
# ---------------------------------------------------------------------------

print("\n[6/6] Exportando TFLite FP32 e INT8...")

# FP32
converter_fp32 = tf.lite.TFLiteConverter.from_keras_model(modelo)
tflite_fp32 = converter_fp32.convert()
path_fp32 = MODELO_DIR / "ceres_mobilenetv2.tflite"
path_fp32.write_bytes(tflite_fp32)
print(f"TFLite FP32: {len(tflite_fp32)/1024:.1f} KB -> {path_fp32}")

# INT8 — calibracao com imagens reais do val set
def gerador_calibracao():
    """Gera amostras do val set para calibrar a quantizacao INT8."""
    for imgs, _ in ds_val.take(50):
        for img in imgs:
            yield [img[tf.newaxis, ...].numpy()]

converter_int8 = tf.lite.TFLiteConverter.from_keras_model(modelo)
converter_int8.optimizations = [tf.lite.Optimize.DEFAULT]
converter_int8.representative_dataset = gerador_calibracao
converter_int8.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter_int8.inference_input_type  = tf.int8
converter_int8.inference_output_type = tf.int8

tflite_int8 = converter_int8.convert()
path_int8 = MODELO_DIR / "ceres_mobilenetv2_int8.tflite"
path_int8.write_bytes(tflite_int8)
print(f"TFLite INT8: {len(tflite_int8)/1024:.1f} KB -> {path_int8}")

# ---------------------------------------------------------------------------
# Relatorio final
# ---------------------------------------------------------------------------

print("\nAvaliando no test set...")
loss_test, acc_test = modelo.evaluate(ds_test, verbose=0)

# Matriz de confusao
y_true, y_pred = [], []
for imgs, labels in ds_test:
    preds = modelo.predict(imgs, verbose=0)
    y_true.extend(np.argmax(labels.numpy(), axis=1))
    y_pred.extend(np.argmax(preds, axis=1))

y_true = np.array(y_true)
y_pred = np.array(y_pred)

relatorio_path = MODELO_DIR / "relatorio_final.txt"
with open(relatorio_path, "w", encoding="utf-8") as f:
    f.write("=" * 60 + "\n")
    f.write("RELATORIO EXPERIMENTO B — TensorFlow Local\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Hardware: RTX 3060 Ti (WSL2), TF {tf.__version__}\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Acuracia no test set : {acc_test*100:.2f}%\n")
    f.write(f"Loss no test set     : {loss_test:.4f}\n")
    f.write(f"Tamanho FP32         : {len(tflite_fp32)/1024:.1f} KB\n")
    f.write(f"Tamanho INT8         : {len(tflite_int8)/1024:.1f} KB\n\n")
    f.write("Acuracia por classe:\n")
    f.write("-" * 40 + "\n")
    for i, classe in enumerate(CLASSES):
        mask = y_true == i
        if mask.sum() > 0:
            acc_classe = (y_pred[mask] == i).mean()
            f.write(f"  {classe:<35} {acc_classe*100:6.2f}%\n")
    f.write("\nMatriz de Confusao (linhas=real, colunas=predito):\n")
    n = NUM_CLASSES
    matriz = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred):
        matriz[t][p] += 1
    header = "".join(f"{c[:6]:>8}" for c in CLASSES)
    f.write(f"{'':>10}{header}\n")
    for i, row in enumerate(matriz):
        linha = "".join(f"{v:>8}" for v in row)
        f.write(f"{CLASSES[i][:10]:>10}{linha}\n")

print(f"\n{'='*50}")
print(f"RESULTADO FINAL — Experimento B")
print(f"Acuracia test set : {acc_test*100:.2f}%")
print(f"TFLite FP32       : {len(tflite_fp32)/1024:.1f} KB")
print(f"TFLite INT8       : {len(tflite_int8)/1024:.1f} KB")
print(f"Relatorio         : {relatorio_path}")
print(f"{'='*50}")
print("\nProximo passo: copiar ceres_mobilenetv2_int8.tflite para firmware/esp32s3_ceres/")
