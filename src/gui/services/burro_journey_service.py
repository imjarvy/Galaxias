"""
Burro Journey Service.
Implementa la lógica unificada del viaje del burro según especificaciones del JSON.
Sigue principios SOLID - Single Responsibility para manejo de lógica de viaje.
"""

from typing import List, Dict, Optional, Tuple
from ...core import Star, BurroAstronauta
from src.utils.burro_utils.journey_step import JourneyStep
from src.utils.burro_utils.burro_math import calculate_eating_capacity, calculate_energy_from_eating, calculate_research_effects




class BurroJourneyService:
    """Servicio unificado para manejar toda la lógica del viaje del burro."""
    
    def __init__(self, space_map):
        self.space_map = space_map
        
        # Cargar configuración del JSON
        self._load_json_config()
    
    def _load_json_config(self):
        """Carga la configuración inicial del JSON."""
        burro_data = self.space_map.burro_data
        
        self.initial_energy = float(burro_data['burroenergiaInicial'])
        self.initial_grass = float(burro_data['pasto'])
        self.initial_health = burro_data['estadoSalud'].lower()
        self.start_age = float(burro_data['startAge'])
        self.death_age = float(burro_data['deathAge'])
        self.initial_life_remaining = self.death_age - self.start_age
        
        # Configuraciones fijas según especificación
        self.energy_eating_threshold = 50.0
        self.eating_time_percentage = 0.5  # 50% para comer
        self.research_time_percentage = 0.5  # 50% para investigar
        self.hypergiant_energy_bonus_percentage = 0.5  # +50%
        self.hypergiant_grass_multiplier = 2.0  # Duplica
        
        # Bonus de salud por kg de pasto
        self.health_bonuses = {
            'excelente': 0.05,  # +5%
            'buena': 0.04,      # +4%
            'mala': 0.03,       # +3%
            'moribundo': 0.02,  # +2%
            'muerto': 0.00      # 0%
        }
    
    def get_health_bonus_percentage(self, health_state: str) -> float:
        """Obtiene el bonus de energía por kg según estado de salud."""
        return self.health_bonuses.get(health_state.lower(), 0.02)
    
    
    def update_health_state(self, current_energy: float, current_life: float) -> str:
        """Actualiza el estado de salud basado en energía y tiempo de vida."""
        if current_life <= 0:
            return "muerto"
        
        if current_energy <= 0:
            return "muerto"
        elif current_energy <= 25:
            return "moribundo"
        elif current_energy <= 50:
            return "mala"
        elif current_energy <= 75:
            return "buena"
        else:
            return "excelente"
    
    def calculate_travel_cost(self, distance: float, age: float) -> Tuple[float, float]:
        """Calcula el costo de viajar entre estrellas."""
        # Factor de edad como estaba implementado
        age_factor = max(1.0, (age - 5) / 10.0)
        
        # Energía consumida por viaje
        energy_consumed = distance * 0.1 * age_factor
        
        # Tiempo de vida consumido por distancia
        life_consumed = distance * 0.01  # 1% del distance en años
        
        return energy_consumed, life_consumed
    
    def process_star_visit(self, star: Star, current_energy: float, current_grass: float, 
                          current_health: str, current_life: float, current_age: float) -> JourneyStep:
        """Procesa una visita completa a una estrella con toda la lógica."""
        
        # Estado al llegar
        energy_on_arrival = current_energy
        grass_on_arrival = current_grass
        health_on_arrival = current_health
        life_on_arrival = current_life
        
        # Análisis de tiempo en la estrella
        total_stay_time = star.radius
        eating_time_available = total_stay_time * self.eating_time_percentage
        research_time = total_stay_time * self.research_time_percentage
        
        # Decisión de comer
        should_eat = current_energy < self.energy_eating_threshold
        kg_capacity = calculate_eating_capacity(star, eating_time_available)
        can_eat = should_eat and current_grass >= kg_capacity and kg_capacity > 0
        kg_actually_eaten = kg_capacity if can_eat else 0.0
        energy_gained_eating = 0.0
        if can_eat:
            health_bonus = self.get_health_bonus_percentage(current_health)
            energy_gained_eating = calculate_energy_from_eating(
                star, kg_actually_eaten, health_bonus
            )
            current_energy = min(100.0, current_energy + energy_gained_eating)
            current_grass -= kg_actually_eaten
        energy_consumed_research, life_effect_research = calculate_research_effects(star)
        current_energy = max(0.0, current_energy - energy_consumed_research)
        current_life += life_effect_research
        
        # Efectos de hipergigante
        is_hypergiant = star.hypergiant
        hypergiant_energy_bonus = 0.0
        hypergiant_grass_bonus = 0.0
        
        if is_hypergiant:
            # +50% de la energía actual
            hypergiant_energy_bonus = current_energy * self.hypergiant_energy_bonus_percentage
            current_energy = min(100.0, current_energy + hypergiant_energy_bonus)
            
            # Duplica el pasto
            hypergiant_grass_bonus = current_grass
            current_grass *= self.hypergiant_grass_multiplier
        
        # Actualizar estado de salud
        new_health = self.update_health_state(current_energy, current_life)
        
        return JourneyStep(
            star=star,
            step_number=0,  # Se asignará externamente
            energy_on_arrival=energy_on_arrival,
            grass_on_arrival=grass_on_arrival,
            health_on_arrival=health_on_arrival,
            life_remaining_on_arrival=life_on_arrival,
            total_stay_time=total_stay_time,
            eating_time_available=eating_time_available,
            research_time=research_time,
            should_eat=should_eat,
            can_eat=can_eat,
            kg_to_eat=kg_capacity,
            kg_actually_eaten=kg_actually_eaten,
            energy_gained_eating=energy_gained_eating,
            health_bonus_percentage=self.get_health_bonus_percentage(current_health),
            energy_consumed_research=energy_consumed_research,
            life_effect_research=life_effect_research,
            is_hypergiant=is_hypergiant,
            hypergiant_energy_bonus=hypergiant_energy_bonus,
            hypergiant_grass_bonus=hypergiant_grass_bonus,
            energy_after_star=current_energy,
            grass_after_star=current_grass,
            health_after_star=new_health,
            life_remaining_after_star=current_life
        )
    
    def simulate_journey(self, path: List[Star], burro: BurroAstronauta) -> List[JourneyStep]:
        """Simula un viaje completo aplicando toda la lógica unificada, usando el estado actual del burro."""
        if not path:
            return []
        try:
            # Usar los valores actuales del burro, no los del JSON
            current_energy = burro.current_energy
            current_grass = burro.current_pasto
            current_health = burro.estado_salud
            current_age = burro.current_age
            # Calcular vida restante según edad actual
            current_life = self.death_age - current_age
            journey_steps = []
            for i, star in enumerate(path):
                try:
                    if i > 0:
                        prev_star = path[i-1]
                        travel_distance = self._get_travel_distance(prev_star, star)
                        if travel_distance:
                            energy_cost, life_cost = self.calculate_travel_cost(travel_distance, current_age)
                            current_energy = max(0.0, current_energy - energy_cost)
                            current_life = max(0.0, current_life - life_cost)
                            current_age += life_cost
                            current_health = self.update_health_state(current_energy, current_life)
                            if journey_steps:
                                journey_steps[-1].travel_distance_next = travel_distance
                                journey_steps[-1].energy_consumed_travel = energy_cost
                                journey_steps[-1].life_consumed_travel = life_cost
                    if current_health == "muerto":
                        break
                    step = self.process_star_visit(
                        star, current_energy, current_grass, current_health, current_life, current_age
                    )
                    step.step_number = i + 1
                    journey_steps.append(step)
                    current_energy = step.energy_after_star
                    current_grass = step.grass_after_star
                    current_health = step.health_after_star
                    current_life = step.life_remaining_after_star
                    if current_health == "muerto":
                        break
                except Exception as e:
                    print(f"Error procesando estrella {star.label}: {e}")
                    return journey_steps
            return journey_steps
        except Exception as e:
            print(f"Error general en simulate_journey: {e}")
            return []
    
    def _get_travel_distance(self, from_star: Star, to_star: Star) -> Optional[float]:
        """Obtiene la distancia de viaje entre dos estrellas."""
        for route_info in from_star.linked_to:
            # route_info es un dict con keys como 'starId', 'distance'
            if route_info.get('starId') == int(to_star.id):
                return float(route_info.get('distance', 0))
        return None
    
    def reset_burro_to_json_values(self, burro: BurroAstronauta):
        """Resetea el burro a los valores iniciales del JSON."""
        burro.current_energy = self.initial_energy
        burro.current_pasto = self.initial_grass
        burro.estado_salud = self.initial_health
        burro.current_age = self.start_age
        burro.total_life_consumed = 0.0
        burro.journey_history = []
        burro.current_location = None
    
    def apply_journey_to_burro(self, burro: BurroAstronauta, journey_steps: List[JourneyStep]):
        """Aplica los resultados del viaje al burro."""
        if not journey_steps:
            return
        
        final_step = journey_steps[-1]
        
        # Aplicar estado final
        burro.current_energy = final_step.energy_after_star
        burro.current_pasto = final_step.grass_after_star
        burro.estado_salud = final_step.health_after_star
        burro.current_age = self.start_age + (self.initial_life_remaining - final_step.life_remaining_after_star)
        burro.total_life_consumed = self.initial_life_remaining - final_step.life_remaining_after_star
        
        # Agregar estrellas al historial de viaje
        burro.journey_history = [step.star for step in journey_steps]
        burro.current_location = final_step.star
    
    def get_journey_summary(self, journey_steps: List[JourneyStep]) -> Dict:
        """Genera un resumen del viaje."""
        if not journey_steps:
            return {
                'success': False,
                'error': 'No se pudieron procesar estrellas'
            }
        
        final_step = journey_steps[-1]
        total_grass_consumed = self.initial_grass - final_step.grass_after_star
        total_life_consumed = self.initial_life_remaining - final_step.life_remaining_after_star
        
        return {
            'success': final_step.health_after_star != "muerto",
            'stars_visited': len(journey_steps),
            'initial_energy': self.initial_energy,
            'final_energy': final_step.energy_after_star,
            'initial_grass': self.initial_grass,
            'final_grass': final_step.grass_after_star,
            'total_grass_consumed': total_grass_consumed,
            'initial_health': self.initial_health,
            'final_health': final_step.health_after_star,
            'initial_life': self.initial_life_remaining,
            'final_life': final_step.life_remaining_after_star,
            'total_life_consumed': total_life_consumed,
            'path_labels': [step.star.label for step in journey_steps]
        }