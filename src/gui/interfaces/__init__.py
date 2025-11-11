"""
GUI Interfaces package for dependency inversion principle.
"""
from .route_service_interface import IRouteService
from .visualization_service_interface import IVisualizationService
from .component_interface import IComponent

__all__ = ['IRouteService', 'IVisualizationService', 'IComponent']