"""
Galaxias - Sistema Interactivo de Rutas Espaciales

Módulos principales:
- models: Clases de datos (Star, Route, SpaceshipDonkey, SpaceMap)
- route_calculator: Algoritmos de cálculo de rutas (Dijkstra)
- visualizer: Visualizaciones con matplotlib
- gui: Interfaz gráfica con tkinter
"""

__version__ = "1.0.0"
__author__ = "imjarvy"

from src.models import Star, Route, SpaceshipDonkey, Comet, SpaceMap
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer

__all__ = [
    'Star',
    'Route', 
    'SpaceshipDonkey',
    'Comet',
    'SpaceMap',
    'RouteCalculator',
    'SpaceVisualizer'
]
