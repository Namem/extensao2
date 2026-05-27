"""Testa inference_service diretamente sem HTTP."""
from pathlib import Path
from diagnostico.inference_service import inferencia_service

modelo = Path("datasets/modelo/ceres_mobilenetv2_int8.tflite")
print("Carregando modelo...")
inferencia_service.carregar(modelo)
print("Modelo carregado OK")

img_path = next(Path("datasets/processed/val").rglob("*.jpg"))
classe_esperada = img_path.parent.name
print(f"Imagem: {classe_esperada}/{img_path.name}")

resultado = inferencia_service.inferir(img_path.read_bytes())
print(f"Predicao  : {resultado['classe']}")
print(f"Confianca : {resultado['confianca']*100:.1f}%")
print(f"Latencia  : {resultado['latencia_ms']}ms")
correto = resultado['classe'] == classe_esperada
print(f"Resultado : {'CORRETO' if correto else 'ERRADO'}")
