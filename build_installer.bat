@echo off
REM Script de compilación automatizado para MultiMinecraft Launcher
REM Este script ejecuta PyInstaller y luego compila el instalador con Inno Setup

echo ========================================
echo Compilando MultiMinecraft Launcher
echo ========================================
echo.

REM Verificar que Python esté disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    pause
    exit /b 1
)

REM Verificar que PyInstaller esté instalado
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo PyInstaller no está instalado. Instalando...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERROR: No se pudo instalar PyInstaller
        pause
        exit /b 1
    )
)

REM Verificar que Inno Setup esté instalado
set "INNO_SETUP_PATH="
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "INNO_SETUP_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "INNO_SETUP_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
) else (
    echo ADVERTENCIA: Inno Setup no se encontró en las ubicaciones estándar
    echo Por favor, instala Inno Setup desde: https://jrsoftware.org/isdl.php
    echo O modifica este script con la ruta correcta a ISCC.exe
    echo.
    echo Continuando sin crear el instalador. El ejecutable ya está en dist\MultiMinecraft.exe
    pause
    exit /b 0
)

echo.
echo [1/3] Limpiando compilaciones anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist\MultiMinecraft" rmdir /s /q "dist\MultiMinecraft"
if exist "dist\MultiMinecraft_Installer.exe" del /q "dist\MultiMinecraft_Installer.exe"

echo.
echo [2/3] Ejecutando PyInstaller...
python -m PyInstaller MultiMinecraft.spec
if errorlevel 1 (
    echo ERROR: PyInstaller falló
    pause
    exit /b 1
)

echo.
echo [3/3] Compilando instalador con Inno Setup...
call "%INNO_SETUP_PATH%" setup.iss
if errorlevel 1 (
    echo ERROR: La compilación del instalador falló
    pause
    exit /b 1
)

echo.
echo ========================================
echo Compilación completada exitosamente!
echo ========================================
echo.
echo El instalador se encuentra en: dist\MultiMinecraft_Installer.exe
echo.
echo Versión: 1.1.0
echo Características incluidas:
echo   - Soporte mejorado para carpetas config
echo   - Diagnóstico de FancyMenu
echo   - Corrección de working directory
echo   - Verificación automática de configuraciones
echo.
pause

