#!/usr/bin/env python3
"""
Configuración centralizada para MultiMinecraft Launcher
"""

import os

# Configuración de optimización
MAX_WORKERS = 4  # Número de hilos para descargas paralelas
CHUNK_SIZE = 8192  # Tamaño de chunk para descargas
BUFFER_SIZE = 1024 * 1024  # 1MB buffer para operaciones de archivo
MAX_CONCURRENT_DOWNLOADS = 3  # Máximo de descargas simultáneas
MAX_CONCURRENT_INSTALLS = 2  # Máximo de instalaciones simultáneas

# Cache para optimizar operaciones repetitivas
CACHE_DURACION = 5  # Segundos que dura el cache

# Configuración de la interfaz
VENTANA_WIDTH = 700
VENTANA_HEIGHT = 500
TITULO_VENTANA = 'MultiMinecraft_v1.0'

# Configuración de rutas
def get_rutas():
    """Obtiene las rutas del sistema"""
    user_window = os.environ.get("USERNAME", "Usuario")
    launcher_root = f"C:/Users/{user_window}/AppData/Roaming/.MultiMinecraft"
    
    return {
        'launcher_root': launcher_root,
        'instancias_root': os.path.join(launcher_root, "Instancias"),
        'logs_dir': os.path.join(launcher_root, "logs"),
        'config_path': os.path.join(launcher_root, "config.json"),
        'settings_path': os.path.join(launcher_root, "settingsMM2.json")
    }

# Configuración de versiones soportadas (ahora dinámica)
# Las versiones se obtienen automáticamente desde la API oficial de Mojang
# Ver version_manager.py para el sistema dinámico

# Versiones de fallback en caso de que falle la API
VERSIONES_FALLBACK = {
    'vanilla': ['1.21.3', '1.20.4', '1.20.1', '1.19.4', '1.18.2', '1.17.1', '1.16.5', '1.15.2', '1.14.4', '1.13.2', '1.12.2', '1.11.2', '1.10.2', '1.9.4', '1.8.9', '1.7.10'],
    'forge': ['1.21.3-forge-49.0.0', '1.20.1-forge-47.4.4', '1.19.4-forge-45.2.0', '1.18.2-forge-40.2.0', '1.16.5-forge-36.2.39', '1.12.2-forge-14.23.5.2859'],
    'fabric': ['1.21.3-fabric-0.15.11', '1.20.1-fabric-0.15.7', '1.19.4-fabric-0.15.3', '1.18.2-fabric-0.14.21', '1.16.5-fabric-0.11.3', '1.12.2-fabric-0.4.2']
}

def get_versiones_soportadas():
    """
    Obtiene las versiones soportadas dinámicamente desde la API oficial
    Prioriza las versiones release (estables) para el usuario
    Si falla la API, usa las versiones de fallback
    
    Returns:
        Dict con las versiones organizadas por tipo
    """
    try:
        # Intentar importar el version manager
        from version_manager import version_manager
        
        # Obtener TODAS las versiones release (estables)
        versiones_release = version_manager.get_versions_by_type('release')
        
        print(f"✅ Obtenidas {len(versiones_release)} versiones release desde la API oficial")
        
        # Organizar en el formato esperado por el launcher
        # Priorizar versiones release para el usuario
        versiones_organizadas = {
            'vanilla': versiones_release,  # TODAS las versiones release
            'release': versiones_release,  # Alias para versiones release
            'snapshot': version_manager.get_versions_by_type('snapshot')[:10],  # Solo las 10 más recientes
            'old_beta': version_manager.get_versions_by_type('old_beta')[:5],   # Solo las 5 más recientes
            'old_alpha': version_manager.get_versions_by_type('old_alpha')[:5]  # Solo las 5 más recientes
        }
        
        # Agregar versiones de Forge y Fabric (estas no están en la API oficial)
        versiones_organizadas['forge'] = VERSIONES_FALLBACK['forge']
        versiones_organizadas['fabric'] = VERSIONES_FALLBACK['fabric']
        
        return versiones_organizadas
        
    except ImportError:
        print("⚠️ Version Manager no disponible, usando versiones de fallback")
        return VERSIONES_FALLBACK
    except Exception as e:
        print(f"⚠️ Error obteniendo versiones dinámicas: {e}, usando fallback")
        return VERSIONES_FALLBACK

# Función de conveniencia para obtener versiones
VERSIONES_SOPORTADAS = get_versiones_soportadas()

# Configuración de RAM recomendada
RAM_RECOMENDADA = {
    'mínima': '2',
    'recomendada': '4',
    'óptima': '8',
    'máxima': '16'
}

# Configuración de timeouts
TIMEOUTS = {
    'descarga': 30,  # segundos
    'instalacion': 300,  # segundos
    'inicio_minecraft': 60  # segundos
}

# Configuración de mensajes
MENSAJES = {
    'exito_instalacion': 'Instancia creada correctamente',
    'error_instalacion': 'No se pudo instalar la versión de Minecraft',
    'exito_eliminacion': 'Instancia eliminada correctamente',
    'error_eliminacion': 'No se pudo eliminar la instancia',
    'exito_edicion': 'Instancia actualizada correctamente',
    'error_edicion': 'No se pudo actualizar la instancia'
}

# Configuración de colores (para CustomTkinter)
COLORES = {
    'tema_oscuro': {
        'bg_color': "gray13",
        'fg_color': "gray25",
        'text_color': "white"
    },
    'tema_claro': {
        'bg_color': "gray90",
        'fg_color': "gray75",
        'text_color': "black"
    }
}

# Configuración de archivos de recursos
RECURSOS = {
    'icono_principal': 'Resources/icon2.png',
    'banner_principal': 'Resources/baner.png',
    'icono_ico': 'icon.ico'
}

# Configuración de logging
LOGGING = {
    'nivel': 'INFO',
    'formato': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'archivo': 'launcher.log'
}

# Configuración de red
RED = {
    'user_agent': 'MultiMinecraft/1.0',
    'timeout_conexion': 10,
    'timeout_lectura': 30,
    'max_reintentos': 3
}

# Configuración de seguridad
SEGURIDAD = {
    'verificar_ssl': True,
    'permitir_redirecciones': True,
    'max_redirecciones': 5
}

def crear_directorios():
    """Crea los directorios necesarios si no existen"""
    rutas = get_rutas()
    
    for ruta in [rutas['launcher_root'], rutas['instancias_root'], rutas['logs_dir']]:
        if not os.path.exists(ruta):
            os.makedirs(ruta)
            print(f"📁 Creado directorio: {ruta}")

def crear_archivos_configuracion():
    """Crea archivos de configuración si no existen"""
    rutas = get_rutas()
    
    # Crear config.json si no existe
    if not os.path.exists(rutas['config_path']):
        with open(rutas['config_path'], "w") as f:
            f.write("{}")
        print(f"📄 Creado archivo: {rutas['config_path']}")
    
    # Crear settingsMM2.json si no existe
    if not os.path.exists(rutas['settings_path']):
        with open(rutas['settings_path'], "w") as f:
            f.write("{}")
        print(f"📄 Creado archivo: {rutas['settings_path']}")

def inicializar_sistema():
    """Inicializa el sistema creando directorios y archivos necesarios"""
    print("🔧 Inicializando sistema...")
    crear_directorios()
    crear_archivos_configuracion()
    print("✅ Sistema inicializado")

if __name__ == "__main__":
    inicializar_sistema() 