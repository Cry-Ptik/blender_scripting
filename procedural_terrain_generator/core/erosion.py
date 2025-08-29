"""
Système d'érosion hydraulique réaliste pour génération de terrain procédural.
Simule l'érosion par l'eau pour créer vallées, canyons et formations naturelles.
"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class WaterDroplet:
    """Représente une gouttelette d'eau pour simulation d'érosion."""
    x: float
    y: float
    velocity_x: float = 0.0
    velocity_y: float = 0.0
    water: float = 1.0
    sediment: float = 0.0
    

class HydraulicErosion:
    """
    Système d'érosion hydraulique avancé.
    Simule l'écoulement d'eau et l'érosion pour créer vallées réalistes.
    """
    
    def __init__(self, 
                 evaporation_rate: float = 0.01,
                 sediment_capacity_factor: float = 4.0,
                 min_sediment_capacity: float = 0.01,
                 erosion_speed: float = 0.3,
                 deposition_speed: float = 0.3,
                 erosion_radius: int = 3,
                 gravity: float = 4.0,
                 max_droplet_lifetime: int = 30):
        """
        Initialize hydraulic erosion system.
        
        Args:
            evaporation_rate: Taux d'évaporation de l'eau
            sediment_capacity_factor: Facteur de capacité de sédiment
            min_sediment_capacity: Capacité minimale de sédiment
            erosion_speed: Vitesse d'érosion
            deposition_speed: Vitesse de dépôt
            erosion_radius: Rayon d'érosion autour de la gouttelette
            gravity: Force de gravité
            max_droplet_lifetime: Durée de vie maximale d'une gouttelette
        """
        self.evaporation_rate = evaporation_rate
        self.sediment_capacity_factor = sediment_capacity_factor
        self.min_sediment_capacity = min_sediment_capacity
        self.erosion_speed = erosion_speed
        self.deposition_speed = deposition_speed
        self.erosion_radius = erosion_radius
        self.gravity = gravity
        self.max_droplet_lifetime = max_droplet_lifetime
        self.num_droplets = 50000
    
    def erode_terrain(self, heightmap: np.ndarray, num_iterations: int = 50000) -> np.ndarray:
        """
        Applique l'érosion hydraulique sur un heightmap.
        
        Args:
            heightmap: Carte d'élévation à éroder
            num_iterations: Nombre d'itérations d'érosion
            
        Returns:
            Heightmap érodé
        """
        height, width = heightmap.shape
        eroded_heightmap = heightmap.copy()
        
        # Pré-calculer les gradients pour optimisation
        gradient_x, gradient_y = np.gradient(eroded_heightmap)
        
        for iteration in range(num_iterations):
            # Créer une gouttelette aléatoire
            droplet = WaterDroplet(
                x=np.random.random() * (width - 1),
                y=np.random.random() * (height - 1)
            )
            
            # Simuler le parcours de la gouttelette
            self._simulate_droplet(eroded_heightmap, droplet, gradient_x, gradient_y)
            
            # Recalculer gradients périodiquement pour performance
            if iteration % 1000 == 0:
                gradient_x, gradient_y = np.gradient(eroded_heightmap)
        
        return eroded_heightmap
    
    def _simulate_droplet(self, heightmap: np.ndarray, droplet: WaterDroplet,
                         gradient_x: np.ndarray, gradient_y: np.ndarray) -> None:
        """Simule le parcours d'une gouttelette d'eau."""
        height, width = heightmap.shape
        
        for lifetime in range(self.max_droplet_lifetime):
            # Position actuelle (avec interpolation)
            node_x = int(droplet.x)
            node_y = int(droplet.y)
            
            # Vérifier les limites
            if (node_x < 0 or node_x >= width - 1 or 
                node_y < 0 or node_y >= height - 1):
                break
            
            # Calculer offset pour interpolation bilinéaire
            cell_offset_x = droplet.x - node_x
            cell_offset_y = droplet.y - node_y
            
            # Hauteur interpolée à la position actuelle
            current_height = self._get_interpolated_height(
                heightmap, droplet.x, droplet.y
            )
            
            # Gradient interpolé
            grad_x = self._interpolate_gradient(gradient_x, droplet.x, droplet.y)
            grad_y = self._interpolate_gradient(gradient_y, droplet.x, droplet.y)
            
            # Direction du mouvement (suivre la pente)
            dir_x = -grad_x
            dir_y = -grad_y
            
            # Normaliser la direction
            dir_length = np.sqrt(dir_x**2 + dir_y**2)
            if dir_length > 0:
                dir_x /= dir_length
                dir_y /= dir_length
            
            # Nouvelle position
            new_x = droplet.x + dir_x
            new_y = droplet.y + dir_y
            
            # Hauteur à la nouvelle position
            new_height = self._get_interpolated_height(heightmap, new_x, new_y)
            
            # Différence de hauteur
            height_diff = current_height - new_height
            
            # Capacité de sédiment basée sur vitesse et différence de hauteur
            speed = np.sqrt(droplet.velocity_x**2 + droplet.velocity_y**2)
            sediment_capacity = max(
                height_diff * speed * droplet.water * self.sediment_capacity_factor,
                self.min_sediment_capacity
            )
            
            # Si la gouttelette transporte plus de sédiment qu'elle ne peut
            if droplet.sediment > sediment_capacity or height_diff < 0:
                # Déposer du sédiment
                amount_to_deposit = min(
                    droplet.sediment - sediment_capacity,
                    -height_diff
                ) if height_diff < 0 else (droplet.sediment - sediment_capacity) * self.deposition_speed
                
                droplet.sediment -= amount_to_deposit
                self._deposit_sediment(heightmap, droplet.x, droplet.y, amount_to_deposit)
            
            else:
                # Éroder le terrain
                amount_to_erode = min(
                    (sediment_capacity - droplet.sediment) * self.erosion_speed,
                    height_diff
                )
                
                self._erode_at_position(heightmap, droplet.x, droplet.y, amount_to_erode)
                droplet.sediment += amount_to_erode
            
            # Mettre à jour la vitesse
            droplet.velocity_x = droplet.velocity_x * 0.9 + dir_x * height_diff * self.gravity
            droplet.velocity_y = droplet.velocity_y * 0.9 + dir_y * height_diff * self.gravity
            
            # Évaporation
            droplet.water *= (1 - self.evaporation_rate)
            
            # Mettre à jour la position
            droplet.x = new_x
            droplet.y = new_y
            
            # Arrêter si plus d'eau
            if droplet.water < 0.01:
                break
    
    def _get_interpolated_height(self, heightmap: np.ndarray, x: float, y: float) -> float:
        """Obtient la hauteur interpolée à une position donnée."""
        height, width = heightmap.shape
        
        # Clamp coordinates
        x = max(0, min(width - 1.001, x))
        y = max(0, min(height - 1.001, y))
        
        # Get integer coordinates
        x0, y0 = int(x), int(y)
        x1, y1 = min(x0 + 1, width - 1), min(y0 + 1, height - 1)
        
        # Interpolation weights
        wx = x - x0
        wy = y - y0
        
        # Bilinear interpolation
        return (heightmap[y0, x0] * (1 - wx) * (1 - wy) +
                heightmap[y0, x1] * wx * (1 - wy) +
                heightmap[y1, x0] * (1 - wx) * wy +
                heightmap[y1, x1] * wx * wy)
    
    def _interpolate_gradient(self, gradient: np.ndarray, x: float, y: float) -> float:
        """Interpole le gradient à une position donnée."""
        return self._get_interpolated_height(gradient, x, y)
    
    def _erode_at_position(self, heightmap: np.ndarray, x: float, y: float, amount: float) -> None:
        """Érode le terrain à une position donnée."""
        height, width = heightmap.shape
        center_x, center_y = int(x), int(y)
        
        # Éroder dans un rayon autour de la position
        for dy in range(-self.erosion_radius, self.erosion_radius + 1):
            for dx in range(-self.erosion_radius, self.erosion_radius + 1):
                coord_x = center_x + dx
                coord_y = center_y + dy
                
                if 0 <= coord_x < width and 0 <= coord_y < height:
                    # Distance au centre
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance <= self.erosion_radius:
                        # Poids basé sur la distance (plus fort au centre)
                        weight = 1 - (distance / self.erosion_radius)
                        heightmap[coord_y, coord_x] -= amount * weight
    
    def _deposit_sediment(self, heightmap: np.ndarray, x: float, y: float, amount: float) -> None:
        """Dépose du sédiment à une position donnée."""
        height, width = heightmap.shape
        center_x, center_y = int(x), int(y)
        
        # Déposer dans un rayon autour de la position
        for dy in range(-self.erosion_radius, self.erosion_radius + 1):
            for dx in range(-self.erosion_radius, self.erosion_radius + 1):
                coord_x = center_x + dx
                coord_y = center_y + dy
                
                if 0 <= coord_x < width and 0 <= coord_y < height:
                    # Distance au centre
                    distance = np.sqrt(dx**2 + dy**2)
                    if distance <= self.erosion_radius:
                        # Poids basé sur la distance
                        weight = 1 - (distance / self.erosion_radius)
                        heightmap[coord_y, coord_x] += amount * weight
