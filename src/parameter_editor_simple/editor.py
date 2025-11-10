"""
Editor principal de parámetros de investigación - Versión simplificada.
Código organizado en módulos para mayor legibilidad manteniendo la funcionalidad original.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
import json

from .models import ResearchParameters
from .presets import PresetManager
from .star_config import StarConfigManager
from .preview import PreviewGenerator


class ResearchParameterEditor:
    """Editor gráfico para parámetros de investigación."""
    
    def __init__(self, parent, space_map, initial_params: Optional[ResearchParameters] = None):
        self.parent = parent
        self.space_map = space_map
        self.result_callback: Optional[Callable] = None
        self.cancelled = True
        
        # Parámetros iniciales
        self.params = initial_params or ResearchParameters()
        
        # Helpers/Managers
        self.preset_manager = PresetManager()
        self.star_manager = StarConfigManager(space_map, self.params)
        self.preview_generator = PreviewGenerator(space_map)
        
        # Crear ventana
        self._create_window()
        self._setup_ui()
        self._load_current_values()
        
        # Eventos
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def _create_window(self):
        """Crea y configura la ventana principal."""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔬 Editor de Parámetros de Investigación")
        self.window.geometry("800x600")
        self.window.configure(bg='#001122')
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"800x600+{x}+{y}")
    
    def _setup_ui(self):
        """Configura la interfaz de usuario principal."""
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#001122')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = tk.Label(main_frame, text="🔬 Configuración de Parámetros de Investigación",
                        font=('Arial', 16, 'bold'), bg='#001122', fg='white')
        title.pack(pady=(0, 20))
        
        # Notebook para pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Crear pestañas
        self._setup_general_params_tab()
        self._setup_star_specific_tab()
        self._setup_presets_tab()
        
        # Botones de acción
        self._setup_action_buttons(main_frame)
    
    def _setup_general_params_tab(self):
        """Configura la pestaña de parámetros generales."""
        frame = tk.Frame(self.notebook, bg='#002244')
        self.notebook.add(frame, text="⚙️ Parámetros Generales")
        
        # Scroll frame
        canvas = tk.Canvas(frame, bg='#002244')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#002244')
        
        scrollable_frame.bind("<Configure>", 
                            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Contenedor de parámetros
        params_frame = tk.LabelFrame(scrollable_frame, text="🔬 Parámetros de Investigación Básicos",
                                   font=('Arial', 12, 'bold'), bg='#002244', fg='white',
                                   relief=tk.GROOVE, borderwidth=2)
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Crear controles de entrada
        self._create_parameter_controls(params_frame)
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_parameter_controls(self, parent):
        """Crea los controles de entrada para parámetros."""
        # Consumo de energía
        energy_frame = tk.Frame(parent, bg='#002244')
        energy_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(energy_frame, text="⚡ Consumo de Energía por Tiempo:",
                bg='#002244', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.energy_rate_var = tk.DoubleVar()
        energy_spinbox = tk.Spinbox(energy_frame, from_=0.1, to=10.0, increment=0.1,
                                   textvariable=self.energy_rate_var, width=10,
                                   font=('Arial', 10))
        energy_spinbox.pack(side=tk.RIGHT, padx=(10, 5))
        
        tk.Label(energy_frame, text="% por unidad de tiempo",
                bg='#002244', fg='#CCCCCC', font=('Arial', 9)).pack(side=tk.RIGHT)
        
        # Porcentaje de tiempo
        time_frame = tk.Frame(parent, bg='#002244')
        time_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(time_frame, text="⏰ Porcentaje Tiempo Investigación:",
                bg='#002244', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.time_percentage_var = tk.DoubleVar()
        time_scale = tk.Scale(time_frame, from_=0.1, to=1.0, resolution=0.05,
                             orient=tk.HORIZONTAL, variable=self.time_percentage_var,
                             bg='#002244', fg='white', font=('Arial', 9))
        time_scale.pack(side=tk.RIGHT, padx=(10, 5))
        
        # Bonus de tiempo de vida
        life_frame = tk.Frame(parent, bg='#002244')
        life_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(life_frame, text="💫 Bonus Tiempo Vida por Investigación:",
                bg='#002244', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.life_bonus_var = tk.DoubleVar()
        life_spinbox = tk.Spinbox(life_frame, from_=-5.0, to=5.0, increment=0.1,
                                 textvariable=self.life_bonus_var, width=10,
                                 font=('Arial', 10))
        life_spinbox.pack(side=tk.RIGHT, padx=(10, 5))
        
        tk.Label(life_frame, text="años por estrella",
                bg='#002244', fg='#CCCCCC', font=('Arial', 9)).pack(side=tk.RIGHT)
        
        # Bonus de energía
        energy_bonus_frame = tk.Frame(parent, bg='#002244')
        energy_bonus_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(energy_bonus_frame, text="🔋 Bonus Energía por Estrella:",
                bg='#002244', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.energy_bonus_var = tk.DoubleVar()
        energy_bonus_spinbox = tk.Spinbox(energy_bonus_frame, from_=0.0, to=20.0, increment=0.5,
                                         textvariable=self.energy_bonus_var, width=10,
                                         font=('Arial', 10))
        energy_bonus_spinbox.pack(side=tk.RIGHT, padx=(10, 5))
        
        tk.Label(energy_bonus_frame, text="% por estrella investigada",
                bg='#002244', fg='#CCCCCC', font=('Arial', 9)).pack(side=tk.RIGHT)
        
        # Multiplicador de conocimiento
        knowledge_frame = tk.Frame(parent, bg='#002244')
        knowledge_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(knowledge_frame, text="📚 Multiplicador Conocimiento:",
                bg='#002244', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.knowledge_mult_var = tk.DoubleVar()
        knowledge_spinbox = tk.Spinbox(knowledge_frame, from_=0.5, to=3.0, increment=0.1,
                                      textvariable=self.knowledge_mult_var, width=10,
                                      font=('Arial', 10))
        knowledge_spinbox.pack(side=tk.RIGHT, padx=(10, 5))
        
        tk.Label(knowledge_frame, text="multiplicador",
                bg='#002244', fg='#CCCCCC', font=('Arial', 9)).pack(side=tk.RIGHT)
    
    def _setup_star_specific_tab(self):
        """Configura la pestaña de configuración específica por estrella."""
        frame = tk.Frame(self.notebook, bg='#002244')
        self.notebook.add(frame, text="⭐ Por Estrella")
        
        # Lista de estrellas
        list_frame = tk.Frame(frame, bg='#002244')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(list_frame, text="🌟 Configuración Específica por Estrella",
                font=('Arial', 12, 'bold'), bg='#002244', fg='white').pack(pady=(0, 10))
        
        # Treeview para estrellas
        self._create_star_treeview(list_frame)
        
        # Botones para edición
        self._create_star_action_buttons(frame)
        
        # Cargar estrellas
        self._load_stars_list()
        
        # Bind doble click
        self.star_tree.bind('<Double-1>', lambda e: self._edit_selected_star())
    
    def _create_star_treeview(self, parent):
        """Crea el TreeView para mostrar estrellas."""
        columns = ('id', 'label', 'tipo', 'energy_rate', 'time_bonus', 'energy_bonus')
        self.star_tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        headers = ['ID', 'Estrella', 'Tipo', 'Consumo %', 'Bonus Tiempo', 'Bonus Energía']
        widths = [50, 120, 100, 100, 100, 100]
        
        for col, header, width in zip(columns, headers, widths):
            self.star_tree.heading(col, text=header)
            self.star_tree.column(col, width=width)
        
        # Scrollbar para treeview
        tree_scroll = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.star_tree.yview)
        self.star_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.star_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_star_action_buttons(self, parent):
        """Crea botones de acción para estrellas."""
        button_frame = tk.Frame(parent, bg='#002244')
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(button_frame, text="✏️ Editar Seleccionada",
                 command=self._edit_selected_star,
                 bg='#4488CC', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="🔄 Resetear Seleccionada",
                 command=self._reset_selected_star,
                 bg='#CC8844', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="📋 Aplicar a Todas",
                 command=self._apply_to_all_stars,
                 bg='#8844CC', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
    
    def _setup_presets_tab(self):
        """Configura la pestaña de presets."""
        frame = tk.Frame(self.notebook, bg='#002244')
        self.notebook.add(frame, text="🎯 Presets")
        
        # Frame para botones de preset
        presets_frame = tk.LabelFrame(frame, text="🎯 Configuraciones Predefinidas",
                                     font=('Arial', 12, 'bold'), bg='#002244', fg='white')
        presets_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Crear botones de preset
        self._create_preset_buttons(presets_frame)
        
        # Descripción del preset
        desc_frame = tk.LabelFrame(frame, text="📝 Descripción del Preset",
                                  font=('Arial', 11, 'bold'), bg='#002244', fg='white')
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.preset_desc_text = tk.Text(desc_frame, height=8, bg='#001133', fg='white',
                                       font=('Arial', 9), wrap=tk.WORD)
        self.preset_desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Información inicial
        self.preset_desc_text.insert('1.0', self.preset_manager.get_preset_info_text())
    
    def _create_preset_buttons(self, parent):
        """Crea botones para presets."""
        presets = self.preset_manager.get_presets()
        
        for i, (name, config) in enumerate(presets):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(parent, text=name,
                           command=lambda c=config, n=name: self._apply_preset(n, c),
                           bg='#336699', fg='white', font=('Arial', 10, 'bold'),
                           relief=tk.RAISED, borderwidth=2, width=25)
            btn.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
        
        # Configurar grid weights
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
    
    def _setup_action_buttons(self, parent):
        """Crea botones de acción principales."""
        button_frame = tk.Frame(parent, bg='#001122')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(button_frame, text="❌ Cancelar",
                 command=self.on_cancel,
                 bg='#CC4444', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="🔄 Resetear",
                 command=self._reset_to_defaults,
                 bg='#FFAA44', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="👁️ Vista Previa",
                 command=self._preview_changes,
                 bg='#44AAFF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="✅ Confirmar y Calcular",
                 command=self._confirm_changes,
                 bg='#44CC44', fg='black', font=('Arial', 12, 'bold'),
                 relief=tk.RAISED, borderwidth=3).pack(side=tk.RIGHT)
    
    # Métodos de datos y lógica
    def _load_current_values(self):
        """Carga los valores actuales en los controles."""
        self.energy_rate_var.set(self.params.energy_consumption_rate)
        self.time_percentage_var.set(self.params.time_percentage)
        self.life_bonus_var.set(self.params.life_time_bonus)
        self.energy_bonus_var.set(self.params.energy_bonus_per_star)
        self.knowledge_mult_var.set(self.params.knowledge_multiplier)
    
    def _load_stars_list(self):
        """Carga la lista de estrellas en el treeview."""
        # Limpiar tabla
        for item in self.star_tree.get_children():
            self.star_tree.delete(item)
        
        # Obtener datos de estrellas y agregarlos
        stars_data = self.star_manager.get_star_display_data()
        for star_data in stars_data:
            self.star_tree.insert('', 'end', values=star_data)
    
    def _collect_current_values(self):
        """Recolecta los valores actuales de la UI."""
        self.params.energy_consumption_rate = self.energy_rate_var.get()
        self.params.time_percentage = self.time_percentage_var.get()
        self.params.life_time_bonus = self.life_bonus_var.get()
        self.params.energy_bonus_per_star = self.energy_bonus_var.get()
        self.params.knowledge_multiplier = self.knowledge_mult_var.get()
    
    # Métodos de acción
    def _edit_selected_star(self):
        """Edita la configuración de la estrella seleccionada."""
        selection = self.star_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una estrella para editar")
            return
        
        item = self.star_tree.item(selection[0])
        star_id = item['values'][0]
        star_label = item['values'][1]
        
        # Crear diálogo de edición
        self._create_star_edit_dialog(star_id, star_label)
    
    def _create_star_edit_dialog(self, star_id: str, star_label: str):
        """Crea un diálogo para editar configuración específica de estrella."""
        dialog = tk.Toplevel(self.window)
        dialog.title(f"✏️ Editar {star_label} (ID: {star_id})")
        dialog.geometry("400x300")
        dialog.configure(bg='#001122')
        dialog.transient(self.window)
        dialog.grab_set()
        
        # Centrar diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Obtener configuración actual
        current_config = self.star_manager.get_star_config(star_id)
        
        # Variables
        energy_var = tk.DoubleVar(value=current_config['energy_rate'])
        time_var = tk.DoubleVar(value=current_config['time_bonus'])
        energy_bonus_var = tk.DoubleVar(value=current_config['energy_bonus'])
        
        # UI del diálogo
        self._setup_star_dialog_ui(dialog, star_label, energy_var, time_var, energy_bonus_var)
        
        # Funciones de acción
        def save_star_config():
            self.star_manager.save_star_config(star_id, energy_var.get(), 
                                             time_var.get(), energy_bonus_var.get())
            self._load_stars_list()
            dialog.destroy()
        
        def reset_star_config():
            self.star_manager.reset_star_config(star_id)
            self._load_stars_list()
            dialog.destroy()
        
        # Configurar botones
        self._setup_star_dialog_buttons(dialog, save_star_config, reset_star_config)
    
    def _setup_star_dialog_ui(self, dialog, star_label, energy_var, time_var, energy_bonus_var):
        """Configura la UI del diálogo de edición de estrella."""
        main_frame = tk.Frame(dialog, bg='#001122')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text=f"⭐ Configuración para {star_label}",
                font=('Arial', 12, 'bold'), bg='#001122', fg='white').pack(pady=(0, 20))
        
        # Controles de entrada
        controls = [
            ("⚡ Consumo Energía:", energy_var, 0.1, 10.0, 0.1),
            ("💫 Bonus Tiempo:", time_var, -5.0, 5.0, 0.1),
            ("🔋 Bonus Energía:", energy_bonus_var, 0.0, 20.0, 0.5)
        ]
        
        for label_text, var, min_val, max_val, increment in controls:
            frame = tk.Frame(main_frame, bg='#001122')
            frame.pack(fill=tk.X, pady=5)
            
            tk.Label(frame, text=label_text, bg='#001122', fg='white').pack(side=tk.LEFT)
            tk.Spinbox(frame, from_=min_val, to=max_val, increment=increment,
                      textvariable=var, width=10).pack(side=tk.RIGHT)
    
    def _setup_star_dialog_buttons(self, dialog, save_callback, reset_callback):
        """Configura los botones del diálogo."""
        button_frame = tk.Frame(dialog, bg='#001122')
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy,
                 bg='#CC4444', fg='white').pack(side=tk.LEFT)
        tk.Button(button_frame, text="🔄 Resetear", command=reset_callback,
                 bg='#FFAA44', fg='black').pack(side=tk.LEFT, padx=(10, 0))
        tk.Button(button_frame, text="✅ Guardar", command=save_callback,
                 bg='#44CC44', fg='black').pack(side=tk.RIGHT)
    
    def _reset_selected_star(self):
        """Resetea la configuración de la estrella seleccionada."""
        selection = self.star_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una estrella para resetear")
            return
        
        item = self.star_tree.item(selection[0])
        star_id = item['values'][0]
        
        if self.star_manager.reset_star_config(star_id):
            self._load_stars_list()
            messagebox.showinfo("Éxito", f"Configuración reseteada para estrella {star_id}")
        else:
            messagebox.showinfo("Info", "La estrella ya usa configuración por defecto")
    
    def _apply_to_all_stars(self):
        """Aplica la configuración general a todas las estrellas."""
        if messagebox.askyesno("Confirmar", "¿Aplicar configuración general a TODAS las estrellas?"):
            self.star_manager.reset_all_stars()
            self._load_stars_list()
            messagebox.showinfo("Éxito", "Configuración general aplicada a todas las estrellas")
    
    def _apply_preset(self, preset_name: str, config: dict):
        """Aplica una configuración preset."""
        if self.preset_manager.apply_preset_to_params(preset_name, self.params):
            self._load_current_values()
            self._load_stars_list()
            
            # Actualizar descripción
            formatted_text = self.preset_manager.format_preset_applied_text(preset_name, config)
            self.preset_desc_text.delete('1.0', tk.END)
            self.preset_desc_text.insert('1.0', formatted_text)
    
    def _reset_to_defaults(self):
        """Resetea todos los parámetros a valores por defecto."""
        if messagebox.askyesno("Confirmar Reset", "¿Resetear TODOS los parámetros a valores por defecto?"):
            self.params = ResearchParameters()
            self.star_manager.research_params = self.params  # Actualizar referencia
            self._load_current_values()
            self._load_stars_list()
            messagebox.showinfo("Reset Completo", "Todos los parámetros han sido reseteados")
    
    def _preview_changes(self):
        """Muestra una vista previa de los cambios."""
        self._collect_current_values()
        
        preview_window = tk.Toplevel(self.window)
        preview_window.title("👁️ Vista Previa de Configuración")
        preview_window.geometry("600x400")
        preview_window.configure(bg='#001122')
        
        text_widget = tk.Text(preview_window, bg='#001133', fg='white', 
                            font=('Courier', 9), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generar y mostrar preview
        preview_text = self.preview_generator.generate_preview_text(self.params)
        text_widget.insert('1.0', preview_text)
        text_widget.config(state='disabled')
    
    def _confirm_changes(self):
        """Confirma los cambios y cierra el editor."""
        self._collect_current_values()
        self.cancelled = False
        
        if messagebox.askyesno("Confirmar Configuración", 
                              "¿Aplicar esta configuración y recalcular la ruta optimizada?"):
            self.window.destroy()
    
    def on_cancel(self):
        """Maneja la cancelación."""
        if messagebox.askyesno("Cancelar", "¿Descartar todos los cambios?"):
            self.cancelled = True
            self.window.destroy()
    
    def get_parameters(self) -> Optional[ResearchParameters]:
        """Retorna los parámetros configurados o None si se canceló."""
        return None if self.cancelled else self.params