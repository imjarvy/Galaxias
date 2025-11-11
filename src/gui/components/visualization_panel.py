"""
Visualization Panel Component.
Implements Single Responsibility Principle - handles only visualization display.
"""
import tkinter as tk
from tkinter import scrolledtext
from typing import Optional, List, Dict, Any
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ...core import Star
from ..interfaces.component_interface import IComponent


class VisualizationPanel(IComponent):
    """Component responsible for visualization display."""
    
    def __init__(self):
        self.frame = None
        self.canvas_frame = None
        self.info_text = None
        self.current_canvas = None
    
    def create_widgets(self, parent: tk.Widget) -> tk.Widget:
        """Create and return the visualization widgets."""
        self.frame = tk.Frame(parent, bg='#000033')
        
        # Canvas for matplotlib
        self.canvas_frame = tk.Frame(self.frame, bg='#000033')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info text at bottom
        self.info_text = scrolledtext.ScrolledText(self.frame, height=6, 
                                                   bg='#000033', fg='white',
                                                   font=('Courier', 9))
        self.info_text.pack(fill=tk.X, pady=5)
        
        return self.frame
    
    def update_display(self):
        """Update the visualization display."""
        # This method is called by the interface but actual updates
        # are handled by update_visualization method
        pass
    
    def update_visualization(self, fig: Figure):
        """Update the visualization with a new figure."""
        # Clear previous canvas
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
        
        # Embed new figure in tkinter
        self.current_canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.current_canvas.draw()
        self.current_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        plt.close(fig)
    
    def update_info_text(self, info: str):
        """Update the information text display."""
        if self.info_text:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, info)
    
    def append_info_text(self, text: str):
        """Append text to the information display."""
        if self.info_text:
            self.info_text.insert(tk.END, text)
            self.info_text.see(tk.END)
    
    def clear_info_text(self):
        """Clear the information text display."""
        if self.info_text:
            self.info_text.delete(1.0, tk.END)