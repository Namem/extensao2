"""
Exporta o melhor modelo salvo para TFLite FP32 e INT8.

Uso (WSL2 com venv ativa):
    python3 .../export_tflite.py

Carrega best_fase2.keras (ou best_fase1.keras se nao existir)
e gera os arquivos .tflite + relatorio final.
"""

import os
import numpy as np
from pathlib import Path
from datetime import datetime

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import tensorflow as tf

print(f"TensorFlow: {tf.__version__}")
print(f"GPU: {tf.config.list_physical_devices('GPU')}")

# ---------------------------------------------------------------------------
# Configuracoes
# ---------------------------------------------------------------------------

IMG_SIZE   = 96
BATCH_SIZE = 32
SEED       = 42

BASE_DIR   = Path("/mnt/c/Users/Namem/Desktop/Codiguins/extensao/ceres-diagnostico/backend")
VAL_DIR    = BASE_DIR / "datasets" / "processed" / "val"
TEST_DIR   = BASE_DIR / "datasets" / "processed" / "test"
MODELO_DIR = BASE_DIR / "datasets" / "modelo"

# Escolhe o melhor checkpoint disponivel
CHECKPOINT = MODELO_DIR / "best_fase2.keras"
if not CHECKPOINT.exists():
    CHECKPOINT = MODELO_DIR / "best_fase1.keras"
    print("[AVISO] best_fase2.keras nao encontrado — usando best_fase1.keras")

print(f"\nCarregando: {CHECKPOINT}")
modelo = tf.keras.models.load_model(str(CHECKPOINT))
modelo.summary()

# ---------------------------------------------------------------------------
# Carregar val e test
# ---------------------------------------------------------------------------

normalizacao = tf.keras.layers.Rescaling(scale=1.0/127.5, offset=-1.0)

def carregar(pasta, shuffle=False):
    ds = tf.keras.utils.image_dataset_from_directory(
        str(pasta),
        image_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        shuffle=shuffle,
        seed=SEED,
        label_mode="categorical",
    )
    return ds.map(
        lambda x, y: (normalizacao(x), y),
        num_parallel_calls=tf.data.AUTOTUNE
    ).prefetch(tf.data.AUTOTUNE)

ds_val  = carregar(VAL_DIR)
ds_test = carregar(TEST_DIR)
CLASSES = ds_val.class_names

# ---------------------------------------------------------------------------
# Exportar TFLite FP32
# ---------------------------------------------------------------------------

print("\n[1/3] Exportando TFLite FP32...")
converter = tf.lite.TFLiteConverter.from_keras_model(modelo)
tflite_fp32 = converter.convert()
path_fp32 = MODELO_DIR / "ceres_mobilenetv2.tflite"
path_fp32.write_bytes(tflite_fp32)
print(f"FP32: {len(tflite_fp32)/1024:.1f} KB")

# ---------------------------------------------------------------------------
# Exportar TFLite INT8
# ---------------------------------------------------------------------------

print("\n[2/3] Exportando TFLite INT8 (calibrando com val set)...")

def gerador_calibracao():
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
print(f"INT8: {len(tflite_int8)/1024:.1f} KB")

# ---------------------------------------------------------------------------
# Relatorio final
# ---------------------------------------------------------------------------

print("\n[3/3] Avaliando no test set...")
loss_test, acc_test = modelo.evaluate(ds_test, verbose=1)

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
    f.write(f"Data      : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Hardware  : RTX 3060 Ti (WSL2), TF {tf.__version__}\n")
    f.write(f"Checkpoint: {CHECKPOINT.name}\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Acuracia test set : {acc_test*100:.2f}%\n")
    f.write(f"Loss test set     : {loss_test:.4f}\n")
    f.write(f"Tamanho FP32      : {len(tflite_fp32)/1024:.1f} KB\n")
    f.write(f"Tamanho INT8      : {len(tflite_int8)/1024:.1f} KB\n\n")
    f.write("Acuracia por classe:\n")
    f.write("-" * 45 + "\n")
    for i, classe in enumerate(CLASSES):
        mask = y_true == i
        if mask.sum() > 0:
            acc_c = (y_pred[mask] == i).mean()
            f.write(f"  {classe:<35} {acc_c*100:6.2f}%\n")
    f.write("\nMatriz de Confusao:\n")
    n = len(CLASSES)
    matriz = np.zeros((n, n), dtype=int)
    for t, p in zip(y_true, y_pred):
        matriz[t][p] += 1
    for i, row in enumerate(matriz):
        f.write(f"  {CLASSES[i][:20]:<22}: {list(row)}\n")

print(f"\n{'='*50}")
print(f"Acuracia test set : {acc_test*100:.2f}%")
print(f"TFLite FP32       : {len(tflite_fp32)/1024:.1f} KB")
print(f"TFLite INT8       : {len(tflite_int8)/1024:.1f} KB")
print(f"Relatorio         : {relatorio_path}")
print(f"{'='*50}")
