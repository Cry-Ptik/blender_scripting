"""
Système de biomes réaliste basé sur altitude, climat et conditions géologiques.
Génère des zones écologiques distinctes pour terrain procédural ultra-réaliste.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class BiomeType(Enum):
    """Types de biomes disponibles."""
    OCEAN = "ocean"
    BEACH = "beach"
    PLAINS = "plains"
    FOREST = "forest"
    HILLS = "hills"
    MOUNTAINS = "mountains"
    ALPINE = "alpine"
    SNOW = "snow"
    DESERT = "desert"
    SWAMP = "swamp"
    TUNDRA = "tundra"


@dataclass
class BiomeProperties:
    """Propriétés d'un biome."""
    name: str
    min_elevation: float
    max_elevation: float
    min_temperature: float
    max_temperature: float
    min_humidity: float
    max_humidity: float
    vegetation_density: float
    rock_exposure: float
    soil_type: str
    color_base: Tuple[float, float, float]
    color_variation: float


class BiomeSystem:
    """
    Système de biomes avancé pour génération de terrain réaliste.
    Détermine les biomes basés sur altitude, température, humidité et géologie.
    """
    
    def __init__(self, world_size: int, sea_level: float = 0.0):
        """
        Initialize biome system.
        
        Args:
            world_size: Size of the world
            sea_level: Sea level elevation
        """
        self.world_size = world_size
        self.sea_level = sea_level
        self.temperature_scale = 1.0
        self.humidity_scale = 1.0
        
        # Initialize biome definitions
        self.biome_definitions = self._create_biome_definitions()
    
    def _create_biome_definitions(self) -> Dict[BiomeType, BiomeProperties]:
        """Create biome definitions with properties."""
        return {
            BiomeType.OCEAN: BiomeProperties(
                name="Ocean",
                min_elevation=-1000.0, max_elevation=0.0,
                min_temperature=0.0, max_temperature=30.0,
                min_humidity=1.0, max_humidity=1.0,
                vegetation_density=0.0, rock_exposure=0.0,
                soil_type="sand", color_base=(0.1, 0.3, 0.6),
                color_variation=0.1
            ),
            BiomeType.BEACH: BiomeProperties(
                name="Beach",
                min_elevation=0.0, max_elevation=10.0,
                min_temperature=15.0, max_temperature=35.0,
                min_humidity=0.6, max_humidity=1.0,
                vegetation_density=0.1, rock_exposure=0.2,
                soil_type="sand", color_base=(0.9, 0.8, 0.6),
                color_variation=0.15
            ),
            BiomeType.PLAINS: BiomeProperties(
                name="Plains",
                min_elevation=10.0, max_elevation=200.0,
                min_temperature=10.0, max_temperature=30.0,
                min_humidity=0.3, max_humidity=0.8,
                vegetation_density=0.6, rock_exposure=0.1,
                soil_type="loam", color_base=(0.4, 0.6, 0.2),
                color_variation=0.2
            ),
            BiomeType.FOREST: BiomeProperties(
                name="Forest",
                min_elevation=50.0, max_elevation=800.0,
                min_temperature=5.0, max_temperature=25.0,
                min_humidity=0.6, max_humidity=1.0,
                vegetation_density=0.9, rock_exposure=0.05,
                soil_type="humus", color_base=(0.2, 0.5, 0.1),
                color_variation=0.25
            ),
            BiomeType.HILLS: BiomeProperties(
                name="Hills",
                min_elevation=200.0, max_elevation=600.0,
                min_temperature=5.0, max_temperature=20.0,
                min_humidity=0.4, max_humidity=0.8,
                vegetation_density=0.5, rock_exposure=0.3,
                soil_type="clay", color_base=(0.5, 0.4, 0.2),
                color_variation=0.3
            ),
            BiomeType.MOUNTAINS: BiomeProperties(
                name="Mountains",
                min_elevation=600.0, max_elevation=2000.0,
                min_temperature=-5.0, max_temperature=15.0,
                min_humidity=0.3, max_humidity=0.7,
                vegetation_density=0.2, rock_exposure=0.7,
                soil_type="rock", color_base=(0.6, 0.5, 0.4),
                color_variation=0.2
            ),
            BiomeType.ALPINE: BiomeProperties(
                name="Alpine",
                min_elevation=2000.0, max_elevation=3500.0,
                min_temperature=-15.0, max_temperature=5.0,
                min_humidity=0.2, max_humidity=0.6,
                vegetation_density=0.1, rock_exposure=0.8,
                soil_type="rock", color_base=(0.7, 0.6, 0.5),
                color_variation=0.15
            ),
            BiomeType.SNOW: BiomeProperties(
                name="Snow",
                min_elevation=3500.0, max_elevation=10000.0,
                min_temperature=-30.0, max_temperature=-5.0,
                min_humidity=0.1, max_humidity=0.5,
                vegetation_density=0.0, rock_exposure=0.9,
                soil_type="rock", color_base=(0.9, 0.9, 1.0),
                color_variation=0.05
            ),
            BiomeType.DESERT: BiomeProperties(
                name="Desert",
                min_elevation=0.0, max_elevation=1000.0,
                min_temperature=20.0, max_temperature=50.0,
                min_humidity=0.0, max_humidity=0.2,
                vegetation_density=0.05, rock_exposure=0.4,
                soil_type="sand", color_base=(0.8, 0.7, 0.4),
                color_variation=0.2
            ),
            BiomeType.TUNDRA: BiomeProperties(
                name="Tundra",
                min_elevation=0.0, max_elevation=500.0,
                min_temperature=-20.0, max_temperature=5.0,
                min_humidity=0.3, max_humidity=0.8,
                vegetation_density=0.2, rock_exposure=0.3,
                soil_type="permafrost", color_base=(0.4, 0.5, 0.3),
                color_variation=0.2
            )
        }
    
    def calculate_climate(self, x: np.ndarray, y: np.ndarray, elevation: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Calcule les conditions climatiques basées sur position et altitude.
        
        Args:
            x, y: Coordonnées normalisées
            elevation: Élévation du terrain
            
        Returns:
            Dictionnaire contenant température et humidité
        """
        # Température basée sur latitude et altitude
        # Plus froid vers les pôles et en altitude
        latitude_factor = np.abs(y - 0.5) * 2  # 0 à l'équateur, 1 aux pôles
        altitude_factor = np.clip(elevation / 1000.0, 0, 5)  # Facteur d'altitude
        
        base_temperature = 30.0 - (latitude_factor * 40.0) - (altitude_factor * 6.5)  # Gradient thermique
        
        # Variation saisonnière et locale
        temperature_noise = np.sin(x * np.pi * 4) * np.cos(y * np.pi * 3) * 5.0
        temperature = base_temperature + temperature_noise
        
        # Humidité basée sur distance aux océans et élévation
        # Plus humide près des côtes, plus sec en altitude
        center_distance = np.sqrt((x - 0.5)**2 + (y - 0.5)**2)
        coastal_humidity = 1.0 - np.clip(center_distance * 2, 0, 1)
        altitude_humidity = np.clip(1.0 - elevation / 2000.0, 0, 1)
        
        # Effet orographique - plus humide au vent des montagnes
        humidity_noise = np.sin(x * np.pi * 6) * np.cos(y * np.pi * 4) * 0.3
        humidity = (coastal_humidity * 0.6 + altitude_humidity * 0.4) + humidity_noise
        humidity = np.clip(humidity, 0, 1)
        
        return {
            'temperature': temperature,
            'humidity': humidity
        }
    
    def determine_biomes(self, x: np.ndarray, y: np.ndarray, elevation: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Détermine les biomes pour chaque point du terrain.
        
        Args:
            x, y: Coordonnées normalisées
            elevation: Élévation du terrain
            
        Returns:
            Dictionnaire avec types de biomes et propriétés
        """
        climate = self.calculate_climate(x, y, elevation)
        temperature = climate['temperature']
        humidity = climate['humidity']
        
        # Initialiser les cartes de biomes
        biome_map = np.full(elevation.shape, BiomeType.PLAINS.value, dtype=object)
        vegetation_density = np.zeros_like(elevation)
        rock_exposure = np.zeros_like(elevation)
        
        # Déterminer le biome pour chaque point
        for i in range(elevation.shape[0]):
            for j in range(elevation.shape[1]):
                elev = elevation[i, j]
                temp = temperature[i, j]
                humid = humidity[i, j]
                
                best_biome = self._find_best_biome(elev, temp, humid)
                biome_map[i, j] = best_biome.value
                
                biome_props = self.biomes[best_biome]
                vegetation_density[i, j] = biome_props.vegetation_density
                rock_exposure[i, j] = biome_props.rock_exposure
        
        return {
            'biome_map': biome_map,
            'vegetation_density': vegetation_density,
            'rock_exposure': rock_exposure,
            'temperature': temperature,
            'humidity': humidity
        }
    
    def _find_best_biome(self, elevation: float, temperature: float, humidity: float) -> BiomeType:
        """
        Trouve le meilleur biome pour des conditions données.
        
        Args:
            elevation: Élévation
            temperature: Température
            humidity: Humidité
            
        Returns:
            Type de biome le plus approprié
        """
        best_score = -1
        best_biome = BiomeType.PLAINS
        
        for biome_type, props in self.biomes.items():
            score = self._calculate_biome_score(elevation, temperature, humidity, props)
            if score > best_score:
                best_score = score
                best_biome = biome_type
        
        return best_biome
    
    def _calculate_biome_score(self, elevation: float, temperature: float, 
                              humidity: float, props: BiomeProperties) -> float:
        """
        Calcule le score d'adéquation pour un biome.
        
        Args:
            elevation: Élévation
            temperature: Température
            humidity: Humidité
            props: Propriétés du biome
            
        Returns:
            Score d'adéquation (plus élevé = meilleur)
        """
        score = 0.0
        
        # Score d'élévation
        if props.min_elevation <= elevation <= props.max_elevation:
            elev_range = props.max_elevation - props.min_elevation
            elev_center = (props.min_elevation + props.max_elevation) / 2
            elev_score = 1.0 - abs(elevation - elev_center) / (elev_range / 2)
            score += elev_score * 0.4
        
        # Score de température
        if props.min_temperature <= temperature <= props.max_temperature:
            temp_range = props.max_temperature - props.min_temperature
            temp_center = (props.min_temperature + props.max_temperature) / 2
            temp_score = 1.0 - abs(temperature - temp_center) / (temp_range / 2)
            score += temp_score * 0.3
        
        # Score d'humidité
        if props.min_humidity <= humidity <= props.max_humidity:
            humid_range = props.max_humidity - props.min_humidity
            humid_center = (props.min_humidity + props.max_humidity) / 2
            humid_score = 1.0 - abs(humidity - humid_center) / (humid_range / 2)
            score += humid_score * 0.3
        
        return score
    
    def get_biome_colors(self, biome_map: np.ndarray) -> np.ndarray:
        """
        Génère les couleurs pour chaque biome.
        
        Args:
            biome_map: Carte des biomes
            
        Returns:
            Array RGB des couleurs
        """
        colors = np.zeros((*biome_map.shape, 3))
        
        for i in range(biome_map.shape[0]):
            for j in range(biome_map.shape[1]):
                biome_name = biome_map[i, j]
                biome_type = BiomeType(biome_name)
                props = self.biomes[biome_type]
                
                # Couleur de base avec variation
                base_color = np.array(props.color_base)
                variation = (np.random.random(3) - 0.5) * props.color_variation
                final_color = np.clip(base_color + variation, 0, 1)
                
                colors[i, j] = final_color
        
        return colors
