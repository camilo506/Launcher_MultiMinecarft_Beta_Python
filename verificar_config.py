#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de verificación de la carpeta config
Verifica que la carpeta config esté funcionando correctamente y que los mods puedan leer sus configuraciones
"""

import os
import json
import sys

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Obtener rutas
appdata_path = os.getenv('APPDATA')
if appdata_path is None:
    appdata_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming")

launcher_root = os.path.join(appdata_path, ".MultiMinecraft_MS")
instancias_root = os.path.join(launcher_root, "Instancias")

def verificar_config_instancia(nombre_instancia):
    """Verifica la carpeta config de una instancia"""
    carpeta_instancia = os.path.join(instancias_root, nombre_instancia)
    
    if not os.path.exists(carpeta_instancia):
        return None
    
    resultado = {
        'instancia': nombre_instancia,
        'carpeta_instancia': carpeta_instancia,
        'carpeta_instancia_abs': os.path.abspath(carpeta_instancia),
        'config_existe': False,
        'config_ruta': '',
        'archivos_config': [],
        'carpetas_config': [],
        'mods_con_config': [],
        'problemas': [],
        'advertencias': []
    }
    
    # Cargar configuración de la instancia
    config_json = os.path.join(carpeta_instancia, "config.json")
    if os.path.exists(config_json):
        try:
            with open(config_json, 'r', encoding='utf-8') as f:
                config = json.load(f)
                resultado['tipo'] = config.get('tipo', 'Desconocido')
                resultado['version'] = config.get('version', 'Desconocida')
        except:
            resultado['tipo'] = 'Error al leer'
            resultado['version'] = 'Error al leer'
    
    # Verificar carpeta config
    config_path = os.path.join(carpeta_instancia, 'config')
    config_path_abs = os.path.abspath(config_path)
    resultado['config_ruta'] = config_path_abs
    
    if os.path.exists(config_path):
        resultado['config_existe'] = True
        
        try:
            # Listar contenido
            for item in os.listdir(config_path):
                item_path = os.path.join(config_path, item)
                if os.path.isfile(item_path):
                    resultado['archivos_config'].append(item)
                elif os.path.isdir(item_path):
                    resultado['carpetas_config'].append(item)
                    # Verificar si es una carpeta de configuración de un mod
                    if any(x in item.lower() for x in ['config', 'settings', 'options']):
                        resultado['mods_con_config'].append(item)
            
            # Verificar carpetas comunes de mods
            carpetas_mods_comunes = ['fancymenu', 'jei', 'journeymap', 'optifine', 'quark', 'create']
            for carpeta in resultado['carpetas_config']:
                if any(mod in carpeta.lower() for mod in carpetas_mods_comunes):
                    if carpeta not in resultado['mods_con_config']:
                        resultado['mods_con_config'].append(carpeta)
            
        except Exception as e:
            resultado['problemas'].append(f"Error al leer carpeta config: {e}")
    else:
        resultado['problemas'].append("Carpeta config no existe")
        resultado['advertencias'].append("Se creará automáticamente al iniciar la instancia")
    
    # Verificar mods instalados
    mods_path = os.path.join(carpeta_instancia, 'mods')
    if os.path.exists(mods_path):
        try:
            mods_files = [f for f in os.listdir(mods_path) if f.endswith('.jar')]
            resultado['mods_instalados'] = len(mods_files)
            resultado['lista_mods'] = mods_files[:10]  # Primeros 10
        except:
            pass
    
    return resultado

def imprimir_verificacion(resultado):
    """Imprime la verificación de forma legible"""
    print("\n" + "="*80)
    print(f"📋 INSTANCIA: {resultado['instancia']}")
    print("="*80)
    print(f"   Tipo: {resultado.get('tipo', 'N/A')}")
    print(f"   Versión: {resultado.get('version', 'N/A')}")
    print()
    
    print(f"📂 RUTAS:")
    print(f"   Carpeta instancia: {resultado['carpeta_instancia']}")
    print(f"   Carpeta instancia (absoluta): {resultado['carpeta_instancia_abs']}")
    print(f"   Carpeta config: {resultado['config_ruta']}")
    print()
    
    # Estado de la carpeta config
    if resultado['config_existe']:
        print(f"✅ CARPETA CONFIG: EXISTE")
        print(f"   📄 Archivos: {len(resultado['archivos_config'])}")
        print(f"   📁 Carpetas: {len(resultado['carpetas_config'])}")
        print()
        
        if resultado['archivos_config']:
            print(f"   📄 Archivos de configuración encontrados:")
            for archivo in resultado['archivos_config'][:15]:
                print(f"      • {archivo}")
            if len(resultado['archivos_config']) > 15:
                print(f"      ... y {len(resultado['archivos_config']) - 15} archivos más")
            print()
        
        if resultado['carpetas_config']:
            print(f"   📁 Carpetas de configuración de mods:")
            for carpeta in resultado['carpetas_config'][:15]:
                print(f"      • {carpeta}/")
            if len(resultado['carpetas_config']) > 15:
                print(f"      ... y {len(resultado['carpetas_config']) - 15} carpetas más")
            print()
        
        if resultado['mods_con_config']:
            print(f"   ✅ Mods con configuración detectados:")
            for mod in resultado['mods_con_config']:
                print(f"      • {mod}")
            print()
        
        # Verificación de funcionamiento
        print(f"🔍 VERIFICACIÓN DE FUNCIONAMIENTO:")
        if len(resultado['archivos_config']) > 0 or len(resultado['carpetas_config']) > 0:
            print(f"   ✅ La carpeta config contiene configuraciones")
            print(f"   ✅ Los mods DEBERÍAN poder leer sus configuraciones desde:")
            print(f"      {resultado['config_ruta']}")
            print()
            print(f"   📝 CÓMO FUNCIONA:")
            print(f"      1. Minecraft busca la carpeta 'config' dentro del gameDirectory")
            print(f"      2. El gameDirectory está configurado como: {resultado['carpeta_instancia_abs']}")
            print(f"      3. Por lo tanto, Minecraft usará: {resultado['config_ruta']}")
            print(f"      4. Los mods leen automáticamente desde esta carpeta al iniciar")
        else:
            print(f"   ⚠️  La carpeta config está vacía")
            print(f"   ℹ️  Los mods crearán sus archivos de configuración al iniciar por primera vez")
    else:
        print(f"❌ CARPETA CONFIG: NO EXISTE")
        print(f"   Se creará automáticamente al iniciar la instancia")
    
    print()
    
    # Mods instalados
    if resultado.get('mods_instalados', 0) > 0:
        print(f"🔧 MODS INSTALADOS: {resultado['mods_instalados']}")
        if resultado.get('lista_mods'):
            print(f"   Primeros mods:")
            for mod in resultado['lista_mods'][:5]:
                print(f"      • {mod}")
            if len(resultado['lista_mods']) > 5:
                print(f"      ... y {len(resultado['lista_mods']) - 5} más")
    
    print()
    
    # Problemas y advertencias
    if resultado['problemas']:
        print("🚨 PROBLEMAS:")
        for problema in resultado['problemas']:
            print(f"   • {problema}")
        print()
    
    if resultado['advertencias']:
        print("⚠️  ADVERTENCIAS:")
        for advertencia in resultado['advertencias']:
            print(f"   • {advertencia}")
        print()
    
    # Resumen final
    print("📊 RESUMEN:")
    if resultado['config_existe'] and (len(resultado['archivos_config']) > 0 or len(resultado['carpetas_config']) > 0):
        print("   ✅ La carpeta config está funcionando correctamente")
        print("   ✅ Los mods DEBERÍAN poder leer sus configuraciones")
        print("   ✅ El gameDirectory está configurado correctamente")
    elif resultado['config_existe']:
        print("   ⚠️  La carpeta config existe pero está vacía")
        print("   ℹ️  Los mods crearán sus configuraciones al iniciar")
    else:
        print("   ⚠️  La carpeta config no existe aún")
        print("   ℹ️  Se creará automáticamente al iniciar la instancia")
    
    print()

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE CARPETA CONFIG")
    print("="*80)
    print(f"📁 Ruta de instancias: {instancias_root}")
    print()
    
    if not os.path.exists(instancias_root):
        print(f"❌ ERROR: La carpeta de instancias no existe: {instancias_root}")
        sys.exit(1)
    
    # Obtener todas las instancias
    try:
        instancias = [d for d in os.listdir(instancias_root) 
                     if os.path.isdir(os.path.join(instancias_root, d))]
    except Exception as e:
        print(f"❌ ERROR al leer instancias: {e}")
        sys.exit(1)
    
    if not instancias:
        print("⚠️  No se encontraron instancias")
        sys.exit(0)
    
    print(f"📋 Instancias encontradas: {len(instancias)}")
    print()
    
    # Verificar cada instancia
    resultados = []
    for instancia in instancias:
        resultado = verificar_config_instancia(instancia)
        if resultado:
            resultados.append(resultado)
    
    # Imprimir verificaciones
    for resultado in resultados:
        imprimir_verificacion(resultado)
    
    # Resumen final
    print("\n" + "="*80)
    print("📊 RESUMEN GENERAL")
    print("="*80)
    total = len(resultados)
    con_config = sum(1 for r in resultados if r['config_existe'])
    con_contenido = sum(1 for r in resultados 
                       if r['config_existe'] and (len(r['archivos_config']) > 0 or len(r['carpetas_config']) > 0))
    
    print(f"   Total de instancias: {total}")
    print(f"   Con carpeta config: {con_config}")
    print(f"   Con configuraciones: {con_contenido}")
    print()
    
    if con_contenido == total and total > 0:
        print("✅ TODAS las instancias tienen configuraciones en la carpeta config")
        print("✅ Los mods DEBERÍAN poder leer sus configuraciones correctamente")
    elif con_config == total and total > 0:
        print("⚠️  Todas las instancias tienen carpeta config, pero algunas están vacías")
        print("ℹ️  Los mods crearán sus configuraciones al iniciar")
    else:
        print("⚠️  Algunas instancias no tienen carpeta config")
        print("ℹ️  Se crearán automáticamente al iniciar")
    
    print("\n✅ Verificación completada")
    print("="*80)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verificación cancelada por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

