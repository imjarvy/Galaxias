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
    label: str
    x: float
    y: float
    radius: float
    time_to_eat: int
    amount_of_energy: int
    hypergiant: bool
    linked_to: List[Dict] = field(default_factory=list)
    
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
class BurroAstronauta:
    """Represents the astronaut donkey based on the JSON structure."""
    name: str
    energia_inicial: int
    estado_salud: str
    pasto: int
    start_age: int
    death_age: int
    current_location: Optional[Star] = None
    journey_history: List[Star] = field(default_factory=list)
    current_energy: int = 0
    current_pasto: int = 0
    
    # Nuevos campos para monitoreo de vida
    current_age: float = 0.0  # Edad actual considerando tiempo transcurrido
    total_life_consumed: float = 0.0  # Total de vida consumida en años
    life_monitor = None  # Instancia del monitor de vida (se asigna externamente)
    
    def __post_init__(self):
        """Initialize current values from initial values."""
        if self.current_energy == 0:
            self.current_energy = self.energia_inicial
        if self.current_pasto == 0:
            self.current_pasto = self.pasto
        if self.current_age == 0.0:
            self.current_age = float(self.start_age)
    
    def consume_resources_eating_star(self, star: Star):
        """Consume resources when eating a star."""
        # Consume grass based on star's eating time
        grass_consumed = star.time_to_eat * 5  # 5 kg per time unit
        self.current_pasto = max(0, self.current_pasto - grass_consumed)
        
        # Gain energy based on star's energy amount
        energy_gained = star.amount_of_energy * 10
        # Bigger stars (radius) give more energy
        energy_bonus = int(star.radius * 5)
        
        total_energy_gain = energy_gained + energy_bonus
        self.current_energy = min(100, self.current_energy + total_energy_gain)
        
        # Update health state based on energy
        self._update_health_state()
    
    def consume_resources_traveling(self, distance: float):
        """Consume resources when traveling between stars."""
        # Energy consumed based on distance and age
        age_factor = max(1, (self.start_age - 5) / 10)  # Older donkeys consume more
        energy_consumed = int(distance * 0.1 * age_factor)
        
        self.current_energy = max(0, self.current_energy - energy_consumed)
        
        # Nuevo: Consumir tiempo de vida si hay monitor activo
        if self.life_monitor and self.life_monitor.is_monitoring:
            life_info = self.life_monitor.consume_life_for_travel(distance)
            self.current_age = life_info['current_age']
            self.total_life_consumed += life_info['life_consumed']
            
            # Verificar si murió por edad
            if life_info['death_imminent']:
                self.estado_salud = "muerto"
        
        self._update_health_state()
    
    def _update_health_state(self):
        """Update health state based on current energy."""
        if self.current_energy <= 0:
            self.estado_salud = "muerto"
        elif self.current_energy <= 25:
            self.estado_salud = "moribundo"
        elif self.current_energy <= 50:
            self.estado_salud = "mala"
        elif self.current_energy <= 75:
            self.estado_salud = "buena"
        else:
            self.estado_salud = "excelente"
    
    def is_alive(self) -> bool:
        """Check if the donkey astronaut is still alive."""
        # Revisar estado de salud Y vida restante
        alive_by_health = self.estado_salud != "muerto" and self.current_pasto > 0
        alive_by_age = self.current_age < self.death_age
        return alive_by_health and alive_by_age
    
    def get_health_state(self) -> str:
        """Get the current health state of the donkey."""
        return self.estado_salud
    
    def get_burro_energia(self) -> int:
        """Get the burro energy percentage (1-100)."""
        return self.current_energy
    
    def can_travel(self, distance: float) -> bool:
        """Check if the donkey has enough resources to travel."""
        if not self.is_alive():
            return False
        
        age_factor = max(1, (self.start_age - 5) / 10)
        energy_needed = int(distance * 0.1 * age_factor)
        
        return self.current_energy > energy_needed and self.current_pasto > 0
    
    def can_eat_star(self, star: Star) -> bool:
        """Check if the donkey can eat a star."""
        grass_needed = star.time_to_eat * 5
        return self.current_pasto >= grass_needed and self.is_alive()
    
    def restore_resources(self):
        """Restore resources to initial values."""
        self.current_energy = self.energia_inicial
        self.current_pasto = self.pasto
        self.current_age = float(self.start_age)
        self.total_life_consumed = 0.0
        self.estado_salud = "excelente" if self.current_energy > 75 else "buena"
        
        # Reiniciar monitor de vida si existe
        if self.life_monitor:
            self.life_monitor.start_monitoring(self.current_age, self.death_age)
    
    def get_status(self) -> Dict:
        """Get current status of the donkey."""
        status = {
            'name': self.name,
            'energia': self.current_energy,
            'estado_salud': self.estado_salud,
            'pasto': self.current_pasto,
            'edad_inicial': self.start_age,
            'edad_actual': self.current_age,
            'edad_muerte': self.death_age,
            'vida_restante': max(0, self.death_age - self.current_age),
            'vida_consumida': self.total_life_consumed,
            'location': self.current_location.label if self.current_location else 'Unknown',
            'journey_length': len(self.journey_history),
            'is_alive': self.is_alive()
        }
        
        # Agregar información del monitor si existe
        if self.life_monitor:
            life_status = self.life_monitor.get_status()
            status.update({
                'life_monitor_active': life_status['is_monitoring'],
                'life_percentage': life_status['life_percentage']
            })
        
        return status

    def set_life_monitor(self, life_monitor):
        """
        Configura el monitor de vida para este burro astronauta.
        
        Args:
            life_monitor: Instancia de LifeMonitor
        """
        self.life_monitor = life_monitor
        if life_monitor and not life_monitor.is_monitoring:
            life_monitor.start_monitoring(self.current_age, self.death_age)
    
    def get_remaining_life(self) -> float:
        """Obtiene el tiempo de vida restante en años."""
        return max(0, self.death_age - self.current_age)
    
    def get_life_percentage(self) -> float:
        """Obtiene el porcentaje de vida restante."""
        total_expected_life = self.death_age - self.start_age
        life_used = self.current_age - self.start_age
        if total_expected_life <= 0:
            return 0.0
        return max(0, ((total_expected_life - life_used) / total_expected_life) * 100)
    
    def calculate_travel_life_cost(self, distance: float) -> float:
        """
        Calcula cuánto tiempo de vida costará un viaje sin ejecutarlo.
        
        Args:
            distance: Distancia del viaje
            
        Returns:
            float: Tiempo de vida que consumirá el viaje en años
        """
        if self.life_monitor:
            return self.life_monitor.calculator.distance_to_life_years(distance)
        else:
            # Fallback: usar warp_factor por defecto
            try:
                import json
                with open("data/spaceship_config.json", 'r') as f:
                    config = json.load(f)
                warp_factor = config.get('scientific_parameters', {}).get('warp_factor', 1.0)
                return distance / warp_factor
            except:
                return distance  # Sin warp_factor, 1:1
    
    def can_survive_travel(self, distance: float) -> bool:
        """
        Verifica si el burro puede sobrevivir un viaje de cierta distancia.
        
        Args:
            distance: Distancia del viaje
            
        Returns:
            bool: True si puede sobrevivir el viaje
        """
        if not self.is_alive():
            return False
        
        # Verificar energía para el viaje (recursos regulares)
        age_factor = max(1, (self.start_age - 5) / 10)
        energy_needed = int(distance * 0.1 * age_factor)
        
        if self.current_energy <= energy_needed or self.current_pasto <= 0:
            return False
        
        # Verificar si tendrá vida suficiente
        life_cost = self.calculate_travel_life_cost(distance)
        remaining_after_travel = self.get_remaining_life() - life_cost
        
        return remaining_after_travel > 0


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
        self.burro_data: Dict = {}
        self.load_data(data_path)
    
    def load_data(self, data_path: str):
        """Load constellation and route data from JSON."""
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        # Load burro data
        self.burro_data = {
            'burroenergiaInicial': data.get('burroenergiaInicial', 100),
            'estadoSalud': data.get('estadoSalud', 'Excelente'),
            'pasto': data.get('pasto', 300),
            'startAge': data.get('startAge', 12),
            'deathAge': data.get('deathAge', 3567),
            'number': data.get('number', 123)
        }

        # Load stars from constellations
        for constellation in data.get('constellations', []):
            for start_data in constellation.get('starts', []):
                star_id = str(start_data['id'])
                star = Star(
                    id=star_id,
                    label=start_data.get('label', star_id),
                    x=float(start_data.get('coordenates', {}).get('x', 0)),
                    y=float(start_data.get('coordenates', {}).get('y', 0)),
                    radius=float(start_data.get('radius', 0.5)),
                    time_to_eat=int(start_data.get('timeToEat', 1)),
                    amount_of_energy=int(start_data.get('amountOfEnergy', 1)),
                    hypergiant=bool(start_data.get('hypergiant', False)),
                    linked_to=start_data.get('linkedTo', [])
                )
                self.stars[star_id] = star

        # Build routes from linkedTo connections
        seen_edges = set()
        for star in self.stars.values():
            for link in star.linked_to:
                to_star_id = str(link['starId'])
                distance = float(link['distance'])
                
                edge_key = tuple(sorted((star.id, to_star_id)))
                if edge_key in seen_edges:
                    continue
                seen_edges.add(edge_key)
                
                if to_star_id in self.stars:
                    to_star = self.stars[to_star_id]
                    danger_level = self._calculate_danger_level(distance)
                    
                    route = Route(
                        from_star=star,
                        to_star=to_star,
                        distance=distance,
                        danger_level=danger_level
                    )
                    self.routes.append(route)
    
    def _calculate_danger_level(self, distance: float) -> int:
        """Calculate danger level based on distance."""
        if distance < 50:
            return 1
        elif distance < 100:
            return 2
        elif distance < 150:
            return 3
        else:
            return 4
    
    def get_star(self, star_id: str) -> Optional[Star]:
        """Get a star by its ID."""
        return self.stars.get(str(star_id))
    
    def get_routes_from(self, star: Star) -> List[Route]:
        """Get all routes starting from or ending at a given star."""
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
    
    def create_burro_astronauta(self, name: str = "Burro Astronauta") -> 'BurroAstronauta':
        """Create a BurroAstronauta instance with data from JSON."""
        return BurroAstronauta(
            name=name,
            energia_inicial=self.burro_data['burroenergiaInicial'],
            estado_salud=self.burro_data['estadoSalud'].lower(),
            pasto=self.burro_data['pasto'],
            start_age=self.burro_data['startAge'],
            death_age=self.burro_data['deathAge']
        )
    
    def verificar_bidireccionalidad_enlaces(self) -> List[Tuple[int, int]]:
        """
        Verifica la bidireccionalidad de enlaces en el JSON.
        
        Returns:
            List[Tuple[int, int]]: Lista vacía si todo OK, 
                                  lista de pares (from_id, to_id) faltantes si hay incumplimiento
        """
        # Recopilar todos los enlaces existentes desde el JSON original
        enlaces_existentes = set()
        
        with open('data/constellations.json', 'r') as f:
            data = json.load(f)
        
        for constellation in data.get('constellations', []):
            for star_data in constellation.get('starts', []):
                star_id = star_data['id']
                
                for link in star_data.get('linkedTo', []):
                    to_star_id = link['starId']
                    enlaces_existentes.add((star_id, to_star_id))
        
        # Verificar qué enlaces inversos faltan
        pares_faltantes = []
        
        for (from_id, to_id) in enlaces_existentes:
            enlace_inverso = (to_id, from_id)
            if enlace_inverso not in enlaces_existentes:
                pares_faltantes.append(enlace_inverso)
        
        return pares_faltantes
