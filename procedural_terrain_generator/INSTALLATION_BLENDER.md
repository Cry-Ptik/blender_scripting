# Installation du Plugin Blender - Générateur de Terrain Procédural

## 📋 Prérequis

- **Blender 4.0+** (compatible avec Blender 5.0)
- **Python 3.10+** (inclus avec Blender)
- **Numpy** et **Scipy** (installés automatiquement)

## 🚀 Installation Rapide

### Méthode 1: Installation via ZIP (Recommandée)

1. **Créer l'archive ZIP**
   - Compresser le dossier `procedural_terrain_generator` en ZIP
   - Ou télécharger le ZIP depuis le repository

2. **Installer dans Blender**
   - Ouvrir Blender
   - Aller dans `Edit > Preferences > Add-ons`
   - Cliquer sur `Install...`
   - Sélectionner le fichier ZIP
   - Activer le plugin "Procedural Terrain Generator"

### Méthode 2: Installation Manuelle

1. **Localiser le dossier des addons Blender**
   ```
   Windows: %APPDATA%\Blender Foundation\Blender\4.x\scripts\addons\
   macOS: ~/Library/Application Support/Blender/4.x/scripts/addons/
   Linux: ~/.config/blender/4.x/scripts/addons/
   ```

2. **Copier le dossier**
   - Copier tout le dossier `procedural_terrain_generator` dans le dossier addons
   - Redémarrer Blender

3. **Activer le plugin**
   - `Edit > Preferences > Add-ons`
   - Rechercher "Procedural Terrain Generator"
   - Cocher la case pour l'activer

## 🎮 Utilisation

### Interface Utilisateur

Le plugin ajoute un panneau **"Terrain"** dans la sidebar de la Vue 3D:

1. **Ouvrir le panneau**
   - Vue 3D → Sidebar (N) → Onglet "Terrain"

2. **Paramètres disponibles**
   - **Taille du monde**: 1000-20000m
   - **Taille des tuiles**: 50-1000m  
   - **Seed principal**: Pour la reproductibilité
   - **Niveau de détail**: Bas/Moyen/Élevé/Ultra
   - **Profil de performance**: Selon votre matériel
   - **Mode preview**: Génération 3x3 tuiles pour test

### Génération Rapide

1. **Mode Preview (Recommandé pour débuter)**
   - Activer "Mode preview"
   - Ajuster le seed si désiré
   - Cliquer "🌍 Générer Terrain"

2. **Génération Complète**
   - Désactiver "Mode preview"
   - Choisir la taille du monde
   - ⚠️ **Attention**: Peut prendre plusieurs minutes

### Export Godot

1. **Configuration**
   - Définir le "Dossier export Godot"
   - Activer "Export Godot" pour export automatique

2. **Export Manuel**
   - Cliquer "🎮 Export Godot" après génération

## ⚙️ Configuration Avancée

### Profils de Performance

- **Matériel modeste**: Optimisé pour GPU intégré, RAM limitée
- **Équilibré**: Configuration par défaut
- **Matériel puissant**: Utilise toute la puissance disponible

### Cache

- **Activé par défaut**: Accélère les générations répétées
- **Vider Cache**: Bouton "🗑️ Vider Cache" si nécessaire

## 🔧 Dépannage

### Erreurs Communes

1. **"Module not found"**
   ```
   Solution: Réinstaller le plugin via ZIP
   ```

2. **"Génération lente"**
   ```
   Solution: Utiliser "Mode preview" ou profil "Matériel modeste"
   ```

3. **"Erreur mémoire"**
   ```
   Solution: Réduire la taille du monde ou utiliser profil bas
   ```

### Logs et Debug

- Les erreurs s'affichent dans la console Blender
- Ouvrir: `Window > Toggle System Console`

## 📁 Structure des Fichiers

```
procedural_terrain_generator/
├── __init__.py              # Plugin principal avec interface
├── config/                  # Configuration
├── core/                    # Systèmes de base
├── blender/                 # Intégration Blender
├── export/                  # Export vers moteurs
├── runtime/                 # Systèmes runtime
├── generators/              # Générateurs de terrain
├── terrain_cache/           # Cache (créé automatiquement)
└── godot_export/           # Export Godot (créé automatiquement)
```

## 🎯 Utilisation CLI (Optionnelle)

Le plugin peut aussi être utilisé en ligne de commande:

```bash
cd procedural_terrain_generator
python main.py generate terrain --preview --seed 123
```

## 🆘 Support

- **Documentation**: Voir README.md
- **Problèmes**: Vérifier la console Blender
- **Performance**: Ajuster les profils selon votre matériel

## 🔄 Mise à Jour

1. Désactiver l'ancien plugin
2. Supprimer l'ancien dossier
3. Installer la nouvelle version
4. Réactiver le plugin
