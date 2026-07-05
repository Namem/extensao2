# Scripts de teste manual — inferência

Testes rápidos (smoke tests) do motor de inferência. Graças ao cabeçalho que
insere a raiz do `backend/` no path e ajusta o `cwd`, podem ser executados de
qualquer diretório com o venv do backend.

| Script | O que testa | Precisa de |
|---|---|---|
| `testar_direto.py` | `inference_service` diretamente (sem HTTP) | modelo + `datasets/processed/val` |
| `testar_view.py` | `InferirImagemView` via Django Test Client | Django + modelo + `datasets/processed/val` |
| `testar_inferencia.py` | endpoint HTTP `POST /api/diagnostico/inferir/` | servidor rodando em `localhost:8080` |

`test_leaf.jpg` — imagem de fixture avulsa (mantida aqui como apoio).

## Uso
```bash
# a partir da raiz do repositório
backend/venv/Scripts/python.exe backend/scripts/testes/testar_direto.py

# testar_inferencia.py exige o servidor no ar:
backend/venv/Scripts/python.exe backend/manage.py runserver 0.0.0.0:8080 --settings=ceres_core.settings_notebook
backend/venv/Scripts/python.exe backend/scripts/testes/testar_inferencia.py
```

Última validação: os 3 scripts retornaram **CORRETO** (D01_requeima, 85,7%).
