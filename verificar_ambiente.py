"""
verificar_ambiente.py — Checklist de ambiente do projeto Ceres Diagnostico

Verifica tudo que e necessario para continuar o desenvolvimento em qualquer
maquina (PC desktop, notebook, WSL2). Roda sem dependencias externas.

Uso:
    python verificar_ambiente.py          # verifica tudo
    python verificar_ambiente.py --fix    # tenta corrigir o que for possivel
    python verificar_ambiente.py --wsl    # inclui verificacoes de GPU/WSL2

Saida: relatorio no terminal + arquivo check_report.txt
"""

import sys
import os
import subprocess
import socket
import importlib
import argparse
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuracao
# ---------------------------------------------------------------------------

RAIZ    = Path(__file__).resolve().parent
BACKEND = RAIZ / "backend"

parser = argparse.ArgumentParser(description="Verificador de ambiente Ceres")
parser.add_argument("--fix",  action="store_true", help="Tentar corrigir problemas automaticamente")
parser.add_argument("--wsl",  action="store_true", help="Incluir verificacoes GPU/WSL2 (Linux)")
parser.add_argument("--json", action="store_true", help="Salvar resultado em check_report.json")
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

VERDE    = "\033[92m"
AMARELO  = "\033[93m"
VERMELHO = "\033[91m"
AZUL     = "\033[94m"
RESET    = "\033[0m"
NEGRITO  = "\033[1m"

def ok(msg):    print(f"  {VERDE}[OK]{RESET}  {msg}")
def warn(msg):  print(f"  {AMARELO}[AV]{RESET}  {msg}")
def erro(msg):  print(f"  {VERMELHO}[XX]{RESET}  {msg}")
def info(msg):  print(f"  {AZUL}[--]{RESET}  {msg}")
def titulo(msg): print(f"\n{NEGRITO}{msg}{RESET}")

resultados = []   # lista de (status, item, detalhe)

def check(status: str, item: str, detalhe: str = ""):
    """Registra resultado: 'ok' | 'warn' | 'erro'"""
    resultados.append((status, item, detalhe))
    if status == "ok":   ok(f"{item}  {detalhe}")
    elif status == "warn": warn(f"{item}  {detalhe}")
    else:                  erro(f"{item}  {detalhe}")

# ---------------------------------------------------------------------------
# 1. Python
# ---------------------------------------------------------------------------

titulo("1. Python")

v = sys.version_info
versao_str = f"{v.major}.{v.minor}.{v.micro}"
if v.major == 3 and v.minor >= 10:
    check("ok", f"Python {versao_str}", "(>= 3.10)")
else:
    check("erro", f"Python {versao_str}", "— precisa >= 3.10. Baixe em python.org")

plataforma = "WSL2/Linux" if sys.platform == "linux" else ("Windows" if sys.platform == "win32" else sys.platform)
info(f"Plataforma: {plataforma}")

# ---------------------------------------------------------------------------
# 2. Ambiente virtual
# ---------------------------------------------------------------------------

titulo("2. Ambiente virtual")

venv_windows = BACKEND / "venv"
venv_wsl     = Path.home() / "venv_ceres"
em_venv      = sys.prefix != sys.base_prefix

if em_venv:
    check("ok", f"venv ativa: {sys.prefix}")
else:
    check("warn", "Nenhum venv ativo",
          "— ative com: backend\\venv\\Scripts\\activate  (Windows)"
          " ou  source ~/venv_ceres/bin/activate  (WSL2)")

if venv_windows.exists():
    check("ok", f"backend/venv/ existe (Windows)")
else:
    check("warn", "backend/venv/ nao encontrado",
          "— crie com: python -m venv backend/venv")

if sys.platform == "linux" and venv_wsl.exists():
    check("ok", f"~/venv_ceres existe (WSL2)")
elif sys.platform == "linux":
    check("warn", "~/venv_ceres nao encontrado",
          "— crie com: python3 -m venv ~/venv_ceres")

# ---------------------------------------------------------------------------
# 3. Pacotes Python essenciais
# ---------------------------------------------------------------------------

titulo("3. Pacotes Python")

PACOTES = {
    # (modulo_import, nome_pip, obrigatorio)
    "django"               : ("django",              "Django>=6.0",            True),
    "rest_framework"       : ("rest_framework",      "djangorestframework",    True),
    "rest_framework_simplejwt": ("rest_framework_simplejwt", "djangorestframework-simplejwt", True),
    "psycopg2"             : ("psycopg2",             "psycopg2-binary",        True),
    "dotenv"               : ("dotenv",               "python-dotenv",          True),
    "paho.mqtt.client"     : ("paho.mqtt.client",     "paho-mqtt>=2.0",         True),
    "PIL"                  : ("PIL",                  "Pillow",                 True),
    "numpy"                : ("numpy",                "numpy",                  True),
    "tflite_runtime"       : ("tflite_runtime",       "tflite-runtime  (ou tensorflow)", False),
    "tensorflow"           : ("tensorflow",           "tensorflow",             False),
    "tqdm"                 : ("tqdm",                 "tqdm",                   False),
    "rembg"                : ("rembg",                "rembg",                  False),
    "openpyxl"             : ("openpyxl",             "openpyxl",               False),
}

faltam_obrigatorios = []
faltam_opcionais    = []

for modulo, (import_path, pip_name, obrigatorio) in PACOTES.items():
    try:
        importlib.import_module(import_path.split(".")[0])
        check("ok", import_path)
    except ImportError:
        if obrigatorio:
            check("erro", import_path, f"— pip install {pip_name}")
            faltam_obrigatorios.append(pip_name)
        else:
            check("warn", import_path, f"(opcional) — pip install {pip_name}")
            faltam_opcionais.append(pip_name)

if args.fix and faltam_obrigatorios:
    print(f"\n  Instalando obrigatorios: {faltam_obrigatorios}")
    subprocess.run(
        [sys.executable, "-m", "pip", "install"] + faltam_obrigatorios,
        check=False
    )

# ---------------------------------------------------------------------------
# 4. Arquivo .env
# ---------------------------------------------------------------------------

titulo("4. Configuracao (.env)")

env_path     = BACKEND / ".env"
env_example  = BACKEND / ".env.example"

if env_path.exists():
    check("ok", "backend/.env existe")
    # Verificar variaveis obrigatorias
    conteudo = env_path.read_text(encoding="utf-8", errors="ignore")
    for var in ["SECRET_KEY", "DB_NAME", "DB_USER", "DB_PASSWORD"]:
        if var in conteudo:
            check("ok", f"  {var} definida")
        else:
            check("erro", f"  {var} nao encontrada no .env")
else:
    check("erro", "backend/.env nao encontrado")
    if env_example.exists():
        info("  .env.example encontrado — copie e edite:")
        info("  copy backend\\.env.example backend\\.env  (Windows)")
        info("  cp backend/.env.example backend/.env      (Linux)")
        if args.fix:
            import shutil
            shutil.copy(env_example, env_path)
            warn("  .env criado a partir do .env.example — edite as senhas!")
    else:
        info("  Crie backend/.env com: SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT=5433")

# ---------------------------------------------------------------------------
# 5. PostgreSQL
# ---------------------------------------------------------------------------

titulo("5. PostgreSQL (porta 5433)")

def checar_porta(host: str, porta: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, porta), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

if checar_porta("localhost", 5433):
    check("ok", "PostgreSQL respondendo em localhost:5433")
else:
    check("erro", "PostgreSQL nao encontrado na porta 5433",
          "— inicie o servico: net start postgresql-x64-18  (Windows)")

# ---------------------------------------------------------------------------
# 6. Mosquitto MQTT (porta 1883)
# ---------------------------------------------------------------------------

titulo("6. Mosquitto MQTT (porta 1883)")

if checar_porta("localhost", 1883):
    check("ok", "Mosquitto respondendo em localhost:1883")
else:
    check("warn", "Mosquitto nao encontrado na porta 1883",
          "— inicie: net start mosquitto  (Windows) "
          "ou  mosquitto -d  (Linux)")

# ---------------------------------------------------------------------------
# 7. Modelo TFLite
# ---------------------------------------------------------------------------

titulo("7. Modelo TFLite (modelo principal)")

modelo_int8 = BACKEND / "datasets" / "modelo" / "ceres_mobilenetv2_int8.tflite"
modelo_ei   = BACKEND / "datasets" / "modelo" / "ei_ceres_int8.tflite"

if modelo_int8.exists():
    tamanho = modelo_int8.stat().st_size / 1024
    check("ok", f"ceres_mobilenetv2_int8.tflite ({tamanho:.0f} KB) — Exp B, modelo escolhido")
else:
    check("erro", "ceres_mobilenetv2_int8.tflite nao encontrado",
          "— faca git pull ou retreine com train_local.py (WSL2)")

if modelo_ei.exists():
    check("ok", "ei_ceres_int8.tflite (Exp A — arquivado)")
else:
    check("warn", "ei_ceres_int8.tflite nao encontrado (opcional — Exp A)")

# ---------------------------------------------------------------------------
# 8. Datasets
# ---------------------------------------------------------------------------

titulo("8. Datasets")

# PlantVillage processado
processed_train = BACKEND / "datasets" / "processed" / "train"
if processed_train.exists():
    n_classes = len([p for p in processed_train.iterdir() if p.is_dir()])
    n_imgs    = sum(1 for p in processed_train.rglob("*.jpg"))
    if n_classes >= 10 and n_imgs > 80000:
        check("ok", f"processed/train: {n_classes} classes, ~{n_imgs:,} imagens")
    else:
        check("warn", f"processed/train incompleto: {n_classes} classes, {n_imgs:,} imgs",
              "— re-execute prepare_plantvillage.py")
else:
    check("erro", "datasets/processed/ nao encontrado",
          "— execute: python backend/datasets/scripts/prepare_plantvillage.py"
          "\n           (precisa do PlantVillage em datasets/raw/)")

# PlantDoc
plantdoc = BACKEND / "datasets" / "raw" / "plantdoc" / "train"
if plantdoc.exists():
    n_pd = sum(1 for p in plantdoc.rglob("*.jpg"))
    check("ok", f"plantdoc/train: ~{n_pd:,} imagens de campo real")
else:
    check("warn", "datasets/raw/plantdoc/ nao encontrado",
          "— copie o PlantDoc para datasets/raw/plantdoc/"
          "\n           (necessario para background_augment.py e avaliar_plantdoc.py)")

# processed_field (background augmentation)
processed_field = BACKEND / "datasets" / "processed_field" / "train"
if processed_field.exists():
    n_field = sum(1 for p in processed_field.rglob("*.jpg"))
    check("ok", f"processed_field/train: ~{n_field:,} imagens (background aug)")
else:
    check("warn", "datasets/processed_field/ nao encontrado",
          "— execute: python backend/datasets/scripts/background_augment.py"
          "\n           (gera dataset com fundos naturais para melhorar acuracia campo)")

# PlantVillage raw (so verifica existencia, nao conta)
pv_raw = BACKEND / "datasets" / "raw"
if pv_raw.exists():
    check("ok", "datasets/raw/ existe")
else:
    check("warn", "datasets/raw/ nao encontrado",
          "— baixe o PlantVillage: kaggle datasets download abdallahalidev/plantvillage-dataset")

# ---------------------------------------------------------------------------
# 9. Scripts essenciais
# ---------------------------------------------------------------------------

titulo("9. Scripts essenciais")

SCRIPTS = {
    "prepare_plantvillage.py" : "prepara dataset PlantVillage",
    "train_local.py"          : "treinamento MobileNetV2 (WSL2)",
    "export_tflite.py"        : "exportacao TFLite INT8",
    "avaliar_plantdoc.py"     : "avaliacao campo real PlantDoc",
    "background_augment.py"   : "background augmentation (resolver gap lab-campo)",
}

scripts_dir = BACKEND / "datasets" / "scripts"
for nome, descricao in SCRIPTS.items():
    caminho = scripts_dir / nome
    if caminho.exists():
        check("ok", f"{nome}  ({descricao})")
    else:
        check("erro", f"{nome} nao encontrado", f"— {descricao}")

# ---------------------------------------------------------------------------
# 10. GPU / WSL2 (apenas se --wsl ou se estiver no Linux)
# ---------------------------------------------------------------------------

if args.wsl or sys.platform == "linux":
    titulo("10. GPU / WSL2")

    # nvidia-smi
    try:
        resultado = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10
        )
        if resultado.returncode == 0 and resultado.stdout.strip():
            gpu_info = resultado.stdout.strip().split("\n")[0]
            check("ok", f"GPU detectada: {gpu_info}")
        else:
            check("warn", "nvidia-smi falhou", "— GPU pode nao estar disponivel no WSL2")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        check("warn", "nvidia-smi nao encontrado", "— GPU nao disponivel ou driver nao instalado")

    # TensorFlow GPU
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            check("ok", f"TensorFlow detectou {len(gpus)} GPU(s): {[g.name for g in gpus]}")
        else:
            check("warn", "TensorFlow sem GPU",
                  "— configure LD_LIBRARY_PATH (veja CLAUDE.md secao WSL2)")
    except ImportError:
        check("warn", "TensorFlow nao instalado no ambiente atual",
              "— instale no venv WSL2: pip install tensorflow[and-cuda]")

    # LD_LIBRARY_PATH
    ld = os.environ.get("LD_LIBRARY_PATH", "")
    if "nvidia" in ld.lower() or "cuda" in ld.lower():
        check("ok", "LD_LIBRARY_PATH contem paths nvidia/CUDA")
    else:
        check("warn", "LD_LIBRARY_PATH sem paths CUDA",
              "— adicione ao ~/.bashrc conforme CLAUDE.md")

# ---------------------------------------------------------------------------
# 11. Git
# ---------------------------------------------------------------------------

titulo("11. Git")

try:
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, cwd=str(RAIZ), timeout=10
    ).stdout.strip()
    check("ok", f"Branch atual: {branch or '(detached HEAD)'}")

    status = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True, cwd=str(RAIZ), timeout=10
    ).stdout.strip()
    n_modificados = len(status.splitlines()) if status else 0
    if n_modificados == 0:
        check("ok", "Sem arquivos modificados nao commitados")
    else:
        check("warn", f"{n_modificados} arquivo(s) modificado(s) nao commitados",
              "— faca git add + git commit antes de mudar de maquina")

    # Verificar se esta atualizado com o remoto
    fetch = subprocess.run(
        ["git", "fetch", "--dry-run"],
        capture_output=True, text=True, cwd=str(RAIZ), timeout=15
    )
    log_tras = subprocess.run(
        ["git", "log", "HEAD..origin/main", "--oneline"],
        capture_output=True, text=True, cwd=str(RAIZ), timeout=10
    ).stdout.strip()
    if log_tras:
        n_atras = len(log_tras.splitlines())
        check("warn", f"Repositorio {n_atras} commit(s) atras do origin/main",
              "— faca git pull antes de continuar")
    else:
        check("ok", "Repositorio atualizado com origin/main")

except (FileNotFoundError, subprocess.TimeoutExpired):
    check("warn", "git nao encontrado ou timeout", "— instale o Git")

# ---------------------------------------------------------------------------
# Relatorio final
# ---------------------------------------------------------------------------

total  = len(resultados)
n_ok   = sum(1 for s, _, _ in resultados if s == "ok")
n_warn = sum(1 for s, _, _ in resultados if s == "warn")
n_err  = sum(1 for s, _, _ in resultados if s == "erro")

print()
print("=" * 60)
print(f"{NEGRITO}RESULTADO FINAL{RESET}")
print("=" * 60)
print(f"  {VERDE}OK    {RESET}: {n_ok}")
print(f"  {AMARELO}Avisos{RESET}: {n_warn}")
print(f"  {VERMELHO}Erros {RESET}: {n_err}")
print()

if n_err == 0 and n_warn == 0:
    print(f"  {VERDE}{NEGRITO}Ambiente completo — pode continuar o desenvolvimento!{RESET}")
elif n_err == 0:
    print(f"  {AMARELO}{NEGRITO}Ambiente funcional com avisos — verifique os [AV] acima.{RESET}")
else:
    print(f"  {VERMELHO}{NEGRITO}Problemas encontrados — resolva os [XX] antes de continuar.{RESET}")

print()

# Acoes prioritarias
if n_err > 0 or n_warn > 0:
    print(f"{NEGRITO}Acoes prioritarias:{RESET}")
    for status, item, detalhe in resultados:
        if status == "erro":
            print(f"  {VERMELHO}-> {item}{RESET}")
            if detalhe:
                for linha in detalhe.split("\n"):
                    print(f"     {linha.strip()}")
    for status, item, detalhe in resultados:
        if status == "warn":
            print(f"  {AMARELO}-> {item}{RESET}")
            if detalhe:
                for linha in detalhe.split("\n"):
                    print(f"     {linha.strip()}")

# ---------------------------------------------------------------------------
# Salvar relatorio em arquivo
# ---------------------------------------------------------------------------

relatorio_path = RAIZ / "check_report.txt"
with open(relatorio_path, "w", encoding="utf-8") as f:
    f.write(f"Ceres Diagnostico — Verificacao de Ambiente\n")
    f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"Maquina: {os.environ.get('COMPUTERNAME', os.uname().nodename if hasattr(os, 'uname') else 'desconhecida')}\n")
    f.write(f"Python: {versao_str} | Plataforma: {plataforma}\n")
    f.write("=" * 60 + "\n\n")
    for status, item, detalhe in resultados:
        simbolo = "OK  " if status == "ok" else ("AVISO" if status == "warn" else "ERRO ")
        f.write(f"[{simbolo}] {item}\n")
        if detalhe:
            for linha in detalhe.split("\n"):
                f.write(f"         {linha.strip()}\n")
    f.write(f"\nRESUMO: {n_ok} OK | {n_warn} avisos | {n_err} erros\n")

print(f"\n  Relatorio salvo em: {relatorio_path}")
print()

# Codigo de saida: 0 se sem erros, 1 se tiver erros
sys.exit(0 if n_err == 0 else 1)
