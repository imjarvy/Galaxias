"""
Script to compute the route that visits the maximum number of stars
starting from a given star ID, using only immutable initial parameters:
estado_salud, edad, burroenergia (1-100), pasto_bodega (kg).

NUEVO: Incluye lógica de saltos hipergigantes para cambios de constelación.
- Detecta cambios de constelación y obliga el paso por hipergigante
- Aplica beneficios: +50% energía, x2 pasto
- Recalcula ruta con recursos mejorados

Assumptions (documentadas en la salida):
- Distancia de una ruta (distance) se convierte a tiempo usando warp_factor del spaceship_config.json.
- El consumo de energía para una arista usa la misma fórmula que en `BurroAstronauta.consume_resources_traveling`:
  energy_cost = int(distance * 0.1 * age_factor), where age_factor = max(1, (edad - 5)/10).
- No se modifica energía ni pasto durante el viaje (son presupuestos inmutables).
- El `death_age` puede ser proporcionado como argumento o tomado del JSON.

Output: JSON-like print con secuencia de IDs/labels, distancia total (años luz), tiempo de vida consumido, y número de estrellas visitadas.
"""
import argparse
import json
import heapq
from typing import List, Set, Tuple, Dict, Optional

from ..core.models import SpaceMap, Star, Route
from ..algorithms.hypergiant_jump import HyperGiantJumpSystem


"""
Script to compute the route that visits the maximum number of stars
starting from a given star ID, using ONLY the initial parameters from constellations.json.

Valores usados (SOLO del JSON):
- burroenergiaInicial: energía inicial del burro (%)
- startAge: edad inicial del burro (años)  
- deathAge: edad de muerte del burro (años)
- pasto: cantidad inicial de pasto (kg)
- estadoSalud: estado de salud inicial

Assumptions:
- Distancia se convierte a tiempo usando warp_factor del spaceship_config.json.
- El consumo de energía usa: energy_cost = int(distance * 0.1 * age_factor)
- No se modifica energía ni pasto durante el viaje (son presupuestos inmutables).
- Solo se requiere el start_id, todos los demás valores vienen del JSON.

Output: JSON con secuencia de estrellas, distancia total, tiempo de vida consumido, y número de estrellas visitadas.
"""


def compute_max_visits_from_json(space_map: SpaceMap,
                                start_id: str,
                                config_path: str = "data/spaceship_config.json") -> Dict:
    """
    Compute path that maximizes number of distinct stars visited.
    USA SOLO los valores iniciales del JSON (constellations.json).
    NUEVO: Incluye lógica de saltos hipergigantes para cambios de constelación.

    Args:
        space_map: SpaceMap instance (ya cargó los datos del JSON)
        start_id: Starting star ID
        config_path: Path to spaceship config for warp factor

    Returns:
        dict with sequence, total_distance, life_time_consumed, num_stars.
    """
    # Load spaceship config for time conversion
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        warp_factor = config.get('scientific_parameters', {}).get('warp_factor', 1.0)
    except Exception:
        warp_factor = 1.0

    # Inicializar sistema de saltos hipergigantes
    jump_system = HyperGiantJumpSystem(space_map)

    # USAR SOLO VALORES DEL JSON - no overrides
    edad = space_map.burro_data['startAge']
    energia_pct = space_map.burro_data['burroenergiaInicial'] 
    pasto_kg = space_map.burro_data['pasto']
    death_age = space_map.burro_data['deathAge']
    estado_salud = space_map.burro_data['estadoSalud'].lower()

    # Normalize start_id
    start_id = str(start_id)

    # Quick rejects
    if estado_salud == 'muerto' or energia_pct <= 0 or pasto_kg <= 0:
        return {
            'sequence': [],
            'total_distance': 0.0,
            'life_time_consumed': 0.0,
            'num_stars': 0,
            'notes': 'Burro no puede iniciar viaje con los parámetros del JSON.'
        }

    start_star = space_map.get_star(start_id)
    if not start_star:
        return {
            'sequence': [],
            'total_distance': 0.0,
            'life_time_consumed': 0.0,
            'num_stars': 0,
            'notes': f'Estrella inicio {start_id} no encontrada.'
        }

    remaining_life = max(0, death_age - edad)
    age_factor = max(1.0, (edad - 5) / 10.0)
    remaining_energy = int(energia_pct)
    current_grass = pasto_kg

    def distance_to_time(distance: float) -> float:
        """Convert distance to travel time using warp factor."""
        return distance / warp_factor

    def edge_cost_and_time(distance: float) -> Tuple[int, float]:
        """Return (energy_cost, travel_time_years) for an edge of given distance."""
        energy_cost = int(distance * 0.1 * age_factor)
        travel_time = distance_to_time(distance)
        return energy_cost, travel_time

    # Build adjacency from routes for quick lookup
    adjacency: Dict[str, List[Tuple[Route, str]]] = {}
    for route in space_map.routes:
        if route.blocked:
            continue
        a = route.from_star.id
        b = route.to_star.id
        adjacency.setdefault(a, []).append((route, b))
        adjacency.setdefault(b, []).append((route, a))

    # Search with heuristics for best path (AHORA CON SALTOS HIPERGIGANTES)
    best = {
        'visited': [start_star],
        'distance': 0.0,
        'hypergiant_jumps': []  # Nuevo: registro de saltos
    }

    def heuristic_score(visited_count: int, remaining_energy: int, remaining_life: float) -> float:
        """Heuristic to prioritize promising paths."""
        base_score = visited_count * 1000
        energy_bonus = remaining_energy * 2
        life_bonus = min(remaining_life, 100) * 5
        return base_score + energy_bonus + life_bonus

    def optimized_dfs(current_id: str,
                     path: List[Star],
                     total_distance: float,
                     energy_left: int,
                     life_left: float,
                     current_grass: float,
                     depth: int = 0):
        nonlocal best
        
        # Pruning: depth limit
        if depth > 15:
            return

        # Update best solution
        if (len(path) > len(best['visited']) or 
            (len(path) == len(best['visited']) and total_distance < best['distance'])):
            best['visited'] = path.copy()
            best['distance'] = total_distance

        # Early pruning
        max_additional = min(10, len(space_map.get_all_stars_list()) - len(path))
        if len(path) + max_additional <= len(best['visited']):
            return

        # Get current star for constellation checks
        current_star = space_map.get_star(current_id)
        if not current_star:
            return

        # Get and sort neighbors by heuristic (INCLUYENDO LÓGICA HIPERGIGANTE)
        neighbors = []
        for (route, neighbor_id) in adjacency.get(current_id, []):
            if neighbor_id in {s.id for s in path}:
                continue

            neighbor_star = space_map.get_star(neighbor_id)
            if not neighbor_star:
                continue

            d = route.distance
            energy_cost, travel_time = edge_cost_and_time(d)

            # NUEVA LÓGICA: Verificar si requiere salto hipergigante
            requires_jump = jump_system.requires_hypergiant_jump(current_star, neighbor_star)
            
            if requires_jump:
                # Buscar hipergigante accesible para el salto
                accessible_hgs = jump_system.find_accessible_hypergiants(current_star)
                
                if not accessible_hgs:
                    continue  # No hay hipergigantes accesibles
                
                # Usar la hipergigante más cercana factible
                best_hg = None
                best_hg_distance = float('inf')
                
                for hg, hg_distance in accessible_hgs:
                    hg_energy_cost, hg_travel_time = edge_cost_and_time(hg_distance)
                    
                    if (hg_energy_cost <= energy_left and hg_travel_time <= life_left and
                        hg_distance < best_hg_distance):
                        best_hg = hg
                        best_hg_distance = hg_distance
                
                if not best_hg:
                    continue  # No hay hipergigante factible
                
                # Calcular costo total del salto hipergigante
                hg_energy_cost, hg_travel_time = edge_cost_and_time(best_hg_distance)
                
                # Simular beneficios del salto hipergigante
                energy_after_jump = energy_left - hg_energy_cost
                energy_boost = energy_after_jump * 0.5  # +50% de energía actual
                new_energy = min(100, energy_after_jump + energy_boost)
                
                new_grass = current_grass * 2  # Duplicar pasto
                new_life = life_left - hg_travel_time
                
                # El salto hipergigante nos lleva directamente al destino
                total_jump_distance = best_hg_distance
                
                # Agregar a la búsqueda con los recursos mejorados
                score = heuristic_score(len(path) + 2, new_energy, new_life)  # +2 stars (hg + destination)
                
                neighbors.append((score, None, neighbor_id, neighbor_star, 
                                new_energy, new_life, new_grass, total_jump_distance, 
                                True, best_hg))  # Marcado como salto hipergigante
            else:
                # Viaje normal (misma constelación)
                if energy_cost > energy_left or travel_time > life_left:
                    continue

                new_energy = energy_left - energy_cost
                new_life = life_left - travel_time
                score = heuristic_score(len(path) + 1, new_energy, new_life)
                
                neighbors.append((score, route, neighbor_id, neighbor_star, 
                                new_energy, new_life, current_grass, d, 
                                False, None))  # Viaje normal

        # Sort by score and limit branches
        neighbors.sort(key=lambda x: x[0], reverse=True)
        max_branches = min(8, len(neighbors))
        
        for i in range(max_branches):
            (score, route, neighbor_id, neighbor_star, new_energy, 
             new_life, new_grass, distance, is_hypergiant_jump, hypergiant) = neighbors[i]
            
            if is_hypergiant_jump:
                # Agregar hipergigante al path si no está ya
                new_path = path.copy()
                if hypergiant not in path:
                    new_path.append(hypergiant)
                new_path.append(neighbor_star)
                
                # Registrar el salto hipergigante
                if len(best['hypergiant_jumps']) < 10:  # Limitar registro
                    jump_info = {
                        'from': current_star.label,
                        'hypergiant': hypergiant.label,
                        'to': neighbor_star.label,
                        'distance': distance
                    }
                    if jump_info not in best['hypergiant_jumps']:
                        best['hypergiant_jumps'].append(jump_info)
            else:
                # Viaje normal
                new_path = path.copy()
                new_path.append(neighbor_star)
            
            # Continuar búsqueda recursiva
            optimized_dfs(neighbor_id, new_path, total_distance + distance,
                         int(new_energy), new_life, new_grass, depth + 1)

    # Execute search with hypergiant jump support
    optimized_dfs(start_star.id, [start_star], 0.0, remaining_energy, remaining_life, current_grass)

    sequence = [{'id': s.id, 'label': s.label} for s in best['visited']]
    total_distance = round(best['distance'], 2)
    life_time_consumed = round(distance_to_time(best['distance']), 2)
    num_stars = len(best['visited'])

    return {
        'sequence': sequence,
        'total_distance': total_distance,
        'life_time_consumed': life_time_consumed,
        'num_stars': num_stars,
        'hypergiant_jumps': best['hypergiant_jumps'],  # Nuevo: info de saltos
        'json_values_used': {
            'energia_inicial': energia_pct,
            'edad_inicial': edad,
            'death_age': death_age,
            'pasto_inicial': pasto_kg,
            'estado_salud': estado_salud,
            'warp_factor': warp_factor
        },
        'notes': (
            f'Valores EXCLUSIVAMENTE del JSON: energia={energia_pct}%, edad={edad}, '
            f'death_age={death_age}, pasto={pasto_kg}kg, salud={estado_salud}. '
            f'Warp_factor={warp_factor} del spaceship_config.json. '
            f'NUEVO: Incluye {len(best["hypergiant_jumps"])} saltos hipergigantes.'
        )
    }


def main():
    parser = argparse.ArgumentParser(description='Compute max-visit route using ONLY JSON initial values')
    parser.add_argument('--start', required=True, help='Start star ID (only required parameter)')
    parser.add_argument('--config', default='data/spaceship_config.json', help='Path to spaceship config (opcional)')

    args = parser.parse_args()

    # Cargar mapa espacial (esto carga los valores del JSON automáticamente)
    sm = SpaceMap('data/constellations.json')

    # Usar SOLO valores del JSON - no se aceptan overrides
    result = compute_max_visits_from_json(sm,
                                         start_id=args.start,
                                         config_path=args.config)

    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Mostrar resumen de valores usados del JSON
    if 'json_values_used' in result:
        print("\n" + "="*50)
        print("VALORES USADOS DEL JSON:")
        print("="*50)
        for key, value in result['json_values_used'].items():
            print(f"{key}: {value}")
        print("="*50)


if __name__ == '__main__':
    main()