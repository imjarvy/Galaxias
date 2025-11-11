"""
Modelos de datos para el editor de parámetros.
Separado del archivo principal para mayor claridad.
"""
from dataclasses import dataclass
from typing import Dict


@dataclass
class ResearchParameters:
    def to_dict(self):
        return {
            'energy_consumption_rate': self.energy_consumption_rate,
            'time_percentage': self.time_percentage,
            'life_time_bonus': self.life_time_bonus,
            'energy_bonus_per_star': self.energy_bonus_per_star,
            'knowledge_multiplier': self.knowledge_multiplier,
            'custom_star_settings': self.custom_star_settings
        }

    @staticmethod
    def from_dict(data):
        return ResearchParameters(
            energy_consumption_rate=data.get('energy_consumption_rate', 2.0),
            time_percentage=data.get('time_percentage', 0.5),
            life_time_bonus=data.get('life_time_bonus', 0.0),
            energy_bonus_per_star=data.get('energy_bonus_per_star', 0.0),
            knowledge_multiplier=data.get('knowledge_multiplier', 1.0),
            custom_star_settings=data.get('custom_star_settings', {})
        )
    """Parámetros configurables para la investigación en estrellas."""
    energy_consumption_rate: float = 2.0  # Energía consumida por unidad de tiempo
    time_percentage: float = 0.5           # Porcentaje del tiempo dedicado a investigación (50%)
    life_time_bonus: float = 0.0           # Bonus/penalty de tiempo de vida por investigación
    energy_bonus_per_star: float = 0.0     # Bonus de energía por estrella investigada
    knowledge_multiplier: float = 1.0      # Multiplicador de conocimiento por tipo de estrella
    custom_star_settings: Dict[str, Dict] = None  # Configuraciones específicas por estrella
    
    def __post_init__(self):
        if self.custom_star_settings is None:
            self.custom_star_settings = {}
    
    def copy(self):
        """Crea una copia de los parámetros."""
        return ResearchParameters(
            energy_consumption_rate=self.energy_consumption_rate,
            time_percentage=self.time_percentage,
            life_time_bonus=self.life_time_bonus,
            energy_bonus_per_star=self.energy_bonus_per_star,
            knowledge_multiplier=self.knowledge_multiplier,
            custom_star_settings=self.custom_star_settings.copy()
        )