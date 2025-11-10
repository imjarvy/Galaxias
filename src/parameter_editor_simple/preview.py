"""
Generador de vista previa para los parámetros de investigación.
"""


class PreviewGenerator:
    """Generador de texto de vista previa para configuraciones."""
    
    def __init__(self, space_map):
        """
        Inicializa el generador.
        
        Args:
            space_map: Mapa espacial para obtener nombres de estrellas
        """
        self.space_map = space_map
    
    def generate_preview_text(self, params) -> str:
        """
        Genera texto de vista previa completo para los parámetros.
        
        Args:
            params: Objeto ResearchParameters
            
        Returns:
            Texto formateado para mostrar en la vista previa
        """
        # Encabezado
        preview_text = (
            "🔬 CONFIGURACIÓN DE PARÁMETROS DE INVESTIGACIÓN\n"
            + "=" * 50 + "\n\n"
        )
        
        # Parámetros generales
        preview_text += self._format_general_params(params)
        
        # Configuraciones específicas
        preview_text += self._format_star_configs(params)
        
        # Estimaciones de impacto
        preview_text += self._format_impact_estimates(params)
        
        return preview_text
    
    def _format_general_params(self, params) -> str:
        """Formatea los parámetros generales."""
        return (
            "⚙️ PARÁMETROS GENERALES:\n"
            f"   ⚡ Consumo de energía: {params.energy_consumption_rate:.1f}% por unidad tiempo\n"
            f"   ⏰ Tiempo investigación: {params.time_percentage*100:.1f}%\n"
            f"   💫 Bonus tiempo vida: {params.life_time_bonus:+.1f} años por estrella\n"
            f"   🔋 Bonus energía: {params.energy_bonus_per_star:+.1f}% por estrella\n"
            f"   📚 Multiplicador: {params.knowledge_multiplier:.1f}x\n\n"
        )
    
    def _format_star_configs(self, params) -> str:
        """Formatea las configuraciones específicas por estrella."""
        star_text = "⭐ CONFIGURACIONES ESPECÍFICAS POR ESTRELLA:\n"
        
        if params.custom_star_settings:
            for star_id, config in params.custom_star_settings.items():
                star_name = self._get_star_name(star_id)
                star_text += (
                    f"\n   🌟 {star_name} (ID: {star_id}):\n"
                    f"      ⚡ Consumo: {config.get('energy_rate', 'default'):.1f}%\n"
                    f"      💫 Bonus tiempo: {config.get('time_bonus', 'default'):+.1f}a\n"
                    f"      🔋 Bonus energía: {config.get('energy_bonus', 'default'):+.1f}%\n"
                )
        else:
            star_text += "\n   (Ninguna configuración específica - usando valores generales)\n"
        
        return star_text + "\n"
    
    def _format_impact_estimates(self, params) -> str:
        """Formatea las estimaciones de impacto."""
        return (
            "=" * 50 + "\n"
            "📊 IMPACTO ESTIMADO:\n"
            f"   • Estrellas con configuración específica: {len(params.custom_star_settings)}\n"
            f"   • Tiempo promedio por estrella: {3 * params.time_percentage:.1f} unidades\n"
            f"   • Consumo promedio por estrella: {3 * params.time_percentage * params.energy_consumption_rate:.1f}%\n"
        )
    
    def _get_star_name(self, star_id: str) -> str:
        """Obtiene el nombre de una estrella por su ID."""
        star = self.space_map.get_star(star_id)
        return star.label if star else f"ID:{star_id}"