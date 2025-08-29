"""
Core modules for procedural terrain generation.
Contains fundamental algorithms for noise generation, geology, and mathematical utilities.
"""

from .noise import OptimizedNoise, NoiseGenerator
from .geology import GeologicalSystem, TectonicPlates, RiverNetwork
from .math_utils import MountainSystem, MountainRange
from .math_utils import MathUtils, VectorizedOperations
from .tectonics import TectonicSystem, TectonicPlate
from .erosion import HydraulicErosion, WaterDroplet
from .biomes import BiomeSystem, BiomeType, BiomeProperties
from .lod import AdaptiveLOD, LODLevel, LODChunk

__all__ = [
    'OptimizedNoise', 'NoiseGenerator',
    'GeologicalSystem', 'TectonicPlates', 'MountainSystem', 'RiverNetwork',
    'TectonicSystem', 'TectonicPlate',
    'HydraulicErosion', 'WaterDroplet',
    'BiomeSystem', 'BiomeType', 'BiomeProperties',
    'AdaptiveLOD', 'LODLevel', 'LODChunk',
    'MathUtils', 'VectorizedOperations'
]
