# Guide d'Utilisation - Générateur de Terrain Procédural

## 🎯 Comment générer un terrain

### Méthode 1: Via l'interface Blender (Recommandée)

1. **Installer le plugin**
   - Suivre `INSTALLATION_BLENDER.md`
   - Activer "Procedural Terrain Generator"

2. **Ouvrir l'interface**
   - Vue 3D → Appuyer `N` (sidebar)
   - Onglet **"Terrain"**

3. **Configuration rapide**
   ```
   ✅ Mode preview: ACTIVÉ (pour test)
   🎲 Seed principal: 12345 (ou votre choix)
   🌍 Taille du monde: 4000m (par défaut)
   ⚡ Profil performance: Équilibré
   ```

4. **Générer**
   - Cliquer **"🌍 Générer Terrain"**
   - Attendre 5-15 secondes
   - Le terrain apparaît dans la scène !

### Méthode 2: Via ligne de commande

```bash
cd procedural_terrain_generator
python main.py generate terrain --preview --seed 123
```

## 🎮 Interface Blender détaillée

### Panneau "Paramètres de base"
- **Taille du monde**: 1000-20000m (recommandé: 4000m)
- **Taille des tuiles**: 50-1000m (recommandé: 250m)
- **Seed principal**: 0-999999 (pour reproductibilité)

### Panneau "Qualité et Performance"
- **Niveau de détail**:
  - `Bas`: Rapide, moins de détails
  - `Moyen`: Équilibré (recommandé)
  - `Élevé`: Plus de détails, plus lent
  - `Ultra`: Maximum qualité, très lent

- **Profil de performance**:
  - `Matériel modeste`: GPU intégré, <8GB RAM
  - `Équilibré`: Configuration moyenne (recommandé)
  - `Matériel puissant`: GPU dédié, >16GB RAM

- **Options**:
  - ✅ `Utiliser le cache`: Accélère les générations répétées
  - ✅ `Mode preview`: Génère 3x3 tuiles seulement (test rapide)

## 🚀 Workflow recommandé

### 1. Premier test (30 secondes)
```
✅ Mode preview: ACTIVÉ
🎲 Seed: 12345
⚡ Performance: Équilibré
🎯 Cliquer: "🌍 Générer Terrain"
```

### 2. Ajustement des paramètres
- Changer le **seed** pour différents terrains
- Tester différents **niveaux de détail**
- Ajuster la **taille du monde** si nécessaire

### 3. Génération finale
```
❌ Mode preview: DÉSACTIVÉ
🌍 Taille: Selon vos besoins
⚡ Performance: Selon votre matériel
⏱️ Temps: 2-10 minutes selon la taille
```

## 🎨 Personnalisation avancée

### Seeds intéressants à tester
- `12345`: Terrain équilibré avec montagnes
- `67890`: Terrain plus plat avec rivières
- `11111`: Terrain montagneux
- `99999`: Terrain avec bassins

### Combinaisons recommandées

**Pour exploration rapide:**
```
Taille monde: 2000m
Mode preview: ✅
Détail: Moyen
Performance: Équilibré
```

**Pour monde de jeu:**
```
Taille monde: 8000m
Mode preview: ❌
Détail: Élevé
Performance: Matériel puissant
```

**Pour rendu cinématique:**
```
Taille monde: 4000m
Mode preview: ❌
Détail: Ultra
Performance: Matériel puissant
```

## 📤 Export vers Godot

### Configuration export
1. **Activer**: "Export Godot" ✅
2. **Dossier**: Définir le chemin (ex: `//godot_export/`)
3. **Auto-export**: Se fait après génération

### Export manuel
- Générer le terrain d'abord
- Cliquer **"🎮 Export Godot"**
- Fichiers créés dans le dossier défini

### Fichiers exportés
```
godot_export/
├── meshes/          # Fichiers .obj des tuiles
├── heightmaps/      # Images .png des hauteurs
├── metadata/        # Fichiers .json avec infos
└── scenes/          # Scènes Godot .tscn
```

## 🔧 Gestion du cache

### Avantages du cache
- **Génération 10x plus rapide** pour même seed
- **Réutilisation** des tuiles identiques
- **Économie** de calcul

### Gestion
- **Vider cache**: Bouton "🗑️ Vider Cache"
- **Localisation**: Dossier `terrain_cache/`
- **Taille**: Surveillée automatiquement

## ⚡ Optimisation des performances

### Si génération trop lente
1. **Activer "Mode preview"** pour tester
2. **Réduire "Taille du monde"**
3. **Choisir "Matériel modeste"**
4. **Utiliser détail "Bas" ou "Moyen"**

### Si manque de mémoire
1. **Fermer autres applications**
2. **Réduire taille du monde**
3. **Profil "Matériel modeste"**
4. **Vider le cache** si nécessaire

### Si Blender plante
1. **Sauvegarder** avant génération
2. **Réduire** tous les paramètres
3. **Tester** en mode preview d'abord

## 🎯 Cas d'usage typiques

### Prototype de jeu
```bash
# CLI rapide
python main.py generate terrain --preview --seed 123
```

### Asset pour film/animation
```
Interface Blender:
- Taille: 4000-8000m
- Détail: Élevé/Ultra
- Preview: ❌
- Export Godot: ❌
```

### Monde pour jeu Godot
```
Interface Blender:
- Taille: 6000-12000m
- Détail: Élevé
- Preview: ❌
- Export Godot: ✅
```

### Test/expérimentation
```
Interface Blender:
- Preview: ✅ (toujours)
- Changer seed souvent
- Tester différents profils
```

## 🆘 Résolution de problèmes

### "Génération trop lente"
- Activer mode preview
- Réduire taille du monde
- Profil "Matériel modeste"

### "Pas de terrain visible"
- Vérifier la console Blender (`Window > Toggle System Console`)
- Essayer seed différent
- Vider le cache

### "Erreur mémoire"
- Fermer autres applications
- Réduire taille du monde
- Redémarrer Blender

### "Export Godot échoue"
- Vérifier le chemin d'export
- Créer le dossier manuellement
- Permissions d'écriture

## 🎨 Après génération

### Dans Blender
- **Matériaux**: Appliqués automatiquement
- **Éclairage**: Ajuster selon vos besoins
- **Caméra**: Positionner pour vue d'ensemble
- **Rendu**: Cycles ou Eevee selon qualité

### Modifications possibles
- **Sculpting**: Affiner certaines zones
- **Texture painting**: Ajouter détails
- **Modifiers**: Subdivision, displacement
- **Animation**: Caméra survol, etc.

Le terrain généré est un **vrai mesh Blender** modifiable normalement !
