# 🌍 Générateur de Terrain Procédural

Architecture modulaire pour génération de terrain procédural ultra-réaliste avec Blender 5.0 et export Godot 4.4.

## 🚀 Fonctionnalités

- **🏔️ Génération géologique réaliste** - Tectonique, montagnes, rivières, bassins
- **⚡ Traitement parallèle optimisé** - Multi-threading avec gestion intelligente des tâches
- **🔍 Système LOD adaptatif** - Optimisation automatique selon la distance
- **💾 Cache intelligent** - Réutilisation des données générées
- **🎮 Export Godot natif** - Pipeline optimisé pour Godot 4.4
- **🏗️ Intégration Blender** - Meshes, matériaux et optimisations automatiques
- **🌊 Streaming dynamique** - Support mondes ouverts infinis

## 📁 Structure du Projet

```
procedural_terrain_generator/
├── config/              # Configuration centralisée
│   ├── __init__.py
│   └── settings.py      # TerrainConfig, PerformanceProfile
├── core/                # Systèmes de base
│   ├── __init__.py
│   ├── noise.py         # Génération de bruit optimisée
│   ├── geology.py       # Systèmes géologiques
│   └── math_utils.py    # Utilitaires mathématiques
├── blender/             # Intégration Blender
│   ├── __init__.py
│   ├── mesh_creator.py  # Création de meshes
│   ├── materials.py     # Système de matériaux
│   └── scene_optimizer.py # Optimisations scène
├── export/              # Export vers moteurs externes
│   ├── __init__.py
│   ├── godot_exporter.py    # Export Godot
│   ├── heightmap_exporter.py # Export heightmaps
│   └── metadata_exporter.py  # Export métadonnées
├── runtime/             # Systèmes runtime
│   ├── __init__.py
│   ├── lod_system.py    # Système LOD
│   ├── streaming.py     # Streaming terrain
│   ├── cache_manager.py # Gestion cache
│   └── memory_manager.py # Gestion mémoire
├── generators/          # Générateurs principaux
│   ├── __init__.py
│   ├── terrain_generator.py # Générateur terrain
│   └── parallel_processor.py # Traitement parallèle
├── main.py              # Point d'entrée principal
├── requirements.txt     # Dépendances
└── README.md           # Ce fichier
```

## 🛠️ Installation

### Pour Blender

```bash
# Dans Blender, ouvrir la console Python et exécuter:
import subprocess
import sys

# Installer les dépendances
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
```

### Pour développement standalone

```bash
pip install -r requirements.txt
```

## 🎯 Utilisation Rapide

### Génération Preview (3x3 tuiles)

```python
from procedural_terrain_generator import quick_preview

# Génération rapide d'un preview
results = quick_preview(radius=1, world_size=2000)
print(f"Généré {results['tile_count']} tuiles en {results['generation_time']:.2f}s")
```

### Génération Complète

```python
from procedural_terrain_generator import WorldGenerator, TerrainConfig

# Configuration personnalisée
config = TerrainConfig()
config.WORLD_SIZE = 8000  # 8km x 8km
config.MASTER_SEED = 12345
config.USE_CACHE = True

# Génération
generator = WorldGenerator(config)
results = generator.generate_complete_world()
```

### Utilisation Modulaire

```python
from procedural_terrain_generator.core import OptimizedNoise, GeologicalSystem
from procedural_terrain_generator.config import TerrainConfig

# Configuration
config = TerrainConfig()

# Générateur de bruit
noise_gen = OptimizedNoise(config.MASTER_SEED)

# Système géologique
geo_system = GeologicalSystem(config, noise_gen)
geo_system.precompute_geological_features()

# Génération d'une tuile
tile_data = geo_system.generate_tile_geology(0, 0, 64)
```

## 🎮 Export Godot

Le système génère automatiquement:

```
terrain_export/
├── godot_project/
│   ├── terrain_tiles/     # Meshes .obj/.gltf
│   ├── heightmaps/        # Heightmaps .png
│   ├── materials/         # Textures PBR
│   └── scripts/           # Scripts Godot
├── metadata/
│   ├── tile_info.json     # Informations tuiles
│   ├── world_config.json  # Configuration monde
│   └── performance_report.json # Rapport performance
└── README_Godot.md        # Guide d'intégration
```

### Intégration dans Godot

1. **Importer le projet** : Copier `godot_project/` dans votre projet Godot
2. **Configurer le streaming** : Utiliser `TerrainStreamer.gd`
3. **Ajuster les matériaux** : Personnaliser les matériaux PBR
4. **Optimiser les LOD** : Configurer les distances LOD

## ⚙️ Configuration

### Profils de Performance

```python
from procedural_terrain_generator import create_optimized_config

# Configuration bas de gamme
config_low = create_optimized_config("low_end")

# Configuration équilibrée (défaut)
config_balanced = create_optimized_config("balanced")

# Configuration haute performance
config_high = create_optimized_config("high_end")
```

### Paramètres Principaux

```python
config = TerrainConfig()

# Monde
config.WORLD_SIZE = 10000        # Taille en mètres
config.TILE_SIZE = 500           # Taille tuile en mètres
config.MASTER_SEED = 42          # Seed génération

# Performance
config.MAX_WORKERS = 8           # Threads parallèles
config.USE_CACHE = True          # Cache activé
config.MEMORY_LIMIT_MB = 4096    # Limite mémoire

# Qualité
config.HIGH_DETAIL_SUBDIVISIONS = 128  # Subdivisions haute qualité
config.MEDIUM_DETAIL_SUBDIVISIONS = 64 # Subdivisions moyennes
config.LOW_DETAIL_SUBDIVISIONS = 32    # Subdivisions basses
```

## 🔧 Développement

### Exécution des Tests

```bash
# Depuis le répertoire du projet
python main.py
```

### Tests de Performance

```python
from procedural_terrain_generator.main import run_performance_test

# Test automatisé
results = run_performance_test()
print(f"Performance: {results['preview_3x3']['tiles_per_second']:.1f} tuiles/sec")
```

### Ajout de Nouveaux Modules

1. Créer le module dans le répertoire approprié
2. Ajouter les imports dans `__init__.py`
3. Documenter les nouvelles fonctionnalités
4. Ajouter des tests si nécessaire

## 📊 Performance

### Benchmarks Typiques

- **Preview 3x3** : ~5-15 tuiles/sec (selon hardware)
- **Génération complète** : 100+ tuiles/sec avec cache
- **Mémoire** : ~2-4GB pour monde 10km x 10km
- **Export Godot** : ~30s pour 100 tuiles

### Optimisations

- **Cache intelligent** : Réutilisation des calculs coûteux
- **Traitement parallèle** : Utilisation optimale des CPU multi-cœurs
- **LOD adaptatif** : Génération selon la distance de vue
- **Streaming** : Chargement/déchargement dynamique

## 🐛 Dépannage

### Problèmes Courants

**Erreur d'import bpy** : Vérifier que le script s'exécute dans Blender

**Mémoire insuffisante** : Réduire `WORLD_SIZE` ou `MAX_WORKERS`

**Performance lente** : Activer le cache avec `USE_CACHE = True`

**Export Godot échoue** : Vérifier les permissions d'écriture

### Logs et Debug

```python
# Activer les logs détaillés
config.DEBUG_MODE = True
config.VERBOSE_LOGGING = True
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Remerciements

- **Blender Foundation** pour l'API Python
- **Godot Engine** pour le moteur de jeu open source
- **NumPy/SciPy** pour les calculs scientifiques optimisés

---

**🌟 Bon développement de mondes procéduraux !**
