"""
Sistema de saltos hipergigantes para cambios de galaxia/constelación.

Implementa la lógica especial para viajes entre constelaciones:
- Detecta cuando un salto requiere cambio de constelación
- Fuerza el paso por una estrella hipergigante
- Aplica beneficios especiales: +50% energía, x2 pasto
- Permite selección de destino en la nueva galaxia
"""

import json
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass
from src.models import SpaceMap, Star, BurroAstronauta, Route


@dataclass
class HyperGiantJumpResult:
    """Resultado de un salto hipergigante."""
    success: bool
    hypergiant_used: Star
    destination_star: Star
    energy_before: float
    energy_after: float
    grass_before: float
    grass_after: float
    message: str
    available_destinations: List[Star] = None
    

class HyperGiantJumpSystem:
    """Sistema de gestión de saltos hipergigantes entre constelaciones."""
    
    def __init__(self, space_map: SpaceMap):
        self.space_map = space_map
        self.constellation_map = self._build_constellation_map()
        self.hypergiant_stars = self._find_hypergiant_stars()
        
    def _build_constellation_map(self) -> Dict[str, str]:
        """Construye mapeo de estrella_id -> nombre_constelación."""
        constellation_map = {}
        
        try:
            with open('data/constellations.json', 'r') as f:
                data = json.load(f)
            
            for constellation in data.get('constellations', []):
                constellation_name = constellation['name']
                for star_data in constellation.get('starts', []):
                    star_id = str(star_data['id'])
                    constellation_map[star_id] = constellation_name
                    
        except Exception as e:
            print(f"Error building constellation map: {e}")
            
        return constellation_map
    
    def _find_hypergiant_stars(self) -> List[Star]:
        """Encuentra todas las estrellas hipergigantes."""
        return [star for star in self.space_map.get_all_stars_list() 
                if star.hypergiant]
    
    def get_star_constellation(self, star: Star) -> Optional[str]:
        """Obtiene la constelación de una estrella."""
        return self.constellation_map.get(star.id)
    
    def requires_hypergiant_jump(self, from_star: Star, to_star: Star) -> bool:
        """
        Determina si un viaje requiere salto hipergigante (cambio de constelación).
        
        Args:
            from_star: Estrella de origen
            to_star: Estrella de destino
            
        Returns:
            bool: True si requiere salto hipergigante
        """
        from_constellation = self.get_star_constellation(from_star)
        to_constellation = self.get_star_constellation(to_star)
        
        # Requiere salto si están en diferentes constelaciones
        return (from_constellation is not None and 
                to_constellation is not None and 
                from_constellation != to_constellation)
    
    def find_accessible_hypergiants(self, from_star: Star) -> List[Tuple[Star, float]]:
        """
        Encuentra hipergigantes accesibles desde una estrella.
        
        Args:
            from_star: Estrella de origen
            
        Returns:
            List[Tuple[Star, float]]: Lista de (hipergigante, distancia)
        """
        accessible = []
        from_constellation = self.get_star_constellation(from_star)
        
        for hypergiant in self.hypergiant_stars:
            hypergiant_constellation = self.get_star_constellation(hypergiant)
            
            # Solo considerar hipergigantes de la misma constelación actual
            if hypergiant_constellation == from_constellation:
                # Buscar ruta directa
                for route in self.space_map.routes:
                    if route.blocked:
                        continue
                        
                    if ((route.from_star.id == from_star.id and route.to_star.id == hypergiant.id) or
                        (route.to_star.id == from_star.id and route.from_star.id == hypergiant.id)):
                        accessible.append((hypergiant, route.distance))
                        break
        
        # Ordenar por distancia
        accessible.sort(key=lambda x: x[1])
        return accessible
    
    def find_destination_options(self, target_constellation: str) -> List[Star]:
        """
        Encuentra estrellas de destino disponibles en una constelación.
        
        Args:
            target_constellation: Nombre de la constelación de destino
            
        Returns:
            List[Star]: Estrellas disponibles en la constelación
        """
        destinations = []
        
        for star in self.space_map.get_all_stars_list():
            if self.get_star_constellation(star) == target_constellation:
                destinations.append(star)
        
        return destinations
    
    def can_perform_hypergiant_jump(self, burro: BurroAstronauta, 
                                   hypergiant: Star, 
                                   distance_to_hypergiant: float) -> bool:
        """
        Verifica si el burro puede realizar un salto hipergigante.
        
        Args:
            burro: Burro astronauta
            hypergiant: Estrella hipergigante
            distance_to_hypergiant: Distancia a la hipergigante
            
        Returns:
            bool: True si puede realizar el salto
        """
        # Calcular costo de energía para llegar a la hipergigante
        age_factor = max(1.0, (burro.current_age - 5) / 10.0)
        energy_cost = int(distance_to_hypergiant * 0.1 * age_factor)
        
        # Verificar recursos suficientes
        has_energy = burro.current_energy > energy_cost
        has_life = burro.can_survive_travel(distance_to_hypergiant)
        
        return has_energy and has_life and burro.is_alive()
    
    def perform_hypergiant_jump(self, burro: BurroAstronauta, 
                               hypergiant: Star,
                               destination: Star,
                               distance_to_hypergiant: float) -> HyperGiantJumpResult:
        """
        Realiza un salto hipergigante completo con todos sus beneficios.
        
        Args:
            burro: Burro astronauta
            hypergiant: Estrella hipergigante para el salto
            destination: Estrella de destino en la nueva galaxia
            distance_to_hypergiant: Distancia a la hipergigante
            
        Returns:
            HyperGiantJumpResult: Resultado del salto
        """
        # Guardar estado inicial
        initial_energy = burro.current_energy
        initial_grass = burro.current_pasto
        
        # Verificar viabilidad
        if not self.can_perform_hypergiant_jump(burro, hypergiant, distance_to_hypergiant):
            return HyperGiantJumpResult(
                success=False,
                hypergiant_used=hypergiant,
                destination_star=destination,
                energy_before=initial_energy,
                energy_after=initial_energy,
                grass_before=initial_grass,
                grass_after=initial_grass,
                message="❌ Recursos insuficientes para el salto hipergigante"
            )
        
        try:
            # 1. Viajar a la hipergigante
            burro.consume_resources_traveling(distance_to_hypergiant)
            burro.current_location = hypergiant
            
            # 2. Aplicar beneficios del salto hipergigante
            # Recargar 50% del nivel actual de energía
            current_energy = burro.current_energy
            energy_boost = current_energy * 0.5
            burro.current_energy = min(100, current_energy + energy_boost)
            
            # Duplicar pasto en bodega
            burro.current_pasto *= 2
            
            # 3. Saltar a la nueva galaxia (destino)
            burro.current_location = destination
            
            # 4. Actualizar historial
            if hypergiant not in burro.journey_history:
                burro.journey_history.append(hypergiant)
            if destination not in burro.journey_history:
                burro.journey_history.append(destination)
            
            # Crear resultado exitoso
            return HyperGiantJumpResult(
                success=True,
                hypergiant_used=hypergiant,
                destination_star=destination,
                energy_before=initial_energy,
                energy_after=burro.current_energy,
                grass_before=initial_grass,
                grass_after=burro.current_pasto,
                message=(f"✨ SALTO HIPERGIGANTE EXITOSO!\n"
                        f"🌟 Hipergigante: {hypergiant.label}\n"
                        f"🎯 Destino: {destination.label}\n"
                        f"⚡ Energía: {initial_energy:.1f}% → {burro.current_energy:.1f}% (+{energy_boost:.1f}%)\n"
                        f"🌱 Pasto: {initial_grass:.1f}kg → {burro.current_pasto:.1f}kg (x2)")
            )
            
        except Exception as e:
            return HyperGiantJumpResult(
                success=False,
                hypergiant_used=hypergiant,
                destination_star=destination,
                energy_before=initial_energy,
                energy_after=burro.current_energy,
                grass_before=initial_grass,
                grass_after=burro.current_pasto,
                message=f"❌ Error durante el salto: {str(e)}"
            )
    
    def plan_intergalactic_route(self, from_star: Star, to_star: Star, 
                                burro: BurroAstronauta) -> Dict:
        """
        Planifica una ruta que incluye salto hipergigante si es necesario.
        
        Args:
            from_star: Estrella de origen
            to_star: Estrella de destino
            burro: Burro astronauta
            
        Returns:
            Dict: Plan de ruta detallado
        """
        plan = {
            'requires_hypergiant_jump': False,
            'accessible_hypergiants': [],
            'destination_options': [],
            'recommended_hypergiant': None,
            'total_distance': 0.0,
            'route_steps': [],
            'feasible': False
        }
        
        # Verificar si requiere salto hipergigante
        if not self.requires_hypergiant_jump(from_star, to_star):
            plan['requires_hypergiant_jump'] = False
            plan['message'] = "No se requiere salto hipergigante (misma constelación)"
            return plan
        
        plan['requires_hypergiant_jump'] = True
        
        # Encontrar hipergigantes accesibles
        accessible_hypergiants = self.find_accessible_hypergiants(from_star)
        plan['accessible_hypergiants'] = [
            {'hypergiant': hg.label, 'distance': dist} 
            for hg, dist in accessible_hypergiants
        ]
        
        if not accessible_hypergiants:
            plan['message'] = "❌ No hay hipergigantes accesibles desde la ubicación actual"
            return plan
        
        # Encontrar destinos en la constelación objetivo
        target_constellation = self.get_star_constellation(to_star)
        destination_options = self.find_destination_options(target_constellation)
        plan['destination_options'] = [star.label for star in destination_options]
        
        # Recomendar la hipergigante más cercana que sea factible
        for hypergiant, distance in accessible_hypergiants:
            if self.can_perform_hypergiant_jump(burro, hypergiant, distance):
                plan['recommended_hypergiant'] = {
                    'star': hypergiant.label,
                    'distance': distance,
                    'energy_cost': int(distance * 0.1 * max(1.0, (burro.current_age - 5) / 10.0))
                }
                plan['feasible'] = True
                plan['total_distance'] = distance  # Solo hasta la hipergigante
                break
        
        if not plan['feasible']:
            plan['message'] = "❌ Recursos insuficientes para alcanzar cualquier hipergigante"
        else:
            plan['message'] = f"✅ Salto hipergigante planificado via {plan['recommended_hypergiant']['star']}"
        
        return plan
    
    def get_hypergiant_statistics(self) -> Dict:
        """Obtiene estadísticas de las estrellas hipergigantes."""
        stats = {
            'total_hypergiants': len(self.hypergiant_stars),
            'hypergiants_by_constellation': {},
            'hypergiant_details': []
        }
        
        for hg in self.hypergiant_stars:
            constellation = self.get_star_constellation(hg)
            if constellation not in stats['hypergiants_by_constellation']:
                stats['hypergiants_by_constellation'][constellation] = 0
            stats['hypergiants_by_constellation'][constellation] += 1
            
            stats['hypergiant_details'].append({
                'id': hg.id,
                'label': hg.label,
                'constellation': constellation,
                'coordinates': f"({hg.x}, {hg.y})",
                'radius': hg.radius,
                'energy': hg.amount_of_energy
            })
        
        return stats


def main():
    """Función de demostración del sistema de saltos hipergigantes."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sistema de saltos hipergigantes')
    parser.add_argument('--demo', action='store_true', help='Ejecutar demostración')
    parser.add_argument('--stats', action='store_true', help='Mostrar estadísticas')
    parser.add_argument('--from', dest='from_star', help='Estrella de origen')
    parser.add_argument('--to', dest='to_star', help='Estrella de destino')
    
    args = parser.parse_args()
    
    # Cargar mapa espacial
    space_map = SpaceMap('data/constellations.json')
    jump_system = HyperGiantJumpSystem(space_map)
    
    if args.stats:
        stats = jump_system.get_hypergiant_statistics()
        print(json.dumps(stats, indent=2, ensure_ascii=False))
        
    elif args.demo or (args.from_star and args.to_star):
        from_id = args.from_star or "1"  # Default demo
        to_id = args.to_star or "13"     # Default demo - different constellation
        
        from_star = space_map.get_star(from_id)
        to_star = space_map.get_star(to_id)
        
        if not from_star or not to_star:
            print("❌ Estrella no encontrada")
            return
        
        # Crear burro para demo
        burro = space_map.create_burro_astronauta()
        burro.current_location = from_star
        
        # Planificar ruta
        plan = jump_system.plan_intergalactic_route(from_star, to_star, burro)
        
        print("="*60)
        print("🌌 SISTEMA DE SALTOS HIPERGIGANTES")
        print("="*60)
        print(f"📍 Origen: {from_star.label} ({jump_system.get_star_constellation(from_star)})")
        print(f"🎯 Destino: {to_star.label} ({jump_system.get_star_constellation(to_star)})")
        print(f"🚀 Requiere salto: {'Sí' if plan['requires_hypergiant_jump'] else 'No'}")
        print("\n" + json.dumps(plan, indent=2, ensure_ascii=False))
        
    else:
        print("Uso: python hypergiant_jump.py [--demo] [--stats] [--from ID --to ID]")


if __name__ == '__main__':
    main()
