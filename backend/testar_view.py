"""
Testa a view InferirImagemView via Django Test Client (sem HTTP real).
Isola se o problema esta na view ou no servidor HTTP.
"""
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'ceres_core.settings_notebook'
django.setup()

from pathlib import Path
from django.test import Client

img_path = next(Path("datasets/processed/val").rglob("*.jpg"))
classe_esperada = img_path.parent.name
print(f"Imagem: {classe_esperada}/{img_path.name}")

client = Client()
with open(img_path, "rb") as f:
    response = client.post(
        "/api/diagnostico/inferir/",
        {"imagem": f},
        format="multipart",
    )

print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Predicao  : {data['classe']}")
    print(f"Confianca : {data['confianca']*100:.1f}%")
    print(f"Latencia  : {data['latencia_ms']}ms")
    correto = data['classe'] == classe_esperada
    print(f"Resultado : {'CORRETO' if correto else 'ERRADO'}")
else:
    print(f"Erro: {response.content}")
