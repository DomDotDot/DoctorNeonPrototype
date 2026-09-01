<#
.SYNOPSIS
    Ren'Py Script & Dialogue Stats Auto-Linter PowerShell Launcher
.DESCRIPTION
    Scans project scripts and updates README.md and README.ru.md with badges and stats.
#>

param(
    [switch]$Check,
    [switch]$Json,
    [switch]$Silent
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonExe = $null

# 1. Check PATH
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonExe = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonExe = "py"
}

# 2. Check Ren'Py SDKs
if (-not $pythonExe) {
    $sdkPaths = Get-ChildItem -Path "$env:USERPROFILE\Downloads\renpy-*", "C:\renpy*" -Directory -ErrorAction SilentlyContinue
    foreach ($sdk in $sdkPaths) {
        $pyPath = Join-Path $sdk.FullName "lib\py3-windows-x86_64\python.exe"
        if (Test-Path $pyPath) {
            $pythonExe = $pyPath
            break
        }
    }
}

# 3. Check AppData / Program Files
if (-not $pythonExe) {
    $stdPy = Get-ChildItem -Path "$env:LOCALAPPDATA\Programs\Python\Python*", "$env:ProgramFiles\Python*" -Filter "python.exe" -Recurse -ErrorAction SilentlyContinue
    if ($stdPy) {
        $pythonExe = $stdPy[0].FullName
    }
}

if (-not $pythonExe) {
    Write-Error "Python 3 was not found! Please install Python or Ren'Py SDK."
    exit 1
}

$linterScript = Join-Path $scriptDir "script_stats_linter.py"
$argsList = @()
if ($Check) { $argsList += "--check" }
if ($Json) { $argsList += "--json" }
if ($Silent) { $argsList += "--silent" }

& $pythonExe $linterScript @argsList
exit $LASTEXITCODE
