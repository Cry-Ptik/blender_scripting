"""
Main terrain generation system coordinating all subsystems.
Orchestrates geological generation, mesh creation, and export processes.
"""

import time
import sys
import os
import numpy as np
from typing import Dict, List, Any, Tuple, Optional

# Add parent directory to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TerrainConfig
from core import GeologicalSystem, OptimizedNoise, BiomeSystem
from blender import BlenderMeshCreator, MaterialSystem, SceneOptimizer
from export import GodotExporter, HeightmapExporter, MetadataExporter
from runtime import LODManager, TerrainStreaming, CacheManager, MemoryManager
from generators.parallel_processor import ParallelProcessor


class TerrainGenerator:
    """
    Core terrain generator for individual tiles.
    Handles single tile generation with geological and noise systems.
    """
    
    def __init__(self, config: TerrainConfig):
        """
        Initialize terrain generator.
        
        Args:
            config: Terrain configuration object
        """
        self.config = config
        
        # Initialize core systems
        self.noise_generator = OptimizedNoise(config.MASTER_SEED)
        self.biome_system = BiomeSystem(config.WORLD_SIZE, sea_level=0.0)
        self.geological_system = GeologicalSystem(config, self.noise_generator, self.biome_system)
        
        # Initialize cache if enabled
        self.cache_manager = CacheManager(config) if config.USE_CACHE else None
        
        # Store user parameters for customization
        self.user_params = {}
    
    def apply_user_parameters(self, params: Dict[str, Any]):
        """
        Apply user-defined parameters to terrain generation systems.
        
        Args:
            params: Dictionary of user parameters
        """
        self.user_params = params
        
        # Apply erosion parameters
        if hasattr(self.geological_system, 'erosion'):
            if 'erosion_strength' in params:
                self.geological_system.erosion.erosion_speed = params['erosion_strength']
            if 'erosion_iterations' in params:
                self.geological_system.erosion.num_droplets = params['erosion_iterations']
        
        # Apply tectonic parameters
        if hasattr(self.geological_system, 'tectonics'):
            if 'tectonic_strength' in params:
                self.geological_system.tectonics.strength_multiplier = params['tectonic_strength']
            if 'tectonic_plates' in params:
                self.geological_system.tectonics.num_plates = params['tectonic_plates']
        
        # Apply mountain parameters
        if hasattr(self.geological_system, 'mountains'):
            if 'mountain_height_scale' in params:
                self.geological_system.mountains.height_scale = params['mountain_height_scale']
            if 'mountain_ranges' in params:
                self.geological_system.mountains.target_range_count = params['mountain_ranges']
        
        # Apply biome parameters
        if hasattr(self.geological_system, 'biomes'):
            if 'temperature_variation' in params:
                self.geological_system.biomes.temperature_scale = params['temperature_variation']
            if 'humidity_variation' in params:
                self.geological_system.biomes.humidity_scale = params['humidity_variation']
    
    def generate_single_tile(self, tile_coords: Tuple[int, int, str]) -> Dict[str, Any]:
        """
        Generate a single terrain tile.
        
        Args:
            tile_coords: (tile_x, tile_y, detail_level) coordinates
            
        Returns:
            Generated tile data
        """
        try:
            tile_x, tile_y, detail_level = tile_coords
            
            # Get subdivisions for detail level
            subdivisions = self._get_subdivisions_for_detail(detail_level)
            
            # Generate coordinate arrays
            x_start = tile_x * self.config.TILE_SIZE
            y_start = tile_y * self.config.TILE_SIZE
            x_end = x_start + self.config.TILE_SIZE
            y_end = y_start + self.config.TILE_SIZE
            
            x = np.linspace(x_start, x_end, subdivisions)
            y = np.linspace(y_start, y_end, subdivisions)
            X, Y = np.meshgrid(x, y)
            
            # Generate terrain elevation using geological system
            elevation = self.geological_system.generate_elevation(X, Y)
            
            # Generate biome data
            biome_data = self.biome_system.generate_biome_data(X, Y, elevation)
            
            return {
                'elevation': elevation,
                'coordinates': (X, Y),
                'biome_data': biome_data,
                'tile_coords': tile_coords,
                'subdivisions': subdivisions
            }
            
        except Exception as e:
            print(f"Error generating tile {tile_coords}: {e}")
            return None
    
    def _get_subdivisions_for_detail(self, detail_level: str) -> int:
        """
        Get subdivision count for detail level.
        
        Args:
            detail_level: Detail level string
            
        Returns:
            Number of subdivisions
        """
        detail_map = {
            "high": self.config.HIGH_DETAIL_SUBDIVISIONS,
            "medium": self.config.MEDIUM_DETAIL_SUBDIVISIONS,
            "low": self.config.LOW_DETAIL_SUBDIVISIONS
        }
        return detail_map.get(detail_level, self.config.MEDIUM_DETAIL_SUBDIVISIONS)


class WorldGenerator:
    """
    High-level world generator coordinating all terrain generation systems.
    Manages the complete pipeline from generation to export.
    """
    
    def __init__(self, config: Optional[TerrainConfig] = None):
        """
        Initialize world generator.
        
        Args:
            config: Terrain configuration (creates default if None)
        """
        self.config = config or TerrainConfig()
        
        # Initialize subsystems
        self.terrain_generator = TerrainGenerator(self.config)
        self.parallel_processor = ParallelProcessor(self.config, self.terrain_generator)
        self.mesh_creator = BlenderMeshCreator(self.config)
        self.material_system = MaterialSystem(self.config)
        self.scene_optimizer = SceneOptimizer(self.config)
        
        # Initialize export systems
        self.godot_exporter = GodotExporter(self.config)
        self.heightmap_exporter = HeightmapExporter(self.config)
        self.metadata_exporter = MetadataExporter(self.config)
        
        # Initialize runtime systems
        self.lod_manager = LODManager(self.config)
        self.terrain_streaming = TerrainStreaming(self.config)
        self.memory_manager = MemoryManager(self.config)
        
        # Generation statistics
        self.generation_stats = {}
    
    def apply_user_parameters(self, params: Dict[str, Any]):
        """
        Apply user-defined parameters to all terrain generation systems.
        
        Args:
            params: Dictionary of user parameters
        """
        # Apply parameters to the terrain generator
        self.terrain_generator.apply_user_parameters(params)
    
    def generate_complete_world(self) -> Dict[str, Any]:
        """
        Generate complete world with all systems.
        
        Returns:
            Generation results dictionary
        """
        try:
            # Simple implementation for testing
            tile_coords = (0, 0, "medium")
            tile_data = self.terrain_generator.generate_single_tile(tile_coords)
            
            if tile_data:
                # Create mesh
                terrain_obj = self.mesh_creator.create_tile_mesh(tile_data, 0, 0)
                
                # Apply materials
                materials = self.material_system.setup_terrain_materials()
                self.material_system.assign_material_to_objects([terrain_obj], "base")
                
                return {
                    'tiles_generated': 1,
                    'terrain_objects': [terrain_obj],
                    'status': 'success'
                }
            else:
                return {
                    'tiles_generated': 0,
                    'status': 'error',
                    'error': 'Failed to generate tile'
                }
                
        except Exception as e:
            return {
                'tiles_generated': 0,
                'status': 'error',
                'error': str(e)
            }
    
    def generate_preview_area(self, center_x: int = 0, center_y: int = 0, radius: int = 1) -> Dict[str, Any]:
        """
        Generate preview area around center coordinates.
        
        Args:
            center_x: Center tile X coordinate
            center_y: Center tile Y coordinate
            radius: Radius in tiles
            
        Returns:
            Generation results
        """
        try:
            results = []
            
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    tile_x = center_x + dx
                    tile_y = center_y + dy
                    
                    tile_coords = (tile_x, tile_y, "medium")
                    tile_data = self.terrain_generator.generate_single_tile(tile_coords)
                    
                    if tile_data:
                        # Create mesh
                        terrain_obj = self.mesh_creator.create_tile_mesh(tile_data, tile_x, tile_y)
                        results.append(terrain_obj)
            
            # Apply materials to all objects
            if results:
                materials = self.material_system.setup_terrain_materials()
                self.material_system.assign_material_to_objects(results, "base")
            
            return {
                'tiles_generated': len(results),
                'terrain_objects': results,
                'status': 'success'
            }
            
        except Exception as e:
            return {
                'tiles_generated': 0,
                'terrain_objects': [],
                'status': 'error',
                'error': str(e)
            }
    
    def export_to_godot(self, export_path: str):
        """
        Export terrain to Godot format.
        
        Args:
            export_path: Path to export directory
        """
        try:
            self.godot_exporter.export_terrain(export_path)
        except Exception as e:
            print(f"Export error: {e}")
