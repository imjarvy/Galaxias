"""
Burro Status Panel Component.
Implements Single Responsibility Principle - handles only burro status display.
"""
import tkinter as tk
from tkinter import scrolledtext, messagebox
from typing import Callable, Optional, Dict, Any
from ...core import BurroAstronauta
from ..interfaces.component_interface import IComponent


class BurroStatusPanel(IComponent):
    """Component responsible for displaying burro astronaut status."""
    
    def __init__(self, burro: BurroAstronauta):
        self.burro = burro
        self.frame = None
        self.status_text = None
        
        # Callbacks
        self.on_restore_resources: Optional[Callable] = None
    
    def create_widgets(self, parent: tk.Widget) -> tk.Widget:
        """Create and return the burro status widgets."""
        self.frame = tk.LabelFrame(parent, text="Estado del Burro Astronauta",
                                  font=('Arial', 12, 'bold'),
                                  bg='#000066', fg='white',
                                  relief=tk.GROOVE, borderwidth=2)
        
        self.status_text = scrolledtext.ScrolledText(self.frame, height=10, width=35,
                                                     bg='#000033', fg='white',
                                                     font=('Courier', 9))
        self.status_text.pack(padx=5, pady=5)
        
        # Restore resources button
        tk.Button(self.frame, text="Restaurar Recursos",
                 command=self._handle_restore_resources,
                 bg='#FFAA44', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=5)
        
        return self.frame
    
    def _handle_restore_resources(self):
        """Handle restore resources button click."""
        if self.on_restore_resources:
            self.on_restore_resources()
    
    def update_display(self):
        """Update the burro status display."""
        if not self.status_text:
            return
            
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
    
    def append_message(self, message: str):
        """Append a message to the status display."""
        if self.status_text:
            self.status_text.insert(tk.END, message)
            self.status_text.see(tk.END)
    
    def clear_messages(self):
        """Clear all messages from status display."""
        if self.status_text:
            self.status_text.delete(1.0, tk.END)