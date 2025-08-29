"""
Test script pour diagnostiquer le problème de classe abstraite OptimizedNoise
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from core.noise import OptimizedNoise, NoiseGenerator
import numpy as np

def test_optimized_noise():
    """Test si OptimizedNoise peut être instanciée"""
    print("=== Test OptimizedNoise ===")
    
    # Vérifier les méthodes de la classe
    print("Méthodes de OptimizedNoise:")
    for method in dir(OptimizedNoise):
        if not method.startswith('_'):
            print(f"  - {method}")
    
    # Vérifier les méthodes abstraites
    print("\nMéthodes abstraites requises:")
    if hasattr(NoiseGenerator, '__abstractmethods__'):
        for method in NoiseGenerator.__abstractmethods__:
            print(f"  - {method}")
            if hasattr(OptimizedNoise, method):
                print(f"    ✅ Implémentée dans OptimizedNoise")
            else:
                print(f"    ❌ MANQUANTE dans OptimizedNoise")
    
    # Tenter l'instanciation
    try:
        noise = OptimizedNoise(seed=42)
        print("\n✅ OptimizedNoise instanciée avec succès!")
        
        # Test de génération
        x = np.linspace(0, 10, 50)
        y = np.linspace(0, 10, 50)
        X, Y = np.meshgrid(x, y)
        
        result = noise.generate_2d(X, Y)
        print(f"✅ generate_2d fonctionne! Shape: {result.shape}")
        print(f"   Min: {result.min():.3f}, Max: {result.max():.3f}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'instanciation: {e}")
        return False

if __name__ == "__main__":
    test_optimized_noise()
