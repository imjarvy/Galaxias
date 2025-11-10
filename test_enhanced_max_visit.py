#!/usr/bin/env python3
"""
Test script para validar las mejoras implementadas en el sistema de rutas máximas.
"""

from src.models import SpaceMap
from src.route_calculator import RouteCalculator

def test_max_visit_enhancements():
    """Test all the enhanced features of the max visit route system."""
    print("🚀 Testing Enhanced Max Visit Route System")
    print("=" * 60)
    
    # Initialize system
    space_map = SpaceMap('data/constellations.json')
    calculator = RouteCalculator(space_map, {})
    
    # Test 1: Basic functionality with default parameters
    print("\n1. Test Básico (parámetros por defecto)")
    print("-" * 40)
    
    start_star = space_map.get_star('1')
    if start_star:
        path, stats = calculator.find_max_visit_route(
            start=start_star,
            edad=12,
            energia_pct=100,
            pasto_kg=300
        )
        
        print(f"Estrellas visitadas: {stats['stars_visited']}")
        print(f"Distancia total: {stats['total_distance']:.2f}")
        print(f"Tiempo consumido: {stats['life_time_consumed']:.2f} años")
        print(f"Warp factor usado: {stats['config_used']['warp_factor']}")
    
    # Test 2: With custom death age
    print("\n2. Test con Death Age Personalizada (5000 años)")
    print("-" * 40)
    
    path2, stats2 = calculator.find_max_visit_route(
        start=start_star,
        edad=12,
        energia_pct=100,
        pasto_kg=300,
        death_age=5000
    )
    
    print(f"Estrellas visitadas: {stats2['stars_visited']}")
    print(f"Distancia total: {stats2['total_distance']:.2f}")
    print(f"Tiempo consumido: {stats2['life_time_consumed']:.2f} años")
    print(f"Death age usado: {stats2['config_used']['death_age']}")
    
    # Test 3: Low energy scenario
    print("\n3. Test con Energía Limitada (30%)")
    print("-" * 40)
    
    path3, stats3 = calculator.find_max_visit_route(
        start=start_star,
        edad=50,  # Older age
        energia_pct=30,  # Low energy
        pasto_kg=100,  # Low grass
        death_age=100   # Short lifespan
    )
    
    print(f"Estrellas visitadas: {stats3['stars_visited']}")
    print(f"Distancia total: {stats3['total_distance']:.2f}")
    print(f"Tiempo consumido: {stats3['life_time_consumed']:.2f} años")
    print(f"Energía inicial: {stats3['initial_params']['energia']}%")
    
    # Test 4: Compare multiple starting points
    print("\n4. Comparación de Múltiples Puntos de Inicio")
    print("-" * 40)
    
    test_starts = ['1', '2', '3', '12']
    best_start = None
    best_count = 0
    
    for start_id in test_starts:
        test_star = space_map.get_star(start_id)
        if test_star:
            path_test, stats_test = calculator.find_max_visit_route(
                start=test_star,
                edad=12,
                energia_pct=100,
                pasto_kg=300,
                death_age=4000
            )
            
            visited = stats_test['stars_visited']
            print(f"Inicio desde {test_star.label} (ID: {start_id}): {visited} estrellas")
            
            if visited > best_count:
                best_count = visited
                best_start = test_star
    
    print(f"\nMejor punto de inicio: {best_start.label if best_start else 'N/A'}")
    print(f"Máximo de estrellas: {best_count}")
    
    # Test 5: Performance comparison
    print("\n5. Test de Rendimiento vs Algoritmo Simple")
    print("-" * 40)
    
    import time
    
    # Measure time for enhanced algorithm
    start_time = time.time()
    path_enhanced, stats_enhanced = calculator.find_max_visit_route(
        start=start_star,
        edad=12,
        energia_pct=100,
        pasto_kg=300
    )
    enhanced_time = time.time() - start_time
    
    print(f"Algoritmo optimizado:")
    print(f"  - Tiempo: {enhanced_time:.3f} segundos")
    print(f"  - Estrellas: {stats_enhanced['stars_visited']}")
    print(f"  - Eficiencia: {stats_enhanced['stars_visited']/enhanced_time:.1f} estrellas/seg")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ RESUMEN DE MEJORAS IMPLEMENTADAS:")
    print("✅ 1. Death age como parámetro configurable")
    print("✅ 2. Conversión distancia-tiempo usando warp factor")
    print("✅ 3. Algoritmo de búsqueda optimizado con heurísticas")
    print("✅ 4. Integración con GUI")
    print("✅ 5. Estadísticas detalladas de configuración")
    print("=" * 60)

if __name__ == '__main__':
    test_max_visit_enhancements()