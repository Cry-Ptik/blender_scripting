"""
Heightmap and texture export system for procedural terrain.
Handles export of elevation data, normal maps, and texture atlases.
"""

import os
import numpy as np
from typing import Dict, List, Any, Tuple, Optional
# Conditional import for Blender API
try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False
    from mock_bpy import mock_bpy as bpy


class TextureExporter:
    """
    Exports various texture types for terrain rendering.
    """
    
    def __init__(self, config):
        """
        Initialize texture exporter.
        
        Args:
            config: Terrain configuration object
        """
        self.config = config
        self.export_path = bpy.path.abspath(config.GODOT_EXPORT_PATH)
        
        # TODO: Add texture format options (PNG, EXR, TIFF)
        # TODO: Implement texture compression settings
    
    def export_normal_maps(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> None:
        """
        Generate and export normal maps from elevation data.
        
        Args:
            all_tiles: Dictionary of terrain tiles
            
        TODO: Implement normal map generation from heightmaps
        TODO: Add normal map strength and detail controls
        """
        if not self.config.EXPORT_NORMAL_MAPS:
            return
        
        print("🗺️ Export des normal maps...")
        
        normal_dir = os.path.join(self.export_path, "normal_maps")
        os.makedirs(normal_dir, exist_ok=True)
        
        for (tile_x, tile_y), tile_data in all_tiles.items():
            elevation = tile_data['elevation']
            
            # TODO: Calculate gradients for normal map generation
            # TODO: Convert gradients to normal map format
            # TODO: Save as image file
            
            normal_file = os.path.join(normal_dir, f"normal_{tile_x}_{tile_y}.png")
            # TODO: Implement actual normal map export
    
    def export_splat_maps(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> None:
        """
        Generate and export splat maps for material blending.
        
        Args:
            all_tiles: Dictionary of terrain tiles
            
        TODO: Generate splat maps based on geological data
        TODO: Add material distribution algorithms
        """
        if not self.config.EXPORT_SPLAT_MAPS:
            return
        
        print("🎨 Export des splat maps...")
        
        splat_dir = os.path.join(self.export_path, "splat_maps")
        os.makedirs(splat_dir, exist_ok=True)
        
        for (tile_x, tile_y), tile_data in all_tiles.items():
            # TODO: Analyze geological data for material distribution
            # TODO: Generate RGBA splat map
            # TODO: Export as texture file
            
            splat_file = os.path.join(splat_dir, f"splat_{tile_x}_{tile_y}.png")
            # TODO: Implement splat map generation and export
    
    def create_texture_atlas(self, texture_list: List[str]) -> str:
        """
        Create texture atlas from individual textures.
        
        Args:
            texture_list: List of texture file paths
            
        Returns:
            Path to created texture atlas
            
        TODO: Implement texture atlas packing algorithm
        TODO: Add UV coordinate adjustment for atlas usage
        """
        atlas_path = os.path.join(self.export_path, "texture_atlas.png")
        
        # TODO: Load individual textures
        # TODO: Pack textures into atlas using efficient algorithm
        # TODO: Generate UV mapping data
        # TODO: Save atlas and mapping information
        
        return atlas_path


class HeightmapExporter:
    """
    Exports heightmaps in various formats for terrain engines.
    """
    
    def __init__(self, config):
        """
        Initialize heightmap exporter.
        
        Args:
            config: Terrain configuration object
        """
        self.config = config
        self.export_path = bpy.path.abspath(config.GODOT_EXPORT_PATH)
        self.texture_exporter = TextureExporter(config)
        
        # TODO: Add heightmap format options
        # TODO: Implement bit depth selection (8-bit, 16-bit, 32-bit)
    
    def export_heightmaps(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> None:
        """
        Export heightmaps for all terrain tiles.
        
        Args:
            all_tiles: Dictionary of terrain tiles
            
        TODO: Port export_heightmaps method from original script
        TODO: Add multiple format support (RAW, PNG, EXR)
        """
        print("🗻 Export des heightmaps...")
        
        heightmap_dir = os.path.join(self.export_path, "heightmaps")
        os.makedirs(heightmap_dir, exist_ok=True)
        
        exported_count = 0
        total_tiles = len(all_tiles)
        
        for (tile_x, tile_y), tile_data in all_tiles.items():
            elevation = tile_data['elevation']
            
            # Normalize elevation data for export
            normalized_elevation = self._normalize_elevation_for_export(elevation)
            
            # Export in multiple formats
            self._export_heightmap_raw(normalized_elevation, tile_x, tile_y, heightmap_dir)
            self._export_heightmap_png(normalized_elevation, tile_x, tile_y, heightmap_dir)
            
            exported_count += 1
            if exported_count % 10 == 0:
                print(f"📊 Heightmaps exported: {exported_count}/{total_tiles}")
        
        # Export additional texture maps
        self.texture_exporter.export_normal_maps(all_tiles)
        self.texture_exporter.export_splat_maps(all_tiles)
    
    def _normalize_elevation_for_export(self, elevation: np.ndarray) -> np.ndarray:
        """
        Normalize elevation data for export format.
        
        Args:
            elevation: Raw elevation data
            
        Returns:
            Normalized elevation data
            
        TODO: Add different normalization methods
        TODO: Preserve elevation range information for reconstruction
        """
        # Normalize to 0-65535 range for 16-bit export
        min_elev = np.min(elevation)
        max_elev = np.max(elevation)
        
        if max_elev == min_elev:
            return np.zeros_like(elevation, dtype=np.uint16)
        
        normalized = ((elevation - min_elev) / (max_elev - min_elev)) * 65535
        return normalized.astype(np.uint16)
    
    def _export_heightmap_raw(self, elevation: np.ndarray, tile_x: int, tile_y: int, 
                             output_dir: str) -> None:
        """
        Export heightmap in RAW format.
        
        Args:
            elevation: Normalized elevation data
            tile_x, tile_y: Tile coordinates
            output_dir: Output directory
            
        TODO: Add RAW format header information
        TODO: Support different bit depths
        """
        raw_file = os.path.join(output_dir, f"heightmap_{tile_x}_{tile_y}.raw")
        elevation.astype(np.uint16).tofile(raw_file)
    
    def _export_heightmap_png(self, elevation: np.ndarray, tile_x: int, tile_y: int,
                             output_dir: str) -> None:
        """
        Export heightmap as PNG image.
        
        Args:
            elevation: Normalized elevation data
            tile_x, tile_y: Tile coordinates
            output_dir: Output directory
            
        TODO: Use PIL or OpenCV for PNG export
        TODO: Add 16-bit PNG support for better precision
        """
        png_file = os.path.join(output_dir, f"heightmap_{tile_x}_{tile_y}.png")
        
        # TODO: Convert numpy array to image format
        # TODO: Save as PNG with proper bit depth
        # For now, save as numpy file (placeholder)
        np.save(png_file.replace('.png', '.npy'), elevation)
    
    def export_world_heightmap(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> str:
        """
        Export complete world as single large heightmap.
        
        Args:
            all_tiles: Dictionary of all terrain tiles
            
        Returns:
            Path to exported world heightmap
            
        TODO: Stitch individual tile heightmaps into world heightmap
        TODO: Handle memory efficiently for large worlds
        """
        print("🌍 Export du heightmap mondial...")
        
        # Calculate world heightmap dimensions
        tiles_count = self.config.TILES_COUNT
        
        # TODO: Determine tile resolution from first tile
        # TODO: Create large array to hold world heightmap
        # TODO: Copy tile data into world array
        # TODO: Export world heightmap in chunks if too large
        
        world_heightmap_path = os.path.join(self.export_path, "world_heightmap.raw")
        return world_heightmap_path
    
    def create_heightmap_pyramid(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> List[str]:
        """
        Create heightmap pyramid for LOD rendering.
        
        Args:
            all_tiles: Dictionary of terrain tiles
            
        Returns:
            List of paths to pyramid levels
            
        TODO: Generate multiple resolution levels
        TODO: Use proper downsampling algorithms
        """
        pyramid_levels = []
        
        # TODO: Generate LOD levels (1/2, 1/4, 1/8, etc.)
        # TODO: Use appropriate filtering for downsampling
        # TODO: Export each level as separate heightmap
        
        return pyramid_levels
    
    def export_heightmap_metadata(self, all_tiles: Dict[Tuple[int, int], Dict[str, Any]]) -> None:
        """
        Export metadata about heightmaps for proper reconstruction.
        
        Args:
            all_tiles: Dictionary of terrain tiles
            
        TODO: Export elevation ranges, scales, and offsets
        TODO: Add coordinate system information
        """
        metadata = {
            'format': 'uint16',
            'tiles': {},
            'world_bounds': {
                'min_x': -self.config.WORLD_SIZE / 2,
                'max_x': self.config.WORLD_SIZE / 2,
                'min_y': -self.config.WORLD_SIZE / 2,
                'max_y': self.config.WORLD_SIZE / 2
            }
        }
        
        for (tile_x, tile_y), tile_data in all_tiles.items():
            elevation = tile_data['elevation']
            metadata['tiles'][f"{tile_x}_{tile_y}"] = {
                'min_elevation': float(np.min(elevation)),
                'max_elevation': float(np.max(elevation)),
                'mean_elevation': float(np.mean(elevation)),
                'resolution': elevation.shape
            }
        
        metadata_file = os.path.join(self.export_path, "heightmap_metadata.json")
        import json
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
