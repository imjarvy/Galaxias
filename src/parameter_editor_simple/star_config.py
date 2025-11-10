"""
Utilidades para la configuración específica de estrellas.
"""
from typing import Dict, Optional


class StarConfigManager:
    """Gestor de configuraciones específicas por estrella."""
    
    def __init__(self, space_map, research_params):
        """
        Inicializa el gestor.
        
        Args:
            space_map: Mapa espacial con información de estrellas
            research_params: Parámetros de investigación
        """
        self.space_map = space_map
        self.research_params = research_params
    
    def get_star_display_data(self) -> list:
        """
        Obtiene datos de todas las estrellas para mostrar en la tabla.
        
        Returns:
            Lista de tuplas con datos de cada estrella para el TreeView
        """
        stars_data = []
        
        for star in self.space_map.get_all_stars_list():
            star_type = "Hipergigante" if star.hypergiant else "Normal"
            
            # Obtener configuración específica si existe
            star_config = self.research_params.custom_star_settings.get(star.id, {})
            energy_rate = star_config.get('energy_rate', self.research_params.energy_consumption_rate)
            time_bonus = star_config.get('time_bonus', self.research_params.life_time_bonus)
            energy_bonus = star_config.get('energy_bonus', self.research_params.energy_bonus_per_star)
            
            stars_data.append((
                star.id,
                star.label,
                star_type,
                f"{energy_rate:.1f}%",
                f"{time_bonus:+.1f}a",
                f"{energy_bonus:+.1f}%"
            ))
        
        return stars_data
    
    def get_star_config(self, star_id: str) -> Dict:
        """
        Obtiene la configuración actual de una estrella.
        
        Args:
            star_id: ID de la estrella
            
        Returns:
            Diccionario con la configuración actual
        """
        current_config = self.research_params.custom_star_settings.get(star_id, {})
        
        return {
            'energy_rate': current_config.get('energy_rate', self.research_params.energy_consumption_rate),
            'time_bonus': current_config.get('time_bonus', self.research_params.life_time_bonus),
            'energy_bonus': current_config.get('energy_bonus', self.research_params.energy_bonus_per_star)
        }
    
    def save_star_config(self, star_id: str, energy_rate: float, 
                        time_bonus: float, energy_bonus: float):
        """
        Guarda la configuración de una estrella.
        
        Args:
            star_id: ID de la estrella
            energy_rate: Consumo de energía
            time_bonus: Bonus de tiempo
            energy_bonus: Bonus de energía
        """
        self.research_params.custom_star_settings[star_id] = {
            'energy_rate': energy_rate,
            'time_bonus': time_bonus,
            'energy_bonus': energy_bonus
        }
    
    def reset_star_config(self, star_id: str) -> bool:
        """
        Resetea la configuración de una estrella a valores por defecto.
        
        Args:
            star_id: ID de la estrella
            
        Returns:
            True si se reseteó, False si no tenía configuración específica
        """
        if star_id in self.research_params.custom_star_settings:
            del self.research_params.custom_star_settings[star_id]
            return True
        return False
    
    def reset_all_stars(self):
        """Resetea todas las configuraciones específicas de estrellas."""
        self.research_params.custom_star_settings.clear()
    
    def get_star_name(self, star_id: str) -> str:
        """
        Obtiene el nombre de una estrella por su ID.
        
        Args:
            star_id: ID de la estrella
            
        Returns:
            Nombre de la estrella o ID si no se encuentra
        """
        star = self.space_map.get_star(star_id)
        return star.label if star else f"ID:{star_id}"