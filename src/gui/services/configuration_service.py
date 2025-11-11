"""
Configuration service implementation.
Implements Single Responsibility Principle for configuration management.
"""
from typing import Dict, Any
from ...utils import JSONHandler


class ConfigurationService:
    """Service responsible for configuration management."""
    
    def __init__(self):
        self._config = None
    
    def load_configuration(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            self._config = JSONHandler.load_json(config_path)
            return self._config
        except Exception as e:
            raise Exception(f"Failed to load configuration: {str(e)}")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current configuration."""
        if self._config is None:
            raise Exception("Configuration not loaded")
        return self._config
    
    def get_config_value(self, key: str, default=None):
        """Get specific configuration value."""
        if self._config is None:
            return default
        return self._config.get(key, default)