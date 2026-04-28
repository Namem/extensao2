@echo off
REM Ceres Diagnostico — Download PlantVillage via Kaggle CLI
REM Pre-requisito: C:\Users\%USERNAME%\.kaggle\kaggle.json deve existir
REM Obtencao: kaggle.com -> Settings -> API -> Create New Token

echo [1/3] Verificando kaggle.json...
if not exist "%USERPROFILE%\.kaggle\kaggle.json" (
    echo ERRO: kaggle.json nao encontrado em %USERPROFILE%\.kaggle\
    echo Acesse kaggle.com ^> Settings ^> API ^> Create New Token
    echo Salve o arquivo baixado em: %USERPROFILE%\.kaggle\kaggle.json
    pause
    exit /b 1
)

echo [2/3] Baixando PlantVillage (~1.2 GB)...
kaggle datasets download abdallahalidev/plantvillage-dataset ^
    -p backend\datasets\raw\ --unzip

echo [3/3] Verificando pasta de tomate...
if exist "backend\datasets\raw\plantvillage dataset\color\Tomato_healthy" (
    echo OK - Dataset extraido com sucesso!
    echo Proximo passo: python backend\datasets\scripts\prepare_plantvillage.py
) else (
    echo AVISO: Pasta de tomate nao encontrada. Verifique a extracao.
)
pause
