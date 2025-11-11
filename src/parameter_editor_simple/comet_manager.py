"""
Gestión de cometas integrada al panel científico.
Módulo para agregar/remover cometas que bloquean rutas espaciales.
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import List, Tuple, Callable
from ..core import Comet
from ..core.comet_impact_system import CometImpactManager, RouteImpactResult


class CometManager:
    """Gestor de cometas para el panel científico."""
    
    def __init__(self, space_map, update_callback: Callable = None):
        self.space_map = space_map
        self.update_callback = update_callback  # Callback para actualizar visualización
        self.comet_list_var = None  # Se inicializa en create_ui()
        
        # Sistema de análisis de impacto (puede ser reemplazado externamente)
        self.comet_impact_manager = None  # Se inicializa en create_ui o externamente
        
    def create_ui(self, parent_frame):
        """Crea la interfaz de gestión de cometas."""
        # Inicializar variables Tkinter
        self.comet_list_var = tk.StringVar()
        
        # Inicializar impact_manager si no se ha hecho externamente
        if not self.comet_impact_manager:
            self.comet_impact_manager = CometImpactManager(self.space_map)
            self.comet_impact_manager.add_impact_listener(self._handle_route_impact)
        
        main_frame = tk.LabelFrame(parent_frame, text="🌌 Gestión de Cometas",
                                  font=('Arial', 12, 'bold'),
                                  bg='#001122', fg='white',
                                  relief=tk.GROOVE, borderwidth=2)
        main_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Frame superior para controles
        control_frame = tk.Frame(main_frame, bg='#001122')
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Columna izquierda - Agregar cometas
        left_col = tk.Frame(control_frame, bg='#001122')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(left_col, text="Nuevo Cometa:", 
                bg='#001122', fg='white', font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Nombre del cometa
        tk.Label(left_col, text="Nombre:", bg='#001122', fg='white').pack(anchor=tk.W, pady=(5,0))
        self.comet_name_entry = tk.Entry(left_col, width=20, bg='#000033', fg='white', 
                                        font=('Arial', 9))
        self.comet_name_entry.pack(fill=tk.X, pady=(2,5))
        
        # Ruta a bloquear
        tk.Label(left_col, text="Ruta a Bloquear:", bg='#001122', fg='white').pack(anchor=tk.W)
        
        route_frame = tk.Frame(left_col, bg='#001122')
        route_frame.pack(fill=tk.X, pady=(2,5))
        
        self.from_star_var = tk.StringVar()
        self.to_star_var = tk.StringVar()
        
        # Combos para seleccionar estrellas
        star_ids = [star.id for star in self.space_map.get_all_stars_list()]
        star_labels = [f"{star.id} ({star.label})" for star in self.space_map.get_all_stars_list()]
        
        tk.Label(route_frame, text="Desde:", bg='#001122', fg='white', font=('Arial', 8)).pack(side=tk.LEFT)
        self.from_combo = ttk.Combobox(route_frame, textvariable=self.from_star_var,
                                      values=star_labels, state='readonly', width=12, font=('Arial', 8))
        self.from_combo.pack(side=tk.LEFT, padx=2)
        
        tk.Label(route_frame, text="→", bg='#001122', fg='yellow', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=2)
        
        tk.Label(route_frame, text="Hasta:", bg='#001122', fg='white', font=('Arial', 8)).pack(side=tk.LEFT)
        self.to_combo = ttk.Combobox(route_frame, textvariable=self.to_star_var,
                                    values=star_labels, state='readonly', width=12, font=('Arial', 8))
        self.to_combo.pack(side=tk.LEFT, padx=2)
        
        # Botones de acción
        button_frame = tk.Frame(left_col, bg='#001122')
        button_frame.pack(fill=tk.X, pady=(5,0))
        
        tk.Button(button_frame, text="➕ Agregar Cometa",
                 command=self.add_comet,
                 bg='#FF4444', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=1).pack(side=tk.LEFT, padx=(0,5))
        
        tk.Button(button_frame, text="🗑️ Remover Seleccionado",
                 command=self.remove_selected_comet,
                 bg='#44AAFF', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=1).pack(side=tk.LEFT)
        
        # Columna derecha - Lista de cometas activos
        right_col = tk.Frame(control_frame, bg='#001122')
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_col, text="Cometas Activos:", 
                bg='#001122', fg='white', font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Lista de cometas activos
        list_frame = tk.Frame(right_col, bg='#001122')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(5,0))
        
        self.comet_listbox = tk.Listbox(list_frame, height=6,
                                       bg='#000033', fg='white', 
                                       font=('Courier', 9),
                                       selectmode=tk.SINGLE)
        self.comet_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar para la lista
        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.comet_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.comet_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame inferior para información adicional
        info_frame = tk.Frame(main_frame, bg='#001122')
        info_frame.pack(fill=tk.X, padx=10, pady=(0,10))
        
        tk.Label(info_frame, text="ℹ️ Los cometas bloquean rutas bidireccionales. "
                                 "Una vez agregado, el cometa impedirá el viaje en ambas direcciones.",
                bg='#001122', fg='#AAAAAA', font=('Arial', 8)).pack(anchor=tk.W)
        
        # Cargar cometas existentes
        self.refresh_comet_list()
        
        return main_frame
    
    def extract_star_id(self, combo_text: str) -> str:
        """Extrae el ID de estrella del texto del combo."""
        if not combo_text:
            return ""
        # Formato: "id (label)"
        if " (" in combo_text:
            return combo_text.split(" (")[0]
        return combo_text
    
    def add_comet(self):
        """Agrega un nuevo cometa."""
        comet_name = self.comet_name_entry.get().strip()
        from_text = self.from_star_var.get()
        to_text = self.to_star_var.get()
        
        if not comet_name:
            messagebox.showerror("Error", "Ingrese un nombre para el cometa")
            return
        
        if not from_text or not to_text:
            messagebox.showerror("Error", "Seleccione las estrellas de origen y destino")
            return
        
        from_id = self.extract_star_id(from_text)
        to_id = self.extract_star_id(to_text)
        
        if from_id == to_id:
            messagebox.showerror("Error", "Las estrellas de origen y destino deben ser diferentes")
            return
        
        # Verificar que las estrellas existen
        if not self.space_map.get_star(from_id) or not self.space_map.get_star(to_id):
            messagebox.showerror("Error", "Una o ambas estrellas no existen")
            return
        
        # Verificar si ya existe un cometa con ese nombre
        for existing_comet in self.space_map.comets:
            if existing_comet.name.lower() == comet_name.lower():
                messagebox.showerror("Error", f"Ya existe un cometa con el nombre '{comet_name}'")
                return
        
        # Crear y agregar cometa
        comet = Comet(name=comet_name, blocked_routes=[(from_id, to_id)])
        
        # Analizar impacto ANTES de agregar el cometa
        impact_result = self.comet_impact_manager.analyze_comet_impact(comet)
        
        # Agregar cometa al mapa
        self.space_map.add_comet(comet)
        
        # Actualizar interfaz
        self.refresh_comet_list()
        self.clear_inputs()
        
        # Callback para actualizar visualización
        if self.update_callback:
            self.update_callback()
        
        # Mostrar resultado con información de impacto
        message_parts = [
            f"✅ Cometa '{comet_name}' agregado exitosamente.",
            f"Ruta bloqueada: {from_id} ↔ {to_id}",
            f"Tipo: Bloqueo bidireccional"
        ]
        
        if impact_result.path_invalidated:
            message_parts.append("\n⚠️ IMPACTO EN RUTAS:")
            message_parts.append(impact_result.impact_summary)
            
            if impact_result.alternative_routes:
                message_parts.append(f"\n🔄 {len(impact_result.alternative_routes)} rutas alternativas disponibles")
                # Mostrar las primeras 2 alternativas
                for i, alt_route in enumerate(impact_result.alternative_routes[:2]):
                    route_str = " → ".join([star.label for star in alt_route])
                    message_parts.append(f"   Alternativa {i+1}: {route_str}")
        else:
            message_parts.append("\n✅ Sin impacto en rutas activas")
        
        messagebox.showinfo("Cometa Agregado", "\n".join(message_parts))
    
    def remove_selected_comet(self):
        """Remueve el cometa seleccionado."""
        selected_indices = self.comet_listbox.curselection()
        
        if not selected_indices:
            messagebox.showerror("Error", "Seleccione un cometa de la lista para remover")
            return
        
        selected_index = selected_indices[0]
        comet_info = self.comet_listbox.get(selected_index)
        
        # Extraer nombre del cometa del formato de la lista
        # Formato: "Nombre: ruta info"
        comet_name = comet_info.split(":")[0].strip()
        
        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar Eliminación", 
                                     f"¿Está seguro de remover el cometa '{comet_name}'?\n\n"
                                     f"Se desbloquearán todas las rutas que está impidiendo.")
        
        if confirm:
            self.space_map.remove_comet(comet_name)
            self.refresh_comet_list()
            
            # Callback para actualizar visualización
            if self.update_callback:
                self.update_callback()
            
            messagebox.showinfo("Cometa Removido", 
                               f"❌ Cometa '{comet_name}' removido exitosamente.\n"
                               f"Las rutas han sido desbloqueadas.")
    
    def refresh_comet_list(self):
        """Actualiza la lista de cometas activos."""
        self.comet_listbox.delete(0, tk.END)
        
        if not self.space_map.comets:
            self.comet_listbox.insert(0, "--- No hay cometas activos ---")
            return
        
        for comet in self.space_map.comets:
            routes_info = []
            for from_id, to_id in comet.blocked_routes:
                from_star = self.space_map.get_star(from_id)
                to_star = self.space_map.get_star(to_id)
                from_label = from_star.label if from_star else from_id
                to_label = to_star.label if to_star else to_id
                routes_info.append(f"{from_id}({from_label}) ↔ {to_id}({to_label})")
            
            routes_text = ", ".join(routes_info)
            display_text = f"{comet.name}: {routes_text}"
            
            self.comet_listbox.insert(tk.END, display_text)
    
    def clear_inputs(self):
        """Limpia los campos de entrada."""
        self.comet_name_entry.delete(0, tk.END)
        self.from_star_var.set("")
        self.to_star_var.set("")
    
    def get_comet_summary(self) -> dict:
        """Retorna un resumen del estado actual de cometas."""
        return {
            'total_comets': len(self.space_map.comets),
            'blocked_routes': sum(len(comet.blocked_routes) for comet in self.space_map.comets),
            'comet_names': [comet.name for comet in self.space_map.comets]
        }
    
    def register_active_journey(self, planned_path: List, current_position: int = 0, 
                               journey_type: str = "unknown") -> None:
        """Registra un viaje activo que puede ser afectado por cometas."""
        if self.comet_impact_manager:
            self.comet_impact_manager.register_active_journey(planned_path, current_position, journey_type)
    
    def get_alternative_routes(self, origin_id: str, destination_id: str) -> List[List]:
        """Obtiene rutas alternativas entre dos puntos."""
        if self.comet_impact_manager:
            return self.comet_impact_manager.get_current_alternatives(origin_id, destination_id)
        return []
    
    def clear_active_journeys(self) -> None:
        """Limpia todos los viajes activos registrados."""
        if self.comet_impact_manager:
            self.comet_impact_manager.clear_active_journeys()
    
    def _handle_route_impact(self, impact_result: RouteImpactResult) -> None:
        """Maneja el impacto de cometas en rutas (callback interno)."""
        # Este método es llamado automáticamente cuando se detecta impacto
        # Aquí se pueden agregar acciones adicionales como logs, notificaciones, etc.
        pass