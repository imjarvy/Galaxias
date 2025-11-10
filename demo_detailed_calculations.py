"""
Script especial para probar el sistema de menor gasto con situación donde el burro necesita comer.
Modifica temporalmente la energía inicial para demostrar todos los cálculos.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import SpaceMap
from src.min_cost_route import MinCostRouteCalculator
import json

def test_detailed_calculations():
    """Prueba con energía baja para mostrar todos los cálculos."""
    print("🧪 PRUEBA ESPECIAL: CÁLCULOS DETALLADOS CON ALIMENTACIÓN")
    print("="*70)
    
    # Cargar datos y modificar energía inicial temporalmente
    space_map = SpaceMap('data/constellations.json')
    
    # MODIFICAR TEMPORALMENTE para demostrar alimentación
    original_energy = space_map.burro_data['burroenergiaInicial']
    space_map.burro_data['burroenergiaInicial'] = 45  # Energía < 50% para que pueda comer
    
    print(f"🔧 MODIFICACIÓN TEMPORAL:")
    print(f"   Energía original: {original_energy}%")
    print(f"   Energía para prueba: {space_map.burro_data['burroenergiaInicial']}%")
    print(f"   Esto permitirá que el burro COMA en las estrellas (< 50%)")
    print(f"   Estado salud: {space_map.burro_data['estadoSalud']} (+5% por kg)")
    
    calculator = MinCostRouteCalculator(space_map)
    
    # Probar con Gama23 que es hipergigante y tiene buen radio
    test_id = '13'  # Gama23
    print(f"\n🌟 PRUEBA DESDE: {space_map.get_star(test_id).label} (ID: {test_id})")
    print(f"   Tipo: Hipergigante (radius: {space_map.get_star(test_id).radius})")
    print(f"   Energía base: {space_map.get_star(test_id).amount_of_energy}")
    print(f"   Tiempo comer: {space_map.get_star(test_id).time_to_eat}")
    
    result = calculator.calculate_min_cost_route(test_id)
    
    if not result.success:
        print(f"❌ ERROR: {result.error_message}")
        return
    
    print(f"\n✅ RESULTADO EXITOSO:")
    print(f"   📍 Estrellas visitadas: {len(result.route_sequence)}")
    print(f"   🌱 Pasto consumido: {result.total_grass_consumed:.2f} kg")
    print(f"   🔋 Energía final: {result.final_energy:.2f}%")
    
    # Mostrar primeras estrellas con cálculos detallados
    print(f"\n" + "="*80)
    print("🔬 EJEMPLO DETALLADO - PRIMERAS 2 ESTRELLAS")
    print("="*80)
    
    for i, action in enumerate(result.star_actions[:2], 1):
        detailed = action.to_detailed_dict()
        
        print(f"\n⭐ ESTRELLA {i}: {detailed['star_info']['label']} (ID: {detailed['star_info']['id']})")
        print("─" * 60)
        
        # Estado inicial
        print(f"🔋 ESTADO AL LLEGAR:")
        print(f"   Energía: {detailed['initial_state']['arrived_energy']}%")
        print(f"   Pasto disponible: {detailed['initial_state']['available_grass']} kg")
        
        # Análisis detallado de alimentación
        print(f"\n🍽️  DECISIÓN DE ALIMENTACIÓN:")
        eat_analysis = detailed['eating_analysis']
        print(f"   ¿Puede comer? {eat_analysis['can_eat']}")
        print(f"   Razón: {eat_analysis['reason']}")
        
        eat_calc = eat_analysis['calculations']
        print(f"\n   📊 CÁLCULOS DE ALIMENTACIÓN:")
        print(f"      Máximo que puede comer: {eat_calc['max_kg_can_eat']} kg")
        print(f"      Realmente comió: {eat_calc['actually_ate_kg']} kg")
        
        if float(eat_calc['actually_ate_kg']) > 0:
            print(f"\n   💡 DESGLOSE ENERGÍA GANADA:")
            print(f"      🌟 Base de estrella: {eat_calc['base_energy_from_star']}%")
            print(f"         (amount_of_energy × 10 = {action.base_energy_star/10:.0f} × 10)")
            print(f"      🏥 Bonus por salud: {eat_calc['eating_bonus_energy']}%")
            print(f"         (kg × {eat_calc['health_bonus_rate']} × 100 = {action.ate_kg:.1f} × {action.health_bonus_percentage:.2f} × 100)")
            print(f"      📏 Bonus por radio: {eat_calc['radius_bonus_energy']}%")
            print(f"         (radius × 5 = {action.radius_bonus_energy/5:.1f} × 5)")
            print(f"      ─────────────────────────")
            print(f"      🔋 TOTAL GANADO: {eat_calc['total_energy_gained']}%")
        else:
            print(f"      🚫 NO COMIÓ: Energía suficiente (≥ 50%)")
        
        # Tiempo detallado
        print(f"\n⏱️  GESTIÓN DEL TIEMPO:")
        time_dist = detailed['time_distribution']
        print(f"   Total en estrella: {time_dist['total_time_at_star']} unidades")
        print(f"   Comiendo: {time_dist['time_eating']} ({time_dist['eating_percentage']})")
        print(f"   Investigando: {time_dist['time_researching']} ({time_dist['research_percentage']})")
        
        # Investigación detallada
        print(f"\n🔬 INVESTIGACIÓN (SIEMPRE OBLIGATORIA):")
        research = detailed['research_calculations']
        print(f"   Tiempo investigando: {research['research_time']}")
        print(f"   Tasa de consumo: {research['energy_rate_per_time']}% por unidad tiempo")
        print(f"   Cálculo: {research['formula']}")
        print(f"   Energía consumida: {research['energy_consumed']}%")
        
        # Flujo completo de energía
        print(f"\n🔄 FLUJO COMPLETO DE ENERGÍA:")
        energy_flow = detailed['energy_flow']
        print(f"   1️⃣ Al llegar: {energy_flow['initial_energy']}%")
        print(f"   2️⃣ Después de comer: {energy_flow['energy_after_eating']}%")
        print(f"      (Ganancia: +{energy_flow['energy_after_eating'] - energy_flow['initial_energy']:.1f}%)")
        print(f"   3️⃣ Después de investigar: {energy_flow['final_energy']}%")
        print(f"      (Pérdida: -{energy_flow['energy_consumed_research']:.1f}%)")
        print(f"   🏁 CAMBIO NETO: {energy_flow['net_energy_change']:+.1f}%")
        
        # Recursos
        print(f"\n🌱 GESTIÓN DE RECURSOS:")
        resources = detailed['resource_consumption']
        print(f"   Pasto gastado aquí: {resources['grass_consumed_this_star']} kg")
        print(f"   Pasto restante: {resources['grass_remaining']} kg")
        
        print()
    
    print("="*80)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("📝 Se pueden ver todos los cálculos numéricos paso a paso")
    print("🧮 Cada fórmula está desglosada con valores específicos")
    print("🔄 El flujo de energía se muestra etapa por etapa")
    print("⚖️ Se respetan todas las reglas de menor gasto posible")

if __name__ == '__main__':
    test_detailed_calculations()