"""
Configurador de parámetros de investigación para el sistema de menor gasto.
Permite editar valores de ganancia/pérdida antes del cálculo de ruta.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Optional, Callable
from dataclasses import dataclass
import json


@dataclass
class ResearchParameters:
    """Parámetros configurables para la investigación en estrellas."""
    energy_consumption_rate: float = 2.0  # Energía consumida por unidad de tiempo
    time_percentage: float = 0.5           # Porcentaje del tiempo dedicado a investigación (50%)
    life_time_bonus: float = 0.0           # Bonus/penalty de tiempo de vida por investigación
    energy_bonus_per_star: float = 0.0     # Bonus de energía por estrella investigada
    knowledge_multiplier: float = 1.0      # Multiplicador de conocimiento por tipo de estrella
    custom_star_settings: Dict[str, Dict] = None  # Configuraciones específicas por estrella
    
    def __post_init__(self):
        if self.custom_star_settings is None:
            self.custom_star_settings = {}


class ResearchParameterEditor:
    """Editor gráfico para parámetros de investigación."""
    
    def __init__(self, parent, space_map, initial_params: Optional[ResearchParameters] = None):
        self.parent = parent
        self.space_map = space_map
        self.result_callback: Optional[Callable] = None
        self.cancelled = True
        
        # Parámetros iniciales
        self.params = initial_params or ResearchParameters()
        
        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title("🔬 Editor de Parámetros de Investigación")
        self.window.geometry("800x600")
        self.window.configure(bg='#001122')
        self.window.transient(parent)
        self.window.grab_set()
        
        # Centrar ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"800x600+{x}+{y}")
        
        self.setup_ui()
        self.load_current_values()
        
        # Eventos
        self.window.protocol("WM_DELETE_WINDOW", self.on_cancel)
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Frame principal con scroll
        main_frame = tk.Frame(self.window, bg='#001122')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = tk.Label(main_frame, text="🔬 Configuración de Parámetros de Investigación",
                        font=('Arial', 16, 'bold'), bg='#001122', fg='white')
        title.pack(pady=(0, 20))
        
        # Notebook para organizar parámetros
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Tab 1: Parámetros Generales
        self.setup_general_params_tab()
        
        # Tab 2: Configuración por Estrella
        self.setup_star_specific_tab()
        
        # Tab 3: Presets
        self.setup_presets_tab()
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#001122')
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(button_frame, text="❌ Cancelar",
                 command=self.on_cancel,
                 bg='#CC4444', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="🔄 Resetear",
                 command=self.reset_to_defaults,
                 bg='#FFAA44', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="👁️ Vista Previa",
                 command=self.preview_changes,
                 bg='#44AAFF', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="✅ Confirmar y Calcular",
                 command=self.confirm_changes,
                 bg='#44CC44', fg='black', font=('Arial', 12, 'bold'),
                 relief=tk.RAISED, borderwidth=3).pack(side=tk.RIGHT)
    
    def setup_general_params_tab(self):
        """Configura la pestaña de parámetros generales."""
        frame = tk.Frame(self.notebook, bg='#002244')
        self.notebook.add(frame, text="⚙️ Parámetros Generales")
        
        # Scroll frame
        canvas = tk.Canvas(frame, bg='#002244')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#002244')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Parámetros básicos
        params_frame = tk.LabelFrame(scrollable_frame, text="🔬 Parámetros de Investigación Básicos",
                                   font=('Arial', 12, 'bold'), bg='#002244', fg='white',
                                   relief=tk.GROOVE, borderwidth=2)
        params_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Consumo de energía
        energy_frame = tk.Frame(params_frame, bg='#002244')
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
        time_frame = tk.Frame(params_frame, bg='#002244')
        time_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(time_frame, text="⏰ Porcentaje Tiempo Investigación:",
                bg='#002244', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.time_percentage_var = tk.DoubleVar()
        time_scale = tk.Scale(time_frame, from_=0.1, to=1.0, resolution=0.05,
                             orient=tk.HORIZONTAL, variable=self.time_percentage_var,
                             bg='#002244', fg='white', font=('Arial', 9))
        time_scale.pack(side=tk.RIGHT, padx=(10, 5))
        
        # Bonus de tiempo de vida
        life_frame = tk.Frame(params_frame, bg='#002244')
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
        energy_bonus_frame = tk.Frame(params_frame, bg='#002244')
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
        knowledge_frame = tk.Frame(params_frame, bg='#002244')
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
        
        # Pack canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_star_specific_tab(self):
        """Configura la pestaña de configuración específica por estrella."""
        frame = tk.Frame(self.notebook, bg='#002244')
        self.notebook.add(frame, text="⭐ Por Estrella")
        
        # Lista de estrellas
        list_frame = tk.Frame(frame, bg='#002244')
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tk.Label(list_frame, text="🌟 Configuración Específica por Estrella",
                font=('Arial', 12, 'bold'), bg='#002244', fg='white').pack(pady=(0, 10))
        
        # Treeview para estrellas
        columns = ('id', 'label', 'tipo', 'energy_rate', 'time_bonus', 'energy_bonus')
        self.star_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.star_tree.heading('id', text='ID')
        self.star_tree.heading('label', text='Estrella')
        self.star_tree.heading('tipo', text='Tipo')
        self.star_tree.heading('energy_rate', text='Consumo %')
        self.star_tree.heading('time_bonus', text='Bonus Tiempo')
        self.star_tree.heading('energy_bonus', text='Bonus Energía')
        
        self.star_tree.column('id', width=50)
        self.star_tree.column('label', width=120)
        self.star_tree.column('tipo', width=100)
        self.star_tree.column('energy_rate', width=100)
        self.star_tree.column('time_bonus', width=100)
        self.star_tree.column('energy_bonus', width=100)
        
        # Scrollbar para treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.star_tree.yview)
        self.star_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.star_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Botones para edición
        button_frame = tk.Frame(frame, bg='#002244')
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        tk.Button(button_frame, text="✏️ Editar Seleccionada",
                 command=self.edit_selected_star,
                 bg='#4488CC', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="🔄 Resetear Seleccionada",
                 command=self.reset_selected_star,
                 bg='#CC8844', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="📋 Aplicar a Todas",
                 command=self.apply_to_all_stars,
                 bg='#8844CC', fg='white', font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
        
        # Cargar estrellas
        self.load_stars_list()
        
        # Bind doble click
        self.star_tree.bind('<Double-1>', lambda e: self.edit_selected_star())
    
    def setup_presets_tab(self):
        """Configura la pestaña de presets."""
        frame = tk.Frame(self.notebook, bg='#002244')
        self.notebook.add(frame, text="🎯 Presets")
        
        presets_frame = tk.LabelFrame(frame, text="🎯 Configuraciones Predefinidas",
                                     font=('Arial', 12, 'bold'), bg='#002244', fg='white')
        presets_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Preset buttons
        preset_configs = [
            ("🔬 Investigador Intensivo", {"energy_consumption_rate": 3.0, "time_percentage": 0.7, "energy_bonus_per_star": 5.0}),
            ("⚡ Conservador de Energía", {"energy_consumption_rate": 1.0, "time_percentage": 0.3, "life_time_bonus": 0.5}),
            ("🌟 Explorador Rápido", {"energy_consumption_rate": 1.5, "time_percentage": 0.4, "knowledge_multiplier": 1.5}),
            ("🎯 Equilibrado", {"energy_consumption_rate": 2.0, "time_percentage": 0.5, "energy_bonus_per_star": 2.0}),
            ("💫 Maximizar Conocimiento", {"energy_consumption_rate": 2.5, "time_percentage": 0.8, "knowledge_multiplier": 2.0}),
            ("🚀 Eficiencia Extrema", {"energy_consumption_rate": 0.5, "time_percentage": 0.2, "life_time_bonus": 1.0})
        ]
        
        for i, (name, config) in enumerate(preset_configs):
            row = i // 2
            col = i % 2
            
            btn = tk.Button(presets_frame, text=name,
                           command=lambda c=config: self.apply_preset(c),
                           bg='#336699', fg='white', font=('Arial', 10, 'bold'),
                           relief=tk.RAISED, borderwidth=2, width=25)
            btn.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
        
        # Configurar grid weights
        presets_frame.grid_columnconfigure(0, weight=1)
        presets_frame.grid_columnconfigure(1, weight=1)
        
        # Descripción del preset actual
        desc_frame = tk.LabelFrame(frame, text="📝 Descripción del Preset",
                                  font=('Arial', 11, 'bold'), bg='#002244', fg='white')
        desc_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.preset_desc_text = tk.Text(desc_frame, height=8, bg='#001133', fg='white',
                                       font=('Arial', 9), wrap=tk.WORD)
        self.preset_desc_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Información inicial
        self.preset_desc_text.insert('1.0', 
            "Selecciona un preset para cargar configuraciones predefinidas:\n\n"
            "🔬 Investigador Intensivo: Máximo conocimiento, alto consumo energético\n"
            "⚡ Conservador de Energía: Mínimo consumo, investigación ligera\n"
            "🌟 Explorador Rápido: Balance entre velocidad y conocimiento\n"
            "🎯 Equilibrado: Configuración estándar recomendada\n"
            "💫 Maximizar Conocimiento: Enfoque total en investigación\n"
            "🚀 Eficiencia Extrema: Mínimo tiempo, máxima eficiencia")
    
    def load_current_values(self):
        """Carga los valores actuales en los controles."""
        self.energy_rate_var.set(self.params.energy_consumption_rate)
        self.time_percentage_var.set(self.params.time_percentage)
        self.life_bonus_var.set(self.params.life_time_bonus)
        self.energy_bonus_var.set(self.params.energy_bonus_per_star)
        self.knowledge_mult_var.set(self.params.knowledge_multiplier)
    
    def load_stars_list(self):
        """Carga la lista de estrellas en el treeview."""
        # Limpiar tabla
        for item in self.star_tree.get_children():
            self.star_tree.delete(item)
        
        # Agregar estrellas
        for star in self.space_map.get_all_stars_list():
            star_type = "Hipergigante" if star.hypergiant else "Normal"
            
            # Obtener configuración específica si existe
            star_config = self.params.custom_star_settings.get(star.id, {})
            energy_rate = star_config.get('energy_rate', self.params.energy_consumption_rate)
            time_bonus = star_config.get('time_bonus', self.params.life_time_bonus)
            energy_bonus = star_config.get('energy_bonus', self.params.energy_bonus_per_star)
            
            self.star_tree.insert('', 'end', values=(
                star.id, star.label, star_type,
                f"{energy_rate:.1f}%", f"{time_bonus:+.1f}a", f"{energy_bonus:+.1f}%"
            ))
    
    def edit_selected_star(self):
        """Edita la configuración de la estrella seleccionada."""
        selection = self.star_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una estrella para editar")
            return
        
        item = self.star_tree.item(selection[0])
        star_id = item['values'][0]
        star_label = item['values'][1]
        
        # Crear diálogo de edición
        self.edit_star_dialog(star_id, star_label)
    
    def edit_star_dialog(self, star_id: str, star_label: str):
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
        current_config = self.params.custom_star_settings.get(star_id, {})
        
        # Variables
        energy_var = tk.DoubleVar(value=current_config.get('energy_rate', self.params.energy_consumption_rate))
        time_var = tk.DoubleVar(value=current_config.get('time_bonus', self.params.life_time_bonus))
        energy_bonus_var = tk.DoubleVar(value=current_config.get('energy_bonus', self.params.energy_bonus_per_star))
        
        # UI del diálogo
        main_frame = tk.Frame(dialog, bg='#001122')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text=f"⭐ Configuración para {star_label}",
                font=('Arial', 12, 'bold'), bg='#001122', fg='white').pack(pady=(0, 20))
        
        # Consumo de energía
        energy_frame = tk.Frame(main_frame, bg='#001122')
        energy_frame.pack(fill=tk.X, pady=5)
        tk.Label(energy_frame, text="⚡ Consumo Energía:", bg='#001122', fg='white').pack(side=tk.LEFT)
        tk.Spinbox(energy_frame, from_=0.1, to=10.0, increment=0.1, textvariable=energy_var,
                  width=10).pack(side=tk.RIGHT)
        
        # Bonus tiempo
        time_frame = tk.Frame(main_frame, bg='#001122')
        time_frame.pack(fill=tk.X, pady=5)
        tk.Label(time_frame, text="💫 Bonus Tiempo:", bg='#001122', fg='white').pack(side=tk.LEFT)
        tk.Spinbox(time_frame, from_=-5.0, to=5.0, increment=0.1, textvariable=time_var,
                  width=10).pack(side=tk.RIGHT)
        
        # Bonus energía
        bonus_frame = tk.Frame(main_frame, bg='#001122')
        bonus_frame.pack(fill=tk.X, pady=5)
        tk.Label(bonus_frame, text="🔋 Bonus Energía:", bg='#001122', fg='white').pack(side=tk.LEFT)
        tk.Spinbox(bonus_frame, from_=0.0, to=20.0, increment=0.5, textvariable=energy_bonus_var,
                  width=10).pack(side=tk.RIGHT)
        
        # Botones
        button_frame = tk.Frame(main_frame, bg='#001122')
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        def save_star_config():
            self.params.custom_star_settings[star_id] = {
                'energy_rate': energy_var.get(),
                'time_bonus': time_var.get(),
                'energy_bonus': energy_bonus_var.get()
            }
            self.load_stars_list()
            dialog.destroy()
        
        def reset_star_config():
            if star_id in self.params.custom_star_settings:
                del self.params.custom_star_settings[star_id]
            self.load_stars_list()
            dialog.destroy()
        
        tk.Button(button_frame, text="❌ Cancelar", command=dialog.destroy,
                 bg='#CC4444', fg='white').pack(side=tk.LEFT)
        tk.Button(button_frame, text="🔄 Resetear", command=reset_star_config,
                 bg='#FFAA44', fg='black').pack(side=tk.LEFT, padx=(10, 0))
        tk.Button(button_frame, text="✅ Guardar", command=save_star_config,
                 bg='#44CC44', fg='black').pack(side=tk.RIGHT)
    
    def reset_selected_star(self):
        """Resetea la configuración de la estrella seleccionada."""
        selection = self.star_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una estrella para resetear")
            return
        
        item = self.star_tree.item(selection[0])
        star_id = item['values'][0]
        
        if star_id in self.params.custom_star_settings:
            del self.params.custom_star_settings[star_id]
            self.load_stars_list()
            messagebox.showinfo("Éxito", f"Configuración reseteada para estrella {star_id}")
    
    def apply_to_all_stars(self):
        """Aplica la configuración general a todas las estrellas."""
        if messagebox.askyesno("Confirmar", "¿Aplicar configuración general a TODAS las estrellas?"):
            self.params.custom_star_settings.clear()
            self.load_stars_list()
            messagebox.showinfo("Éxito", "Configuración general aplicada a todas las estrellas")
    
    def apply_preset(self, config: Dict):
        """Aplica una configuración preset."""
        for key, value in config.items():
            if hasattr(self.params, key):
                setattr(self.params, key, value)
        
        self.load_current_values()
        self.load_stars_list()
        
        # Actualizar descripción
        preset_name = [k for k, v in [
            ("🔬 Investigador Intensivo", {"energy_consumption_rate": 3.0}),
            ("⚡ Conservador de Energía", {"energy_consumption_rate": 1.0}),
            ("🌟 Explorador Rápido", {"energy_consumption_rate": 1.5}),
            ("🎯 Equilibrado", {"energy_consumption_rate": 2.0}),
            ("💫 Maximizar Conocimiento", {"energy_consumption_rate": 2.5}),
            ("🚀 Eficiencia Extrema", {"energy_consumption_rate": 0.5})
        ] if v.get("energy_consumption_rate") == config.get("energy_consumption_rate", 0)][0]
        
        self.preset_desc_text.delete('1.0', tk.END)
        self.preset_desc_text.insert('1.0', f"✅ Preset aplicado: {preset_name}\n\n" + 
                                     json.dumps(config, indent=2, ensure_ascii=False))
    
    def reset_to_defaults(self):
        """Resetea todos los parámetros a valores por defecto."""
        if messagebox.askyesno("Confirmar Reset", "¿Resetear TODOS los parámetros a valores por defecto?"):
            self.params = ResearchParameters()
            self.load_current_values()
            self.load_stars_list()
            messagebox.showinfo("Reset Completo", "Todos los parámetros han sido reseteados")
    
    def preview_changes(self):
        """Muestra una vista previa de los cambios."""
        self.collect_current_values()
        
        preview_window = tk.Toplevel(self.window)
        preview_window.title("👁️ Vista Previa de Configuración")
        preview_window.geometry("600x400")
        preview_window.configure(bg='#001122')
        
        text_widget = tk.Text(preview_window, bg='#001133', fg='white', font=('Courier', 9))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Generar preview
        preview_text = f"""
🔬 CONFIGURACIÓN DE PARÁMETROS DE INVESTIGACIÓN
{'='*50}

⚙️ PARÁMETROS GENERALES:
   ⚡ Consumo de energía: {self.params.energy_consumption_rate:.1f}% por unidad tiempo
   ⏰ Tiempo investigación: {self.params.time_percentage*100:.1f}%
   💫 Bonus tiempo vida: {self.params.life_time_bonus:+.1f} años por estrella
   🔋 Bonus energía: {self.params.energy_bonus_per_star:+.1f}% por estrella
   📚 Multiplicador: {self.params.knowledge_multiplier:.1f}x

⭐ CONFIGURACIONES ESPECÍFICAS POR ESTRELLA:
"""
        
        if self.params.custom_star_settings:
            for star_id, config in self.params.custom_star_settings.items():
                star = self.space_map.get_star(star_id)
                star_name = star.label if star else f"ID:{star_id}"
                preview_text += f"""
   🌟 {star_name} (ID: {star_id}):
      ⚡ Consumo: {config.get('energy_rate', 'default'):.1f}%
      💫 Bonus tiempo: {config.get('time_bonus', 'default'):+.1f}a
      🔋 Bonus energía: {config.get('energy_bonus', 'default'):+.1f}%
"""
        else:
            preview_text += "\n   (Ninguna configuración específica - usando valores generales)\n"
        
        preview_text += f"""
{'='*50}
📊 IMPACTO ESTIMADO:
   • Estrellas con configuración específica: {len(self.params.custom_star_settings)}
   • Tiempo promedio por estrella: {3 * self.params.time_percentage:.1f} unidades
   • Consumo promedio por estrella: {3 * self.params.time_percentage * self.params.energy_consumption_rate:.1f}%
"""
        
        text_widget.insert('1.0', preview_text)
        text_widget.config(state='disabled')
    
    def collect_current_values(self):
        """Recolecta los valores actuales de la UI."""
        self.params.energy_consumption_rate = self.energy_rate_var.get()
        self.params.time_percentage = self.time_percentage_var.get()
        self.params.life_time_bonus = self.life_bonus_var.get()
        self.params.energy_bonus_per_star = self.energy_bonus_var.get()
        self.params.knowledge_multiplier = self.knowledge_mult_var.get()
    
    def confirm_changes(self):
        """Confirma los cambios y cierra el editor."""
        self.collect_current_values()
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


def test_parameter_editor():
    """Función de prueba del editor."""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from src.models import SpaceMap
    
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    space_map = SpaceMap('data/constellations.json')
    editor = ResearchParameterEditor(root, space_map)
    
    root.wait_window(editor.window)
    
    params = editor.get_parameters()
    if params:
        print("✅ Parámetros configurados:")
        print(f"   Consumo energía: {params.energy_consumption_rate}")
        print(f"   Tiempo investigación: {params.time_percentage}")
        print(f"   Configuraciones específicas: {len(params.custom_star_settings)}")
    else:
        print("❌ Operación cancelada")
    
    root.destroy()


if __name__ == '__main__':
    test_parameter_editor()