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
                
                # Calculate cost using simplified approach
                edge_cost = route.distance + (route.danger_level * 10)
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
                'num_jumps': 0,
                'path_stars': [],
                'total_energy_needed': 0,
                'total_grass_needed': 0
            }
        
        total_distance = 0
        total_danger = 0
        total_energy_for_eating = 0
        total_grass_needed = 0
        
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
        
        # Calculate energy and grass for eating stars
        for star in path:
            total_energy_for_eating += star.amount_of_energy
            total_grass_needed += star.time_to_eat * 5  # 5 kg per time unit
        
        return {
            'total_distance': round(total_distance, 2),
            'total_danger': total_danger,
            'num_jumps': len(path) - 1,
            'path_stars': [star.label for star in path],
            'total_energy_needed': total_distance * 0.1,  # Energy for traveling
            'total_grass_needed': total_grass_needed,
            'total_energy_gained': total_energy_for_eating * 10,  # Energy from eating stars
            'net_energy': (total_energy_for_eating * 10) - (total_distance * 0.1)
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
    
    def find_optimal_eating_sequence(self, start: Star, available_energy: int, available_grass: int) -> List[Star]:
        """
        Find the optimal sequence of stars to eat based on available resources.
        
        Args:
            start: Starting star
            available_energy: Current energy of the burro
            available_grass: Current grass of the burro
            
        Returns:
            List of stars in optimal eating sequence
        """
        visited = set()
        eating_sequence = []
        current_star = start
        current_energy = available_energy
        current_grass = available_grass
        
        while current_energy > 10 and current_grass > 5:
            # Find best nearby star to eat
            best_star = None
            best_benefit = -1
            
            for star in self.space_map.get_all_stars_list():
                if star.id in visited:
                    continue
                
                path, cost = self.dijkstra(current_star, star)
                if not path:
                    continue
                
                # Calculate travel cost
                travel_energy = sum(route.distance for route in self.space_map.routes 
                                  if self._route_in_path(route, path)) * 0.1
                
                # Calculate eating benefit
                eating_benefit = star.amount_of_energy * 10
                grass_cost = star.time_to_eat * 5
                
                # Net benefit
                net_benefit = eating_benefit - travel_energy
                
                # Check if feasible
                if (current_energy > travel_energy + 10 and 
                    current_grass >= grass_cost and 
                    net_benefit > best_benefit):
                    best_benefit = net_benefit
                    best_star = star
            
            if best_star is None:
                break
            
            # Move to and eat the best star
            path, _ = self.dijkstra(current_star, best_star)
            travel_cost = sum(route.distance for route in self.space_map.routes 
                            if self._route_in_path(route, path)) * 0.1
            
            current_energy -= travel_cost
            current_energy += best_star.amount_of_energy * 10
            current_grass -= best_star.time_to_eat * 5
            
            eating_sequence.append(best_star)
            visited.add(best_star.id)
            current_star = best_star
        
        return eating_sequence
    
    def _route_in_path(self, route, path: List[Star]) -> bool:
        """Check if a route is part of a path."""
        for i in range(len(path) - 1):
            current_star = path[i]
            next_star = path[i + 1]
            if ((route.from_star == current_star and route.to_star == next_star) or
                (route.to_star == current_star and route.from_star == next_star)):
                return True
        return False
