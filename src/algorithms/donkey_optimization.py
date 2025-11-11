"""
Sistema de optimización de rutas para el Burro Astronauta.
Calcula la ruta que permite visitar la mayor cantidad de estrellas antes de morir.
"""
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from ..core import Star, SpaceMap, BurroAstronauta, Route
from .route_calculator import RouteCalculator
import itertools


class DonkeyRouteOptimizer:
    """Optimizador de rutas para maximizar estrellas visitadas."""
    
    def __init__(self, space_map: SpaceMap):
        self.space_map = space_map
        self.calculator = RouteCalculator(space_map, self._get_default_config())
    
    def _get_default_config(self) -> Dict:
        """Configuración por defecto para cálculos."""
        return {
            'consumption_rates': {
                'fuel_per_unit_distance': 2,
                'food_per_unit_distance': 0.1,
                'oxygen_per_unit_distance': 0.5,
                'health_decay_per_danger': 5
            }
        }
    
    def calculate_star_eating_benefit(self, star: Star) -> int:
        """Calcula el beneficio neto de comer una estrella."""
        # Energía ganada
        energy_gain = star.amount_of_energy * 10
        radius_bonus = int(star.radius * 5)
        total_gain = energy_gain + radius_bonus
        
        # Costo de tiempo/pasto
        grass_cost = star.time_to_eat * 5
        
        # El beneficio neto es la energía ganada menos el costo en pasto
        # Convertimos pasto a "energía equivalente" para comparación
        return total_gain - (grass_cost // 2)
    
    def simulate_journey(self, 
                        start_star: Star, 
                        burro: BurroAstronauta,
                        max_iterations: int = 1000) -> Tuple[List[Star], Dict]:
        """
        Simula un viaje para encontrar la ruta que maximiza estrellas visitadas.
        
        Args:
            start_star: Estrella de inicio
            burro: Burro astronauta
            max_iterations: Máximo número de iteraciones para evitar bucles infinitos
            
        Returns:
            Tupla con (ruta_optima, estadisticas)
        """
        if not burro.is_alive():
            return [], {"error": "El burro está muerto, no puede viajar"}
        
        visited_stars = []
        current_star = start_star
        iterations = 0
        
        # Copiar el burro para no modificar el original
        working_burro = BurroAstronauta(
            name=burro.name,
            energia_inicial=burro.energia_inicial,
            estado_salud=burro.estado_salud,
            pasto=burro.pasto,
            start_age=burro.start_age,
            death_age=burro.death_age
        )
        working_burro.current_energy = burro.current_energy
        working_burro.current_pasto = burro.current_pasto
        working_burro.current_location = start_star
        
        while (working_burro.is_alive() and 
               iterations < max_iterations):
            
            # Intentar comer la estrella actual si es posible y beneficioso
            if working_burro.can_eat_star(current_star) and current_star not in visited_stars:
                benefit = self.calculate_star_eating_benefit(current_star)
                if benefit > 0:  # Solo comer si es beneficioso
                    visited_stars.append(current_star)
                    working_burro.consume_resources_eating_star(current_star)
            
            # Encontrar la siguiente mejor estrella
            next_star = self._find_next_optimal_star(
                current_star, visited_stars, working_burro
            )
            
            if next_star is None:
                break
            
            # Calcular costo del viaje
            path, travel_cost = self.calculator.dijkstra(current_star, next_star)
            
            if path is None or len(path) < 2:
                break
            
            # Calcular distancia total del camino
            total_distance = 0
            for i in range(len(path) - 1):
                route = self._find_route_between_stars(path[i], path[i + 1])
                if route:
                    total_distance += route.distance
            
            # Verificar si puede hacer el viaje
            if not working_burro.can_travel(total_distance):
                break
            
            # Realizar el viaje
            working_burro.consume_resources_traveling(total_distance)
            current_star = next_star
            working_burro.current_location = current_star
            iterations += 1
        
        # Estadísticas del viaje
        stats = {
            "stars_visited": len(visited_stars),
            "final_energy": working_burro.current_energy,
            "final_grass": working_burro.current_pasto,
            "final_health_state": working_burro.estado_salud,
            "total_iterations": iterations,
            "route": [star.label for star in visited_stars],
            "initial_condition": {
                "energia_inicial": burro.energia_inicial,
                "estado_salud": burro.estado_salud,
                "pasto": burro.pasto,
                "edad": burro.start_age
            },
            "success": working_burro.is_alive() and len(visited_stars) > 0
        }
        
        return visited_stars, stats
    
    def _find_next_optimal_star(self, 
                               current: Star, 
                               visited: List[Star], 
                               burro: BurroAstronauta) -> Optional[Star]:
        """Encuentra la siguiente estrella óptima para visitar."""
        visited_ids = {star.id for star in visited}
        best_star = None
        best_score = -1
        
        # Evaluar todas las estrellas no visitadas
        for star in self.space_map.get_all_stars_list():
            if star.id in visited_ids:
                continue
            
            # Calcular ruta y costo
            path, cost = self.calculator.dijkstra(current, star)
            if path is None or len(path) < 2:
                continue
            
            # Calcular distancia real del camino
            total_distance = 0
            for i in range(len(path) - 1):
                route = self._find_route_between_stars(path[i], path[i + 1])
                if route:
                    total_distance += route.distance
            
            # Verificar si puede viajar hasta allí
            if not burro.can_travel(total_distance):
                continue
            
            # Calcular score de la estrella
            eating_benefit = self.calculate_star_eating_benefit(star)
            travel_cost = total_distance * 0.1 * max(1, (burro.start_age - 5) / 10)
            
            # Score considera beneficio vs costo
            score = eating_benefit - travel_cost
            
            # Bonus por estrellas hipergigantes
            if star.hypergiant:
                score += 20
            
            # Bonus por distancia corta (prefiere estrellas cercanas)
            if total_distance < 50:
                score += 10
            elif total_distance < 100:
                score += 5
            
            # Penalización por viajes muy largos
            if total_distance > 150:
                score -= 10
            
            if score > best_score:
                best_score = score
                best_star = star
        
        return best_star
    
    def _find_route_between_stars(self, star1: Star, star2: Star) -> Optional['Route']:
        """Encuentra la ruta entre dos estrellas."""
        for route in self.space_map.routes:
            if ((route.from_star == star1 and route.to_star == star2) or
                (route.to_star == star1 and route.from_star == star2)):
                return route
        return None
    
    def optimize_route_from_json_data(self, start_star_id: str) -> Tuple[List[Star], Dict]:
        """
        Optimiza la ruta usando los datos del JSON del burro.
        
        Args:
            start_star_id: ID de la estrella de inicio
            
        Returns:
            Tupla con (ruta_optima, estadisticas)
        """
        # Crear burro desde los datos del JSON
        burro = self.space_map.create_burro_astronauta()
        
        # Buscar estrella de inicio
        start_star = self.space_map.get_star(start_star_id)
        if start_star is None:
            return [], {"error": f"Estrella {start_star_id} no encontrada"}
        
        return self.simulate_journey(start_star, burro)
    
    def find_best_starting_star(self) -> Tuple[Star, int]:
        """
        Encuentra la mejor estrella para comenzar el viaje.
        
        Returns:
            Tupla con (mejor_estrella, max_estrellas_visitadas)
        """
        best_star = None
        max_stars_visited = 0
        
        all_stars = self.space_map.get_all_stars_list()
        
        for star in all_stars:
            route, stats = self.optimize_route_from_json_data(star.id)
            stars_visited = stats.get('stars_visited', 0)
            
            if stars_visited > max_stars_visited:
                max_stars_visited = stars_visited
                best_star = star
        
        return best_star, max_stars_visited


# Función de utilidad para uso fácil
def optimize_donkey_route(space_map: SpaceMap, start_star_id: str) -> Tuple[List[Star], Dict]:
    """
    Función de conveniencia para optimizar la ruta del burro.
    
    Args:
        space_map: Mapa espacial cargado
        start_star_id: ID de la estrella de inicio
        
    Returns:
        Tupla con (ruta_optima, estadisticas)
    """
    optimizer = DonkeyRouteOptimizer(space_map)
    return optimizer.optimize_route_from_json_data(start_star_id)