"""
Cache management system for procedural terrain generation.
Handles intelligent caching of terrain data to improve performance.
"""

import os
import pickle
import hashlib
import time
import json
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
# Conditional import for Blender API
try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    from mock_bpy import mock_bpy as bpy


class CacheManager:
    """
    High-level cache management for terrain generation.
    Coordinates different cache types and manages cache lifecycle.
    """
    
    def __init__(self, config):
        """
        Initialize cache manager.
        
        Args:
            config: Terrain configuration object
        """
        self.config = config
        self.cache_enabled = config.USE_CACHE
        self.cache_root = bpy.path.abspath(config.CACHE_PATH)
        
        # Initialize cache directories
        self.terrain_cache = TerrainCache(os.path.join(self.cache_root, "terrain"))
        self.mesh_cache = MeshCache(os.path.join(self.cache_root, "meshes"))
        self.texture_cache = TextureCache(os.path.join(self.cache_root, "textures"))
        
        # Cache statistics
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_size_mb': 0.0
        }
    
    def clear_all_caches(self):
        """Clear all cached data."""
        try:
            if hasattr(self, 'terrain_cache'):
                self.terrain_cache.clear()
            if hasattr(self, 'mesh_cache'):
                self.mesh_cache.clear()
            if hasattr(self, 'texture_cache'):
                self.texture_cache.clear()
            
            # Reset statistics
            self.cache_stats = {
                'hits': 0,
                'misses': 0,
                'evictions': 0,
                'total_size_mb': 0.0
            }
        except Exception as e:
            print(f"Erreur lors du vidage du cache: {e}")
        
        # TODO: Add cache warming strategies
        # TODO: Implement cache compression
    
    def get_cache_key(self, tile_x: int, tile_y: int, seed: int, 
                     detail_level: str, **kwargs) -> str:
        """
        Generate cache key for terrain data.
        
        Args:
            tile_x, tile_y: Tile coordinates
            seed: Generation seed
            detail_level: LOD level
            **kwargs: Additional parameters affecting generation
            
        Returns:
            Unique cache key string
            
        TODO: Add parameter hashing for complex configurations
        TODO: Implement cache key versioning
        """
        key_data = {
            'tile_x': tile_x,
            'tile_y': tile_y,
            'seed': seed,
            'detail_level': detail_level,
            'world_size': self.config.WORLD_SIZE,
            'tile_size': self.config.TILE_SIZE,
            **kwargs
        }
        
        # Create hash from parameters
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def is_cached(self, cache_type: str, cache_key: str) -> bool:
        """
        Check if data is cached.
        
        Args:
            cache_type: Type of cache ("terrain", "mesh", "texture")
            cache_key: Cache key to check
            
        Returns:
            True if data is cached
            
        TODO: Add cache validation (check if cache is still valid)
        """
        if not self.cache_enabled:
            return False
        
        cache_instance = self._get_cache_instance(cache_type)
        return cache_instance.is_cached(cache_key) if cache_instance else False
    
    def get_cached_data(self, cache_type: str, cache_key: str) -> Optional[Any]:
        """
        Retrieve cached data.
        
        Args:
            cache_type: Type of cache
            cache_key: Cache key
            
        Returns:
            Cached data or None if not found
            
        TODO: Add cache hit/miss statistics tracking
        """
        if not self.cache_enabled:
            return None
        
        cache_instance = self._get_cache_instance(cache_type)
        if cache_instance and cache_instance.is_cached(cache_key):
            self.cache_stats['hits'] += 1
            return cache_instance.load_data(cache_key)
        
        self.cache_stats['misses'] += 1
        return None
    
    def cache_data(self, cache_type: str, cache_key: str, data: Any) -> bool:
        """
        Store data in cache.
        
        Args:
            cache_type: Type of cache
            cache_key: Cache key
            data: Data to cache
            
        Returns:
            True if caching was successful
            
        TODO: Add cache size management
        TODO: Implement cache eviction policies
        """
        if not self.cache_enabled:
            return False
        
        cache_instance = self._get_cache_instance(cache_type)
        if cache_instance:
            return cache_instance.save_data(cache_key, data)
        
        return False
    
    def _get_cache_instance(self, cache_type: str):
        """Get cache instance by type."""
        cache_map = {
            'terrain': self.terrain_cache,
            'mesh': self.mesh_cache,
            'texture': self.texture_cache
        }
        return cache_map.get(cache_type)
    
    def clear_cache(self, cache_type: Optional[str] = None) -> None:
        """
        Clear cache data.
        
        Args:
            cache_type: Specific cache type to clear, or None for all
            
        TODO: Add selective cache clearing
        """
        if cache_type:
            cache_instance = self._get_cache_instance(cache_type)
            if cache_instance:
                cache_instance.clear()
        else:
            self.terrain_cache.clear()
            self.mesh_cache.clear()
            self.texture_cache.clear()
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive cache statistics.
        
        Returns:
            Dictionary containing cache statistics
            
        TODO: Add detailed per-cache statistics
        """
        total_size = (self.terrain_cache.get_cache_size() +
                     self.mesh_cache.get_cache_size() +
                     self.texture_cache.get_cache_size())
        
        hit_rate = (self.cache_stats['hits'] / 
                   max(1, self.cache_stats['hits'] + self.cache_stats['misses']))
        
        return {
            'enabled': self.cache_enabled,
            'total_size_mb': total_size / (1024 * 1024),
            'hit_rate': hit_rate,
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'evictions': self.cache_stats['evictions'],
            'terrain_cache_size': self.terrain_cache.get_cache_size(),
            'mesh_cache_size': self.mesh_cache.get_cache_size(),
            'texture_cache_size': self.texture_cache.get_cache_size()
        }


class TerrainCache:
    """
    Intelligent cache system for terrain elevation data.
    Handles caching of generated terrain tiles with compression.
    """
    
    def __init__(self, cache_dir: str):
        """
        Initialize terrain cache.
        
        Args:
            cache_dir: Directory for cache storage
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # Cache metadata
        self.metadata_file = os.path.join(cache_dir, "cache_metadata.json")
        self.metadata = self._load_metadata()
        
        # TODO: Add cache size limits
        # TODO: Implement LRU eviction policy
    
    def _load_metadata(self) -> Dict[str, Any]:
        """Load cache metadata."""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {'entries': {}, 'total_size': 0}
    
    def _save_metadata(self) -> None:
        """Save cache metadata."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def is_cached(self, cache_key: str) -> bool:
        """
        Check if terrain data is cached.
        
        Args:
            cache_key: Cache key to check
            
        Returns:
            True if cached
            
        TODO: Port is_cached method from original script
        """
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.npy")
        return os.path.exists(cache_file)
    
    def save_data(self, cache_key: str, tile_data: Dict[str, Any]) -> bool:
        """
        Save terrain tile data to cache.
        
        Args:
            cache_key: Cache key
            tile_data: Terrain data to cache
            
        Returns:
            True if successful
            
        TODO: Port save_tile method from original script
        TODO: Add data compression
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.npy")
            
            # Save elevation data
            np.save(cache_file, tile_data['elevation'])
            
            # Save metadata
            metadata_file = os.path.join(self.cache_dir, f"{cache_key}_meta.json")
            meta_data = {
                'tile_info': tile_data.get('tile_info', {}),
                'timestamp': time.time(),
                'coordinates_shape': tile_data['coordinates'][0].shape if 'coordinates' in tile_data else None
            }
            
            with open(metadata_file, 'w') as f:
                json.dump(meta_data, f)
            
            # Update cache metadata
            file_size = os.path.getsize(cache_file)
            self.metadata['entries'][cache_key] = {
                'size': file_size,
                'timestamp': time.time()
            }
            self.metadata['total_size'] += file_size
            self._save_metadata()
            
            return True
            
        except Exception as e:
            print(f"Cache save error: {e}")
            return False
    
    def load_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """
        Load terrain tile data from cache.
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached terrain data or None
            
        TODO: Port load_tile method from original script
        TODO: Add data decompression
        """
        try:
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.npy")
            metadata_file = os.path.join(self.cache_dir, f"{cache_key}_meta.json")
            
            if not (os.path.exists(cache_file) and os.path.exists(metadata_file)):
                return None
            
            # Load elevation data
            elevation = np.load(cache_file)
            
            # Load metadata
            with open(metadata_file, 'r') as f:
                meta_data = json.load(f)
            
            # Reconstruct coordinate arrays from tile info
            tile_info = meta_data.get('tile_info', {})
            tile_x = tile_info.get('x', 0)
            tile_y = tile_info.get('y', 0)
            subdivisions = tile_info.get('subdivisions', 64)
            
            # Reconstruct coordinates using the same logic as in geology.py
            tile_size = 250  # Default tile size from config
            world_size = 4000  # Default world size from config
            
            start_x = (tile_x * tile_size) - (world_size / 2)
            start_y = (tile_y * tile_size) - (world_size / 2)
            
            x_coords = np.linspace(start_x, start_x + tile_size, subdivisions)
            y_coords = np.linspace(start_y, start_y + tile_size, subdivisions)
            X, Y = np.meshgrid(x_coords, y_coords)
            
            return {
                'elevation': elevation,
                'tile_info': tile_info,
                'coordinates': (X, Y)
            }
            
        except Exception as e:
            print(f"Cache load error: {e}")
            return None
    
    def clear(self) -> None:
        """Clear all cached terrain data."""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
        self.metadata = {'entries': {}, 'total_size': 0}
        self._save_metadata()
    
    def get_cache_size(self) -> int:
        """Get total cache size in bytes."""
        return self.metadata.get('total_size', 0)


class MeshCache:
    """
    Cache system for generated Blender meshes.
    """
    
    def __init__(self, cache_dir: str):
        """
        Initialize mesh cache.
        
        Args:
            cache_dir: Directory for cache storage
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # TODO: Add mesh serialization/deserialization
        # TODO: Implement mesh compression
    
    def is_cached(self, cache_key: str) -> bool:
        """Check if mesh is cached."""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.blend")
        return os.path.exists(cache_file)
    
    def save_data(self, cache_key: str, mesh_data: Any) -> bool:
        """
        Save mesh data to cache.
        
        Args:
            cache_key: Cache key
            mesh_data: Mesh data to cache
            
        Returns:
            True if successful
            
        TODO: Implement mesh serialization
        """
        # TODO: Serialize Blender mesh data
        return False
    
    def load_data(self, cache_key: str) -> Optional[Any]:
        """
        Load mesh data from cache.
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached mesh data or None
            
        TODO: Implement mesh deserialization
        """
        # TODO: Deserialize Blender mesh data
        return None
    
    def clear(self) -> None:
        """Clear all cached mesh data."""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_cache_size(self) -> int:
        """Get total cache size in bytes."""
        total_size = 0
        if os.path.exists(self.cache_dir):
            for root, dirs, files in os.walk(self.cache_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
        return total_size


class TextureCache:
    """
    Cache system for generated textures and materials.
    """
    
    def __init__(self, cache_dir: str):
        """
        Initialize texture cache.
        
        Args:
            cache_dir: Directory for cache storage
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
        # TODO: Add texture format support
        # TODO: Implement texture compression
    
    def is_cached(self, cache_key: str) -> bool:
        """Check if texture is cached."""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.png")
        return os.path.exists(cache_file)
    
    def save_data(self, cache_key: str, texture_data: Any) -> bool:
        """
        Save texture data to cache.
        
        Args:
            cache_key: Cache key
            texture_data: Texture data to cache
            
        Returns:
            True if successful
            
        TODO: Implement texture serialization
        """
        # TODO: Save texture/image data
        return False
    
    def load_data(self, cache_key: str) -> Optional[Any]:
        """
        Load texture data from cache.
        
        Args:
            cache_key: Cache key
            
        Returns:
            Cached texture data or None
            
        TODO: Implement texture deserialization
        """
        # TODO: Load texture/image data
        return None
    
    def clear(self) -> None:
        """Clear all cached texture data."""
        import shutil
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_cache_size(self) -> int:
        """Get total cache size in bytes."""
        total_size = 0
        if os.path.exists(self.cache_dir):
            for root, dirs, files in os.walk(self.cache_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
        return total_size
