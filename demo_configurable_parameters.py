"""
Demo del sistema de parámetros de investigación configurables.
Muestra la funcionalidad de edición de parámetros antes del cálculo de ruta.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import SpaceMap
from src.min_cost_route import MinCostRouteCalculator
from src.parameter_editor_simple import ResearchParameters
import json


def demo_configurable_parameters():
    """Demuestra el uso de parámetros configurables."""
    print("🔬 DEMO: SISTEMA DE PARÁMETROS CONFIGURABLES")
    print("="*60)
    
    # Cargar mapa espacial
    space_map = SpaceMap('data/constellations.json')
    
    print("\n1️⃣ CALCULANDO CON PARÁMETROS POR DEFECTO:")
    print("-" * 50)
    
    # Parámetros por defecto
    default_params = ResearchParameters()
    calculator_default = MinCostRouteCalculator(space_map, research_params=default_params)
    result_default = calculator_default.calculate_min_cost_route('13')
    
    if result_default.success:
        print(f"✅ Estrellas visitadas: {len(result_default.star_actions)}")
        print(f"✅ Pasto consumido: {result_default.total_grass_consumed:.2f} kg")
        print(f"✅ Energía final: {result_default.final_energy:.1f}%")
        print(f"✅ Parámetros usados:")
        print(f"   • Consumo energía: {default_params.energy_consumption_rate:.1f}% por tiempo")
        print(f"   • Tiempo investigación: {default_params.time_percentage*100:.0f}%")
    
    print("\n2️⃣ CONFIGURANDO PARÁMETROS PERSONALIZADOS:")
    print("-" * 50)
    
    # Crear parámetros personalizados
    custom_params = ResearchParameters(
        energy_consumption_rate=1.5,  # Menos consumo
        time_percentage=0.7,          # Más tiempo de investigación
        life_time_bonus=0.5,          # Bonus de tiempo vida
        energy_bonus_per_star=3.0,    # Bonus de energía por estrella
        knowledge_multiplier=1.5      # Multiplicador de conocimiento
    )
    
    # Configurar parámetros específicos para algunas estrellas
    custom_params.custom_star_settings = {
        '13': {
            'energy_rate': 0.5,      # Muy bajo consumo en estrella inicial
            'time_bonus': 1.0,       # Gran bonus de tiempo
            'energy_bonus': 10.0     # Gran bonus de energía
        },
        '14': {
            'energy_rate': 3.0,      # Alto consumo
            'time_bonus': -0.5,      # Penalty de tiempo
            'energy_bonus': 1.0      # Bajo bonus
        }
    }
    
    print(f"✨ Configuración personalizada:")
    print(f"   • Consumo energía general: {custom_params.energy_consumption_rate:.1f}% por tiempo")
    print(f"   • Tiempo investigación: {custom_params.time_percentage*100:.0f}%")
    print(f"   • Bonus tiempo vida: {custom_params.life_time_bonus:+.1f} años por estrella")
    print(f"   • Bonus energía: {custom_params.energy_bonus_per_star:+.1f}% por estrella")
    print(f"   • Estrellas con configuración específica: {len(custom_params.custom_star_settings)}")
    
    for star_id, config in custom_params.custom_star_settings.items():
        star = space_map.get_star(star_id)
        star_name = star.label if star else f"ID:{star_id}"
        print(f"     🌟 {star_name}: consumo={config['energy_rate']:.1f}%, bonus_tiempo={config['time_bonus']:+.1f}a, bonus_energía={config['energy_bonus']:+.1f}%")
    
    print("\n3️⃣ CALCULANDO CON PARÁMETROS PERSONALIZADOS:")
    print("-" * 50)
    
    calculator_custom = MinCostRouteCalculator(space_map, research_params=custom_params)
    result_custom = calculator_custom.calculate_min_cost_route('13')
    
    if result_custom.success:
        print(f"✅ Estrellas visitadas: {len(result_custom.star_actions)}")
        print(f"✅ Pasto consumido: {result_custom.total_grass_consumed:.2f} kg")
        print(f"✅ Energía final: {result_custom.final_energy:.1f}%")
        
        print(f"\n📊 COMPARACIÓN DE RESULTADOS:")
        print(f"   • Diferencia estrellas: {len(result_custom.star_actions) - len(result_default.star_actions):+d}")
        print(f"   • Diferencia pasto: {result_custom.total_grass_consumed - result_default.total_grass_consumed:+.2f} kg")
        print(f"   • Diferencia energía: {result_custom.final_energy - result_default.final_energy:+.1f}%")
    
    print("\n4️⃣ DETALLES DE ACCIONES CON PARÁMETROS ESPECÍFICOS:")
    print("-" * 50)
    
    if result_custom.success and len(result_custom.star_actions) > 0:
        # Mostrar primera acción en detalle
        first_action = result_custom.star_actions[0]
        detailed_dict = first_action.to_detailed_dict()
        
        print(f"🌟 Primera estrella: {detailed_dict['star_info']['label']}")
        print(f"   📊 Cálculos de investigación:")
        print(f"      • Tiempo investigación: {detailed_dict['time_distribution']['time_researching']} unidades")
        print(f"      • Tasa consumo energía: {detailed_dict['research_calculations']['energy_rate_per_time']:.1f}%")
        print(f"      • Energía consumida: {detailed_dict['research_calculations']['energy_consumed']:.1f}%")
        print(f"      • Fórmula: {detailed_dict['research_calculations']['formula']}")
        
        print(f"   ⚡ Flujo de energía:")
        print(f"      • Energía inicial: {detailed_dict['energy_flow']['initial_energy']:.1f}%")
        print(f"      • Energía tras comer: {detailed_dict['energy_flow']['energy_after_eating']:.1f}%")
        print(f"      • Energía final: {detailed_dict['energy_flow']['final_energy']:.1f}%")
    
    print("\n5️⃣ CONFIGURACIONES PREDEFINIDAS (PRESETS):")
    print("-" * 50)
    
    # Mostrar algunos presets ejemplo
    presets = [
        ("🔬 Investigador Intensivo", ResearchParameters(
            energy_consumption_rate=3.0, time_percentage=0.7, energy_bonus_per_star=5.0
        )),
        ("⚡ Conservador de Energía", ResearchParameters(
            energy_consumption_rate=1.0, time_percentage=0.3, life_time_bonus=0.5
        )),
        ("🎯 Equilibrado", ResearchParameters(
            energy_consumption_rate=2.0, time_percentage=0.5, energy_bonus_per_star=2.0
        ))
    ]
    
    for preset_name, preset_params in presets:
        calculator_preset = MinCostRouteCalculator(space_map, research_params=preset_params)
        result_preset = calculator_preset.calculate_min_cost_route('13')
        
        if result_preset.success:
            print(f"{preset_name}:")
            print(f"   • Estrellas: {len(result_preset.star_actions)}, Energía: {preset_params.energy_consumption_rate:.1f}%, Tiempo: {preset_params.time_percentage*100:.0f}%")
            print(f"   • Resultado: {result_preset.total_grass_consumed:.1f}kg pasto, {result_preset.final_energy:.1f}% energía final")
    
    print("\n" + "="*60)
    print("✅ DEMO COMPLETADO - Sistema de parámetros configurables funcional")
    print("💡 Use el botón '⚙️ Configurar Parámetros' en la GUI para la experiencia completa")


if __name__ == '__main__':
    demo_configurable_parameters()