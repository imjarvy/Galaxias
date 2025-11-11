from dataclasses import dataclass
from typing import Optional
from ...core import Star

@dataclass
class JourneyStep:
    """Representa un paso del viaje con todos los cálculos detallados."""
    star: Star
    step_number: int
    energy_on_arrival: float
    grass_on_arrival: float
    health_on_arrival: str
    life_remaining_on_arrival: float
    total_stay_time: float
    eating_time_available: float
    research_time: float
    should_eat: bool
    can_eat: bool
    kg_to_eat: float
    kg_actually_eaten: float
    energy_gained_eating: float
    health_bonus_percentage: float
    energy_consumed_research: float
    life_effect_research: float
    is_hypergiant: bool
    hypergiant_energy_bonus: float
    hypergiant_grass_bonus: float
    energy_after_star: float
    grass_after_star: float
    health_after_star: str
    life_remaining_after_star: float
    travel_distance_next: Optional[float] = None
    energy_consumed_travel: Optional[float] = None
    life_consumed_travel: Optional[float] = None
