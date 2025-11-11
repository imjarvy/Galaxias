"""
Main GUI Application for Galaxias space route simulation.
Refactored to implement SOLID principles.

Key improvements:
1. Single Responsibility Principle: Each class has one responsibility
2. Open/Closed Principle: Easy to extend without modifying existing code
3. Liskov Substitution Principle: Interfaces can be swapped
4. Interface Segregation Principle: Small, focused interfaces
5. Dependency Inversion Principle: Depends on abstractions, not concretions
"""

import tkinter as tk
from typing import List, Optional
from ..core import Star
from .gui_init import (
    initialize_services, initialize_models, initialize_components, initialize_controllers
)
from .gui_callbacks import setup_additional_callbacks
from .services.burro_journey_service import BurroJourneyService


class GalaxiasGUI:
    """
    Main GUI application for Galaxias space route simulation.
    
    This class acts as a coordinator (following Facade pattern) that:
    - Initializes all services and components
    - Sets up the main window layout
    - Coordinates communication between components
    
    Follows SOLID principles:
    - Single Responsibility: Only responsible for application setup and coordination
    - Open/Closed: New components can be added without modifying this class
    - Dependency Inversion: Depends on interfaces, not concrete implementations
    """
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self._setup_window()
        # Modular initialization
        (self.config_service, self.config, self.space_map, self.route_service,
         self.visualization_service, self.journey_service) = initialize_services()
        self.burro, self.hypergiant_system = initialize_models(self.space_map)
        (self.route_panel, self.burro_panel, self.reports_panel, self.visualization_panel) = initialize_components(self.space_map, self.burro)
        (self.route_controller, self.burro_controller, self.visualization_controller) = initialize_controllers(
            self.route_service, self.space_map, self.route_panel, self.visualization_panel,
            self.visualization_service, self.burro, self.burro_panel)
        self.route_controller.on_state_change = self._update_all_displays
        self.burro_controller.on_state_change = self._update_all_displays
        setup_additional_callbacks(
            self.route_panel, self.reports_panel,
            self.route_controller,
            self._start_journey, self._generate_report
        )
        self._setup_layout()
        self._initial_updates()
    
    def _setup_window(self):
        """Configure the main window."""
        self.root.title("Galaxias - Sistema de Rutas del Burro Astronauta")
        self.root.geometry("1400x900")
        self.root.configure(bg='#000033')
    
    
    def _setup_layout(self):
        """Setup the main UI layout."""
        # Main container
        main_frame = tk.Frame(self.root, bg='#000033')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg='#000066', relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0)
        
        # Title
        title = tk.Label(left_panel, text="🫏 Galaxias 🌟", 
                        font=('Arial', 20, 'bold'), 
                        bg='#000066', fg='white')
        title.pack(pady=10)
        
        # Create component widgets
        self.route_panel.create_widgets(left_panel).pack(fill=tk.BOTH, padx=10, pady=5)
        self.burro_panel.create_widgets(left_panel).pack(fill=tk.BOTH, padx=10, pady=5)
        self.reports_panel.create_widgets(left_panel).pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Right panel - Visualization
        right_panel = tk.Frame(main_frame, bg='#000033')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.visualization_panel.create_widgets(right_panel).pack(fill=tk.BOTH, expand=True)
    
    def _initial_updates(self):
        """Perform initial updates to all components."""
        self._update_all_displays()
        
        # Initial visualization
        self.visualization_controller.update_visualization()
    
    def _update_all_displays(self):
        """Update all component displays."""
        try:
            # Update burro status
            self.burro_controller.update_display()
            # Update visualization with current burro position AND current path
            current_path = self.route_controller.get_current_path()
            self.visualization_controller.update_visualization(path=current_path)
            # Force UI refresh
            self.root.update_idletasks()
        except Exception as e:
            print(f"Warning: Error updating displays: {e}")  # Debug info
    
    def _start_journey(self):
        """Start the journey along the calculated path."""
        current_path = self.route_controller.get_current_path()
        
        if not current_path or len(current_path) == 0:
            from tkinter import messagebox
            messagebox.showerror("Error", "Primero calcule una ruta")
            return
        
        # Journey simulation logic
        self._simulate_journey(current_path)
    
    def _simulate_journey(self, path: List[Star]):
        """Simulate the journey along the given path using unified burro logic."""
        from tkinter import messagebox
        
        if not path:
            messagebox.showerror("Error", "No hay ruta para simular")
            return
        
        # Resetear burro a valores del JSON antes del viaje
        self.journey_service.reset_burro_to_json_values(self.burro)
        initial_msg = (f"\n🔄 REINICIANDO A VALORES DEL JSON:"
                      f"\n✨ Energía inicial: {self.journey_service.initial_energy}%"
                      f"\n🌾 Pasto inicial: {self.journey_service.initial_grass} kg"
                      f"\n💚 Salud inicial: {self.journey_service.initial_health.upper()}"
                      f"\n⏰ Vida restante: {self.journey_service.initial_life_remaining:.1f} años")
        self.burro_controller.append_status_message(initial_msg)
        self._update_all_displays()
        self.root.update()
        
        # Simular el viaje completo con la lógica unificada
        start_msg = f"\n🚀 INICIANDO VIAJE - Ruta de {len(path)} estrellas"
        self.burro_controller.append_status_message(start_msg)
        self._update_all_displays()
        self.root.update()
        
        try:
            # Procesar viaje paso a paso
            journey_steps = self.journey_service.simulate_journey(path, self.burro)
            
            if not journey_steps:
                messagebox.showerror("Error", "No se pudo procesar el viaje")
                return
            
            # Mostrar cada paso del viaje
            for i, step in enumerate(journey_steps):
                self._display_journey_step(step, i)
                
                # Aplicar cambios al burro paso a paso
                self.burro.current_energy = step.energy_after_star
                self.burro.current_pasto = step.grass_after_star
                self.burro.estado_salud = step.health_after_star
                self.burro.current_age = (self.journey_service.start_age + 
                                         (self.journey_service.initial_life_remaining - step.life_remaining_after_star))
                self.burro.total_life_consumed = (self.journey_service.initial_life_remaining - 
                                                 step.life_remaining_after_star)
                self.burro.current_location = step.star
                if step.star not in self.burro.journey_history:
                    self.burro.journey_history.append(step.star)
                
                # Actualizar GUI
                self._update_all_displays()
                self.root.update()
                
                # Pausa para visualización
                import time
                time.sleep(0.8)  # Pausa más larga para ver los cambios
                
                # Verificar si murió
                if step.health_after_star == "muerto":
                    death_msg = f"\n💀 EL BURRO ASTRONAUTA HA MUERTO EN {step.star.label}"
                    self.burro_controller.append_status_message(death_msg)
                    self._update_all_displays()
                    messagebox.showerror("Viaje Fallido", 
                                        f"El Burro Astronauta murió en {step.star.label}\n"
                                        f"Visitó {len(journey_steps)} estrellas antes de morir")
                    return
            
            # Aplicar estado final al burro
            self.journey_service.apply_journey_to_burro(self.burro, journey_steps)
            
            # Generar resumen del viaje
            summary = self.journey_service.get_journey_summary(journey_steps)
            
            # Mostrar resumen final
            final_msg = (f"\n🎉 VIAJE COMPLETADO EXITOSAMENTE!"
                        f"\n📊 Estrellas visitadas: {summary['stars_visited']}"
                        f"\n⚡ Energía: {summary['initial_energy']}% → {summary['final_energy']:.1f}%"
                        f"\n🌾 Pasto: {summary['initial_grass']} kg → {summary['final_grass']:.1f} kg"
                        f"\n💚 Salud: {summary['initial_health'].upper()} → {summary['final_health'].upper()}"
                        f"\n⏰ Vida: {summary['initial_life']:.1f} → {summary['final_life']:.1f} años"
                        f"\n🍽️ Pasto consumido: {summary['total_grass_consumed']:.1f} kg"
                        f"\n�️ Vida consumida: {summary['total_life_consumed']:.1f} años")
            
            self.burro_controller.append_status_message(final_msg)
            self._update_all_displays()
            
            messagebox.showinfo("Viaje Completado", 
                               f"¡Viaje exitoso!\n"
                               f"Estrellas visitadas: {summary['stars_visited']}\n"
                               f"Energía final: {summary['final_energy']:.1f}%\n"
                               f"Pasto restante: {summary['final_grass']:.1f} kg\n"
                               f"Estado final: {summary['final_health'].upper()}")
        
        except Exception as e:
            error_msg = f"\n❌ ERROR DURANTE EL VIAJE: {str(e)}"
            self.burro_controller.append_status_message(error_msg)
            self._update_all_displays()
            messagebox.showerror("Error", f"Error durante la simulación: {str(e)}")
        
        # Mantener la visualización de la ruta recorrida
        # No limpiar el path para que las flechas sigan mostrándose
        # self.route_controller._clear_current_path()  # Comentado para mantener visualización
    
    def _display_journey_step(self, step, step_index: int):
        """Muestra los detalles de un paso del viaje."""
        # Mensaje de llegada
        if step_index == 0:
            arrival_msg = f"\n🎯 LLEGANDO A ESTRELLA INICIAL: {step.star.label}"
        else:
            travel_info = ""
            if hasattr(step, 'travel_distance_next') and step_index > 0:
                # Buscar info de viaje del paso anterior
                prev_step = None  # Se podría pasar como parámetro si es necesario
            arrival_msg = f"\n📍 LLEGANDO A: {step.star.label}"
        
        self.burro_controller.append_status_message(arrival_msg)
        
        # Estado al llegar
        status_msg = (f"\n📊 ESTADO AL LLEGAR:"
                     f"\n   ⚡ Energía: {step.energy_on_arrival:.1f}%"
                     f"\n   🌾 Pasto: {step.grass_on_arrival:.1f} kg"
                     f"\n   💚 Salud: {step.health_on_arrival.upper()}"
                     f"\n   ⏰ Vida restante: {step.life_remaining_on_arrival:.1f} años")
        self.burro_controller.append_status_message(status_msg)
        
        # Análisis de tiempo
        time_msg = (f"\n⏱️ ANÁLISIS DE TIEMPO EN ESTRELLA:"
                   f"\n   🏠 Tiempo total de estadía: {step.total_stay_time:.2f}"
                   f"\n   🍽️ Tiempo disponible para comer: {step.eating_time_available:.2f}"
                   f"\n   🔬 Tiempo para investigación: {step.research_time:.2f}")
        self.burro_controller.append_status_message(time_msg)
        
        # Decisión y acción de comer
        if step.should_eat:
            if step.can_eat:
                eat_msg = (f"\n🍽️ COMIENDO PASTO (Energía < 50%):"
                          f"\n   🌾 Puede comer: {step.kg_to_eat:.1f} kg"
                          f"\n   ✅ Comió: {step.kg_actually_eaten:.1f} kg"
                          f"\n   ⚡ Energía ganada: +{step.energy_gained_eating:.1f}%"
                          f"\n   💪 Bonus por salud: {step.health_bonus_percentage*100:.1f}%/kg")
            else:
                eat_msg = f"\n❌ NO PUEDE COMER - Sin pasto suficiente o sin tiempo"
        else:
            eat_msg = f"\n⚡ NO NECESITA COMER - Energía ≥ 50%"
        
        self.burro_controller.append_status_message(eat_msg)
        
        # Investigación
        research_msg = (f"\n🔬 INVESTIGACIÓN:"
                       f"\n   📉 Energía consumida: -{step.energy_consumed_research:.1f}%"
                       f"\n   🕰️ Efecto en vida: {step.life_effect_research:+.2f} años")
        self.burro_controller.append_status_message(research_msg)
        
        # Efectos de hipergigante
        if step.is_hypergiant:
            hyper_msg = (f"\n🌟 ESTRELLA HIPERGIGANTE:"
                        f"\n   ⚡ Bonus energía (+50%): +{step.hypergiant_energy_bonus:.1f}%"
                        f"\n   🌾 Pasto duplicado: +{step.hypergiant_grass_bonus:.1f} kg")
            self.burro_controller.append_status_message(hyper_msg)
        
        # Estado final
        final_msg = (f"\n✅ ESTADO DESPUÉS DE {step.star.label}:"
                    f"\n   ⚡ Energía final: {step.energy_after_star:.1f}%"
                    f"\n   🌾 Pasto final: {step.grass_after_star:.1f} kg"
                    f"\n   💚 Salud final: {step.health_after_star.upper()}"
                    f"\n   ⏰ Vida restante: {step.life_remaining_after_star:.1f} años"
                    f"\n   {'─'*50}")
        self.burro_controller.append_status_message(final_msg)
    
    def _generate_report(self):
        """Generate visual journey report."""
        path_stats = self.route_controller.get_current_path_stats()
        self.visualization_controller.generate_report(path_stats)


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = GalaxiasGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()