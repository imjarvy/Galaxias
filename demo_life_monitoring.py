"""
Demo del sistema de monitoreo de vida del Burro Astronauta.

Este script demuestra las nuevas funcionalidades implementadas:
- Cálculo de tiempo de vida consumido por distancia
- Monitoreo en tiempo real de vida restante
- Alertas cuando la vida llega a niveles críticos o cero
- Sonidos de muerte de burro
- Integración con la GUI
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models import SpaceMap
from src.life_monitor import LifeMonitor, BasicSoundManager, SimpleAlertSystem
from src.gui_life_monitor import TkinterAlertSystem, LifeEventLogger
import json


def demo_basic_life_monitoring():
    """Demo básico del sistema de monitoreo de vida."""
    print("=" * 60)
    print("🔬 DEMO: Sistema de Monitoreo de Vida del Burro Astronauta")
    print("=" * 60)
    
    # Cargar mapa espacial y crear burro
    space_map = SpaceMap('data/constellations.json')
    burro = space_map.create_burro_astronauta()
    
    # Configurar sistema de monitoreo de vida
    alert_system = SimpleAlertSystem()
    sound_manager = BasicSoundManager()
    life_monitor = LifeMonitor(alert_system, sound_manager)
    event_logger = LifeEventLogger()
    
    # Conectar el monitor al burro
    burro.set_life_monitor(life_monitor)
    life_monitor.add_observer(event_logger)
    
    print(f"\n👤 Burro Astronauta: {burro.name}")
    print(f"🎂 Edad inicial: {burro.start_age} años")
    print(f"⚰️ Edad de muerte: {burro.death_age} años") 
    print(f"💫 Vida total esperada: {burro.death_age - burro.start_age} años")
    print(f"⚡ Energía inicial: {burro.energia_inicial}%")
    
    # Cargar warp factor para mostrar conversiones
    try:
        with open('data/spaceship_config.json', 'r') as f:
            config = json.load(f)
        warp_factor = config['scientific_parameters']['warp_factor']
        print(f"🚀 Warp Factor: {warp_factor}")
    except:
        warp_factor = 1.0
        print(f"🚀 Warp Factor: {warp_factor} (default)")
    
    print(f"\n🔍 Monitor de vida iniciado")
    
    # Simular varios viajes con diferentes distancias
    viajes_demo = [
        {"destino": "Estrella Alpha", "distancia": 50},
        {"destino": "Estrella Beta", "distancia": 120},
        {"destino": "Estrella Gamma", "distancia": 200},
        {"destino": "Estrella Delta", "distancia": 300},
        {"destino": "Estrella Épsilon", "distancia": 500},
        {"destino": "Estrella Final", "distancia": 1000}  # Este debería ser mortal
    ]
    
    print(f"\n🛤️ Simulando {len(viajes_demo)} viajes...")
    print("-" * 60)
    
    for i, viaje in enumerate(viajes_demo, 1):
        destino = viaje['destino']
        distancia = viaje['distancia']
        
        print(f"\n🚀 VIAJE {i}: Hacia {destino}")
        print(f"📏 Distancia: {distancia} unidades espaciales")
        
        # Calcular costo de vida antes del viaje
        vida_costo = burro.calculate_travel_life_cost(distancia)
        vida_antes = burro.get_remaining_life()
        
        print(f"⏰ Costo de vida: {vida_costo:.2f} años")
        print(f"💫 Vida antes del viaje: {vida_antes:.1f} años")
        
        # Verificar si puede sobrevivir
        if not burro.can_survive_travel(distancia):
            print(f"💀 ¡VIAJE MORTAL! El burro no puede sobrevivir este viaje.")
            print(f"   Vida requerida: {vida_costo:.2f} años")
            print(f"   Vida disponible: {vida_antes:.1f} años")
            print(f"   Déficit: {vida_costo - vida_antes:.2f} años")
            break
        
        # Ejecutar viaje
        print(f"🛸 Viajando...")
        burro.consume_resources_traveling(distancia)
        
        # Mostrar estado después del viaje
        vida_despues = burro.get_remaining_life()
        porcentaje_vida = burro.get_life_percentage()
        
        print(f"✅ Viaje completado")
        print(f"💫 Vida después: {vida_despues:.1f} años ({porcentaje_vida:.1f}%)")
        print(f"📈 Edad actual: {burro.current_age:.1f} años")
        print(f"💚 Estado: {burro.estado_salud.title()}")
        print(f"💖 ¿Vivo?: {'Sí' if burro.is_alive() else 'No'}")
        
        # Si murió, detener la simulación
        if not burro.is_alive():
            print(f"💀 El Burro Astronauta ha muerto durante el viaje {i}")
            break
        
        print("-" * 40)
    
    # Mostrar resumen del viaje
    print(f"\n📊 RESUMEN DEL VIAJE")
    print("=" * 60)
    
    status = burro.get_status()
    print(f"👤 Burro: {status['name']}")
    print(f"🎂 Edad inicial: {status['edad_inicial']} años")
    print(f"📅 Edad actual: {status['edad_actual']:.1f} años")
    print(f"⏰ Vida consumida: {status['vida_consumida']:.1f} años")
    print(f"💫 Vida restante: {status['vida_restante']:.1f} años")
    print(f"📊 Porcentaje de vida: {burro.get_life_percentage():.1f}%")
    print(f"💖 Estado final: {'Vivo' if status['is_alive'] else 'Muerto'}")
    
    # Mostrar eventos de vida registrados
    print(f"\n📋 EVENTOS DE VIDA REGISTRADOS:")
    print("-" * 60)
    eventos = event_logger.get_recent_events(10)
    
    if eventos:
        for evento in eventos:
            print(f"⏰ {evento.timestamp.strftime('%H:%M:%S')} - {evento.event_type.value.upper()}")
            print(f"   💬 {evento.message}")
            print(f"   📊 Vida restante: {evento.remaining_life:.1f} años")
            if evento.life_consumed > 0:
                print(f"   🔥 Vida consumida: {evento.life_consumed:.2f} años")
            print()
    else:
        print("   (Sin eventos registrados)")
    
    # Obtener resumen completo del monitor
    if life_monitor.is_monitoring:
        travel_summary = life_monitor.get_travel_summary()
        print(f"\n📈 ESTADÍSTICAS DEL MONITOR:")
        print("-" * 60)
        print(f"📊 Total de eventos: {travel_summary['total_events']}")
        print(f"🛤️ Viajes realizados: {travel_summary['summary']['trips_made']}")
        print(f"⚠️ Advertencias emitidas: {travel_summary['summary']['warnings_issued']}")
        print(f"🚨 Alertas críticas: {travel_summary['summary']['critical_alerts']}")
        print(f"💀 Muerte registrada: {'Sí' if travel_summary['summary']['died'] else 'No'}")
    
    print(f"\n🎯 DEMO COMPLETADO")
    print("=" * 60)


def demo_distance_calculations():
    """Demo de cálculos de distancia y tiempo de vida."""
    print("\n🔢 DEMO: Cálculos de Distancia vs Tiempo de Vida")
    print("=" * 60)
    
    # Cargar configuración
    try:
        with open('data/spaceship_config.json', 'r') as f:
            config = json.load(f)
        warp_factor = config['scientific_parameters']['warp_factor']
    except:
        warp_factor = 1.0
    
    print(f"🚀 Warp Factor configurado: {warp_factor}")
    print(f"📏 Conversión: 1 unidad de distancia = {1/warp_factor:.2f} años de vida\n")
    
    # Ejemplos de conversión
    distancias_demo = [10, 25, 50, 100, 200, 500, 1000, 1500]
    
    print("TABLA DE CONVERSIÓN DISTANCIA → TIEMPO DE VIDA:")
    print("-" * 50)
    print(f"{'Distancia':>10} {'Tiempo de Vida':>15} {'Equivale a':>20}")
    print("-" * 50)
    
    for distancia in distancias_demo:
        tiempo_vida = distancia / warp_factor
        
        # Crear descripciones amigables
        if tiempo_vida < 1:
            equivalencia = f"{tiempo_vida*12:.1f} meses"
        elif tiempo_vida < 10:
            equivalencia = f"{tiempo_vida:.1f} años"
        elif tiempo_vida < 100:
            equivalencia = f"{tiempo_vida:.0f} años"
        else:
            equivalencia = f"{tiempo_vida/100:.1f} siglos"
        
        print(f"{distancia:>10} {tiempo_vida:>13.2f} años {equivalencia:>20}")
    
    print("-" * 50)
    print(f"💡 Con warp_factor = {warp_factor}, viajes más largos consumen menos tiempo de vida")


def main():
    """Función principal del demo."""
    try:
        # Demo de cálculos básicos
        demo_distance_calculations()
        
        # Demo del sistema completo
        demo_basic_life_monitoring()
        
        print(f"\n✨ ¡Sistema de monitoreo de vida implementado exitosamente!")
        print(f"🎮 Para probarlo con GUI, ejecute: python src/gui.py")
        
    except Exception as e:
        print(f"❌ Error en el demo: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()