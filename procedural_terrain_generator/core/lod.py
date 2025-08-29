"""
Système LOD (Level of Detail) adaptatif pour optimisation des performances.
Gère la génération de terrain à différents niveaux de détail selon la distance.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class LODLevel(Enum):
    """Niveaux de détail disponibles."""
    ULTRA_HIGH = 0  # 1024x1024 - Distance < 100m
    HIGH = 1        # 512x512  - Distance < 500m  
    MEDIUM = 2      # 256x256  - Distance < 2km
    LOW = 3         # 128x128  - Distance < 10km
    ULTRA_LOW = 4   # 64x64    - Distance > 10km


@dataclass
class LODChunk:
    """Représente un chunk de terrain avec son niveau de détail."""
    x: int
    y: int
    size: int
    lod_level: LODLevel
    resolution: int
    distance_to_camera: float
    is_loaded: bool = False
    heightmap: Optional[np.ndarray] = None
    last_update: float = 0.0


class AdaptiveLOD:
    """
    Système LOD adaptatif pour génération de terrain procédural.
    Optimise les performances en ajustant la résolution selon la distance.
    """
    
    def __init__(self, world_size: int = 10000, chunk_size: int = 1000):
        """
        Initialize adaptive LOD system.
        
        Args:
            world_size: Taille totale du monde
            chunk_size: Taille de base des chunks
        """
        self.world_size = world_size
        self.chunk_size = chunk_size
        
        # Configuration des niveaux LOD
        self.lod_config = {
            LODLevel.ULTRA_HIGH: {
                'resolution': 1024,
                'max_distance': 100.0,
                'update_frequency': 0.1  # Mise à jour très fréquente
            },
            LODLevel.HIGH: {
                'resolution': 512,
                'max_distance': 500.0,
                'update_frequency': 0.5
            },
            LODLevel.MEDIUM: {
                'resolution': 256,
                'max_distance': 2000.0,
                'update_frequency': 1.0
            },
            LODLevel.LOW: {
                'resolution': 128,
                'max_distance': 10000.0,
                'update_frequency': 2.0
            },
            LODLevel.ULTRA_LOW: {
                'resolution': 64,
                'max_distance': float('inf'),
                'update_frequency': 5.0  # Mise à jour rare
            }
        }
        
        # Cache des chunks
        self.loaded_chunks: Dict[Tuple[int, int], LODChunk] = {}
        self.camera_position = np.array([0.0, 0.0, 0.0])
        
        # Statistiques de performance
        self.stats = {
            'total_chunks': 0,
            'active_chunks': 0,
            'memory_usage': 0,
            'generation_time': 0.0
        }
    
    def update_camera_position(self, position: np.ndarray) -> None:
        """
        Met à jour la position de la caméra pour recalculer les LOD.
        
        Args:
            position: Position de la caméra [x, y, z]
        """
        self.camera_position = position
        self._update_chunk_lod_levels()
    
    def get_required_chunks(self, view_distance: float = 15000.0) -> List[Tuple[int, int]]:
        """
        Détermine quels chunks doivent être chargés selon la position de la caméra.
        
        Args:
            view_distance: Distance maximale de vue
            
        Returns:
            Liste des coordonnées de chunks à charger
        """
        camera_chunk_x = int(self.camera_position[0] // self.chunk_size)
        camera_chunk_y = int(self.camera_position[1] // self.chunk_size)
        
        chunk_radius = int(view_distance // self.chunk_size) + 1
        required_chunks = []
        
        for dx in range(-chunk_radius, chunk_radius + 1):
            for dy in range(-chunk_radius, chunk_radius + 1):
                chunk_x = camera_chunk_x + dx
                chunk_y = camera_chunk_y + dy
                
                # Vérifier si le chunk est dans les limites du monde
                if (0 <= chunk_x * self.chunk_size < self.world_size and
                    0 <= chunk_y * self.chunk_size < self.world_size):
                    
                    # Calculer la distance au chunk
                    chunk_center_x = (chunk_x + 0.5) * self.chunk_size
                    chunk_center_y = (chunk_y + 0.5) * self.chunk_size
                    distance = np.sqrt(
                        (chunk_center_x - self.camera_position[0])**2 +
                        (chunk_center_y - self.camera_position[1])**2
                    )
                    
                    if distance <= view_distance:
                        required_chunks.append((chunk_x, chunk_y))
        
        return required_chunks
    
    def determine_lod_level(self, chunk_x: int, chunk_y: int) -> LODLevel:
        """
        Détermine le niveau LOD approprié pour un chunk.
        
        Args:
            chunk_x, chunk_y: Coordonnées du chunk
            
        Returns:
            Niveau LOD approprié
        """
        # Calculer la distance au centre du chunk
        chunk_center_x = (chunk_x + 0.5) * self.chunk_size
        chunk_center_y = (chunk_y + 0.5) * self.chunk_size
        
        distance = np.sqrt(
            (chunk_center_x - self.camera_position[0])**2 +
            (chunk_center_y - self.camera_position[1])**2
        )
        
        # Déterminer le niveau LOD basé sur la distance
        for lod_level in LODLevel:
            if distance <= self.lod_config[lod_level]['max_distance']:
                return lod_level
        
        return LODLevel.ULTRA_LOW
    
    def get_chunk_resolution(self, lod_level: LODLevel) -> int:
        """
        Obtient la résolution pour un niveau LOD donné.
        
        Args:
            lod_level: Niveau LOD
            
        Returns:
            Résolution du heightmap
        """
        return self.lod_config[lod_level]['resolution']
    
    def should_update_chunk(self, chunk: LODChunk, current_time: float) -> bool:
        """
        Détermine si un chunk doit être mis à jour.
        
        Args:
            chunk: Chunk à vérifier
            current_time: Temps actuel
            
        Returns:
            True si le chunk doit être mis à jour
        """
        update_frequency = self.lod_config[chunk.lod_level]['update_frequency']
        return (current_time - chunk.last_update) >= update_frequency
    
    def create_chunk(self, chunk_x: int, chunk_y: int, lod_level: LODLevel) -> LODChunk:
        """
        Crée un nouveau chunk avec le niveau LOD spécifié.
        
        Args:
            chunk_x, chunk_y: Coordonnées du chunk
            lod_level: Niveau LOD
            
        Returns:
            Nouveau chunk LOD
        """
        resolution = self.get_chunk_resolution(lod_level)
        
        # Calculer la distance à la caméra
        chunk_center_x = (chunk_x + 0.5) * self.chunk_size
        chunk_center_y = (chunk_y + 0.5) * self.chunk_size
        distance = np.sqrt(
            (chunk_center_x - self.camera_position[0])**2 +
            (chunk_center_y - self.camera_position[1])**2
        )
        
        return LODChunk(
            x=chunk_x,
            y=chunk_y,
            size=self.chunk_size,
            lod_level=lod_level,
            resolution=resolution,
            distance_to_camera=distance
        )
    
    def _update_chunk_lod_levels(self) -> None:
        """Met à jour les niveaux LOD de tous les chunks chargés."""
        chunks_to_update = []
        
        for (chunk_x, chunk_y), chunk in self.loaded_chunks.items():
            new_lod_level = self.determine_lod_level(chunk_x, chunk_y)
            
            if new_lod_level != chunk.lod_level:
                chunks_to_update.append((chunk_x, chunk_y, new_lod_level))
        
        # Mettre à jour les chunks qui ont changé de niveau LOD
        for chunk_x, chunk_y, new_lod_level in chunks_to_update:
            old_chunk = self.loaded_chunks[(chunk_x, chunk_y)]
            new_chunk = self.create_chunk(chunk_x, chunk_y, new_lod_level)
            new_chunk.is_loaded = False  # Marquer pour rechargement
            self.loaded_chunks[(chunk_x, chunk_y)] = new_chunk
    
    def unload_distant_chunks(self, max_distance: float = 20000.0) -> None:
        """
        Décharge les chunks trop éloignés pour libérer la mémoire.
        
        Args:
            max_distance: Distance maximale avant déchargement
        """
        chunks_to_unload = []
        
        for (chunk_x, chunk_y), chunk in self.loaded_chunks.items():
            if chunk.distance_to_camera > max_distance:
                chunks_to_unload.append((chunk_x, chunk_y))
        
        for chunk_coords in chunks_to_unload:
            del self.loaded_chunks[chunk_coords]
            self.stats['active_chunks'] -= 1
    
    def get_performance_stats(self) -> Dict:
        """
        Retourne les statistiques de performance du système LOD.
        
        Returns:
            Dictionnaire des statistiques
        """
        memory_usage = sum(
            chunk.heightmap.nbytes if chunk.heightmap is not None else 0
            for chunk in self.loaded_chunks.values()
        )
        
        lod_distribution = {}
        for lod_level in LODLevel:
            count = sum(1 for chunk in self.loaded_chunks.values() 
                       if chunk.lod_level == lod_level)
            lod_distribution[lod_level.name] = count
        
        return {
            'total_chunks': len(self.loaded_chunks),
            'memory_usage_mb': memory_usage / (1024 * 1024),
            'lod_distribution': lod_distribution,
            'camera_position': self.camera_position.tolist()
        }
    
    def optimize_for_performance(self) -> None:
        """
        Optimise le système LOD pour de meilleures performances.
        """
        # Décharger les chunks distants
        self.unload_distant_chunks()
        
        # Ajuster les niveaux LOD selon la charge système
        current_memory = self.get_performance_stats()['memory_usage_mb']
        
        if current_memory > 2000:  # Plus de 2GB
            # Réduire la qualité des chunks distants
            for chunk in self.loaded_chunks.values():
                if (chunk.distance_to_camera > 5000 and 
                    chunk.lod_level.value < LODLevel.LOW.value):
                    chunk.lod_level = LODLevel.LOW
                    chunk.resolution = self.get_chunk_resolution(LODLevel.LOW)
                    chunk.is_loaded = False  # Marquer pour rechargement
