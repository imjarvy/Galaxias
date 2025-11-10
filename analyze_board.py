#!/usr/bin/env python3
"""
Script para analizar los parámetros del tablero de renderizado del sistema Galaxias.
"""

import matplotlib.pyplot as plt
from src.models import SpaceMap
from src.visualizer import SpaceVisualizer
import numpy as np

def analyze_board_parameters():
    """Analiza los parámetros del tablero donde se renderizan las estrellas."""
    print("="*70)
    print("🖥️  GALAXIAS - ANÁLISIS DEL TABLERO DE RENDERIZADO 📏")
    print("="*70)
    print()
    
    # 1. Cargar el sistema y crear visualizador
    space_map = SpaceMap('data/constellations.json')
    visualizer = SpaceVisualizer(space_map)
    
    # 2. Obtener coordenadas de todas las estrellas
    stars = space_map.get_all_stars_list()
    x_coords = [star.x for star in stars]
    y_coords = [star.y for star in stars]
    
    print("📍 COORDENADAS DE LAS ESTRELLAS:")
    print("-" * 50)
    for star in stars:
        print(f"  {star.label} (ID: {star.id}): ({star.x}, {star.y})")
    print()
    
    # 3. Calcular rangos de coordenadas
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    range_x = max_x - min_x
    range_y = max_y - min_y
    
    print("📐 RANGOS DE COORDENADAS:")
    print("-" * 50)
    print(f"  Coordenada X: {min_x} a {max_x} (rango: {range_x})")
    print(f"  Coordenada Y: {min_y} a {max_y} (rango: {range_y})")
    print(f"  Área ocupada: {range_x} x {range_y} = {range_x * range_y} unidades²")
    print()
    
    # 4. Crear figura para analizar parámetros de matplotlib
    print("🎨 PARÁMETROS DEL TABLERO MATPLOTLIB:")
    print("-" * 50)
    
    # Crear la figura como lo hace el visualizador
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plotear las estrellas para que matplotlib ajuste automáticamente
    for star in stars:
        color = '#FF00FF' if star.hypergiant else '#FFFF44'
        size = max(100, star.radius * 300)
        ax.scatter(star.x, star.y, s=size, c=color, 
                  edgecolors='white', linewidth=1, zorder=5)
        ax.annotate(f"{star.label}\nE:{star.amount_of_energy}", 
                   (star.x, star.y), 
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8, color='white',
                   bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor='black', alpha=0.7))
    
    # Obtener límites automáticos de matplotlib
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    
    # Configurar como lo hace el visualizador
    ax.set_facecolor('black')
    fig.patch.set_facecolor('#000033')
    ax.set_title('Galaxias - Mapa de Constelaciones', 
                color='white', fontsize=16, fontweight='bold')
    ax.set_xlabel('Coordenada X', color='white')
    ax.set_ylabel('Coordenada Y', color='white')
    ax.tick_params(colors='white')
    ax.grid(True, alpha=0.2, color='white')
    
    # Obtener dimensiones finales
    final_xlim = ax.get_xlim()
    final_ylim = ax.get_ylim()
    
    print(f"  📊 Tamaño de figura (matplotlib): 12 x 10 pulgadas")
    print(f"  📊 DPI por defecto: {fig.dpi}")
    print(f"  📊 Tamaño en píxeles: {12 * fig.dpi} x {10 * fig.dpi} px")
    print()
    print(f"  📏 Límites X automáticos: {final_xlim[0]:.2f} a {final_xlim[1]:.2f}")
    print(f"  📏 Límites Y automáticos: {final_ylim[0]:.2f} a {final_ylim[1]:.2f}")
    print(f"  📏 Ancho del tablero: {final_xlim[1] - final_xlim[0]:.2f} unidades")
    print(f"  📏 Alto del tablero: {final_ylim[1] - final_ylim[0]:.2f} unidades")
    print(f"  📏 Área total del tablero: {(final_xlim[1] - final_xlim[0]) * (final_ylim[1] - final_ylim[0]):.2f} unidades²")
    print()
    
    # 5. Verificar requisitos mínimos
    board_width = final_xlim[1] - final_xlim[0]
    board_height = final_ylim[1] - final_ylim[0]
    
    print("✅ VERIFICACIÓN DE REQUISITOS:")
    print("-" * 50)
    print(f"  Ancho mínimo requerido: 200 unidades")
    print(f"  Alto mínimo requerido: 200 unidades")
    print(f"  Ancho actual: {board_width:.2f} unidades {'✅' if board_width >= 200 else '❌'}")
    print(f"  Alto actual: {board_height:.2f} unidades {'✅' if board_height >= 200 else '❌'}")
    print()
    
    # 6. Analizar escalado
    print("⚖️  ANÁLISIS DE ESCALADO:")
    print("-" * 50)
    print("  🔍 Escalado de coordenadas:")
    print(f"     - Coordenadas originales se mantienen 1:1")
    print(f"     - No hay transformación de escala aplicada")
    print(f"     - Matplotlib ajusta automáticamente los límites")
    print()
    print("  🔍 Escalado de tamaños de estrellas:")
    print("     - Fórmula: tamaño = max(100, radio * 300)")
    print("     - Tamaño mínimo: 100 píxeles")
    print("     - Factor de escalado: 300x el radio")
    print()
    
    for star in stars:
        calculated_size = max(100, star.radius * 300)
        print(f"     - {star.label}: radio {star.radius} → tamaño {calculated_size} px")
    print()
    
    # 7. Información de archivos responsables
    print("📁 ARCHIVOS RESPONSABLES:")
    print("-" * 50)
    print("  1. src/visualizer.py:")
    print("     - Función plot_space_map() línea ~36")
    print("     - Tamaño de figura: figsize=(12, 10)")
    print("     - Escalado de estrellas: max(100, star.radius * 300)")
    print("     - Configuración de colores y grid")
    print()
    print("  2. src/gui.py:")
    print("     - Función update_visualization() línea ~481")
    print("     - Integración con tkinter via FigureCanvasTkAgg")
    print("     - Ventana principal: 1400x900 píxeles")
    print()
    print("  3. data/constellations.json:")
    print("     - Define coordenadas originales de las estrellas")
    print("     - Define radios para escalado de tamaños")
    print()
    
    # 8. Guardar imagen de ejemplo
    plt.tight_layout()
    plt.savefig('assets/tablero_analysis.png', facecolor=fig.get_facecolor(), dpi=150)
    print("  📸 Imagen del tablero guardada en: assets/tablero_analysis.png")
    plt.close(fig)
    
    print()
    print("="*70)
    print("✅ ANÁLISIS COMPLETADO")
    print("="*70)

if __name__ == "__main__":
    analyze_board_parameters()