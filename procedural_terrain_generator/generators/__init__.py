"""
Terrain generation modules for procedural terrain.
Handles main generation logic and parallel processing coordination.
"""

from .terrain_generator import TerrainGenerator, WorldGenerator
from .parallel_processor import ParallelProcessor, TerrainTask

__all__ = [
    'TerrainGenerator', 'WorldGenerator',
    'ParallelProcessor', 'TerrainTask'
]
