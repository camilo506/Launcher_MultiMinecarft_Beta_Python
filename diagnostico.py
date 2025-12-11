#!/usr/bin/env python3
"""
Script de diagnóstico para el launcher de Minecraft
"""

import sys
import os
import importlib

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas correctamente"""
    print("🔍 Verificando dependencias...")
    
    dependencias = [
        ('customtkinter', 'customtkinter'),
        ('minecraft_launcher_lib', 'minecraft-launcher-lib'),
        ('requests', 'requests'),
        ('PIL', 'Pillow'),
        ('pygetwindow', 'pygetwindow')
    ]
    
    todas_ok = True
    
    for modulo, paquete in dependencias:
        try:
            importlib.import_module(modulo)
            print(f"✅ {paquete} - OK")
        except ImportError as e:
            print(f"❌ {paquete} - ERROR: {e}")
            todas_ok = False
    
    return todas_ok

def verificar_archivos():
    """Verifica que los archivos necesarios existan"""
    print("\n📁 Verificando archivos...")
    
    archivos_necesarios = [
        'MultiMinecraft.py',
        'requirements.txt',
        'Resources/icon2.png',
        'Resources/baner.png'
    ]
    
    todas_ok = True
    
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo} - OK")
        else:
            print(f"❌ {archivo} - NO ENCONTRADO")
            todas_ok = False
    
    return todas_ok

def verificar_instalaciones():
    """Verifica las instalaciones existentes"""
    print("\n🎮 Verificando instalaciones...")
    
    user_window = os.environ.get("USERNAME", "Usuario")
    launcher_root = f"C:/Users/{user_window}/AppData/Roaming/.MultiMinecraft"
    instancias_root = os.path.join(launcher_root, "Instancias")
    
    if os.path.exists(launcher_root):
        print(f"✅ Directorio del launcher: {launcher_root}")
        
        if os.path.exists(instancias_root):
            print(f"✅ Directorio de instancias: {instancias_root}")
            
            # Contar instancias
            instancias = [d for d in os.listdir(instancias_root) 
                        if os.path.isdir(os.path.join(instancias_root, d))]
            print(f"📊 Instancias encontradas: {len(instancias)}")
            
            for instancia in instancias:
                config_path = os.path.join(instancias_root, instancia, "config.json")
                if os.path.exists(config_path):
                    print(f"  ✅ {instancia} - Configuración OK")
                else:
                    print(f"  ⚠️  {instancia} - Sin configuración")
        else:
            print(f"⚠️  Directorio de instancias no existe: {instancias_root}")
    else:
        print(f"⚠️  Directorio del launcher no existe: {launcher_root}")
    
    return True

def verificar_minecraft_launcher_lib():
    """Verifica la funcionalidad de minecraft_launcher_lib"""
    print("\n🔧 Verificando minecraft_launcher_lib...")
    
    try:
        import minecraft_launcher_lib
        
        # Verificar funciones básicas
        funciones_basicas = [
            'install_minecraft_version',
            'command.get_minecraft_command',
            'forge.find_forge_version',
            'fabric.install_fabric'
        ]
        
        for funcion in funciones_basicas:
            try:
                # Intentar acceder a la función
                if '.' in funcion:
                    modulo, func = funcion.split('.')
                    getattr(getattr(minecraft_launcher_lib, modulo), func)
                else:
                    getattr(minecraft_launcher_lib.install, funcion)
                print(f"✅ {funcion} - Disponible")
            except AttributeError:
                print(f"❌ {funcion} - No disponible")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando minecraft_launcher_lib: {e}")
        return False

def verificar_entorno_virtual():
    """Verifica si estamos en un entorno virtual"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def main():
    """Función principal del diagnóstico"""
    print("🚀 Diagnóstico del Launcher de Minecraft (Entorno Virtual)")
    print("=" * 60)
    
    # Verificar entorno virtual
    if verificar_entorno_virtual():
        print("✅ Entorno virtual activo")
    else:
        print("⚠️  No se detectó entorno virtual activo")
        print("💡 Se recomienda usar el entorno virtual .venv")
    
    # Verificar Python
    print(f"🐍 Python versión: {sys.version}")
    
    # Verificar dependencias
    deps_ok = verificar_dependencias()
    
    # Verificar archivos
    archivos_ok = verificar_archivos()
    
    # Verificar instalaciones
    verificar_instalaciones()
    
    # Verificar minecraft_launcher_lib
    mcl_ok = verificar_minecraft_launcher_lib()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 50)
    
    if deps_ok and archivos_ok and mcl_ok:
        print("✅ TODO OK - El launcher debería funcionar correctamente")
        print("\n🎮 Puedes ejecutar el launcher con: python MultiMinecraft.py")
    else:
        print("❌ HAY PROBLEMAS - Revisa los errores arriba")
        
        if not deps_ok:
            print("\n💡 Para solucionar problemas de dependencias:")
            print("   Ejecuta: python actualizar_dependencias.py")
        
        if not archivos_ok:
            print("\n💡 Para solucionar problemas de archivos:")
            print("   Asegúrate de que todos los archivos estén en su lugar")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...") 