"""
Blender integration modules for procedural terrain generation.
Handles mesh creation, materials, and Blender-specific optimizations.
"""

from .mesh_creator import BlenderMeshCreator, OptimizedMeshBuilder
from .materials import MaterialSystem, TerrainMaterialGenerator
from .scene_optimizer import SceneOptimizer, ViewportOptimizer

__all__ = [
    'BlenderMeshCreator', 'OptimizedMeshBuilder',
    'MaterialSystem', 'TerrainMaterialGenerator', 
    'SceneOptimizer', 'ViewportOptimizer'
]
