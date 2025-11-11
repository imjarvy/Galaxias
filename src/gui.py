"""
Graphical User Interface for the Galaxias space route simulation.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.models import SpaceMap, BurroAstronauta, Comet, Star
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer
from src.donkey_optimization import DonkeyRouteOptimizer
from src.parameter_editor_simple import ResearchParameterEditor, ResearchParameters
from src.research_impact_validator import ResearchImpactValidatorGUI
from src.life_monitor import LifeMonitor, BasicSoundManager
from src.gui_life_monitor import (TkinterAlertSystem, GuiLifeStatusWidget, 
                                   TravelDistanceAnalyzer, LifeEventLogger)
from src.hypergiant_jump import HyperGiantJumpSystem
from src.gui_hypergiant_jump import HyperGiantJumpGUI


class GalaxiasGUI:
    """Main GUI application for Galaxias space route simulation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Galaxias - Sistema de Rutas del Burro Astronauta")
        self.root.geometry("1400x900")
        self.root.configure(bg='#000033')
        
        # Load configuration
        with open('data/spaceship_config.json', 'r') as f:
            self.config = json.load(f)
        
        # Initialize space map
        self.space_map = SpaceMap('data/constellations.json')
        
        # Initialize burro astronauta
        self.burro = self.space_map.create_burro_astronauta()
        
        # Initialize life monitoring system
        self.life_alert_system = TkinterAlertSystem(self.root)
        self.life_sound_manager = BasicSoundManager()
        self.life_monitor = LifeMonitor(
            alert_system=self.life_alert_system,
            sound_manager=self.life_sound_manager
        )
        self.life_event_logger = LifeEventLogger()
        self.travel_analyzer = TravelDistanceAnalyzer(self.root)
        
        # Configure burro with life monitor
        self.burro.set_life_monitor(self.life_monitor)
        self.life_monitor.add_observer(self.life_event_logger)
        self.travel_analyzer.set_burro(self.burro)
        
        # Initialize calculator, visualizer, and optimizer
        self.calculator = RouteCalculator(self.space_map, self.config)
        self.visualizer = SpaceVisualizer(self.space_map)
        self.optimizer = DonkeyRouteOptimizer(self.space_map)
        
        # Initialize hypergiant jump system
        self.hypergiant_system = HyperGiantJumpSystem(self.space_map)
        self.hypergiant_gui = HyperGiantJumpGUI(self.root, self.space_map, self.burro)
        
        # Research parameters for min cost calculations
        self.research_parameters = ResearchParameters()
        
        # Research impact validator
        self.research_impact_validator = None
        
        # Current path
        self.current_path = None
        self.current_path_stats = None
        
        # Comet impact manager (will be initialized in parameter editor)
        self.comet_impact_manager = None
        
        # Setup UI
        self.setup_ui()
        
        # Update initial button status
        self.update_config_button_status()
        
        # Initial visualization
        self.update_visualization()
    
    def setup_ui(self):
        """Setup the user interface."""
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
        
        # Route Planning Section
        route_frame = tk.LabelFrame(left_panel, text="Planificación de Ruta",
                                   font=('Arial', 12, 'bold'),
                                   bg='#000066', fg='white', 
                                   relief=tk.GROOVE, borderwidth=2)
        route_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        # Start star selection
        tk.Label(route_frame, text="Estrella Origen:", 
                bg='#000066', fg='white').pack(anchor=tk.W, padx=5, pady=(5,0))
        
        self.start_star_var = tk.StringVar()
        star_names = [f"{s.label} ({s.id}) - E:{s.amount_of_energy}" for s in self.space_map.get_all_stars_list()]
        self.start_combo = ttk.Combobox(route_frame, textvariable=self.start_star_var,
                                       values=star_names, state='readonly', width=30)
        self.start_combo.pack(padx=5, pady=5)
        if star_names:
            self.start_combo.current(0)
        
        # End star selection
        tk.Label(route_frame, text="Estrella Destino:", 
                bg='#000066', fg='white').pack(anchor=tk.W, padx=5)
        
        self.end_star_var = tk.StringVar()
        self.end_combo = ttk.Combobox(route_frame, textvariable=self.end_star_var,
                                     values=star_names, state='readonly', width=30)
        self.end_combo.pack(padx=5, pady=5)
        if len(star_names) > 1:
            self.end_combo.current(1)
        
        # Calculate route button
        tk.Button(route_frame, text="Calcular Ruta Óptima",
                 command=self.calculate_route,
                 bg='#4444FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        # Optimize route button
        tk.Button(route_frame, text="Optimizar Ruta para Comer Estrellas",
                 command=self.optimize_eating_route,
                 bg='#FF44FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)

        # Max visit route button (NEW)
        tk.Button(route_frame, text="Maximizar Estrellas Visitadas",
                 command=self.calculate_max_visit_route,
                 bg='#44FFAA', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)

        # Min cost route button (NEW)
        tk.Button(route_frame, text="Ruta Menor Gasto Posible",
                 command=self.calculate_min_cost_route,
                 bg='#AA44FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        # Edit research parameters button (NEW)
        self.config_params_button = tk.Button(route_frame, text="⚙️ Configurar Parámetros",
                 command=self.edit_research_parameters,
                 bg='#CC6600', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2)
        self.config_params_button.pack(pady=2)
        
        # Research Impact Validation button (NEW)
        tk.Button(route_frame, text="🔬 Validar Impactos de Investigación",
                 command=self.validate_research_impacts,
                 bg='#FF6600', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=2)
        
        # Travel button
        self.travel_button = tk.Button(route_frame, text="Iniciar Viaje",
                                       command=self.start_journey,
                                       bg='#44FF44', fg='black', 
                                       font=('Arial', 10, 'bold'),
                                       relief=tk.RAISED, borderwidth=2,
                                       state=tk.DISABLED)
        self.travel_button.pack(pady=5)
        
        # Burro Status Section
        status_frame = tk.LabelFrame(left_panel, text="Estado del Burro Astronauta",
                                    font=('Arial', 12, 'bold'),
                                    bg='#000066', fg='white',
                                    relief=tk.GROOVE, borderwidth=2)
        status_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=10, width=35,
                                                     bg='#000033', fg='white',
                                                     font=('Courier', 9))
        self.status_text.pack(padx=5, pady=5)
        
        # Restore resources button
        tk.Button(status_frame, text="Restaurar Recursos",
                 command=self.restore_burro_resources,
                 bg='#FFAA44', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        # Life Monitor Section (NEW)
        life_frame = tk.LabelFrame(left_panel, text="Monitoreo de Vida",
                                  font=('Arial', 12, 'bold'),
                                  bg='#000066', fg='white',
                                  relief=tk.GROOVE, borderwidth=2)
        life_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Widget de estado de vida
        self.life_status_widget = GuiLifeStatusWidget(life_frame)
        self.life_status_widget.pack(fill=tk.X, padx=5, pady=5)
        
        # Botón para análisis de viaje
        tk.Button(life_frame, text="📊 Analizar Próximo Viaje",
                 command=self.analyze_next_travel,
                 bg='#6633FF', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=2)
        
        # Botón para simular countdown (DEMO)
        tk.Button(life_frame, text="⏰ Demo Countdown",
                 command=self.demo_countdown,
                 bg='#FF3366', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=2)
        
        # === COMET MANAGEMENT MOVED TO SCIENTIFIC PANEL ===
        # La gestión de cometas ahora está disponible en el panel científico
        # Acceso: ⚙️ Configurar Parámetros → pestaña "🌌 Cometas"
        
        # Reports Section
        report_frame = tk.LabelFrame(left_panel, text="Reportes",
                                    font=('Arial', 12, 'bold'),
                                    bg='#000066', fg='white',
                                    relief=tk.GROOVE, borderwidth=2)
        report_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        tk.Button(report_frame, text="Generar Reporte Visual",
                 command=self.generate_report,
                 bg='#FFFF44', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=10)
        
        # Right panel - Visualization
        right_panel = tk.Frame(main_frame, bg='#000033')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas for matplotlib
        self.canvas_frame = tk.Frame(right_panel, bg='#000033')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info text at bottom
        self.info_text = scrolledtext.ScrolledText(right_panel, height=6, 
                                                   bg='#000033', fg='white',
                                                   font=('Courier', 9))
        self.info_text.pack(fill=tk.X, pady=5)
        
        # Update status
        self.update_status_display()
    
    def extract_star_id(self, combo_text: str) -> Optional[str]:
        """Extract star ID from combo box text."""
        if not combo_text:
            return None
        # Format is "Label (id) - E:energy"
        start = combo_text.find('(')
        end = combo_text.find(')')
        if start != -1 and end != -1:
            return combo_text[start+1:end]
        return None
    
    def calculate_route(self):
        """Calculate optimal route between selected stars."""
        start_id = self.extract_star_id(self.start_star_var.get())
        end_id = self.extract_star_id(self.end_star_var.get())
        
        if not start_id or not end_id:
            messagebox.showerror("Error", "Seleccione estrellas de origen y destino")
            return
        
        start_star = self.space_map.get_star(start_id)
        end_star = self.space_map.get_star(end_id)
        
        if not start_star or not end_star:
            messagebox.showerror("Error", "Estrellas no encontradas")
            return
        
        # Calculate path
        path, cost = self.calculator.dijkstra(start_star, end_star)
        
        if not path:
            messagebox.showwarning("Sin Ruta", 
                                  "No hay ruta disponible entre estas estrellas.\n"
                                  "Verifique si hay cometas bloqueando el camino.")
            self.current_path = None
            self.current_path_stats = None
            self.travel_button.config(state=tk.DISABLED)
            return
        
        # Calculate path statistics
        self.current_path = path
        self.current_path_stats = self.calculator.calculate_path_stats(path)
        
        # Register as active journey for comet impact analysis
        self._register_active_journey(path, "optimal")
        
        # Update info text
        info = f"""
RUTA CALCULADA
{'='*60}
Origen: {start_star.label}
Destino: {end_star.label}
Costo Total: {cost:.2f}

Estadísticas:
- Distancia Total: {self.current_path_stats['total_distance']} unidades
- Saltos: {self.current_path_stats['num_jumps']}
- Peligro Total: {self.current_path_stats['total_danger']}

Recursos Necesarios:
- Energía para Viajar: {self.current_path_stats['total_energy_needed']:.2f}
- Pasto Necesario: {self.current_path_stats['total_grass_needed']:.2f} kg
- Energía Ganada: {self.current_path_stats['total_energy_gained']:.2f}
- Balance Neto: {self.current_path_stats['net_energy']:.2f}

Ruta: {' → '.join(self.current_path_stats['path_stars'])}
        """
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
        
        # Enable travel button
        self.travel_button.config(state=tk.NORMAL)
        
        # Update visualization
        self.update_visualization()
        
        messagebox.showinfo("Ruta Calculada", 
                           f"Ruta encontrada con {self.current_path_stats['num_jumps']} saltos")
    
    def optimize_eating_route(self):
        """Optimize route for maximum star eating."""
        start_id = self.extract_star_id(self.start_star_var.get())
        
        if not start_id:
            messagebox.showerror("Error", "Seleccione estrella de origen")
            return
        
        # Use the optimizer
        optimal_path, stats = self.optimizer.optimize_route_from_json_data(start_id)
        
        if stats.get('error'):
            messagebox.showerror("Error", stats['error'])
            return
        
        if not optimal_path:
            messagebox.showwarning("Sin Ruta", "No se pudo encontrar una ruta óptima")
            return
        
        # Set as current path
        self.current_path = optimal_path
        self.current_path_stats = self.calculator.calculate_path_stats(optimal_path)
        
        # Register as active journey for comet impact analysis
        self._register_active_journey(optimal_path, "eating_optimization")
        
        # Update info text
        info = f"""
RUTA OPTIMIZADA PARA COMER ESTRELLAS
{'='*60}
Estrellas Visitadas: {stats['stars_visited']}
Energía Final: {stats['final_energy']}%
Pasto Final: {stats['final_grass']} kg
Estado Final: {stats['final_health_state']}
Éxito: {'SÍ' if stats['success'] else 'NO'}

Condiciones Iniciales:
- Energía: {stats['initial_condition']['energia_inicial']}%
- Pasto: {stats['initial_condition']['pasto']} kg
- Edad: {stats['initial_condition']['edad']} años

Ruta Optimizada:
{' → '.join(stats['route'])}
        """
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
        
        # Enable travel button
        self.travel_button.config(state=tk.NORMAL)
        
        # Update visualization
        self.update_visualization()
        
        messagebox.showinfo("Ruta Optimizada", 
                           f"Ruta optimizada encontrada: {stats['stars_visited']} estrellas visitadas")
    
    def calculate_max_visit_route(self):
        """Calculate route that maximizes number of stars visited using ONLY JSON values."""
        start_id = self.extract_star_id(self.start_star_var.get())
        
        if not start_id:
            messagebox.showerror("Error", "Selecciona una estrella de inicio")
            return
        
        start_star = self.space_map.get_star(start_id)
        if not start_star:
            messagebox.showerror("Error", "Estrella de inicio no encontrada")
            return
        
        # Usar SOLO valores del JSON - no parámetros del burro actual
        max_path, stats = self.calculator.find_max_visit_route_from_json(start=start_star)
        
        if stats.get('error'):
            messagebox.showerror("Error", stats['error'])
            return
        
        if not max_path:
            messagebox.showwarning("Sin Resultado", "No se pudo encontrar ruta válida con valores del JSON")
            return
        
        # Set as current path
        self.current_path = max_path
        self.current_path_stats = self.calculator.calculate_path_stats(max_path)
        
        # Update info text
        json_values = stats.get('json_values_used', {})
        
        info = f"""
RUTA DE MÁXIMAS ESTRELLAS (SOLO VALORES DEL JSON)
{'='*60}
Estrellas Visitadas: {stats['stars_visited']}
Distancia Total: {stats['total_distance']:.2f} unidades
Tiempo de Vida Consumido: {stats['life_time_consumed']:.2f} años

VALORES USADOS DEL JSON (INMUTABLES):
- Energía Inicial: {json_values.get('energia_inicial', 'N/A')}%
- Pasto Inicial: {json_values.get('pasto_inicial', 'N/A')} kg
- Edad Inicial: {json_values.get('edad_inicial', 'N/A')} años
- Death Age: {json_values.get('death_age', 'N/A')} años
- Estado Salud: {json_values.get('estado_salud', 'N/A').title()}
- Warp Factor: {json_values.get('warp_factor', 'N/A')}
- Age Factor: {json_values.get('age_factor', 'N/A'):.2f}

Secuencia de Estrellas:
{' → '.join(stats['path_stars'])}

IMPORTANTE: Esta ruta usa EXCLUSIVAMENTE los valores 
iniciales del archivo constellations.json. No se 
consideran cambios actuales del burro astronauta.

{stats.get('notes', '')}
        """
        
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
        
        # Enable travel button
        self.travel_button.config(state=tk.NORMAL)
        
        # Update visualization
        self.update_visualization()
        
        messagebox.showinfo("Ruta de Máximo Alcance (JSON)", 
                           f"Ruta encontrada usando valores del JSON:\n"
                           f"• {stats['stars_visited']} estrellas visitadas\n"
                           f"• {stats['life_time_consumed']:.1f} años de vida\n"
                           f"• Energía inicial: {json_values.get('energia_inicial')}%\n"
                           f"• Edad inicial: {json_values.get('edad_inicial')} años")
    
    def calculate_min_cost_route(self):
        """Calcula la ruta de menor gasto posible con reglas específicas."""
        try:
            start_text = self.start_star_var.get()
            start_id = self.extract_star_id(start_text)
            
            if not start_id:
                messagebox.showwarning("Advertencia", "Por favor selecciona una estrella de origen")
                return
            
            start_star = self.space_map.get_star(start_id)
            if not start_star:
                messagebox.showerror("Error", f"Estrella {start_id} no encontrada")
                return
            
            # Mostrar información sobre las reglas con parámetros actuales
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
            
            if not messagebox.askyesno("Confirmar Reglas", rules_info):
                return
            
            self.status_text.insert(tk.END, "\n" + "="*40)
            self.status_text.insert(tk.END, "\nCalculando ruta de MENOR GASTO...")
            self.status_text.insert(tk.END, f"\nDesde: {start_star.label} ({start_id})")
            self.status_text.insert(tk.END, "\nReglas específicas activadas...")
            self.status_text.see(tk.END)
            self.root.update()
            
            # Calcular ruta de menor gasto usando parámetros configurables
            path, stats = self.calculator.find_min_cost_route_from_json(start_star, research_params=self.research_parameters)
            
            if not path or 'error' in stats:
                error_msg = stats.get('error', 'No se pudo calcular la ruta')
                self.status_text.insert(tk.END, f"\n❌ Error: {error_msg}")
                self.status_text.see(tk.END)
                return
            
            # Actualizar visualización
            self.current_path = path
            self.current_path_stats = stats
            self.update_visualization()
            self.travel_button.config(state=tk.NORMAL)
            
            # Mostrar resultados detallados
            self.status_text.insert(tk.END, "\n" + "="*40)
            self.status_text.insert(tk.END, "\n🎯 RUTA DE MENOR GASTO CALCULADA")
            self.status_text.insert(tk.END, "\n" + "="*40)
            self.status_text.insert(tk.END, f"\n📍 Estrellas visitadas: {stats['stars_visited']}")
            self.status_text.insert(tk.END, f"\n📏 Distancia total: {stats['total_distance']} años luz")
            self.status_text.insert(tk.END, f"\n⏱️ Tiempo vida usado: {stats['life_time_consumed']:.2f} años")
            self.status_text.insert(tk.END, f"\n🌱 Pasto consumido: {stats['total_grass_consumed']:.2f} kg")
            self.status_text.insert(tk.END, f"\n⚡ Energía final: {stats['final_energy']:.2f}%")
            self.status_text.insert(tk.END, f"\n💫 Vida restante: {stats['remaining_life']:.2f} años")
            
            # Mostrar secuencia de estrellas
            self.status_text.insert(tk.END, "\n\n📋 SECUENCIA DE ESTRELLAS:")
            for i, star in enumerate(path, 1):
                self.status_text.insert(tk.END, f"\n  {i}. {star.label} (ID: {star.id})")
            
            # Mostrar detalle de acciones si está disponible
            if 'star_actions_detail' in stats:
                self.status_text.insert(tk.END, "\n\n🔍 DETALLE DE ACCIONES POR ESTRELLA:")
                for action in stats['star_actions_detail']:
                    self.status_text.insert(tk.END, f"\n\n⭐ {action.star_label} (ID: {action.star_id})")
                    self.status_text.insert(tk.END, f"\n   Energía al llegar: {action.arrived_energy:.1f}%")
                    self.status_text.insert(tk.END, f"\n   Puede comer: {'Sí' if action.can_eat else 'No'}")
                    if action.can_eat and action.ate_kg > 0:
                        self.status_text.insert(tk.END, f"\n   Comió: {action.ate_kg:.2f} kg")
                        self.status_text.insert(tk.END, f"\n   Energía ganada: +{action.energy_gained_eating:.1f}%")
                        self.status_text.insert(tk.END, f"\n   Tiempo comiendo: {action.time_eating:.1f}")
                    self.status_text.insert(tk.END, f"\n   Tiempo investigando: {action.time_researching:.1f}")
                    self.status_text.insert(tk.END, f"\n   Energía por investigar: -{action.energy_consumed_research:.1f}%")
                    self.status_text.insert(tk.END, f"\n   Energía final: {action.final_energy:.1f}%")
            
            self.status_text.insert(tk.END, "\n" + "="*40)
            self.status_text.insert(tk.END, "\n✅ Cálculo completado!")
            self.status_text.see(tk.END)
            
            messagebox.showinfo("Éxito", 
                f"Ruta de menor gasto calculada!\n"
                f"Estrellas visitadas: {stats['stars_visited']}\n"
                f"Pasto consumido: {stats['total_grass_consumed']:.2f} kg\n"
                f"Energía final: {stats['final_energy']:.2f}%")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error calculando ruta de menor gasto: {str(e)}")

    def start_journey(self):
        """Start the journey along the calculated path."""
        if not self.current_path or len(self.current_path) == 0:
            messagebox.showerror("Error", "Primero calcule una ruta")
            return
        
        # Simulate the journey
        self.burro.current_location = self.current_path[0]
        self.burro.journey_history = []
        
        for i, star in enumerate(self.current_path):
            # Check if can eat the star
            if self.burro.can_eat_star(star):
                self.burro.consume_resources_eating_star(star)
                self.burro.journey_history.append(star)
                
                if not self.burro.is_alive():
                    messagebox.showerror("Viaje Fallido",
                                        f"El Burro Astronauta no sobrevivió.\n"
                                        f"Llegó hasta: {star.label}")
                    break
            
            # Travel to next star if not the last one
            if i < len(self.current_path) - 1:
                next_star = self.current_path[i + 1]
                
                # Calculate travel distance
                travel_distance = 0
                path, _ = self.calculator.dijkstra(star, next_star)
                if path and len(path) > 1:
                    for j in range(len(path) - 1):
                        current = path[j]
                        next_node = path[j + 1]
                        for route in self.space_map.routes:
                            if ((route.from_star == current and route.to_star == next_node) or
                                (route.to_star == current and route.from_star == next_node)):
                                travel_distance += route.distance
                                break
                
                # Check if can travel
                if not self.burro.can_travel(travel_distance):
                    messagebox.showwarning("Viaje Interrumpido",
                                          f"El Burro no tiene suficientes recursos para continuar.\n"
                                          f"Se detuvo en: {star.label}")
                    break
                
                # Travel
                self.burro.consume_resources_traveling(travel_distance)
                self.burro.current_location = next_star
        
        # Update displays
        self.update_status_display()
        self.update_visualization()
        
        if self.burro.is_alive():
            messagebox.showinfo("Viaje Completado",
                               f"¡Viaje exitoso!\n"
                               f"El Burro Astronauta visitó {len(self.burro.journey_history)} estrellas\n"
                               f"Energía restante: {self.burro.current_energy}%")
        
        # Reset path
        self.current_path = None
        self.travel_button.config(state=tk.DISABLED)
    
    def restore_burro_resources(self):
        """Restore the burro's resources."""
        self.burro.restore_resources()
        self.update_status_display()
        messagebox.showinfo("Recursos Restaurados", "Recursos restaurados a valores iniciales")
    
    def add_comet(self):
        """Add a comet to block a route - MOVED TO SCIENTIFIC PANEL."""
        messagebox.showinfo("Función Reubicada", 
                           "🌌 La gestión de cometas se ha movido al panel científico.\n\n"
                           "Para agregar/remover cometas:\n"
                           "1. Haga clic en '⚙️ Configurar Parámetros'\n"
                           "2. Vaya a la pestaña '🌌 Cometas'\n"
                           "3. Use la interfaz mejorada para gestionar cometas")
    
    def remove_comet(self):
        """Remove a comet - MOVED TO SCIENTIFIC PANEL."""
        messagebox.showinfo("Función Reubicada", 
                           "🌌 La gestión de cometas se ha movido al panel científico.\n\n"
                           "Para agregar/remover cometas:\n"
                           "1. Haga clic en '⚙️ Configurar Parámetros'\n"
                           "2. Vaya a la pestaña '🌌 Cometas'\n"
                           "3. Use la interfaz mejorada para gestionar cometas")
    
    def generate_report(self):
        """Generate visual report."""
        if not self.current_path_stats:
            # Use empty stats
            self.current_path_stats = self.calculator.calculate_path_stats([])
        
        self.visualizer.plot_journey_report(
            self.burro,
            self.current_path_stats,
            save_path='assets/journey_report.png',
            show=True
        )
    
    def update_status_display(self):
        """Update the status text display."""
        status = self.burro.get_status()
        
        status_str = f"""
{'='*30}
BURRO ASTRONAUTA
{'='*30}
Nombre: {status['name']}
Ubicación: {status['location']}

RECURSOS:
  Energía:     {status['energia']}% / 100%
  Pasto:       {status['pasto']} kg
  Edad inicial:{status['edad_inicial']} años
  Edad actual: {status['edad_actual']:.1f} años

TIEMPO DE VIDA:
  Vida restante:   {status['vida_restante']:.1f} años
  Vida consumida:  {status['vida_consumida']:.1f} años
  Muerte prevista: {status['edad_muerte']} años
  Monitor activo:  {'Sí' if status.get('life_monitor_active', False) else 'No'}

ESTADO:
  Salud:       {status['estado_salud'].upper()}
  Viajes:      {status['journey_length']}
  Estado:      {'✅ VIVO' if status['is_alive'] else '❌ MUERTO'}

DATOS JSON:
  BurroEnergía:    {status['energia']}%
  Estado Salud:    {status['estado_salud']}
        """
        
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, status_str)
        
        # Actualizar widget de vida
        if hasattr(self, 'life_status_widget'):
            self.life_status_widget.update_status(status)
    
    def update_visualization(self):
        """Update the space map visualization."""
        # Clear previous canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Create new figure
        fig = self.visualizer.plot_space_map(
            highlight_path=self.current_path,
            donkey_location=self.burro.current_location,
            show=False
        )
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.close(fig)
    
    def edit_research_parameters(self):
        """Abre el editor de parámetros de investigación."""
        try:
            self.status_text.insert(tk.END, "\n🔧 Abriendo editor de parámetros de investigación...")
            self.status_text.see(tk.END)
            self.root.update()
            
            # Crear editor con parámetros actuales y callback de visualización
            editor = ResearchParameterEditor(self.root, self.space_map, self.research_parameters, 
                                           self.update_visualization)
            
            # Pasar el manager de impacto de cometas al editor si existe
            if hasattr(editor, 'comet_manager'):
                editor.comet_manager.comet_impact_manager = self._get_comet_impact_manager()
            
            # Esperar a que se cierre la ventana
            self.root.wait_window(editor.window)
            
            # Obtener parámetros configurados
            new_params = editor.get_parameters()
            
            if new_params is not None:
                # Actualizar parámetros
                self.research_parameters = new_params
                
                # Actualizar indicador visual del botón
                self.update_config_button_status()
                
                self.status_text.insert(tk.END, "\n✅ Parámetros de investigación actualizados:")
                self.status_text.insert(tk.END, f"\n   • Consumo energía: {new_params.energy_consumption_rate:.1f}% por tiempo")
                self.status_text.insert(tk.END, f"\n   • Tiempo investigación: {new_params.time_percentage*100:.1f}%")
                self.status_text.insert(tk.END, f"\n   • Bonus tiempo vida: {new_params.life_time_bonus:+.1f} años")
                self.status_text.insert(tk.END, f"\n   • Bonus energía: {new_params.energy_bonus_per_star:+.1f}% por estrella")
                self.status_text.insert(tk.END, f"\n   • Configuraciones específicas: {len(new_params.custom_star_settings)} estrellas")
                
                # Información adicional
                if new_params.custom_star_settings:
                    self.status_text.insert(tk.END, "\n\n📝 Estrellas con configuración específica:")
                    for star_id, config in new_params.custom_star_settings.items():
                        star = self.space_map.get_star(star_id)
                        star_name = star.label if star else f"ID:{star_id}"
                        self.status_text.insert(tk.END, f"\n   🌟 {star_name}: energía={config.get('energy_rate', 'default'):.1f}%, tiempo={config.get('time_bonus', 'default'):+.1f}a")
                
                
                # Preguntar si desea recalcular rutas automáticamente
                recalculate = messagebox.askyesno("Parámetros Actualizados", 
                    f"Se han configurado exitosamente los parámetros de investigación.\n\n"
                    f"Resumen:\n"
                    f"• Consumo energía: {new_params.energy_consumption_rate:.1f}% por tiempo\n"
                    f"• Tiempo investigación: {new_params.time_percentage*100:.1f}%\n"
                    f"• Configuraciones específicas: {len(new_params.custom_star_settings)}\n\n"
                    f"¿Desea recalcular automáticamente las rutas con los nuevos parámetros?")
                
                if recalculate:
                    self.status_text.insert(tk.END, "\n\n🔄 Recalculando rutas con nuevos parámetros...")
                    self.recalculate_routes_with_new_parameters()
                else:
                    self.status_text.insert(tk.END, "\n\n💡 Los nuevos parámetros se aplicarán en el próximo cálculo manual de ruta.")
                
            else:
                self.status_text.insert(tk.END, "\n❌ Configuración de parámetros cancelada")
            
            self.status_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir editor de parámetros: {str(e)}")
            self.status_text.insert(tk.END, f"\n❌ Error: {str(e)}")
            self.status_text.see(tk.END)
    
    def recalculate_routes_with_new_parameters(self):
        """Recalcula las rutas disponibles con los nuevos parámetros de investigación."""
        try:
            # Verificar que tenemos estrellas seleccionadas
            if not self.start_star_var.get():
                self.status_text.insert(tk.END, "\n⚠️  Seleccione una estrella de origen para recalcular")
                return
            
            start_id = self.extract_star_id(self.start_star_var.get())
            start_star = self.space_map.get_star(start_id)
            
            if not start_star:
                self.status_text.insert(tk.END, "\n❌ Estrella de origen no encontrada")
                return
            
            self.status_text.insert(tk.END, f"\n\n🚀 RECALCULANDO RUTAS CON NUEVOS PARÁMETROS")
            self.status_text.insert(tk.END, f"\n{'=' * 50}")
            
            # 1. Recalcular ruta de menor gasto
            self.status_text.insert(tk.END, "\n\n1️⃣ Recalculando ruta de menor gasto...")
            try:
                path, stats = self.calculator.find_min_cost_route_from_json(
                    start_star, 
                    research_params=self.research_parameters
                )
                
                if path and len(path) > 1:
                    route_summary = " → ".join([s.label for s in path])
                    self.status_text.insert(tk.END, f"\n   ✅ Ruta menor gasto: {route_summary}")
                    self.status_text.insert(tk.END, f"\n   📊 Estrellas: {stats.get('num_stars', 0)}, Tiempo: {stats.get('life_time_consumed', 0):.1f}a")
                    
                    # Actualizar visualización
                    self.current_path = path
                    self.current_path_stats = stats
                else:
                    self.status_text.insert(tk.END, "\n   ❌ No se encontró ruta de menor gasto válida")
                    
            except Exception as e:
                self.status_text.insert(tk.END, f"\n   ❌ Error en ruta menor gasto: {str(e)}")
            
            # 2. Recalcular ruta de máximas visitas
            self.status_text.insert(tk.END, "\n\n2️⃣ Recalculando ruta de máximas visitas...")
            try:
                path, stats = self.calculator.find_max_visit_route_from_json(start_star)
                
                if path and len(path) > 0:
                    route_summary = " → ".join([s.label for s in path])
                    self.status_text.insert(tk.END, f"\n   ✅ Ruta máximas visitas: {route_summary}")
                    self.status_text.insert(tk.END, f"\n   📊 Estrellas: {len(path)}, Tiempo: {stats.get('life_time_consumed', 0):.1f}a")
                else:
                    self.status_text.insert(tk.END, "\n   ❌ No se encontró ruta de máximas visitas válida")
                    
            except Exception as e:
                self.status_text.insert(tk.END, f"\n   ❌ Error en ruta máximas visitas: {str(e)}")
            
            # 3. Recalcular optimización para comer estrellas
            self.status_text.insert(tk.END, "\n\n3️⃣ Recalculando optimización para comer estrellas...")
            try:
                optimal_path, optimization_stats = self.optimizer.simulate_journey(start_star, self.burro)
                
                if optimal_path and len(optimal_path) > 0:
                    eating_summary = " → ".join([s.label for s in optimal_path])
                    self.status_text.insert(tk.END, f"\n   ✅ Ruta optimizada: {eating_summary}")
                    self.status_text.insert(tk.END, f"\n   📊 Estrellas comidas: {optimization_stats.get('stars_visited', 0)}")
                    self.status_text.insert(tk.END, f"\n   📊 Energía final: {optimization_stats.get('final_energy', 0):.1f}%")
                else:
                    self.status_text.insert(tk.END, "\n   ❌ No se encontró optimización para comer estrellas válida")
                    
            except Exception as e:
                self.status_text.insert(tk.END, f"\n   ❌ Error en optimización: {str(e)}")
            
            # Actualizar visualización con la mejor ruta encontrada
            if self.current_path:
                self.update_visualization()
                self.status_text.insert(tk.END, "\n\n🎨 Visualización actualizada con la nueva ruta")
            
            self.status_text.insert(tk.END, "\n\n✅ RECÁLCULO COMPLETADO")
            self.status_text.insert(tk.END, "\n💡 Los resultados reflejan los nuevos parámetros de investigación")
            self.status_text.see(tk.END)
            
        except Exception as e:
            self.status_text.insert(tk.END, f"\n❌ Error durante recálculo: {str(e)}")
            self.status_text.see(tk.END)
    
    def update_config_button_status(self):
        """Actualiza el estado visual del botón de configurar parámetros."""
        try:
            # Verificar si hay configuraciones personalizadas
            has_custom_config = (
                self.research_parameters.energy_consumption_rate != 2.0 or
                self.research_parameters.time_percentage != 0.5 or
                self.research_parameters.life_time_bonus != 0.0 or
                self.research_parameters.energy_bonus_per_star != 0.0 or
                len(self.research_parameters.custom_star_settings) > 0
            )
            
            if has_custom_config:
                # Configuración personalizada activa
                self.config_params_button.config(
                    text="✅ Parámetros Configurados",
                    bg='#00AA00',
                    fg='white'
                )
            else:
                # Configuración por defecto
                self.config_params_button.config(
                    text="⚙️ Configurar Parámetros",
                    bg='#CC6600',
                    fg='white'
                )
        except Exception as e:
            print(f"Error actualizando botón: {e}")
    
    def validate_research_impacts(self):
        """Abre el validador de impactos de investigación por estrella."""
        try:
            self.status_text.insert(tk.END, "\n🔬 Abriendo validador de impactos de investigación...")
            self.status_text.see(tk.END)
            self.root.update()
            
            # Crear validador
            validator_gui = ResearchImpactValidatorGUI(self.root, self.space_map)
            
            # Esperar a que se cierre la ventana
            self.root.wait_window(validator_gui.window)
            
            # Obtener resultado
            validator = validator_gui.get_result()
            
            if validator is not None:
                # Actualizar validador
                self.research_impact_validator = validator
                
                self.status_text.insert(tk.END, "\n✅ Validador de impactos configurado exitosamente")
                
                # Obtener configuración actual para mostrar resumen
                all_star_ids = [star.id for star in self.space_map.get_all_stars_list()]
                route_impact = validator.calculate_route_impact(all_star_ids)
                
                self.status_text.insert(tk.END, f"\n📊 RESUMEN DE IMPACTOS CONFIGURADOS:")
                self.status_text.insert(tk.END, f"\n   • Estrellas analizadas: {route_impact['stars_analyzed']}")
                self.status_text.insert(tk.END, f"\n   • Impacto total en salud: {route_impact['total_health_impact']:+.1f} puntos")
                self.status_text.insert(tk.END, f"\n   • Impacto total en vida: {route_impact['total_life_impact']:+.1f} años")
                self.status_text.insert(tk.END, f"\n   • Riesgo general: {route_impact['overall_risk']}")
                
                # Mostrar estrellas de riesgo si las hay
                if route_impact['risk_stars']:
                    self.status_text.insert(tk.END, f"\n   🚨 Estrellas de riesgo: {len(route_impact['risk_stars'])}")
                    for risk_star in route_impact['risk_stars'][:3]:  # Mostrar solo las primeras 3
                        self.status_text.insert(tk.END, f"\n     - {risk_star['star']} ({risk_star['risk']})")
                
                self.status_text.insert(tk.END, "\n💡 Los impactos se aplicarán en futuros cálculos de rutas.")
                
                # Mensaje informativo
                messagebox.showinfo("Impactos Configurados", 
                    f"Se han configurado exitosamente los impactos de investigación.\n\n"
                    f"Resumen:\n"
                    f"• Estrellas analizadas: {route_impact['stars_analyzed']}\n"
                    f"• Impacto en salud: {route_impact['total_health_impact']:+.1f} puntos\n"
                    f"• Impacto en vida: {route_impact['total_life_impact']:+.1f} años\n"
                    f"• Riesgo general: {route_impact['overall_risk']}\n\n"
                    f"Use 'Calcular Rutas' para ver el impacto en las rutas.")
                
            else:
                self.status_text.insert(tk.END, "\n❌ Validación de impactos cancelada")
            
            self.status_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir validador de impactos: {str(e)}")
            self.status_text.insert(tk.END, f"\n❌ Error: {str(e)}")
            self.status_text.see(tk.END)
    
    def analyze_next_travel(self):
        """Analiza el costo de vida del próximo viaje planificado incluyendo saltos hipergigantes."""
        try:
            if not self.current_path or len(self.current_path) < 2:
                messagebox.showinfo("Sin Ruta", 
                                  "Primero calcule una ruta para analizar su costo de vida.")
                return
            
            # Verificar saltos hipergigantes en la ruta
            hypergiant_jumps_needed = []
            total_distance = 0
            route_description = f"{self.current_path[0].label}"
            
            for i in range(len(self.current_path) - 1):
                from_star = self.current_path[i]
                to_star = self.current_path[i + 1]
                
                # Verificar si este segmento requiere salto hipergigante
                if self.hypergiant_system.requires_hypergiant_jump(from_star, to_star):
                    from_constellation = self.hypergiant_system.get_star_constellation(from_star)
                    to_constellation = self.hypergiant_system.get_star_constellation(to_star)
                    hypergiant_jumps_needed.append({
                        'from': from_star.label,
                        'to': to_star.label,
                        'from_constellation': from_constellation,
                        'to_constellation': to_constellation
                    })
                
                # Buscar distancia de la ruta
                for route in self.space_map.routes:
                    if ((route.from_star == from_star and route.to_star == to_star) or
                        (route.to_star == from_star and route.from_star == to_star)):
                        total_distance += route.distance
                        break
                
                route_description += f" → {to_star.label}"
            
            # Si hay saltos hipergigantes necesarios, mostrar advertencia
            if hypergiant_jumps_needed:
                message = "🌌 SALTOS HIPERGIGANTES REQUERIDOS EN LA RUTA\n\n"
                message += "Los siguientes segmentos requieren saltos hipergigantes:\n\n"
                
                for jump in hypergiant_jumps_needed:
                    message += f"• {jump['from']} → {jump['to']}\n"
                    message += f"  ({jump['from_constellation']} → {jump['to_constellation']})\n\n"
                
                message += "Beneficios por cada salto hipergigante:\n"
                message += "⚡ +50% energía actual\n"
                message += "🌱 x2 pasto en bodega\n\n"
                message += "¿Continuar con análisis estándar?"
                
                response = messagebox.askyesno("Saltos Hipergigantes Detectados", message)
                if not response:
                    return
            
            # Mostrar análisis de viaje
            self.travel_analyzer.show_travel_preview(total_distance, route_description)
            
            # Agregar información sobre saltos hipergigantes al análisis
            if hypergiant_jumps_needed:
                self.status_text.insert(tk.END, f"\n🌌 SALTOS HIPERGIGANTES NECESARIOS: {len(hypergiant_jumps_needed)}")
                for jump in hypergiant_jumps_needed:
                    self.status_text.insert(tk.END, f"\n  • {jump['from']} → {jump['to']} (cambio de constelación)")
                self.status_text.see(tk.END)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al analizar viaje: {str(e)}")
    
    def demo_countdown(self):
        """Demuestra el contador decremental con un viaje simulado."""
        try:
            # Simular un viaje corto para ver el efecto countdown
            demo_distance = 50  # 33 años de vida con warp_factor 1.5
            
            response = messagebox.askyesno("Demo Countdown", 
                f"🎮 DEMO: Simular viaje con countdown en tiempo real\n\n"
                f"📏 Distancia: {demo_distance} unidades\n"
                f"⏰ Costo de vida: ~{demo_distance/1.5:.1f} años\n"
                f"🕐 Duración del demo: ~{demo_distance/1.5:.0f} segundos\n\n"
                f"El contador decrementará visualmente y emitirá sonido si llega a 0.\n\n"
                f"¿Iniciar demostración?")
            
            if response:
                # Activar countdown acelerado en el widget
                if hasattr(self, 'life_status_widget'):
                    self.life_status_widget.simulate_travel_countdown(demo_distance)
                    
                    # Mostrar mensaje en el status
                    self.status_text.insert(tk.END, f"\n🎮 DEMO COUNTDOWN INICIADO:")
                    self.status_text.insert(tk.END, f"\n   Observe el contador decremental en tiempo real")
                    self.status_text.insert(tk.END, f"\n   ⏰ Costo de vida: {demo_distance/1.5:.1f} años")
                    self.status_text.see(tk.END)
                else:
                    messagebox.showwarning("Widget no disponible", 
                                         "El widget de vida no está inicializado")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en demo countdown: {str(e)}")
    
    def check_hypergiant_requirements(self, from_star, to_star):
        """
        Verifica si un viaje requiere salto hipergigante y maneja el proceso.
        
        Args:
            from_star: Estrella de origen
            to_star: Estrella de destino
            
        Returns:
            bool: True si se procesó un salto hipergigante, False si es viaje normal
        """
        if self.hypergiant_system.requires_hypergiant_jump(from_star, to_star):
            # Mostrar información sobre el salto requerido
            from_constellation = self.hypergiant_system.get_star_constellation(from_star)
            to_constellation = self.hypergiant_system.get_star_constellation(to_star)
            
            message = (f"🌌 SALTO HIPERGIGANTE REQUERIDO\n\n"
                      f"📍 Origen: {from_star.label} ({from_constellation})\n"
                      f"🎯 Destino: {to_star.label} ({to_constellation})\n\n"
                      f"Para viajar entre constelaciones diferentes,\n"
                      f"debe usar una estrella hipergigante.\n\n"
                      f"Beneficios del salto hipergigante:\n"
                      f"⚡ +50% energía actual\n"
                      f"🌱 x2 pasto en bodega\n\n"
                      f"¿Abrir planificador de saltos?")
            
            response = messagebox.askyesno("Salto Hipergigante Requerido", message)
            
            if response:
                return self.hypergiant_gui.show_jump_planner(from_star, to_star)
            else:
                self.status_text.insert(tk.END, f"\n❌ Salto hipergigante cancelado por el usuario")
                self.status_text.see(tk.END)
                return True  # Procesado (aunque cancelado)
        
        return False  # No requiere salto hipergigante
    
    def _register_active_journey(self, path, journey_type: str = "unknown"):
        """Registra un viaje activo para análisis de impacto de cometas."""
        if self.comet_impact_manager and path and len(path) > 1:
            self.comet_impact_manager.register_active_journey(path, 0, journey_type)
    
    def _get_comet_impact_manager(self):
        """Obtiene o inicializa el gestor de impacto de cometas."""
        if not self.comet_impact_manager:
            from src.comet_impact_system import CometImpactManager
            self.comet_impact_manager = CometImpactManager(self.space_map)
        return self.comet_impact_manager
    
    def get_alternative_routes(self, origin_id: str, destination_id: str):
        """Obtiene rutas alternativas entre dos puntos."""
        manager = self._get_comet_impact_manager()
        return manager.get_current_alternatives(origin_id, destination_id)


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = GalaxiasGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
