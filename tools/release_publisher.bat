@echo off
setlocal
title Semitone Resonance - GitHub Release Publisher

set "SCRIPT_DIR=%~dp0"
set "PY_EXEC="
set "PYW_EXEC="

:: 1. Prefer pythonw / python in PATH
where pythonw >nul 2>nul
if %errorlevel% equ 0 (
    set "PYW_EXEC=pythonw"
)
where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_EXEC=python"
    goto :launch
)

:: 2. Try py launcher
where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_EXEC=py"
    goto :launch
)

:: 3. Check standard Python installations
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXEC=%%D\python.exe"
        if exist "%%D\pythonw.exe" set "PYW_EXEC=%%D\pythonw.exe"
        goto :launch
    )
)

for /d %%D in ("%ProgramFiles%\Python*") do (
    if exist "%%D\python.exe" (
        set "PY_EXEC=%%D\python.exe"
        if exist "%%D\pythonw.exe" set "PYW_EXEC=%%D\pythonw.exe"
        goto :launch
    )
)

:launch
if "%PY_EXEC%"=="" (
    echo [ERROR] Python 3 not found on your system!
    pause
    exit /b 1
)

if not "%1"=="" (
    "%PY_EXEC%" "%SCRIPT_DIR%release_publisher.py" %*
    if %errorlevel% neq 0 pause
    exit /b %errorlevel%
)

if not "%PYW_EXEC%"=="" (
    start "" "%PYW_EXEC%" "%SCRIPT_DIR%release_publisher.py"
    exit /b 0
)

"%PY_EXEC%" "%SCRIPT_DIR%release_publisher.py"
if %errorlevel% neq 0 pause
