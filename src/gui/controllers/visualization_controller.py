"""
Visualization Controller.
Implements Single Responsibility Principle - handles only visualization operations.
"""
from typing import Optional, List, Dict, Any
from ...core import BurroAstronauta, Star
from ..interfaces.visualization_service_interface import IVisualizationService
from ..components.visualization_panel import VisualizationPanel


class VisualizationController:
    """Controller for visualization operations."""
    
    def __init__(self, visualization_service: IVisualizationService, 
                 visualization_panel: VisualizationPanel, burro: BurroAstronauta):
        self.visualization_service = visualization_service
        self.visualization_panel = visualization_panel
        self.burro = burro
    
    def update_visualization(self, path: Optional[List[Star]] = None):
        """Update the space map visualization."""
        try:
            fig = self.visualization_service.update_visualization(
                path=path, 
                burro_location=self.burro.current_location
            )
            self.visualization_panel.update_visualization(fig)
        except Exception as e:
            self.visualization_panel.append_info_text(f"\nError en visualización: {str(e)}")
    
    def generate_report(self, path_stats: Optional[Dict[str, Any]] = None):
        """Generate visual journey report."""
        try:
            if not path_stats:
                # Use empty stats if none provided
                from ...algorithms import RouteCalculator
                from ...core import SpaceMap
                space_map = SpaceMap('data/constellations.json')
                config = {}
                calculator = RouteCalculator(space_map, config)
                path_stats = calculator.calculate_path_stats([])
            
            self.visualization_service.generate_journey_report(self.burro, path_stats)
        except Exception as e:
            self.visualization_panel.append_info_text(f"\nError generando reporte: {str(e)}")
    
    def update_info_text(self, text: str):
        """Update the information text."""
        self.visualization_panel.update_info_text(text)
    
    def append_info_text(self, text: str):
        """Append text to the information display."""
        self.visualization_panel.append_info_text(text)