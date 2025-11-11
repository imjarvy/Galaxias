"""
Parameter Editor Simple - Versión organizada y legible.

Este paquete contiene una refactorización del editor de parámetros original,
organizando el código en módulos separados para mayor legibilidad y mantenimiento.

Estructura:
- models.py: Definición de ResearchParameters
- presets.py: Gestión de configuraciones predefinidas  
- star_config.py: Lógica de configuración específica por estrella
- preview.py: Generación de texto de vista previa
- editor.py: Interfaz principal del editor

Uso:
    from src.parameter_editor_simple import ResearchParameterEditor, ResearchParameters
    
    # Crear parámetros
    params = ResearchParameters()
    
    # Crear editor
    editor = ResearchParameterEditor(parent_window, space_map, params)
    
    # Obtener resultado
    result = editor.get_parameters()
"""

from .models import ResearchParameters
from .editor import ResearchParameterEditor
from .presets import PresetManager
from .star_config import StarConfigManager
from .preview import PreviewGenerator
from .comet_manager import CometManager

__all__ = [
    'ResearchParameters',
    'ResearchParameterEditor', 
    'PresetManager',
    'StarConfigManager',
    'PreviewGenerator',
    'CometManager'
]

__version__ = "1.0.0"