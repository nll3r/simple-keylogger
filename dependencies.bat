@echo off

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing...
    start https://www.python.org/downloads/
    exit /b
)

:: Check if pip is installed
python -m ensurepip --upgrade >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing...
    python -m ensurepip --upgrade
)

:: Install the required libraries
echo Installing required libraries...
pip install keyboard requests pygetwindow

echo Libraries installed successfully!
