#!/usr/bin/env python3
"""
Generador de colores automático para constelaciones usando función hash.
Implementa paleta de colores distintivos y manejo de estrellas compartidas.
"""
import hashlib
import json
from typing import Dict, List, Tuple, Set

def generate_constellation_color(name: str) -> str:
    """
    Genera un color único para una constelación basado en hash de su nombre.
    
    Args:
        name: Nombre de la constelación
        
    Returns:
        str: Color en formato hexadecimal (#RRGGBB)
    """
    # Normalizar nombre (minúsculas, sin espacios extra)
    normalized_name = name.lower().strip()
    
    # Crear hash del nombre
    hash_object = hashlib.md5(normalized_name.encode())
    hex_dig = hash_object.hexdigest()
    
    # Usar los primeros 6 caracteres como color, pero evitar colores reservados
    base_color = "#" + hex_dig[:6]
    
    # Asegurar que el color no sea muy oscuro ni muy parecido a los reservados
    r = int(hex_dig[0:2], 16)
    g = int(hex_dig[2:4], 16) 
    b = int(hex_dig[4:6], 16)
    
    # Evitar colores muy oscuros (aumentar brillo mínimo)
    if r < 80: r += 80
    if g < 80: g += 80
    if b < 80: b += 80
    
    # Evitar colores muy parecidos a los reservados
    # Hipergigante: #FF00FF (magenta)
    # Compartida: #d62728 (rojo intenso)
    # Normal: #FFFF44 (amarillo)
    
    # Si es muy parecido al magenta hipergigante, ajustar
    if r > 200 and b > 200 and g < 100:
        g += 100  # Agregar verde
    
    # Si es muy parecido al rojo compartido, ajustar
    if r > 180 and g < 80 and b < 80:
        b += 100  # Agregar azul
    
    # Si es muy parecido al amarillo normal, ajustar
    if r > 200 and g > 200 and b < 100:
        r -= 50  # Reducir rojo
    
    # Limitar valores a rango válido
    r = min(255, max(0, r))
    g = min(255, max(0, g))
    b = min(255, max(0, b))
    
    return f"#{r:02x}{g:02x}{b:02x}"

def get_constellation_colors_mapping() -> Dict[str, str]:
    """
    Genera mapa de colores para todas las constelaciones en el JSON.
    
    Returns:
        Dict[str, str]: Mapeo de nombre_constelación -> color_hex
    """
    with open('data/constellations.json', 'r') as f:
        data = json.load(f)
    
    color_mapping = {}
    
    for constellation in data.get('constellations', []):
        name = constellation['name']
        color = generate_constellation_color(name)
        color_mapping[name] = color
    
    return color_mapping

def find_shared_stars_by_coordinates() -> Set[Tuple[float, float]]:
    """
    Identifica coordenadas que tienen múltiples estrellas (estrellas compartidas).
    
    Returns:
        Set[Tuple[float, float]]: Conjunto de coordenadas con estrellas compartidas
    """
    with open('data/constellations.json', 'r') as f:
        data = json.load(f)
    
    coordinate_counts = {}
    
    # Contar cuántas estrellas hay en cada coordenada
    for constellation in data.get('constellations', []):
        for star in constellation.get('starts', []):
            x = star['coordenates']['x']
            y = star['coordenates']['y']
            coord = (x, y)
            
            coordinate_counts[coord] = coordinate_counts.get(coord, 0) + 1
    
    # Retornar coordenadas con más de una estrella
    return {coord for coord, count in coordinate_counts.items() if count > 1}

def determine_star_color(star_data: Dict, constellation_name: str, 
                        constellation_colors: Dict[str, str],
                        shared_coordinates: Set[Tuple[float, float]]) -> str:
    """
    Determina el color de una estrella según las reglas de prioridad:
    1. Hipergigante: #FF00FF (máxima prioridad)
    2. Compartida: #d62728 (segunda prioridad)
    3. Constelación: color generado automáticamente (tercera prioridad)
    4. Default: #FFFF44 (última prioridad)
    
    Args:
        star_data: Datos de la estrella del JSON
        constellation_name: Nombre de la constelación
        constellation_colors: Mapeo de colores de constelaciones
        shared_coordinates: Coordenadas con estrellas compartidas
        
    Returns:
        str: Color en formato hexadecimal
    """
    # Prioridad 1: Hipergigante
    if star_data.get('hypergiant', False):
        return '#FF00FF'
    
    # Prioridad 2: Estrella compartida (por coordenadas)
    x = star_data['coordenates']['x']
    y = star_data['coordenates']['y']
    if (x, y) in shared_coordinates:
        return '#d62728'
    
    # Prioridad 3: Color de constelación
    if constellation_name in constellation_colors:
        return constellation_colors[constellation_name]
    
    # Prioridad 4: Default (normal)
    return '#FFFF44'

def test_color_system():
    """Prueba el sistema de colores completo."""
    print("🎨 SISTEMA DE COLORES POR CONSTELACIÓN")
    print("="*50)
    
    # Generar colores de constelaciones
    constellation_colors = get_constellation_colors_mapping()
    print("\n🌌 Colores de Constelaciones:")
    for name, color in constellation_colors.items():
        print(f"   {name}: {color}")
    
    # Identificar estrellas compartidas
    shared_coords = find_shared_stars_by_coordinates()
    print(f"\n🔗 Coordenadas compartidas: {len(shared_coords)}")
    if shared_coords:
        for coord in shared_coords:
            print(f"   {coord}")
    else:
        print("   ✅ No hay estrellas compartidas actualmente")
    
    # Mostrar colores especiales
    print(f"\n🎯 Colores Especiales:")
    print(f"   Hipergigante: #FF00FF")
    print(f"   Compartida: #d62728") 
    print(f"   Default: #FFFF44")
    
    # Probar colores para todas las estrellas
    print(f"\n⭐ Asignación de Colores por Estrella:")
    print("-" * 50)
    
    with open('data/constellations.json', 'r') as f:
        data = json.load(f)
    
    for constellation in data.get('constellations', []):
        constellation_name = constellation['name']
        print(f"\n📍 {constellation_name} ({constellation_colors[constellation_name]}):")
        
        for star in constellation.get('starts', []):
            color = determine_star_color(star, constellation_name, 
                                       constellation_colors, shared_coords)
            
            star_type = ""
            if star.get('hypergiant', False):
                star_type = " [HIPERGIGANTE]"
            elif (star['coordenates']['x'], star['coordenates']['y']) in shared_coords:
                star_type = " [COMPARTIDA]"
            
            print(f"   ⭐ {star['label']} (ID: {star['id']}) -> {color}{star_type}")

if __name__ == "__main__":
    test_color_system()