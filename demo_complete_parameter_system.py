#!/usr/bin/env python3
"""
Demostración completa del sistema de parámetros de investigación.

Este script muestra:
1. Cálculo con parámetros por defecto
2. Configuración de parámetros personalizados
3. Recálculo automático con nuevos parámetros
4. Comparación de resultados
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.models import SpaceMap
from src.route_calculator import RouteCalculator
from src.parameter_editor_simple import ResearchParameters

def demo_parameter_system():
    """Demostración completa del sistema de parámetros."""
    print("🔬 DEMOSTRACIÓN: SISTEMA COMPLETO DE PARÁMETROS DE INVESTIGACIÓN")
    print("=" * 70)
    
    # Cargar mapa espacial
    space_map = SpaceMap('data/constellations.json')
    calculator = RouteCalculator(space_map, {})
    
    # Seleccionar estrella de inicio
    start_star = space_map.get_star("13")  # Gama23 - estrella hipergigante
    if not start_star:
        print("❌ Error: No se pudo encontrar estrella de inicio")
        return
    
    print(f"🚀 Estrella de inicio: {start_star.label} (ID: {start_star.id})")
    print(f"   • Hipergigante: {'Sí' if start_star.hypergiant else 'No'}")
    print(f"   • Energía: {start_star.amount_of_energy}")
    print(f"   • Tiempo comer: {start_star.time_to_eat}")
    
    print("\n" + "=" * 70)
    print("1️⃣ CÁLCULO CON PARÁMETROS POR DEFECTO")
    print("-" * 50)
    
    # Parámetros por defecto
    default_params = ResearchParameters()
    print(f"📊 Parámetros por defecto:")
    print(f"   • Consumo energía: {default_params.energy_consumption_rate:.1f}% por tiempo")
    print(f"   • Tiempo investigación: {default_params.time_percentage*100:.1f}%")
    print(f"   • Bonus tiempo vida: {default_params.life_time_bonus:+.1f} años")
    print(f"   • Bonus energía: {default_params.energy_bonus_per_star:+.1f}% por estrella")
    
    try:
        # Calcular ruta con parámetros por defecto
        path_default, stats_default = calculator.find_min_cost_route_from_json(
            start_star, research_params=default_params
        )
        
        if path_default and len(path_default) > 1:
            route_summary = " → ".join([s.label for s in path_default])
            print(f"\n✅ Ruta calculada: {route_summary}")
            print(f"📊 Estadísticas:")
            print(f"   • Estrellas visitadas: {stats_default.get('num_stars', 0)}")
            print(f"   • Tiempo de vida: {stats_default.get('life_time_consumed', 0):.1f} años")
            print(f"   • Distancia total: {stats_default.get('total_distance', 0):.1f} años luz")
        else:
            print("❌ No se pudo calcular ruta con parámetros por defecto")
            stats_default = {'num_stars': 0, 'life_time_consumed': 0, 'total_distance': 0}
            
    except Exception as e:
        print(f"❌ Error con parámetros por defecto: {e}")
        stats_default = {'num_stars': 0, 'life_time_consumed': 0, 'total_distance': 0}
    
    print("\n" + "=" * 70)
    print("2️⃣ CONFIGURACIÓN DE PARÁMETROS PERSONALIZADOS")
    print("-" * 50)
    
    # Crear parámetros personalizados
    custom_params = ResearchParameters(
        energy_consumption_rate=1.5,     # Menos consumo de energía
        time_percentage=0.7,             # Más tiempo de investigación
        life_time_bonus=0.5,            # Bonus de tiempo de vida
        energy_bonus_per_star=3.0,      # Bonus de energía por estrella
        custom_star_settings={
            "13": {  # Gama23 - configuración especial
                "energy_rate": 0.5,      # Muy bajo consumo
                "time_bonus": 1.0,       # +1 año de vida
                "energy_bonus": 10.0     # +10% energía
            },
            "14": {  # Theta14 - configuración diferente
                "energy_rate": 3.0,      # Alto consumo
                "time_bonus": -0.5,      # -0.5 años de vida
                "energy_bonus": 1.0      # +1% energía
            }
        }
    )
    
    print(f"✨ Parámetros personalizados configurados:")
    print(f"   • Consumo energía: {custom_params.energy_consumption_rate:.1f}% por tiempo")
    print(f"   • Tiempo investigación: {custom_params.time_percentage*100:.1f}%")
    print(f"   • Bonus tiempo vida: {custom_params.life_time_bonus:+.1f} años")
    print(f"   • Bonus energía: {custom_params.energy_bonus_per_star:+.1f}% por estrella")
    print(f"   • Configuraciones específicas: {len(custom_params.custom_star_settings)} estrellas")
    
    for star_id, config in custom_params.custom_star_settings.items():
        star = space_map.get_star(star_id)
        star_name = star.label if star else f"ID:{star_id}"
        print(f"     🌟 {star_name}: consumo={config['energy_rate']:.1f}%, "
              f"bonus_tiempo={config['time_bonus']:+.1f}a, "
              f"bonus_energía={config['energy_bonus']:+.1f}%")
    
    print("\n" + "=" * 70)
    print("3️⃣ RECÁLCULO CON PARÁMETROS PERSONALIZADOS")
    print("-" * 50)
    
    try:
        # Calcular ruta con parámetros personalizados
        path_custom, stats_custom = calculator.find_min_cost_route_from_json(
            start_star, research_params=custom_params
        )
        
        if path_custom and len(path_custom) > 1:
            route_summary = " → ".join([s.label for s in path_custom])
            print(f"✅ Ruta recalculada: {route_summary}")
            print(f"📊 Estadísticas:")
            print(f"   • Estrellas visitadas: {stats_custom.get('num_stars', 0)}")
            print(f"   • Tiempo de vida: {stats_custom.get('life_time_consumed', 0):.1f} años")
            print(f"   • Distancia total: {stats_custom.get('total_distance', 0):.1f} años luz")
        else:
            print("❌ No se pudo calcular ruta con parámetros personalizados")
            stats_custom = {'num_stars': 0, 'life_time_consumed': 0, 'total_distance': 0}
            
    except Exception as e:
        print(f"❌ Error con parámetros personalizados: {e}")
        stats_custom = {'num_stars': 0, 'life_time_consumed': 0, 'total_distance': 0}
    
    print("\n" + "=" * 70)
    print("4️⃣ COMPARACIÓN DE RESULTADOS")
    print("-" * 50)
    
    # Comparar resultados
    stars_diff = stats_custom.get('num_stars', 0) - stats_default.get('num_stars', 0)
    time_diff = stats_custom.get('life_time_consumed', 0) - stats_default.get('life_time_consumed', 0)
    distance_diff = stats_custom.get('total_distance', 0) - stats_default.get('total_distance', 0)
    
    print(f"📊 COMPARACIÓN (Personalizado vs Defecto):")
    print(f"   • Diferencia estrellas: {stars_diff:+d}")
    print(f"   • Diferencia tiempo: {time_diff:+.1f} años")
    print(f"   • Diferencia distancia: {distance_diff:+.1f} años luz")
    
    if stars_diff > 0:
        print(f"   ✅ Los parámetros personalizados permiten visitar {stars_diff} estrella(s) adicional(es)")
    elif stars_diff < 0:
        print(f"   ⚠️  Los parámetros personalizados reducen las visitas en {abs(stars_diff)} estrella(s)")
    else:
        print(f"   ➖ Mismo número de estrellas visitadas")
    
    if time_diff < 0:
        print(f"   ✅ Los parámetros personalizados ahorran {abs(time_diff):.1f} años de tiempo")
    elif time_diff > 0:
        print(f"   ⚠️  Los parámetros personalizados consumen {time_diff:.1f} años adicionales")
    else:
        print(f"   ➖ Mismo tiempo de vida consumido")
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("💡 El sistema permite configurar parámetros detallados para optimizar rutas")
    print("🔧 Use el botón '⚙️ Configurar Parámetros' en la GUI para la experiencia completa")

if __name__ == "__main__":
    demo_parameter_system()