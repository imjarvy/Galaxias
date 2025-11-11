"""
Interface for visualization services.
Implements Dependency Inversion Principle.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Any
from ...core import Star, BurroAstronauta
import matplotlib.figure


class IVisualizationService(ABC):
    """Interface for visualization services."""
    
    @abstractmethod
    def update_visualization(self, path: Optional[List[Star]] = None, 
                           burro_location: Optional[Star] = None) -> matplotlib.figure.Figure:
        """Update the space map visualization."""
        pass
    
    @abstractmethod
    def generate_journey_report(self, burro: BurroAstronauta, stats: dict) -> None:
        """Generate visual journey report."""
        pass