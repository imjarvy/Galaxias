"""
GUI Components package.
Each component handles a single responsibility.
"""
from .route_planning_panel import RoutePlanningPanel
from .burro_status_panel import BurroStatusPanel
from .life_monitoring_panel import LifeMonitoringPanel
from .reports_panel import ReportsPanel
from .visualization_panel import VisualizationPanel

__all__ = [
    'RoutePlanningPanel', 
    'BurroStatusPanel', 
    'LifeMonitoringPanel',
    'ReportsPanel',
    'VisualizationPanel'
]