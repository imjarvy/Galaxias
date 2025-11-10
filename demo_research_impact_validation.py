#!/usr/bin/env python3
"""
Demostración del validador de impactos de investigación por estrella.

Este script muestra cómo el sistema permite:
1. Configurar impactos específicos para cada estrella
2. Calcular efectos en salud y tiempo de vida
3. Validar rutas considerando estos impactos
4. Mostrar análisis de riesgo detallado
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

from src.models import SpaceMap
from src.research_impact_validator import ResearchImpactValidator, StarResearchImpact

def demo_research_impact_validation():
    """Demostración completa del sistema de validación de impactos."""
    print("🔬 DEMOSTRACIÓN: VALIDADOR DE IMPACTOS DE INVESTIGACIÓN")
    print("=" * 70)
    
    # Cargar mapa espacial
    space_map = SpaceMap('data/constellations.json')
    validator = ResearchImpactValidator(space_map)
    
    print("🌟 Sistema inicializado con estrellas disponibles:")
    for star in space_map.get_all_stars_list()[:5]:  # Mostrar solo las primeras 5
        print(f"   • {star.label} (ID: {star.id}) - Energía: {star.amount_of_energy}, Tiempo: {star.time_to_eat}")
    print(f"   ... y {len(space_map.get_all_stars_list()) - 5} estrellas más")
    
    print("\n" + "=" * 70)
    print("1️⃣ CONFIGURANDO IMPACTOS ESPECÍFICOS POR ESTRELLA")
    print("-" * 50)
    
    # Configurar impactos para estrellas específicas
    configuraciones = [
        {
            'star_id': '13',  # Gama23 (Hipergigante)
            'config': {
                'health_impact': 50.0,
                'health_probability': 0.8,
                'life_time_impact': 2.5,
                'energy_efficiency': 1.5,
                'experiment_bonus': 25.0
            },
            'descripcion': "Hipergigante beneficiosa - alta ganancia de salud y energía"
        },
        {
            'star_id': '3',   # Alpha53 (Hipergigante)
            'config': {
                'health_impact': 30.0,
                'health_probability': 0.9,
                'life_time_impact': 1.8,
                'energy_efficiency': 1.3,
                'experiment_bonus': 20.0
            },
            'descripcion': "Hipergigante estable - beneficios moderados pero seguros"
        },
        {
            'star_id': '14',  # Theta14
            'config': {
                'health_impact': -20.0,
                'health_probability': 0.4,
                'life_time_impact': -0.8,
                'energy_efficiency': 0.8,
                'experiment_bonus': 5.0
            },
            'descripcion': "Estrella riesgosa - posibles pérdidas de salud"
        },
        {
            'star_id': '2',   # Beta23
            'config': {
                'health_impact': 10.0,
                'health_probability': 0.6,
                'life_time_impact': 0.5,
                'energy_efficiency': 1.1,
                'experiment_bonus': 15.0
            },
            'descripcion': "Estrella equilibrada - beneficios menores pero estables"
        },
        {
            'star_id': '7',   # Zeta7
            'config': {
                'health_impact': -40.0,
                'health_probability': 0.3,
                'life_time_impact': -1.5,
                'energy_efficiency': 0.6,
                'experiment_bonus': 0.0
            },
            'descripcion': "Estrella altamente peligrosa - riesgo crítico"
        }
    ]
    
    for config_data in configuraciones:
        star_id = config_data['star_id']
        config = config_data['config']
        descripcion = config_data['descripcion']
        
        star = space_map.get_star(star_id)
        if star:
            impact = StarResearchImpact(
                star_id=star_id,
                star_label=star.label,
                base_time_to_eat=star.time_to_eat,
                base_energy=star.amount_of_energy,
                **config
            )
            
            validator.update_star_impact(star_id, impact)
            
            print(f"\n🌟 {star.label} (ID: {star_id})")
            print(f"   📝 {descripcion}")
            print(f"   💊 Impacto salud: {config['health_impact']:+.1f} (prob: {config['health_probability']:.1f})")
            print(f"   ⏰ Impacto vida: {config['life_time_impact']:+.1f} años")
            print(f"   ⚡ Eficiencia: {config['energy_efficiency']:.1f}x")
            print(f"   🎯 Bonus: {config['experiment_bonus']:.0f}%")
            print(f"   ⚠️ Riesgo: {impact.risk_level}")
    
    print("\n" + "=" * 70)
    print("2️⃣ ANÁLISIS INDIVIDUAL DETALLADO")
    print("-" * 50)
    
    for config_data in configuraciones:
        star_id = config_data['star_id']
        impact = validator.get_star_impact(star_id)
        
        if impact:
            print(f"\n🔬 ANÁLISIS DETALLADO: {impact.star_label}")
            print(f"   📊 Salud esperada: {impact.final_health_delta:+.1f} puntos")
            print(f"      Cálculo: {impact.health_impact:+.1f} × {impact.health_probability:.1f} = {impact.final_health_delta:+.1f}")
            print(f"   📊 Vida esperada: {impact.final_life_delta:+.1f} años")
            print(f"   📊 Multiplicador energético: {impact.final_energy_multiplier:.1f}x")
            print(f"   📊 Nivel de riesgo: {impact.risk_level}")
            
            if impact.risk_level in ["ALTO", "MEDIO"]:
                print(f"   🚨 ¡ATENCIÓN! Esta estrella presenta riesgos significativos")
    
    print("\n" + "=" * 70)
    print("3️⃣ VALIDACIÓN DE RUTA COMPLETA")
    print("-" * 50)
    
    # Simular una ruta que incluye varias estrellas configuradas
    ruta_ejemplo = ['13', '3', '14', '2', '7']  # Hipergigantes + algunas riesgosas
    
    print("🚀 Simulando ruta de ejemplo:")
    route_names = []
    for star_id in ruta_ejemplo:
        star = space_map.get_star(star_id)
        if star:
            route_names.append(star.label)
    
    print(f"   Ruta: {' → '.join(route_names)}")
    
    # Calcular impacto total de la ruta
    route_impact = validator.calculate_route_impact(ruta_ejemplo)
    
    print(f"\n📊 IMPACTO TOTAL DE LA RUTA:")
    print(f"   🔬 Estrellas analizadas: {route_impact['stars_analyzed']}")
    print(f"   💊 Impacto total en salud: {route_impact['total_health_impact']:+.1f} puntos")
    print(f"   ⏰ Impacto total en vida: {route_impact['total_life_impact']:+.1f} años")
    print(f"   ⚡ Multiplicador energético: {route_impact['energy_efficiency_multiplier']:.3f}x")
    print(f"   ⚠️ Riesgo general: {route_impact['overall_risk']}")
    
    print(f"\n🚨 ANÁLISIS DE RIESGO:")
    if route_impact['risk_stars']:
        print(f"   Estrellas de riesgo encontradas: {len(route_impact['risk_stars'])}")
        for risk_star in route_impact['risk_stars']:
            print(f"   • {risk_star['star']} - Riesgo {risk_star['risk']}")
            print(f"     Salud: {risk_star['health_impact']:+.1f}, Vida: {risk_star['life_impact']:+.1f}a")
    else:
        print(f"   ✅ No se detectaron estrellas de alto riesgo")
    
    print("\n" + "=" * 70)
    print("4️⃣ RECOMENDACIONES AUTOMÁTICAS")
    print("-" * 50)
    
    # Generar recomendaciones basadas en el análisis
    recomendaciones = []
    
    if route_impact['overall_risk'] == "CRÍTICO":
        recomendaciones.append("🚨 CRÍTICO: Considere replantear completamente la ruta")
    elif route_impact['overall_risk'] == "ALTO":
        recomendaciones.append("⚠️ ALTO RIESGO: Evite estrellas peligrosas si es posible")
    
    if route_impact['total_health_impact'] < -30:
        recomendaciones.append("💊 Prepare medicinas adicionales para compensar pérdida de salud")
    
    if route_impact['total_life_impact'] < -2:
        recomendaciones.append("⏰ Considere acelerar la misión para compensar pérdida de tiempo")
    
    if route_impact['energy_efficiency_multiplier'] < 0.8:
        recomendaciones.append("⚡ Lleve suministros energéticos adicionales")
    
    if len(route_impact['risk_stars']) > 2:
        recomendaciones.append("🔀 Considere rutas alternativas evitando tantas estrellas riesgosas")
    
    if route_impact['total_health_impact'] > 50:
        recomendaciones.append("✅ Excelente ruta para mejorar la salud del astronauta")
    
    if recomendaciones:
        print("📋 RECOMENDACIONES AUTOMÁTICAS:")
        for i, recomendacion in enumerate(recomendaciones, 1):
            print(f"   {i}. {recomendacion}")
    else:
        print("✅ Ruta bien balanceada - no se requieren ajustes especiales")
    
    print("\n" + "=" * 70)
    print("5️⃣ EXPORTACIÓN DE CONFIGURACIÓN")
    print("-" * 50)
    
    # Mostrar ejemplo de configuración exportada
    config_json = validator.export_configuration()
    print("💾 Configuración exportable (primeras líneas):")
    lines = config_json.split('\n')[:15]
    for line in lines:
        print(f"   {line}")
    print(f"   ... ({len(lines)} líneas en total)")
    
    print("\n" + "=" * 70)
    print("✅ DEMOSTRACIÓN COMPLETADA")
    print("=" * 70)
    
    print("🎯 CARACTERÍSTICAS DEMOSTRADAS:")
    print("   ✅ Configuración manual de impactos por estrella")
    print("   ✅ Cálculo automático de efectos en salud y vida")
    print("   ✅ Análisis de riesgo por estrella individual")
    print("   ✅ Validación de impacto total de rutas")
    print("   ✅ Recomendaciones automáticas de seguridad")
    print("   ✅ Exportación/importación de configuraciones")
    
    print("\n💡 FUNCIONALIDADES IMPLEMENTADAS:")
    print("   🔬 Validación de impactos de investigación por estrella")
    print("   📊 Cálculo de probabilidades y efectos específicos")
    print("   ⚠️ Sistema de análisis de riesgo automático")
    print("   🎛️ Interfaz gráfica para configuración manual")
    print("   🔄 Recálculo automático de rutas con nuevos impactos")
    print("   💾 Persistencia de configuraciones personalizadas")
    
    print("\n🚀 Use la GUI principal para acceder a todas estas funcionalidades!")

if __name__ == "__main__":
    demo_research_impact_validation()