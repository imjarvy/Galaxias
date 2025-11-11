"""
Burro Controller.
Implements Single Responsibility Principle - handles only burro-related operations.
"""
from typing import Optional
from tkinter import messagebox
from ...core import BurroAstronauta
from ..components.burro_status_panel import BurroStatusPanel


class BurroController:
    """Controller for burro astronaut operations."""
    
    def __init__(self, burro: BurroAstronauta, burro_panel: BurroStatusPanel):
        self.burro = burro
        self.burro_panel = burro_panel
        
        # Callback for state changes
        self.on_state_change: Optional[callable] = None
        
        # Setup callbacks
        self._setup_callbacks()
    
    def _setup_callbacks(self):
        """Setup callbacks for the burro panel."""
        self.burro_panel.on_restore_resources = self.restore_resources
    
    def restore_resources(self):
        """Restore the burro's resources to initial values."""
        try:
            self.burro.restore_resources()
            self.burro_panel.update_display()
            
            # Notify state change
            if self.on_state_change:
                self.on_state_change()
            
            messagebox.showinfo("Recursos Restaurados", "Recursos restaurados a valores iniciales")
        except Exception as e:
            messagebox.showerror("Error", f"Error al restaurar recursos: {str(e)}")
    
    def update_display(self):
        """Update the burro status display."""
        self.burro_panel.update_display()
    
    def append_status_message(self, message: str):
        """Append a message to the burro status display."""
        self.burro_panel.append_message(message)