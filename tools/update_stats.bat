@echo off
setlocal enabledelayedexpansion
title Ren'Py Script Stats Auto-Linter

echo ======================================================
echo    The Brightest Neon - Script & Dialogue Stats Auto-Linter
echo ======================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "ROOT_DIR=%SCRIPT_DIR%.."
set "PY_EXEC="

:: 1. Check if 'python' is in PATH
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_EXEC=python"
    goto :run
)

:: 2. Check if 'py' launcher is in PATH
where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_EXEC=py"
    goto :run
)

:: 3. Check Ren'Py SDK installations in Downloads or C:\
for /d %%D in ("%USERPROFILE%\Downloads\renpy-*") do (
    if exist "%%D\lib\py3-windows-x86_64\python.exe" (
        set "PY_EXEC=%%D\lib\py3-windows-x86_64\python.exe"
        goto :run
    )
)

for /d %%D in ("C:\renpy*") do (
    if exist "%%D\lib\py3-windows-x86_64\python.exe" (
        set "PY_EXEC=%%D\lib\py3-windows-x86_64\python.exe"
        goto :run
    )
)

:: 4. Check Standard Python installations
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXEC=%%D\python.exe"
        goto :run
    )
)

for /d %%D in ("%ProgramFiles%\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXEC=%%D\python.exe"
        goto :run
    )
)

:run
if "%PY_EXEC%"=="" (
    echo [ERROR] Python not found on your system!
    echo Please install Python 3 or make sure Ren'Py SDK is installed.
    echo.
    if not defined CI if not "%1"=="--no-pause" pause
    exit /b 1
)

echo [Found Python] Using: %PY_EXEC%
echo.

"%PY_EXEC%" "%SCRIPT_DIR%script_stats_linter.py" %*

echo.
echo ======================================================
echo Done!
echo ======================================================
if not defined CI if not "%1"=="--no-pause" pause
