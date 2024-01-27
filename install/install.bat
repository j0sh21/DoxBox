@echo off


rem Check if pip is installed
pip --version 2>nul
if errorlevel 1 (
    echo Pip is not installed. Please install it.
    exit /b 1
)

rem Install packages from requirements.txt
pip install -r requirements.txt

rem Check the exit code of pip
if %errorlevel% equ 0 (
    echo Packages installed successfully.
) else (
    echo Error: Failed to install packages.
)
pause
