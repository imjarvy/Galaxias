"""
System constants for the Galaxias space simulation.
Centralizes all magic numbers and configuration constants.
"""

# File paths
DEFAULT_CONSTELLATIONS_PATH = "data/constellations.json"
DEFAULT_SPACESHIP_CONFIG_PATH = "data/spaceship_config.json"

# GUI Configuration
WINDOW_TITLE = "🌌 Sistema de Navegación Galaxias"
DEFAULT_WINDOW_SIZE = "1400x800"
FONT_FAMILY = "Arial"
SMALL_FONT_SIZE = 10
MEDIUM_FONT_SIZE = 12
LARGE_FONT_SIZE = 14

# Colors
PRIMARY_COLOR = "#2E86AB"
SECONDARY_COLOR = "#A23B72"
SUCCESS_COLOR = "#4CAF50"
WARNING_COLOR = "#FF9800"
ERROR_COLOR = "#F44336"
BACKGROUND_COLOR = "#F5F5F5"

# Visualization
STAR_COLORS = {
    'normal': 'lightblue',
    'hypergiant': 'gold',
    'visited': 'lightgreen',
    'start': 'red',
    'goal': 'green'
}

ROUTE_COLORS = {
    'normal': 'gray',
    'optimal': 'blue',
    'blocked': 'red',
    'dangerous': 'orange'
}

# Physics constants
DEFAULT_FUEL_RATE = 1.0
DEFAULT_DANGER_PENALTY = 10.0
MIN_ENERGY_THRESHOLD = 0
MAX_DANGER_LEVEL = 10

# Algorithm parameters
MAX_ITERATIONS = 1000
CONVERGENCE_THRESHOLD = 0.001

# Life monitoring
CRITICAL_LIFE_THRESHOLD = 20
WARNING_LIFE_THRESHOLD = 50
LIFE_CONSUMPTION_RATE = 1.0

# Research parameters
DEFAULT_RESEARCH_IMPACT = 1.0
MIN_RESEARCH_IMPACT = 0.1
MAX_RESEARCH_IMPACT = 10.0