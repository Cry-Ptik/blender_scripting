"""
Configuration settings for the procedural terrain generator.
Centralized configuration management for all modules.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class TerrainConfig:
    """
    Main configuration class for terrain generation.
    Contains all parameters for world generation, optimization, and export.
    """
    
    # === WORLD PARAMETERS ===
    WORLD_SIZE: int = 8000  # World size in meters (8km x 8km)
    TILE_SIZE: int = 500    # Tile size in meters (500m x 500m)
    MASTER_SEED: int = 42   # Master seed for reproducible generation
    
    # === RESOLUTION SETTINGS ===
    HIGH_DETAIL_SUBDIVISIONS: int = 150   # Close to player
    MEDIUM_DETAIL_SUBDIVISIONS: int = 75   # Medium distance
    LOW_DETAIL_SUBDIVISIONS: int = 25      # Far distance
    
    # === PERFORMANCE OPTIMIZATION ===
    MAX_VERTICES_PER_CHUNK: int = 50000
    USE_NUMPY_VECTORIZATION: bool = True
    PARALLEL_PROCESSING: bool = True
    MAX_WORKERS: int = 8
    
    # === EXPORT SETTINGS ===
    GODOT_EXPORT_PATH: str = "//terrain_export/"
    EXPORT_HEIGHTMAPS: bool = True
    EXPORT_SPLAT_MAPS: bool = True
    EXPORT_NORMAL_MAPS: bool = True
    EXPORT_FORMAT: str = "gltf"  # "gltf" or "obj"
    
    # === CACHE SYSTEM ===
    USE_CACHE: bool = True
    CACHE_PATH: str = "./terrain_cache/"
    
    # === MEMORY MANAGEMENT ===
    MEMORY_BUDGET_MB: int = 2048
    CHUNK_MEMORY_ESTIMATE_MB: int = 10
    
    def __post_init__(self):
        """Initialize computed properties after dataclass creation."""
        self.TILES_COUNT = self.WORLD_SIZE // self.TILE_SIZE
        
        # TODO: Add validation for configuration parameters
        # TODO: Add auto-detection of optimal MAX_WORKERS based on CPU
        # TODO: Add configuration file loading/saving functionality
    
    @property
    def tiles_count(self) -> int:
        """Calculate total number of tiles."""
        return self.TILES_COUNT
    
    def validate_config(self) -> bool:
        """
        Validate configuration parameters.
        
        Returns:
            bool: True if configuration is valid
            
        TODO: Implement comprehensive validation:
        - Check if WORLD_SIZE is divisible by TILE_SIZE
        - Validate memory settings
        - Check export path accessibility
        - Validate subdivision levels
        """
        return True
    
    def get_lod_config(self) -> Dict[str, Dict[str, Any]]:
        """
        Get LOD (Level of Detail) configuration.
        
        Returns:
            Dict containing LOD levels and their parameters
            
        TODO: Implement dynamic LOD configuration based on hardware capabilities
        """
        return {
            'ultra': {'max_distance': 200, 'subdivisions': self.HIGH_DETAIL_SUBDIVISIONS * 1.3},
            'high': {'max_distance': 500, 'subdivisions': self.HIGH_DETAIL_SUBDIVISIONS},
            'medium': {'max_distance': 1000, 'subdivisions': self.MEDIUM_DETAIL_SUBDIVISIONS},
            'low': {'max_distance': 2000, 'subdivisions': self.LOW_DETAIL_SUBDIVISIONS},
            'ultra_low': {'max_distance': float('inf'), 'subdivisions': 10}
        }
    
    def get_geological_config(self) -> Dict[str, Any]:
        """
        Get geological system configuration.
        
        Returns:
            Dict containing geological parameters
            
        TODO: Make geological parameters configurable
        TODO: Add biome-specific configurations
        """
        return {
            'tectonic_strength': 2.0,
            'mountain_height_factor': 1.0,
            'erosion_factor': 0.5,
            'river_density': 0.3,
            'basin_depth_factor': 1.0
        }
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'TerrainConfig':
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            TerrainConfig instance
            
        TODO: Implement JSON/YAML configuration file loading
        """
        # For now, return default config
        return cls()
    
    def save_to_file(self, config_path: str) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path where to save configuration
            
        TODO: Implement JSON/YAML configuration file saving
        """
        pass


class PerformanceProfile:
    """
    Performance profiles for different hardware configurations.
    """
    
    @staticmethod
    def get_low_end_config() -> TerrainConfig:
        """
        Configuration optimized for low-end hardware.
        
        TODO: Implement low-end optimized settings
        """
        config = TerrainConfig()
        config.WORLD_SIZE = 2000
        config.MAX_WORKERS = 2
        config.MEMORY_BUDGET_MB = 512
        return config
    
    @staticmethod
    def get_high_end_config() -> TerrainConfig:
        """
        Configuration optimized for high-end hardware.
        
        TODO: Implement high-end optimized settings
        """
        config = TerrainConfig()
        config.WORLD_SIZE = 16000
        config.MAX_WORKERS = 16
        config.MEMORY_BUDGET_MB = 8192
        return config
