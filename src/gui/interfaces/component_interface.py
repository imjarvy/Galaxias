"""
Interface for GUI components.
Implements Single Responsibility Principle.
"""
from abc import ABC, abstractmethod
import tkinter as tk


class IComponent(ABC):
    """Base interface for GUI components."""
    
    @abstractmethod
    def create_widgets(self, parent: tk.Widget) -> tk.Widget:
        """Create and return the component's widgets."""
        pass
    
    @abstractmethod
    def update_display(self) -> None:
        """Update the component's display."""
        pass