"""
Simple test script to verify terrain generation core functionality.
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_core_systems():
    """Test core terrain generation systems without Blender dependencies."""
    print("🧪 TEST: Systèmes de base du générateur de terrain")
    print("=" * 60)
    
    try:
        # Test noise generation
        print("🔍 Test 1: Génération de bruit...")
        from core.noise import OptimizedNoise
        noise_gen = OptimizedNoise(seed=12345)
        
        # Generate test coordinates
        x = np.linspace(0, 1000, 100)
        y = np.linspace(0, 1000, 100)
        X, Y = np.meshgrid(x, y)
        
        # Test noise generation
        noise_values = noise_gen.generate_noise(X, Y)
        print(f"✅ Bruit généré: {noise_values.shape}, min={np.min(noise_values):.3f}, max={np.max(noise_values):.3f}")
        
        # Test mountain system
        print("🔍 Test 2: Système de montagnes...")
        from core.math_utils import MountainSystem
        mountain_sys = MountainSystem(1000.0, noise_gen)
        
        # Generate mountain ranges
        ranges = mountain_sys.generate_mountain_ranges()
        print(f"✅ Chaînes de montagnes générées: {len(ranges)}")
        
        # Test mountain elevation calculation
        mountain_elevation = mountain_sys.calculate_mountain_elevation(X, Y)
        print(f"✅ Élévation montagnes: min={np.min(mountain_elevation):.1f}m, max={np.max(mountain_elevation):.1f}m")
        
        # Test erosion system
        print("🔍 Test 3: Système d'érosion...")
        from core.erosion import HydraulicErosion
        erosion_sys = HydraulicErosion()
        
        # Create test heightmap
        test_heightmap = np.random.rand(64, 64) * 100
        eroded_heightmap = erosion_sys.erode_terrain(test_heightmap, num_iterations=1000)
        print(f"✅ Érosion appliquée: différence moyenne={np.mean(np.abs(test_heightmap - eroded_heightmap)):.2f}m")
        
        # Test tectonic system
        print("🔍 Test 4: Système tectonique...")
        from core.tectonics import TectonicSystem
        tectonic_sys = TectonicSystem(1000, num_plates=6)
        print(f"✅ Système tectonique initialisé: {len(tectonic_sys.plates)} plaques")
        
        # Test biome system
        print("🔍 Test 5: Système de biomes...")
        from core.biomes import BiomeSystem
        biome_sys = BiomeSystem(1000, sea_level=0.0)
        print(f"✅ Système de biomes initialisé: {len(biome_sys.biome_definitions)} types")
        
        # Test geological system integration
        print("🔍 Test 6: Système géologique intégré...")
        from config import TerrainConfig
        from core.geology import GeologicalSystem
        
        config = TerrainConfig()
        geo_sys = GeologicalSystem(config, noise_gen, biome_sys)
        
        # Generate terrain data
        terrain_data = geo_sys.generate_terrain(X, Y)
        print(f"✅ Terrain généré: élévation min={np.min(terrain_data):.1f}m, max={np.max(terrain_data):.1f}m")
        
        print("\n🎉 TOUS LES TESTS DE BASE RÉUSSIS!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_parameter_application():
    """Test parameter application to systems."""
    print("\n🧪 TEST: Application des paramètres utilisateur")
    print("=" * 60)
    
    try:
        from config import TerrainConfig
        from generators.terrain_generator import TerrainGenerator
        
        config = TerrainConfig()
        terrain_gen = TerrainGenerator(config)
        
        # Test parameter application
        test_params = {
            'erosion_strength': 0.8,
            'erosion_iterations': 100000,
            'mountain_height_scale': 2.0,
            'mountain_count': 6,
            'tectonic_strength': 1.5,
            'num_tectonic_plates': 10,
            'temperature_variation': 1.2,
            'humidity_variation': 1.3
        }
        
        print("🔍 Application des paramètres...")
        terrain_gen.apply_user_parameters(test_params)
        print("✅ Paramètres appliqués avec succès")
        
        # Verify parameters were applied
        if hasattr(terrain_gen.geological_system, 'erosion'):
            erosion_speed = terrain_gen.geological_system.erosion.erosion_speed
            print(f"✅ Érosion: force={erosion_speed}")
        
        if hasattr(terrain_gen.geological_system, 'mountains'):
            height_scale = terrain_gen.geological_system.mountains.height_scale
            print(f"✅ Montagnes: échelle={height_scale}")
        
        print("\n🎉 TEST PARAMÈTRES RÉUSSI!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR PARAMÈTRES: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 TESTS SIMPLIFIÉS DU GÉNÉRATEUR DE TERRAIN")
    print("=" * 80)
    
    # Test core systems
    core_success = test_core_systems()
    
    # Test parameter application
    param_success = test_parameter_application()
    
    print("\n🏁 RÉSULTATS FINAUX")
    print("=" * 80)
    print(f"📊 Tests de base: {'✅ Réussis' if core_success else '❌ Échoués'}")
    print(f"📊 Tests paramètres: {'✅ Réussis' if param_success else '❌ Échoués'}")
    
    if core_success and param_success:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("Le générateur de terrain fonctionne correctement.")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus.")
