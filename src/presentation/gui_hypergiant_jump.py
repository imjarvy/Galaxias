"""
Interfaz gráfica para el sistema de saltos hipergigantes.
Permite al usuario gestionar saltos entre constelaciones con confirmaciones interactivas.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Optional, List
import json

from ..algorithms.hypergiant_jump import HyperGiantJumpSystem, HyperGiantJumpResult
from ..core import SpaceMap, Star, BurroAstronauta


class HyperGiantJumpGUI:
    """GUI para gestión de saltos hipergigantes."""
    
    def __init__(self, parent: tk.Widget, space_map: SpaceMap, burro: BurroAstronauta):
        self.parent = parent
        self.space_map = space_map
        self.burro = burro
        self.jump_system = HyperGiantJumpSystem(space_map)
        
        # Variables para el salto actual
        self.current_from_star = None
        self.current_to_star = None
        self.selected_hypergiant = None
        self.selected_destination = None
        
        self.window = None
        
    def show_jump_planner(self, from_star: Star, to_star: Star):
        """
        Muestra la ventana de planificación de salto hipergigante.
        
        Args:
            from_star: Estrella de origen
            to_star: Estrella de destino
        """
        self.current_from_star = from_star
        self.current_to_star = to_star
        
        # Verificar si realmente necesita salto hipergigante
        if not self.jump_system.requires_hypergiant_jump(from_star, to_star):
            messagebox.showinfo("No Requerido", 
                              "El destino está en la misma constelación. "
                              "No se requiere salto hipergigante.")
            return False
        
        self._create_jump_window()
        return True
        
    def _create_jump_window(self):
        """Crea la ventana principal del planificador."""
        if self.window and self.window.winfo_exists():
            self.window.destroy()
            
        self.window = tk.Toplevel(self.parent)
        self.window.title("🌌 Planificador de Saltos Hipergigantes")
        self.window.geometry("800x600")
        self.window.configure(bg='#000033')
        
        # Hacer modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Información del viaje
        info_frame = tk.LabelFrame(self.window, text="Información del Viaje",
                                  bg='#000066', fg='white', font=('Arial', 12, 'bold'))
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        from_constellation = self.jump_system.get_star_constellation(self.current_from_star)
        to_constellation = self.jump_system.get_star_constellation(self.current_to_star)
        
        tk.Label(info_frame, 
                text=f"📍 Origen: {self.current_from_star.label} ({from_constellation})",
                bg='#000066', fg='white', font=('Arial', 10)).pack(anchor=tk.W, padx=5, pady=2)
        
        tk.Label(info_frame, 
                text=f"🎯 Destino: {self.current_to_star.label} ({to_constellation})",
                bg='#000066', fg='white', font=('Arial', 10)).pack(anchor=tk.W, padx=5, pady=2)
        
        # Estado actual del burro
        status_frame = tk.LabelFrame(self.window, text="Estado del Burro",
                                    bg='#000066', fg='white', font=('Arial', 12, 'bold'))
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(status_frame,
                text=f"⚡ Energía: {self.burro.current_energy:.1f}%",
                bg='#000066', fg='white', font=('Arial', 10)).pack(anchor=tk.W, padx=5, pady=1)
        
        tk.Label(status_frame,
                text=f"🌱 Pasto: {self.burro.current_pasto:.1f}kg",
                bg='#000066', fg='white', font=('Arial', 10)).pack(anchor=tk.W, padx=5, pady=1)
        
        tk.Label(status_frame,
                text=f"💫 Vida restante: {self.burro.get_remaining_life():.1f} años",
                bg='#000066', fg='white', font=('Arial', 10)).pack(anchor=tk.W, padx=5, pady=1)
        
        # Selección de hipergigante
        self._create_hypergiant_selection(self.window)
        
        # Selección de destino
        self._create_destination_selection(self.window)
        
        # Botones de acción
        self._create_action_buttons(self.window)
        
        # Cargar datos iniciales
        self._update_hypergiant_options()
        
    def _create_hypergiant_selection(self, parent):
        """Crea la sección de selección de hipergigante."""
        hg_frame = tk.LabelFrame(parent, text="🌟 Seleccionar Hipergigante",
                                bg='#000066', fg='white', font=('Arial', 12, 'bold'))
        hg_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Lista de hipergigantes disponibles
        self.hg_listbox = tk.Listbox(hg_frame, height=6, bg='#000033', fg='white',
                                    selectmode=tk.SINGLE, font=('Courier', 9))
        self.hg_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.hg_listbox.bind('<<ListboxSelect>>', self._on_hypergiant_selected)
        
        # Información de la hipergigante seleccionada
        self.hg_info_label = tk.Label(hg_frame, text="Seleccione una hipergigante",
                                     bg='#000066', fg='yellow', font=('Arial', 10))
        self.hg_info_label.pack(pady=5)
        
    def _create_destination_selection(self, parent):
        """Crea la sección de selección de destino."""
        dest_frame = tk.LabelFrame(parent, text="🎯 Seleccionar Destino en Nueva Galaxia",
                                  bg='#000066', fg='white', font=('Arial', 12, 'bold'))
        dest_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Lista de destinos disponibles
        self.dest_listbox = tk.Listbox(dest_frame, height=6, bg='#000033', fg='white',
                                      selectmode=tk.SINGLE, font=('Courier', 9))
        self.dest_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.dest_listbox.bind('<<ListboxSelect>>', self._on_destination_selected)
        
        # Información del destino seleccionado
        self.dest_info_label = tk.Label(dest_frame, text="Seleccione un destino",
                                       bg='#000066', fg='yellow', font=('Arial', 10))
        self.dest_info_label.pack(pady=5)
        
    def _create_action_buttons(self, parent):
        """Crea los botones de acción."""
        button_frame = tk.Frame(parent, bg='#000033')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="🚀 Ejecutar Salto Hipergigante",
                 command=self._execute_jump, bg='#00AA00', fg='white',
                 font=('Arial', 12, 'bold'), relief=tk.RAISED).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="📊 Simular Salto",
                 command=self._simulate_jump, bg='#AAAA00', fg='black',
                 font=('Arial', 12, 'bold'), relief=tk.RAISED).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="❌ Cancelar",
                 command=self._cancel_jump, bg='#AA0000', fg='white',
                 font=('Arial', 12, 'bold'), relief=tk.RAISED).pack(side=tk.RIGHT, padx=5)
        
    def _update_hypergiant_options(self):
        """Actualiza la lista de hipergigantes disponibles."""
        self.hg_listbox.delete(0, tk.END)
        
        accessible_hypergiants = self.jump_system.find_accessible_hypergiants(self.current_from_star)
        
        if not accessible_hypergiants:
            self.hg_listbox.insert(tk.END, "❌ No hay hipergigantes accesibles")
            return
            
        for i, (hypergiant, distance) in enumerate(accessible_hypergiants):
            # Calcular costo energético
            age_factor = max(1.0, (self.burro.current_age - 5) / 10.0)
            energy_cost = int(distance * 0.1 * age_factor)
            
            # Verificar si es factible
            feasible = self.jump_system.can_perform_hypergiant_jump(
                self.burro, hypergiant, distance)
            
            status_icon = "✅" if feasible else "❌"
            
            entry = (f"{status_icon} {hypergiant.label} | "
                    f"Distancia: {distance:.1f} | "
                    f"Energía: -{energy_cost}%")
            
            self.hg_listbox.insert(tk.END, entry)
            
            # Almacenar datos para referencia
            self.hg_listbox.insert(tk.END, f"    ID: {hypergiant.id} | Coordenadas: ({hypergiant.x}, {hypergiant.y})")
        
        # Cargar destinos de la constelación objetivo
        self._update_destination_options()
        
    def _update_destination_options(self):
        """Actualiza la lista de destinos disponibles."""
        self.dest_listbox.delete(0, tk.END)
        
        target_constellation = self.jump_system.get_star_constellation(self.current_to_star)
        destinations = self.jump_system.find_destination_options(target_constellation)
        
        for dest in destinations:
            entry = (f"⭐ {dest.label} | "
                    f"ID: {dest.id} | "
                    f"Coordenadas: ({dest.x}, {dest.y}) | "
                    f"Energía: {dest.amount_of_energy}")
            self.dest_listbox.insert(tk.END, entry)
            
    def _on_hypergiant_selected(self, event):
        """Maneja la selección de una hipergigante."""
        selection = self.hg_listbox.curselection()
        if not selection:
            return
            
        # Los índices pares son las hipergigantes, impares son detalles
        index = selection[0]
        if index % 2 != 0:  # Es una línea de detalle
            return
            
        hg_index = index // 2
        accessible_hypergiants = self.jump_system.find_accessible_hypergiants(self.current_from_star)
        
        if hg_index < len(accessible_hypergiants):
            self.selected_hypergiant, distance = accessible_hypergiants[hg_index]
            
            # Actualizar información
            constellation = self.jump_system.get_star_constellation(self.selected_hypergiant)
            feasible = self.jump_system.can_perform_hypergiant_jump(
                self.burro, self.selected_hypergiant, distance)
            
            info_text = (f"🌟 {self.selected_hypergiant.label} | "
                        f"Constelación: {constellation} | "
                        f"Factible: {'Sí' if feasible else 'No'}")
            
            self.hg_info_label.config(text=info_text, 
                                     fg='lightgreen' if feasible else 'red')
            
    def _on_destination_selected(self, event):
        """Maneja la selección de destino."""
        selection = self.dest_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        target_constellation = self.jump_system.get_star_constellation(self.current_to_star)
        destinations = self.jump_system.find_destination_options(target_constellation)
        
        if index < len(destinations):
            self.selected_destination = destinations[index]
            
            info_text = f"🎯 {self.selected_destination.label} seleccionado como destino"
            self.dest_info_label.config(text=info_text, fg='lightblue')
            
    def _simulate_jump(self):
        """Simula el salto sin ejecutarlo realmente."""
        if not self._validate_selections():
            return
            
        # Crear copia temporal del burro para simulación
        burro_copy = BurroAstronauta(
            name=self.burro.name,
            energia_inicial=self.burro.energia_inicial,
            estado_salud=self.burro.estado_salud,
            pasto=self.burro.pasto,
            start_age=self.burro.start_age,
            death_age=self.burro.death_age
        )
        burro_copy.current_energy = self.burro.current_energy
        burro_copy.current_pasto = self.burro.current_pasto
        burro_copy.current_age = self.burro.current_age
        
        # Calcular distancia
        accessible_hypergiants = self.jump_system.find_accessible_hypergiants(self.current_from_star)
        distance = None
        for hg, dist in accessible_hypergiants:
            if hg.id == self.selected_hypergiant.id:
                distance = dist
                break
                
        if distance is None:
            messagebox.showerror("Error", "No se pudo calcular la distancia")
            return
            
        # Simular salto
        result = self.jump_system.perform_hypergiant_jump(
            burro_copy, self.selected_hypergiant, self.selected_destination, distance)
        
        # Mostrar resultados de simulación
        self._show_jump_results(result, simulation=True)
        
    def _execute_jump(self):
        """Ejecuta el salto hipergigante real."""
        if not self._validate_selections():
            return
            
        # Confirmación final
        response = messagebox.askyesno(
            "Confirmar Salto Hipergigante",
            f"¿Confirmar salto hipergigante?\n\n"
            f"🌟 Hipergigante: {self.selected_hypergiant.label}\n"
            f"🎯 Destino: {self.selected_destination.label}\n\n"
            f"Beneficios:\n"
            f"⚡ +50% energía actual\n"
            f"🌱 x2 pasto en bodega\n\n"
            f"Esta acción no se puede deshacer.")
        
        if not response:
            return
            
        # Calcular distancia
        accessible_hypergiants = self.jump_system.find_accessible_hypergiants(self.current_from_star)
        distance = None
        for hg, dist in accessible_hypergiants:
            if hg.id == self.selected_hypergiant.id:
                distance = dist
                break
                
        if distance is None:
            messagebox.showerror("Error", "No se pudo calcular la distancia")
            return
            
        # Ejecutar salto
        result = self.jump_system.perform_hypergiant_jump(
            self.burro, self.selected_hypergiant, self.selected_destination, distance)
        
        # Mostrar resultados
        self._show_jump_results(result, simulation=False)
        
        if result.success:
            # Cerrar ventana si el salto fue exitoso
            self.window.destroy()
            
    def _validate_selections(self):
        """Valida que se hayan hecho las selecciones necesarias."""
        if not self.selected_hypergiant:
            messagebox.showwarning("Selección Incompleta", 
                                 "Debe seleccionar una hipergigante")
            return False
            
        if not self.selected_destination:
            messagebox.showwarning("Selección Incompleta", 
                                 "Debe seleccionar un destino")
            return False
            
        return True
        
    def _show_jump_results(self, result: HyperGiantJumpResult, simulation: bool = False):
        """Muestra los resultados del salto hipergigante."""
        title = "🎮 Simulación de Salto" if simulation else "🚀 Resultado del Salto"
        
        if result.success:
            message = result.message
            messagebox.showinfo(title, message)
        else:
            messagebox.showerror(title, result.message)
            
    def _cancel_jump(self):
        """Cancela el planificador de salto."""
        self.window.destroy()


# Función utilitaria para integrar con la GUI principal
def integrate_hypergiant_jump_to_gui(gui_instance, space_map: SpaceMap, burro: BurroAstronauta):
    """
    Integra el sistema de saltos hipergigantes a la GUI principal.
    
    Args:
        gui_instance: Instancia de la GUI principal
        space_map: Mapa espacial
        burro: Burro astronauta
    """
    # Crear instancia del sistema de saltos
    jump_gui = HyperGiantJumpGUI(gui_instance.root, space_map, burro)
    
    # Agregar método a la GUI principal
    def check_and_handle_hypergiant_jump(from_star, to_star):
        """Verifica si se necesita salto hipergigante y maneja el proceso."""
        jump_system = HyperGiantJumpSystem(space_map)
        
        if jump_system.requires_hypergiant_jump(from_star, to_star):
            return jump_gui.show_jump_planner(from_star, to_star)
        return False
    
    # Inyectar el método en la GUI principal
    gui_instance.check_hypergiant_jump = check_and_handle_hypergiant_jump
    gui_instance.jump_system = HyperGiantJumpSystem(space_map)
    
    return jump_gui


def main():
    """Función de prueba independiente."""
    import sys
    sys.path.append('.')
    
    # Crear ventana de prueba
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Cargar datos
    space_map = SpaceMap('data/constellations.json')
    burro = space_map.create_burro_astronauta()
    
    # Crear GUI
    jump_gui = HyperGiantJumpGUI(root, space_map, burro)
    
    # Simular salto entre constelaciones (estrella 1 a 13)
    from_star = space_map.get_star("1")
    to_star = space_map.get_star("13")
    
    if from_star and to_star:
        burro.current_location = from_star
        jump_gui.show_jump_planner(from_star, to_star)
        root.mainloop()
    else:
        print("❌ Estrellas no encontradas")


if __name__ == '__main__':
    main()
