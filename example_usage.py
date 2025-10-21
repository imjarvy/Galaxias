#!/usr/bin/env python3
"""
Example script demonstrating programmatic use of Galaxias.

This shows how to use the Galaxias API without the GUI or CLI.
"""

import json
from src.models import SpaceMap, SpaceshipDonkey, Comet
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer


def main():
    print("=" * 70)
    print("GALAXIAS API EXAMPLE - Programmatic Usage")
    print("=" * 70)
    print()
    
    # Step 1: Load configuration and initialize components
    print("Step 1: Loading configuration...")
    with open('data/spaceship_config.json', 'r') as f:
        config = json.load(f)
    
    space_map = SpaceMap('data/constellations.json')
    print(f"  ✅ Loaded {len(space_map.stars)} stars and {len(space_map.routes)} routes")
    
    # Step 2: Create spaceship donkey
    print("\nStep 2: Creating Burro Astronauta...")
    ship_config = config['spaceship_donkey']
    donkey = SpaceshipDonkey(
        name=ship_config['name'],
        health=ship_config['initial_health'],
        fuel=ship_config['initial_fuel'],
        food=ship_config['initial_food'],
        oxygen=ship_config['initial_oxygen']
    )
    print(f"  ✅ {donkey.name} ready with {donkey.health} health")
    
    # Step 3: Calculate route
    print("\nStep 3: Calculating route from Vega to Sirius...")
    calculator = RouteCalculator(space_map, config)
    
    vega = space_map.get_star('lyra_1')
    sirius = space_map.get_star('canis_1')
    
    path, cost = calculator.dijkstra(vega, sirius)
    
    if path:
        path_stats = calculator.calculate_path_stats(path)
        print(f"  ✅ Route found!")
        print(f"     Path: {' → '.join([s.name for s in path])}")
        print(f"     Distance: {path_stats['total_distance']} units")
        print(f"     Jumps: {path_stats['num_jumps']}")
        print(f"     Cost: {cost:.2f}")
    else:
        print("  ❌ No route found")
        return
    
    # Step 4: Check if donkey can make the journey
    print("\nStep 4: Checking resources...")
    can_travel = donkey.can_travel(path_stats['total_distance'], config)
    print(f"  {'✅' if can_travel else '❌'} Can travel: {can_travel}")
    
    if not can_travel:
        print("  ⚠️  Insufficient resources, refueling...")
        donkey.refuel()
    
    # Step 5: Simulate the journey
    print("\nStep 5: Simulating journey...")
    donkey.current_location = path[0]
    donkey.journey_history = [path[0]]
    
    print(f"  Starting at: {path[0].name}")
    
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
            print(f"  → Traveling to {next_star.name} "
                  f"(distance: {route.distance}, danger: {route.danger_level})...")
            
            donkey.consume_resources(route.distance, route.danger_level, config)
            donkey.current_location = next_star
            donkey.journey_history.append(next_star)
            
            if not donkey.is_alive():
                print(f"  ❌ Journey failed at {next_star.name}")
                break
    
    # Step 6: Report final status
    print("\nStep 6: Final status")
    status = donkey.get_status()
    print(f"  Location: {status['location']}")
    print(f"  Health: {status['health']:.1f}")
    print(f"  Fuel: {status['fuel']:.1f}")
    print(f"  Food: {status['food']:.1f}")
    print(f"  Oxygen: {status['oxygen']:.1f}")
    print(f"  Status: {'✅ Alive' if donkey.is_alive() else '❌ Dead'}")
    
    # Step 7: Add a comet and recalculate
    print("\nStep 7: Adding comet to block a route...")
    comet = Comet(name="Example Comet", blocked_routes=[('ursa_3', 'lyra_1')])
    space_map.add_comet(comet)
    print(f"  ✅ Added comet blocking Alioth ↔ Vega")
    
    # Recalculate route
    print("\nStep 8: Recalculating route with comet...")
    path2, cost2 = calculator.dijkstra(vega, sirius)
    
    path_stats_for_report = path_stats  # Use original stats if no new path
    
    if path2:
        path_stats2 = calculator.calculate_path_stats(path2)
        path_stats_for_report = path_stats2
        print(f"  ✅ New route found!")
        print(f"     Path: {' → '.join([s.name for s in path2])}")
        print(f"     Distance: {path_stats2['total_distance']} units")
        print(f"     Cost: {cost2:.2f}")
        print(f"     Difference: {path_stats2['total_distance'] - path_stats['total_distance']:.1f} units longer")
    else:
        print(f"  ❌ No alternate route available with comet blocking")
        path2 = None
    
    # Step 9: Generate visualizations
    print("\nStep 9: Generating visualizations...")
    visualizer = SpaceVisualizer(space_map)
    
    visualizer.plot_space_map(
        highlight_path=path2,
        donkey_location=donkey.current_location,
        save_path='assets/example_map.png',
        show=False
    )
    print("  ✅ Space map saved to: assets/example_map.png")
    
    visualizer.plot_resource_status(
        donkey,
        save_path='assets/example_resources.png',
        show=False
    )
    print("  ✅ Resources chart saved to: assets/example_resources.png")
    
    visualizer.plot_journey_report(
        donkey,
        path_stats_for_report,
        save_path='assets/example_report.png',
        show=False
    )
    print("  ✅ Journey report saved to: assets/example_report.png")
    
    print("\n" + "=" * 70)
    print("EXAMPLE COMPLETED SUCCESSFULLY")
    print("=" * 70)
    print("\nCheck the 'assets' directory for generated visualizations.")


if __name__ == "__main__":
    main()
