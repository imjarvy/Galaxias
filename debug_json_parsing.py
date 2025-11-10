#!/usr/bin/env python3
"""
Script para verificar el parseo de los archivos JSON del sistema Galaxias.
"""

import json
from src.models import SpaceMap

def debug_json_parsing():
    """Debuggea el parseo de los archivos JSON."""
    print("="*60)
    print("🫏 GALAXIAS - DEBUG DE PARSEO JSON 🌟")
    print("="*60)
    print()
    
    # 1. Verificar carga directa del JSON de constelaciones
    print("1. ARCHIVO CONSTELLATIONS.JSON:")
    print("-" * 40)
    with open('data/constellations.json', 'r') as f:
        raw_data = json.load(f)
    
    print(f"Constelaciones encontradas: {len(raw_data.get('constellations', []))}")
    print()
    
    for i, constellation in enumerate(raw_data.get('constellations', []), 1):
        name = constellation.get('name', 'Sin nombre')
        stars = constellation.get('starts', [])  # Nota: 'starts' no 'stars'
        print(f"  {i}. {name}")
        print(f"     Estrellas: {len(stars)}")
        
        for star in stars:
            star_id = star.get('id')
            label = star.get('label', 'Sin label')
            coords = star.get('coordenates', {})
            x = coords.get('x', 0)
            y = coords.get('y', 0)
            energy = star.get('amountOfEnergy', 0)
            time_to_eat = star.get('timeToEat', 0)
            radius = star.get('radius', 0)
            hypergiant = star.get('hypergiant', False)
            linked_to = star.get('linkedTo', [])
            
            print(f"       - {label} (ID: {star_id})")
            print(f"         Coordenadas: ({x}, {y})")
            print(f"         Energía: {energy}, Radio: {radius}, Tiempo: {time_to_eat}")
            print(f"         Hipergigante: {hypergiant}")
            print(f"         Conexiones: {len(linked_to)}")
        print()
    
    # 2. Información del burro
    print("2. DATOS DEL BURRO ASTRONAUTA:")
    print("-" * 40)
    print(f"Energía inicial: {raw_data.get('burroenergiaInicial', 'No definida')}")
    print(f"Estado de salud: {raw_data.get('estadoSalud', 'No definido')}")
    print(f"Pasto inicial: {raw_data.get('pasto', 'No definido')} kg")
    print(f"Edad inicial: {raw_data.get('startAge', 'No definida')} años")
    print(f"Edad de muerte: {raw_data.get('deathAge', 'No definida')} años")
    print(f"Número: {raw_data.get('number', 'No definido')}")
    print()
    
    # 3. Verificar carga del spaceship_config.json
    print("3. ARCHIVO SPACESHIP_CONFIG.JSON:")
    print("-" * 40)
    with open('data/spaceship_config.json', 'r') as f:
        config_data = json.load(f)
    
    print("Parámetros de consumo:")
    for key, value in config_data.get('consumption_rates', {}).items():
        print(f"  - {key}: {value}")
    
    print("\nParámetros científicos:")
    for key, value in config_data.get('scientific_parameters', {}).items():
        print(f"  - {key}: {value}")
    print()
    
    # 4. Verificar carga en el sistema (SpaceMap)
    print("4. PARSEO EN EL SISTEMA SPACEMAP:")
    print("-" * 40)
    space_map = SpaceMap('data/constellations.json')
    
    print(f"Total de estrellas cargadas: {len(space_map.stars)}")
    print(f"Total de rutas generadas: {len(space_map.routes)}")
    print()
    
    print("Estrellas en el sistema:")
    for star_id, star in space_map.stars.items():
        print(f"  - {star.label} (ID: {star_id})")
        print(f"    Coordenadas: ({star.x}, {star.y})")
        print(f"    Energía: {star.amount_of_energy}, Radio: {star.radius}")
        print(f"    Tiempo para comer: {star.time_to_eat}")
        print(f"    Hipergigante: {star.hypergiant}")
        print(f"    Conexiones definidas: {len(star.linked_to)}")
    print()
    
    print("Rutas generadas en el sistema:")
    for i, route in enumerate(space_map.routes[:10], 1):  # Solo primeras 10 para no saturar
        print(f"  {i}. {route.from_star.label} ↔ {route.to_star.label}")
        print(f"     Distancia: {route.distance:.2f}, Peligro: {route.danger_level}")
    
    if len(space_map.routes) > 10:
        print(f"  ... y {len(space_map.routes) - 10} rutas más.")
    print()
    
    # 5. Verificar datos del burro en el sistema
    print("5. BURRO ASTRONAUTA EN EL SISTEMA:")
    print("-" * 40)
    burro = space_map.create_burro_astronauta()
    print(f"Nombre: {burro.name}")
    print(f"Energía inicial: {burro.energia_inicial}%")
    print(f"Estado de salud: {burro.estado_salud}")
    print(f"Pasto inicial: {burro.pasto} kg")
    print(f"Edad: {burro.start_age} años")
    print(f"Edad de muerte: {burro.death_age} años")
    print(f"Energía actual: {burro.current_energy}%")
    print(f"Pasto actual: {burro.current_pasto} kg")
    print(f"¿Está vivo?: {burro.is_alive()}")
    print()
    
    print("="*60)
    print("✅ PARSEO COMPLETADO EXITOSAMENTE")
    print("="*60)

if __name__ == "__main__":
    debug_json_parsing()