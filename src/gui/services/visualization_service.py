"""
Visualization service implementation.
Implements Single Responsibility Principle for visualization operations.
"""
from typing import List, Optional
import matplotlib.pyplot as plt
import matplotlib.figure
from ...core import SpaceMap, Star, BurroAstronauta
from ...presentation import SpaceVisualizer
from ..interfaces.visualization_service_interface import IVisualizationService


class VisualizationService(IVisualizationService):
    """Service responsible for visualization operations."""
    
    def __init__(self, space_map: SpaceMap):
        self.space_map = space_map
        self.visualizer = SpaceVisualizer(space_map)
    
    def update_visualization(self, path: Optional[List[Star]] = None, 
                           burro_location: Optional[Star] = None) -> matplotlib.figure.Figure:
        """Update the space map visualization."""
        fig = self.visualizer.plot_space_map(
            highlight_path=path,
            donkey_location=burro_location,
            show=False
        )
        return fig
    
    def generate_journey_report(self, burro: BurroAstronauta, stats: dict) -> None:
        """Generate visual journey report."""
        self.visualizer.plot_journey_report(
            burro,
            stats,
            save_path='assets/journey_report.png',
            show=True
        )