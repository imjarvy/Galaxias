"""
Scripts ejecutables del sistema Galaxias.

Contiene herramientas de línea de comandos:
- max_visit_route: Maximiza estrellas visitadas
- min_cost_route: Minimiza costo de recursos
- demos/: Scripts de demostración
"""

from .min_cost_route import main as run_min_cost
from .max_visit_route import main as run_max_visit, compute_max_visits_from_json

__all__ = [
    'run_min_cost',
    'run_max_visit',
    'compute_max_visits_from_json'
]