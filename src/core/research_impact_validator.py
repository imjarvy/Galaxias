"""
Validador de impactos de investigación por estrella.

Este módulo implementa la validación detallada de cómo las labores investigativas
afectan la salud y tiempo de vida del burro astronauta para cada estrella individual.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
import json


@dataclass
class StarResearchImpact:
    """Representa el impacto de investigación para una estrella específica."""
    star_id: str
    star_label: str
    
    # Parámetros base de la estrella
    base_time_to_eat: int
    base_energy: int
    
    # Impactos configurables
    health_impact: float = 0.0          # Puntos de salud ganados/perdidos (-100 a +100)
    health_probability: float = 0.5     # Probabilidad de que ocurra el impacto (0.0 a 1.0)
    life_time_impact: float = 0.0       # Años de vida ganados/perdidos (-10 a +10)
    energy_efficiency: float = 1.0      # Multiplicador de eficiencia energética (0.1 a 3.0)
    experiment_bonus: float = 0.0       # Bonus por experimento completado (0 a 100)
    
    # Campos calculados
    final_health_delta: float = field(init=False)
    final_life_delta: float = field(init=False)
    final_energy_multiplier: float = field(init=False)
    risk_level: str = field(init=False)
    
    def __post_init__(self):
        self.calculate_final_impacts()
    
    def calculate_final_impacts(self):
        """Calcula los impactos finales basados en probabilidades."""
        self.final_health_delta = self.health_impact * self.health_probability
        self.final_life_delta = self.life_time_impact * (1.0 if self.health_impact >= 0 else 0.7)
        self.final_energy_multiplier = self.energy_efficiency
        
        # Determinar nivel de riesgo
        if self.health_impact < -30 or self.life_time_impact < -2:
            self.risk_level = "ALTO"
        elif self.health_impact < 0 or self.life_time_impact < 0:
            self.risk_level = "MEDIO"
        else:
            self.risk_level = "BAJO"
    
    def to_dict(self) -> Dict:
        """Convierte a diccionario para serialización."""
        return {
            'star_id': self.star_id,
            'star_label': self.star_label,
            'health_impact': self.health_impact,
            'health_probability': self.health_probability,
            'life_time_impact': self.life_time_impact,
            'energy_efficiency': self.energy_efficiency,
            'experiment_bonus': self.experiment_bonus,
            'final_health_delta': self.final_health_delta,
            'final_life_delta': self.final_life_delta,
            'risk_level': self.risk_level
        }


class ResearchImpactValidator:
    """Validador principal para impactos de investigación por estrella."""
    
    def __init__(self, space_map):
        """
        Inicializa el validador.
        
        Args:
            space_map: Mapa espacial con las estrellas disponibles
        """
        self.space_map = space_map
        self.star_impacts: Dict[str, StarResearchImpact] = {}
        self._initialize_default_impacts()
    
    def _initialize_default_impacts(self):
        """Inicializa impactos por defecto para todas las estrellas."""
        for star in self.space_map.get_all_stars_list():
            self.star_impacts[star.id] = StarResearchImpact(
                star_id=star.id,
                star_label=star.label,
                base_time_to_eat=star.time_to_eat,
                base_energy=star.amount_of_energy
            )
    
    def get_star_impact(self, star_id: str) -> Optional[StarResearchImpact]:
        """Obtiene el impacto configurado para una estrella."""
        return self.star_impacts.get(star_id)
    
    def update_star_impact(self, star_id: str, impact: StarResearchImpact):
        """Actualiza el impacto para una estrella."""
        self.star_impacts[star_id] = impact
    
    def calculate_route_impact(self, star_ids: List[str]) -> Dict:
        """
        Calcula el impacto total de una ruta sobre la salud y vida.
        
        Args:
            star_ids: Lista de IDs de estrellas en la ruta
            
        Returns:
            Diccionario con impactos totales calculados
        """
        total_health_delta = 0.0
        total_life_delta = 0.0
        total_energy_multiplier = 1.0
        risk_stars = []
        
        for star_id in star_ids:
            impact = self.get_star_impact(star_id)
            if impact:
                total_health_delta += impact.final_health_delta
                total_life_delta += impact.final_life_delta
                total_energy_multiplier *= impact.final_energy_multiplier
                
                if impact.risk_level in ["ALTO", "MEDIO"]:
                    risk_stars.append({
                        'star': impact.star_label,
                        'risk': impact.risk_level,
                        'health_impact': impact.health_impact,
                        'life_impact': impact.life_time_impact
                    })
        
        return {
            'total_health_impact': round(total_health_delta, 2),
            'total_life_impact': round(total_life_delta, 2),
            'energy_efficiency_multiplier': round(total_energy_multiplier, 3),
            'risk_stars': risk_stars,
            'stars_analyzed': len(star_ids),
            'overall_risk': self._calculate_overall_risk(total_health_delta, total_life_delta)
        }
    
    def _calculate_overall_risk(self, health_delta: float, life_delta: float) -> str:
        """Calcula el riesgo general de la ruta."""
        if health_delta < -50 or life_delta < -3:
            return "CRÍTICO"
        elif health_delta < -20 or life_delta < -1:
            return "ALTO"
        elif health_delta < 0 or life_delta < 0:
            return "MEDIO"
        else:
            return "BAJO"
    
    def export_configuration(self) -> str:
        """Exporta la configuración actual a JSON."""
        config = {
            'research_impacts': {
                star_id: impact.to_dict() 
                for star_id, impact in self.star_impacts.items()
            },
            'metadata': {
                'total_stars': len(self.star_impacts),
                'configured_stars': sum(1 for impact in self.star_impacts.values() 
                                      if impact.health_impact != 0 or impact.life_time_impact != 0)
            }
        }
        return json.dumps(config, indent=2, ensure_ascii=False)
    
    def import_configuration(self, json_config: str) -> bool:
        """
        Importa configuración desde JSON.
        
        Args:
            json_config: Configuración en formato JSON
            
        Returns:
            True si la importación fue exitosa
        """
        try:
            config = json.loads(json_config)
            impacts = config.get('research_impacts', {})
            
            for star_id, impact_data in impacts.items():
                if star_id in self.star_impacts:
                    impact = self.star_impacts[star_id]
                    impact.health_impact = impact_data.get('health_impact', 0.0)
                    impact.health_probability = impact_data.get('health_probability', 0.5)
                    impact.life_time_impact = impact_data.get('life_time_impact', 0.0)
                    impact.energy_efficiency = impact_data.get('energy_efficiency', 1.0)
                    impact.experiment_bonus = impact_data.get('experiment_bonus', 0.0)
                    impact.calculate_final_impacts()
            
            return True
        except Exception:
            return False


class ResearchImpactValidatorGUI:
    """Interfaz gráfica para el validador de impactos de investigación."""
    
    def __init__(self, parent, space_map):
        """
        Inicializa la interfaz gráfica.
        
        Args:
            parent: Ventana padre
            space_map: Mapa espacial
        """
        self.parent = parent
        self.space_map = space_map
        self.validator = ResearchImpactValidator(space_map)
        self.result = None
        
        # Crear ventana
        self.window = tk.Toplevel(parent)
        self.window.title("Validador de Impactos de Investigación")
        self.window.geometry("1000x700")
        self.window.configure(bg='#001122')
        self.window.resizable(True, True)
        
        # Hacer ventana modal
        self.window.transient(parent)
        self.window.grab_set()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Frame principal
        main_frame = tk.Frame(self.window, bg='#001122')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = tk.Label(main_frame, 
                        text="🔬 Validador de Impactos de Investigación por Estrella",
                        font=('Arial', 16, 'bold'),
                        bg='#001122', fg='#FFD700')
        title.pack(pady=10)
        
        # Frame de contenido principal
        content_frame = tk.Frame(main_frame, bg='#001122')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Panel izquierdo - Lista de estrellas
        left_panel = tk.Frame(content_frame, bg='#003344', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 5))
        
        tk.Label(left_panel, text="⭐ Seleccionar Estrella:",
                font=('Arial', 12, 'bold'),
                bg='#003344', fg='white').pack(pady=5)
        
        # Lista de estrellas
        self.star_listbox = tk.Listbox(left_panel, width=25, height=15,
                                      bg='#002233', fg='white',
                                      selectbackground='#0066AA')
        self.star_listbox.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Poblar lista de estrellas
        for star in self.space_map.get_all_stars_list():
            display_text = f"{star.label} (ID:{star.id})"
            if star.hypergiant:
                display_text += " ⭐"
            self.star_listbox.insert(tk.END, display_text)
        
        self.star_listbox.bind('<<ListboxSelect>>', self.on_star_select)
        
        # Panel derecho - Configuración de impacto
        right_panel = tk.Frame(content_frame, bg='#003344', relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.setup_impact_config_panel(right_panel)
        
        # Panel inferior - Resumen y acciones
        bottom_panel = tk.Frame(main_frame, bg='#001122')
        bottom_panel.pack(fill=tk.X, pady=10)
        
        self.setup_bottom_panel(bottom_panel)
    
    def setup_impact_config_panel(self, parent):
        """Configura el panel de configuración de impactos."""
        tk.Label(parent, text="🧪 Configuración de Impacto de Investigación",
                font=('Arial', 12, 'bold'),
                bg='#003344', fg='#FFD700').pack(pady=10)
        
        # Frame scrollable para los controles
        canvas = tk.Canvas(parent, bg='#003344')
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#003344')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Información de estrella seleccionada
        self.star_info_label = tk.Label(scrollable_frame,
                                       text="Seleccione una estrella para configurar",
                                       font=('Arial', 10, 'italic'),
                                       bg='#003344', fg='#CCCCCC')
        self.star_info_label.pack(pady=5)
        
        # Controles de impacto en salud
        health_frame = tk.LabelFrame(scrollable_frame, text="💊 Impacto en Salud",
                                   bg='#003344', fg='white',
                                   font=('Arial', 10, 'bold'))
        health_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(health_frame, text="Puntos de salud (-100 a +100):",
                bg='#003344', fg='white').pack(anchor=tk.W, padx=5)
        self.health_impact_var = tk.DoubleVar()
        self.health_impact_scale = tk.Scale(health_frame, from_=-100, to=100,
                                           orient=tk.HORIZONTAL, resolution=1,
                                           variable=self.health_impact_var,
                                           bg='#003344', fg='white',
                                           command=self.on_impact_change)
        self.health_impact_scale.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(health_frame, text="Probabilidad (0.0 a 1.0):",
                bg='#003344', fg='white').pack(anchor=tk.W, padx=5)
        self.health_prob_var = tk.DoubleVar(value=0.5)
        self.health_prob_scale = tk.Scale(health_frame, from_=0.0, to=1.0,
                                         orient=tk.HORIZONTAL, resolution=0.1,
                                         variable=self.health_prob_var,
                                         bg='#003344', fg='white',
                                         command=self.on_impact_change)
        self.health_prob_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Controles de impacto en tiempo de vida
        life_frame = tk.LabelFrame(scrollable_frame, text="⏰ Impacto en Tiempo de Vida",
                                 bg='#003344', fg='white',
                                 font=('Arial', 10, 'bold'))
        life_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(life_frame, text="Años ganados/perdidos (-10 a +10):",
                bg='#003344', fg='white').pack(anchor=tk.W, padx=5)
        self.life_impact_var = tk.DoubleVar()
        self.life_impact_scale = tk.Scale(life_frame, from_=-10, to=10,
                                        orient=tk.HORIZONTAL, resolution=0.1,
                                        variable=self.life_impact_var,
                                        bg='#003344', fg='white',
                                        command=self.on_impact_change)
        self.life_impact_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Controles adicionales
        bonus_frame = tk.LabelFrame(scrollable_frame, text="⚡ Configuraciones Adicionales",
                                  bg='#003344', fg='white',
                                  font=('Arial', 10, 'bold'))
        bonus_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(bonus_frame, text="Eficiencia energética (0.1 a 3.0):",
                bg='#003344', fg='white').pack(anchor=tk.W, padx=5)
        self.energy_eff_var = tk.DoubleVar(value=1.0)
        self.energy_eff_scale = tk.Scale(bonus_frame, from_=0.1, to=3.0,
                                       orient=tk.HORIZONTAL, resolution=0.1,
                                       variable=self.energy_eff_var,
                                       bg='#003344', fg='white',
                                       command=self.on_impact_change)
        self.energy_eff_scale.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(bonus_frame, text="Bonus por experimento (0 a 100):",
                bg='#003344', fg='white').pack(anchor=tk.W, padx=5)
        self.experiment_bonus_var = tk.DoubleVar()
        self.experiment_bonus_scale = tk.Scale(bonus_frame, from_=0, to=100,
                                             orient=tk.HORIZONTAL, resolution=1,
                                             variable=self.experiment_bonus_var,
                                             bg='#003344', fg='white',
                                             command=self.on_impact_change)
        self.experiment_bonus_scale.pack(fill=tk.X, padx=5, pady=2)
        
        # Resumen de impacto calculado
        self.impact_summary = tk.Text(scrollable_frame, height=8, width=50,
                                    bg='#002233', fg='white',
                                    font=('Courier', 9))
        self.impact_summary.pack(fill=tk.X, padx=10, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def setup_bottom_panel(self, parent):
        """Configura el panel inferior con acciones."""
        # Botones de acción
        buttons_frame = tk.Frame(parent, bg='#001122')
        buttons_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(buttons_frame, text="📊 Validar Ruta Actual",
                 command=self.validate_current_route,
                 bg='#0066AA', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="💾 Exportar Configuración",
                 command=self.export_config,
                 bg='#AA6600', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="📂 Importar Configuración",
                 command=self.import_config,
                 bg='#6600AA', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="✅ Aplicar y Cerrar",
                 command=self.apply_and_close,
                 bg='#006600', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.RIGHT, padx=5)
        
        tk.Button(buttons_frame, text="❌ Cancelar",
                 command=self.cancel,
                 bg='#AA0000', fg='white',
                 font=('Arial', 10, 'bold')).pack(side=tk.RIGHT, padx=5)
    
    def on_star_select(self, event):
        """Maneja la selección de una estrella."""
        selection = self.star_listbox.curselection()
        if selection:
            index = selection[0]
            stars = list(self.space_map.get_all_stars_list())
            if index < len(stars):
                star = stars[index]
                self.load_star_config(star)
    
    def load_star_config(self, star):
        """Carga la configuración de una estrella en los controles."""
        impact = self.validator.get_star_impact(star.id)
        if impact:
            self.star_info_label.config(
                text=f"🌟 {star.label} (ID: {star.id}) - Energía: {star.amount_of_energy}, Tiempo: {star.time_to_eat}"
            )
            
            # Cargar valores en controles
            self.health_impact_var.set(impact.health_impact)
            self.health_prob_var.set(impact.health_probability)
            self.life_impact_var.set(impact.life_time_impact)
            self.energy_eff_var.set(impact.energy_efficiency)
            self.experiment_bonus_var.set(impact.experiment_bonus)
            
            self.current_star = star
            self.update_impact_summary()
    
    def on_impact_change(self, value=None):
        """Maneja cambios en los controles de impacto."""
        if hasattr(self, 'current_star'):
            self.update_star_impact()
            self.update_impact_summary()
    
    def update_star_impact(self):
        """Actualiza el impacto de la estrella actual."""
        if hasattr(self, 'current_star'):
            star = self.current_star
            impact = StarResearchImpact(
                star_id=star.id,
                star_label=star.label,
                base_time_to_eat=star.time_to_eat,
                base_energy=star.amount_of_energy,
                health_impact=self.health_impact_var.get(),
                health_probability=self.health_prob_var.get(),
                life_time_impact=self.life_impact_var.get(),
                energy_efficiency=self.energy_eff_var.get(),
                experiment_bonus=self.experiment_bonus_var.get()
            )
            self.validator.update_star_impact(star.id, impact)
    
    def update_impact_summary(self):
        """Actualiza el resumen de impacto."""
        if hasattr(self, 'current_star'):
            impact = self.validator.get_star_impact(self.current_star.id)
            if impact:
                summary = (
                    f"📊 RESUMEN DE IMPACTO - {impact.star_label}\n"
                    + "=" * 40 + "\n"
                    f"💊 Salud esperada: {impact.final_health_delta:+.1f} puntos\n"
                    f"⏰ Tiempo de vida: {impact.final_life_delta:+.1f} años\n"
                    f"⚡ Eficiencia energética: {impact.final_energy_multiplier:.1f}x\n"
                    f"🎯 Bonus experimento: {impact.experiment_bonus:.0f}%\n"
                    f"⚠️ Nivel de riesgo: {impact.risk_level}\n\n"
                    f"📝 Cálculos:\n"
                    f"   Salud = {impact.health_impact:.1f} × {impact.health_probability:.1f} = {impact.final_health_delta:+.1f}\n"
                    f"   Vida = {impact.life_time_impact:.1f} × factor = {impact.final_life_delta:+.1f}\n"
                )
                
                self.impact_summary.delete('1.0', tk.END)
                self.impact_summary.insert('1.0', summary)
    
    def validate_current_route(self):
        """Valida el impacto de la ruta actual."""
        # Obtener estrellas seleccionadas (simplificado para demo)
        all_stars = [star.id for star in self.space_map.get_all_stars_list()]
        route_impact = self.validator.calculate_route_impact(all_stars)
        
        message = (
            f"📊 VALIDACIÓN DE IMPACTO DE RUTA\n\n"
            f"🔬 Estrellas analizadas: {route_impact['stars_analyzed']}\n"
            f"💊 Impacto total en salud: {route_impact['total_health_impact']:+.1f} puntos\n"
            f"⏰ Impacto total en vida: {route_impact['total_life_impact']:+.1f} años\n"
            f"⚡ Multiplicador energético: {route_impact['energy_efficiency_multiplier']:.2f}x\n"
            f"⚠️ Riesgo general: {route_impact['overall_risk']}\n\n"
        )
        
        if route_impact['risk_stars']:
            message += "🚨 ESTRELLAS DE RIESGO:\n"
            for risk_star in route_impact['risk_stars']:
                message += f"   • {risk_star['star']} ({risk_star['risk']})\n"
        
        messagebox.showinfo("Validación de Ruta", message)
    
    def export_config(self):
        """Exporta la configuración actual."""
        config_json = self.validator.export_configuration()
        
        # Crear ventana para mostrar JSON
        export_window = tk.Toplevel(self.window)
        export_window.title("Exportar Configuración")
        export_window.geometry("600x400")
        
        text_area = tk.Text(export_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_area.insert('1.0', config_json)
        
        tk.Button(export_window, text="Copiar al Portapapeles",
                 command=lambda: self.window.clipboard_append(config_json)).pack(pady=5)
    
    def import_config(self):
        """Importa configuración desde JSON."""
        import_window = tk.Toplevel(self.window)
        import_window.title("Importar Configuración")
        import_window.geometry("600x400")
        
        tk.Label(import_window, text="Pegue la configuración JSON:").pack(pady=5)
        
        text_area = tk.Text(import_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        def do_import():
            json_text = text_area.get('1.0', tk.END).strip()
            if self.validator.import_configuration(json_text):
                messagebox.showinfo("Éxito", "Configuración importada correctamente")
                import_window.destroy()
            else:
                messagebox.showerror("Error", "Error al importar configuración")
        
        tk.Button(import_window, text="Importar", command=do_import).pack(pady=5)
    
    def apply_and_close(self):
        """Aplica los cambios y cierra la ventana."""
        self.result = self.validator
        self.window.destroy()
    
    def cancel(self):
        """Cancela sin aplicar cambios."""
        self.result = None
        self.window.destroy()
    
    def get_result(self) -> Optional[ResearchImpactValidator]:
        """Obtiene el resultado del validador."""
        return self.result