"""
Graphical User Interface for the Galaxias space route simulation.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
from typing import Optional
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.models import SpaceMap, SpaceshipDonkey, Comet, Star
from src.route_calculator import RouteCalculator
from src.visualizer import SpaceVisualizer


class GalaxiasGUI:
    """Main GUI application for Galaxias space route simulation."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Galaxias - Sistema de Rutas Espaciales")
        self.root.geometry("1400x900")
        self.root.configure(bg='#000033')
        
        # Load configuration
        with open('data/spaceship_config.json', 'r') as f:
            self.config = json.load(f)
        
        # Initialize space map
        self.space_map = SpaceMap('data/constellations.json')
        
        # Initialize spaceship donkey
        ship_config = self.config['spaceship_donkey']
        self.donkey = SpaceshipDonkey(
            name=ship_config['name'],
            health=ship_config['initial_health'],
            fuel=ship_config['initial_fuel'],
            food=ship_config['initial_food'],
            oxygen=ship_config['initial_oxygen']
        )
        
        # Initialize calculator and visualizer
        self.calculator = RouteCalculator(self.space_map, self.config)
        self.visualizer = SpaceVisualizer(self.space_map)
        
        # Current path
        self.current_path = None
        self.current_path_stats = None
        
        # Setup UI
        self.setup_ui()
        
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
        title = tk.Label(left_panel, text="🫏 Galaxias 🚀", 
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
        star_names = [f"{s.name} ({s.id})" for s in self.space_map.get_all_stars_list()]
        self.start_combo = ttk.Combobox(route_frame, textvariable=self.start_star_var,
                                       values=star_names, state='readonly', width=25)
        self.start_combo.pack(padx=5, pady=5)
        if star_names:
            self.start_combo.current(0)
        
        # End star selection
        tk.Label(route_frame, text="Estrella Destino:", 
                bg='#000066', fg='white').pack(anchor=tk.W, padx=5)
        
        self.end_star_var = tk.StringVar()
        self.end_combo = ttk.Combobox(route_frame, textvariable=self.end_star_var,
                                     values=star_names, state='readonly', width=25)
        self.end_combo.pack(padx=5, pady=5)
        if len(star_names) > 1:
            self.end_combo.current(1)
        
        # Calculate route button
        tk.Button(route_frame, text="Calcular Ruta Óptima",
                 command=self.calculate_route,
                 bg='#4444FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=10)
        
        # Travel button
        self.travel_button = tk.Button(route_frame, text="Iniciar Viaje",
                                       command=self.start_journey,
                                       bg='#44FF44', fg='black', 
                                       font=('Arial', 10, 'bold'),
                                       relief=tk.RAISED, borderwidth=2,
                                       state=tk.DISABLED)
        self.travel_button.pack(pady=5)
        
        # Spaceship Status Section
        status_frame = tk.LabelFrame(left_panel, text="Estado del Burro Astronauta",
                                    font=('Arial', 12, 'bold'),
                                    bg='#000066', fg='white',
                                    relief=tk.GROOVE, borderwidth=2)
        status_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=8, width=30,
                                                     bg='#000033', fg='white',
                                                     font=('Courier', 9))
        self.status_text.pack(padx=5, pady=5)
        
        # Refuel button
        tk.Button(status_frame, text="Recargar Recursos",
                 command=self.refuel_donkey,
                 bg='#FFAA44', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        # Comet Management Section
        comet_frame = tk.LabelFrame(left_panel, text="Gestión de Cometas",
                                   font=('Arial', 12, 'bold'),
                                   bg='#000066', fg='white',
                                   relief=tk.GROOVE, borderwidth=2)
        comet_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        tk.Label(comet_frame, text="Nombre del Cometa:", 
                bg='#000066', fg='white').pack(anchor=tk.W, padx=5, pady=(5,0))
        
        self.comet_name_entry = tk.Entry(comet_frame, width=25, bg='#000033', fg='white')
        self.comet_name_entry.pack(padx=5, pady=5)
        
        tk.Label(comet_frame, text="Ruta a Bloquear (desde_id,hasta_id):", 
                bg='#000066', fg='white').pack(anchor=tk.W, padx=5)
        
        self.comet_route_entry = tk.Entry(comet_frame, width=25, bg='#000033', fg='white')
        self.comet_route_entry.pack(padx=5, pady=5)
        
        tk.Button(comet_frame, text="Agregar Cometa",
                 command=self.add_comet,
                 bg='#FF4444', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        tk.Button(comet_frame, text="Remover Cometa",
                 command=self.remove_comet,
                 bg='#44FFFF', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        # Scientific Parameters Section
        params_frame = tk.LabelFrame(left_panel, text="Parámetros Científicos",
                                    font=('Arial', 12, 'bold'),
                                    bg='#000066', fg='white',
                                    relief=tk.GROOVE, borderwidth=2)
        params_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        tk.Button(params_frame, text="Ver/Modificar Parámetros",
                 command=self.show_parameters,
                 bg='#FF44FF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=10)
        
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
        # Format is "Name (id)"
        start = combo_text.rfind('(')
        end = combo_text.rfind(')')
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
        
        # Update info text
        info = f"""
RUTA CALCULADA
{'='*60}
Origen: {start_star.name}
Destino: {end_star.name}
Costo Total: {cost:.2f}

Estadísticas:
- Distancia Total: {self.current_path_stats['total_distance']} unidades
- Saltos: {self.current_path_stats['num_jumps']}
- Peligro Total: {self.current_path_stats['total_danger']}

Recursos Necesarios:
- Combustible: {self.current_path_stats['total_fuel_needed']}
- Comida: {self.current_path_stats['total_food_needed']}
- Oxígeno: {self.current_path_stats['total_oxygen_needed']}
- Pérdida de Salud Estimada: {self.current_path_stats['estimated_health_loss']}

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
    
    def start_journey(self):
        """Start the journey along the calculated path."""
        if not self.current_path or len(self.current_path) < 2:
            messagebox.showerror("Error", "Primero calcule una ruta")
            return
        
        # Check if donkey can make the journey
        if not self.donkey.can_travel(self.current_path_stats['total_distance'], self.config):
            messagebox.showerror("Recursos Insuficientes",
                                "El Burro Astronauta no tiene suficientes recursos para este viaje.\n"
                                "Recargue los recursos antes de continuar.")
            return
        
        # Simulate the journey
        self.donkey.current_location = self.current_path[0]
        self.donkey.journey_history = [self.current_path[0]]
        
        for i in range(len(self.current_path) - 1):
            current_star = self.current_path[i]
            next_star = self.current_path[i + 1]
            
            # Find the route
            route = None
            for r in self.space_map.routes:
                if ((r.from_star == current_star and r.to_star == next_star) or
                    (r.to_star == current_star and r.from_star == next_star)):
                    route = r
                    break
            
            if route:
                self.donkey.consume_resources(route.distance, route.danger_level, self.config)
                self.donkey.current_location = next_star
                self.donkey.journey_history.append(next_star)
                
                if not self.donkey.is_alive():
                    messagebox.showerror("Viaje Fallido",
                                        f"El Burro Astronauta no sobrevivió el viaje.\n"
                                        f"Llegó hasta: {next_star.name}")
                    break
        
        # Update displays
        self.update_status_display()
        self.update_visualization()
        
        if self.donkey.is_alive():
            messagebox.showinfo("Viaje Completado",
                               f"¡Viaje exitoso!\n"
                               f"El Burro Astronauta llegó a {self.donkey.current_location.name}\n"
                               f"Salud restante: {self.donkey.health:.1f}")
        
        # Reset path
        self.current_path = None
        self.travel_button.config(state=tk.DISABLED)
    
    def refuel_donkey(self):
        """Refuel the spaceship donkey."""
        self.donkey.refuel()
        self.update_status_display()
        messagebox.showinfo("Recarga Completada", "Recursos recargados exitosamente")
    
    def add_comet(self):
        """Add a comet to block a route."""
        comet_name = self.comet_name_entry.get().strip()
        route_spec = self.comet_route_entry.get().strip()
        
        if not comet_name or not route_spec:
            messagebox.showerror("Error", "Ingrese nombre del cometa y ruta a bloquear")
            return
        
        # Parse route specification
        try:
            from_id, to_id = route_spec.split(',')
            from_id = from_id.strip()
            to_id = to_id.strip()
        except ValueError:
            messagebox.showerror("Error", "Formato de ruta inválido. Use: desde_id,hasta_id")
            return
        
        # Create and add comet
        comet = Comet(name=comet_name, blocked_routes=[(from_id, to_id)])
        self.space_map.add_comet(comet)
        
        self.update_visualization()
        messagebox.showinfo("Cometa Agregado", 
                           f"Cometa '{comet_name}' agregado.\n"
                           f"Ruta bloqueada: {from_id} ↔ {to_id}")
        
        # Clear entries
        self.comet_name_entry.delete(0, tk.END)
        self.comet_route_entry.delete(0, tk.END)
    
    def remove_comet(self):
        """Remove a comet."""
        comet_name = self.comet_name_entry.get().strip()
        
        if not comet_name:
            messagebox.showerror("Error", "Ingrese el nombre del cometa a remover")
            return
        
        self.space_map.remove_comet(comet_name)
        self.update_visualization()
        messagebox.showinfo("Cometa Removido", f"Cometa '{comet_name}' removido")
        
        self.comet_name_entry.delete(0, tk.END)
    
    def show_parameters(self):
        """Show and allow editing scientific parameters."""
        param_window = tk.Toplevel(self.root)
        param_window.title("Parámetros Científicos")
        param_window.geometry("500x400")
        param_window.configure(bg='#000066')
        
        tk.Label(param_window, text="Parámetros Científicos",
                font=('Arial', 14, 'bold'),
                bg='#000066', fg='white').pack(pady=10)
        
        # Display parameters
        params_text = scrolledtext.ScrolledText(param_window, height=15, width=50,
                                               bg='#000033', fg='white',
                                               font=('Courier', 10))
        params_text.pack(padx=10, pady=10)
        
        params_str = json.dumps(self.config, indent=2)
        params_text.insert(1.0, params_str)
        
        tk.Button(param_window, text="Cerrar",
                 command=param_window.destroy,
                 bg='#4444FF', fg='white', font=('Arial', 10, 'bold')).pack(pady=10)
    
    def generate_report(self):
        """Generate visual report."""
        if not self.current_path_stats:
            # Use empty stats
            self.current_path_stats = self.calculator.calculate_path_stats([])
        
        self.visualizer.plot_journey_report(
            self.donkey,
            self.current_path_stats,
            save_path='assets/journey_report.png',
            show=True
        )
    
    def update_status_display(self):
        """Update the status text display."""
        status = self.donkey.get_status()
        
        status_str = f"""
{'='*30}
BURRO ASTRONAUTA
{'='*30}
Nombre: {status['name']}
Ubicación: {status['location']}

RECURSOS:
  Salud:       {status['health']:.1f} / 100
  Combustible: {status['fuel']:.1f}
  Comida:      {status['food']:.1f}
  Oxígeno:     {status['oxygen']:.1f}

Viajes:        {status['journey_length']}
Estado:        {'✅ Vivo' if self.donkey.is_alive() else '❌ Muerto'}
        """
        
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, status_str)
    
    def update_visualization(self):
        """Update the space map visualization."""
        # Clear previous canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Create new figure
        fig = self.visualizer.plot_space_map(
            highlight_path=self.current_path,
            donkey_location=self.donkey.current_location,
            show=False
        )
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.close(fig)


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = GalaxiasGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
