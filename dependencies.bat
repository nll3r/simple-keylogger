@echo off

:: Verificar se o Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python não está instalado. Instalando...
    start https://www.python.org/downloads/
    exit /b
)

:: Verificar se o pip está instalado
python -m ensurepip --upgrade >nul 2>&1
if %errorlevel% neq 0 (
    echo pip não está instalado. Instalando...
    python -m ensurepip --upgrade
)

:: Instalar as bibliotecas necessárias
echo Instalando bibliotecas necessárias...
pip install keyboard requests pygetwindow

echo Bibliotecas instaladas com sucesso!


