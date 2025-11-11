"""
Life Monitoring Panel Component.
Implements Single Responsibility Principle - handles only life monitoring UI.
"""
import tkinter as tk
from typing import Callable, Optional
from ...core import BurroAstronauta
# TODO: Refactorizar life monitor imports para nueva arquitectura
# from src.gui_life_monitor import GuiLifeStatusWidget, TravelDistanceAnalyzer
from ..interfaces.component_interface import IComponent


class LifeMonitoringPanel(IComponent):
    """Component responsible for life monitoring interface."""
    
    def __init__(self, root: tk.Tk, burro: BurroAstronauta):
        self.root = root
        self.burro = burro
        self.frame = None
        self.life_status_widget = None
        self.travel_analyzer = None
        
        # Callbacks
        self.on_analyze_travel: Optional[Callable] = None
        self.on_demo_countdown: Optional[Callable] = None
    
    def create_widgets(self, parent: tk.Widget) -> tk.Widget:
        """Create and return the life monitoring widgets."""
        self.frame = tk.LabelFrame(parent, text="Monitoreo de Vida",
                                  font=('Arial', 12, 'bold'),
                                  bg='#000066', fg='white',
                                  relief=tk.GROOVE, borderwidth=2)
        
        # TODO: Implementar widgets de life monitoring en nueva arquitectura
        # self.life_status_widget = GuiLifeStatusWidget(self.frame)
        # self.life_status_widget.pack(fill=tk.X, padx=5, pady=5)
        self.life_label = tk.Label(self.frame, text="Life Monitoring (Placeholder)")
        self.life_label.pack()
        
        # TODO: Implementar travel analyzer en nueva arquitectura
        # self.travel_analyzer = TravelDistanceAnalyzer(self.root)
        # self.travel_analyzer.set_burro(self.burro)
        
        # Botón para análisis de viaje
        tk.Button(self.frame, text="📊 Analizar Próximo Viaje",
                 command=self._handle_analyze_travel,
                 bg='#6633FF', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=2)
        
        # Botón para simular countdown (DEMO)
        tk.Button(self.frame, text="⏰ Demo Countdown",
                 command=self._handle_demo_countdown,
                 bg='#FF3366', fg='white', font=('Arial', 9, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=2)
        
        return self.frame
    
    def _handle_analyze_travel(self):
        """Handle analyze travel button click."""
        if self.on_analyze_travel:
            self.on_analyze_travel()
    
    def _handle_demo_countdown(self):
        """Handle demo countdown button click."""
        if self.on_demo_countdown:
            self.on_demo_countdown()
    
    def update_display(self):
        """Update the life monitoring display."""
        if self.life_status_widget:
            status = self.burro.get_status()
            self.life_status_widget.update_status(status)
    
    def get_travel_analyzer(self):
        """Get the travel analyzer instance."""
        return self.travel_analyzer
    
    def get_life_status_widget(self):
        """Get the life status widget instance."""
        return self.life_status_widget