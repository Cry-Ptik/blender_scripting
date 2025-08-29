"""
Procedural Terrain Generator - Plugin Blender
Générateur de terrain procédural ultra-réaliste pour Blender 5.0+
"""

bl_info = {
    "name": "Procedural Terrain Generator",
    "author": "Procedural Terrain Generator Team",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Terrain",
    "description": "Générateur de terrain procédural ultra-réaliste avec export Godot",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from bpy.props import (
    IntProperty,
    FloatProperty,
    BoolProperty,
    EnumProperty,
    StringProperty
)
from bpy.types import (
    Panel,
    Operator,
    PropertyGroup
)

# Import des modules du générateur
from .config import TerrainConfig, PerformanceProfile
from .generators import WorldGenerator, TerrainGenerator
from .core import (
    OptimizedNoise, NoiseGenerator, GeologicalSystem,
    TectonicSystem, HydraulicErosion, BiomeSystem, AdaptiveLOD
)
from .runtime import LODManager, TerrainStreaming, MemoryManager

# ===== PROPRIÉTÉS DU PLUGIN =====

class TerrainGeneratorProperties(PropertyGroup):
    """Propriétés du générateur de terrain pour l'interface Blender."""
    
    # Paramètres de base
    world_size: IntProperty(
        name="Taille du monde",
        description="Taille du monde en mètres",
        default=4000,
        min=1000,
        max=20000
    )
    
    tile_size: IntProperty(
        name="Taille des tuiles",
        description="Taille des tuiles en mètres",
        default=250,
        min=50,
        max=1000
    )
    
    master_seed: IntProperty(
        name="Seed principal",
        description="Seed pour la génération procédurale",
        default=12345,
        min=0,
        max=999999
    )
    
    # Niveau de détail
    detail_level: EnumProperty(
        name="Niveau de détail",
        description="Niveau de détail pour la génération",
        items=[
            ('low', 'Bas', 'Détail bas pour performance'),
            ('medium', 'Moyen', 'Équilibre performance/qualité'),
            ('high', 'Élevé', 'Haute qualité, plus lent'),
            ('ultra', 'Ultra', 'Qualité maximale')
        ],
        default='medium'
    )
    
    # Profil de performance
    performance_profile: EnumProperty(
        name="Profil de performance",
        description="Profil optimisé selon votre matériel",
        items=[
            ('low_end', 'Matériel modeste', 'Optimisé pour matériel bas de gamme'),
            ('balanced', 'Équilibré', 'Configuration équilibrée'),
            ('high_end', 'Matériel puissant', 'Optimisé pour matériel haut de gamme')
        ],
        default='balanced'
    )
    
    # Options de génération
    use_cache: BoolProperty(
        name="Utiliser Cache",
        description="Utilise le cache pour accélérer la génération",
        default=True
    )
    
    preview_mode: BoolProperty(
        name="Mode Aperçu",
        description="Génère seulement une zone d'aperçu (plus rapide)",
        default=False
    )
    
    # Paramètres Érosion
    erosion_strength: FloatProperty(
        name="Force Érosion",
        description="Intensité de l'érosion hydraulique",
        default=0.3,
        min=0.0,
        max=1.0
    )
    
    erosion_iterations: IntProperty(
        name="Itérations Érosion",
        description="Nombre d'itérations d'érosion",
        default=50000,
        min=1000,
        max=200000
    )
    
    # Paramètres Tectoniques
    tectonic_strength: FloatProperty(
        name="Force Tectonique",
        description="Intensité des effets tectoniques",
        default=1.0,
        min=0.0,
        max=2.0
    )
    
    num_tectonic_plates: IntProperty(
        name="Nombre Plaques",
        description="Nombre de plaques tectoniques",
        default=8,
        min=4,
        max=16
    )
    
    # Paramètres Montagnes
    mountain_height_scale: FloatProperty(
        name="Échelle Hauteur Montagnes",
        description="Multiplicateur pour la hauteur des montagnes",
        default=1.0,
        min=0.1,
        max=3.0
    )
    
    mountain_count: IntProperty(
        name="Nombre Chaînes Montagneuses",
        description="Nombre de chaînes de montagnes à générer",
        default=4,
        min=1,
        max=10
    )
    
    # Paramètres Biomes
    temperature_variation: FloatProperty(
        name="Variation Température",
        description="Amplitude des variations de température",
        default=1.0,
        min=0.1,
        max=2.0
    )
    
    humidity_variation: FloatProperty(
        name="Variation Humidité",
        description="Amplitude des variations d'humidité",
        default=1.0,
        min=0.1,
        max=2.0
    )
    
    # Export
    export_to_godot: BoolProperty(
        name="Export Godot",
        description="Exporter automatiquement vers Godot après génération",
        default=False
    )
    
    godot_export_path: StringProperty(
        name="Dossier export Godot",
        description="Chemin vers le dossier d'export Godot",
        default="//godot_export/",
        subtype='DIR_PATH'
    )

# ===== OPÉRATEURS =====

class TERRAIN_OT_generate(Operator):
    """Générer le terrain procédural"""
    bl_idname = "terrain.generate"
    bl_label = "Générer Terrain"
    bl_description = "Lance la génération de terrain procédural"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = context.scene.terrain_generator
        
        try:
            # Nettoyer les objets existants pour éviter le bug de régénération
            import bpy
            for obj in bpy.context.scene.objects:
                if obj.name.startswith("Terrain_"):
                    bpy.data.objects.remove(obj, do_unlink=True)
            
            # Configuration avec seed et paramètres utilisateur
            config = TerrainConfig()
            config.MASTER_SEED = props.master_seed
            config.WORLD_SIZE = props.world_size
            config.TILE_SIZE = props.tile_size
            config.DETAIL_LEVEL = props.detail_level
            
            # Créer le générateur avec paramètres personnalisés
            generator = WorldGenerator(config)
            
            # Appliquer les paramètres utilisateur aux systèmes
            generator.apply_user_parameters({
                'erosion_strength': props.erosion_strength,
                'erosion_iterations': props.erosion_iterations,
                'tectonic_strength': props.tectonic_strength,
                'num_tectonic_plates': props.num_tectonic_plates,
                'mountain_height_scale': props.mountain_height_scale,
                'mountain_count': props.mountain_count,
                'temperature_variation': props.temperature_variation,
                'humidity_variation': props.humidity_variation
            })
            
            # Générer selon le mode
            if props.preview_mode:
                results = generator.generate_preview_area(
                    config.TILES_COUNT // 2,
                    config.TILES_COUNT // 2,
                    1  # Rayon de 1 tuile = 3x3
                )
                self.report({'INFO'}, f"Preview généré: {len(results)} tuiles")
            else:
                results = generator.generate_complete_world()
                self.report({'INFO'}, f"Monde complet généré: {len(results)} tuiles")
            
            # Export Godot si demandé
            if props.export_to_godot:
                generator.export_to_godot(props.godot_export_path)
                self.report({'INFO'}, f"Export Godot vers: {props.godot_export_path}")
            
            return {'FINISHED'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Erreur génération: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'CANCELLED'}

class TERRAIN_OT_clear_cache(Operator):
    """Vider le cache du terrain"""
    bl_idname = "terrain.clear_cache"
    bl_label = "Vider Cache"
    bl_description = "Vide le cache de génération de terrain"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        try:
            from .runtime.cache_manager import CacheManager
            config = TerrainConfig()
            cache_manager = CacheManager(config)
            cache_manager.clear_all_caches()
            self.report({'INFO'}, "Cache vidé avec succès")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Erreur vidage cache: {str(e)}")
            return {'CANCELLED'}

class TERRAIN_OT_export_godot(Operator):
    """Exporter vers Godot"""
    bl_idname = "terrain.export_godot"
    bl_label = "Export Godot"
    bl_description = "Exporte le terrain vers Godot"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        props = context.scene.terrain_generator
        
        try:
            config = TerrainConfig()
            generator = WorldGenerator(config)
            generator.export_to_godot(props.godot_export_path)
            self.report({'INFO'}, f"Export Godot terminé: {props.godot_export_path}")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Erreur export: {str(e)}")
            return {'CANCELLED'}

# ===== INTERFACE UTILISATEUR =====

class TERRAIN_PT_main_panel(Panel):
    """Panneau principal du générateur de terrain"""
    bl_label = "Générateur de Terrain"
    bl_idname = "TERRAIN_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Terrain"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.terrain_generator
        
        # Paramètres de base
        box = layout.box()
        box.label(text="Paramètres de base:", icon='SETTINGS')
        box.prop(props, "world_size")
        box.prop(props, "tile_size")
        box.prop(props, "master_seed")
        
        # Qualité et performance
        box = layout.box()
        box.label(text="Qualité et Performance:", icon='PREFERENCES')
        box.prop(props, "detail_level")
        box.prop(props, "performance_profile")
        box.prop(props, "use_cache")
        box.prop(props, "preview_mode")
        
        # Paramètres Érosion
        box = layout.box()
        box.label(text="Érosion Hydraulique:", icon='MOD_FLUIDSIM')
        box.prop(props, "erosion_strength")
        box.prop(props, "erosion_iterations")
        
        # Paramètres Tectoniques
        box = layout.box()
        box.label(text="Tectonique:", icon='FORCE_FORCE')
        box.prop(props, "tectonic_strength")
        box.prop(props, "num_tectonic_plates")
        
        # Paramètres Montagnes
        box = layout.box()
        box.label(text="Montagnes:", icon='MESH_MONKEY')
        box.prop(props, "mountain_height_scale")
        box.prop(props, "mountain_count")
        
        # Paramètres Biomes
        box = layout.box()
        box.label(text="Biomes:", icon='WORLD')
        box.prop(props, "temperature_variation")
        box.prop(props, "humidity_variation")
        
        # Génération
        layout.separator()
        layout.operator("terrain.generate", text="Générer Terrain", icon='MESH_GRID')
        
        # Cache
        row = layout.row()
        row.operator("terrain.clear_cache", text="Vider Cache", icon='TRASH')

class TERRAIN_PT_export_panel(Panel):
    """Panneau d'export"""
    bl_label = "Export"
    bl_idname = "TERRAIN_PT_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Terrain"
    bl_parent_id = "TERRAIN_PT_main_panel"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.terrain_generator
        
        box = layout.box()
        box.label(text="Export Godot:", icon='EXPORT')
        box.prop(props, "export_to_godot")
        box.prop(props, "godot_export_path")
        
        if not props.export_to_godot:
            layout.operator("terrain.export_godot", text="🎮 Export Godot", icon='EXPORT')

# ===== ENREGISTREMENT =====

classes = (
    TerrainGeneratorProperties,
    TERRAIN_OT_generate,
    TERRAIN_OT_clear_cache,
    TERRAIN_OT_export_godot,
    TERRAIN_PT_main_panel,
    TERRAIN_PT_export_panel,
)

def register():
    """Enregistrer le plugin"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.terrain_generator = bpy.props.PointerProperty(
        type=TerrainGeneratorProperties
    )

def unregister():
    """Désenregistrer le plugin"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.terrain_generator

if __name__ == "__main__":
    register()
