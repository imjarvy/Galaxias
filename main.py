#!/usr/bin/env python3
"""
Galaxias - Sistema Interactivo de Rutas Espaciales
===================================================

Sistema de simulación de rutas espaciales entre estrellas de constelaciones
cercanas en la Vía Láctea con un burro astronauta.

Uso:
    python main.py              # Iniciar GUI
    python main.py --cli        # Modo línea de comandos
    python main.py --demo       # Ejecutar demostración
"""

import sys
import json
import argparse
from src.models import SpaceMap, SpaceshipDonkey, Comet
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer


def run_gui():
    """Run the graphical user interface."""
    from src.gui import main
    main()


def run_cli():
    """Run in command-line interface mode."""
    print("=" * 60)
    print("🫏 GALAXIAS - Sistema de Rutas Espaciales 🚀")
    print("=" * 60)
    print()
    
    # Load configuration
    with open('data/spaceship_config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize space map
    space_map = SpaceMap('data/constellations.json')
    
    # Initialize spaceship donkey
    ship_config = config['spaceship_donkey']
    donkey = SpaceshipDonkey(
        name=ship_config['name'],
        health=ship_config['initial_health'],
        fuel=ship_config['initial_fuel'],
        food=ship_config['initial_food'],
        oxygen=ship_config['initial_oxygen']
    )
    
    # Initialize calculator and visualizer
    calculator = RouteCalculator(space_map, config)
    visualizer = SpaceVisualizer(space_map)
    
    # Display available stars
    print("Estrellas disponibles:")
    stars_list = space_map.get_all_stars_list()
    for i, star in enumerate(stars_list, 1):
        print(f"  {i}. {star.name} ({star.id}) - {star.type}")
    print()
    
    # Get user input for route
    try:
        start_idx = int(input("Seleccione número de estrella origen (1-{}): ".format(len(stars_list)))) - 1
        end_idx = int(input("Seleccione número de estrella destino (1-{}): ".format(len(stars_list)))) - 1
        
        if 0 <= start_idx < len(stars_list) and 0 <= end_idx < len(stars_list):
            start_star = stars_list[start_idx]
            end_star = stars_list[end_idx]
            
            print(f"\nCalculando ruta de {start_star.name} a {end_star.name}...")
            
            # Calculate path
            path, cost = calculator.dijkstra(start_star, end_star)
            
            if path:
                path_stats = calculator.calculate_path_stats(path)
                
                print("\n" + "=" * 60)
                print("RUTA ENCONTRADA")
                print("=" * 60)
                print(f"Costo total: {cost:.2f}")
                print(f"Distancia: {path_stats['total_distance']} unidades")
                print(f"Saltos: {path_stats['num_jumps']}")
                print(f"Peligro: {path_stats['total_danger']}")
                print(f"\nRuta: {' → '.join(path_stats['path_stars'])}")
                print(f"\nRecursos necesarios:")
                print(f"  - Combustible: {path_stats['total_fuel_needed']}")
                print(f"  - Comida: {path_stats['total_food_needed']}")
                print(f"  - Oxígeno: {path_stats['total_oxygen_needed']}")
                print(f"  - Pérdida de salud: {path_stats['estimated_health_loss']}")
                
                # Ask if user wants to start journey
                response = input("\n¿Iniciar viaje? (s/n): ").lower()
                if response == 's':
                    # Simulate journey
                    donkey.current_location = path[0]
                    donkey.journey_history = [path[0]]
                    
                    for i in range(len(path) - 1):
                        current_star = path[i]
                        next_star = path[i + 1]
                        
                        # Find the route
                        route = None
                        for r in space_map.routes:
                            if ((r.from_star == current_star and r.to_star == next_star) or
                                (r.to_star == current_star and r.from_star == next_star)):
                                route = r
                                break
                        
                        if route:
                            print(f"\nViajando de {current_star.name} a {next_star.name}...")
                            donkey.consume_resources(route.distance, route.danger_level, config)
                            donkey.current_location = next_star
                            donkey.journey_history.append(next_star)
                            
                            status = donkey.get_status()
                            print(f"  Salud: {status['health']:.1f}, "
                                  f"Combustible: {status['fuel']:.1f}, "
                                  f"Oxígeno: {status['oxygen']:.1f}")
                            
                            if not donkey.is_alive():
                                print(f"\n❌ El Burro Astronauta no sobrevivió el viaje.")
                                print(f"   Llegó hasta: {next_star.name}")
                                break
                    
                    if donkey.is_alive():
                        print(f"\n✅ ¡Viaje exitoso!")
                        print(f"   El Burro Astronauta llegó a {donkey.current_location.name}")
                        print(f"   Salud restante: {donkey.health:.1f}")
                
                # Generate visualization
                response = input("\n¿Generar visualización? (s/n): ").lower()
                if response == 's':
                    print("\nGenerando visualización...")
                    visualizer.plot_space_map(
                        highlight_path=path,
                        donkey_location=donkey.current_location,
                        save_path='assets/space_map.png'
                    )
                    print("Visualización guardada en: assets/space_map.png")
                    
                    visualizer.plot_journey_report(
                        donkey,
                        path_stats,
                        save_path='assets/journey_report.png'
                    )
                    print("Reporte guardado en: assets/journey_report.png")
            else:
                print("\n❌ No se encontró ruta entre estas estrellas.")
        else:
            print("Índices inválidos.")
    
    except (ValueError, KeyboardInterrupt):
        print("\nOperación cancelada.")
    except Exception as e:
        print(f"\nError: {e}")


def run_demo():
    """Run a demonstration of the system."""
    print("=" * 60)
    print("🫏 GALAXIAS - DEMOSTRACIÓN 🚀")
    print("=" * 60)
    print()
    
    # Load configuration
    with open('data/spaceship_config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize space map
    space_map = SpaceMap('data/constellations.json')
    
    # Initialize spaceship donkey
    ship_config = config['spaceship_donkey']
    donkey = SpaceshipDonkey(
        name=ship_config['name'],
        health=ship_config['initial_health'],
        fuel=ship_config['initial_fuel'],
        food=ship_config['initial_food'],
        oxygen=ship_config['initial_oxygen']
    )
    
    # Initialize calculator and visualizer
    calculator = RouteCalculator(space_map, config)
    visualizer = SpaceVisualizer(space_map)
    
    print("1. Calculando ruta de Betelgeuse a Sirius...")
    start_star = space_map.get_star('orion_1')  # Betelgeuse
    end_star = space_map.get_star('canis_1')    # Sirius
    
    path, cost = calculator.dijkstra(start_star, end_star)
    
    if path:
        path_stats = calculator.calculate_path_stats(path)
        print(f"   ✅ Ruta encontrada: {' → '.join([s.name for s in path])}")
        print(f"   Distancia: {path_stats['total_distance']} unidades")
        print(f"   Saltos: {path_stats['num_jumps']}")
    
    print("\n2. Agregando cometa Halley que bloquea Orion-Canis...")
    comet = Comet(name="Halley", blocked_routes=[('orion_2', 'canis_1')])
    space_map.add_comet(comet)
    print("   ✅ Cometa agregado")
    
    print("\n3. Recalculando ruta con cometa...")
    path2, cost2 = calculator.dijkstra(start_star, end_star)
    if path2:
        path_stats2 = calculator.calculate_path_stats(path2)
        print(f"   ✅ Nueva ruta encontrada: {' → '.join([s.name for s in path2])}")
        print(f"   Distancia: {path_stats2['total_distance']} unidades")
    
    print("\n4. Simulando viaje...")
    donkey.current_location = path2[0]
    donkey.journey_history = [path2[0]]
    
    for i in range(len(path2) - 1):
        current_star = path2[i]
        next_star = path2[i + 1]
        
        # Find the route
        route = None
        for r in space_map.routes:
            if ((r.from_star == current_star and r.to_star == next_star) or
                (r.to_star == current_star and r.from_star == next_star)):
                route = r
                break
        
        if route:
            donkey.consume_resources(route.distance, route.danger_level, config)
            donkey.current_location = next_star
            donkey.journey_history.append(next_star)
    
    print(f"   ✅ Viaje completado")
    print(f"   Salud final: {donkey.health:.1f}")
    print(f"   Combustible restante: {donkey.fuel:.1f}")
    
    print("\n5. Generando visualizaciones...")
    visualizer.plot_space_map(
        highlight_path=path2,
        donkey_location=donkey.current_location,
        save_path='assets/demo_space_map.png',
        show=False
    )
    print("   ✅ Mapa guardado: assets/demo_space_map.png")
    
    visualizer.plot_resource_status(
        donkey,
        save_path='assets/demo_resources.png',
        show=False
    )
    print("   ✅ Estado de recursos guardado: assets/demo_resources.png")
    
    visualizer.plot_journey_report(
        donkey,
        path_stats2,
        save_path='assets/demo_report.png',
        show=False
    )
    print("   ✅ Reporte guardado: assets/demo_report.png")
    
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN COMPLETADA")
    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Galaxias - Sistema Interactivo de Rutas Espaciales'
    )
    parser.add_argument('--cli', action='store_true',
                       help='Ejecutar en modo línea de comandos')
    parser.add_argument('--demo', action='store_true',
                       help='Ejecutar demostración')
    
    args = parser.parse_args()
    
    if args.cli:
        run_cli()
    elif args.demo:
        run_demo()
    else:
        run_gui()


if __name__ == "__main__":
    main()
