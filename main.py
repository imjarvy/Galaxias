#!/usr/bin/env python3
"""
Galaxias - Sistema Interactivo de Rutas Espaciales del Burro Astronauta
=======================================================================

Sistema de simulación de rutas espaciales entre estrellas de constelaciones
con un burro astronauta que come estrellas para obtener energía.

Uso:
    python main.py              # Iniciar GUI
    python main.py --cli        # Modo línea de comandos
    python main.py --demo       # Ejecutar demostración
"""

import sys
import json
import argparse
from src.models import SpaceMap, BurroAstronauta, Comet
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer
from src.donkey_optimization import DonkeyRouteOptimizer


def run_gui():
    """Run the graphical user interface."""
    from src.gui import main
    main()


def run_cli():
    """Run in command-line interface mode."""
    print("=" * 60)
    print("🫏 GALAXIAS - Sistema del Burro Astronauta 🌟")
    print("=" * 60)
    print()
    
    # Load configuration
    with open('data/spaceship_config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize space map
    space_map = SpaceMap('data/constellations.json')
    
    # Initialize burro astronauta
    burro = space_map.create_burro_astronauta()
    
    # Initialize calculator, visualizer and optimizer
    calculator = RouteCalculator(space_map, config)
    visualizer = SpaceVisualizer(space_map)
    optimizer = DonkeyRouteOptimizer(space_map)
    
    # Display available stars
    print("Estrellas disponibles:")
    stars_list = space_map.get_all_stars_list()
    for i, star in enumerate(stars_list, 1):
        hypergiant_mark = "⭐" if star.hypergiant else "✨"
        print(f"  {i}. {hypergiant_mark} {star.label} ({star.id}) - Energía: {star.amount_of_energy}, Radio: {star.radius}")
    print()
    
    # Show burro status
    print("Estado inicial del Burro Astronauta:")
    status = burro.get_status()
    print(f"  Energía: {status['energia']}%")
    print(f"  Pasto: {status['pasto']} kg")
    print(f"  Edad: {status['edad']} años")
    print(f"  Estado de salud: {status['estado_salud']}")
    print()
    
    # Get user input for route type
    print("Opciones:")
    print("1. Calcular ruta directa entre dos estrellas")
    print("2. Optimizar ruta para comer máximo número de estrellas")
    
    try:
        option = int(input("Seleccione opción (1-2): "))
        
        if option == 1:
            # Direct route between two stars
            start_idx = int(input("Seleccione número de estrella origen (1-{}): ".format(len(stars_list)))) - 1
            end_idx = int(input("Seleccione número de estrella destino (1-{}): ".format(len(stars_list)))) - 1
            
            if 0 <= start_idx < len(stars_list) and 0 <= end_idx < len(stars_list):
                start_star = stars_list[start_idx]
                end_star = stars_list[end_idx]
                
                print(f"\nCalculando ruta de {start_star.label} a {end_star.label}...")
                
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
                    print(f"  - Energía para viajar: {path_stats['total_energy_needed']:.2f}")
                    print(f"  - Pasto necesario: {path_stats['total_grass_needed']:.2f} kg")
                    print(f"  - Energía ganada: {path_stats['total_energy_gained']:.2f}")
                    print(f"  - Balance neto: {path_stats['net_energy']:.2f}")
                else:
                    print("\n❌ No se encontró ruta entre estas estrellas.")
            else:
                print("Índices inválidos.")
        
        elif option == 2:
            # Optimize route for eating stars
            start_idx = int(input("Seleccione número de estrella origen (1-{}): ".format(len(stars_list)))) - 1
            
            if 0 <= start_idx < len(stars_list):
                start_star = stars_list[start_idx]
                
                print(f"\nOptimizando ruta desde {start_star.label} para comer máximo número de estrellas...")
                
                # Optimize route
                optimal_path, stats = optimizer.optimize_route_from_json_data(start_star.id)
                
                if stats.get('error'):
                    print(f"\n❌ Error: {stats['error']}")
                elif optimal_path:
                    print("\n" + "=" * 60)
                    print("RUTA OPTIMIZADA ENCONTRADA")
                    print("=" * 60)
                    print(f"Estrellas visitadas: {stats['stars_visited']}")
                    print(f"Energía final: {stats['final_energy']}%")
                    print(f"Pasto final: {stats['final_grass']} kg")
                    print(f"Estado final: {stats['final_health_state']}")
                    print(f"Éxito: {'SÍ' if stats['success'] else 'NO'}")
                    print(f"\nRuta optimizada: {' → '.join(stats['route'])}")
                else:
                    print("\n❌ No se pudo encontrar una ruta optimizada.")
            else:
                print("Índice inválido.")
        
        else:
            print("Opción inválida.")
        
        # Generate visualization
        response = input("\n¿Generar visualización? (s/n): ").lower()
        if response == 's':
            print("\nGenerando visualización...")
            if option == 1 and 'path' in locals() and path:
                visualizer.plot_space_map(
                    highlight_path=path,
                    donkey_location=burro.current_location,
                    save_path='assets/space_map.png'
                )
            elif option == 2 and 'optimal_path' in locals() and optimal_path:
                visualizer.plot_space_map(
                    highlight_path=optimal_path,
                    donkey_location=burro.current_location,
                    save_path='assets/space_map.png'
                )
            print("Visualización guardada en: assets/space_map.png")
    
    except (ValueError, KeyboardInterrupt):
        print("\nOperación cancelada.")
    except Exception as e:
        print(f"\nError: {e}")


def run_demo():
    """Run a demonstration of the system."""
    print("=" * 60)
    print("🫏 GALAXIAS - DEMOSTRACIÓN DEL BURRO ASTRONAUTA 🌟")
    print("=" * 60)
    print()
    
    # Load configuration
    with open('data/spaceship_config.json', 'r') as f:
        config = json.load(f)
    
    # Initialize space map
    space_map = SpaceMap('data/constellations.json')
    
    # Initialize burro astronauta
    burro = space_map.create_burro_astronauta()
    
    # Initialize calculator, visualizer and optimizer
    calculator = RouteCalculator(space_map, config)
    visualizer = SpaceVisualizer(space_map)
    optimizer = DonkeyRouteOptimizer(space_map)
    
    print("1. Estado inicial del burro:")
    status = burro.get_status()
    print(f"   Energía: {status['energia']}%")
    print(f"   Pasto: {status['pasto']} kg")
    print(f"   Estado: {status['estado_salud']}")
    
    print("\n2. Estrellas disponibles:")
    stars_list = space_map.get_all_stars_list()
    for star in stars_list[:5]:  # Show first 5
        hypergiant_mark = "⭐" if star.hypergiant else "✨"
        print(f"   {hypergiant_mark} {star.label} - Energía: {star.amount_of_energy}, Radio: {star.radius}")
    
    print("\n3. Calculando ruta optimizada...")
    start_star = stars_list[0]
    optimal_path, stats = optimizer.optimize_route_from_json_data(start_star.id)
    
    if optimal_path and stats.get('success'):
        print(f"   ✅ Ruta optimizada encontrada")
        print(f"   Estrellas visitadas: {stats['stars_visited']}")
        print(f"   Energía final: {stats['final_energy']}%")
        print(f"   Ruta: {' → '.join(stats['route'][:5])}{'...' if len(stats['route']) > 5 else ''}")
    else:
        print("   ❌ No se pudo optimizar la ruta")
    
    print("\n4. Agregando cometa que bloquea rutas...")
    # Get first two stars for demonstration
    if len(stars_list) >= 2:
        star1, star2 = stars_list[0], stars_list[1]
        comet = Comet(name="Cometa Halley", blocked_routes=[(star1.id, star2.id)])
        space_map.add_comet(comet)
        print(f"   ✅ Cometa agregado bloqueando ruta entre {star1.label} y {star2.label}")
    
    print("\n5. Recalculando con cometa...")
    optimal_path2, stats2 = optimizer.optimize_route_from_json_data(start_star.id)
    
    if optimal_path2:
        print(f"   ✅ Nueva ruta encontrada evitando el cometa")
        print(f"   Estrellas visitadas: {stats2['stars_visited']}")
        print(f"   Energía final: {stats2['final_energy']}%")
    else:
        print("   ❌ No se pudo encontrar nueva ruta")
    
    print("\n6. Generando visualizaciones...")
    visualizer.plot_space_map(
        highlight_path=optimal_path2 if optimal_path2 else optimal_path,
        donkey_location=burro.current_location,
        save_path='assets/demo_space_map.png',
        show=False
    )
    print("   ✅ Mapa guardado: assets/demo_space_map.png")
    
    visualizer.plot_resource_status(
        burro,
        save_path='assets/demo_resources.png',
        show=False
    )
    print("   ✅ Estado de recursos guardado: assets/demo_resources.png")
    
    if optimal_path2 or optimal_path:
        path_to_use = optimal_path2 if optimal_path2 else optimal_path
        stats_to_use = stats2 if optimal_path2 else stats
        path_stats = calculator.calculate_path_stats(path_to_use)
        
        visualizer.plot_journey_report(
            burro,
            path_stats,
            save_path='assets/demo_report.png',
            show=False
        )
        print("   ✅ Reporte guardado: assets/demo_report.png")
    
    print("\n" + "=" * 60)
    print("DEMOSTRACIÓN COMPLETADA")
    print("Archivos generados en la carpeta 'assets/'")
    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Galaxias - Sistema del Burro Astronauta'
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
