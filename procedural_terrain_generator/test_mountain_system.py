#!/usr/bin/env python3
"""
Test script for MountainSystem moved to math_utils.py
"""

import sys
import os
import numpy as np

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_mountain_system():
    """Test MountainSystem initialization and basic functionality."""
    try:
        print("Testing MountainSystem from math_utils...")
        
        # Import required modules
        from core.math_utils import MountainSystem, MountainRange
        from core.noise import OptimizedNoise
        
        print("✓ Imports successful")
        
        # Initialize noise generator
        noise_generator = OptimizedNoise()
        print("✓ Noise generator created")
        
        # Initialize MountainSystem
        world_size = 1000.0
        mountain_system = MountainSystem(world_size, noise_generator)
        print("✓ MountainSystem initialized successfully")
        
        # Generate mountain ranges
        ranges = mountain_system.generate_mountain_ranges()
        print(f"✓ Generated {len(ranges)} mountain ranges")
        
        # Test elevation calculation
        x = np.linspace(0, world_size, 100)
        y = np.linspace(0, world_size, 100)
        X, Y = np.meshgrid(x, y)
        
        elevation = mountain_system.calculate_elevation(X, Y)
        print(f"✓ Elevation calculation successful, shape: {elevation.shape}")
        print(f"  Elevation range: {elevation.min():.2f} to {elevation.max():.2f}")
        
        # Test individual mountain range properties
        for i, mountain_range in enumerate(ranges):
            print(f"  Range {i+1}: center=({mountain_range.center_x:.1f}, {mountain_range.center_y:.1f}), "
                  f"height={mountain_range.height:.1f}m")
        
        print("\n✅ All MountainSystem tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing MountainSystem: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_geological_system_integration():
    """Test GeologicalSystem with new MountainSystem location."""
    try:
        print("\nTesting GeologicalSystem integration...")
        
        from core.geology import GeologicalSystem
        from core.noise import OptimizedNoise
        from core.biomes import BiomeSystem
        from config.settings import TerrainConfig
        
        # Initialize components
        noise_generator = OptimizedNoise()
        config = TerrainConfig()
        biome_system = BiomeSystem(world_size=config.WORLD_SIZE)
        
        # Initialize GeologicalSystem
        geological_system = GeologicalSystem(config, noise_generator, biome_system)
        print("✓ GeologicalSystem initialized with MountainSystem from math_utils")
        
        # Test terrain generation
        x = np.linspace(0, 1000, 50)
        y = np.linspace(0, 1000, 50)
        X, Y = np.meshgrid(x, y)
        
        elevation = geological_system.generate_terrain(X, Y)
        print(f"✓ Terrain generation successful, shape: {elevation.shape}")
        print(f"  Elevation range: {elevation.min():.2f} to {elevation.max():.2f}")
        
        print("✅ GeologicalSystem integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing GeologicalSystem integration: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MOUNTAIN SYSTEM TEST SUITE")
    print("=" * 60)
    
    success = True
    
    # Test MountainSystem directly
    success &= test_mountain_system()
    
    # Test integration with GeologicalSystem
    success &= test_geological_system_integration()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED - MountainSystem working correctly!")
    else:
        print("❌ SOME TESTS FAILED - Check errors above")
    print("=" * 60)
