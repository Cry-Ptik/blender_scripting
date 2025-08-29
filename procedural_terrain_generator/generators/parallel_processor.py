"""
Parallel processing system for terrain generation.
Handles multi-threaded terrain generation with load balancing and progress tracking.
"""

import time
import threading
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Any, Tuple, Callable, Optional
from dataclasses import dataclass
from enum import Enum
import queue

# Add parent directory to path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TerrainConfig


class TaskStatus(Enum):
    """Status of terrain generation tasks."""
    PENDING = 0
    RUNNING = 1
    COMPLETED = 2
    FAILED = 3


@dataclass
class TerrainTask:
    """Represents a terrain generation task."""
    task_id: str
    tile_x: int
    tile_y: int
    detail_level: str
    priority: float
    status: TaskStatus = TaskStatus.PENDING
    start_time: Optional[float] = None
    completion_time: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None


class ParallelProcessor:
    """
    Manages parallel terrain generation with load balancing and progress tracking.
    """
    
    def __init__(self, config, terrain_generator):
        """
        Initialize parallel processor.
        
        Args:
            config: Terrain configuration object
            terrain_generator: Terrain generator instance
        """
        self.config = config
        self.terrain_generator = terrain_generator
        
        # Threading configuration
        self.max_workers = config.MAX_WORKERS
        self.parallel_processing = config.PARALLEL_PROCESSING
        
        # Task management
        self.task_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.completed_tasks: Dict[str, TerrainTask] = {}
        self.failed_tasks: Dict[str, TerrainTask] = {}
        
        # Progress tracking
        self.total_tasks = 0
        self.completed_count = 0
        self.failed_count = 0
        self.start_time = 0.0
        
        # Performance metrics
        self.task_times: List[float] = []
        self.throughput_history: List[float] = []
        
        # TODO: Add adaptive worker count based on performance
        # TODO: Implement task retry mechanism
    
    def generate_world_parallel(self, tile_tasks: List[Tuple[int, int, str]]) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """
        Generate terrain world using parallel processing.
        
        Args:
            tile_tasks: List of (tile_x, tile_y, detail_level) tuples
            
        Returns:
            Dictionary of generated tile data
            
        TODO: Port generate_world_parallel method from original script
        TODO: Add dynamic load balancing
        """
        print(f"🌍 Génération parallèle avec {self.max_workers} workers")
        
        # Initialize progress tracking
        self.total_tasks = len(tile_tasks)
        self.completed_count = 0
        self.failed_count = 0
        self.start_time = time.time()
        
        # Create terrain tasks
        tasks = []
        for i, (tile_x, tile_y, detail_level) in enumerate(tile_tasks):
            task = TerrainTask(
                task_id=f"tile_{tile_x}_{tile_y}_{detail_level}",
                tile_x=tile_x,
                tile_y=tile_y,
                detail_level=detail_level,
                priority=self._calculate_task_priority(tile_x, tile_y)
            )
            tasks.append(task)
        
        # Execute tasks
        if self.parallel_processing:
            results = self._execute_parallel(tasks)
        else:
            results = self._execute_sequential(tasks)
        
        # Generate performance report
        self._generate_performance_report()
        
        return results
    
    def _calculate_task_priority(self, tile_x: int, tile_y: int) -> float:
        """
        Calculate task priority based on tile position.
        
        Args:
            tile_x, tile_y: Tile coordinates
            
        Returns:
            Priority value (higher = more important)
            
        TODO: Add distance-based priority calculation
        TODO: Implement user-defined priority zones
        """
        # Center tiles have higher priority
        center = self.config.TILES_COUNT // 2
        distance = abs(tile_x - center) + abs(tile_y - center)
        return 1.0 / (distance + 1.0)
    
    def _execute_parallel(self, tasks: List[TerrainTask]) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """
        Execute tasks using parallel processing.
        
        Args:
            tasks: List of terrain tasks
            
        Returns:
            Dictionary of results
            
        TODO: Add progress reporting during execution
        TODO: Implement task failure recovery
        """
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._execute_single_task, task): task 
                for task in tasks
            }
            
            # Process completed tasks
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                
                try:
                    result = future.result()
                    task.status = TaskStatus.COMPLETED
                    task.completion_time = time.time()
                    task.result = result
                    
                    # Store result
                    tile_key = (task.tile_x, task.tile_y)
                    results[tile_key] = result
                    
                    self.completed_tasks[task.task_id] = task
                    self.completed_count += 1
                    
                    # Update progress
                    self._update_progress()
                    
                except Exception as exc:
                    task.status = TaskStatus.FAILED
                    task.error = str(exc)
                    self.failed_tasks[task.task_id] = task
                    self.failed_count += 1
                    
                    print(f"❌ Task {task.task_id} failed: {exc}")
        
        return results
    
    def _execute_sequential(self, tasks: List[TerrainTask]) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """
        Execute tasks sequentially (for debugging).
        
        Args:
            tasks: List of terrain tasks
            
        Returns:
            Dictionary of results
            
        TODO: Add sequential execution with progress tracking
        """
        results = {}
        
        for task in tasks:
            try:
                result = self._execute_single_task(task)
                task.status = TaskStatus.COMPLETED
                task.completion_time = time.time()
                task.result = result
                
                tile_key = (task.tile_x, task.tile_y)
                results[tile_key] = result
                
                self.completed_tasks[task.task_id] = task
                self.completed_count += 1
                
                self._update_progress()
                
            except Exception as exc:
                task.status = TaskStatus.FAILED
                task.error = str(exc)
                self.failed_tasks[task.task_id] = task
                self.failed_count += 1
                
                print(f"❌ Task {task.task_id} failed: {exc}")
        
        return results
    
    def _execute_single_task(self, task: TerrainTask) -> Dict[str, Any]:
        """
        Execute a single terrain generation task.
        
        Args:
            task: Task to execute
            
        Returns:
            Generated terrain data
            
        TODO: Add task execution timing
        TODO: Implement task caching integration
        """
        task.status = TaskStatus.RUNNING
        task.start_time = time.time()
        
        # Generate terrain tile
        result = self.terrain_generator.generate_single_tile(
            (task.tile_x, task.tile_y, task.detail_level)
        )
        
        # Record task timing
        execution_time = time.time() - task.start_time
        self.task_times.append(execution_time)
        
        return result
    
    def _update_progress(self) -> None:
        """
        Update and display generation progress.
        
        TODO: Add ETA calculation
        TODO: Implement progress callbacks
        """
        if self.completed_count % 10 == 0:
            progress = (self.completed_count / self.total_tasks) * 100
            elapsed = time.time() - self.start_time
            
            if self.completed_count > 0:
                avg_time_per_task = elapsed / self.completed_count
                eta = avg_time_per_task * (self.total_tasks - self.completed_count)
                
                print(f"⏳ Progression: {progress:.1f}% ({self.completed_count}/{self.total_tasks}) "
                      f"ETA: {eta:.1f}s")
    
    def _generate_performance_report(self) -> None:
        """
        Generate performance report after completion.
        
        TODO: Add detailed performance analysis
        TODO: Export performance data for optimization
        """
        total_time = time.time() - self.start_time
        
        if self.task_times:
            avg_task_time = sum(self.task_times) / len(self.task_times)
            throughput = self.completed_count / total_time
        else:
            avg_task_time = 0
            throughput = 0
        
        print(f"✅ Génération terminée en {total_time:.2f}s")
        print(f"⚡ Performance: {throughput:.1f} tuiles/seconde")
        print(f"📊 Temps moyen par tuile: {avg_task_time:.3f}s")
        
        if self.failed_count > 0:
            print(f"⚠️ Échecs: {self.failed_count}/{self.total_tasks}")
    
    def get_performance_statistics(self) -> Dict[str, Any]:
        """
        Get detailed performance statistics.
        
        Returns:
            Dictionary containing performance metrics
            
        TODO: Add memory usage statistics
        TODO: Include worker efficiency metrics
        """
        total_time = time.time() - self.start_time if self.start_time > 0 else 0
        
        stats = {
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_count,
            'failed_tasks': self.failed_count,
            'success_rate': self.completed_count / max(1, self.total_tasks),
            'total_time_seconds': total_time,
            'throughput_tasks_per_second': self.completed_count / max(1, total_time),
            'max_workers': self.max_workers,
            'parallel_processing': self.parallel_processing
        }
        
        if self.task_times:
            stats.update({
                'average_task_time': sum(self.task_times) / len(self.task_times),
                'min_task_time': min(self.task_times),
                'max_task_time': max(self.task_times),
                'task_time_std': self._calculate_std(self.task_times)
            })
        
        return stats
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation of values."""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def optimize_worker_count(self) -> int:
        """
        Optimize worker count based on performance history.
        
        Returns:
            Recommended worker count
            
        TODO: Implement adaptive worker count optimization
        TODO: Add hardware capability detection
        """
        # Simple optimization based on CPU count and performance
        import os
        cpu_count = os.cpu_count() or 4
        
        # Start with CPU count, but consider performance history
        if len(self.throughput_history) > 3:
            # If throughput is decreasing, reduce workers
            recent_throughput = self.throughput_history[-3:]
            if all(recent_throughput[i] > recent_throughput[i+1] for i in range(len(recent_throughput)-1)):
                return max(1, self.max_workers - 1)
        
        return min(cpu_count, self.max_workers + 1)
    
    def retry_failed_tasks(self) -> Dict[Tuple[int, int], Dict[str, Any]]:
        """
        Retry failed tasks.
        
        Returns:
            Results from retried tasks
            
        TODO: Implement intelligent retry with backoff
        TODO: Add failure analysis and recovery
        """
        if not self.failed_tasks:
            return {}
        
        print(f"🔄 Retry de {len(self.failed_tasks)} tâches échouées...")
        
        # Convert failed tasks back to task list
        retry_tasks = []
        for task in self.failed_tasks.values():
            # Reset task status
            task.status = TaskStatus.PENDING
            task.start_time = None
            task.completion_time = None
            task.error = None
            retry_tasks.append(task)
        
        # Clear failed tasks
        self.failed_tasks.clear()
        
        # Execute retry
        if self.parallel_processing:
            return self._execute_parallel(retry_tasks)
        else:
            return self._execute_sequential(retry_tasks)
