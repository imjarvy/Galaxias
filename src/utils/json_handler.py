"""
JSON handling utilities for the Galaxias system.
Centralizes all JSON reading/writing operations.
"""
import json
import os
from typing import Dict, Any, Optional

class JSONHandler:
    """Centralized JSON file operations."""
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """Load JSON file with error handling."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"JSON file not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str) -> None:
        """Save data to JSON file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise IOError(f"Error saving JSON to {file_path}: {e}")
    
    @staticmethod
    def load_constellations(file_path: str = "data/constellations.json") -> Dict[str, Any]:
        """Load constellation data specifically."""
        return JSONHandler.load_json(file_path)
    
    @staticmethod
    def load_spaceship_config(file_path: str = "data/spaceship_config.json") -> Dict[str, Any]:
        """Load spaceship configuration specifically."""
        return JSONHandler.load_json(file_path)