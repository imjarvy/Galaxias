"""
Validation utilities for the Galaxias system.
Provides common validation functions across the application.
"""
from typing import Dict, List, Any, Optional, Union
import re

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class Validators:
    """Collection of validation functions."""
    
    @staticmethod
    def validate_star_id(star_id: Union[str, int]) -> str:
        """Validate and normalize star ID."""
        if isinstance(star_id, int):
            star_id = str(star_id)
        
        if not isinstance(star_id, str):
            raise ValidationError(f"Star ID must be string or int, got {type(star_id)}")
        
        star_id = star_id.strip()
        if not star_id:
            raise ValidationError("Star ID cannot be empty")
        
        return star_id
    
    @staticmethod
    def validate_coordinates(x: float, y: float) -> tuple[float, float]:
        """Validate star coordinates."""
        try:
            x, y = float(x), float(y)
        except (ValueError, TypeError):
            raise ValidationError(f"Coordinates must be numeric, got x={x}, y={y}")
        
        if not (-1000 <= x <= 1000) or not (-1000 <= y <= 1000):
            raise ValidationError(f"Coordinates out of range: ({x}, {y})")
        
        return x, y
    
    @staticmethod
    def validate_energy(energy: int) -> int:
        """Validate energy amount."""
        try:
            energy = int(energy)
        except (ValueError, TypeError):
            raise ValidationError(f"Energy must be integer, got {energy}")
        
        if energy < 0:
            raise ValidationError(f"Energy cannot be negative: {energy}")
        
        return energy
    
    @staticmethod
    def validate_danger_level(danger: int) -> int:
        """Validate danger level."""
        try:
            danger = int(danger)
        except (ValueError, TypeError):
            raise ValidationError(f"Danger level must be integer, got {danger}")
        
        if not (0 <= danger <= 10):
            raise ValidationError(f"Danger level must be 0-10, got {danger}")
        
        return danger
    
    @staticmethod
    def validate_constellation_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate constellation JSON structure."""
        required_fields = ['stars', 'routes', 'metadata']
        
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
        
        if not isinstance(data['stars'], list):
            raise ValidationError("'stars' must be a list")
        
        if not isinstance(data['routes'], list):
            raise ValidationError("'routes' must be a list")
        
        return data
    
    @staticmethod
    def validate_spaceship_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate spaceship configuration."""
        required_fields = ['fuel_rate', 'danger_penalty', 'initial_life']
        
        for field in required_fields:
            if field not in config:
                raise ValidationError(f"Missing required spaceship config field: {field}")
        
        # Validate numeric fields
        try:
            config['fuel_rate'] = float(config['fuel_rate'])
            config['danger_penalty'] = float(config['danger_penalty'])
            config['initial_life'] = int(config['initial_life'])
        except (ValueError, TypeError) as e:
            raise ValidationError(f"Invalid spaceship config values: {e}")
        
        if config['fuel_rate'] <= 0:
            raise ValidationError("Fuel rate must be positive")
        
        if config['danger_penalty'] < 0:
            raise ValidationError("Danger penalty cannot be negative")
        
        if config['initial_life'] <= 0:
            raise ValidationError("Initial life must be positive")
        
        return config
    
    @staticmethod
    def validate_route_parameters(start: str, goal: Optional[str] = None) -> tuple[str, Optional[str]]:
        """Validate route calculation parameters."""
        start = Validators.validate_star_id(start)
        
        if goal is not None:
            goal = Validators.validate_star_id(goal)
            if start == goal:
                raise ValidationError("Start and goal cannot be the same star")
        
        return start, goal