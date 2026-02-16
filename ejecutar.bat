@echo off
REM Script para ejecutar MultiMinecraft Launcher activando el entorno virtual
echo ========================================
echo MultiMinecraft Launcher
echo Activando entorno virtual...
echo ========================================

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Activar el entorno virtual
call venv\Scripts\activate.bat

REM Verificar que el entorno virtual se activó correctamente
if errorlevel 1 (
    echo ERROR: No se pudo activar el entorno virtual
    echo Asegurate de que el entorno virtual existe en: venv
    pause
    exit /b 1
)

REM Ejecutar el launcher
echo.
echo Ejecutando MultiMinecraft Launcher...
echo.
python MultiMinecraft.py

REM Si hay un error, mantener la ventana abierta
if errorlevel 1 (
    echo.
    echo ERROR: El launcher se cerró con un error
    pause
)

REM Desactivar el entorno virtual al salir
deactivate

