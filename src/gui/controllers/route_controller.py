"""
Route Controller.
Implements Single Responsibility Principle - handles only route-related logic.
"""
from typing import List, Optional, Dict, Any
from tkinter import messagebox
from ...core import SpaceMap, Star, ResearchImpactValidator
from ...core.research_impact_validator import ResearchImpactValidatorGUI
from ...parameter_editor_simple.editor import ResearchParameterEditor
from ...parameter_editor_simple.models import ResearchParameters
from ..interfaces.route_service_interface import IRouteService
from ..interfaces.visualization_service_interface import IVisualizationService
from ..components.route_planning_panel import RoutePlanningPanel
from ..components.visualization_panel import VisualizationPanel


class RouteController:
    """Controller for route planning operations."""
    
    def __init__(self, route_service: IRouteService, space_map: SpaceMap,
                 route_panel: RoutePlanningPanel, visualization_panel: VisualizationPanel,
                 visualization_service: IVisualizationService):
        self.route_service = route_service
        self.space_map = space_map
        self.route_panel = route_panel
        self.visualization_panel = visualization_panel
        self.visualization_service = visualization_service
        
        # State
        self.current_path: Optional[List[Star]] = None
        self.current_path_stats: Optional[Dict[str, Any]] = None
        
        # Callback for state changes
        self.on_state_change: Optional[callable] = None
        
        # Research parameters - initialize with defaults from module
        try:
            self.research_parameters = ResearchParameters()
        except:
            # Fallback if module not available
            class TempResearchParameters:
                def __init__(self):
                    self.time_percentage = 0.3  # 30% investigating, 70% eating
                    self.energy_consumption_rate = 2.0  # 2% per time unit
                    self.custom_star_settings = {}  # Empty for now
                    self.life_time_bonus = 0.0  # Default bonus
                    self.energy_bonus_per_star = 0.0  # Default bonus
            
            self.research_parameters = TempResearchParameters()
        
        # Research validator
        self.research_impact_validator = ResearchImpactValidator(space_map)
        self.comet_impact_manager = None
        
        # Setup callbacks
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup callbacks for the route panel."""
        self.route_panel.on_calculate_route = self.calculate_optimal_route
        self.route_panel.on_max_visit_route = self.calculate_max_visit_route
        self.route_panel.on_min_cost_route = self.calculate_min_cost_route
        self.route_panel.on_edit_parameters = self.edit_research_parameters
        self.route_panel.on_validate_impacts = self.validate_research_impacts
    
    def calculate_optimal_route(self, start_text: str, end_text: str):
        """Calculate optimal route between selected stars."""
        start_id = self.route_service.extract_star_id_from_text(start_text)
        end_id = self.route_service.extract_star_id_from_text(end_text)
        
        if not start_id or not end_id:
            messagebox.showerror("Error", "Seleccione estrellas de origen y destino")
            return
        
        start_star = self.space_map.get_star(start_id)
        end_star = self.space_map.get_star(end_id)
        
        if not start_star or not end_star:
            messagebox.showerror("Error", "Estrellas no encontradas")
            return
        
        # Calculate path
        path, stats = self.route_service.calculate_optimal_route(start_star, end_star)
        
        if not path:
            error_msg = stats.get('error', 'Error desconocido') if stats else 'Error desconocido'
            messagebox.showwarning("Sin Ruta", 
                                  f"No hay ruta disponible entre estas estrellas.\n{error_msg}")
            self._clear_current_path()
            return
        
        # Update current path
        self.current_path = path
        self.current_path_stats = stats
        
        # Register for comet impact analysis
        self._register_active_journey(path, "optimal")
        
        # Update displays
        self._update_info_display(start_star, end_star, stats)
        self._update_route_visualization(path)
        self.route_panel.set_travel_enabled(True)
        
        # Notify state change for GUI updates
        if self.on_state_change:
            self.on_state_change()
        
        messagebox.showinfo("Ruta Calculada", 
                           f"Ruta encontrada con {stats.get('num_jumps', 0)} saltos")

    
    def calculate_max_visit_route(self, start_text: str):
        """Calculate route that maximizes star visits."""
        start_id = self.route_service.extract_star_id_from_text(start_text)
        
        if not start_id:
            messagebox.showerror("Error", "Selecciona una estrella de inicio")
            return
        
        start_star = self.space_map.get_star(start_id)
        if not start_star:
            messagebox.showerror("Error", "Estrella de inicio no encontrada")
            return
        
        path, stats = self.route_service.calculate_max_visit_route(start_star)
        
        if not path:
            error_msg = stats.get('error', 'No se pudo encontrar ruta válida') if stats else 'Error desconocido'
            messagebox.showwarning("Sin Resultado", error_msg)
            return
        
        # Update current path
        self.current_path = path
        self.current_path_stats = self.route_service.calculate_path_stats(path)
        
        # Update info display
        self._update_max_visit_info(stats)
        self._update_route_visualization(path)
        self.route_panel.set_travel_enabled(True)
        
        # Notify state change for GUI updates
        if self.on_state_change:
            self.on_state_change()
        
        json_values = stats.get('json_values_used', {})
        messagebox.showinfo("Ruta de Máximo Alcance (JSON)", 
                           f"Ruta encontrada usando valores del JSON:\n"
                           f"• {stats.get('stars_visited', 0)} estrellas visitadas\n"
                           f"• {stats.get('life_time_consumed', 0):.1f} años de vida\n"
                           f"• Energía inicial: {json_values.get('energia_inicial', 'N/A')}%\n"
                           f"• Edad inicial: {json_values.get('edad_inicial', 'N/A')} años")
    
    def calculate_min_cost_route(self, start_text: str):
        """Calculate minimum cost route."""
        start_id = self.route_service.extract_star_id_from_text(start_text)
        
        if not start_id:
            messagebox.showwarning("Advertencia", "Por favor selecciona una estrella de origen")
            return
        
        start_star = self.space_map.get_star(start_id)
        if not start_star:
            messagebox.showerror("Error", f"Estrella {start_id} no encontrada")
            return
        
        # Show rules confirmation
        if not self._confirm_min_cost_rules():
            return
        
        path, stats = self.route_service.calculate_min_cost_route(start_star, self.research_parameters)
        
        if not path:
            error_msg = stats.get('error', 'No se pudo calcular la ruta') if stats else 'Error desconocido'
            messagebox.showerror("Error", error_msg)
            return
        
        # Update current path
        self.current_path = path
        self.current_path_stats = stats
        
        # Update info display
        self._update_min_cost_info(stats)
        self._update_route_visualization(path)
        self.route_panel.set_travel_enabled(True)
        
        # Notify state change for GUI updates
        if self.on_state_change:
            self.on_state_change()
        
        messagebox.showinfo("Éxito", 
            f"Ruta de menor gasto calculada!\n"
            f"Estrellas visitadas: {stats.get('stars_visited', 0)}\n"
            f"Pasto consumido: {stats.get('total_grass_consumed', 0):.2f} kg\n"
            f"Energía final: {stats.get('final_energy', 0):.2f}%")
    
    def edit_research_parameters(self):
        """Open research parameters editor."""
        try:
            # Create parameter editor window
            import tkinter as tk
            
            # Get the root window for the editor
            root = self.route_panel.frame.winfo_toplevel()
            
            # Create parameter editor
            editor = ResearchParameterEditor(
                root, 
                self.space_map, 
                self.research_parameters,
                update_visualization_callback=self._update_visualization_callback
            )
            
            # Wait for the editor window to close
            root.wait_window(editor.window)
            
            # Get the result after window closes
            result = editor.get_parameters()
            
            if result:
                self.research_parameters = result
                self._update_config_button_status()
                messagebox.showinfo("Éxito", "Parámetros de investigación actualizados correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir editor de parámetros: {str(e)}")
    
    def validate_research_impacts(self):
        """Open research impact validator."""
        try:
            # Get the root window for the validator
            root = self.route_panel.frame.winfo_toplevel()
            
            # Create validator GUI - it opens automatically in __init__
            validator_gui = ResearchImpactValidatorGUI(root, self.space_map)
            
            # Note: No need to call show() as the window is created and shown in __init__
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir validador de impactos: {str(e)}")
    
    def get_current_path(self) -> Optional[List[Star]]:
        """Get the current calculated path."""
        return self.current_path
    
    def get_current_path_stats(self) -> Optional[Dict[str, Any]]:
        """Get the current path statistics."""
        return self.current_path_stats
    
    def _clear_current_path(self):
        """Clear the current path."""
        self.current_path = None
        self.current_path_stats = None
        self.route_panel.set_travel_enabled(False)
    
    def _register_active_journey(self, path: List[Star], journey_type: str):
        """Register an active journey for comet impact analysis."""
        if self.comet_impact_manager and path and len(path) > 1:
            self.comet_impact_manager.register_active_journey(path, 0, journey_type)
    
    def _update_info_display(self, start_star: Star, end_star: Star, stats: Dict[str, Any]):
        """Update the information display for optimal route."""
        info = f"""
RUTA CALCULADA
{'='*60}
Origen: {start_star.label}
Destino: {end_star.label}
Costo Total: {stats.get('cost', 0):.2f}

Estadísticas:
- Distancia Total: {stats.get('total_distance', 0)} unidades
- Saltos: {stats.get('num_jumps', 0)}
- Peligro Total: {stats.get('total_danger', 0)}

Recursos Necesarios:
- Energía para Viajar: {stats.get('total_energy_needed', 0):.2f}
- Pasto Necesario: {stats.get('total_grass_needed', 0):.2f} kg
- Energía Ganada: {stats.get('total_energy_gained', 0):.2f}
- Balance Neto: {stats.get('net_energy', 0):.2f}

Ruta: {' → '.join(stats.get('path_stars', []))}
        """
        self.visualization_panel.update_info_text(info)
    
    def _update_eating_route_info(self, stats: Dict[str, Any]):
        """Update info display for eating route."""
        info = f"""
RUTA OPTIMIZADA PARA COMER ESTRELLAS
{'='*60}
Estrellas Visitadas: {stats.get('stars_visited', 0)}
Energía Final: {stats.get('final_energy', 0)}%
Pasto Final: {stats.get('final_grass', 0)} kg
Estado Final: {stats.get('final_health_state', 'N/A')}
Éxito: {'SÍ' if stats.get('success', False) else 'NO'}

Condiciones Iniciales:
- Energía: {stats.get('initial_condition', {}).get('energia_inicial', 'N/A')}%
- Pasto: {stats.get('initial_condition', {}).get('pasto', 'N/A')} kg
- Edad: {stats.get('initial_condition', {}).get('edad', 'N/A')} años

Ruta Optimizada:
{' → '.join(stats.get('route', []))}
        """
        self.visualization_panel.update_info_text(info)
    
    def _update_max_visit_info(self, stats: Dict[str, Any]):
        """Update info display for max visit route."""
        json_values = stats.get('json_values_used', {})
        
        info = f"""
RUTA DE MÁXIMAS ESTRELLAS (SOLO VALORES DEL JSON)
{'='*60}
Estrellas Visitadas: {stats.get('stars_visited', 0)}
Distancia Total: {stats.get('total_distance', 0):.2f} unidades
Tiempo de Vida Consumido: {stats.get('life_time_consumed', 0):.2f} años

VALORES USADOS DEL JSON (INMUTABLES):
- Energía Inicial: {json_values.get('energia_inicial', 'N/A')}%
- Pasto Inicial: {json_values.get('pasto_inicial', 'N/A')} kg
- Edad Inicial: {json_values.get('edad_inicial', 'N/A')} años
- Death Age: {json_values.get('death_age', 'N/A')} años
- Estado Salud: {json_values.get('estado_salud', 'N/A').title()}
- Warp Factor: {json_values.get('warp_factor', 'N/A')}
- Age Factor: {json_values.get('age_factor', 'N/A'):.2f}

Secuencia de Estrellas:
{' → '.join(stats.get('path_stars', []))}

IMPORTANTE: Esta ruta usa EXCLUSIVAMENTE los valores 
iniciales del archivo constellations.json.

{stats.get('notes', '')}
        """
        self.visualization_panel.update_info_text(info)
    
    def _update_min_cost_info(self, stats: Dict[str, Any]):
        """Update info display for min cost route."""
        info = f"""
RUTA DE MENOR GASTO POSIBLE
{'='*60}
Estrellas Visitadas: {stats.get('stars_visited', 0)}
Distancia Total: {stats.get('total_distance', 0):.2f} unidades
Pasto Consumido: {stats.get('total_grass_consumed', 0):.2f} kg
Energía Final: {stats.get('final_energy', 0):.2f}%

Condiciones Iniciales:
- Energía: {stats.get('initial_energy', 0):.2f}%
- Pasto: {stats.get('initial_grass', 0):.2f} kg
- Edad: {stats.get('initial_age', 0):.1f} años

Recursos Finales:
- Balance de Energía: {stats.get('net_energy', 0):.2f}%
- Pasto Restante: {stats.get('final_grass', 0):.2f} kg
- Estado Final: {stats.get('final_state', 'N/A')}

División de Tiempo Aplicada:
- Tiempo Comiendo: {(1-self.research_parameters.time_percentage)*100:.0f}%
- Tiempo Investigando: {self.research_parameters.time_percentage*100:.0f}%

Configuraciones Especiales:
- Consumo Energía Investigación: {self.research_parameters.energy_consumption_rate:.1f}%
- Estrellas con Config. Personalizada: {len(self.research_parameters.custom_star_settings)}

Ruta Optimizada:
{' → '.join(stats.get('path_stars', []))}

NOTA: Esta ruta minimiza el gasto total de recursos
siguiendo las reglas de investigación configuradas.
        """
        self.visualization_panel.update_info_text(info)
    
    def _confirm_min_cost_rules(self) -> bool:
        """Show min cost rules confirmation dialog."""
        rules_info = f"""
REGLAS DE MENOR GASTO POSIBLE:

• Solo puede comer si energía < 50%
• Bonus por estado de salud:
  - Excelente: +5% por kg
  - Regular: +3% por kg  
  - Malo: +2% por kg
• División de tiempo:
  - {(1-self.research_parameters.time_percentage)*100:.0f}% comer
  - {self.research_parameters.time_percentage*100:.0f}% investigar
• Consumo energía investigación: {self.research_parameters.energy_consumption_rate:.1f}% por tiempo
• Configuraciones específicas: {len(self.research_parameters.custom_star_settings)} estrellas
• Una estrella solo se visita una vez
• Objetivo: MENOR GASTO total

¿Continuar con el cálculo?"""
        
        return messagebox.askyesno("Confirmar Reglas", rules_info)
    
    def _update_config_button_status(self):
        """Update configuration button visual status."""
        has_custom_config = (
            self.research_parameters.energy_consumption_rate != 2.0 or
            self.research_parameters.time_percentage != 0.5 or
            self.research_parameters.life_time_bonus != 0.0 or
            self.research_parameters.energy_bonus_per_star != 0.0 or
            len(self.research_parameters.custom_star_settings) > 0
        )
        
        self.route_panel.update_config_button_status(has_custom_config)
    
    def _update_route_visualization(self, path: List[Star]):
        """Update the route visualization."""
        try:
            # Get burro location for visualization
            burro = self.space_map.create_burro_astronauta()
            
            # Generate visualization figure
            fig = self.visualization_service.update_visualization(
                path=path, 
                burro_location=burro.current_location
            )
            
            # Update the visualization panel
            self.visualization_panel.update_visualization(fig)
        except Exception as e:
            print(f"Error updating visualization: {e}")  # Debug info
    
    def _update_visualization_callback(self):
        """Callback for updating visualization when comets change."""
        try:
            # Update visualization without a specific path to show all changes
            burro = self.space_map.create_burro_astronauta()
            fig = self.visualization_service.update_visualization(
                path=self.current_path,
                burro_location=burro.current_location
            )
            self.visualization_panel.update_visualization(fig)
        except Exception as e:
            print(f"Error in visualization callback: {e}")  # Debug info