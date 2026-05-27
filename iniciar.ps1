# iniciar.ps1 - Sobe emulador + Django (Docker) + Flutter com um comando
# Uso: .\iniciar.ps1
# Encerrar: pressione 'q' no Flutter

$root     = Split-Path -Parent $MyInvocation.MyCommand.Path
$appCeres = "$root\app_ceres"
$backend  = "$root\backend"
$flutter  = "C:\Users\Rachid\flutter\bin\flutter.bat"
$adb      = "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe"
$emulExe  = "$env:LOCALAPPDATA\Android\Sdk\emulator\emulator.exe"
$valDir   = "$backend\datasets\processed\val"
$avdName  = "Pixel8"

Write-Host ""
Write-Host "=== Ceres Diagnostico - iniciando ===" -ForegroundColor Green
Write-Host ""

# 1. EMULADOR
$devicesOut = & $adb devices 2>&1
$emulatorJaRodando = ($devicesOut -join "") -match "emulator"

if ($emulatorJaRodando) {
    Write-Host "[1/4] Emulador ja em execucao." -ForegroundColor Green
} else {
    Write-Host "[1/4] Iniciando emulador $avdName..." -ForegroundColor Cyan
    Start-Process $emulExe -ArgumentList "-avd $avdName -no-audio -no-boot-anim"
    Write-Host "      Aguardando boot do Android (30-60s)..." -ForegroundColor Gray
    $booted = $false
    for ($i = 0; $i -lt 60; $i++) {
        Start-Sleep 2
        $prop = & $adb shell getprop sys.boot_completed 2>$null
        if ($prop -match "1") { $booted = $true; break }
    }
    if ($booted) {
        Write-Host "      Emulador pronto!" -ForegroundColor Green
    } else {
        Write-Host "      Emulador ainda carregando - continuando..." -ForegroundColor Yellow
    }
}

# 2. FOTOS DE TESTE
Write-Host "[2/4] Enviando fotos de teste ao emulador..." -ForegroundColor Cyan
& $adb shell mkdir -p /sdcard/Pictures/Ceres 2>$null

$enviadas = 0
if (Test-Path $valDir) {
    $classes = Get-ChildItem $valDir -Directory
    foreach ($classe in $classes) {
        $img = Get-ChildItem $classe.FullName -Filter "*.jpg" | Select-Object -First 1
        if (-not $img) {
            $img = Get-ChildItem $classe.FullName -Filter "*.JPG" | Select-Object -First 1
        }
        if ($img) {
            $dest = "/sdcard/Pictures/Ceres/$($classe.Name).jpg"
            & $adb push $img.FullName $dest 2>$null
            $enviadas++
        }
    }
    & $adb shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d "file:///sdcard/Pictures/Ceres/" 2>$null
    Write-Host "      $enviadas fotos enviadas (1 por classe)." -ForegroundColor Green
} else {
    Write-Host "      Dataset val nao encontrado - pulando fotos." -ForegroundColor Yellow
}

# 3. DJANGO via Docker
Write-Host "[3/4] Subindo Django via Docker (porta 8080)..." -ForegroundColor Cyan

$portaEmUso = $false
try {
    $null = Invoke-WebRequest "http://localhost:8080/api/diagnostico/" -TimeoutSec 2 -ErrorAction Stop
    $portaEmUso = $true
} catch { }

if ($portaEmUso) {
    Write-Host "      Django ja esta rodando na porta 8080." -ForegroundColor Green
} else {
    Set-Location $root
    docker compose up -d --build
    Write-Host "      Aguardando Django iniciar..." -ForegroundColor Gray
    $djangoOk = $false
    for ($i = 0; $i -lt 15; $i++) {
        Start-Sleep 2
        try {
            $null = Invoke-WebRequest "http://localhost:8080/api/diagnostico/" -TimeoutSec 2 -ErrorAction Stop
            $djangoOk = $true
            break
        } catch { }
    }
    if ($djangoOk) {
        Write-Host "      Django OK!" -ForegroundColor Green
    } else {
        Write-Host "      Django ainda iniciando - verifique: docker compose logs django" -ForegroundColor Yellow
    }
}

# 4. FLUTTER
Write-Host "[4/4] Iniciando Flutter no emulador..." -ForegroundColor Cyan
Write-Host "      Pressione 'q' para encerrar Flutter (Django continua rodando)." -ForegroundColor Gray
Write-Host "      Para parar Django: docker compose down" -ForegroundColor Gray
Write-Host ""

Set-Location $appCeres
& $flutter run

Write-Host ""
Write-Host "Flutter encerrado." -ForegroundColor Yellow
Write-Host "Django continua rodando. Para parar: docker compose down" -ForegroundColor Gray
