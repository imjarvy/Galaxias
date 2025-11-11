"""
Sistema de monitoreo de tiempo de vida del Burro Astronauta.

Este módulo implementa el seguimiento detallado del consumo de vida por distancia
y emite eventos/alertas cuando la vida llega a niveles críticos o cero.

Principios SOLID aplicados:
- SRP: Cada clase tiene una responsabilidad específica
- OCP: Sistema extensible para nuevos tipos de eventos
- LSP: Interfaces bien definidas
- ISP: Interfaces específicas por funcionalidad  
- DIP: Dependencias por abstracción
"""
import json
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from datetime import datetime


class LifeEventType(Enum):
    """Tipos de eventos de vida."""
    LIFE_WARNING = "vida_advertencia"
    LIFE_CRITICAL = "vida_critica" 
    LIFE_DEATH = "muerte_burro"
    TRAVEL_START = "inicio_viaje"
    TRAVEL_END = "fin_viaje"
    LIFE_CONSUMED = "vida_consumida"


@dataclass
class LifeEvent:
    """Representa un evento relacionado con el tiempo de vida."""
    event_type: LifeEventType
    current_age: float
    remaining_life: float
    life_consumed: float
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convierte el evento a diccionario."""
        return {
            'type': self.event_type.value,
            'current_age': self.current_age,
            'remaining_life': self.remaining_life, 
            'life_consumed': self.life_consumed,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


class ILifeObserver(ABC):
    """Interfaz para observadores de eventos de vida."""
    
    @abstractmethod
    def handle_life_event(self, event: LifeEvent):
        """Maneja un evento de vida."""
        pass


class IAlertSystem(ABC):
    """Interfaz para sistemas de alertas."""
    
    @abstractmethod
    def show_warning(self, title: str, message: str):
        """Muestra una advertencia."""
        pass
    
    @abstractmethod 
    def show_error(self, title: str, message: str):
        """Muestra un error."""
        pass
    
    @abstractmethod
    def show_info(self, title: str, message: str):
        """Muestra información."""
        pass


class ISoundManager(ABC):
    """Interfaz para manejo de sonidos."""
    
    @abstractmethod
    def play_warning_sound(self):
        """Reproduce sonido de advertencia."""
        pass
    
    @abstractmethod
    def play_death_sound(self):
        """Reproduce sonido de muerte de burro."""
        pass
    
    @abstractmethod
    def play_travel_sound(self):
        """Reproduce sonido de viaje."""
        pass


class SimpleAlertSystem(IAlertSystem):
    """Sistema de alertas simple usando print."""
    
    def show_warning(self, title: str, message: str):
        print(f"⚠️  ADVERTENCIA - {title}: {message}")
    
    def show_error(self, title: str, message: str):
        print(f"❌ ERROR - {title}: {message}")
    
    def show_info(self, title: str, message: str):
        print(f"ℹ️  INFO - {title}: {message}")


class BasicSoundManager(ISoundManager):
    """Gestor de sonidos básico (placeholder)."""
    
    def play_warning_sound(self):
        """Reproduce sonido de advertencia (simulado)."""
        print("🔔 *Sonido de advertencia*")
    
    def play_death_sound(self):
        """Reproduce sonido de muerte de burro (simulado).""" 
        print("💀 *Sonido de muerte de burro: BRAY-YYYY...*")
    
    def play_travel_sound(self):
        """Reproduce sonido de viaje (simulado)."""
        print("🚀 *Sonido de viaje espacial: WHOOSH*")


# Implementación avanzada de sonido (opcional)
try:
    import pygame
    
    class PygameSoundManager(ISoundManager):
        """Gestor de sonidos usando pygame."""
        
        def __init__(self, sound_config: Optional[Dict[str, str]] = None):
            """
            Inicializa el gestor de sonidos.
            
            Args:
                sound_config: Dict con rutas a archivos de sonido
                              {'warning': 'path/to/warning.wav', ...}
            """
            pygame.mixer.init()
            self.sounds = {}
            
            default_config = {
                'warning': 'assets/sounds/warning.wav',
                'death': 'assets/sounds/death_burro.wav', 
                'travel': 'assets/sounds/travel.wav'
            }
            
            config = sound_config or default_config
            
            # Cargar sonidos si existen los archivos
            for key, path in config.items():
                try:
                    self.sounds[key] = pygame.mixer.Sound(path)
                except pygame.error:
                    print(f"No se pudo cargar sonido: {path}")
                    self.sounds[key] = None
        
        def play_warning_sound(self):
            if self.sounds.get('warning'):
                self.sounds['warning'].play()
            else:
                print("🔔 *Sonido de advertencia*")
        
        def play_death_sound(self):
            if self.sounds.get('death'):
                self.sounds['death'].play()
            else:
                print("💀 *Sonido de muerte de burro*")
        
        def play_travel_sound(self):
            if self.sounds.get('travel'):
                self.sounds['travel'].play()
            else:
                print("🚀 *Sonido de viaje*")

except ImportError:
    # Si pygame no está disponible, crear clase placeholder
    class PygameSoundManager:
        def __init__(self, *args, **kwargs):
            raise ImportError("pygame no está disponible. Use BasicSoundManager.")


class LifeDistanceCalculator:
    """Calculadora de consumo de vida por distancia."""
    
    def __init__(self, config_path: str = "data/spaceship_config.json"):
        """
        Inicializa el calculador.
        
        Args:
            config_path: Ruta al archivo de configuración con warp_factor
        """
        self.warp_factor = self._load_warp_factor(config_path)
    
    def _load_warp_factor(self, config_path: str) -> float:
        """Carga el warp factor del archivo de configuración."""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            return config.get('scientific_parameters', {}).get('warp_factor', 1.0)
        except Exception:
            return 1.0
    
    def distance_to_life_years(self, distance: float) -> float:
        """
        Convierte distancia a tiempo de vida consumido en años.
        
        Args:
            distance: Distancia en unidades espaciales
            
        Returns:
            float: Tiempo de vida consumido en años
        """
        return distance / self.warp_factor
    
    def life_years_to_distance(self, life_years: float) -> float:
        """
        Convierte tiempo de vida en años a distancia equivalente.
        
        Args:
            life_years: Tiempo de vida en años
            
        Returns:
            float: Distancia equivalente en unidades espaciales
        """
        return life_years * self.warp_factor


class LifeMonitor:
    """Monitor principal del tiempo de vida del Burro Astronauta."""
    
    def __init__(self, 
                 alert_system: Optional[IAlertSystem] = None,
                 sound_manager: Optional[ISoundManager] = None,
                 config_path: str = "data/spaceship_config.json"):
        """
        Inicializa el monitor de vida.
        
        Args:
            alert_system: Sistema de alertas a usar
            sound_manager: Gestor de sonidos a usar 
            config_path: Ruta al archivo de configuración
        """
        self.alert_system = alert_system or SimpleAlertSystem()
        self.sound_manager = sound_manager or BasicSoundManager()
        self.calculator = LifeDistanceCalculator(config_path)
        
        # Estado del monitoreo
        self.current_age: float = 0.0
        self.death_age: float = 0.0
        self.total_life_consumed: float = 0.0
        self.is_monitoring: bool = False
        
        # Umbrales de alerta (porcentajes de vida restante)
        self.warning_threshold: float = 0.25  # 25% vida restante
        self.critical_threshold: float = 0.10  # 10% vida restante
        
        # Observadores de eventos
        self.observers: List[ILifeObserver] = []
        
        # Historial de eventos
        self.event_history: List[LifeEvent] = []
    
    def add_observer(self, observer: ILifeObserver):
        """Agrega un observador de eventos de vida."""
        self.observers.append(observer)
    
    def remove_observer(self, observer: ILifeObserver):
        """Remueve un observador de eventos de vida."""
        if observer in self.observers:
            self.observers.remove(observer)
    
    def start_monitoring(self, initial_age: float, death_age: float):
        """
        Inicia el monitoreo de vida.
        
        Args:
            initial_age: Edad inicial del burro en años
            death_age: Edad de muerte del burro en años
        """
        self.current_age = initial_age
        self.death_age = death_age
        self.total_life_consumed = 0.0
        self.is_monitoring = True
        
        self._emit_event(LifeEventType.TRAVEL_START,
                        message=f"Iniciando monitoreo de vida. Edad: {initial_age} años, "
                               f"Esperanza: {death_age} años")
    
    def stop_monitoring(self):
        """Detiene el monitoreo de vida."""
        self.is_monitoring = False
        self._emit_event(LifeEventType.TRAVEL_END,
                        message="Monitoreo de vida detenido")
    
    def consume_life_for_travel(self, distance: float) -> Dict[str, float]:
        """
        Consume tiempo de vida por un viaje de cierta distancia.
        
        Args:
            distance: Distancia del viaje
            
        Returns:
            Dict con información del consumo
        """
        if not self.is_monitoring:
            raise ValueError("Monitor de vida no está activo")
        
        # Calcular tiempo de vida consumido
        life_consumed = self.calculator.distance_to_life_years(distance)
        
        # Actualizar estado
        self.current_age += life_consumed
        self.total_life_consumed += life_consumed
        remaining_life = max(0, self.death_age - self.current_age)
        
        # Crear resultado
        result = {
            'distance': distance,
            'life_consumed': life_consumed,
            'current_age': self.current_age,
            'remaining_life': remaining_life,
            'death_imminent': remaining_life <= 0
        }
        
        # Emitir evento de consumo
        self._emit_event(LifeEventType.LIFE_CONSUMED,
                        life_consumed=life_consumed,
                        message=f"Viaje consumió {life_consumed:.2f} años de vida")
        
        # Verificar alertas
        self._check_life_alerts(remaining_life)
        
        return result
    
    def get_remaining_life(self) -> float:
        """Obtiene el tiempo de vida restante en años."""
        return max(0, self.death_age - self.current_age)
    
    def get_life_percentage(self) -> float:
        """Obtiene el porcentaje de vida restante."""
        total_life = self.death_age - (self.death_age - self.total_life_consumed - (self.death_age - self.current_age + self.total_life_consumed))
        if total_life <= 0:
            return 0.0
        return (self.get_remaining_life() / (self.death_age - (self.current_age - self.total_life_consumed))) * 100
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado completo del monitor."""
        remaining_life = self.get_remaining_life()
        return {
            'is_monitoring': self.is_monitoring,
            'current_age': self.current_age,
            'death_age': self.death_age,
            'remaining_life': remaining_life,
            'life_percentage': self.get_life_percentage(),
            'total_consumed': self.total_life_consumed,
            'is_alive': remaining_life > 0,
            'warp_factor': self.calculator.warp_factor
        }
    
    def _check_life_alerts(self, remaining_life: float):
        """Verifica y emite alertas según el tiempo de vida restante."""
        life_percentage = self.get_life_percentage()
        
        if remaining_life <= 0:
            # Muerte
            self._emit_event(LifeEventType.LIFE_DEATH,
                           message="¡El Burro Astronauta ha muerto!")
            self.alert_system.show_error("💀 ¡MUERTE DEL BURRO!",
                                       "El Burro Astronauta ha agotado su tiempo de vida.")
            self.sound_manager.play_death_sound()
            
        elif life_percentage <= self.critical_threshold * 100:
            # Vida crítica
            self._emit_event(LifeEventType.LIFE_CRITICAL,
                           message=f"¡Vida crítica! Solo {remaining_life:.1f} años restantes")
            self.alert_system.show_error("🚨 VIDA CRÍTICA",
                                       f"Solo {remaining_life:.1f} años de vida restantes!")
            self.sound_manager.play_warning_sound()
            
        elif life_percentage <= self.warning_threshold * 100:
            # Advertencia de vida baja
            self._emit_event(LifeEventType.LIFE_WARNING,
                           message=f"Advertencia: {remaining_life:.1f} años de vida restantes")
            self.alert_system.show_warning("⚠️ VIDA BAJA",
                                         f"Cuidado: {remaining_life:.1f} años de vida restantes")
            self.sound_manager.play_warning_sound()
    
    def _emit_event(self, event_type: LifeEventType, life_consumed: float = 0.0, message: str = ""):
        """Emite un evento de vida a todos los observadores."""
        event = LifeEvent(
            event_type=event_type,
            current_age=self.current_age,
            remaining_life=self.get_remaining_life(),
            life_consumed=life_consumed,
            message=message
        )
        
        # Agregar al historial
        self.event_history.append(event)
        
        # Notificar a observadores
        for observer in self.observers:
            try:
                observer.handle_life_event(event)
            except Exception as e:
                print(f"Error notificando observador: {e}")
    
    def get_travel_summary(self) -> Dict[str, Any]:
        """Obtiene un resumen del viaje con consumo de vida."""
        events_by_type = {}
        for event in self.event_history:
            event_type = event.event_type.value
            if event_type not in events_by_type:
                events_by_type[event_type] = []
            events_by_type[event_type].append(event.to_dict())
        
        return {
            'total_events': len(self.event_history),
            'events_by_type': events_by_type,
            'current_status': self.get_status(),
            'summary': {
                'total_life_consumed': self.total_life_consumed,
                'remaining_life': self.get_remaining_life(), 
                'trips_made': len(events_by_type.get('vida_consumida', [])),
                'warnings_issued': len(events_by_type.get('vida_advertencia', [])),
                'critical_alerts': len(events_by_type.get('vida_critica', [])),
                'died': len(events_by_type.get('muerte_burro', [])) > 0
            }
        }


class LifeMonitorObserver(ILifeObserver):
    """Observador de ejemplo para eventos de vida."""
    
    def __init__(self, name: str):
        self.name = name
        self.events_received = []
    
    def handle_life_event(self, event: LifeEvent):
        """Maneja un evento de vida."""
        self.events_received.append(event)
        print(f"[{self.name}] Evento: {event.event_type.value} - {event.message}")