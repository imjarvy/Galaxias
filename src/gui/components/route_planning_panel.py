"""
Route Planning Panel Component.
Implements Single Responsibility Principle - handles only route planning UI.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Callable, Optional
from ...core import SpaceMap, Star
from ..interfaces.component_interface import IComponent


class RoutePlanningPanel(IComponent):
    """Component responsible for route planning interface."""
    
    def __init__(self, space_map: SpaceMap):
        self.space_map = space_map
        self.frame = None
        
        # UI Variables
        self.start_star_var = tk.StringVar()
        self.end_star_var = tk.StringVar()
        
        # Callbacks - implementing Observer pattern
        self.on_calculate_route: Optional[Callable] = None
        self.on_optimize_eating: Optional[Callable] = None
        self.on_max_visit_route: Optional[Callable] = None
        self.on_min_cost_route: Optional[Callable] = None
        self.on_edit_parameters: Optional[Callable] = None
        self.on_validate_impacts: Optional[Callable] = None
        self.on_travel: Optional[Callable] = None
        
        # State
        self.travel_enabled = False
    
    def create_widgets(self, parent: tk.Widget) -> tk.Widget:
        """Create and return the route planning widgets."""
        self.frame = tk.LabelFrame(parent, text="Planificación de Ruta",
                                  font=('Arial', 12, 'bold'),
                                  bg='#000066', fg='white', 
                                  relief=tk.GROOVE, borderwidth=2)
        
        self._create_star_selectors()
        self._create_route_buttons()
        self._create_config_buttons()
        self._create_travel_button()
        
        return self.frame
    
    def _create_star_selectors(self):
        """Create star selection widgets."""
        # Start star selection
        tk.Label(self.frame, text="Estrella Origen:", 
                bg='#000066', fg='white').pack(anchor=tk.W, padx=5, pady=(5,0))
        
        star_names = [f"{s.label} ({s.id}) - E:{s.amount_of_energy}" 
                     for s in self.space_map.get_all_stars_list()]
        
        self.start_combo = ttk.Combobox(self.frame, textvariable=self.start_star_var,
                                       values=star_names, state='readonly', width=30)
        self.start_combo.pack(padx=5, pady=5)
        if star_names:
            self.start_combo.current(0)
        
        # End star selection
        tk.Label(self.frame, text="Estrella Destino:", 
                bg='#000066', fg='white').pack(anchor=tk.W, padx=5)
        
        self.end_combo = ttk.Combobox(self.frame, textvariable=self.end_star_var,
                                     values=star_names, state='readonly', width=30)
        self.end_combo.pack(padx=5, pady=5)
        if len(star_names) > 1:
            self.end_combo.current(1)
    
    def _create_route_buttons(self):
        """Create route calculation buttons."""
        tk.Button(self.frame, text="Calcular Ruta Óptima",
                 command=self._handle_calculate_route,
                 bg='#4444FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        tk.Button(self.frame, text="Optimizar Ruta para Comer Estrellas",
                 command=self._handle_optimize_eating,
                 bg='#FF44FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)

        tk.Button(self.frame, text="Maximizar Estrellas Visitadas",
                 command=self._handle_max_visit_route,
                 bg='#44FFAA', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)

        tk.Button(self.frame, text="Ruta Menor Gasto Posible",
                 command=self._handle_min_cost_route,
                 bg='#AA44FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
    
    def _create_config_buttons(self):
        """Create configuration buttons."""
        self.config_params_button = tk.Button(self.frame, text="⚙️ Configurar Parámetros",
                 command=self._handle_edit_parameters,
                 bg='#CC6600', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2)
        self.config_params_button.pack(pady=2)
        
        tk.Button(self.frame, text="🔬 Validar Impactos de Investigación",
                 command=self._handle_validate_impacts,
                 bg='#FF6600', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=2)
    
    def _create_travel_button(self):
        """Create travel button."""
        self.travel_button = tk.Button(self.frame, text="Iniciar Viaje",
                                       command=self._handle_travel,
                                       bg='#44FF44', fg='black', 
                                       font=('Arial', 10, 'bold'),
                                       relief=tk.RAISED, borderwidth=2,
                                       state=tk.DISABLED)
        self.travel_button.pack(pady=5)
    
    def _handle_calculate_route(self):
        """Handle calculate route button click."""
        if self.on_calculate_route:
            self.on_calculate_route(self.start_star_var.get(), self.end_star_var.get())
    
    def _handle_optimize_eating(self):
        """Handle optimize eating route button click."""
        if self.on_optimize_eating:
            self.on_optimize_eating(self.start_star_var.get())
    
    def _handle_max_visit_route(self):
        """Handle max visit route button click."""
        if self.on_max_visit_route:
            self.on_max_visit_route(self.start_star_var.get())
    
    def _handle_min_cost_route(self):
        """Handle min cost route button click."""
        if self.on_min_cost_route:
            self.on_min_cost_route(self.start_star_var.get())
    
    def _handle_edit_parameters(self):
        """Handle edit parameters button click."""
        if self.on_edit_parameters:
            self.on_edit_parameters()
    
    def _handle_validate_impacts(self):
        """Handle validate impacts button click."""
        if self.on_validate_impacts:
            self.on_validate_impacts()
    
    def _handle_travel(self):
        """Handle travel button click."""
        if self.on_travel:
            self.on_travel()
    
    def update_display(self):
        """Update the component's display."""
        if self.travel_button:
            state = tk.NORMAL if self.travel_enabled else tk.DISABLED
            self.travel_button.config(state=state)
    
    def set_travel_enabled(self, enabled: bool):
        """Enable or disable travel button."""
        self.travel_enabled = enabled
        self.update_display()
    
    def update_config_button_status(self, has_custom_config: bool):
        """Update configuration button visual status."""
        if has_custom_config:
            self.config_params_button.config(
                text="✅ Parámetros Configurados",
                bg='#00AA00',
                fg='white'
            )
        else:
            self.config_params_button.config(
                text="⚙️ Configurar Parámetros",
                bg='#CC6600',
                fg='white'
            )