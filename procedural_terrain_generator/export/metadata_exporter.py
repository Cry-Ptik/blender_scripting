"""
Metadata export system for procedural terrain.
Handles export of terrain information, statistics, and configuration data.
"""

import json
import os
from typing import Dict, List, Any, Tuple
import numpy as np
# Conditional import for Blender API
try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    from mock_bpy import mock_bpy as bpy


class TerrainInfoGenerator:
    """
    Generates comprehensive terrain information for external engines.
    """
    
    def __init__(self, config):
        """
        Initialize terrain info generator.
        
        Args:
            config: Terrain configuration object
        """
        self.config = config
        
        # TODO: Add info generation templates
        # TODO: Implement custom info formats
    
    def generate_tile_statistics(self, tile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate statistics for a single terrain tile.
        
        Args:
            tile_data: Tile elevation and geological data
            
        Returns:
            Dictionary containing tile statistics
            
        TODO: Add comprehensive geological statistics
        TODO: Include material distribution data
        """
        elevation = tile_data['elevation']
        
        stats = {
            'elevation': {
                'min': float(np.min(elevation)),
                'max': float(np.max(elevation)),
                'mean': float(np.mean(elevation)),
                'std': float(np.std(elevation)),
                'range': float(np.max(elevation) - np.min(elevation))
            },
            'geometry': {
                'resolution': elevation.shape,
                'vertex_count': elevation.size,
                'face_count': (elevation.shape[0] - 1) * (elevation.shape[1] - 1) * 2
            }
        }
        
        # Add geological statistics if available
        if 'geological_data' in tile_data:
            geological_data = tile_data['geological_data']
            stats['geology'] = {}
            
            for layer_name, layer_data in geological_data.items():
                if isinstance(layer_data, np.ndarray):
                    stats['geology'][layer_name] = {
                        'min': float(np.min(layer_data)),
                        'max': float(np.max(layer_data)),
                        'mean': float(np.mean(layer_data))
                    }
        
        return stats
    
    def generate_world_overview(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate overview statistics for the entire world.
        
        Args:
            all_tiles: Dictionary of all terrain tiles
            
        Returns:
            World overview statistics
            
        TODO: Add world-scale geological analysis
        TODO: Include biome distribution statistics
        """
        world_stats = {
            'world_size': self.config.WORLD_SIZE,
            'tile_size': self.config.TILE_SIZE,
            'tiles_count': self.config.TILES_COUNT,
            'total_tiles': len(all_tiles),
            'master_seed': self.config.MASTER_SEED
        }
        
        # Calculate world elevation statistics
        all_elevations = []
        for tile_data in all_tiles.values():
            all_elevations.extend(tile_data['elevation'].flatten())
        
        all_elevations = np.array(all_elevations)
        world_stats['elevation'] = {
            'global_min': float(np.min(all_elevations)),
            'global_max': float(np.max(all_elevations)),
            'global_mean': float(np.mean(all_elevations)),
            'global_std': float(np.std(all_elevations))
        }
        
        return world_stats


class MetadataExporter:
    """
    Main metadata export system for terrain data.
    """
    
    def __init__(self, config):
        """
        Initialize metadata exporter.
        
        Args:
            config: Terrain configuration object
        """
        self.config = config
        self.export_path = bpy.path.abspath(config.GODOT_EXPORT_PATH)
        self.info_generator = TerrainInfoGenerator(config)
        
        # TODO: Add metadata format options (JSON, XML, YAML)
        # TODO: Implement metadata validation
    
    def export_tile_info(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> None:
        """
        Export comprehensive tile information.
        
        Args:
            all_tiles: Dictionary of all terrain tiles
            
        TODO: Port export_tile_info method from original script
        TODO: Add export format options
        """
        print("📋 Export des métadonnées...")
        
        # Generate world overview
        world_overview = self.info_generator.generate_world_overview(all_tiles)
        
        # Generate detailed tile information
        tile_info = {
            'world_info': world_overview,
            'tiles': {}
        }
        
        for (tile_x, tile_y), tile_data in all_tiles.items():
            tile_key = f"{tile_x}_{tile_y}"
            tile_stats = self.info_generator.generate_tile_statistics(tile_data)
            
            tile_info['tiles'][tile_key] = {
                'coordinates': {'x': tile_x, 'y': tile_y},
                'subdivisions': tile_data['tile_info']['subdivisions'],
                'statistics': tile_stats,
                'world_position': {
                    'start_x': (tile_x * self.config.TILE_SIZE) - (self.config.WORLD_SIZE / 2),
                    'start_y': (tile_y * self.config.TILE_SIZE) - (self.config.WORLD_SIZE / 2),
                    'end_x': ((tile_x + 1) * self.config.TILE_SIZE) - (self.config.WORLD_SIZE / 2),
                    'end_y': ((tile_y + 1) * self.config.TILE_SIZE) - (self.config.WORLD_SIZE / 2)
                }
            }
        
        # Export tile information
        info_file = os.path.join(self.export_path, "terrain_info.json")
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(tile_info, f, indent=2, ensure_ascii=False)
    
    def export_configuration(self) -> None:
        """
        Export terrain generation configuration.
        
        TODO: Export complete configuration for reproducibility
        TODO: Add configuration validation
        """
        config_data = {
            'world_parameters': {
                'world_size': self.config.WORLD_SIZE,
                'tile_size': self.config.TILE_SIZE,
                'master_seed': self.config.MASTER_SEED
            },
            'resolution_settings': {
                'high_detail_subdivisions': self.config.HIGH_DETAIL_SUBDIVISIONS,
                'medium_detail_subdivisions': self.config.MEDIUM_DETAIL_SUBDIVISIONS,
                'low_detail_subdivisions': self.config.LOW_DETAIL_SUBDIVISIONS
            },
            'performance_settings': {
                'max_vertices_per_chunk': self.config.MAX_VERTICES_PER_CHUNK,
                'use_numpy_vectorization': self.config.USE_NUMPY_VECTORIZATION,
                'parallel_processing': self.config.PARALLEL_PROCESSING,
                'max_workers': self.config.MAX_WORKERS
            },
            'export_settings': {
                'export_heightmaps': self.config.EXPORT_HEIGHTMAPS,
                'export_splat_maps': self.config.EXPORT_SPLAT_MAPS,
                'export_normal_maps': self.config.EXPORT_NORMAL_MAPS,
                'export_format': getattr(self.config, 'EXPORT_FORMAT', 'obj')
            }
        }
        
        config_file = os.path.join(self.export_path, "generation_config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2)
    
    def export_geological_metadata(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> None:
        """
        Export geological system metadata.
        
        Args:
            all_tiles: Dictionary of terrain tiles
            
        TODO: Export geological formation data
        TODO: Add tectonic plate information
        """
        geological_metadata = {
            'geological_systems': {
                'tectonic_plates': [],
                'mountain_ranges': [],
                'river_networks': [],
                'basin_systems': []
            },
            'geological_parameters': {
                'tectonic_strength': 2.0,
                'mountain_height_factor': 1.0,
                'erosion_factor': 0.5,
                'river_density': 0.3
            }
        }
        
        # TODO: Extract geological system data from tiles
        # TODO: Add geological formation analysis
        
        geo_file = os.path.join(self.export_path, "geological_metadata.json")
        with open(geo_file, 'w', encoding='utf-8') as f:
            json.dump(geological_metadata, f, indent=2)
    
    def export_performance_report(self, generation_stats: Dict[str, Any]) -> None:
        """
        Export performance and generation statistics.
        
        Args:
            generation_stats: Statistics from terrain generation
            
        TODO: Add detailed performance metrics
        TODO: Include memory usage statistics
        """
        performance_report = {
            'generation_time': generation_stats.get('generation_time', 0),
            'tiles_generated': generation_stats.get('tiles_generated', 0),
            'performance_metrics': {
                'tiles_per_second': generation_stats.get('tiles_per_second', 0),
                'memory_usage_mb': generation_stats.get('memory_usage_mb', 0),
                'cache_hit_rate': generation_stats.get('cache_hit_rate', 0)
            },
            'optimization_settings': {
                'parallel_processing': self.config.PARALLEL_PROCESSING,
                'max_workers': self.config.MAX_WORKERS,
                'cache_enabled': self.config.USE_CACHE
            }
        }
        
        perf_file = os.path.join(self.export_path, "performance_report.json")
        with open(perf_file, 'w', encoding='utf-8') as f:
            json.dump(performance_report, f, indent=2)
    
    def create_readme_file(self) -> None:
        """
        Create README file with export information.
        
        TODO: Generate comprehensive documentation
        TODO: Add usage instructions for different engines
        """
        readme_content = f"""# Procedural Terrain Export

This directory contains exported terrain data generated by the Procedural Terrain Generator.

## World Information
- World Size: {self.config.WORLD_SIZE}m x {self.config.WORLD_SIZE}m
- Tile Size: {self.config.TILE_SIZE}m x {self.config.TILE_SIZE}m
- Total Tiles: {self.config.TILES_COUNT}²
- Master Seed: {self.config.MASTER_SEED}

## Directory Structure
- `meshes/` - Terrain mesh files (OBJ/GLTF format)
- `heightmaps/` - Elevation data in various formats
- `normal_maps/` - Generated normal maps for terrain detail
- `splat_maps/` - Material blending maps
- `terrain_info.json` - Comprehensive terrain metadata
- `generation_config.json` - Generation parameters used
- `terrain_manager.gd` - Godot script for terrain streaming

## Usage in Godot
1. Copy the terrain_manager.gd script to your Godot project
2. Attach the script to a Node3D in your scene
3. Configure the export path in the script
4. The terrain will automatically stream based on player position

## File Formats
- Meshes: {'GLTF' if getattr(self.config, 'EXPORT_FORMAT', 'obj') == 'gltf' else 'OBJ'}
- Heightmaps: RAW (16-bit) and PNG formats
- Metadata: JSON format

## Performance Notes
- Generated with {self.config.MAX_WORKERS} worker threads
- {'Cache enabled' if self.config.USE_CACHE else 'Cache disabled'}
- {'Parallel processing enabled' if self.config.PARALLEL_PROCESSING else 'Sequential processing'}

For more information, see the generation_config.json file.
"""
        
        readme_file = os.path.join(self.export_path, "README.md")
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
    
    def validate_export_completeness(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate that all expected files were exported.
        
        Args:
            all_tiles: Dictionary of terrain tiles
            
        Returns:
            Validation report
            
        TODO: Check file existence and integrity
        TODO: Validate file formats and sizes
        """
        validation_report = {
            'total_tiles': len(all_tiles),
            'missing_files': [],
            'validation_passed': True,
            'file_counts': {
                'meshes': 0,
                'heightmaps': 0,
                'metadata_files': 0
            }
        }
        
        # Check mesh files
        mesh_dir = os.path.join(self.export_path, "meshes")
        if os.path.exists(mesh_dir):
            mesh_files = os.listdir(mesh_dir)
            validation_report['file_counts']['meshes'] = len(mesh_files)
        
        # Check heightmap files
        heightmap_dir = os.path.join(self.export_path, "heightmaps")
        if os.path.exists(heightmap_dir):
            heightmap_files = os.listdir(heightmap_dir)
            validation_report['file_counts']['heightmaps'] = len(heightmap_files)
        
        # Check metadata files
        expected_metadata = ['terrain_info.json', 'generation_config.json', 'README.md']
        for metadata_file in expected_metadata:
            if os.path.exists(os.path.join(self.export_path, metadata_file)):
                validation_report['file_counts']['metadata_files'] += 1
            else:
                validation_report['missing_files'].append(metadata_file)
        
        if validation_report['missing_files']:
            validation_report['validation_passed'] = False
        
        return validation_report
