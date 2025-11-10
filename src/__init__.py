"""
Galaxias - Sistema del Burro Astronauta

Módulos principales:
- models: Clases de datos (Star, Route, BurroAstronauta, SpaceMap)
- route_calculator: Algoritmos de cálculo de rutas (Dijkstra)
- visualizer: Visualizaciones con matplotlib
- donkey_optimization: Optimización de rutas para el burro astronauta
- gui: Interfaz gráfica con tkinter
"""

__version__ = "2.0.0"
__author__ = "imjarvy"

from src.models import Star, Route, BurroAstronauta, Comet, SpaceMap
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer
from src.donkey_optimization import DonkeyRouteOptimizer

__all__ = [
    'Star',
    'Route', 
    'BurroAstronauta',
    'Comet',
    'SpaceMap',
    'RouteCalculator',
    'SpaceVisualizer',
    'DonkeyRouteOptimizer'
]
