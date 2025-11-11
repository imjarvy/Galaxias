"""
Sistema de gestión de rutas con impacto de cometas.
Maneja invalidación, recálculo y búsqueda de alternativas.
"""
from typing import List, Dict, Optional, Tuple, Callable
from dataclasses import dataclass
from src.models import Star, Route, SpaceMap, Comet


@dataclass
class RouteImpactResult:
    """Resultado del análisis de impacto de cometas en rutas."""
    path_invalidated: bool
    affected_segments: List[Tuple[str, str]]  # [(from_id, to_id), ...]
    alternative_routes: List[List[Star]]  # Lista de rutas alternativas
    recalculation_needed: bool
    impact_summary: str


@dataclass
class ActiveJourney:
    """Representa un viaje activo que puede ser impactado por cometas."""
    planned_path: List[Star]
    current_position: int  # Índice en planned_path
    origin: Star
    destination: Star
    journey_type: str  # "optimal", "max_visit", "min_cost"


class IRouteValidator:
    """Interface para validadores de rutas."""
    
    def validate_path(self, path: List[Star], space_map: SpaceMap) -> bool:
        """Valida si una ruta es completamente transitable."""
        raise NotImplementedError
    
    def find_blocked_segments(self, path: List[Star], space_map: SpaceMap) -> List[Tuple[str, str]]:
        """Encuentra segmentos bloqueados en una ruta."""
        raise NotImplementedError


class IRouteCalculator:
    """Interface para calculadores de rutas."""
    
    def calculate_route(self, origin: Star, destination: Star, space_map: SpaceMap) -> Optional[List[Star]]:
        """Calcula una ruta entre dos puntos."""
        raise NotImplementedError
    
    def calculate_alternative_routes(self, origin: Star, destination: Star, 
                                   space_map: SpaceMap, max_alternatives: int = 3) -> List[List[Star]]:
        """Calcula rutas alternativas."""
        raise NotImplementedError


class RouteValidator(IRouteValidator):
    """Validador básico de rutas."""
    
    def validate_path(self, path: List[Star], space_map: SpaceMap) -> bool:
        """Valida si una ruta es completamente transitable."""
        if not path or len(path) < 2:
            return True  # Ruta vacía o de un solo punto es válida
        
        for i in range(len(path) - 1):
            from_star = path[i]
            to_star = path[i + 1]
            
            # Buscar la ruta entre estas estrellas
            route = self._find_route_between(from_star, to_star, space_map)
            if not route or route.blocked:
                return False
        
        return True
    
    def find_blocked_segments(self, path: List[Star], space_map: SpaceMap) -> List[Tuple[str, str]]:
        """Encuentra segmentos bloqueados en una ruta."""
        blocked_segments = []
        
        if not path or len(path) < 2:
            return blocked_segments
        
        for i in range(len(path) - 1):
            from_star = path[i]
            to_star = path[i + 1]
            
            route = self._find_route_between(from_star, to_star, space_map)
            if route and route.blocked:
                blocked_segments.append((from_star.id, to_star.id))
        
        return blocked_segments
    
    def _find_route_between(self, from_star: Star, to_star: Star, space_map: SpaceMap) -> Optional[Route]:
        """Encuentra la ruta entre dos estrellas."""
        for route in space_map.routes:
            if ((route.from_star == from_star and route.to_star == to_star) or
                (route.from_star == to_star and route.to_star == from_star)):
                return route
        return None


class BasicRouteCalculator(IRouteCalculator):
    """Calculador básico de rutas usando Dijkstra."""
    
    def calculate_route(self, origin: Star, destination: Star, space_map: SpaceMap) -> Optional[List[Star]]:
        """Calcula una ruta usando el calculador existente."""
        try:
            # Usar el calculador existente del sistema
            from src.route_calculator import RouteCalculator
            calculator = RouteCalculator(space_map, {})
            path, _ = calculator.dijkstra(origin, destination)
            return path
        except:
            return None
    
    def calculate_alternative_routes(self, origin: Star, destination: Star, 
                                   space_map: SpaceMap, max_alternatives: int = 3) -> List[List[Star]]:
        """Calcula rutas alternativas bloqueando temporalmente rutas ya encontradas."""
        alternatives = []
        blocked_routes_backup = []
        
        try:
            # Encontrar múltiples rutas bloqueando temporalmente las ya encontradas
            for attempt in range(max_alternatives):
                path = self.calculate_route(origin, destination, space_map)
                
                if path and len(path) > 1:
                    alternatives.append(path)
                    
                    # Bloquear temporalmente esta ruta para encontrar alternativas
                    routes_to_block = []
                    for i in range(len(path) - 1):
                        from_star = path[i]
                        to_star = path[i + 1]
                        
                        for route in space_map.routes:
                            if ((route.from_star == from_star and route.to_star == to_star) or
                                (route.from_star == to_star and route.to_star == from_star)):
                                if not route.blocked:
                                    route.blocked = True
                                    routes_to_block.append(route)
                                    blocked_routes_backup.append(route)
                                break
                else:
                    break  # No más rutas disponibles
            
            # Restaurar rutas bloqueadas temporalmente
            for route in blocked_routes_backup:
                route.blocked = False
            
            return alternatives
            
        except Exception:
            # Restaurar rutas en caso de error
            for route in blocked_routes_backup:
                route.blocked = False
            return alternatives


class CometImpactManager:
    """Gestor principal del impacto de cometas en rutas planificadas."""
    
    def __init__(self, space_map: SpaceMap, 
                 route_validator: IRouteValidator = None,
                 route_calculator: IRouteCalculator = None):
        self.space_map = space_map
        self.route_validator = route_validator or RouteValidator()
        self.route_calculator = route_calculator or BasicRouteCalculator()
        self.active_journeys: List[ActiveJourney] = []
        self.impact_listeners: List[Callable[[RouteImpactResult], None]] = []
    
    def register_active_journey(self, planned_path: List[Star], current_position: int, 
                               journey_type: str = "unknown") -> None:
        """Registra un viaje activo que puede ser afectado por cometas."""
        if planned_path and len(planned_path) >= 2:
            journey = ActiveJourney(
                planned_path=planned_path,
                current_position=current_position,
                origin=planned_path[0],
                destination=planned_path[-1],
                journey_type=journey_type
            )
            self.active_journeys.append(journey)
    
    def add_impact_listener(self, listener: Callable[[RouteImpactResult], None]) -> None:
        """Agrega un listener para ser notificado de impactos de cometas."""
        self.impact_listeners.append(listener)
    
    def analyze_comet_impact(self, comet: Comet) -> RouteImpactResult:
        """Analiza el impacto de un cometa en rutas activas."""
        impact_result = RouteImpactResult(
            path_invalidated=False,
            affected_segments=[],
            alternative_routes=[],
            recalculation_needed=False,
            impact_summary=""
        )
        
        # Verificar impacto en viajes activos
        for journey in self.active_journeys:
            if self._journey_affected_by_comet(journey, comet):
                impact_result.path_invalidated = True
                impact_result.recalculation_needed = True
                
                # Encontrar segmentos afectados
                blocked_segments = self.route_validator.find_blocked_segments(
                    journey.planned_path, self.space_map)
                impact_result.affected_segments.extend(blocked_segments)
                
                # Calcular rutas alternativas
                alternatives = self.route_calculator.calculate_alternative_routes(
                    journey.origin, journey.destination, self.space_map)
                
                # Filtrar alternativas válidas (no bloqueadas)
                valid_alternatives = [alt for alt in alternatives 
                                    if self.route_validator.validate_path(alt, self.space_map)]
                impact_result.alternative_routes.extend(valid_alternatives)
        
        # Generar resumen
        impact_result.impact_summary = self._generate_impact_summary(impact_result)
        
        # Notificar listeners
        for listener in self.impact_listeners:
            try:
                listener(impact_result)
            except Exception:
                pass  # No fallar si un listener tiene problemas
        
        return impact_result
    
    def get_current_alternatives(self, origin_id: str, destination_id: str) -> List[List[Star]]:
        """Obtiene rutas alternativas actuales entre dos puntos."""
        origin = self.space_map.get_star(origin_id)
        destination = self.space_map.get_star(destination_id)
        
        if not origin or not destination:
            return []
        
        alternatives = self.route_calculator.calculate_alternative_routes(
            origin, destination, self.space_map)
        
        # Filtrar solo las rutas válidas (no bloqueadas)
        valid_alternatives = [alt for alt in alternatives 
                            if self.route_validator.validate_path(alt, self.space_map)]
        
        return valid_alternatives
    
    def clear_active_journeys(self) -> None:
        """Limpia todos los viajes activos."""
        self.active_journeys.clear()
    
    def _journey_affected_by_comet(self, journey: ActiveJourney, comet: Comet) -> bool:
        """Verifica si un viaje es afectado por un cometa."""
        for from_id, to_id in comet.blocked_routes:
            # Verificar si algún segmento del viaje usa esta ruta
            for i in range(len(journey.planned_path) - 1):
                current_from = journey.planned_path[i].id
                current_to = journey.planned_path[i + 1].id
                
                if ((current_from == from_id and current_to == to_id) or
                    (current_from == to_id and current_to == from_id)):
                    return True
        return False
    
    def _generate_impact_summary(self, impact_result: RouteImpactResult) -> str:
        """Genera un resumen del impacto."""
        if not impact_result.path_invalidated:
            return "✅ No hay impacto en rutas activas"
        
        summary_parts = []
        summary_parts.append(f"⚠️ Ruta invalidada por cometa")
        
        if impact_result.affected_segments:
            segments_str = ", ".join([f"{s[0]}→{s[1]}" for s in impact_result.affected_segments[:3]])
            summary_parts.append(f"📍 Segmentos afectados: {segments_str}")
        
        if impact_result.alternative_routes:
            summary_parts.append(f"🔄 {len(impact_result.alternative_routes)} rutas alternativas encontradas")
        else:
            summary_parts.append("❌ No se encontraron rutas alternativas")
        
        return "\n".join(summary_parts)