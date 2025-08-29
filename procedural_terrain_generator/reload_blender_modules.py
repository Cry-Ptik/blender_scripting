"""
Script de rechargement forcé des modules pour Blender
À exécuter dans la console Blender pour forcer le rechargement complet
"""

import bpy
import sys
import importlib

def force_reload_terrain_modules():
    """Force le rechargement de tous les modules du terrain generator"""
    
    print("=== RECHARGEMENT FORCÉ DES MODULES ===")
    
    # Liste des modules à recharger
    modules_to_reload = [
        'procedural_terrain_generator',
        'procedural_terrain_generator.core',
        'procedural_terrain_generator.core.noise',
        'procedural_terrain_generator.core.geology',
        'procedural_terrain_generator.blender',
        'procedural_terrain_generator.blender.mesh_creator',
        'procedural_terrain_generator.runtime',
        'procedural_terrain_generator.runtime.cache_manager'
    ]
    
    # Désactiver le plugin
    try:
        bpy.ops.preferences.addon_disable(module='procedural_terrain_generator')
        print("✅ Plugin désactivé")
    except:
        print("⚠️ Plugin déjà désactivé")
    
    # Supprimer tous les modules du cache
    modules_removed = []
    for module_name in list(sys.modules.keys()):
        if 'procedural_terrain_generator' in module_name:
            del sys.modules[module_name]
            modules_removed.append(module_name)
    
    print(f"🗑️ {len(modules_removed)} modules supprimés du cache")
    for mod in modules_removed:
        print(f"   - {mod}")
    
    # Réactiver le plugin
    try:
        bpy.ops.preferences.addon_enable(module='procedural_terrain_generator')
        print("✅ Plugin réactivé")
        
        # Test d'instanciation
        from procedural_terrain_generator.core.noise import OptimizedNoise
        noise = OptimizedNoise(seed=42)
        print("✅ OptimizedNoise instanciée avec succès!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la réactivation: {e}")
        return False

# Exécuter automatiquement si dans Blender
if __name__ == "__main__" and 'bpy' in globals():
    force_reload_terrain_modules()
