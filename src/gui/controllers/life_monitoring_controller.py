"""
Life Monitoring Controller.
Implements Single Responsibility Principle - handles only life monitoring operations.
"""
from tkinter import messagebox
from typing import Optional, List
from ...core import BurroAstronauta, Star


class LifeMonitoringController:
    """Controller for life monitoring operations (sin panel visual)."""
    def __init__(self, burro: BurroAstronauta):
        self.burro = burro
    
    # Métodos eliminados: analyze_next_travel, demo_countdown, update_display