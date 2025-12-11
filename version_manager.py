#!/usr/bin/env python3
"""
Version Manager - Sistema dinámico para obtener versiones de Minecraft
Obtiene automáticamente todas las versiones disponibles desde la API oficial de Mojang
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

class VersionManager:
    """Gestor de versiones de Minecraft con cache y actualización automática"""
    
    def __init__(self, cache_dir: str = None):
        """
        Inicializa el gestor de versiones
        
        Args:
            cache_dir: Directorio para almacenar el cache de versiones
        """
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), "cache")
        self.cache_file = os.path.join(self.cache_dir, "versions_cache.json")
        self.manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
        self.cache_duration = 24 * 3600  # 24 horas en segundos
        
        # Crear directorio de cache si no existe
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Cache en memoria
        self._versions_cache = None
        self._last_update = 0
    
    def _load_cache(self) -> Optional[Dict]:
        """Carga el cache de versiones desde el archivo"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    return cache_data
        except Exception as e:
            print(f"⚠️ Error cargando cache de versiones: {e}")
        return None
    
    def _save_cache(self, versions_data: Dict) -> bool:
        """Guarda el cache de versiones en el archivo"""
        try:
            cache_data = {
                'timestamp': time.time(),
                'data': versions_data,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"⚠️ Error guardando cache de versiones: {e}")
            return False
    
    def _is_cache_valid(self) -> bool:
        """Verifica si el cache es válido y no ha expirado"""
        try:
            if not os.path.exists(self.cache_file):
                return False
            
            cache_data = self._load_cache()
            if not cache_data:
                return False
            
            cache_time = cache_data.get('timestamp', 0)
            current_time = time.time()
            
            return (current_time - cache_time) < self.cache_duration
        except Exception:
            return False
    
    def _fetch_versions_from_api(self) -> Optional[Dict]:
        """Obtiene las versiones desde la API oficial de Mojang"""
        try:
            print("🌐 Obteniendo versiones desde la API oficial de Mojang...")
            response = requests.get(self.manifest_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            print(f"✅ Obtenidas {len(data.get('versions', []))} versiones desde la API")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión a la API de Mojang: {e}")
            return None
        except Exception as e:
            print(f"❌ Error procesando respuesta de la API: {e}")
            return None
    
    def get_all_versions(self, force_update: bool = False) -> Dict:
        """
        Obtiene todas las versiones de Minecraft
        
        Args:
            force_update: Si True, fuerza la actualización del cache
            
        Returns:
            Diccionario con todas las versiones organizadas por tipo
        """
        # Verificar cache si no se fuerza la actualización
        if not force_update and self._is_cache_valid():
            cache_data = self._load_cache()
            if cache_data:
                print("📋 Usando versiones desde cache")
                return cache_data.get('data', {})
        
        # Obtener versiones desde la API
        api_data = self._fetch_versions_from_api()
        if not api_data:
            # Si falla la API, intentar usar cache aunque esté expirado
            print("⚠️ API no disponible, intentando usar cache expirado...")
            cache_data = self._load_cache()
            if cache_data:
                return cache_data.get('data', {})
            return {}
        
        # Procesar y organizar las versiones
        versions_data = self._process_versions(api_data)
        
        # Guardar en cache
        self._save_cache(versions_data)
        
        return versions_data
    
    def _process_versions(self, api_data: Dict) -> Dict:
        """Procesa y organiza las versiones obtenidas de la API"""
        try:
            versions = api_data.get('versions', [])
            
            # Organizar por tipo
            organized_versions = {
                'release': [],
                'snapshot': [],
                'old_beta': [],
                'old_alpha': [],
                'all': []
            }
            
            for version in versions:
                version_id = version.get('id', '')
                version_type = version.get('type', 'unknown')
                release_time = version.get('releaseTime', '')
                url = version.get('url', '')
                
                version_info = {
                    'id': version_id,
                    'type': version_type,
                    'releaseTime': release_time,
                    'url': url
                }
                
                # Agregar a la lista correspondiente
                if version_type in organized_versions:
                    organized_versions[version_type].append(version_info)
                
                # Agregar a la lista general
                organized_versions['all'].append(version_info)
            
            # Ordenar por fecha de lanzamiento (más recientes primero)
            for version_type in organized_versions:
                if version_type != 'all':
                    organized_versions[version_type].sort(
                        key=lambda x: x.get('releaseTime', ''), 
                        reverse=True
                    )
            
            # Agregar metadatos
            organized_versions['metadata'] = {
                'total_versions': len(versions),
                'last_updated': datetime.now().isoformat(),
                'api_url': self.manifest_url,
                'latest_release': organized_versions['release'][0]['id'] if organized_versions['release'] else None,
                'latest_snapshot': organized_versions['snapshot'][0]['id'] if organized_versions['snapshot'] else None
            }
            
            print(f"📊 Versiones organizadas:")
            print(f"   🎯 Release: {len(organized_versions['release'])}")
            print(f"   🔧 Snapshot: {len(organized_versions['snapshot'])}")
            print(f"   📦 Old Beta: {len(organized_versions['old_beta'])}")
            print(f"   🏗️ Old Alpha: {len(organized_versions['old_alpha'])}")
            print(f"   📋 Total: {len(organized_versions['all'])}")
            
            return organized_versions
            
        except Exception as e:
            print(f"❌ Error procesando versiones: {e}")
            return {}
    
    def get_versions_by_type(self, version_type: str = 'release') -> List[str]:
        """
        Obtiene versiones de un tipo específico
        
        Args:
            version_type: Tipo de versión ('release', 'snapshot', 'old_beta', 'old_alpha')
            
        Returns:
            Lista de IDs de versiones
        """
        versions_data = self.get_all_versions()
        versions = versions_data.get(version_type, [])
        return [v['id'] for v in versions]
    
    def get_latest_version(self, version_type: str = 'release') -> Optional[str]:
        """
        Obtiene la versión más reciente de un tipo específico
        
        Args:
            version_type: Tipo de versión
            
        Returns:
            ID de la versión más reciente o None
        """
        versions_data = self.get_all_versions()
        versions = versions_data.get(version_type, [])
        return versions[0]['id'] if versions else None
    
    def search_versions(self, query: str) -> List[Dict]:
        """
        Busca versiones que coincidan con una consulta
        
        Args:
            query: Consulta de búsqueda
            
        Returns:
            Lista de versiones que coinciden
        """
        versions_data = self.get_all_versions()
        all_versions = versions_data.get('all', [])
        
        matches = []
        query_lower = query.lower()
        
        for version in all_versions:
            version_id = version.get('id', '').lower()
            if query_lower in version_id:
                matches.append(version)
        
        return matches
    
    def get_version_info(self, version_id: str) -> Optional[Dict]:
        """
        Obtiene información detallada de una versión específica
        
        Args:
            version_id: ID de la versión
            
        Returns:
            Información de la versión o None
        """
        versions_data = self.get_all_versions()
        all_versions = versions_data.get('all', [])
        
        for version in all_versions:
            if version.get('id') == version_id:
                return version
        
        return None
    
    def get_supported_versions_for_launcher(self) -> Dict[str, List[str]]:
        """
        Obtiene versiones organizadas para el launcher
        
        Returns:
            Diccionario con versiones organizadas por tipo para el launcher
        """
        versions_data = self.get_all_versions()
        
        # Obtener versiones release (las más estables)
        release_versions = self.get_versions_by_type('release')
        
        # Obtener versiones snapshot (para usuarios avanzados)
        snapshot_versions = self.get_versions_by_type('snapshot')
        
        # Obtener versiones old_beta y old_alpha (para nostalgia)
        old_beta_versions = self.get_versions_by_type('old_beta')
        old_alpha_versions = self.get_versions_by_type('old_alpha')
        
        return {
            'vanilla': release_versions,
            'snapshot': snapshot_versions,
            'old_beta': old_beta_versions,
            'old_alpha': old_alpha_versions,
            'all_release': release_versions,
            'all_snapshot': snapshot_versions,
            'all_old': old_beta_versions + old_alpha_versions
        }
    
    def update_cache(self) -> bool:
        """
        Fuerza la actualización del cache
        
        Returns:
            True si la actualización fue exitosa
        """
        print("🔄 Actualizando cache de versiones...")
        versions_data = self.get_all_versions(force_update=True)
        return bool(versions_data)
    
    def get_cache_info(self) -> Dict:
        """
        Obtiene información sobre el cache
        
        Returns:
            Información del cache
        """
        cache_data = self._load_cache()
        if not cache_data:
            return {
                'exists': False,
                'valid': False,
                'last_updated': None,
                'expires_in': None
            }
        
        cache_time = cache_data.get('timestamp', 0)
        current_time = time.time()
        time_remaining = self.cache_duration - (current_time - cache_time)
        
        return {
            'exists': True,
            'valid': self._is_cache_valid(),
            'last_updated': cache_data.get('last_updated'),
            'expires_in': max(0, time_remaining),
            'total_versions': len(cache_data.get('data', {}).get('all', []))
        }

# Instancia global del gestor de versiones
version_manager = VersionManager()

def get_minecraft_versions(force_update: bool = False) -> Dict:
    """
    Función de conveniencia para obtener versiones de Minecraft
    
    Args:
        force_update: Si True, fuerza la actualización del cache
        
    Returns:
        Diccionario con todas las versiones
    """
    return version_manager.get_all_versions(force_update)

def get_supported_versions() -> Dict[str, List[str]]:
    """
    Función de conveniencia para obtener versiones soportadas por el launcher
    
    Returns:
        Diccionario con versiones organizadas para el launcher
    """
    return version_manager.get_supported_versions_for_launcher()

def update_versions_cache() -> bool:
    """
    Función de conveniencia para actualizar el cache de versiones
    
    Returns:
        True si la actualización fue exitosa
    """
    return version_manager.update_cache()

if __name__ == "__main__":
    # Prueba del sistema
    print("🧪 Probando Version Manager...")
    
    # Obtener versiones
    versions = get_minecraft_versions()
    
    if versions:
        print("\n📊 Información del cache:")
        cache_info = version_manager.get_cache_info()
        for key, value in cache_info.items():
            print(f"   {key}: {value}")
        
        print(f"\n🎯 Últimas 5 versiones release:")
        release_versions = version_manager.get_versions_by_type('release')
        for version in release_versions[:5]:
            print(f"   • {version}")
        
        print(f"\n🔧 Últimas 3 versiones snapshot:")
        snapshot_versions = version_manager.get_versions_by_type('snapshot')
        for version in snapshot_versions[:3]:
            print(f"   • {version}")
        
        print(f"\n🔍 Buscando versiones que contengan '1.12':")
        search_results = version_manager.search_versions('1.12')
        for version in search_results[:5]:
            print(f"   • {version['id']} ({version['type']})")
    else:
        print("❌ No se pudieron obtener las versiones")
