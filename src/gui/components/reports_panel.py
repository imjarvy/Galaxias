"""
Reports Panel Component.
Implements Single Responsibility Principle - handles only reports UI.
"""
import tkinter as tk
from typing import Callable, Optional
from ..interfaces.component_interface import IComponent


class ReportsPanel(IComponent):
    """Component responsible for reports interface."""
    
    def __init__(self):
        self.frame = None
        
        # Callbacks
        self.on_generate_report: Optional[Callable] = None
    
    def create_widgets(self, parent: tk.Widget) -> tk.Widget:
        """Create and return the reports widgets."""
        self.frame = tk.LabelFrame(parent, text="Reportes",
                                  font=('Arial', 12, 'bold'),
                                  bg='#000066', fg='white',
                                  relief=tk.GROOVE, borderwidth=2)
        
        tk.Button(self.frame, text="Generar Reporte Visual",
                 command=self._handle_generate_report,
                 bg='#FFFF44', fg='black', font=('Arial', 10, 'bold'),
                 relief=tk.RAISED, borderwidth=2).pack(pady=10)
        
        return self.frame
    
    def _handle_generate_report(self):
        """Handle generate report button click."""
        if self.on_generate_report:
            self.on_generate_report()
    
    def update_display(self):
        """Update the reports display."""
        # No display updates needed for this component
        pass