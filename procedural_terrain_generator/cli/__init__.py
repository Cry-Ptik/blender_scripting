"""
CLI package for procedural terrain generator.
Provides command-line interface for terrain generation operations.
"""

import typer
from .commands import generate_app, export_app, optimize_app

# Main CLI application
app = typer.Typer(
    name="terrain-generator",
    help="Générateur de Terrain Procédural - Interface en ligne de commande",
    add_completion=False,
    rich_markup_mode="rich"
)

# Add sub-applications
app.add_typer(generate_app, name="generate", help="Génération de terrain et heightmaps")
app.add_typer(export_app, name="export", help="Export vers moteurs externes")
app.add_typer(optimize_app, name="optimize", help="Optimisations Blender et performance")

__all__ = ['app', 'generate_app', 'export_app', 'optimize_app']