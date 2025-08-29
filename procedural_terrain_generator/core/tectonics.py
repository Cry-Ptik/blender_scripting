"""
Système tectonique réaliste pour génération de terrain procédural.
Simule les plaques tectoniques, failles et formations géologiques.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class PlateType(Enum):
    """Types de plaques tectoniques."""
    OCEANIC = "oceanic"
    CONTINENTAL = "continental"
    MIXED = "mixed"


class BoundaryType(Enum):
    """Types de frontières entre plaques."""
    DIVERGENT = "divergent"      # Plaques s'éloignent
    CONVERGENT = "convergent"    # Plaques se rapprochent
    TRANSFORM = "transform"      # Plaques glissent


@dataclass
class TectonicPlate:
    """Représente une plaque tectonique."""
    id: int
    center: Tuple[float, float]
    radius: float
    plate_type: PlateType
    velocity: Tuple[float, float]  # Vitesse de déplacement
    age: float  # Âge géologique
    density: float  # Densité de la plaque
    thickness: float  # Épaisseur


class TectonicSystem:
    """
    Système tectonique avancé pour génération de terrain réaliste.
    Simule les interactions entre plaques tectoniques.
    """
    
    def __init__(self, world_size: int, num_plates: int = 8):
        """
        Initialize tectonic system.
        
        Args:
            world_size: Taille du monde
            num_plates: Nombre de plaques tectoniques
        """
        self.world_size = world_size
        self.num_plates = num_plates
        self.plates: List[TectonicPlate] = []
        self.strength_multiplier = 1.0
        
        # Generate tectonic plates
        self._generate_plates()
        
        # Calculate boundaries
        self.boundaries = self._calculate_boundaries()
        
        # Fault zones
        self.fault_zones = self._generate_fault_zones()
    
    def _generate_plates(self) -> None:
        """Génère les plaques tectoniques de manière réaliste."""
        np.random.seed(42)  # Pour reproductibilité
        
        for i in range(self.num_plates):
            # Position aléatoire
            center_x = np.random.uniform(0.1, 0.9)
            center_y = np.random.uniform(0.1, 0.9)
            
            # Rayon basé sur la taille du monde
            radius = np.random.uniform(0.15, 0.35)
            
            # Type de plaque (plus de plaques continentales)
            if np.random.random() < 0.6:
                plate_type = PlateType.CONTINENTAL
                density = np.random.uniform(2.7, 3.0)  # Densité continentale
                thickness = np.random.uniform(30, 70)   # km
            else:
                plate_type = PlateType.OCEANIC
                density = np.random.uniform(3.0, 3.3)  # Densité océanique
                thickness = np.random.uniform(5, 15)    # km
            
            # Vitesse de déplacement (cm/an converti en unités normalisées)
            velocity_x = np.random.uniform(-0.001, 0.001)
            velocity_y = np.random.uniform(-0.001, 0.001)
            
            # Âge géologique (millions d'années)
            age = np.random.uniform(10, 200)
            
            plate = TectonicPlate(
                id=i,
                center=(center_x, center_y),
                radius=radius,
                plate_type=plate_type,
                velocity=(velocity_x, velocity_y),
                age=age,
                density=density,
                thickness=thickness
            )
            
            self.plates.append(plate)
    
    def _calculate_boundaries(self) -> List[Dict]:
        """Calcule les frontières entre plaques."""
        boundaries = []
        
        for i, plate1 in enumerate(self.plates):
            for j, plate2 in enumerate(self.plates[i+1:], i+1):
                # Distance entre centres
                dx = plate2.center[0] - plate1.center[0]
                dy = plate2.center[1] - plate1.center[1]
                distance = np.sqrt(dx**2 + dy**2)
                
                # Vérifier si les plaques sont adjacentes
                if distance < (plate1.radius + plate2.radius) * 1.2:
                    # Déterminer le type de frontière
                    boundary_type = self._determine_boundary_type(plate1, plate2)
                    
                    boundary = {
                        'plate1_id': plate1.id,
                        'plate2_id': plate2.id,
                        'type': boundary_type,
                        'strength': self._calculate_boundary_strength(plate1, plate2),
                        'position': ((plate1.center[0] + plate2.center[0]) / 2,
                                   (plate1.center[1] + plate2.center[1]) / 2)
                    }
                    boundaries.append(boundary)
        
        return boundaries
    
    def _determine_boundary_type(self, plate1: TectonicPlate, plate2: TectonicPlate) -> BoundaryType:
        """Détermine le type de frontière entre deux plaques."""
        # Vecteurs de vitesse
        v1 = np.array(plate1.velocity)
        v2 = np.array(plate2.velocity)
        
        # Vecteur entre centres
        center_vec = np.array([
            plate2.center[0] - plate1.center[0],
            plate2.center[1] - plate1.center[1]
        ])
        center_vec = center_vec / np.linalg.norm(center_vec)
        
        # Vitesse relative
        relative_velocity = v2 - v1
        
        # Produit scalaire pour déterminer le type
        dot_product = np.dot(relative_velocity, center_vec)
        
        if abs(dot_product) < 0.0001:  # Mouvement parallèle
            return BoundaryType.TRANSFORM
        elif dot_product > 0:  # Plaques s'éloignent
            return BoundaryType.DIVERGENT
        else:  # Plaques se rapprochent
            return BoundaryType.CONVERGENT
    
    def _calculate_boundary_strength(self, plate1: TectonicPlate, plate2: TectonicPlate) -> float:
        """Calcule la force d'interaction entre deux plaques."""
        # Basé sur la différence de densité et vitesse relative
        density_diff = abs(plate1.density - plate2.density)
        
        v1 = np.array(plate1.velocity)
        v2 = np.array(plate2.velocity)
        velocity_magnitude = np.linalg.norm(v2 - v1)
        
        return (density_diff * 0.5 + velocity_magnitude * 1000) * 0.5
    
    def _generate_fault_zones(self) -> List[Dict]:
        """Génère les zones de failles."""
        fault_zones = []
        
        for boundary in self.boundaries:
            plate1 = self.plates[boundary['plate1_id']]
            plate2 = self.plates[boundary['plate2_id']]
            
            # Nombre de failles selon le type de frontière
            if boundary['type'] == BoundaryType.CONVERGENT:
                num_faults = np.random.randint(3, 8)
            elif boundary['type'] == BoundaryType.DIVERGENT:
                num_faults = np.random.randint(2, 5)
            else:  # TRANSFORM
                num_faults = np.random.randint(1, 4)
            
            for _ in range(num_faults):
                # Position aléatoire près de la frontière
                center_x, center_y = boundary['position']
                fault_x = center_x + np.random.uniform(-0.1, 0.1)
                fault_y = center_y + np.random.uniform(-0.1, 0.1)
                
                fault = {
                    'position': (fault_x, fault_y),
                    'length': np.random.uniform(0.05, 0.2),
                    'angle': np.random.uniform(0, 2 * np.pi),
                    'depth': np.random.uniform(5, 25),  # km
                    'activity': np.random.uniform(0.1, 1.0),
                    'boundary_type': boundary['type']
                }
                fault_zones.append(fault)
        
        return fault_zones
    
    def calculate_tectonic_influence(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Calcule l'influence tectonique sur l'élévation du terrain.
        
        Args:
            x, y: Coordonnées normalisées (0-1)
            
        Returns:
            Influence tectonique sur l'élévation
        """
        influence = np.zeros_like(x)
        
        # Influence des plaques
        for plate in self.plates:
            # Distance à la plaque
            dx = x - plate.center[0]
            dy = y - plate.center[1]
            distance = np.sqrt(dx**2 + dy**2)
            
            # Influence basée sur le type de plaque
            if plate.plate_type == PlateType.CONTINENTAL:
                # Plaques continentales créent des élévations
                plate_influence = np.exp(-distance / (plate.radius * 0.5)) * 0.8
            else:
                # Plaques océaniques créent des dépressions
                plate_influence = -np.exp(-distance / (plate.radius * 0.3)) * 0.4
            
            influence += plate_influence
        
        # Influence des frontières (zones de collision)
        for boundary in self.boundaries:
            bx, by = boundary['position']
            dx = x - bx
            dy = y - by
            distance = np.sqrt(dx**2 + dy**2)
            
            if boundary['type'] == BoundaryType.CONVERGENT:
                # Collision crée des montagnes
                boundary_influence = np.exp(-distance / 0.1) * boundary['strength'] * 1.5
            elif boundary['type'] == BoundaryType.DIVERGENT:
                # Divergence crée des vallées/rifts
                boundary_influence = -np.exp(-distance / 0.08) * boundary['strength'] * 0.8
            else:  # TRANSFORM
                # Failles transformantes créent des variations locales
                boundary_influence = np.sin(distance * 20) * np.exp(-distance / 0.05) * boundary['strength'] * 0.3
            
            influence += boundary_influence
        
        # Influence des failles
        for fault in self.fault_zones:
            fx, fy = fault['position']
            dx = x - fx
            dy = y - fy
            distance = np.sqrt(dx**2 + dy**2)
            
            # Influence directionnelle selon l'angle de la faille
            angle = fault['angle']
            directional_factor = np.abs(np.cos(angle) * dx + np.sin(angle) * dy)
            
            fault_influence = (np.exp(-distance / 0.03) * 
                             fault['activity'] * 
                             (1 + directional_factor) * 0.2)
            
            if fault['boundary_type'] == BoundaryType.CONVERGENT:
                influence += fault_influence
            else:
                influence -= fault_influence * 0.5
        
        return influence
    
    def get_plate_at_position(self, x: float, y: float) -> Optional[TectonicPlate]:
        """
        Retourne la plaque tectonique à une position donnée.
        
        Args:
            x, y: Coordonnées normalisées
            
        Returns:
            Plaque tectonique ou None
        """
        for plate in self.plates:
            dx = x - plate.center[0]
            dy = y - plate.center[1]
            distance = np.sqrt(dx**2 + dy**2)
            
            if distance <= plate.radius:
                return plate
        
        return None
    
    def get_geological_age(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Calcule l'âge géologique du terrain.
        
        Args:
            x, y: Coordonnées normalisées
            
        Returns:
            Âge géologique en millions d'années
        """
        age = np.zeros_like(x)
        
        for plate in self.plates:
            dx = x - plate.center[0]
            dy = y - plate.center[1]
            distance = np.sqrt(dx**2 + dy**2)
            
            # Influence de l'âge de la plaque
            plate_mask = distance <= plate.radius
            age[plate_mask] = plate.age
        
        return age
    
    def get_tectonic_stress(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Calcule le stress tectonique (pour érosion différentielle).
        
        Args:
            x, y: Coordonnées normalisées
            
        Returns:
            Niveau de stress tectonique
        """
        stress = np.zeros_like(x)
        
        # Stress élevé près des frontières
        for boundary in self.boundaries:
            bx, by = boundary['position']
            dx = x - bx
            dy = y - by
            distance = np.sqrt(dx**2 + dy**2)
            
            boundary_stress = np.exp(-distance / 0.15) * boundary['strength']
            stress += boundary_stress
        
        # Stress des failles
        for fault in self.fault_zones:
            fx, fy = fault['position']
            dx = x - fx
            dy = y - fy
            distance = np.sqrt(dx**2 + dy**2)
            
            fault_stress = np.exp(-distance / 0.05) * fault['activity']
            stress += fault_stress
        
        return stress
