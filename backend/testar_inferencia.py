"""
Testa o endpoint POST /api/diagnostico/inferir/ localmente.
Usar com Django rodando em 0.0.0.0:8000.

Uso:
  python testar_inferencia.py
"""
import requests
from pathlib import Path

# Pega a primeira imagem do val set
val_dir = Path("datasets/processed/val")
img_path = next(val_dir.rglob("*.jpg"), None) or next(val_dir.rglob("*.JPG"), None)

if not img_path:
    print("ERRO: nenhuma imagem encontrada em datasets/processed/val/")
    exit(1)

print(f"Imagem: {img_path}")
classe_esperada = img_path.parent.name

with open(img_path, "rb") as f:
    resp = requests.post(
        "http://localhost:8080/api/diagnostico/inferir/",
        files={"imagem": (img_path.name, f, "image/jpeg")},
        timeout=30,
    )

print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    data = resp.json()
    print(f"Classe esperada : {classe_esperada}")
    print(f"Predição        : {data['classe']}")
    print(f"Confiança       : {data['confianca']*100:.1f}%")
    print(f"Latência        : {data['latencia_ms']}ms")
    correto = data['classe'] == classe_esperada
    print(f"Resultado       : {'CORRETO' if correto else 'ERRADO'}")
else:
    print(f"Erro: {resp.text}")
