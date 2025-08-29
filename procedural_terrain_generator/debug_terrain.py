#!/usr/bin/env python3
"""
Debug script to test terrain generation and identify mesh creation issues.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
from generators.terrain_generator import TerrainGenerator, WorldGenerator
from config.settings import TerrainConfig

def test_terrain_generation():
    """Test basic terrain generation without Blender."""
    print("🔍 Testing terrain generation...")
    
    # Initialize config
    config = TerrainConfig()
    
    # Create terrain generator
    terrain_gen = TerrainGenerator(config)
    
    # Test user parameters
    user_params = {
        'erosion_strength': 0.5,
        'erosion_iterations': 10000,
        'tectonic_strength': 1.0,
        'tectonic_plates': 8,
        'mountain_height_scale': 2.0,
        'mountain_ranges': 5,
        'temperature_variation': 1.2,
        'humidity_variation': 1.1
    }
    
    terrain_gen.apply_user_parameters(user_params)
    
    # Generate a single tile
    tile_coords = (0, 0, "medium")
    print(f"📍 Generating tile at {tile_coords}...")
    
    try:
        tile_data = terrain_gen.generate_single_tile(tile_coords)
        
        if tile_data:
            elevation = tile_data.get('elevation')
            coordinates = tile_data.get('coordinates')
            
            if elevation is not None:
                print(f"✅ Elevation data shape: {elevation.shape}")
                print(f"📊 Elevation range: {np.min(elevation):.2f} to {np.max(elevation):.2f}")
                print(f"📈 Elevation mean: {np.mean(elevation):.2f}")
                print(f"📉 Elevation std: {np.std(elevation):.2f}")
                
                # Check for flat terrain
                if np.std(elevation) < 0.1:
                    print("⚠️ WARNING: Terrain appears very flat!")
                
                if coordinates:
                    X, Y = coordinates
                    print(f"🗺️ Coordinate ranges: X[{np.min(X):.1f}, {np.max(X):.1f}], Y[{np.min(Y):.1f}, {np.max(Y):.1f}]")
                
                return True
            else:
                print("❌ No elevation data generated")
                return False
        else:
            print("❌ No tile data generated")
            return False
            
    except Exception as e:
        print(f"❌ Error generating terrain: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_world_generation():
    """Test world generation with mesh creation."""
    print("\n🌍 Testing world generation...")
    
    config = TerrainConfig()
    world_gen = WorldGenerator(config)
    
    # Apply user parameters
    user_params = {
        'erosion_strength': 0.8,
        'mountain_height_scale': 3.0,
        'mountain_ranges': 3
    }
    
    world_gen.apply_user_parameters(user_params)
    
    try:
        # Generate preview area (smaller test)
        print("🎯 Generating preview area...")
        result = world_gen.generate_preview_area()
        
        print(f"📋 Generation result: {result}")
        
        if result.get('status') == 'success':
            print("✅ World generation successful")
            return True
        else:
            print(f"❌ World generation failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error in world generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function."""
    print("🚀 Starting terrain generation debug...")
    
    # Test basic terrain generation
    terrain_ok = test_terrain_generation()
    
    # Test world generation
    world_ok = test_world_generation()
    
    print(f"\n📊 Debug Results:")
    print(f"   Terrain Generation: {'✅ OK' if terrain_ok else '❌ FAILED'}")
    print(f"   World Generation: {'✅ OK' if world_ok else '❌ FAILED'}")
    
    if not terrain_ok:
        print("\n🔧 Terrain generation issues detected. Check:")
        print("   - Noise generation systems")
        print("   - Mountain elevation calculation")
        print("   - Geological systems initialization")
    
    if not world_ok:
        print("\n🔧 World generation issues detected. Check:")
        print("   - Mesh creation pipeline")
        print("   - Blender object creation")
        print("   - Scene organization")

if __name__ == "__main__":
    main()
