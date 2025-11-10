#!/usr/bin/env python3
"""
Ejemplo de uso del nuevo sistema Galaxias basado en los JSONs actualizados.
Este archivo demuestra cómo usar todas las funcionalidades del sistema.
"""

from src.models import SpaceMap, BurroAstronauta
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer
from src.donkey_optimization import DonkeyRouteOptimizer
import json

def main():
    print("=" * 70)
    print("🫏 EJEMPLO DEL NUEVO SISTEMA GALAXIAS 🌟")
    print("=" * 70)
    print()
    
    # 1. Cargar el mapa espacial desde el JSON
    print("1. Cargando mapa espacial...")
    space_map = SpaceMap('data/constellations.json')
    print(f"   ✅ Cargadas {len(space_map.stars)} estrellas")
    print(f"   ✅ Generadas {len(space_map.routes)} rutas")
    
    # 2. Crear el burro astronauta con datos del JSON
    print("\n2. Creando burro astronauta...")
    burro = space_map.create_burro_astronauta()
    status = burro.get_status()
    print(f"   ✅ Burro creado: {status['name']}")
    print(f"   📊 Energía inicial: {status['energia']}%")
    print(f"   🌾 Pasto inicial: {status['pasto']} kg")
    print(f"   👶 Edad: {status['edad']} años")
    print(f"   ❤️ Estado: {status['estado_salud']}")
    
    # 3. Mostrar información de estrellas
    print("\n3. Información de estrellas disponibles:")
    stars_list = space_map.get_all_stars_list()
    for star in stars_list:
        type_icon = "⭐" if star.hypergiant else "✨"
        print(f"   {type_icon} {star.label} (ID: {star.id})")
        print(f"      Energía: {star.amount_of_energy}, Radio: {star.radius}, Tiempo: {star.time_to_eat}")
        print(f"      Coordenadas: ({star.x}, {star.y})")
        print()
    
    # 4. Inicializar herramientas
    print("4. Inicializando herramientas...")
    config = {
        'consumption_rates': {
            'fuel_per_unit_distance': 2,
            'food_per_unit_distance': 0.1,
            'oxygen_per_unit_distance': 0.5,
            'health_decay_per_danger': 5
        }
    }
    
    calculator = RouteCalculator(space_map, config)
    visualizer = SpaceVisualizer(space_map)
    optimizer = DonkeyRouteOptimizer(space_map)
    
    # 5. Ejemplo de ruta directa
    print("\n5. Calculando ruta directa...")
    if len(stars_list) >= 2:
        start_star = stars_list[0]
        end_star = stars_list[1]
        
        path, cost = calculator.dijkstra(start_star, end_star)
        if path:
            stats = calculator.calculate_path_stats(path)
            print(f"   ✅ Ruta encontrada de {start_star.label} a {end_star.label}")
            print(f"   📏 Distancia: {stats['total_distance']:.2f}")
            print(f"   🦘 Saltos: {stats['num_jumps']}")
            print(f"   ⚡ Energía necesaria: {stats['total_energy_needed']:.2f}")
            print(f"   🌾 Pasto necesario: {stats['total_grass_needed']:.2f} kg")
            print(f"   💎 Energía ganada: {stats['total_energy_gained']:.2f}")
            print(f"   📊 Balance neto: {stats['net_energy']:.2f}")
    
    # 6. Ejemplo de optimización de ruta
    print("\n6. Optimizando ruta para comer estrellas...")
    if stars_list:
        start_star = stars_list[0]
        optimal_path, opt_stats = optimizer.optimize_route_from_json_data(start_star.id)
        
        if opt_stats.get('success'):
            print(f"   ✅ Ruta optimizada encontrada")
            print(f"   🌟 Estrellas visitadas: {opt_stats['stars_visited']}")
            print(f"   ⚡ Energía final: {opt_stats['final_energy']}%")
            print(f"   🌾 Pasto final: {opt_stats['final_grass']} kg")
            print(f"   ❤️ Estado final: {opt_stats['final_health_state']}")
            print(f"   🛤️ Ruta: {' → '.join(opt_stats['route'][:5])}")
            if len(opt_stats['route']) > 5:
                print(f"      ... y {len(opt_stats['route']) - 5} más")
        else:
            print("   ❌ No se pudo optimizar la ruta")
    
    # 7. Ejemplo de simulación de viaje
    print("\n7. Simulando consumo de recursos al comer una estrella...")
    if stars_list:
        test_star = stars_list[0]
        print(f"   🎯 Estrella objetivo: {test_star.label}")
        print(f"   📊 Estado antes - Energía: {burro.current_energy}%, Pasto: {burro.current_pasto}kg")
        
        if burro.can_eat_star(test_star):
            burro.consume_resources_eating_star(test_star)
            print(f"   ✅ Estrella consumida exitosamente")
            print(f"   📊 Estado después - Energía: {burro.current_energy}%, Pasto: {burro.current_pasto}kg")
            print(f"   ❤️ Nuevo estado de salud: {burro.estado_salud}")
        else:
            print("   ❌ No se puede comer esta estrella (recursos insuficientes)")
    
    # 8. Ejemplo de viaje entre estrellas
    print("\n8. Simulando viaje entre estrellas...")
    if len(stars_list) >= 2:
        star1, star2 = stars_list[0], stars_list[1]
        path, _ = calculator.dijkstra(star1, star2)
        
        if path and len(path) >= 2:
            # Calcular distancia total
            total_distance = 0
            for i in range(len(path) - 1):
                current = path[i]
                next_star = path[i + 1]
                for route in space_map.routes:
                    if ((route.from_star == current and route.to_star == next_star) or
                        (route.to_star == current and route.from_star == next_star)):
                        total_distance += route.distance
                        break
            
            print(f"   🚀 Viajando de {star1.label} a {star2.label}")
            print(f"   📏 Distancia: {total_distance:.2f}")
            print(f"   📊 Estado antes - Energía: {burro.current_energy}%")
            
            if burro.can_travel(total_distance):
                burro.consume_resources_traveling(total_distance)
                burro.current_location = star2
                print(f"   ✅ Viaje completado")
                print(f"   📊 Estado después - Energía: {burro.current_energy}%")
            else:
                print("   ❌ No se puede realizar el viaje (energía insuficiente)")
    
    # 9. Estado final
    print("\n9. Estado final del burro astronauta:")
    final_status = burro.get_status()
    print(f"   📍 Ubicación: {final_status['location']}")
    print(f"   ⚡ Energía: {final_status['energia']}%")
    print(f"   🌾 Pasto: {final_status['pasto']} kg")
    print(f"   ❤️ Estado: {final_status['estado_salud']}")
    print(f"   🚀 Viajes realizados: {final_status['journey_length']}")
    print(f"   💚 ¿Está vivo?: {'SÍ' if final_status['is_alive'] else 'NO'}")
    
    print("\n" + "=" * 70)
    print("✅ EJEMPLO COMPLETADO")
    print("💡 Para usar el sistema completo, ejecute: python main.py")
    print("🎮 Para la interfaz gráfica: python main.py")
    print("💻 Para línea de comandos: python main.py --cli")
    print("🎬 Para demostración: python main.py --demo")
    print("=" * 70)

if __name__ == "__main__":
    main()