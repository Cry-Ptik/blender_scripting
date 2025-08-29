#!/usr/bin/env python3
"""
Simple test for MountainSystem functionality
"""

import sys
import os
import numpy as np

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        print("Testing MountainSystem...")
        
        # Import modules
        from core.math_utils import MountainSystem
        from core.noise import OptimizedNoise
        
        # Initialize
        noise = OptimizedNoise()
        mountain_system = MountainSystem(1000.0, noise)
        
        print("✓ MountainSystem created successfully")
        
        # Generate ranges
        ranges = mountain_system.generate_mountain_ranges()
        print(f"✓ Generated {len(ranges)} mountain ranges")
        
        # Test elevation calculation
        x = np.array([[0, 500], [250, 750]])
        y = np.array([[0, 250], [500, 750]])
        
        elevation = mountain_system.calculate_elevation(x, y)
        print(f"✓ Elevation calculated: {elevation.shape}")
        print(f"  Min elevation: {elevation.min():.2f}")
        print(f"  Max elevation: {elevation.max():.2f}")
        
        print("\n🎉 MountainSystem working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
