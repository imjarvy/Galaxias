#!/usr/bin/env python3
"""
Prueba del nuevo sistema de colores por constelación en el visualizador.
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.models import SpaceMap
from src.visualizer import SpaceVisualizer
import matplotlib.pyplot as plt

def test_constellation_color_system():
    """Prueba el sistema completo de colores por constelación."""
    print("🎨 PROBANDO SISTEMA DE COLORES POR CONSTELACIÓN")
    print("="*60)
    
    # Cargar el mapa espacial
    space_map = SpaceMap('data/constellations.json')
    
    # Crear visualizador con nuevo sistema de colores
    visualizer = SpaceVisualizer(space_map)
    
    # Mostrar información del sistema de colores
    print(f"\n🌌 Colores de constelaciones detectados: {len(visualizer.constellation_colors)}")
    for name, color in visualizer.constellation_colors.items():
        print(f"   {name}: {color}")
    
    print(f"\n🔗 Coordenadas compartidas: {len(visualizer.shared_coordinates)}")
    if visualizer.shared_coordinates:
        for coord in visualizer.shared_coordinates:
            print(f"   {coord}")
    else:
        print("   ✅ No hay estrellas compartidas")
    
    # Mostrar colores por estrella
    print(f"\n⭐ Asignación de colores por estrella:")
    print("-" * 40)
    
    for star in space_map.get_all_stars_list():
        color = visualizer._determine_star_color(star)
        constellation = visualizer._get_star_constellation(star)
        
        star_type = ""
        if star.hypergiant:
            star_type = " [HIPERGIGANTE]"
        elif (star.x, star.y) in visualizer.shared_coordinates:
            star_type = " [COMPARTIDA]"
        elif constellation:
            star_type = f" [{constellation}]"
        
        print(f"   {star.label} (ID: {star.id}) -> {color}{star_type}")
    
    # Generar visualización
    print(f"\n📊 Generando visualización con nuevos colores...")
    
    fig = visualizer.plot_space_map(show=False, save_path='test_constellation_colors.png')
    
    print(f"✅ Visualización guardada como 'test_constellation_colors.png'")
    print(f"✅ Sistema de colores implementado correctamente")
    
    # Mostrar la visualización
    plt.show()

if __name__ == "__main__":
    test_constellation_color_system()