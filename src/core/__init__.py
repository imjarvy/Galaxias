"""
Core business logic package for Galaxias.

Contains the fundamental domain entities and business rules:
- Models: Star, BurroAstronauta, Route, SpaceMap
- Research impact validation
- Comet impact system
"""
from .models import Star, Route, BurroAstronauta, SpaceMap, Comet
from .research_impact_validator import ResearchImpactValidator
from .comet_impact_system import CometImpactManager

__all__ = [
    # Core Models
    'Star', 
    'Route', 
    'BurroAstronauta', 
    'SpaceMap',
    'Comet',
    
    # Domain Services
    'ResearchImpactValidator',
    'CometImpactManager'
]