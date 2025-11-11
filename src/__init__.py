"""
🌌 Sistema de Navegación Galaxias - Arquitectura Limpia
======================================================

Arquitectura SOLID con separación clara de responsabilidades:

CORE DOMAIN:
- core/: Entidades fundamentales (Star, Route, BurroAstronauta, SpaceMap)
- algorithms/: Algoritmos de cálculo (RouteCalculator, HyperGiantJumpSystem)  
- presentation/: Visualización (SpaceVisualizer, LifeMonitor)
- utils/: Utilidades compartidas (JSONHandler, Validators)

PRESENTATION LAYER:
- gui/: Interfaz gráfica modular siguiendo principios SOLID

PUBLIC API:
Exposición limpia de las funcionalidades principales del sistema.
"""

__version__ = "2.0.0"
__author__ = "imjarvy"

# Core Domain
from .core import Star, Route, BurroAstronauta, SpaceMap

# Algorithms
from .algorithms import RouteCalculator, HyperGiantJumpSystem

# Presentation  
from .presentation import SpaceVisualizer, LifeMonitor

# GUI (Main Entry Point)
from .gui import main as gui_main

# Utilities
from .utils import JSONHandler, Validators, ValidationError

__all__ = [
    # Core Models
    'Star',
    'Route', 
    'BurroAstronauta',
    'SpaceMap',
    
    # Algorithms
    'RouteCalculator',
    'HyperGiantJumpSystem',
    
    # Presentation
    'SpaceVisualizer',
    'LifeMonitor',
    
    # Utilities
    'JSONHandler',
    'Validators',
    'ValidationError',
    
    # Main entry point
    'gui_main'
]

def main():
    """Punto de entrada principal de la aplicación."""
    return gui_main()

def create_galaxy():
    """Factory method para crear una nueva galaxia."""
    return SpaceMap()

def calculate_route(start, goal, galaxy=None):
    """Método de conveniencia para calcular rutas."""
    if galaxy is None:
        galaxy = create_galaxy()
    calculator = RouteCalculator(galaxy)
    return calculator.find_shortest_path(start, goal)
