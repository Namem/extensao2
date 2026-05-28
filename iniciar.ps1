# iniciar.ps1 - Sobe Django (venv) + Flutter Windows desktop
# Uso: .\iniciar.ps1

$root     = Split-Path -Parent $MyInvocation.MyCommand.Path
$appCeres = "$root\app_ceres"
$backend  = "$root\backend"
$flutter  = "C:\Users\Namem\flutter\bin\flutter.bat"
$settings = "ceres_core.settings_notebook"

Write-Host ""
Write-Host "=== Ceres Diagnostico - PC (sem Docker) ===" -ForegroundColor Green
Write-Host ""

# 1. Verificar modelo TFLite
$modelo = "$backend\datasets\modelo\ceres_expe_int8.tflite"
if (-not (Test-Path $modelo)) {
    Write-Host "[ERRO] Modelo nao encontrado: $modelo" -ForegroundColor Red
    exit 1
}
$tamanhoKB = [int]((Get-Item $modelo).Length / 1KB)
Write-Host "[1/3] Modelo TFLite OK ($tamanhoKB KB) - ceres_expe_int8.tflite" -ForegroundColor Green

# 2. Django via venv (nova janela PowerShell)
Write-Host "[2/3] Iniciando Django na porta 8080..." -ForegroundColor Cyan
$djangoCmd = "Set-Location '$backend'; .\venv\Scripts\Activate.ps1; python manage.py runserver 0.0.0.0:8080 --settings=$settings --noreload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $djangoCmd

Write-Host "      Aguardando Django iniciar..." -ForegroundColor Gray
$djangoOk = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep 2
    try {
        $null = Invoke-WebRequest "http://localhost:8080/api/diagnostico/historico/" -TimeoutSec 2 -ErrorAction Stop
        $djangoOk = $true
        break
    } catch { }
}
if ($djangoOk) {
    Write-Host "      Django OK! http://localhost:8080" -ForegroundColor Green
} else {
    Write-Host "      Django ainda iniciando - verifique a janela de Django." -ForegroundColor Yellow
}

# 3. Flutter Windows desktop
Write-Host "[3/3] Iniciando Flutter (Windows desktop)..." -ForegroundColor Cyan
Write-Host "      Pressione q para encerrar o Flutter." -ForegroundColor Gray
Write-Host ""

Set-Location $appCeres
& $flutter run -d windows
