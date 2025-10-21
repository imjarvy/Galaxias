"""
Core classes for the Galaxias space route simulation system.
"""
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import math


@dataclass
class Star:
    """Represents a star in a constellation."""
    id: str
    name: str
    x: float
    y: float
    type: str
    distance_ly: float
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Star):
            return self.id == other.id
        return False


@dataclass
class Route:
    """Represents a route between two stars."""
    from_star: Star
    to_star: Star
    distance: float
    danger_level: int
    blocked: bool = False
    blocked_by_comet: str = ""
    
    def calculate_cost(self, fuel_rate: float, danger_penalty: float) -> float:
        """Calculate the total cost of traveling this route."""
        base_cost = self.distance * fuel_rate
        danger_cost = self.danger_level * danger_penalty
        return base_cost + danger_cost if not self.blocked else float('inf')


@dataclass
class SpaceshipDonkey:
    """Represents the astronaut donkey and its spaceship."""
    name: str
    health: float
    fuel: float
    food: float
    oxygen: float
    current_location: Optional[Star] = None
    journey_history: List[Star] = field(default_factory=list)
    
    def consume_resources(self, distance: float, danger: int, config: Dict):
        """Consume resources based on travel distance and danger."""
        rates = config['consumption_rates']
        self.fuel -= distance * rates['fuel_per_unit_distance']
        self.food -= distance * rates['food_per_unit_distance']
        self.oxygen -= distance * rates['oxygen_per_unit_distance']
        self.health -= danger * rates['health_decay_per_danger']
        
        # Clamp values to non-negative
        self.fuel = max(0, self.fuel)
        self.food = max(0, self.food)
        self.oxygen = max(0, self.oxygen)
        self.health = max(0, self.health)
    
    def is_alive(self) -> bool:
        """Check if the donkey astronaut is still alive."""
        return self.health > 0 and self.oxygen > 0
    
    def can_travel(self, distance: float, config: Dict) -> bool:
        """Check if the donkey has enough resources to travel."""
        rates = config['consumption_rates']
        required_fuel = distance * rates['fuel_per_unit_distance']
        required_food = distance * rates['food_per_unit_distance']
        required_oxygen = distance * rates['oxygen_per_unit_distance']
        
        return (self.fuel >= required_fuel and 
                self.food >= required_food and 
                self.oxygen >= required_oxygen and 
                self.is_alive())
    
    def refuel(self, fuel: float = 500, food: float = 25, oxygen: float = 50):
        """Refuel the spaceship at a star station."""
        self.fuel += fuel
        self.food += food
        self.oxygen += oxygen
    
    def get_status(self) -> Dict:
        """Get current status of the spaceship."""
        return {
            'name': self.name,
            'health': round(self.health, 2),
            'fuel': round(self.fuel, 2),
            'food': round(self.food, 2),
            'oxygen': round(self.oxygen, 2),
            'location': self.current_location.name if self.current_location else 'Unknown',
            'journey_length': len(self.journey_history)
        }


@dataclass
class Comet:
    """Represents a comet that can block routes."""
    name: str
    blocked_routes: List[Tuple[str, str]] = field(default_factory=list)
    
    def blocks_route(self, from_id: str, to_id: str) -> bool:
        """Check if this comet blocks a specific route."""
        return ((from_id, to_id) in self.blocked_routes or 
                (to_id, from_id) in self.blocked_routes)


class SpaceMap:
    """Represents the entire space map with stars and routes."""
    
    def __init__(self, data_path: str = "data/constellations.json"):
        self.stars: Dict[str, Star] = {}
        self.routes: List[Route] = []
        self.comets: List[Comet] = []
        self.load_data(data_path)
    
    def load_data(self, data_path: str):
        """Load constellation and route data from JSON."""
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        # Load stars
        for constellation in data['constellations']:
            for star_data in constellation['stars']:
                star = Star(**star_data)
                self.stars[star.id] = star
        
        # Load routes
        for route_data in data['routes']:
            from_star = self.stars[route_data['from']]
            to_star = self.stars[route_data['to']]
            route = Route(
                from_star=from_star,
                to_star=to_star,
                distance=route_data['distance'],
                danger_level=route_data['danger_level']
            )
            self.routes.append(route)
    
    def get_star(self, star_id: str) -> Optional[Star]:
        """Get a star by its ID."""
        return self.stars.get(star_id)
    
    def get_routes_from(self, star: Star) -> List[Route]:
        """Get all routes starting from a given star."""
        return [r for r in self.routes if r.from_star == star or r.to_star == star]
    
    def add_comet(self, comet: Comet):
        """Add a comet that blocks certain routes."""
        self.comets.append(comet)
        # Update route blocking status
        for route in self.routes:
            if comet.blocks_route(route.from_star.id, route.to_star.id):
                route.blocked = True
                route.blocked_by_comet = comet.name
    
    def remove_comet(self, comet_name: str):
        """Remove a comet and unblock its routes."""
        comet_to_remove = None
        for comet in self.comets:
            if comet.name == comet_name:
                comet_to_remove = comet
                break
        
        if comet_to_remove:
            self.comets.remove(comet_to_remove)
            # Unblock routes
            for route in self.routes:
                if route.blocked_by_comet == comet_name:
                    route.blocked = False
                    route.blocked_by_comet = ""
    
    def get_all_stars_list(self) -> List[Star]:
        """Get a list of all stars."""
        return list(self.stars.values())
