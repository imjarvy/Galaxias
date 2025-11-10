"""
Route calculation algorithms for finding optimal paths through space.
"""
import heapq
import json
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
    
    def find_max_visit_route_from_json(self, 
                                      start: Star,
                                      config_path: str = "data/spaceship_config.json") -> Tuple[List[Star], Dict]:
        """
        Find the route that visits the maximum number of stars using ONLY JSON initial values.
        
        Args:
            start: Starting star
            config_path: Path to spaceship config
            
        Returns:
            Tuple of (optimal_path, statistics)
        """
        # USAR SOLO VALORES DEL JSON - no overrides
        edad = self.space_map.burro_data['startAge']
        energia_pct = self.space_map.burro_data['burroenergiaInicial'] 
        pasto_kg = self.space_map.burro_data['pasto']
        death_age = self.space_map.burro_data['deathAge']
        estado_salud = self.space_map.burro_data['estadoSalud'].lower()

        # Load spaceship config
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            warp_factor = config.get('scientific_parameters', {}).get('warp_factor', 1.0)
        except Exception:
            warp_factor = 1.0

        # Quick rejects
        if estado_salud == 'muerto' or energia_pct <= 0 or pasto_kg <= 0:
            return [], {
                'stars_visited': 0,
                'total_distance': 0.0,
                'life_time_consumed': 0.0,
                'error': 'Burro no puede iniciar viaje con los parámetros del JSON.',
                'json_values_used': {
                    'energia_inicial': energia_pct,
                    'edad_inicial': edad,
                    'death_age': death_age,
                    'pasto_inicial': pasto_kg,
                    'estado_salud': estado_salud
                }
            }

        remaining_life = max(0, death_age - edad)
        age_factor = max(1.0, (edad - 5) / 10.0)
        remaining_energy = int(energia_pct)

        def distance_to_time(distance: float) -> float:
            return distance / warp_factor

        def edge_cost_and_time(distance: float) -> Tuple[int, float]:
            energy_cost = int(distance * 0.1 * age_factor)
            travel_time = distance_to_time(distance)
            return energy_cost, travel_time

        # Build adjacency from routes
        adjacency: Dict[str, List[Tuple[Route, str]]] = {}
        for route in self.space_map.routes:
            if route.blocked:
                continue
            a = route.from_star.id
            b = route.to_star.id
            adjacency.setdefault(a, []).append((route, b))
            adjacency.setdefault(b, []).append((route, a))

        # Search with heuristics
        best = {
            'visited': [start],
            'distance': 0.0
        }

        def heuristic_score(visited_count: int, remaining_energy: int, remaining_life: float) -> float:
            base_score = visited_count * 1000
            energy_bonus = remaining_energy * 2
            life_bonus = min(remaining_life, 100) * 5
            return base_score + energy_bonus + life_bonus

        def optimized_search(current_id: str,
                           path: List[Star],
                           total_distance: float,
                           energy_left: int,
                           life_left: float,
                           depth: int = 0):
            nonlocal best
            
            if depth > 12:
                return

            if (len(path) > len(best['visited']) or 
                (len(path) == len(best['visited']) and total_distance < best['distance'])):
                best['visited'] = path.copy()
                best['distance'] = total_distance

            max_additional = min(8, len(self.space_map.get_all_stars_list()) - len(path))
            if len(path) + max_additional <= len(best['visited']):
                return

            neighbors = []
            for (route, neighbor_id) in adjacency.get(current_id, []):
                if neighbor_id in {s.id for s in path}:
                    continue

                d = route.distance
                energy_cost, travel_time = edge_cost_and_time(d)

                if energy_cost > energy_left or travel_time > life_left:
                    continue

                neighbor_star = self.space_map.get_star(neighbor_id)
                if not neighbor_star:
                    continue

                new_energy = energy_left - energy_cost
                new_life = life_left - travel_time
                score = heuristic_score(len(path) + 1, new_energy, new_life)
                
                neighbors.append((score, route, neighbor_id, neighbor_star, energy_cost, travel_time))

            neighbors.sort(key=lambda x: x[0], reverse=True)
            max_branches = min(6, len(neighbors))
            
            for i in range(max_branches):
                _, route, neighbor_id, neighbor_star, energy_cost, travel_time = neighbors[i]
                
                path.append(neighbor_star)
                optimized_search(neighbor_id,
                               path,
                               total_distance + route.distance,
                               energy_left - energy_cost,
                               life_left - travel_time,
                               depth + 1)
                path.pop()

        # Execute search
        optimized_search(start.id, [start], 0.0, remaining_energy, remaining_life)

        # Prepare statistics
        total_distance = round(best['distance'], 2)
        life_consumed = round(distance_to_time(best['distance']), 2)
        
        stats = {
            'stars_visited': len(best['visited']),
            'total_distance': total_distance,
            'life_time_consumed': life_consumed,
            'path_stars': [star.label for star in best['visited']],
            'json_values_used': {
                'energia_inicial': energia_pct,
                'edad_inicial': edad,
                'death_age': death_age,
                'pasto_inicial': pasto_kg,
                'estado_salud': estado_salud,
                'warp_factor': warp_factor,
                'age_factor': age_factor
            },
            'notes': f'Valores EXCLUSIVAMENTE del JSON: energia={energia_pct}%, edad={edad}, death_age={death_age}, pasto={pasto_kg}kg, salud={estado_salud}'
        }

        return best['visited'], stats
