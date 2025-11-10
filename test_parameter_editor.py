#!/usr/bin/env python3
"""
Script de prueba para verificar el editor de parámetros de investigación.

Este script crea una ventana con el editor de parámetros para probar su funcionalidad.
"""

import sys
import os
sys.path.append(os.path.abspath('.'))

import tkinter as tk
from src.models import SpaceMap
from src.parameter_editor_simple import ResearchParameterEditor, ResearchParameters

def test_parameter_editor():
    """Prueba la funcionalidad del editor de parámetros."""
    print("🧪 PRUEBA: Editor de Parámetros de Investigación")
    print("=" * 60)
    
    # Crear ventana raíz
    root = tk.Tk()
    root.title("Prueba - Editor de Parámetros")
    root.geometry("300x200")
    root.configure(bg='#000033')
    
    # Cargar mapa espacial
    space_map = SpaceMap('data/constellations.json')
    
    # Crear parámetros de investigación por defecto
    research_params = ResearchParameters()
    
    # Etiqueta de instrucciones
    instructions = tk.Label(root, 
                           text="Haga clic en el botón para\nabrir el editor de parámetros:",
                           font=('Arial', 12),
                           bg='#000033', fg='white')
    instructions.pack(pady=20)
    
    def open_editor():
        """Abre el editor de parámetros."""
        nonlocal research_params
        try:
            print("\n🔧 Abriendo editor de parámetros...")
            
            # Crear editor
            editor = ResearchParameterEditor(root, space_map, research_params)
            
            # Esperar a que se cierre
            root.wait_window(editor.window)
            
            # Obtener resultado
            result = editor.get_parameters()
            
            if result is not None:
                print("✅ Parámetros configurados exitosamente:")
                print(f"   • Consumo energía: {result.energy_consumption_rate:.1f}% por tiempo")
                print(f"   • Tiempo investigación: {result.time_percentage*100:.1f}%")
                print(f"   • Bonus tiempo vida: {result.life_time_bonus:+.1f} años")
                print(f"   • Bonus energía: {result.energy_bonus_per_star:+.1f}% por estrella")
                print(f"   • Configuraciones específicas: {len(result.custom_star_settings)} estrellas")
                
                if result.custom_star_settings:
                    print("   🌟 Estrellas configuradas:")
                    for star_id, config in result.custom_star_settings.items():
                        star = space_map.get_star(star_id)
                        star_name = star.label if star else f"ID:{star_id}"
                        print(f"      - {star_name}: energía={config.get('energy_rate', 2.0):.1f}%, "
                              f"tiempo={config.get('time_bonus', 0.0):+.1f}a, "
                              f"energía_bonus={config.get('energy_bonus', 0.0):+.1f}%")
                
                # Actualizar parámetros globales
                research_params = result
                
                # Actualizar etiqueta de estado
                status_label.config(text="✅ Parámetros actualizados")
                
            else:
                print("❌ Configuración cancelada")
                status_label.config(text="❌ Configuración cancelada")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            status_label.config(text=f"❌ Error: {e}")
    
    # Botón para abrir editor
    open_button = tk.Button(root, 
                           text="⚙️ Configurar Parámetros",
                           command=open_editor,
                           bg='#4444FF', fg='white',
                           font=('Arial', 12, 'bold'),
                           relief=tk.RAISED, borderwidth=2)
    open_button.pack(pady=10)
    
    # Etiqueta de estado
    status_label = tk.Label(root,
                           text="Esperando configuración...",
                           font=('Arial', 10),
                           bg='#000033', fg='#CCCCCC')
    status_label.pack(pady=10)
    
    # Botón para cerrar
    close_button = tk.Button(root,
                           text="Cerrar Prueba",
                           command=root.destroy,
                           bg='#CC4444', fg='white',
                           font=('Arial', 10))
    close_button.pack(pady=5)
    
    print("🚀 Abriendo ventana de prueba...")
    print("💡 Use el botón para probar el editor de parámetros.")
    
    # Ejecutar loop principal
    root.mainloop()
    
    print("\n🏁 Prueba completada.")

if __name__ == "__main__":
    test_parameter_editor()