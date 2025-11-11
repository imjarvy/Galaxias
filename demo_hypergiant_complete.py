#!/usr/bin/env python3
"""
Demostración completa del sistema de saltos hipergigantes.

Este script demuestra:
1. Detección automática de cambios de constelación
2. Identificación de hipergigantes disponibles
3. Cálculo de beneficios del salto hipergigante
4. Integración con algoritmos de rutas MAX_VISIT y MIN_COST
5. GUI interactiva para gestión de saltos
"""

import sys
import os
import json
from typing import Dict, List

# Agregar path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import SpaceMap, BurroAstronauta
from src.hypergiant_jump import HyperGiantJumpSystem
from src.max_visit_route import compute_max_visits_from_json
from src.min_cost_route import MinCostRouteCalculator


def demo_hypergiant_detection():
    """Demuestra la detección de cambios de constelación."""
    print("="*70)
    print("🌌 DEMOSTRACIÓN: DETECCIÓN DE SALTOS HIPERGIGANTES")
    print("="*70)
    
    # Cargar mapa espacial
    space_map = SpaceMap('data/constellations.json')
    jump_system = HyperGiantJumpSystem(space_map)
    
    # Casos de prueba
    test_cases = [
        ("1", "3"),    # Misma constelación - NO requiere salto
        ("1", "13"),   # Diferentes constelaciones - SÍ requiere salto
        ("3", "13"),   # Desde hipergigante a otra constelación
        ("2", "15"),   # Otro cambio de constelación
    ]
    
    for from_id, to_id in test_cases:
        from_star = space_map.get_star(from_id)
        to_star = space_map.get_star(to_id)
        
        if from_star and to_star:
            from_constellation = jump_system.get_star_constellation(from_star)
            to_constellation = jump_system.get_star_constellation(to_star)
            requires_jump = jump_system.requires_hypergiant_jump(from_star, to_star)
            
            print(f"\n📍 Viaje: {from_star.label} → {to_star.label}")
            print(f"   Constelaciones: {from_constellation} → {to_constellation}")
            print(f"   Requiere salto hipergigante: {'✅ SÍ' if requires_jump else '❌ NO'}")
            
            if requires_jump:
                accessible_hgs = jump_system.find_accessible_hypergiants(from_star)
                if accessible_hgs:
                    print(f"   Hipergigantes accesibles: {len(accessible_hgs)}")
                    for hg, distance in accessible_hgs:
                        print(f"     • {hg.label} (distancia: {distance:.1f})")
                else:
                    print("   ❌ No hay hipergigantes accesibles")


def demo_hypergiant_benefits():
    """Demuestra los beneficios de un salto hipergigante."""
    print("\n" + "="*70)
    print("⚡ DEMOSTRACIÓN: BENEFICIOS DEL SALTO HIPERGIGANTE")
    print("="*70)
    
    # Cargar sistema
    space_map = SpaceMap('data/constellations.json')
    jump_system = HyperGiantJumpSystem(space_map)
    burro = space_map.create_burro_astronauta()
    
    # Configurar estado inicial
    burro.current_energy = 60  # 60% energía
    burro.current_pasto = 150  # 150kg pasto
    
    print(f"📊 ESTADO INICIAL DEL BURRO:")
    print(f"   ⚡ Energía: {burro.current_energy}%")
    print(f"   🌱 Pasto: {burro.current_pasto}kg")
    print(f"   💫 Vida restante: {burro.get_remaining_life():.1f} años")
    
    # Simular salto hipergigante
    from_star = space_map.get_star("1")
    to_star = space_map.get_star("13")
    hypergiant = space_map.get_star("3")  # Alpha53 es hipergigante
    
    if from_star and to_star and hypergiant:
        # Encontrar distancia a hipergigante
        distance_to_hg = None
        for route in space_map.routes:
            if ((route.from_star.id == from_star.id and route.to_star.id == hypergiant.id) or
                (route.to_star.id == from_star.id and route.from_star.id == hypergiant.id)):
                distance_to_hg = route.distance
                break
        
        if distance_to_hg:
            print(f"\n🚀 EJECUTANDO SALTO HIPERGIGANTE:")
            print(f"   📍 {from_star.label} → 🌟 {hypergiant.label} → 🎯 {to_star.label}")
            print(f"   📏 Distancia a hipergigante: {distance_to_hg} años luz")
            
            # Realizar salto
            result = jump_system.perform_hypergiant_jump(burro, hypergiant, to_star, distance_to_hg)
            
            print(f"\n📈 RESULTADO DEL SALTO:")
            print(f"   {'✅ ÉXITO' if result.success else '❌ FALLO'}")
            print(f"   ⚡ Energía: {result.energy_before:.1f}% → {result.energy_after:.1f}%")
            print(f"   🌱 Pasto: {result.grass_before:.1f}kg → {result.grass_after:.1f}kg")
            print(f"\n💬 {result.message}")


def demo_route_algorithms_with_hypergiants():
    """Demuestra los algoritmos de rutas con soporte para saltos hipergigantes."""
    print("\n" + "="*70)
    print("🧭 DEMOSTRACIÓN: ALGORITMOS CON SALTOS HIPERGIGANTES")
    print("="*70)
    
    space_map = SpaceMap('data/constellations.json')
    
    print("\n🎯 ALGORITMO MAX_VISIT con Saltos Hipergigantes:")
    print("-"*50)
    
    # Probar MAX_VISIT desde estrella en una constelación
    result_max = compute_max_visits_from_json(space_map, "1")
    
    print(f"📊 Resultado MAX_VISIT:")
    print(f"   ⭐ Estrellas visitadas: {result_max['num_stars']}")
    print(f"   📏 Distancia total: {result_max['total_distance']} años luz")
    print(f"   ⏱️ Vida consumida: {result_max['life_time_consumed']} años")
    
    if 'hypergiant_jumps' in result_max and result_max['hypergiant_jumps']:
        print(f"   🌌 Saltos hipergigantes: {len(result_max['hypergiant_jumps'])}")
        for jump in result_max['hypergiant_jumps']:
            print(f"     • {jump['from']} → {jump['hypergiant']} → {jump['to']}")
    else:
        print(f"   🌌 Saltos hipergigantes: 0 (ruta dentro de la misma constelación)")
    
    print(f"\n🛣️ Secuencia de estrellas:")
    sequence_labels = [star['label'] for star in result_max['sequence']]
    print(f"   {' → '.join(sequence_labels)}")
    
    print("\n💰 ALGORITMO MIN_COST con Saltos Hipergigantes:")
    print("-"*50)
    
    # Probar MIN_COST
    try:
        min_calculator = MinCostRouteCalculator(space_map)
        result_min = min_calculator.calculate_min_cost_route("1")
        
        print(f"📊 Resultado MIN_COST:")
        print(f"   ⭐ Estrellas visitadas: {len(result_min.route_sequence)}")
        print(f"   🌱 Pasto consumido: {result_min.total_grass_consumed:.2f}kg")
        print(f"   ⚡ Energía final: {result_min.final_energy:.2f}%")
        print(f"   ✅ Éxito: {'Sí' if result_min.success else 'No'}")
        
        if result_min.success:
            print(f"\n🛣️ Ruta MIN_COST:")
            route_labels = [item['star_label'] for item in result_min.route_sequence]
            print(f"   {' → '.join(route_labels)}")
            
    except Exception as e:
        print(f"   ❌ Error en MIN_COST: {str(e)}")


def demo_hypergiant_statistics():
    """Muestra estadísticas de las estrellas hipergigantes."""
    print("\n" + "="*70)
    print("📈 ESTADÍSTICAS DE ESTRELLAS HIPERGIGANTES")
    print("="*70)
    
    space_map = SpaceMap('data/constellations.json')
    jump_system = HyperGiantJumpSystem(space_map)
    
    stats = jump_system.get_hypergiant_statistics()
    
    print(f"🌟 Total de hipergigantes: {stats['total_hypergiants']}")
    
    print(f"\n📊 Distribución por constelación:")
    for constellation, count in stats['hypergiants_by_constellation'].items():
        print(f"   • {constellation}: {count} hipergigante(s)")
    
    print(f"\n🗃️ Detalles de hipergigantes:")
    for hg in stats['hypergiant_details']:
        print(f"   🌟 {hg['label']} (ID: {hg['id']})")
        print(f"       Constelación: {hg['constellation']}")
        print(f"       Coordenadas: {hg['coordinates']}")
        print(f"       Radio: {hg['radius']} | Energía: {hg['energy']}")
        print()


def demo_interactive_planning():
    """Demuestra la planificación interactiva de saltos hipergigantes."""
    print("\n" + "="*70)
    print("🎮 PLANIFICACIÓN INTERACTIVA DE SALTOS")
    print("="*70)
    
    space_map = SpaceMap('data/constellations.json')
    jump_system = HyperGiantJumpSystem(space_map)
    burro = space_map.create_burro_astronauta()
    
    # Casos de prueba interactivos
    test_routes = [
        ("1", "13", "Burro → Gama23 (entre constelaciones)"),
        ("2", "15", "Beta23 → Otra constelación"),
        ("3", "1", "Desde hipergigante a estrella normal")
    ]
    
    for from_id, to_id, description in test_routes:
        from_star = space_map.get_star(from_id)
        to_star = space_map.get_star(to_id)
        
        if from_star and to_star:
            print(f"\n🎯 Caso: {description}")
            print(f"   Desde: {from_star.label} → Hasta: {to_star.label}")
            
            plan = jump_system.plan_intergalactic_route(from_star, to_star, burro)
            
            print(f"   Requiere salto: {'✅ Sí' if plan['requires_hypergiant_jump'] else '❌ No'}")
            
            if plan['requires_hypergiant_jump']:
                if plan['feasible']:
                    recommended = plan['recommended_hypergiant']
                    print(f"   🌟 Hipergigante recomendada: {recommended['star']}")
                    print(f"   📏 Distancia: {recommended['distance']} años luz")
                    print(f"   ⚡ Costo energía: {recommended['energy_cost']} puntos")
                    
                    print(f"   🎯 Destinos disponibles: {len(plan['destination_options'])}")
                    print(f"     {', '.join(plan['destination_options'][:5])}" + 
                          ("..." if len(plan['destination_options']) > 5 else ""))
                else:
                    print(f"   ❌ No factible: {plan.get('message', 'Recursos insuficientes')}")


def main():
    """Función principal para ejecutar todas las demostraciones."""
    print("🌌 SISTEMA COMPLETO DE SALTOS HIPERGIGANTES")
    print("="*70)
    print("Este sistema implementa la lógica requerida para viajes entre constelaciones:")
    print("• Detección automática de cambios de constelación")
    print("• Obligatoriedad de usar hipergigantes para saltos intergalácticos")
    print("• Beneficios: +50% energía, x2 pasto")
    print("• Selección de destino en nueva galaxia")
    print("• Integración con algoritmos de rutas existentes")
    print("="*70)
    
    try:
        # Ejecutar demostraciones
        demo_hypergiant_detection()
        demo_hypergiant_benefits()
        demo_hypergiant_statistics()
        demo_interactive_planning()
        demo_route_algorithms_with_hypergiants()
        
        print("\n" + "="*70)
        print("✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*70)
        print("\n🎮 Para usar la GUI interactiva, ejecute:")
        print("   python src/gui.py")
        print("\n📊 Para análisis específicos, use:")
        print("   python src/hypergiant_jump.py --demo")
        print("   python src/hypergiant_jump.py --stats")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ERROR EN LA DEMOSTRACIÓN: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
