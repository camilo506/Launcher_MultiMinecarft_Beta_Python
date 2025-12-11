#!/usr/bin/env python3
"""
Script para actualizar las dependencias del launcher de Minecraft
Optimizado para entorno virtual .venv
"""

import subprocess
import sys
import os

def verificar_entorno_virtual():
    """Verifica si estamos en un entorno virtual"""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def activar_entorno_virtual():
    """Activa el entorno virtual si existe"""
    venv_path = os.path.join(os.getcwd(), '.venv')
    if os.path.exists(venv_path):
        # En Windows, el script de activación está en Scripts
        if os.name == 'nt':  # Windows
            activate_script = os.path.join(venv_path, 'Scripts', 'activate')
        else:  # Unix/Linux
            activate_script = os.path.join(venv_path, 'bin', 'activate')
        
        if os.path.exists(activate_script):
            print(f"✅ Entorno virtual detectado: {venv_path}")
            return True
    return False

def actualizar_dependencias():
    """Actualiza las dependencias de Python en el entorno virtual"""
    print("🔄 Actualizando dependencias en entorno virtual...")
    
    # Verificar si estamos en entorno virtual
    if not verificar_entorno_virtual():
        print("⚠️  No se detectó entorno virtual activo")
        print("💡 Asegúrate de activar el entorno virtual:")
        print("   .venv\\Scripts\\activate  # En Windows")
        print("   source .venv/bin/activate  # En Unix/Linux")
        return False
    
    try:
        # Actualizar pip en el entorno virtual
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("✅ pip actualizado en entorno virtual")
        
        # Instalar/actualizar dependencias desde requirements.txt
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--upgrade"])
        print("✅ Dependencias actualizadas en entorno virtual")
        
        # Verificar versión de minecraft-launcher-lib
        try:
            import minecraft_launcher_lib
            print(f"✅ minecraft-launcher-lib instalado en entorno virtual")
            # Intentar obtener la versión
            try:
                version = minecraft_launcher_lib.__version__
                print(f"   Versión: {version}")
            except AttributeError:
                print("   Versión: No disponible")
        except ImportError:
            print("❌ No se pudo importar minecraft_launcher_lib")
            return False
        
        print("\n🎉 Actualización completada exitosamente en entorno virtual!")
        print("Ahora puedes ejecutar el launcher sin problemas.")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error actualizando dependencias: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    return True

def crear_entorno_virtual():
    """Crea el entorno virtual si no existe"""
    venv_path = os.path.join(os.getcwd(), '.venv')
    
    if not os.path.exists(venv_path):
        print("📁 Creando entorno virtual...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
            print("✅ Entorno virtual creado: .venv")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creando entorno virtual: {e}")
            return False
    else:
        print("✅ Entorno virtual ya existe: .venv")
        return True

def main():
    """Función principal"""
    print("🚀 Actualizador de Dependencias - MultiMinecraft (Entorno Virtual)")
    print("=" * 60)
    
    # Verificar si existe el entorno virtual
    if not os.path.exists('.venv'):
        print("📁 No se encontró entorno virtual .venv")
        respuesta = input("¿Deseas crear el entorno virtual? (s/n): ").lower()
        if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
            if crear_entorno_virtual():
                print("\n💡 Ahora activa el entorno virtual:")
                print("   .venv\\Scripts\\activate  # En Windows")
                print("   source .venv/bin/activate  # En Unix/Linux")
                print("   Luego ejecuta: python actualizar_dependencias.py")
            else:
                print("❌ No se pudo crear el entorno virtual")
            return
        else:
            print("❌ Se requiere entorno virtual para continuar")
            return
    
    # Verificar si estamos en el entorno virtual
    if not verificar_entorno_virtual():
        print("⚠️  No estás en el entorno virtual")
        print("💡 Activa el entorno virtual primero:")
        print("   .venv\\Scripts\\activate  # En Windows")
        print("   source .venv/bin/activate  # En Unix/Linux")
        return
    
    # Actualizar dependencias
    if actualizar_dependencias():
        print("\n✅ Todo listo! El launcher está actualizado en el entorno virtual")
    else:
        print("\n❌ La actualización falló. Revisa los errores arriba.")

if __name__ == "__main__":
    main()
    input("\nPresiona Enter para salir...") 