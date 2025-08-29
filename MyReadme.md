# 🌍 Procedural Terrain Generator

**Procedural Terrain Generator (PTG)** est un framework modulaire en Python pour la **génération de mondes procéduraux** réalistes.  
Il permet de créer rapidement des **terrains 3D**, des **heightmaps**, et d’exporter directement vers **Blender** et **Godot**.

🎯 Pensé pour les **indépendants, chercheurs et créateurs de jeux**, PTG combine :
- un **cœur scientifique** (bruit, géologie, érosion),
- des **générateurs parallélisés**,
- un système **runtime optimisé** (LOD, streaming),
- et des **intégrations natives** avec les outils de création 3D.

---

## ✨ Fonctionnalités

- 🔢 **Bruit procédural** (Perlin, Simplex, FBM…)
- 🏔️ **Systèmes géologiques** (érosion, sédimentation, strates)
- ⚡ **Parallélisation** pour de grandes cartes
- 🖼️ **Exports** :
  - Blender (`.blend`, `.gltf`)
  - Godot (scènes prêtes à l’emploi)
  - Heightmaps (`.png`, `.raw`)
- 🎮 **Runtime pour jeux** :
  - Streaming de chunks
  - Gestion mémoire
  - Système LOD dynamique
- 🧩 **Architecture extensible** avec plugins (biomes, générateurs custom)

---

## 🚀 Installation

```bash
git clone https://github.com/ton-pseudo/procedural_terrain_generator.git
cd procedural_terrain_generator
pip install -r requirements.txt
```

---

## ⚡ Utilisation rapide (CLI)

Exemple : générer un terrain désert de 512x512 et l’exporter en `.gltf` :

```bash
ptgen generate --size 512 --biome desert --export gltf
```

---

## 🐍 Utilisation en Python

```python
from generators.terrain_generator import TerrainGenerator

gen = TerrainGenerator(size=512, biome="mountain")
terrain = gen.generate()

# Export vers Godot
from export.godot_exporter import GodotExporter
GodotExporter().export(terrain, "terrain_scene.tscn")
```

---

## 📂 Structure du projet

```
procedural_terrain_generator/
├── main.py                # Point d'entrée principal
├── config/                # Configuration globale
├── core/                  # Math, bruit, géologie
├── generators/            # Générateurs procéduraux
├── blender/               # Intégration Blender
├── export/                # Export vers Godot/Heightmap
├── runtime/               # Runtime (LOD, streaming, mémoire)
├── plugins/               # (Futur) Plugins biomes/érosion
└── tests/                 # Tests unitaires
```

---

## 📌 Roadmap

- [ ] Génération de base (heightmap + bruit procédural)
- [ ] Export Blender / Godot
- [ ] Intégration CLI
- [ ] Plugins biomes
- [ ] Runtime optimisé pour jeux
- [ ] Version SaaS (génération cloud)

---

## 🤝 Contribution

Les contributions sont bienvenues 🎉  
Proposez vos idées de **biomes, générateurs ou exporters** dans le dossier `plugins/`.

---

## 📜 Licence

MIT – Utilisation libre pour projets personnels, académiques ou commerciaux.

---

🚀 Avec PTG, passez de l’**idée** au **monde jouable** en quelques lignes de code.
