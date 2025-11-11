import math
from ...core import Star

def calculate_eating_capacity(star: Star, available_time: float) -> float:
    if star.time_to_eat <= 0:
        return 0.0
    kg_capacity = available_time / star.time_to_eat
    return math.floor(kg_capacity)

def calculate_energy_from_eating(star: Star, kg_eaten: float, health_bonus: float) -> float:
    if kg_eaten <= 0:
        return 0.0
    base_energy = star.amount_of_energy * 10
    eating_bonus = kg_eaten * health_bonus * 100
    radius_bonus = star.radius * 5
    total_energy = base_energy + eating_bonus + radius_bonus
    return total_energy

def calculate_research_effects(star: Star) -> tuple:
    energy_consumed = star.amount_of_energy * 2
    life_effect = 0.0
    return energy_consumed, life_effect
