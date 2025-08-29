"""
Script de test pour vérifier l'interface Blender du générateur de terrain.
À exécuter dans Blender pour diagnostiquer les problèmes d'interface.
"""

import bpy

def test_addon_registration():
    """Test si le plugin est correctement enregistré."""
    print("=== Test d'enregistrement du plugin ===")
    
    # Vérifier si les classes sont enregistrées
    try:
        # Test des opérateurs
        if hasattr(bpy.ops, 'terrain'):
            print("✅ Opérateurs terrain trouvés")
            if hasattr(bpy.ops.terrain, 'generate'):
                print("✅ Opérateur terrain.generate trouvé")
            else:
                print("❌ Opérateur terrain.generate MANQUANT")
        else:
            print("❌ Aucun opérateur terrain trouvé")
        
        # Test des propriétés
        if hasattr(bpy.types.Scene, 'terrain_generator'):
            print("✅ Propriétés terrain_generator trouvées")
        else:
            print("❌ Propriétés terrain_generator MANQUANTES")
        
        # Test des panneaux
        panel_found = False
        for cls_name in dir(bpy.types):
            if 'TERRAIN_PT' in cls_name:
                print(f"✅ Panneau trouvé: {cls_name}")
                panel_found = True
        
        if not panel_found:
            print("❌ Aucun panneau TERRAIN_PT trouvé")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

def test_addon_execution():
    """Test d'exécution du générateur."""
    print("\n=== Test d'exécution ===")
    
    try:
        # Essayer d'exécuter la génération
        result = bpy.ops.terrain.generate()
        print(f"✅ Génération exécutée: {result}")
    except Exception as e:
        print(f"❌ Erreur génération: {e}")

def show_addon_info():
    """Affiche les informations sur les addons chargés."""
    print("\n=== Addons actifs ===")
    
    for addon_name in bpy.context.preferences.addons.keys():
        if 'terrain' in addon_name.lower() or 'procedural' in addon_name.lower():
            print(f"✅ Addon trouvé: {addon_name}")
            addon = bpy.context.preferences.addons[addon_name]
            if hasattr(addon, 'module'):
                print(f"   Module: {addon.module}")

def create_test_ui():
    """Crée une interface de test simple."""
    print("\n=== Création interface de test ===")
    
    # Créer un panneau de test simple
    class TERRAIN_PT_test_panel(bpy.types.Panel):
        bl_label = "Test Terrain Generator"
        bl_idname = "TERRAIN_PT_test_panel"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = "Test"
        
        def draw(self, context):
            layout = self.layout
            layout.label(text="Plugin Terrain Generator")
            
            # Test si l'opérateur existe
            try:
                layout.operator("terrain.generate", text="🌍 Test Générer")
            except:
                layout.label(text="❌ Opérateur terrain.generate introuvable")
    
    # Enregistrer le panneau de test
    try:
        bpy.utils.register_class(TERRAIN_PT_test_panel)
        print("✅ Panneau de test créé dans l'onglet 'Test'")
    except Exception as e:
        print(f"❌ Erreur création panneau test: {e}")

if __name__ == "__main__":
    print("🔍 Diagnostic du plugin Terrain Generator")
    print("=" * 50)
    
    show_addon_info()
    test_addon_registration()
    test_addon_execution()
    create_test_ui()
    
    print("\n" + "=" * 50)
    print("📋 Instructions:")
    print("1. Vérifiez les messages ci-dessus")
    print("2. Si ❌ erreurs → Réinstaller le plugin")
    print("3. Si ✅ tout OK → Chercher onglet 'Test' dans sidebar")
    print("4. Redémarrer Blender si nécessaire")
