"""
Gestión de presets predefinidos para el editor de parámetros.
"""
from typing import Dict, List, Tuple
import json


class PresetManager:
    """Gestor de configuraciones predefinidas."""
    
    def __init__(self):
        """Inicializa el gestor con presets predefinidos."""
        self._presets = self._load_default_presets()
    
    def get_presets(self) -> List[Tuple[str, Dict]]:
        """
        Retorna la lista de presets disponibles.
        
        Returns:
            Lista de tuplas (nombre, configuración)
        """
        return list(self._presets.items())
    
    def apply_preset_to_params(self, preset_name: str, params) -> bool:
        """
        Aplica un preset a los parámetros dados.
        
        Args:
            preset_name: Nombre del preset a aplicar
            params: Objeto ResearchParameters a modificar
            
        Returns:
            True si se aplicó correctamente
        """
        if preset_name not in self._presets:
            return False
        
        config = self._presets[preset_name]
        for key, value in config.items():
            if hasattr(params, key):
                setattr(params, key, value)
        
        return True
    
    def get_preset_description(self, preset_name: str) -> str:
        """
        Obtiene la descripción de un preset.
        
        Args:
            preset_name: Nombre del preset
            
        Returns:
            Descripción del preset o cadena vacía si no existe
        """
        descriptions = {
            "🔬 Investigador Intensivo": "Máximo conocimiento, alto consumo energético",
            "⚡ Conservador de Energía": "Mínimo consumo, investigación ligera",
            "🌟 Explorador Rápido": "Balance entre velocidad y conocimiento",
            "🎯 Equilibrado": "Configuración estándar recomendada",
            "💫 Maximizar Conocimiento": "Enfoque total en investigación",
            "🚀 Eficiencia Extrema": "Mínimo tiempo, máxima eficiencia"
        }
        return descriptions.get(preset_name, "")
    
    def _load_default_presets(self) -> Dict[str, Dict]:
        """Carga los presets predefinidos del sistema."""
        return {
            "🔬 Investigador Intensivo": {
                "energy_consumption_rate": 3.0,
                "time_percentage": 0.7,
                "energy_bonus_per_star": 5.0
            },
            "⚡ Conservador de Energía": {
                "energy_consumption_rate": 1.0,
                "time_percentage": 0.3,
                "life_time_bonus": 0.5
            },
            "🌟 Explorador Rápido": {
                "energy_consumption_rate": 1.5,
                "time_percentage": 0.4,
                "knowledge_multiplier": 1.5
            },
            "🎯 Equilibrado": {
                "energy_consumption_rate": 2.0,
                "time_percentage": 0.5,
                "energy_bonus_per_star": 2.0
            },
            "💫 Maximizar Conocimiento": {
                "energy_consumption_rate": 2.5,
                "time_percentage": 0.8,
                "knowledge_multiplier": 2.0
            },
            "🚀 Eficiencia Extrema": {
                "energy_consumption_rate": 0.5,
                "time_percentage": 0.2,
                "life_time_bonus": 1.0
            }
        }
    
    def get_preset_info_text(self) -> str:
        """Retorna texto informativo sobre todos los presets."""
        return (
            "Selecciona un preset para cargar configuraciones predefinidas:\n\n"
            "🔬 Investigador Intensivo: Máximo conocimiento, alto consumo energético\n"
            "⚡ Conservador de Energía: Mínimo consumo, investigación ligera\n"
            "🌟 Explorador Rápido: Balance entre velocidad y conocimiento\n"
            "🎯 Equilibrado: Configuración estándar recomendada\n"
            "💫 Maximizar Conocimiento: Enfoque total en investigación\n"
            "🚀 Eficiencia Extrema: Mínimo tiempo, máxima eficiencia"
        )
    
    def format_preset_applied_text(self, preset_name: str, config: Dict) -> str:
        """
        Formatea el texto que se muestra cuando se aplica un preset.
        
        Args:
            preset_name: Nombre del preset aplicado
            config: Configuración del preset
            
        Returns:
            Texto formateado para mostrar al usuario
        """
        return (f"✅ Preset aplicado: {preset_name}\n\n" + 
                json.dumps(config, indent=2, ensure_ascii=False))