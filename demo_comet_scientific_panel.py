#!/usr/bin/env python3
"""
Demo de la nueva gestión de cometas integrada al panel científico.
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import SpaceMap
from src.gui import GalaxiasGUI
import tkinter as tk


def main():
    """Función principal para demostrar la nueva gestión de cometas."""
    print("🌌 Demo: Nueva Gestión de Cometas en Panel Científico")
    print("=" * 60)
    
    # Crear ventana principal
    root = tk.Tk()
    
    try:
        # Crear aplicación GUI
        app = GalaxiasGUI(root)
        
        # Mensaje informativo
        print("\n✅ GUI iniciada exitosamente")
        print("\nPara probar la nueva gestión de cometas:")
        print("1. Haz clic en '⚙️ Configurar Parámetros'")
        print("2. Ve a la pestaña '🌌 Cometas'")
        print("3. Agrega/remueve cometas usando la nueva interfaz")
        print("\nCaracterísticas de la nueva interfaz:")
        print("• Combos desplegables para seleccionar estrellas")
        print("• Lista visual de cometas activos")
        print("• Información detallada sobre el funcionamiento")
        print("• Validación mejorada de entrada")
        print("• Actualización automática de la visualización")
        
        # Iniciar loop de la aplicación
        root.mainloop()
        
    except Exception as e:
        print(f"\n❌ Error al inicializar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n🎉 Demo completado exitosamente")
    return 0


if __name__ == "__main__":
    exit(main())