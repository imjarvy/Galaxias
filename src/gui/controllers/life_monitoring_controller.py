"""
Life Monitoring Controller.
Implements Single Responsibility Principle - handles only life monitoring operations.
"""
from tkinter import messagebox
from typing import Optional, List
from ...core import BurroAstronauta, Star
from ..components.life_monitoring_panel import LifeMonitoringPanel


class LifeMonitoringController:
    """Controller for life monitoring operations."""
    
    def __init__(self, burro: BurroAstronauta, life_panel: LifeMonitoringPanel):
        self.burro = burro
        self.life_panel = life_panel
        
        # Setup callbacks
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup callbacks for the life monitoring panel."""
        self.life_panel.on_analyze_travel = self.analyze_next_travel
        self.life_panel.on_demo_countdown = self.demo_countdown
    
    def analyze_next_travel(self, current_path: Optional[List[Star]] = None):
        """Analyze the cost of life for the next planned travel."""
        try:
            if not current_path or len(current_path) < 2:
                messagebox.showinfo("Sin Ruta", 
                                  "Primero calcule una ruta para analizar su costo de vida.")
                return
            
            # Calculate total distance
            total_distance = 0
            route_description = f"{current_path[0].label}"
            
            for i in range(len(current_path) - 1):
                # Here you would calculate actual distance between stars
                # For now, using a placeholder
                total_distance += 10  # Placeholder distance
                route_description += f" → {current_path[i + 1].label}"
            
            # Show travel preview using the travel analyzer
            travel_analyzer = self.life_panel.get_travel_analyzer()
            if travel_analyzer:
                travel_analyzer.show_travel_preview(total_distance, route_description)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar viaje: {str(e)}")
    
    def demo_countdown(self):
        """Demonstrate the countdown with a simulated trip."""
        try:
            # Simulate a short trip to see the countdown effect
            demo_distance = 50  # 33 years of life with warp_factor 1.5
            
            response = messagebox.askyesno("Demo Countdown", 
                f"🎮 DEMO: Simular viaje con countdown en tiempo real\n\n"
                f"📏 Distancia: {demo_distance} unidades\n"
                f"⏰ Costo de vida: ~{demo_distance/1.5:.1f} años\n"
                f"🕐 Duración del demo: ~{demo_distance/1.5:.0f} segundos\n\n"
                f"El contador decrementará visualmente y emitirá sonido si llega a 0.\n\n"
                f"¿Iniciar demostración?")
            
            if response:
                # Activate accelerated countdown in the widget
                life_widget = self.life_panel.get_life_status_widget()
                if life_widget:
                    life_widget.simulate_travel_countdown(demo_distance)
                else:
                    messagebox.showwarning("Widget no disponible", 
                                         "El widget de vida no está inicializado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en demo countdown: {str(e)}")
    
    def update_display(self):
        """Update the life monitoring display."""
        self.life_panel.update_display()