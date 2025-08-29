"""
Test script for CLI functionality - creates minimal placeholders to test the CLI.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test imports
try:
    from config import TerrainConfig, PerformanceProfile
    print("✅ Config import OK")
except ImportError as e:
    print(f"❌ Config import failed: {e}")

# Create minimal placeholders for missing modules
def create_placeholder_modules():
    """Create minimal placeholder modules for testing."""
    
    # Create core placeholders
    core_init = """
from .noise import OptimizedNoise
from .geology import GeologicalSystem
from .math_utils import MathUtils

__all__ = ['OptimizedNoise', 'GeologicalSystem', 'MathUtils']
"""
    
    noise_py = """
class OptimizedNoise:
    def __init__(self, seed):
        self.seed = seed
"""
    
    geology_py = """
class GeologicalSystem:
    def __init__(self, config, noise_gen):
        self.config = config
        self.noise_gen = noise_gen
    
    def precompute_geological_features(self):
        print("🏔️ Geological features precomputed (placeholder)")
    
    def generate_tile_geology(self, x, y, subdivisions):
        return {'height_data': [], 'geology_type': 'mountain'}
"""
    
    math_utils_py = """
class MathUtils:
    @staticmethod
    def interpolate(a, b, t):
        return a + (b - a) * t
"""
    
    # Create blender placeholders
    blender_init = """
from .mesh_creator import BlenderMeshCreator
from .materials import MaterialSystem
from .scene_optimizer import SceneOptimizer

__all__ = ['BlenderMeshCreator', 'MaterialSystem', 'SceneOptimizer']
"""
    
    mesh_creator_py = """
class BlenderMeshCreator:
    def __init__(self, config):
        self.config = config
    
    def create_world_from_tiles(self, tiles):
        print(f"🏗️ Creating meshes for {len(tiles)} tiles (placeholder)")
        return []
"""
    
    materials_py = """
class MaterialSystem:
    def __init__(self, config):
        self.config = config
    
    def setup_terrain_materials(self):
        print("🎨 Setting up materials (placeholder)")
        return {}
    
    def assign_material_to_objects(self, objects, material_name):
        print(f"🎨 Assigning {material_name} to {len(objects)} objects (placeholder)")
"""
    
    scene_optimizer_py = """
class SceneOptimizer:
    def __init__(self, config):
        self.config = config
    
    def setup_optimized_scene(self):
        print("⚡ Setting up optimized scene (placeholder)")
    
    def apply_final_optimizations(self, objects):
        print(f"⚡ Applying optimizations to {len(objects)} objects (placeholder)")
"""
    
    # Create export placeholders
    export_init = """
from .godot_exporter import GodotExporter
from .heightmap_exporter import HeightmapExporter
from .metadata_exporter import MetadataExporter

__all__ = ['GodotExporter', 'HeightmapExporter', 'MetadataExporter']
"""
    
    godot_exporter_py = """
class GodotExporter:
    def __init__(self, config):
        self.config = config
    
    def export_for_godot(self, tiles):
        print(f"🎮 Exporting {len(tiles)} tiles for Godot (placeholder)")
"""
    
    heightmap_exporter_py = """
class HeightmapExporter:
    def __init__(self, config):
        self.config = config
    
    def export_heightmaps(self, tiles):
        print(f"🗻 Exporting heightmaps for {len(tiles)} tiles (placeholder)")
"""
    
    metadata_exporter_py = """
class MetadataExporter:
    def __init__(self, config):
        self.config = config
    
    def export_tile_info(self, tiles):
        print(f"📄 Exporting metadata for {len(tiles)} tiles (placeholder)")
    
    def export_configuration(self):
        print("📄 Exporting configuration (placeholder)")
    
    def create_readme_file(self):
        print("📄 Creating README file (placeholder)")
"""
    
    # Create runtime placeholders
    runtime_init = """
from .lod_system import LODManager
from .streaming import TerrainStreaming
from .cache_manager import CacheManager
from .memory_manager import MemoryManager

__all__ = ['LODManager', 'TerrainStreaming', 'CacheManager', 'MemoryManager']
"""
    
    lod_system_py = """
class LODManager:
    def __init__(self, config):
        self.config = config
"""
    
    streaming_py = """
class TerrainStreaming:
    def __init__(self, config):
        self.config = config
"""
    
    cache_manager_py = """
class CacheManager:
    def __init__(self, config):
        self.config = config
    
    def get_cache_key(self, x, y, seed, detail):
        return f"{x}_{y}_{seed}_{detail}"
    
    def get_cached_data(self, cache_type, key):
        return None  # No cache for placeholder
    
    def cache_data(self, cache_type, key, data):
        pass  # No caching for placeholder
    
    def get_cache_statistics(self):
        return {'enabled': False, 'hit_rate': 0.0}
"""
    
    memory_manager_py = """
class MemoryManager:
    def __init__(self, config):
        self.config = config
    
    def get_memory_statistics(self):
        return {'memory_budget_mb': self.config.MEMORY_BUDGET_MB}
"""
    
    # Write all files
    files_to_create = [
        ('core/noise.py', noise_py),
        ('core/geology.py', geology_py),
        ('core/math_utils.py', math_utils_py),
        ('blender/mesh_creator.py', mesh_creator_py),
        ('blender/materials.py', materials_py),
        ('blender/scene_optimizer.py', scene_optimizer_py),
        ('export/godot_exporter.py', godot_exporter_py),
        ('export/heightmap_exporter.py', heightmap_exporter_py),
        ('export/metadata_exporter.py', metadata_exporter_py),
        ('runtime/lod_system.py', lod_system_py),
        ('runtime/streaming.py', streaming_py),
        ('runtime/cache_manager.py', cache_manager_py),
        ('runtime/memory_manager.py', memory_manager_py),
    ]
    
    for file_path, content in files_to_create:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        if not os.path.exists(full_path):
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Created {file_path}")
        else:
            print(f"⏭️ Skipped {file_path} (already exists)")

if __name__ == "__main__":
    print("🔧 Creating placeholder modules for CLI testing...")
    create_placeholder_modules()
    print("\n🎯 Testing CLI...")
    
    try:
        from cli import app
        print("✅ CLI import successful!")
        print("🚀 Run: python main.py --help")
    except ImportError as e:
        print(f"❌ CLI import failed: {e}")
