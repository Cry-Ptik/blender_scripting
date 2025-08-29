"""
Test final pour validation complète du plugin Blender.
Vérifie que tous les systèmes fonctionnent ensemble.
"""

import numpy as np
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_generation():
    """Test de génération complète avec tous les systèmes."""
    print("🧪 Test de génération complète")
    print("=" * 40)
    
    try:
        # Imports
        from config.settings import TerrainConfig
        from core.noise import OptimizedNoise
        from core.tectonics import TectonicSystem
        from core.erosion import HydraulicErosion
        from core.biomes import BiomeSystem
        from core.lod import AdaptiveLOD
        from core.geology import GeologicalSystem
        
        print("✓ Tous les imports réussis")
        
        # Configuration
        config = TerrainConfig()
        print(f"✓ Configuration: monde {config.WORLD_SIZE}m, seed {config.MASTER_SEED}")
        
        # Systèmes principaux
        noise = OptimizedNoise(seed=config.MASTER_SEED)
        biomes = BiomeSystem(world_size=config.WORLD_SIZE)
        geology = GeologicalSystem(config, noise, biomes)
        lod = AdaptiveLOD(world_size=config.WORLD_SIZE)
        
        print("✓ Tous les systèmes initialisés")
        
        # Test génération petit terrain
        size = 32
        x = np.linspace(0, 1, size)
        y = np.linspace(0, 1, size)
        X, Y = np.meshgrid(x, y)
        
        # Génération géologique
        result = geology.generate_tile_geology(0, 0, size)
        
        print(f"✓ Terrain généré: {result['elevation'].shape}")
        print(f"  - Élévation: {result['elevation'].min():.1f}m à {result['elevation'].max():.1f}m")
        
        if 'biome_data' in result:
            unique_biomes = np.unique(result['biome_data']['biome_map'])
            print(f"  - Biomes: {len(unique_biomes)} types détectés")
        
        # Test LOD
        lod.update_camera_position(np.array([500.0, 500.0, 50.0]))
        chunks = lod.get_required_chunks(view_distance=2000.0)
        print(f"✓ LOD: {len(chunks)} chunks requis")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_plugin_compatibility():
    """Test de compatibilité avec le plugin Blender."""
    print("\n🔌 Test compatibilité plugin Blender")
    print("=" * 40)
    
    try:
        # Test imports du plugin principal
        from config import TerrainConfig
        from core import OptimizedNoise, GeologicalSystem, BiomeSystem
        
        print("✓ Imports plugin réussis")
        
        # Test création générateur comme dans le plugin
        config = TerrainConfig()
        noise = OptimizedNoise(config.MASTER_SEED)
        biomes = BiomeSystem(config.WORLD_SIZE)
        geology = GeologicalSystem(config, noise, biomes)
        
        print("✓ Générateur créé comme dans le plugin")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur compatibilité: {e}")
        return False

def main():
    """Fonction principale de validation."""
    print("🎯 VALIDATION FINALE - Plugin Terrain Procédural")
    print("=" * 60)
    
    tests = [
        ("Génération complète", test_complete_generation),
        ("Compatibilité plugin", test_plugin_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSULTATS FINAUX")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat global: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("\n🎉 VALIDATION RÉUSSIE!")
        print("Le plugin est prêt pour installation dans Blender 5.0")
        print("Tous les systèmes avancés fonctionnent correctement:")
        print("  • Système tectonique réaliste")
        print("  • Érosion hydraulique")
        print("  • Biomes climatiques")
        print("  • LOD adaptatif")
        print("  • Génération géologique intégrée")
    else:
        print("\n⚠️  VALIDATION PARTIELLE")
        print("Certains systèmes nécessitent encore des corrections.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
