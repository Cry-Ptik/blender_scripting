"""
Test script for terrain generation with user parameters.
Tests the complete pipeline including UI parameters and regeneration stability.
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock Blender context for testing outside Blender
class MockContext:
    def __init__(self):
        self.selected_objects = []
        self.scene = MockScene()

class MockScene:
    def __init__(self):
        self.objects = []

# Set up mock bpy for testing
class MockBpy:
    def __init__(self):
        self.context = MockContext()
        self.data = MockData()
        self.ops = MockOps()

class MockData:
    def __init__(self):
        pass
    
    def meshes(self):
        return MockMeshes()
    
    def materials(self):
        return MockMaterials()

class MockMeshes:
    def new(self, name):
        return MockMesh(name)

class MockMaterials:
    def new(self, name):
        return MockMaterial(name)

class MockMesh:
    def __init__(self, name):
        self.name = name

class MockMaterial:
    def __init__(self, name):
        self.name = name

class MockOps:
    def __init__(self):
        pass

# Install mock bpy
sys.modules['bpy'] = MockBpy()

from config import TerrainConfig
from generators.terrain_generator import WorldGenerator

def test_terrain_generation_with_parameters():
    """Test terrain generation with various user parameters."""
    print("🧪 TEST: Génération de terrain avec paramètres utilisateur")
    print("=" * 60)
    
    # Create configuration
    config = TerrainConfig()
    config.MASTER_SEED = 12345
    config.WORLD_SIZE = 1000
    config.TILE_SIZE = 256
    
    # Create world generator
    generator = WorldGenerator(config)
    
    # Test different parameter sets
    test_cases = [
        {
            'name': 'Paramètres par défaut',
            'params': {}
        },
        {
            'name': 'Érosion forte',
            'params': {
                'erosion_strength': 0.8,
                'erosion_iterations': 100000
            }
        },
        {
            'name': 'Montagnes hautes',
            'params': {
                'mountain_height_scale': 2.5,
                'mountain_count': 8
            }
        },
        {
            'name': 'Tectonique intense',
            'params': {
                'tectonic_strength': 1.8,
                'num_tectonic_plates': 12
            }
        },
        {
            'name': 'Biomes variés',
            'params': {
                'temperature_variation': 1.5,
                'humidity_variation': 1.8
            }
        }
    ]
    
    results = {}
    
    for i, test_case in enumerate(test_cases):
        print(f"\n🔬 Test {i+1}: {test_case['name']}")
        print("-" * 40)
        
        try:
            # Apply parameters
            if test_case['params']:
                generator.apply_user_parameters(test_case['params'])
                print(f"✅ Paramètres appliqués: {test_case['params']}")
            
            # Generate terrain
            result = generator.generate_preview_area(0, 0, 1)
            
            if result['status'] == 'success':
                print(f"✅ Génération réussie: {result['tiles_generated']} tuiles")
                
                # Analyze elevation data
                if result['results'] and len(result['results']) > 0:
                    tile_data = result['results'][0]
                    if 'elevation' in tile_data:
                        elevation = tile_data['elevation']
                        min_elev = np.min(elevation)
                        max_elev = np.max(elevation)
                        mean_elev = np.mean(elevation)
                        std_elev = np.std(elevation)
                        
                        print(f"📊 Élévation - Min: {min_elev:.1f}m, Max: {max_elev:.1f}m")
                        print(f"📊 Moyenne: {mean_elev:.1f}m, Écart-type: {std_elev:.1f}m")
                        
                        results[test_case['name']] = {
                            'success': True,
                            'min_elevation': min_elev,
                            'max_elevation': max_elev,
                            'mean_elevation': mean_elev,
                            'std_elevation': std_elev
                        }
                    else:
                        print("⚠️ Pas de données d'élévation")
                        results[test_case['name']] = {'success': False, 'error': 'No elevation data'}
                else:
                    print("⚠️ Pas de résultats de tuiles")
                    results[test_case['name']] = {'success': False, 'error': 'No tile results'}
            else:
                print(f"❌ Échec génération: {result.get('error', 'Unknown error')}")
                results[test_case['name']] = {'success': False, 'error': result.get('error', 'Unknown error')}
                
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            results[test_case['name']] = {'success': False, 'error': str(e)}
    
    # Print summary
    print("\n📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    successful_tests = 0
    for test_name, result in results.items():
        if result['success']:
            successful_tests += 1
            print(f"✅ {test_name}")
            if 'max_elevation' in result:
                print(f"   Relief max: {result['max_elevation']:.1f}m")
        else:
            print(f"❌ {test_name}: {result['error']}")
    
    print(f"\n🎯 Tests réussis: {successful_tests}/{len(test_cases)}")
    
    return results

def test_regeneration_stability():
    """Test terrain regeneration stability."""
    print("\n🔄 TEST: Stabilité de la régénération")
    print("=" * 60)
    
    config = TerrainConfig()
    config.MASTER_SEED = 54321
    
    generator = WorldGenerator(config)
    
    # Generate same terrain multiple times
    results = []
    for i in range(3):
        print(f"\n🔄 Génération {i+1}/3")
        
        try:
            result = generator.generate_preview_area(0, 0, 1)
            
            if result['status'] == 'success' and result['results']:
                tile_data = result['results'][0]
                if 'elevation' in tile_data:
                    elevation = tile_data['elevation']
                    results.append(elevation.copy())
                    print(f"✅ Génération {i+1} réussie")
                else:
                    print(f"⚠️ Génération {i+1}: pas de données d'élévation")
            else:
                print(f"❌ Génération {i+1} échouée: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"❌ Erreur génération {i+1}: {str(e)}")
    
    # Compare results
    if len(results) >= 2:
        print(f"\n🔍 Comparaison des générations:")
        
        # Compare first two results
        diff = np.abs(results[0] - results[1])
        max_diff = np.max(diff)
        mean_diff = np.mean(diff)
        
        print(f"📊 Différence max: {max_diff:.6f}m")
        print(f"📊 Différence moyenne: {mean_diff:.6f}m")
        
        if max_diff < 0.001:  # Less than 1mm difference
            print("✅ Régénération stable (différences < 1mm)")
            return True
        else:
            print("⚠️ Régénération instable (différences significatives)")
            return False
    else:
        print("❌ Pas assez de générations réussies pour comparer")
        return False

if __name__ == "__main__":
    print("🚀 TESTS DU GÉNÉRATEUR DE TERRAIN PROCÉDURAL")
    print("=" * 80)
    
    # Test parameter application
    param_results = test_terrain_generation_with_parameters()
    
    # Test regeneration stability
    stability_result = test_regeneration_stability()
    
    print("\n🏁 TESTS TERMINÉS")
    print("=" * 80)
    
    # Final summary
    successful_param_tests = sum(1 for r in param_results.values() if r['success'])
    total_param_tests = len(param_results)
    
    print(f"📊 Tests de paramètres: {successful_param_tests}/{total_param_tests}")
    print(f"📊 Stabilité régénération: {'✅ Stable' if stability_result else '❌ Instable'}")
    
    if successful_param_tests == total_param_tests and stability_result:
        print("\n🎉 TOUS LES TESTS RÉUSSIS!")
        print("Le générateur de terrain est prêt pour utilisation.")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("Vérifiez les erreurs ci-dessus.")
