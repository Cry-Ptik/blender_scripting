"""
Script de test simple pour vérifier les imports du plugin Blender.
Teste les imports sans exécuter de génération complète.
"""

import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test des imports de base."""
    print("=== Test des imports de base ===")
    
    try:
        import numpy as np
        print(f"✓ NumPy: {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy manquant: {e}")
        return False
    
    return True

def test_core_imports():
    """Test des imports du module core."""
    print("\n=== Test des imports core ===")
    
    try:
        from core.noise import OptimizedNoise, NoiseGenerator
        print("✓ Noise modules importés")
        
        from core.tectonics import TectonicSystem, TectonicPlate
        print("✓ Tectonics modules importés")
        
        from core.erosion import HydraulicErosion, WaterDroplet
        print("✓ Erosion modules importés")
        
        from core.biomes import BiomeSystem, BiomeType, BiomeProperties
        print("✓ Biomes modules importés")
        
        from core.lod import AdaptiveLOD, LODLevel, LODChunk
        print("✓ LOD modules importés")
        
        from core.geology import GeologicalSystem
        print("✓ Geology module importé")
        
        return True
        
    except ImportError as e:
        print(f"✗ Erreur import core: {e}")
        return False

def test_config_imports():
    """Test des imports de configuration."""
    print("\n=== Test des imports config ===")
    
    try:
        from config.settings import TerrainConfig
        print("✓ TerrainConfig importé")
        return True
        
    except ImportError as e:
        print(f"✗ Erreur import config: {e}")
        return False

def test_plugin_imports():
    """Test des imports du plugin principal."""
    print("\n=== Test des imports plugin ===")
    
    try:
        # Test import du plugin sans Blender
        import importlib.util
        
        # Charger le module sans l'exécuter
        spec = importlib.util.spec_from_file_location(
            "procedural_terrain_generator", 
            "__init__.py"
        )
        
        if spec is None:
            print("✗ Impossible de charger le spec du plugin")
            return False
            
        print("✓ Plugin spec chargé")
        
        # Tester les imports individuels du plugin
        from config import TerrainConfig
        print("✓ Config importé dans plugin")
        
        from core import OptimizedNoise, NoiseGenerator, GeologicalSystem
        print("✓ Core modules importés dans plugin")
        
        return True
        
    except ImportError as e:
        print(f"✗ Erreur import plugin: {e}")
        return False

def test_simple_instantiation():
    """Test d'instanciation simple des classes principales."""
    print("\n=== Test d'instanciation ===")
    
    try:
        from config.settings import TerrainConfig
        from core.noise import OptimizedNoise
        from core.biomes import BiomeSystem
        
        # Test config
        config = TerrainConfig()
        print(f"✓ TerrainConfig créé: world_size={config.WORLD_SIZE}")
        
        # Test noise
        noise = OptimizedNoise(seed=12345)
        print("✓ OptimizedNoise créé")
        
        # Test biomes
        biomes = BiomeSystem(world_size=1000)
        print("✓ BiomeSystem créé")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur instanciation: {e}")
        return False

def main():
    """Fonction principale de test."""
    print("🔍 Test des imports du plugin Terrain Procédural")
    print("=" * 50)
    
    tests = [
        ("Imports de base", test_basic_imports),
        ("Imports core", test_core_imports),
        ("Imports config", test_config_imports),
        ("Imports plugin", test_plugin_imports),
        ("Instanciation simple", test_simple_instantiation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS D'IMPORTS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ OK" if result else "❌ ÉCHEC"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("🎉 Tous les imports fonctionnent!")
        print("Le plugin peut être installé dans Blender.")
    else:
        print("⚠️  Certains imports échouent.")
        print("Vérifiez les dépendances et la structure des modules.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
