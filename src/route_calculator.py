"""
Route calculation algorithms for finding optimal paths through space.
"""
import heapq
from typing import Dict, List, Optional, Tuple
from src.models import Star, Route, SpaceMap


class RouteCalculator:
    """Calculate optimal routes between stars using graph algorithms."""
    
    def __init__(self, space_map: SpaceMap, config: Dict):
        self.space_map = space_map
        self.config = config
    
    def dijkstra(self, start: Star, end: Star) -> Tuple[Optional[List[Star]], float]:
        """
        Find the shortest path between two stars using Dijkstra's algorithm.
        Returns tuple of (path, total_cost) or (None, infinity) if no path exists.
        """
        # Priority queue: (cost, star)
        pq = [(0, start.id)]
        # Distance dictionary
        distances = {star.id: float('inf') for star in self.space_map.get_all_stars_list()}
        distances[start.id] = 0
        # Previous star in optimal path
        previous = {star.id: None for star in self.space_map.get_all_stars_list()}
        # Visited set
        visited = set()
        
        rates = self.config['consumption_rates']
        fuel_rate = rates['fuel_per_unit_distance']
        danger_penalty = rates['health_decay_per_danger'] * 10
        
        while pq:
            current_cost, current_id = heapq.heappop(pq)
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            if current_id == end.id:
                # Reconstruct path
                path = []
                current = end.id
                while current is not None:
                    path.append(self.space_map.get_star(current))
                    current = previous[current]
                path.reverse()
                return path, distances[end.id]
            
            current_star = self.space_map.get_star(current_id)
            
            # Check all neighboring routes
            for route in self.space_map.get_routes_from(current_star):
                if route.blocked:
                    continue
                
                # Determine neighbor
                if route.from_star == current_star:
                    neighbor = route.to_star
                else:
                    neighbor = route.from_star
                
                if neighbor.id in visited:
                    continue
                
                # Calculate cost
                edge_cost = route.calculate_cost(fuel_rate, danger_penalty)
                new_cost = current_cost + edge_cost
                
                if new_cost < distances[neighbor.id]:
                    distances[neighbor.id] = new_cost
                    previous[neighbor.id] = current_id
                    heapq.heappush(pq, (new_cost, neighbor.id))
        
        # No path found
        return None, float('inf')
    
    def calculate_path_stats(self, path: List[Star]) -> Dict:
        """Calculate statistics for a given path."""
        if not path or len(path) < 2:
            return {
                'total_distance': 0,
                'total_danger': 0,
                'total_fuel_needed': 0,
                'total_food_needed': 0,
                'total_oxygen_needed': 0,
                'estimated_health_loss': 0,
                'num_jumps': 0
            }
        
        total_distance = 0
        total_danger = 0
        rates = self.config['consumption_rates']
        
        for i in range(len(path) - 1):
            current_star = path[i]
            next_star = path[i + 1]
            
            # Find the route between these stars
            route = None
            for r in self.space_map.routes:
                if ((r.from_star == current_star and r.to_star == next_star) or
                    (r.to_star == current_star and r.from_star == next_star)):
                    route = r
                    break
            
            if route:
                total_distance += route.distance
                total_danger += route.danger_level
        
        return {
            'total_distance': round(total_distance, 2),
            'total_danger': total_danger,
            'total_fuel_needed': round(total_distance * rates['fuel_per_unit_distance'], 2),
            'total_food_needed': round(total_distance * rates['food_per_unit_distance'], 2),
            'total_oxygen_needed': round(total_distance * rates['oxygen_per_unit_distance'], 2),
            'estimated_health_loss': round(total_danger * rates['health_decay_per_danger'], 2),
            'num_jumps': len(path) - 1,
            'path_stars': [star.name for star in path]
        }
    
    def find_all_reachable_stars(self, start: Star, max_distance: float) -> List[Tuple[Star, float]]:
        """Find all stars reachable within a maximum distance."""
        reachable = []
        
        for star in self.space_map.get_all_stars_list():
            if star == start:
                continue
            
            path, cost = self.dijkstra(start, star)
            if path and cost <= max_distance:
                reachable.append((star, cost))
        
        # Sort by distance
        reachable.sort(key=lambda x: x[1])
        return reachable
