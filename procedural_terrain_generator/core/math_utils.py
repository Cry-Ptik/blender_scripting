"""
Mathematical utilities for procedural terrain generation.
Vectorized operations and geometric calculations optimized for large datasets.
"""

import numpy as np
from typing import Tuple, Union, List
import math

# Import numba optionally for performance optimization
try:
    from numba import jit, vectorize
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False
    # Create dummy decorators when numba is not available
    def jit(*args, **kwargs):
        def decorator(func):
            return func
        return decorator if args else decorator
    
    def vectorize(*args, **kwargs):
        def decorator(func):
            return func
        return decorator if args else decorator


class MountainRange:
    """
    Represents a mountain range with geological properties.
    """
    
    def __init__(self, center_x: float, center_y: float, length: float, 
                 width: float, height: float, orientation: float):
        """
        Initialize mountain range.
        
        Args:
            center_x, center_y: Center coordinates
            length: Length of the mountain range
            width: Width of the mountain range
            height: Maximum height
            orientation: Orientation angle in radians
        """
        self.center_x = center_x
        self.center_y = center_y
        self.length = length
        self.width = width
        self.height = height
        self.orientation = orientation


class MountainSystem:
    """
    Manages mountain range generation and evolution.
    Moved from geology.py to resolve import conflicts.
    """
    
    def __init__(self, world_size: float, noise_generator):
        """
        Initialize mountain system.
        
        Args:
            world_size: Size of the world in meters
            noise_generator: Noise generator for mountain variation
        """
        self.world_size = world_size
        self.noise_generator = noise_generator
        self.mountain_ranges: List[MountainRange] = []
        self.height_scale = 1.0
        self.target_range_count = 4
        
    def generate_mountain_ranges(self) -> List[MountainRange]:
        """
        Generate realistic mountain range systems.
        
        Returns:
            List of mountain ranges
        """
        # Generate mountain ranges based on target count
        num_ranges = self.target_range_count
        ranges = []
        
        for i in range(num_ranges):
            # Random position within world bounds
            center_x = np.random.uniform(0.1 * self.world_size, 0.9 * self.world_size)
            center_y = np.random.uniform(0.1 * self.world_size, 0.9 * self.world_size)
            
            # Range properties
            length = np.random.uniform(0.2 * self.world_size, 0.6 * self.world_size)
            width = np.random.uniform(0.05 * self.world_size, 0.15 * self.world_size)
            height = np.random.uniform(1000, 4000)  # meters
            orientation = np.random.uniform(0, 2 * np.pi)
            
            # Create mountain range
            mountain_range = MountainRange(
                center_x=center_x,
                center_y=center_y,
                length=length,
                width=width,
                height=height,
                orientation=orientation
            )
            ranges.append(mountain_range)
        
        self.mountain_ranges = ranges
        return ranges
    
    def calculate_mountain_elevation(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Calculate mountain elevation at given coordinates.
        
        Args:
            x, y: Coordinate arrays
            
        Returns:
            Elevation array
        """
        if not self.mountain_ranges:
            self.generate_mountain_ranges()
        
        elevation = np.zeros_like(x, dtype=np.float64)
        
        for mountain_range in self.mountain_ranges:
            # Calculate relative position to mountain center
            dx = x - mountain_range.center_x
            dy = y - mountain_range.center_y
            
            # Rotate coordinates based on mountain orientation
            cos_angle = np.cos(-mountain_range.orientation)
            sin_angle = np.sin(-mountain_range.orientation)
            local_x = dx * cos_angle - dy * sin_angle
            local_y = dx * sin_angle + dy * cos_angle
            
            # Calculate distance from mountain axis
            axis_distance = np.abs(local_y)
            along_axis = np.abs(local_x)
            
            # Mountain profile using smooth falloff
            width_factor = np.maximum(0, 1.0 - axis_distance / (mountain_range.width / 2))
            length_factor = np.maximum(0, 1.0 - along_axis / (mountain_range.length / 2))
            
            # Apply smooth falloff
            width_factor = width_factor ** 2
            length_factor = length_factor ** 2
            
            # Add noise variation
            noise_scale = 0.001  # Adjust for detail level
            noise_value = self.noise_generator.generate_noise(x * noise_scale, y * noise_scale)
            noise_factor = 1.0 + 0.3 * noise_value  # 30% variation
            
            # Calculate final elevation contribution
            mountain_elevation = (mountain_range.height * width_factor * 
                                length_factor * noise_factor * self.height_scale)
            
            elevation += mountain_elevation
        
        return elevation
    
    def calculate_elevation(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """
        Calculate mountain elevation at given coordinates (alias for backward compatibility).
        
        Args:
            x, y: Coordinate arrays
            
        Returns:
            Elevation array
        """
        return self.calculate_mountain_elevation(x, y)


class VectorizedOperations:
    """
    Collection of vectorized mathematical operations for terrain generation.
    All methods are optimized for NumPy arrays and large-scale computations.
    """
    
    @staticmethod
    def point_to_segment_distance(points_x: np.ndarray, points_y: np.ndarray,
                                 seg_start_x: float, seg_start_y: float,
                                 seg_end_x: float, seg_end_y: float) -> np.ndarray:
        """
        Calculate vectorized distance from points to line segment.
        
        Args:
            points_x, points_y: Arrays of point coordinates
            seg_start_x, seg_start_y: Segment start coordinates
            seg_end_x, seg_end_y: Segment end coordinates
            
        Returns:
            Array of distances from each point to the segment
            
        TODO: Port the point_to_segment_distance_vectorized method from original script
        TODO: Optimize for memory usage with very large point arrays
        """
        # Segment vector
        seg_len_sq = (seg_end_x - seg_start_x)**2 + (seg_end_y - seg_start_y)**2
        
        if seg_len_sq == 0:
            return np.sqrt((points_x - seg_start_x)**2 + (points_y - seg_start_y)**2)
        
        # Project points onto segment
        t = np.maximum(0, np.minimum(1, 
            ((points_x - seg_start_x) * (seg_end_x - seg_start_x) + 
             (points_y - seg_start_y) * (seg_end_y - seg_start_y)) / seg_len_sq))
        
        # Closest point on segment
        proj_x = seg_start_x + t * (seg_end_x - seg_start_x)
        proj_y = seg_start_y + t * (seg_end_y - seg_start_y)
        
        return np.sqrt((points_x - proj_x)**2 + (points_y - proj_y)**2)
    
    @staticmethod
    def distance_field_2d(x: np.ndarray, y: np.ndarray, 
                         center_x: float, center_y: float) -> np.ndarray:
        """
        Calculate 2D distance field from a center point.
        
        Args:
            x, y: Coordinate arrays
            center_x, center_y: Center point coordinates
            
        Returns:
            Distance field array
            
        TODO: Add different distance metrics (Manhattan, Chebyshev)
        TODO: Optimize for GPU computation using CuPy
        """
        return np.sqrt((x - center_x)**2 + (y - center_y)**2)
    
    @staticmethod
    def smooth_step(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
        """
        Smooth step function for smooth transitions.
        
        Args:
            edge0: Lower edge of transition
            edge1: Upper edge of transition
            x: Input values
            
        Returns:
            Smoothly interpolated values between 0 and 1
            
        TODO: Add different smoothing functions (smootherstep, etc.)
        """
        t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return t * t * (3.0 - 2.0 * t)
    
    @staticmethod
    def remap_range(value: np.ndarray, old_min: float, old_max: float,
                   new_min: float, new_max: float) -> np.ndarray:
        """
        Remap values from one range to another.
        
        Args:
            value: Input values to remap
            old_min, old_max: Original range
            new_min, new_max: Target range
            
        Returns:
            Remapped values
            
        TODO: Add clamping option for out-of-range values
        TODO: Add different interpolation modes (linear, exponential, etc.)
        """
        old_range = old_max - old_min
        new_range = new_max - new_min
        
        if old_range == 0:
            return np.full_like(value, new_min)
        
        return (((value - old_min) * new_range) / old_range) + new_min
    
    @staticmethod
    def gradient_2d(elevation: np.ndarray, spacing: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate 2D gradient of elevation data.
        
        Args:
            elevation: 2D elevation array
            spacing: Grid spacing for gradient calculation
            
        Returns:
            Tuple of (gradient_x, gradient_y) arrays
            
        TODO: Add different gradient calculation methods (Sobel, Scharr)
        TODO: Optimize boundary handling
        """
        grad_y, grad_x = np.gradient(elevation, spacing)
        return grad_x, grad_y
    
    @staticmethod
    def slope_aspect(elevation: np.ndarray, spacing: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate slope and aspect from elevation data.
        
        Args:
            elevation: 2D elevation array
            spacing: Grid spacing
            
        Returns:
            Tuple of (slope, aspect) arrays in radians
            
        TODO: Add option to return degrees instead of radians
        TODO: Optimize for large elevation arrays
        """
        grad_x, grad_y = VectorizedOperations.gradient_2d(elevation, spacing)
        
        slope = np.arctan(np.sqrt(grad_x**2 + grad_y**2))
        aspect = np.arctan2(-grad_x, grad_y)
        
        return slope, aspect


class MathUtils:
    """
    General mathematical utilities for terrain generation.
    """
    
    @staticmethod
    def normalize_elevation(elevation: np.ndarray, target_min: float = 0.0, 
                          target_max: float = 1.0) -> np.ndarray:
        """
        Normalize elevation data to a target range.
        
        Args:
            elevation: Input elevation array
            target_min: Target minimum value
            target_max: Target maximum value
            
        Returns:
            Normalized elevation array
            
        TODO: Add different normalization methods (z-score, robust scaling)
        TODO: Handle edge cases (constant elevation, NaN values)
        """
        current_min = np.min(elevation)
        current_max = np.max(elevation)
        
        if current_max == current_min:
            return np.full_like(elevation, target_min)
        
        return VectorizedOperations.remap_range(
            elevation, current_min, current_max, target_min, target_max
        )
    
    @staticmethod
    def apply_falloff(values: np.ndarray, center_x: float, center_y: float,
                     x: np.ndarray, y: np.ndarray, radius: float,
                     falloff_type: str = "linear") -> np.ndarray:
        """
        Apply distance-based falloff to values.
        
        Args:
            values: Input values to modify
            center_x, center_y: Center of falloff
            x, y: Coordinate arrays
            radius: Falloff radius
            falloff_type: Type of falloff ("linear", "quadratic", "exponential")
            
        Returns:
            Values with falloff applied
            
        TODO: Implement different falloff functions
        TODO: Add custom falloff curve support
        """
        distance = VectorizedOperations.distance_field_2d(x, y, center_x, center_y)
        
        if falloff_type == "linear":
            falloff = np.maximum(0, 1.0 - distance / radius)
        elif falloff_type == "quadratic":
            falloff = np.maximum(0, (1.0 - distance / radius)**2)
        elif falloff_type == "exponential":
            falloff = np.exp(-distance / radius)
        else:
            falloff = np.ones_like(distance)
        
        return values * falloff
    
    @staticmethod
    def blend_layers(layer1: np.ndarray, layer2: np.ndarray, 
                    blend_mode: str = "add", factor: float = 1.0) -> np.ndarray:
        """
        Blend two terrain layers using different blend modes.
        
        Args:
            layer1: First layer
            layer2: Second layer
            blend_mode: Blending mode ("add", "multiply", "overlay", "max", "min")
            factor: Blending factor (0-1)
            
        Returns:
            Blended layer
            
        TODO: Implement more blend modes (screen, soft light, etc.)
        TODO: Add mask-based blending
        """
        layer2_scaled = layer2 * factor
        
        if blend_mode == "add":
            return layer1 + layer2_scaled
        elif blend_mode == "multiply":
            return layer1 * (1 + layer2_scaled)
        elif blend_mode == "overlay":
            return np.where(layer1 < 0.5,
                          2 * layer1 * layer2_scaled,
                          1 - 2 * (1 - layer1) * (1 - layer2_scaled))
        elif blend_mode == "max":
            return np.maximum(layer1, layer2_scaled)
        elif blend_mode == "min":
            return np.minimum(layer1, layer2_scaled)
        else:
            return layer1
    
    @staticmethod
    def calculate_curvature(elevation: np.ndarray, spacing: float = 1.0) -> np.ndarray:
        """
        Calculate surface curvature from elevation data.
        
        Args:
            elevation: 2D elevation array
            spacing: Grid spacing
            
        Returns:
            Curvature array (positive for convex, negative for concave)
            
        TODO: Implement different curvature types (mean, Gaussian, principal)
        TODO: Optimize for large arrays using sparse matrices
        """
        # Second derivatives
        d2_dx2 = np.gradient(np.gradient(elevation, spacing, axis=1), spacing, axis=1)
        d2_dy2 = np.gradient(np.gradient(elevation, spacing, axis=0), spacing, axis=0)
        d2_dxdy = np.gradient(np.gradient(elevation, spacing, axis=1), spacing, axis=0)
        
        # First derivatives
        dx, dy = VectorizedOperations.gradient_2d(elevation, spacing)
        
        # Mean curvature calculation
        numerator = (1 + dx**2) * d2_dy2 - 2 * dx * dy * d2_dxdy + (1 + dy**2) * d2_dx2
        denominator = 2 * (1 + dx**2 + dy**2)**(3/2)
        
        return -numerator / (denominator + 1e-8)  # Add small epsilon to avoid division by zero


class GeometricUtils:
    """
    Geometric utilities for terrain generation.
    """
    
    @staticmethod
    def generate_voronoi_cells(width: int, height: int, num_points: int, 
                              seed: int = 42) -> np.ndarray:
        """
        Generate Voronoi cell diagram for terrain regions.
        
        Args:
            width, height: Output dimensions
            num_points: Number of Voronoi seed points
            seed: Random seed
            
        Returns:
            2D array with Voronoi cell indices
            
        TODO: Implement efficient Voronoi calculation
        TODO: Add different distance metrics for cell shapes
        """
        np.random.seed(seed)
        
        # Generate random seed points
        points_x = np.random.uniform(0, width, num_points)
        points_y = np.random.uniform(0, height, num_points)
        
        # Create coordinate grids
        x, y = np.meshgrid(np.arange(width), np.arange(height))
        
        # Calculate distances to all points
        voronoi = np.zeros((height, width), dtype=np.int32)
        
        for i in range(num_points):
            dist = (x - points_x[i])**2 + (y - points_y[i])**2
            if i == 0:
                min_dist = dist
                voronoi = np.full_like(voronoi, i)
            else:
                mask = dist < min_dist
                voronoi[mask] = i
                min_dist = np.minimum(min_dist, dist)
        
        return voronoi
    
    @staticmethod
    def generate_delaunay_triangulation(points: np.ndarray) -> np.ndarray:
        """
        Generate Delaunay triangulation from points.
        
        Args:
            points: Array of 2D points (N x 2)
            
        Returns:
            Array of triangle indices
            
        TODO: Implement Delaunay triangulation algorithm
        TODO: Add constraint handling for terrain features
        """
        # Placeholder - would need scipy.spatial.Delaunay or custom implementation
        return np.array([])
    
    @staticmethod
    def calculate_mesh_normals(vertices: np.ndarray, faces: np.ndarray) -> np.ndarray:
        """
        Calculate vertex normals for a mesh.
        
        Args:
            vertices: Vertex positions (N x 3)
            faces: Face indices (M x 3)
            
        Returns:
            Vertex normals (N x 3)
            
        TODO: Implement efficient normal calculation
        TODO: Add weighted normals based on face area
        """
        normals = np.zeros_like(vertices)
        
        # TODO: Calculate face normals and accumulate to vertices
        # TODO: Normalize the resulting vertex normals
        
        return normals
