# Instrucciones de Compilación - MultiMinecraft Launcher

Esta guía te ayudará a compilar el instalador profesional del launcher.

## Requisitos Previos

### 1. Python 3.8 o superior
- Descarga desde: https://www.python.org/downloads/
- Asegúrate de marcar "Add Python to PATH" durante la instalación

### 2. PyInstaller
Se instalará automáticamente si no está presente, o puedes instalarlo manualmente:
```bash
pip install pyinstaller
```

### 3. Inno Setup (Requerido para el instalador)
- Descarga desde: https://jrsoftware.org/isdl.php
- Instala la versión 6 o superior
- El script de compilación buscará Inno Setup en:
  - `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`
  - `C:\Program Files\Inno Setup 6\ISCC.exe`
  - Si está en otra ubicación, modifica `build_installer.bat`

### 4. Todas las dependencias del proyecto
Asegúrate de tener instaladas todas las dependencias:
```bash
pip install -r requirements.txt
```

## Proceso de Compilación

### Método Automático (Recomendado)

1. Abre una terminal en el directorio del proyecto
2. Ejecuta:
   ```bash
   build_installer.bat
   ```

El script automáticamente:
- Limpiará compilaciones anteriores
- Ejecutará PyInstaller para crear el ejecutable
- Compilará el instalador con Inno Setup
- El instalador final estará en `dist\MultiMinecraft_Installer.exe`

### Método Manual

Si prefieres hacerlo paso a paso:

#### Paso 1: Compilar con PyInstaller
```bash
python -m PyInstaller MultiMinecraft.spec
```

Esto creará el ejecutable en `dist\MultiMinecraft\`

#### Paso 2: Compilar el Instalador con Inno Setup
1. Abre Inno Setup Compiler
2. Abre el archivo `setup.iss`
3. Haz clic en "Build" > "Compile" (o presiona F9)
4. El instalador se generará en `dist\MultiMinecraft_Installer.exe`

## Estructura de Archivos Después de la Compilación

```
dist/
├── MultiMinecraft/              ← Ejecutable y dependencias (PyInstaller)
│   ├── MultiMinecraft.exe
│   ├── _internal/
│   └── Resources/
└── MultiMinecraft_Installer.exe  ← Instalador final (Inno Setup)
```

## Solución de Problemas

### Error: "PyInstaller no está instalado"
```bash
pip install pyinstaller
```

### Error: "Inno Setup no encontrado"
- Instala Inno Setup desde: https://jrsoftware.org/isdl.php
- O modifica `build_installer.bat` con la ruta correcta a `ISCC.exe`

### Error: "ModuleNotFoundError" durante la compilación
- Asegúrate de tener todas las dependencias instaladas:
  ```bash
  pip install -r requirements.txt
  ```

### El ejecutable no encuentra los recursos (iconos, imágenes)
- Verifica que `MultiMinecraft.spec` incluya `('Resources', 'Resources')` en `datas`
- Asegúrate de que la función `get_resource_path()` esté correctamente implementada

### El instalador no se crea
- Verifica que Inno Setup esté instalado correctamente
- Revisa que el archivo `setup.iss` esté en el directorio raíz
- Verifica que el ejecutable de PyInstaller esté en `dist\MultiMinecraft\`

## Personalización del Instalador

### Cambiar el nombre de la aplicación
Edita `setup.iss` y modifica:
```iss
#define MyAppName "Tu Nombre Aquí"
```

### Cambiar la versión
Edita `setup.iss`:
```iss
#define MyAppVersion "1.0.0"
```

### Cambiar el icono del instalador
Asegúrate de que `Resources\icon.ico` exista y esté configurado en:
```iss
SetupIconFile=Resources\icon.ico
```

### Incluir Java en el instalador
Para incluir Java automáticamente, necesitarás:
1. Descargar Java Runtime portable
2. Agregarlo a la sección `[Files]` en `setup.iss`
3. Modificar el código para detectar y usar Java incluido

## Distribución

Una vez compilado, el archivo `dist\MultiMinecraft_Installer.exe` es todo lo que necesitas distribuir.

Los usuarios solo necesitan:
1. Ejecutar el instalador
2. Seguir las instrucciones del asistente
3. El launcher se instalará en `C:\Program Files\MultiMinecraft Launcher\`
4. Se crearán accesos directos en el escritorio y menú de inicio

## Notas Importantes

- **Datos del usuario**: Los datos del usuario (instancias, configuraciones) se guardan en `%APPDATA%\.MultiMinecraft_MS\` y NO se eliminan al desinstalar
- **Java**: El instalador verifica si Java está instalado, pero no lo instala automáticamente. Los usuarios deben tener Java instalado para jugar Minecraft
- **Permisos**: El instalador requiere permisos de administrador para instalar en Program Files

## Verificación

Después de compilar, prueba el instalador:
1. Ejecuta `dist\MultiMinecraft_Installer.exe`
2. Instala en una ubicación de prueba
3. Verifica que el launcher se ejecute correctamente
4. Verifica que los recursos (iconos) se carguen correctamente
5. Prueba crear una instancia de Minecraft

