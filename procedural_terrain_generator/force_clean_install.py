"""
Script pour forcer une installation propre du plugin dans Blender
"""

import bpy
import sys
import os
import shutil

def force_clean_install():
    """Force une installation complètement propre"""
    
    print("=== NETTOYAGE COMPLET ===")
    
    # 1. Désactiver le plugin
    try:
        bpy.ops.preferences.addon_disable(module='procedural_terrain_generator')
        print("✅ Plugin désactivé")
    except:
        print("⚠️ Plugin déjà désactivé")
    
    # 2. Supprimer TOUS les modules du cache Python
    modules_to_remove = []
    for module_name in list(sys.modules.keys()):
        if 'procedural_terrain_generator' in module_name or 'noise' in module_name:
            modules_to_remove.append(module_name)
    
    for module_name in modules_to_remove:
        if module_name in sys.modules:
            del sys.modules[module_name]
    
    print(f"🗑️ {len(modules_to_remove)} modules supprimés du cache")
    
    # 3. Supprimer le dossier physique du plugin
    addon_path = bpy.utils.user_resource('SCRIPTS', path="addons")
    plugin_path = os.path.join(addon_path, "procedural_terrain_generator")
    
    if os.path.exists(plugin_path):
        try:
            shutil.rmtree(plugin_path)
            print(f"🗑️ Dossier supprimé: {plugin_path}")
        except Exception as e:
            print(f"⚠️ Impossible de supprimer le dossier: {e}")
    
    # 4. Forcer le garbage collector
    import gc
    gc.collect()
    
    print("✅ Nettoyage terminé")
    print("📋 ÉTAPES SUIVANTES:")
    print("1. Fermer Blender complètement")
    print("2. Recréer l'archive ZIP avec les nouveaux fichiers")
    print("3. Relancer Blender")
    print("4. Installer le plugin depuis l'archive")
    
    return True

# Exécuter
if __name__ == "__main__":
    force_clean_install()
