# TODO - Amélioration Terrain Procédural Réaliste

## 🏔️ PRIORITÉ HAUTE - Relief et Volume

### 1. Amélioration du système de bruit
- [ ] **Augmenter l'amplitude du bruit Perlin** (actuellement trop faible)
- [ ] **Implémenter bruit multi-octaves avancé** avec paramètres réalistes
- [ ] **Ajouter bruit ridged** pour crêtes montagneuses
- [ ] **Implémenter bruit Worley** pour formations rocheuses
- [ ] **Combiner plusieurs types de bruit** selon altitude

### 2. Système géologique réaliste
- [ ] **Implémenter formation tectonique** (plaques, failles)
- [ ] **Ajouter système de chaînes montagneuses** avec orientation
- [ ] **Créer zones d'élévation différenciées** (plaines, collines, montagnes)
- [ ] **Implémenter érosion hydraulique** pour vallées réalistes
- [ ] **Ajouter érosion thermique** pour éboulis et pentes

### 3. Paramètres d'élévation
- [ ] **Augmenter range d'élévation** (actuellement ~25 unités → 500+ unités)
- [ ] **Implémenter courbes d'élévation** non-linéaires
- [ ] **Ajouter masques d'altitude** pour contrôler distribution
- [ ] **Créer profils de montagne** réalistes (pentes, sommets)

## 🌍 PRIORITÉ MOYENNE - Réalisme géographique

### 4. Biomes et zones climatiques
- [ ] **Système de biomes** basé sur altitude/latitude
- [ ] **Transition graduelle** entre biomes
- [ ] **Végétation procédurale** selon biome
- [ ] **Système météorologique** influençant terrain

### 5. Hydrographie avancée
- [ ] **Réseau de rivières** suivant pentes naturelles
- [ ] **Lacs et bassins** dans dépressions
- [ ] **Deltas et estuaires** réalistes
- [ ] **Érosion fluviale** creusant canyons

### 6. Détails géologiques
- [ ] **Strates rocheuses** visibles sur falaises
- [ ] **Formations karstiques** (grottes, dolines)
- [ ] **Volcans et caldeiras** avec coulées de lave
- [ ] **Glaciers et moraines** en haute altitude

## ⚡ PRIORITÉ MOYENNE - Performance et Optimisation

### 7. Génération optimisée
- [ ] **LOD adaptatif** selon distance caméra
- [ ] **Streaming de chunks** pour mondes infinis
- [ ] **Cache intelligent** des calculs géologiques
- [ ] **Parallélisation GPU** avec compute shaders

### 8. Pipeline Blender-Godot
- [ ] **Export optimisé** vers Godot 4.4
- [ ] **Matériaux PBR** automatiques selon géologie
- [ ] **Collision meshes** simplifiées
- [ ] **Lightmaps** pré-calculées

## 🎨 PRIORITÉ BASSE - Esthétique et Finition

### 9. Matériaux procéduraux
- [ ] **Textures selon pente** (roche/herbe/neige)
- [ ] **Masques d'humidité** pour mousse/lichen
- [ ] **Variation de couleur** selon exposition solaire
- [ ] **Détails de surface** (cailloux, fissures)

### 10. Éclairage et atmosphère
- [ ] **Système jour/nuit** dynamique
- [ ] **Brouillard volumétrique** dans vallées
- [ ] **Éclairage indirect** pour crevasses
- [ ] **Ombres de relief** réalistes

## 🔧 PRIORITÉ IMMÉDIATE - Corrections urgentes

### 11. Fixes critiques
- [x] ~~Classe OptimizedNoise sans ABC~~
- [ ] **Multiplier élévations par facteur 10-20x**
- [ ] **Ajuster paramètres FBM** (octaves, persistence, lacunarity)
- [ ] **Implémenter vraie géologie** au lieu de placeholders
- [ ] **Tester avec différentes seeds** pour variété

---

## 📋 Plan d'action immédiat

1. **Augmenter amplitude** : Modifier `base_elevation * 25` → `base_elevation * 500`
2. **Améliorer FBM** : Octaves=8, persistence=0.7, lacunarity=2.5
3. **Ajouter bruit ridged** pour montagnes dramatiques
4. **Implémenter masques d'élévation** pour zones distinctes
5. **Tester et itérer** jusqu'à relief satisfaisant

## 🎯 Objectif final
Créer des terrains avec **relief dramatique**, **montagnes imposantes**, **vallées profondes** et **géologie crédible** pour jeux/visualisations ultra-réalistes.
