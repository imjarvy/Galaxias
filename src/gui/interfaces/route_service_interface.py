"""
Interface for route service operations.
Implements Dependency Inversion Principle.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Dict, Any
from ...core import Star


class IRouteService(ABC):
    """Interface for route calculation services."""
    
    @abstractmethod
    def calculate_optimal_route(self, start: Star, end: Star) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate optimal route between two stars."""
        pass
    
    @abstractmethod
    def calculate_eating_route(self, start_id: str) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate route optimized for star eating."""
        pass
    
    @abstractmethod
    def calculate_max_visit_route(self, start: Star) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate route that maximizes star visits."""
        pass
    
    @abstractmethod
    def calculate_min_cost_route(self, start: Star, research_params=None) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate minimum cost route."""
        pass
    
    @abstractmethod
    def calculate_path_stats(self, path: List[Star]) -> Dict[str, Any]:
        """Calculate statistics for a given path."""
        pass