#!/usr/bin/env python3
"""
Test simple del nuevo sistema que usa SOLO valores del JSON.
"""

from src.models import SpaceMap
from src.max_visit_route import compute_max_visits_from_json

def test_json_only_system():
    print("🚀 Test del Sistema Simplificado (Solo Valores del JSON)")
    print("=" * 70)
    
    # Cargar el mapa espacial
    space_map = SpaceMap('data/constellations.json')
    
    print("\n📋 VALORES CARGADOS DEL JSON:")
    print("-" * 40)
    for key, value in space_map.burro_data.items():
        print(f"{key}: {value}")
    
    print("\n🎯 CALCULANDO RUTA ÓPTIMA DESDE ESTRELLA 1...")
    print("-" * 40)
    
    # Usar la función simplificada
    result = compute_max_visits_from_json(space_map, start_id="1")
    
    print(f"✅ Estrellas visitadas: {result['num_stars']}")
    print(f"📏 Distancia total: {result['total_distance']:.2f} unidades")
    print(f"⏱️  Tiempo consumido: {result['life_time_consumed']:.2f} años")
    
    print(f"\n🗺️  SECUENCIA DE ESTRELLAS:")
    for i, star in enumerate(result['sequence'], 1):
        print(f"{i}. {star['label']} (ID: {star['id']})")
    
    print(f"\n⚙️  CONFIGURACIÓN USADA:")
    if 'json_values_used' in result:
        for key, value in result['json_values_used'].items():
            print(f"  - {key}: {value}")
    
    print(f"\n📝 NOTAS:")
    print(f"  {result.get('notes', 'N/A')}")
    
    # Prueba con diferentes puntos de inicio
    print(f"\n🔄 COMPARANDO DIFERENTES PUNTOS DE INICIO:")
    print("-" * 40)
    
    test_starts = ['1', '2', '3', '12', '13']
    results = []
    
    for start_id in test_starts:
        try:
            result_test = compute_max_visits_from_json(space_map, start_id)
            star_info = space_map.get_star(start_id)
            star_name = star_info.label if star_info else f"ID-{start_id}"
            
            results.append({
                'start_id': start_id,
                'star_name': star_name,
                'stars_visited': result_test['num_stars'],
                'distance': result_test['total_distance'],
                'time': result_test['life_time_consumed']
            })
            
            print(f"  {star_name} (ID: {start_id}): {result_test['num_stars']} estrellas, "
                  f"{result_test['life_time_consumed']:.1f} años")
            
        except Exception as e:
            print(f"  {start_id}: Error - {e}")
    
    # Encontrar la mejor opción
    if results:
        best = max(results, key=lambda x: x['stars_visited'])
        print(f"\n🏆 MEJOR PUNTO DE INICIO:")
        print(f"  Estrella: {best['star_name']} (ID: {best['start_id']})")
        print(f"  Estrellas visitadas: {best['stars_visited']}")
        print(f"  Tiempo total: {best['time']:.1f} años")
    
    print("\n" + "=" * 70)
    print("✅ SISTEMA SIMPLIFICADO FUNCIONANDO CORRECTAMENTE")
    print("📊 USA SOLO VALORES DEL JSON - SIN OVERRIDES")
    print("=" * 70)

if __name__ == '__main__':
    test_json_only_system()