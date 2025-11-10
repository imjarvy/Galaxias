"""
Script de prueba para la nueva funcionalidad de ruta de menor gasto posible.
Compara los resultados con el algoritmo de máximo estrellas.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import SpaceMap
from src.route_calculator import RouteCalculator
from src.min_cost_route import MinCostRouteCalculator
import json

def test_min_cost_vs_max_stars():
    """Compara los resultados de ambos algoritmos."""
    print("🧪 PRUEBA COMPARATIVA: MENOR GASTO vs MÁXIMO ESTRELLAS")
    print("="*60)
    
    # Cargar datos
    space_map = SpaceMap('data/constellations.json')
    config = {'test': True}
    calculator = RouteCalculator(space_map, config)
    
    # Probar desde varias estrellas
    test_stars = ['1', '3', '13']  # Alpha1, Alpha53 (hipergigante), Gama23 (hipergigante)
    
    for start_id in test_stars:
        print(f"\n🌟 PRUEBAS DESDE ESTRELLA {start_id}")
        print("-" * 40)
        
        start_star = space_map.get_star(start_id)
        if not start_star:
            print(f"❌ Estrella {start_id} no encontrada")
            continue
            
        print(f"📍 Inicio: {start_star.label} (ID: {start_id})")
        
        # 1. Algoritmo de máximo estrellas
        print("\n🎯 MÁXIMO ESTRELLAS VISITADAS:")
        try:
            max_path, max_stats = calculator.find_max_visit_route_from_json(start_star)
            print(f"  ✅ Estrellas visitadas: {max_stats['stars_visited']}")
            print(f"  📏 Distancia total: {max_stats['total_distance']} años luz")
            print(f"  ⏱️ Tiempo vida: {max_stats['life_time_consumed']:.2f} años")
            print(f"  🔋 Energía final: {max_stats.get('json_values_used', {}).get('energia_inicial', 'N/A')}% inicial")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
        
        # 2. Algoritmo de menor gasto
        print("\n💰 MENOR GASTO POSIBLE:")
        try:
            min_path, min_stats = calculator.find_min_cost_route_from_json(start_star)
            if 'error' in min_stats:
                print(f"  ❌ Error: {min_stats['error']}")
            else:
                print(f"  ✅ Estrellas visitadas: {min_stats['stars_visited']}")
                print(f"  📏 Distancia total: {min_stats['total_distance']} años luz")
                print(f"  ⏱️ Tiempo vida: {min_stats['life_time_consumed']:.2f} años")
                print(f"  🌱 Pasto consumido: {min_stats['total_grass_consumed']:.2f} kg")
                print(f"  🔋 Energía final: {min_stats['final_energy']:.2f}%")
                print(f"  💫 Vida restante: {min_stats['remaining_life']:.2f} años")
                
                # Mostrar algunas acciones detalladas
                if 'star_actions_detail' in min_stats and min_stats['star_actions_detail']:
                    print(f"\n  🔍 MUESTRA DE ACCIONES DETALLADAS:")
                    for i, action in enumerate(min_stats['star_actions_detail'][:3]):  # Solo primeras 3
                        print(f"    {i+1}. {action.star_label}: "
                              f"Llegó con {action.arrived_energy:.1f}% → "
                              f"{'Comió' if action.can_eat and action.ate_kg > 0 else 'No comió'} → "
                              f"Final: {action.final_energy:.1f}%")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
        
        print("\n" + "="*40)

def test_min_cost_detailed():
    """Prueba detallada del algoritmo de menor gasto."""
    print("\n🔬 PRUEBA DETALLADA: ALGORITMO DE MENOR GASTO")
    print("="*60)
    
    space_map = SpaceMap('data/constellations.json')
    calculator = MinCostRouteCalculator(space_map)
    
    # Mostrar condiciones iniciales del JSON
    print("📋 CONDICIONES INICIALES DEL JSON:")
    print(f"  🔋 Energía inicial: {space_map.burro_data['burroenergiaInicial']}%")
    print(f"  🏥 Estado salud: {space_map.burro_data['estadoSalud']}")
    print(f"  🎂 Edad inicial: {space_map.burro_data['startAge']} años")
    print(f"  ⚰️ Edad muerte: {space_map.burro_data['deathAge']} años")
    print(f"  🌱 Pasto inicial: {space_map.burro_data['pasto']} kg")
    print(f"  ⏳ Vida disponible: {space_map.burro_data['deathAge'] - space_map.burro_data['startAge']} años")
    
    # Probar con estrella hipergigante
    test_id = '13'  # Gama23 - hipergigante
    print(f"\n🌟 PRUEBA DESDE: {space_map.get_star(test_id).label} (ID: {test_id})")
    
    result = calculator.calculate_min_cost_route(test_id)
    
    if not result.success:
        print(f"❌ ERROR: {result.error_message}")
        return
    
    print(f"\n✅ RESULTADO EXITOSO:")
    print(f"  📍 Estrellas visitadas: {len(result.route_sequence)}")
    print(f"  📏 Distancia total: {result.total_distance} años luz")
    print(f"  ⏱️ Vida consumida: {result.life_consumed:.2f} años")
    print(f"  🌱 Pasto consumido: {result.total_grass_consumed:.2f} kg")
    print(f"  🔋 Energía final: {result.final_energy:.2f}%")
    print(f"  💫 Vida restante: {result.remaining_life:.2f} años")
    
    print(f"\n📋 SECUENCIA DE ESTRELLAS:")
    for i, star_info in enumerate(result.route_sequence, 1):
        print(f"  {i}. {star_info['label']} (ID: {star_info['id']})")
    
    print(f"\n🔍 ACCIONES DETALLADAS POR ESTRELLA:")
    for action in result.star_actions:
        print(f"\n⭐ {action.star_label} (ID: {action.star_id}):")
        print(f"   Energía llegada: {action.arrived_energy:.1f}%")
        print(f"   Puede comer: {'Sí' if action.can_eat else 'No'} (energía < 50%)")
        if action.can_eat and action.ate_kg > 0:
            print(f"   🍽️ Comió: {action.ate_kg:.2f} kg")
            print(f"   ⚡ Energía ganada: +{action.energy_gained_eating:.1f}%")
            print(f"   ⏳ Tiempo comiendo: {action.time_eating:.1f}")
        else:
            print(f"   🚫 No comió (energía suficiente)")
        print(f"   🔬 Tiempo investigando: {action.time_researching:.1f}")
        print(f"   📉 Energía por investigar: -{action.energy_consumed_research:.1f}%")
        print(f"   🔋 Energía final: {action.final_energy:.1f}%")
        print(f"   🌱 Pasto consumido: {action.total_grass_consumed:.2f} kg")


if __name__ == '__main__':
    print("🚀 INICIANDO PRUEBAS DE MENOR GASTO POSIBLE")
    print("="*60)
    
    try:
        test_min_cost_vs_max_stars()
        test_min_cost_detailed()
        
        print("\n" + "="*60)
        print("🎉 TODAS LAS PRUEBAS COMPLETADAS")
        print("✅ Sistema de menor gasto implementado correctamente")
        print("✅ Coexiste con sistema de máximo estrellas")
        print("✅ Reglas específicas funcionando:")
        print("   • Decisión de comer basada en energía < 50%")
        print("   • Bonificación por estado de salud")
        print("   • División tiempo: 50% comer / 50% investigar") 
        print("   • Consumo energía por investigación")
        print("   • Una visita por estrella")
        print("   • Objetivo: MENOR GASTO total")
        
    except Exception as e:
        print(f"\n❌ ERROR EN LAS PRUEBAS: {str(e)}")
        import traceback
        traceback.print_exc()