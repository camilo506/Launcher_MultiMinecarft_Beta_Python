# Script PowerShell para ejecutar MultiMinecraft Launcher activando el entorno virtual
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MultiMinecraft Launcher" -ForegroundColor Cyan
Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del script
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Ruta del script de activación del entorno virtual
$activateScript = Join-Path $scriptDir "venv\Scripts\Activate.ps1"

# Verificar que el entorno virtual existe
if (-Not (Test-Path $activateScript)) {
    Write-Host "ERROR: No se encontró el entorno virtual en: venv" -ForegroundColor Red
    Write-Host "Asegurate de que el entorno virtual existe en: $activateScript" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Activar el entorno virtual
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow
& $activateScript

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: No se pudo activar el entorno virtual" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host ""
Write-Host "Ejecutando MultiMinecraft Launcher..." -ForegroundColor Green
Write-Host ""

# Ejecutar el launcher
python MultiMinecraft.py

# Si hay un error, mantener la ventana abierta
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: El launcher se cerró con un error" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
}

# Desactivar el entorno virtual al salir
deactivate

