"""
Main entry point for the Procedural Terrain Generator.
Supports both programmatic usage and CLI interface.
"""

import sys
import os
from typing import Optional

# Add the project root to Python path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# CLI imports
try:
    from cli import app as cli_app
    CLI_AVAILABLE = True
except ImportError:
    CLI_AVAILABLE = False
    print("CLI non disponible. Installez 'typer' pour utiliser l'interface en ligne de commande.")

# Original imports for programmatic usage
from config import TerrainConfig, PerformanceProfile
from generators import WorldGenerator
from core import OptimizedNoise, GeologicalSystem
from runtime import MemoryManager


def create_optimized_config() -> TerrainConfig:
    """
    Create optimized configuration based on system capabilities.
    
    Returns:
        Optimized terrain configuration
    """
    # Start with default configuration
    config = TerrainConfig()
    
    # Adjust based on available CPU cores
    import os
    cpu_count = os.cpu_count() or 4
    config.MAX_WORKERS = min(8, cpu_count)
    
    # Optimize for development/testing (smaller world)
    config.WORLD_SIZE = 4000  # 4km x 4km for faster generation
    config.USE_CACHE = True
    config.PARALLEL_PROCESSING = True
    
    return config


def generate_full_world(config: Optional[TerrainConfig] = None) -> dict:
    """Generate a complete procedural world."""
    if config is None:
        config = create_optimized_config()
    
    generator = WorldGenerator(config)
    return generator.generate_complete_world()


def generate_preview(center_x: int = None, center_y: int = None, 
                    radius: int = 2, config: Optional[TerrainConfig] = None) -> dict:
    """Generate a small preview area for testing."""
    if config is None:
        config = create_optimized_config()
    
    if center_x is None:
        center_x = config.TILES_COUNT // 2
    if center_y is None:
        center_y = config.TILES_COUNT // 2
    
    generator = WorldGenerator(config)
    return generator.generate_preview_area(center_x, center_y, radius)


def main():
    """
    Main function - routes to CLI or programmatic demo based on arguments.
    """
    # If CLI is available and arguments are provided, use CLI
    if CLI_AVAILABLE and len(sys.argv) > 1:
        cli_app()
    else:
        # Fallback to programmatic demo
        print("🌍 GÉNÉRATEUR DE TERRAIN PROCÉDURAL")
        print("Architecture modulaire pour Blender et Godot")
        print("="*60)
        
        if not CLI_AVAILABLE:
            print("Pour utiliser la CLI, installez: pip install typer rich")
            print("Puis utilisez: python main.py generate terrain --help")
        
        print("\nMode démonstration programmatique...")
        
        try:
            # Quick preview generation
            print("\nGénération preview rapide...")
            preview_results = generate_preview(radius=1)
            
            if preview_results:
                print(f"Preview généré: {preview_results['tile_count']} tuiles")
                print(f"Temps: {preview_results['generation_time']:.2f}s")
            
            print("\n" + "="*60)
            print("DÉMONSTRATION TERMINÉE!")
            print("\nUtilisation CLI disponible:")
            print("python main.py generate terrain --seed 123 --size 4000")
            print("python main.py export godot --output ./my_project")
            print("python main.py optimize scene --level high")
            
        except Exception as e:
            print(f"\n ERREUR: {e}")
            return 1
    
    return 0


if __name__ == "__main__":
    """
    Entry point when script is run directly.
    
    CLI Usage examples:
    - python main.py generate terrain --seed 123 --size 1024
    - python main.py generate heightmap --size 2048 --format png
    - python main.py export godot --output ./godot_project
    - python main.py optimize scene --level high --render
    - python main.py generate info
    """
    exit_code = main()
    sys.exit(exit_code)