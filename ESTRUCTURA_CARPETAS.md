# 📁 ESTRUCTURA DE CARPETAS DEL PROYECTO

## MultiMinecraft Launcher - Estructura de Directorios

```
%APPDATA%\.MultiMinecraft_MS\
├── 📄 config.json                          ← Configuración global del launcher (GLOBAL)
├── 📄 settingsMM2.json                     ← Configuración de settings del launcher (GLOBAL)
├── 📁 logs/                                ← Logs globales del launcher (GLOBAL)
│   ├── 📄 latest.log                       ← Último log generado
│   ├── 📄 debug.log                        ← Logs de depuración
│   └── 📄 [fecha]-[número].log.gz         ← Logs comprimidos por fecha
├── 📁 cache/                               ← Cache del sistema (GLOBAL, opcional)
│   └── 📄 versions_cache.json              ← Cache de versiones de Minecraft (si se usa version_manager)
└── 📁 Instancias/                          ← Carpeta principal de instancias (GLOBAL)
    └── 📁 [NombreInstancia]/               ← Instancia individual de Minecraft
        ├── 📄 config.json                  ← Configuración de la instancia (nombre, usuario, versión, RAM, tipo)
        ├── 📄 launcher_profiles.json       ← Perfiles de launcher de la instancia
        ├── 📄 Instancias_profiles.json     ← Perfiles adicionales de la instancia (opcional)
        ├── 📁 versions/                    ← Versiones de Minecraft instaladas (POR INSTANCIA)
        │   ├── 📁 [version]/               ← Versión Vanilla (ej: 1.21.3)
        │   │   ├── 📄 [version].json       ← Archivo de configuración de la versión
        │   │   ├── 📄 [version].jar        ← Archivo ejecutable de la versión
        │   │   └── 📁 natives/             ← Librerías nativas de esta versión (POR VERSIÓN)
        │   │       ├── 📄 lwjgl.dll/.so/.dylib  ← Librería gráfica LWJGL
        │   │       ├── 📄 OpenAL32.dll/.so/.dylib  ← Librería de audio OpenAL
        │   │       ├── 📄 jinput-*.dll/.so/.dylib  ← Entrada de dispositivos
        │   │       └── 📄 [otros_nativos]  ← Otras librerías nativas según versión
        │   ├── 📁 [version]-forge-[forge_version]/  ← Versión Forge (ej: 1.20.1-forge-47.4.4)
        │   │   ├── 📄 [version]-forge-[forge_version].json  ← Configuración de Forge
        │   │   ├── 📄 [version]-forge-[forge_version].jar   ← Ejecutable de Forge
        │   │   └── 📁 natives/             ← Librerías nativas de Forge (POR VERSIÓN)
        │   │       └── 📄 [archivos_nativos_forge]  ← Natives específicas de Forge
        │   └── 📁 [version]-fabric-[fabric_version]/  ← Versión Fabric (ej: 1.20.1-fabric-0.15.7)
        │       ├── 📄 [version]-fabric-[fabric_version].json  ← Configuración de Fabric
        │       ├── 📄 [version]-fabric-[fabric_version].jar   ← Ejecutable de Fabric
        │       └── 📁 natives/             ← Librerías nativas de Fabric (POR VERSIÓN)
        │           └── 📄 [archivos_nativos_fabric]  ← Natives específicas de Fabric
        ├── 📁 assets/                      ← Texturas, sonidos, recursos (POR INSTANCIA)
        │   ├── 📁 indexes/                 ← Archivos de índice de assets
        │   │   └── 📄 [version].json       ← Índice de assets por versión
        │   └── 📁 objects/                 ← Archivos de assets organizados por hash
        │       └── 📁 [hash]/              ← Carpetas organizadas por hash (primeros 2 caracteres)
        │           └── 📄 [hash_completo]  ← Archivo de asset completo
        ├── 📁 libraries/                   ← Librerías Java específicas de la instancia (POR INSTANCIA)
        │   └── 📁 [organizacion]/          ← Librerías organizadas por paquete
        │       └── 📁 [libreria]/          ← Librerías específicas
        │           └── 📄 [version].jar    ← Archivos JAR de librerías
        ├── 📁 mods/                        ← Mods instalados en la instancia (POR INSTANCIA)
        │   └── 📄 [nombre_mod].jar         ← Archivos de mods
        ├── 📁 shaderpacks/                 ← Shader packs instalados (POR INSTANCIA)
        │   └── 📁 [nombre_shader]/         ← Carpeta de shader pack
        ├── 📁 resourcepacks/               ← Resource packs instalados (POR INSTANCIA)
        │   └── 📁 [nombre_resourcepack]/   ← Carpeta de resource pack
        ├── 📁 saves/                       ← Mundos guardados de Minecraft (POR INSTANCIA)
        │   └── 📁 [nombre_mundo]/          ← Carpeta de mundo guardado
        │       └── 📁 datapacks/           ← Datapacks del mundo (opcional)
        ├── 📁 config/                      ← Configuración de mods y Minecraft (POR INSTANCIA)
        │   └── 📄 [archivos_config]        ← Archivos de configuración de mods
        ├── 📁 logs/                        ← Logs de la instancia (POR INSTANCIA)
        │   └── 📄 latest.log               ← Último log de la instancia
        ├── 📁 natives/                     ← Librerías nativas compartidas (POR INSTANCIA, opcional)
        │   └── 📄 [archivos_nativos_compartidos]  ← Natives compartidas entre versiones (si aplica)
        ├── 📁 runtime/                     ← Runtime de Java de la instancia (POR INSTANCIA)
        │   └── 📁 [version_java]/          ← Versión específica de Java
        ├── 📄 options.txt                  ← Opciones de configuración de Minecraft (POR INSTANCIA)
        ├── 📁 screenshots/                    ← Capturas de pantalla (POR INSTANCIA)
        │   └── 📄 [fecha]_[hora].png       ← Capturas de pantalla
        ├── 📁 stats/                       ← Estadísticas del jugador (POR INSTANCIA)
        │   └── 📄 [uuid].json              ← Estadísticas por jugador
        └── 📁 crash-reports/               ← Reportes de crash (POR INSTANCIA)
            └── 📄 crash-[fecha]_[hora].txt ← Reportes de errores
```

## 📋 Descripción de Carpetas y Archivos

### 🔷 Nivel Global (`.MultiMinecraft_MS`)

| Carpeta/Archivo | Descripción | Tipo |
|----------------|-------------|------|
| `config.json` | Configuración global del launcher (preferencias, ajustes generales) | GLOBAL |
| `settingsMM2.json` | Configuración de settings avanzados del launcher | GLOBAL |
| `logs/` | Logs globales del launcher y sistema | GLOBAL |
| `cache/` | Cache del sistema (versiones, metadatos) - Solo si se usa version_manager | GLOBAL (opcional) |
| `Instancias/` | Contenedor principal de todas las instancias de Minecraft | GLOBAL |

### 🔷 Nivel de Instancia (`Instancias/[NombreInstancia]/`)

| Carpeta/Archivo | Descripción | Tipo |
|----------------|-------------|------|
| `config.json` | Configuración específica de la instancia (nombre, usuario, versión, RAM, tipo, último uso) | POR INSTANCIA |
| `launcher_profiles.json` | Perfiles de launcher de Minecraft para esta instancia | POR INSTANCIA |
| `Instancias_profiles.json` | Perfiles adicionales de la instancia (opcional) | POR INSTANCIA |
| `versions/` | Versiones de Minecraft instaladas en esta instancia (Vanilla, Forge, Fabric) | POR INSTANCIA |
| `assets/` | Recursos de Minecraft (texturas, sonidos, modelos) | POR INSTANCIA |
| `libraries/` | Librerías Java necesarias para ejecutar Minecraft | POR INSTANCIA |
| `mods/` | Mods instalados en esta instancia | POR INSTANCIA |
| `shaderpacks/` | Shader packs instalados en esta instancia | POR INSTANCIA |
| `resourcepacks/` | Resource packs instalados en esta instancia | POR INSTANCIA |
| `saves/` | Mundos guardados de esta instancia (incluye datapacks) | POR INSTANCIA |
| `options.txt` | Configuración de opciones de Minecraft (gráficos, controles, etc.) | POR INSTANCIA |
| `screenshots/` | Capturas de pantalla tomadas en el juego | POR INSTANCIA |
| `stats/` | Estadísticas del jugador (tiempo jugado, bloques minados, etc.) | POR INSTANCIA |
| `crash-reports/` | Reportes de crash cuando el juego falla | POR INSTANCIA |
| `config/` | Configuración de mods y ajustes de Minecraft | POR INSTANCIA |
| `logs/` | Logs específicos de esta instancia | POR INSTANCIA |
| `versions/[version]/natives/` | Librerías nativas específicas de cada versión (LWJGL, OpenAL, jinput, etc.) | POR VERSIÓN |
| `natives/` | Librerías nativas compartidas (opcional, puede no existir) | POR INSTANCIA |
| `runtime/` | Runtime de Java específico de la instancia | POR INSTANCIA |

## 🔍 Notas Importantes

1. **Ruta Base**: La ruta base del launcher es `%APPDATA%\.MultiMinecraft_MS` (equivalente a `C:\Users\[Usuario]\AppData\Roaming\.MultiMinecraft_MS`)

2. **Aislamiento de Instancias**: Cada instancia tiene sus propias carpetas de `versions/`, `assets/`, `libraries/`, `mods/`, etc., lo que permite tener múltiples versiones y configuraciones sin conflictos.

3. **Archivos de Configuración**:
   - `config.json` (global): Configuración del launcher
   - `config.json` (instancia): Configuración específica de cada instancia
   - `launcher_profiles.json`: Perfiles de Minecraft para la instancia
   - `options.txt`: Opciones de Minecraft (gráficos, controles, audio, etc.)

4. **Versiones de Minecraft**:
   - **Vanilla**: Versiones puras de Minecraft (ej: `1.21.3`)
   - **Forge**: Versiones con Forge instalado (ej: `1.20.1-forge-47.4.4`)
   - **Fabric**: Versiones con Fabric instalado (ej: `1.20.1-fabric-0.15.7`)
   - Cada tipo de versión tiene su propia carpeta en `versions/` con archivos `.json` y `.jar` específicos

5. **Cache**: 
   - El sistema utiliza un cache en memoria para optimizar las operaciones de carga de instancias (5 segundos de duración)
   - Si se usa `version_manager.py`, se crea una carpeta `cache/` en el directorio del proyecto (no en AppData) con `versions_cache.json`
   - La carpeta `cache/` en AppData es opcional y solo se crea si se usa el version_manager con esa ubicación

6. **Logs**: Los logs se organizan en dos niveles:
   - Logs globales del launcher en `logs/`
   - Logs específicos de cada instancia en `Instancias/[NombreInstancia]/logs/`

7. **Carpetas Generadas por Minecraft**: Algunas carpetas se crean automáticamente cuando se ejecuta Minecraft:
   - `options.txt`: Se crea al iniciar Minecraft por primera vez
   - `screenshots/`: Se crea cuando se toma la primera captura
   - `stats/`: Se crea cuando se juega por primera vez
   - `crash-reports/`: Se crea cuando ocurre un crash

8. **Librerías Nativas (natives/)**: Las natives son librerías específicas del sistema operativo extraídas de las librerías Java:
   - **Ubicación Principal**: Cada versión tiene su propia carpeta `natives/` dentro de `versions/[version]/natives/`
   - **Windows**: Archivos `.dll` (lwjgl.dll, OpenAL32.dll, jinput-dx8_64.dll, etc.)
   - **Linux**: Archivos `.so` (lwjgl.so, libopenal.so, libjinput-linux64.so, etc.)
   - **macOS**: Archivos `.dylib` o `.jnilib` (lwjgl.dylib, libopenal.dylib, libjinput-osx.jnilib, etc.)
   - Se extraen automáticamente durante la instalación de cada versión específica
   - Incluyen librerías para gráficos (LWJGL), audio (OpenAL) y entrada de dispositivos (jinput)
   - Cada versión (Vanilla, Forge, Fabric) tiene sus propias natives específicas
   - Puede existir una carpeta `natives/` a nivel de instancia para natives compartidas (opcional)

9. **Carpetas Temporales**: El sistema puede crear carpetas temporales durante operaciones específicas:
   - `Instancias/temp_versions/`: Carpeta temporal para verificar versiones disponibles (se elimina automáticamente)
   - Estas carpetas temporales no deben aparecer en el diagrama ya que son efímeras

10. **Estructura de Assets**: Los assets se organizan de forma jerárquica:
    - `assets/indexes/`: Contiene archivos JSON que indexan todos los assets de cada versión
    - `assets/objects/`: Contiene los archivos reales organizados por hash (primeros 2 caracteres del hash como nombre de carpeta)

## 🚀 Características del Sistema

- ✅ **Multidescarga**: Descarga paralela de assets, librerías y versiones
- ✅ **Instancias Aisladas**: Cada instancia es completamente independiente
- ✅ **Gestión de Versiones**: Soporte para versiones vanilla, Forge y Fabric
- ✅ **Cache Inteligente**: Sistema de cache para optimizar rendimiento
- ✅ **Logs Detallados**: Sistema de logging completo en múltiples niveles
