"""
Sistema de optimización de rutas para el Burro Astronauta con criterio de MENOR GASTO POSIBLE.
NUEVO: Incluye lógica de saltos hipergigantes para cambios de constelación.

Implementa las reglas específicas:
- Si energía < 50% el burro puede comer en la estrella
- Efecto por kg de pasto según estado de salud: +5% (excelente), +3% (regular), +2% (malo)
- División de tiempo: 50% comer, 50% investigar
- Consumo de energía por investigación
- Una estrella solo puede visitarse una vez
- Objetivo: menor gasto posible visitando máximo estrellas
- NUEVO: Saltos hipergigantes obligatorios para cambios de constelación con beneficios
"""
import argparse
import json
import sys
import os
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass

# Agregar path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import SpaceMap, Star, Route
from src.parameter_editor_simple import ResearchParameters
from src.algorithms.hypergiant_jump import HyperGiantJumpSystem


@dataclass
class StarAction:
    """Representa las acciones realizadas en una estrella con cálculos detallados."""
    star_id: str
    star_label: str
    
    # Estado inicial
    arrived_energy: float
    available_grass: float
    
    # Análisis de capacidad para comer
    can_eat: bool
    
    # Cálculos de tiempo
    total_time_star: float
    time_eating: float
    time_researching: float
    
    # Cálculos de comer (si aplica)
    max_kg_can_eat: float
    ate_kg: float
    base_energy_star: float
    health_bonus_percentage: float
    eating_bonus_energy: float
    radius_bonus_energy: float
    total_energy_gained_eating: float
    
    # Cálculos de investigación (siempre aplica)
    energy_consumed_research: float
    
    # Estado final
    energy_after_eating: float
    final_energy: float
    total_grass_consumed: float
    
    # Constantes con valores por defecto
    energy_threshold: float = 50.0
    research_energy_rate: float = 2.0
    
    def to_detailed_dict(self) -> Dict:
        """Convierte a diccionario con todos los cálculos detallados."""
        return {
            'star_info': {
                'id': self.star_id,
                'label': self.star_label
            },
            'initial_state': {
                'arrived_energy': round(self.arrived_energy, 2),
                'available_grass': round(self.available_grass, 2)
            },
            'eating_analysis': {
                'can_eat': self.can_eat,
                'reason': f"Energía {self.arrived_energy:.1f}% {'<' if self.can_eat else '>='} {self.energy_threshold}%",
                'calculations': {
                    'max_kg_can_eat': round(self.max_kg_can_eat, 2),
                    'actually_ate_kg': round(self.ate_kg, 2),
                    'base_energy_from_star': round(self.base_energy_star, 1),
                    'health_bonus_rate': f"{self.health_bonus_percentage*100:.1f}%",
                    'eating_bonus_energy': round(self.eating_bonus_energy, 1),
                    'radius_bonus_energy': round(self.radius_bonus_energy, 1),
                    'total_energy_gained': round(self.total_energy_gained_eating, 1)
                }
            },
            'time_distribution': {
                'total_time_at_star': round(self.total_time_star, 1),
                'time_eating': round(self.time_eating, 1),
                'time_researching': round(self.time_researching, 1),
                'eating_percentage': f"{(self.time_eating/self.total_time_star)*100:.1f}%" if self.total_time_star > 0 else "0%",
                'research_percentage': f"{(self.time_researching/self.total_time_star)*100:.1f}%" if self.total_time_star > 0 else "0%"
            },
            'research_calculations': {
                'research_time': round(self.time_researching, 1),
                'energy_rate_per_time': self.research_energy_rate,
                'formula': f"{self.time_researching:.1f} × {self.research_energy_rate} = {self.energy_consumed_research:.1f}%",
                'energy_consumed': round(self.energy_consumed_research, 1)
            },
            'energy_flow': {
                'initial_energy': round(self.arrived_energy, 1),
                'energy_after_eating': round(self.energy_after_eating, 1),
                'energy_consumed_research': round(self.energy_consumed_research, 1),
                'final_energy': round(self.final_energy, 1),
                'net_energy_change': round(self.final_energy - self.arrived_energy, 1)
            },
            'resource_consumption': {
                'grass_consumed_this_star': round(self.total_grass_consumed, 2),
                'grass_remaining': round(self.available_grass - self.total_grass_consumed, 2)
            }
        }


@dataclass
class MinCostResult:
    """Resultado del cálculo de ruta de menor gasto."""
    route_sequence: List[Dict]
    star_actions: List[StarAction]
    total_grass_consumed: float
    final_energy: float
    remaining_life: float
    total_distance: float
    life_consumed: float
    success: bool
    error_message: Optional[str] = None


class MinCostRouteCalculator:
    """Calculador de rutas con criterio de menor gasto posible."""
    
    def __init__(self, space_map: SpaceMap, config_path: str = "data/spaceship_config.json", research_params: Optional[ResearchParameters] = None):
        """
        Inicializa el calculador.
        
        Args:
            space_map: Mapa espacial
            config_path: Ruta al archivo de configuración
            research_params: Parámetros configurables de investigación
        """
        self.space_map = space_map
        self.research_params = research_params or ResearchParameters()
        self.warp_factor = self._load_warp_factor(config_path)
    
    def _get_effective_research_params(self, star: Star) -> Dict[str, float]:
        """
        Obtiene los parámetros de investigación efectivos para una estrella específica.
        
        Args:
            star: Estrella para la cual obtener parámetros
            
        Returns:
            Dict con parámetros efectivos para la estrella
        """
        star_config = self.research_params.custom_star_settings.get(star.id, {})
        
        return {
            'energy_consumption_rate': star_config.get('energy_rate', self.research_params.energy_consumption_rate),
            'time_percentage': self.research_params.time_percentage,
            'life_time_bonus': star_config.get('time_bonus', self.research_params.life_time_bonus),
            'energy_bonus': star_config.get('energy_bonus', self.research_params.energy_bonus_per_star),
            'knowledge_multiplier': self.research_params.knowledge_multiplier
        }
    
    def _load_warp_factor(self, config_path: str) -> float:
        """Carga el warp factor del archivo de configuración."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get('scientific_parameters', {}).get('warp_factor', 1.0)
        except Exception:
            return 1.0
    
    def _get_health_bonus(self, health_state: str) -> float:
        """Obtiene el bonus de energía por kg según estado de salud."""
        health_bonuses = {
            'excelente': 0.05,  # +5%
            'regular': 0.03,    # +3%
            'malo': 0.02        # +2%
        }
        return health_bonuses.get(health_state.lower(), 0.02)
    
    def _calculate_eating_benefits(self, star: Star, health_state: str) -> Tuple[float, float]:
        """
        Calcula los beneficios de comer en una estrella.
        
        Returns:
            Tuple[kg_to_eat, energy_gained]
        """
        # Cantidad máxima que puede comer (basado en tiempo disponible)
        max_eating_time = star.time_to_eat * 0.5  # 50% del tiempo total
        kg_to_eat = max_eating_time  # Asumimos 1 kg por unidad de tiempo
        
        # Energía base por la estrella
        base_energy = star.amount_of_energy * 10
        
        # Bonus por kg consumido según estado de salud
        health_bonus = self._get_health_bonus(health_state)
        eating_bonus = kg_to_eat * health_bonus * 100  # Convertir porcentaje a energía
        
        # Bonus por radio de la estrella
        radius_bonus = star.radius * 5
        
        total_energy_gained = base_energy + eating_bonus + radius_bonus
        
        return kg_to_eat, total_energy_gained
    
    def _calculate_research_cost(self, star: Star) -> Tuple[float, float]:
        """
        Calcula el tiempo y energía consumidos en investigación usando parámetros configurables.
        
        Args:
            star: Estrella donde se realiza la investigación
            
        Returns:
            Tuple[research_time, energy_consumed]
        """
        # Obtener parámetros específicos para esta estrella
        params = self._get_effective_research_params(star)
        
        # Tiempo de investigación basado en el porcentaje configurado
        research_time = star.time_to_eat * params['time_percentage']
        
        # Energía consumida basada en la tasa configurada
        energy_consumed = research_time * params['energy_consumption_rate']
        
        return research_time, energy_consumed
    
    def calculate_min_cost_route(self, start_id: str) -> MinCostResult:
        """
        Calcula la ruta que permite visitar la mayor cantidad de estrellas con el menor gasto posible.
        """
        # Cargar parámetros del JSON
        edad = self.space_map.burro_data['startAge']
        energia_inicial = self.space_map.burro_data['burroenergiaInicial']
        pasto_inicial = self.space_map.burro_data['pasto']
        death_age = self.space_map.burro_data['deathAge']
        estado_salud = self.space_map.burro_data['estadoSalud'].lower()
        
        # Validaciones iniciales
        if estado_salud == 'muerto' or energia_inicial <= 0 or pasto_inicial <= 0:
            return MinCostResult(
                route_sequence=[],
                star_actions=[],
                total_grass_consumed=0.0,
                final_energy=0.0,
                remaining_life=0.0,
                total_distance=0.0,
                life_consumed=0.0,
                success=False,
                error_message="Burro no puede iniciar viaje con los parámetros del JSON."
            )
        
        start_star = self.space_map.get_star(start_id)
        if not start_star:
            return MinCostResult(
                route_sequence=[],
                star_actions=[],
                total_grass_consumed=0.0,
                final_energy=0.0,
                remaining_life=0.0,
                total_distance=0.0,
                life_consumed=0.0,
                success=False,
                error_message=f"Estrella inicio {start_id} no encontrada."
            )
        
        # Estado inicial
        current_energy = float(energia_inicial)
        current_grass = float(pasto_inicial)
        remaining_life = max(0, death_age - edad)
        age_factor = max(1.0, (edad - 5) / 10.0)
        
        visited_stars = set()
        route_sequence = []
        star_actions = []
        current_star = start_star
        total_distance = 0.0
        
        # Construir grafo de adyacencia
        adjacency = self._build_adjacency_graph()
        
        while True:
            # Verificar si puede actuar en la estrella actual
            if current_star.id not in visited_stars:
                visited_stars.add(current_star.id)
                route_sequence.append({
                    'id': current_star.id,
                    'label': current_star.label
                })
                
                # Procesar acciones en la estrella actual
                action = self._process_star_actions(
                    current_star, current_energy, current_grass, estado_salud
                )
                
                star_actions.append(action)
                
                # Actualizar estado después de las acciones
                current_energy = action.final_energy
                current_grass -= action.total_grass_consumed
                
                # Verificar si aún está vivo después de las acciones
                if current_energy <= 0 or current_grass <= 0:
                    break
            
            # Buscar siguiente estrella óptima
            next_star, travel_cost = self._find_next_optimal_star(
                current_star, visited_stars, current_energy, current_grass,
                remaining_life, age_factor, adjacency
            )
            
            if not next_star:
                break
            
            # Verificar si puede realizar el viaje
            energy_cost = int(travel_cost * 0.1 * age_factor)
            travel_time = travel_cost / self.warp_factor
            
            if energy_cost > current_energy or travel_time > remaining_life:
                break
            
            # Realizar el viaje
            current_energy -= energy_cost
            remaining_life -= travel_time
            total_distance += travel_cost
            current_star = next_star
            
            # Verificar supervivencia después del viaje
            if current_energy <= 0 or remaining_life <= 0:
                break
        
        life_consumed = total_distance / self.warp_factor
        
        return MinCostResult(
            route_sequence=route_sequence,
            star_actions=star_actions,
            total_grass_consumed=pasto_inicial - current_grass,
            final_energy=current_energy,
            remaining_life=remaining_life,
            total_distance=round(total_distance, 2),
            life_consumed=round(life_consumed, 2),
            success=len(visited_stars) > 0
        )
    
    def _process_star_actions(self, star: Star, current_energy: float, 
                             current_grass: float, health_state: str) -> StarAction:
        """Procesa todas las acciones en una estrella con cálculos detallados usando parámetros configurables."""
        arrived_energy = current_energy
        
        # Obtener parámetros específicos para esta estrella
        params = self._get_effective_research_params(star)
        
        # Determinar si puede y debe comer (energía < 50%)
        can_eat = current_energy < 50.0
        
        # Cálculos de tiempo en la estrella usando parámetros configurables
        total_time_star = star.time_to_eat
        time_eating = 0.0
        time_researching = star.time_to_eat * params['time_percentage']
        
        # Cálculos detallados de comer
        max_kg_can_eat, _ = self._calculate_eating_benefits(star, health_state)
        ate_kg = 0.0
        base_energy_star = star.amount_of_energy * 10
        health_bonus_percentage = self._get_health_bonus(health_state)
        eating_bonus_energy = 0.0
        radius_bonus_energy = star.radius * 5
        total_energy_gained_eating = 0.0
        energy_after_eating = current_energy
        
        if can_eat and current_grass >= max_kg_can_eat:
            # Realizar cálculos de comer - tiempo complementario al de investigación
            time_eating = star.time_to_eat * (1.0 - params['time_percentage'])
            ate_kg = max_kg_can_eat
            eating_bonus_energy = ate_kg * health_bonus_percentage * 100
            
            # Aplicar bonus específico de la estrella si está configurado
            star_energy_bonus = params['energy_bonus']
            total_energy_gained_eating = base_energy_star + eating_bonus_energy + radius_bonus_energy + star_energy_bonus
            energy_after_eating = min(100.0, current_energy + total_energy_gained_eating)
        
        # Cálculos de investigación usando parámetros configurables
        research_energy_rate = params['energy_consumption_rate']
        energy_consumed_research = time_researching * research_energy_rate
        final_energy = max(0.0, energy_after_eating - energy_consumed_research)
        
        return StarAction(
            star_id=star.id,
            star_label=star.label,
            arrived_energy=arrived_energy,
            available_grass=current_grass,
            can_eat=can_eat,
            total_time_star=total_time_star,
            time_eating=time_eating,
            time_researching=time_researching,
            max_kg_can_eat=max_kg_can_eat,
            ate_kg=ate_kg,
            base_energy_star=base_energy_star,
            health_bonus_percentage=health_bonus_percentage,
            eating_bonus_energy=eating_bonus_energy,
            radius_bonus_energy=radius_bonus_energy,
            total_energy_gained_eating=total_energy_gained_eating,
            energy_consumed_research=energy_consumed_research,
            energy_after_eating=energy_after_eating,
            final_energy=final_energy,
            total_grass_consumed=ate_kg
        )
    
    def _build_adjacency_graph(self) -> Dict[str, List[Tuple[Route, str]]]:
        """Construye el grafo de adyacencia para navegación rápida."""
        adjacency = {}
        for route in self.space_map.routes:
            if route.blocked:
                continue
            a = route.from_star.id
            b = route.to_star.id
            adjacency.setdefault(a, []).append((route, b))
            adjacency.setdefault(b, []).append((route, a))
        return adjacency
    
    def _find_next_optimal_star(self, current_star: Star, visited: Set[str],
                               current_energy: float, current_grass: float,
                               remaining_life: float, age_factor: float,
                               adjacency: Dict) -> Tuple[Optional[Star], float]:
        """
        Encuentra la siguiente estrella óptima usando criterio de menor gasto.
        """
        best_star = None
        best_cost = float('inf')
        
        # Evaluar todas las estrellas vecinas no visitadas
        for route, neighbor_id in adjacency.get(current_star.id, []):
            if neighbor_id in visited:
                continue
            
            neighbor_star = self.space_map.get_star(neighbor_id)
            if not neighbor_star:
                continue
            
            # Calcular costo de viaje
            travel_cost = route.distance
            energy_cost = int(travel_cost * 0.1 * age_factor)
            travel_time = travel_cost / self.warp_factor
            
            # Verificar viabilidad del viaje
            if energy_cost > current_energy or travel_time > remaining_life:
                continue
            
            # Calcular "costo total" considerando beneficios potenciales
            total_cost = self._calculate_total_cost(
                travel_cost, energy_cost, neighbor_star, current_energy - energy_cost
            )
            
            if total_cost < best_cost:
                best_cost = total_cost
                best_star = neighbor_star
        
        return best_star, best_cost if best_star else (None, 0)
    
    def _calculate_total_cost(self, travel_distance: float, energy_cost: int,
                             target_star: Star, energy_after_travel: float) -> float:
        """
        Calcula el costo total considerando distancia, energía y beneficios potenciales.
        """
        base_cost = travel_distance + energy_cost * 2  # Peso doble a la energía
        
        # Descuento si puede comer en la estrella (energía < 50%)
        if energy_after_travel < 50.0:
            # Mayor valor para estrellas que dan más energía
            energy_benefit = target_star.amount_of_energy * 5
            base_cost -= energy_benefit
        
        # Penalización por radio pequeño (menos eficiente)
        radius_penalty = max(0, 1.0 - target_star.radius) * 10
        base_cost += radius_penalty
        
        return max(0.1, base_cost)  # Evitar costos negativos o cero


def main():
    """Función principal para ejecutar desde línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Calcular ruta de menor gasto posible visitando máximo estrellas'
    )
    parser.add_argument('--start', required=True, help='ID de estrella de inicio')
    parser.add_argument('--config', default='data/spaceship_config.json',
                       help='Ruta al archivo de configuración')
    
    args = parser.parse_args()
    
    # Cargar mapa espacial
    space_map = SpaceMap('data/constellations.json')
    
    # Crear calculador
    calculator = MinCostRouteCalculator(space_map, args.config)
    
    # Calcular ruta
    result = calculator.calculate_min_cost_route(args.start)
    
    # Formatear resultado para salida
    output = {
        'route_proposed': result.route_sequence,
        'star_actions_summary': [
            {
                'star_id': action.star_id,
                'star_label': action.star_label,
                'arrived_energy': round(action.arrived_energy, 2),
                'can_eat': action.can_eat,
                'ate_kg': round(action.ate_kg, 2),
                'energy_gained_eating': round(action.total_energy_gained_eating, 2),
                'time_eating': round(action.time_eating, 2),
                'time_researching': round(action.time_researching, 2),
                'energy_consumed_research': round(action.energy_consumed_research, 2),
                'final_energy': round(action.final_energy, 2)
            }
            for action in result.star_actions
        ],
        'star_actions_detailed': [action.to_detailed_dict() for action in result.star_actions],
        'total_grass_consumed': round(result.total_grass_consumed, 2),
        'final_energy': round(result.final_energy, 2),
        'remaining_life': round(result.remaining_life, 2),
        'total_distance': result.total_distance,
        'life_consumed': result.life_consumed,
        'success': result.success
    }
    
    if result.error_message:
        output['error'] = result.error_message
    
    print(json.dumps(output, indent=2, ensure_ascii=False))
    
    # Mostrar resumen
    print("\n" + "="*60)
    print("RESUMEN - RUTA DE MENOR GASTO POSIBLE")
    print("="*60)
    print(f"Estrellas visitadas: {len(result.route_sequence)}")
    print(f"Pasto total consumido: {result.total_grass_consumed:.2f} kg")
    print(f"Energía final: {result.final_energy:.2f}%")
    print(f"Vida restante: {result.remaining_life:.2f} años")
    print(f"Distancia total: {result.total_distance} años luz")
    print(f"Tiempo de vida consumido: {result.life_consumed:.2f} años")
    print(f"Éxito: {'Sí' if result.success else 'No'}")
    print("="*60)
    
    # Mostrar análisis detallado paso a paso
    if result.success and result.star_actions:
        print("\n" + "="*80)
        print("🔬 ANÁLISIS DETALLADO PASO A PASO POR ESTRELLA")
        print("="*80)
        
        for i, action in enumerate(result.star_actions, 1):
            detailed = action.to_detailed_dict()
            
            print(f"\n⭐ ESTRELLA {i}: {detailed['star_info']['label']} (ID: {detailed['star_info']['id']})")
            print("─" * 60)
            
            # Estado inicial
            print(f"🔋 ESTADO INICIAL:")
            print(f"   Energía al llegar: {detailed['initial_state']['arrived_energy']}%")
            print(f"   Pasto disponible: {detailed['initial_state']['available_grass']} kg")
            
            # Análisis de comer
            print(f"\n🍽️  ANÁLISIS DE ALIMENTACIÓN:")
            eat_calc = detailed['eating_analysis']['calculations']
            print(f"   Puede comer: {detailed['eating_analysis']['can_eat']} ({detailed['eating_analysis']['reason']})")
            print(f"   Máximo puede comer: {eat_calc['max_kg_can_eat']} kg")
            print(f"   Realmente comió: {eat_calc['actually_ate_kg']} kg")
            
            if eat_calc['actually_ate_kg'] > 0:
                print(f"   💡 Cálculo energía ganada:")
                print(f"      Base estrella: {eat_calc['base_energy_from_star']}%")
                print(f"      Bonus salud ({eat_calc['health_bonus_rate']}): {eat_calc['eating_bonus_energy']}%")
                print(f"      Bonus radio: {eat_calc['radius_bonus_energy']}%")
                print(f"      TOTAL ganado: {eat_calc['total_energy_gained']}%")
            
            # Distribución de tiempo
            print(f"\n⏱️  DISTRIBUCIÓN DE TIEMPO:")
            time_dist = detailed['time_distribution']
            print(f"   Tiempo total en estrella: {time_dist['total_time_at_star']}")
            print(f"   Tiempo comiendo: {time_dist['time_eating']} ({time_dist['eating_percentage']})")
            print(f"   Tiempo investigando: {time_dist['time_researching']} ({time_dist['research_percentage']})")
            
            # Cálculo investigación
            print(f"\n🔬 CÁLCULO INVESTIGACIÓN:")
            research = detailed['research_calculations']
            print(f"   Fórmula: {research['formula']}")
            print(f"   Energía consumida: {research['energy_consumed']}%")
            
            # Flujo de energía
            print(f"\n🔄 FLUJO DE ENERGÍA:")
            energy_flow = detailed['energy_flow']
            print(f"   Inicial: {energy_flow['initial_energy']}%")
            print(f"   Después de comer: {energy_flow['energy_after_eating']}%")
            print(f"   Después de investigar: {energy_flow['final_energy']}%")
            print(f"   Cambio neto: {energy_flow['net_energy_change']:+.1f}%")
            
            # Consumo recursos
            print(f"\n🌱 RECURSOS:")
            resources = detailed['resource_consumption']
            print(f"   Pasto usado aquí: {resources['grass_consumed_this_star']} kg")
            print(f"   Pasto restante: {resources['grass_remaining']} kg")
            
            if i < len(result.star_actions):
                print(f"\n   ➡️  Preparándose para viajar a siguiente estrella...")
        
        print("\n" + "="*80)


if __name__ == '__main__':
    main()