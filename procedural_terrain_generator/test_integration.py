"""
Script de test pour vérifier l'intégration complète des nouveaux systèmes.
Teste les systèmes tectoniques, d'érosion, de biomes et LOD ensemble.
"""

import numpy as np
import sys
import os

# Ajouter le chemin du module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.noise import OptimizedNoise
from core.tectonics import TectonicSystem
from core.erosion import HydraulicErosion
from core.biomes import BiomeSystem
from core.lod import AdaptiveLOD, LODLevel
from config.settings import TerrainConfig


def test_noise_system():
    """Test du système de bruit optimisé."""
    print("=== Test du système de bruit ===")
    
    try:
        noise = OptimizedNoise(seed=12345)
        
        # Test génération 2D
        x = np.linspace(0, 1, 100)
        y = np.linspace(0, 1, 100)
        X, Y = np.meshgrid(x, y)
        
        noise_2d = noise.generate_2d(X, Y)
        print(f"✓ Génération 2D: {noise_2d.shape}, min={noise_2d.min():.3f}, max={noise_2d.max():.3f}")
        
        # Test FBM
        fbm = noise.fbm(X, Y, octaves=6, persistence=0.5, lacunarity=2.0)
        print(f"✓ FBM: {fbm.shape}, min={fbm.min():.3f}, max={fbm.max():.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur système de bruit: {e}")
        return False


def test_tectonic_system():
    """Test du système tectonique."""
    print("\n=== Test du système tectonique ===")
    
    try:
        tectonics = TectonicSystem(world_size=1000, num_plates=6)
        
        # Test génération des plaques
        print(f"✓ Nombre de plaques: {len(tectonics.plates)}")
        
        # Test calcul d'influence tectonique
        x = np.linspace(0, 1, 50)
        y = np.linspace(0, 1, 50)
        X, Y = np.meshgrid(x, y)
        
        influence = tectonics.calculate_tectonic_influence(X, Y)
        print(f"✓ Influence tectonique: {influence.shape}, min={influence.min():.3f}, max={influence.max():.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur système tectonique: {e}")
        return False


def test_erosion_system():
    """Test du système d'érosion hydraulique."""
    print("\n=== Test du système d'érosion ===")
    
    try:
        erosion = HydraulicErosion(
            evaporation_rate=0.01,
            erosion_speed=0.3,
            erosion_radius=3
        )
        
        # Créer un heightmap de test
        heightmap = np.random.random((100, 100)) * 100
        
        # Test d'érosion (version réduite pour le test)
        eroded = erosion.erode_terrain(heightmap, num_iterations=1000)
        print(f"✓ Érosion appliquée: {eroded.shape}, différence moyenne={np.mean(np.abs(eroded - heightmap)):.3f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur système d'érosion: {e}")
        return False


def test_biome_system():
    """Test du système de biomes."""
    print("\n=== Test du système de biomes ===")
    
    try:
        biomes = BiomeSystem(world_size=1000, sea_level=0.0)
        
        # Test calcul du climat
        x = np.linspace(0, 1, 50)
        y = np.linspace(0, 1, 50)
        elevation = np.random.random((50, 50)) * 1000
        X, Y = np.meshgrid(x, y)
        
        climate = biomes.calculate_climate(X, Y, elevation)
        print(f"✓ Climat calculé: température {climate['temperature'].min():.1f}°C à {climate['temperature'].max():.1f}°C")
        print(f"✓ Humidité: {climate['humidity'].min():.2f} à {climate['humidity'].max():.2f}")
        
        # Test détermination des biomes
        biome_data = biomes.determine_biomes(X, Y, elevation)
        unique_biomes = np.unique(biome_data['biome_map'])
        print(f"✓ Biomes détectés: {len(unique_biomes)} types différents")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur système de biomes: {e}")
        return False


def test_lod_system():
    """Test du système LOD."""
    print("\n=== Test du système LOD ===")
    
    try:
        lod = AdaptiveLOD(world_size=10000, chunk_size=1000)
        
        # Test mise à jour position caméra
        camera_pos = np.array([5000.0, 5000.0, 100.0])
        lod.update_camera_position(camera_pos)
        print(f"✓ Position caméra mise à jour: {lod.camera_position}")
        
        # Test détermination des chunks requis
        required_chunks = lod.get_required_chunks(view_distance=3000.0)
        print(f"✓ Chunks requis: {len(required_chunks)} chunks")
        
        # Test création de chunk
        chunk = lod.create_chunk(5, 5, LODLevel.HIGH)
        print(f"✓ Chunk créé: LOD {chunk.lod_level.name}, résolution {chunk.resolution}")
        
        # Test statistiques
        stats = lod.get_performance_stats()
        print(f"✓ Statistiques: {stats['total_chunks']} chunks, {stats['memory_usage_mb']:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur système LOD: {e}")
        return False


def test_integrated_generation():
    """Test de génération intégrée avec tous les systèmes."""
    print("\n=== Test de génération intégrée ===")
    
    try:
        # Initialiser tous les systèmes
        config = TerrainConfig()
        noise = OptimizedNoise(seed=config.MASTER_SEED)
        tectonics = TectonicSystem(world_size=config.WORLD_SIZE, num_plates=8)
        erosion = HydraulicErosion()
        biomes = BiomeSystem(world_size=config.WORLD_SIZE)
        lod = AdaptiveLOD(world_size=config.WORLD_SIZE)
        
        print("✓ Tous les systèmes initialisés")
        
        # Générer un petit terrain de test
        size = 64
        x = np.linspace(0, 1, size)
        y = np.linspace(0, 1, size)
        X, Y = np.meshgrid(x, y)
        
        # 1. Génération du bruit de base
        base_elevation = noise.fbm(X, Y, octaves=6, persistence=0.6, lacunarity=2.0) * 500
        print(f"✓ Élévation de base générée: {base_elevation.min():.1f}m à {base_elevation.max():.1f}m")
        
        # 2. Influence tectonique
        tectonic_influence = tectonics.calculate_tectonic_influence(X, Y)
        combined_elevation = base_elevation + tectonic_influence * 200
        print(f"✓ Influence tectonique ajoutée: {combined_elevation.min():.1f}m à {combined_elevation.max():.1f}m")
        
        # 3. Érosion (version légère pour le test)
        eroded_elevation = erosion.erode_terrain(combined_elevation, num_iterations=500)
        print(f"✓ Érosion appliquée: différence moyenne {np.mean(np.abs(eroded_elevation - combined_elevation)):.2f}m")
        
        # 4. Détermination des biomes
        biome_data = biomes.determine_biomes(X, Y, eroded_elevation)
        unique_biomes = np.unique(biome_data['biome_map'])
        print(f"✓ Biomes déterminés: {len(unique_biomes)} types")
        
        # 5. Test LOD
        lod.update_camera_position(np.array([500.0, 500.0, 50.0]))
        chunk = lod.create_chunk(0, 0, LODLevel.HIGH)
        print(f"✓ Chunk LOD créé: résolution {chunk.resolution}")
        
        print("\n🎉 Génération intégrée réussie!")
        return True
        
    except Exception as e:
        print(f"✗ Erreur génération intégrée: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Fonction principale de test."""
    print("🧪 Test d'intégration des systèmes de terrain procédural")
    print("=" * 60)
    
    tests = [
        ("Système de bruit", test_noise_system),
        ("Système tectonique", test_tectonic_system),
        ("Système d'érosion", test_erosion_system),
        ("Système de biomes", test_biome_system),
        ("Système LOD", test_lod_system),
        ("Génération intégrée", test_integrated_generation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nRésultat global: {passed}/{len(tests)} tests réussis")
    
    if passed == len(tests):
        print("🎉 Tous les systèmes fonctionnent correctement!")
        print("Le terrain procédural est prêt pour l'intégration Blender.")
    else:
        print("⚠️  Certains systèmes nécessitent des corrections.")
    
    return passed == len(tests)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
