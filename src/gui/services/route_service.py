"""
Route service implementation.
Implements Single Responsibility Principle for route operations.
"""
from typing import List, Tuple, Optional, Dict, Any
from ...core import SpaceMap, Star, BurroAstronauta
from ...algorithms import RouteCalculator, DonkeyRouteOptimizer
from ..interfaces.route_service_interface import IRouteService


class RouteService(IRouteService):
    """Service responsible for route calculations."""
    
    def __init__(self, space_map: SpaceMap, config: dict):
        self.space_map = space_map
        self.config = config
        self.calculator = RouteCalculator(space_map, config)
        self.optimizer = DonkeyRouteOptimizer(space_map)
    
    def calculate_optimal_route(self, start: Star, end: Star) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate optimal route between two stars."""
        try:
            path, cost = self.calculator.dijkstra(start, end)
            
            if not path:
                return None, {"error": "No route found"}
            
            stats = self.calculator.calculate_path_stats(path)
            stats['cost'] = cost
            
            return path, stats
        except Exception as e:
            return None, {"error": str(e)}
    
    def calculate_eating_route(self, start_id: str) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate route optimized for star eating."""
        try:
            optimal_path, stats = self.optimizer.optimize_route_from_json_data(start_id)
            
            if stats.get('error'):
                return None, stats
            
            return optimal_path, stats
        except Exception as e:
            return None, {"error": str(e)}
    
    def calculate_max_visit_route(self, start: Star) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate route that maximizes star visits."""
        try:
            path, stats = self.calculator.find_max_visit_route_from_json(start)
            
            if stats.get('error'):
                return None, stats
            
            return path, stats
        except Exception as e:
            return None, {"error": str(e)}
    
    def calculate_min_cost_route(self, start: Star, research_params=None) -> Tuple[Optional[List[Star]], Optional[Dict[str, Any]]]:
        """Calculate minimum cost route."""
        try:
            path, stats = self.calculator.find_min_cost_route_from_json(start, research_params)
            
            if not path or 'error' in stats:
                return None, stats
            
            return path, stats
        except Exception as e:
            return None, {"error": str(e)}
    
    def calculate_path_stats(self, path: List[Star]) -> Dict[str, Any]:
        """Calculate statistics for a given path."""
        try:
            return self.calculator.calculate_path_stats(path)
        except Exception as e:
            return {"error": str(e)}
    
    def extract_star_id_from_text(self, combo_text: str) -> Optional[str]:
        """Extract star ID from combo box text."""
        if not combo_text:
            return None
        # Format is "Label (id) - E:energy"
        start = combo_text.find('(')
        end = combo_text.find(')')
        if start != -1 and end != -1:
            return combo_text[start+1:end]
        return None