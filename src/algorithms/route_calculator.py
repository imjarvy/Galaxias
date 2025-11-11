"""
Route calculation algorithms for finding optimal paths through space.
"""
import heapq
from typing import Dict, List, Optional, Tuple
from ..core import Star, Route, SpaceMap
from ..utils.burro_utils.burro_math import calculate_energy_from_eating
from ..utils.json_handler import JSONHandler

def get_route_and_stats(space_map, path):
    total_distance = 0
    total_danger = 0
    for i in range(len(path) - 1):
        route = next((r for r in space_map.routes if
                      (r.from_star == path[i] and r.to_star == path[i+1]) or
                      (r.to_star == path[i] and r.from_star == path[i+1])), None)
        if route:
            total_distance += route.distance
            total_danger += route.danger_level
    return total_distance, total_danger

def get_energy_and_grass(path):
    total_energy = 0
    total_grass = 0
    for star in path:
        total_energy += calculate_energy_from_eating(star, 1.0, 1.0)
        total_grass += star.time_to_eat * 5
    return total_energy, total_grass

class RouteCalculator:
    """Calculate optimal routes between stars using graph algorithms."""
    
    def __init__(self, space_map: SpaceMap, config: Dict):
        self.space_map = space_map
        self.config = config
    
    def dijkstra(self, start: Star, end: Star) -> Tuple[Optional[List[Star]], float]:
        pq = [(0, start.id)]
        distances = {star.id: float('inf') for star in self.space_map.get_all_stars_list()}
        distances[start.id] = 0
        previous = {star.id: None for star in self.space_map.get_all_stars_list()}
        visited = set()
        while pq:
            current_cost, current_id = heapq.heappop(pq)
            if current_id in visited:
                continue
            visited.add(current_id)
            if current_id == end.id:
                path = []
                current = end.id
                while current is not None:
                    path.append(self.space_map.get_star(current))
                    current = previous[current]
                path.reverse()
                return path, distances[end.id]
            current_star = self.space_map.get_star(current_id)
            for route in self.space_map.get_routes_from(current_star):
                if route.blocked:
                    continue
                neighbor = route.to_star if route.from_star == current_star else route.from_star
                if neighbor.id in visited:
                    continue
                edge_cost = route.distance + (route.danger_level * 10)
                new_cost = current_cost + edge_cost
                if new_cost < distances[neighbor.id]:
                    distances[neighbor.id] = new_cost
                    previous[neighbor.id] = current_id
                    heapq.heappush(pq, (new_cost, neighbor.id))
        return None, float('inf')
    
    def calculate_path_stats(self, path: List[Star]) -> Dict:
        if not path or len(path) < 2:
            return {
                'total_distance': 0,
                'total_danger': 0,
                'num_jumps': 0,
                'path_stars': [],
                'total_energy_needed': 0,
                'total_grass_needed': 0
            }
        total_distance, total_danger = get_route_and_stats(self.space_map, path)
        total_energy_for_eating, total_grass_needed = get_energy_and_grass(path)
        return {
            'total_distance': round(total_distance, 2),
            'total_danger': total_danger,
            'num_jumps': len(path) - 1,
            'path_stars': [star.label for star in path],
            'total_energy_needed': total_distance * 0.1,
            'total_grass_needed': total_grass_needed,
            'total_energy_gained': total_energy_for_eating,
            'net_energy': total_energy_for_eating - (total_distance * 0.1)
        }
    
    def find_all_reachable_stars(self, start: Star, max_distance: float) -> List[Tuple[Star, float]]:
        reachable = []
        for star in self.space_map.get_all_stars_list():
            if star == start:
                continue
            path, cost = self.dijkstra(start, star)
            if path and cost <= max_distance:
                reachable.append((star, cost))
        reachable.sort(key=lambda x: x[1])
        return reachable
    
    def find_optimal_eating_sequence(self, start: Star, available_energy: int, available_grass: int) -> List[Star]:
        visited = set()
        eating_sequence = []
        current_star = start
        current_energy = available_energy
        current_grass = available_grass
        while current_energy > 10 and current_grass > 5:
            best_star = None
            best_benefit = -1
            for star in self.space_map.get_all_stars_list():
                if star.id in visited:
                    continue
                path, cost = self.dijkstra(current_star, star)
                if not path:
                    continue
                travel_energy = sum(route.distance for route in self.space_map.routes 
                                  if self._route_in_path(route, path)) * 0.1
                eating_benefit = star.amount_of_energy * 10
                grass_cost = star.time_to_eat * 5
                net_benefit = eating_benefit - travel_energy
                if (current_energy > travel_energy + 10 and 
                    current_grass >= grass_cost and 
                    net_benefit > best_benefit):
                    best_benefit = net_benefit
                    best_star = star
            if best_star is None:
                break
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
        for i in range(len(path) - 1):
            current_star = path[i]
            next_star = path[i + 1]
            if ((route.from_star == current_star and route.to_star == next_star) or
                (route.to_star == current_star and route.from_star == next_star)):
                return True
        return False
    
    def find_max_visit_route_from_json(self, start: Star, config_path: str = "data/spaceship_config.json") -> Tuple[List[Star], Dict]:
        edad = self.space_map.burro_data['startAge']
        energia_pct = self.space_map.burro_data['burroenergiaInicial'] 
        pasto_kg = self.space_map.burro_data['pasto']
        death_age = self.space_map.burro_data['deathAge']
        estado_salud = self.space_map.burro_data['estadoSalud'].lower()
        try:
            config = JSONHandler.load_spaceship_config(config_path)
            warp_factor = config.get('scientific_parameters', {}).get('warp_factor', 1.0)
        except Exception:
            warp_factor = 1.0
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
        adjacency: Dict[str, List[Tuple[Route, str]]] = {}
        for route in self.space_map.routes:
            if route.blocked:
                continue
            a = route.from_star.id
            b = route.to_star.id
            adjacency.setdefault(a, []).append((route, b))
            adjacency.setdefault(b, []).append((route, a))
        best = {
            'visited': [start],
            'distance': 0.0
        }
        def heuristic_score(visited_count: int, remaining_energy: int, remaining_life: float) -> float:
            base_score = visited_count * 1000
            energy_bonus = remaining_energy * 2
            life_bonus = min(remaining_life, 100) * 5
            return base_score + energy_bonus + life_bonus
        def optimized_search(current_id: str, path: List[Star], total_distance: float, energy_left: int, life_left: float, depth: int = 0):
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
                optimized_search(neighbor_id, path, total_distance + route.distance, energy_left - energy_cost, life_left - travel_time, depth + 1)
                path.pop()
        optimized_search(start.id, [start], 0.0, remaining_energy, remaining_life)
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

    def find_min_cost_route_from_json(self, start: Star, config_path: str = "data/spaceship_config.json", research_params=None) -> Tuple[List[Star], Dict]:
        from ..route_tools.min_cost_route import MinCostRouteCalculator
        calculator = MinCostRouteCalculator(self.space_map, config_path, research_params)
        result = calculator.calculate_min_cost_route(start.id)
        if not result.success:
            return [], {
                'error': result.error_message or 'No se pudo calcular ruta de menor gasto',
                'stars_visited': 0,
                'total_grass_consumed': 0.0,
                'final_energy': 0.0,
                'remaining_life': 0.0
            }
        path_stars = []
        for route_item in result.route_sequence:
            star = self.space_map.get_star(route_item['id'])
            if star:
                path_stars.append(star)
        stats = {
            'stars_visited': len(path_stars),
            'total_distance': result.total_distance,
            'life_time_consumed': result.life_consumed,
            'path_stars': [star.label for star in path_stars],
            'total_grass_consumed': result.total_grass_consumed,
            'final_energy': result.final_energy,
            'remaining_life': result.remaining_life,
            'star_actions_detail': result.star_actions,
            'calculation_type': 'minimum_cost',
            'research_parameters_used': {
                'energy_consumption_rate': research_params.energy_consumption_rate if research_params else 2.0,
                'time_percentage': research_params.time_percentage if research_params else 0.5,
                'custom_star_configurations': len(research_params.custom_star_settings) if research_params else 0
            } if research_params else None,
            'notes': 'Ruta optimizada para MENOR GASTO con reglas específicas de comer/investigar y parámetros configurables'
        }
        return path_stars, stats