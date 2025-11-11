"""
Presentation layer package for visualization and reporting.

Contains components for:
- Space map visualization
- Life monitoring widgets
- GUI components and utilities
- Journey reports and charts
"""
from .visualizer import SpaceVisualizer
from .life_monitor import LifeMonitor
from .gui_life_monitor import TkinterAlertSystem, GuiLifeStatusWidget
from .gui_hypergiant_jump import HyperGiantJumpGUI

__all__ = [
    'SpaceVisualizer',
    'LifeMonitor',
    'TkinterAlertSystem',
    'GuiLifeStatusWidget', 
    'HyperGiantJumpGUI'
]