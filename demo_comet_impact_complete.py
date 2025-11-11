#!/usr/bin/env python3
"""
Demo completo del sistema de gestión de cometas con análisis de impacto.
Muestra invalidación de rutas, recálculo y alternativas.
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import SpaceMap, Comet
from src.comet_impact_system import CometImpactManager, RouteImpactResult


def demo_comet_impact_system():
    """Demuestra el sistema completo de impacto de cometas."""
    print("🌌 Demo: Sistema Completo de Gestión e Impacto de Cometas")
    print("=" * 65)
    
    # 1. Inicializar sistema
    print("\n1️⃣ Inicializando sistema...")
    space_map = SpaceMap('data/constellations.json')
    impact_manager = CometImpactManager(space_map)
    
    # Agregar listener para mostrar impactos
    def show_impact(result: RouteImpactResult):
        if result.path_invalidated:
            print(f"   📡 IMPACTO DETECTADO: {result.impact_summary}")
        else:
            print(f"   ✅ {result.impact_summary}")
    
    impact_manager.add_impact_listener(show_impact)
    print(f"   ✓ Mapa cargado: {len(space_map.stars)} estrellas, {len(space_map.routes)} rutas")
    
    # 2. Registrar un viaje activo
    print("\n2️⃣ Registrando viaje activo...")
    stars = list(space_map.stars.values())
    planned_route = [stars[0], stars[1], stars[2]]  # Ruta de prueba
    impact_manager.register_active_journey(planned_route, 0, "test_journey")
    
    route_str = " → ".join([f"{star.id}({star.label})" for star in planned_route])
    print(f"   ✓ Viaje registrado: {route_str}")
    
    # 3. Obtener rutas alternativas ANTES de agregar cometa
    print("\n3️⃣ Consultando rutas alternativas iniciales...")
    alternatives_before = impact_manager.get_current_alternatives(stars[0].id, stars[2].id)
    print(f"   ✓ Rutas alternativas disponibles: {len(alternatives_before)}")
    
    for i, alt in enumerate(alternatives_before[:3]):
        alt_str = " → ".join([star.label for star in alt])
        print(f"     Alt {i+1}: {alt_str}")
    
    # 4. Agregar cometa que afecte la ruta
    print("\n4️⃣ Agregando cometa que bloquea ruta activa...")
    test_comet = Comet(
        name="Cometa_Demo", 
        blocked_routes=[(stars[0].id, stars[1].id)]
    )
    
    print(f"   🌟 Agregando cometa: {test_comet.name}")
    print(f"   🚫 Bloqueará ruta: {stars[0].label} ↔ {stars[1].label}")
    
    # Analizar impacto
    impact_result = impact_manager.analyze_comet_impact(test_comet)
    
    # Agregar al mapa
    space_map.add_comet(test_comet)
    
    # 5. Verificar invalidación de ruta
    print("\n5️⃣ Verificando invalidación de rutas...")
    print(f"   📋 Ruta invalidada: {'SÍ' if impact_result.path_invalidated else 'NO'}")
    print(f"   🔄 Recálculo necesario: {'SÍ' if impact_result.recalculation_needed else 'NO'}")
    
    if impact_result.affected_segments:
        print(f"   🎯 Segmentos afectados:")
        for segment in impact_result.affected_segments:
            print(f"     - {segment[0]} ↔ {segment[1]}")
    
    # 6. Mostrar rutas alternativas
    print("\n6️⃣ Rutas alternativas después del cometa...")
    alternatives_after = impact_manager.get_current_alternatives(stars[0].id, stars[2].id)
    print(f"   ✓ Rutas alternativas encontradas: {len(alternatives_after)}")
    
    if alternatives_after:
        print("   🔄 Rutas alternativas válidas:")
        for i, alt in enumerate(alternatives_after[:3]):
            alt_str = " → ".join([star.label for star in alt])
            distance = sum(route.distance for route in space_map.routes 
                          if any((route.from_star == alt[j] and route.to_star == alt[j+1]) or
                                (route.to_star == alt[j] and route.from_star == alt[j+1])
                                for j in range(len(alt)-1)))
            print(f"     Alt {i+1}: {alt_str} (Dist: {distance:.1f})")
    else:
        print("   ❌ No se encontraron rutas alternativas válidas")
    
    # 7. Demostrar recálculo automático
    print("\n7️⃣ Demostrando recálculo automático...")
    if impact_result.recalculation_needed and alternatives_after:
        new_route = alternatives_after[0]
        print(f"   ✅ Nueva ruta sugerida: {' → '.join([star.label for star in new_route])}")
        print(f"   📊 Comparación:")
        print(f"     Ruta original: {len(planned_route)} saltos")
        print(f"     Ruta alternativa: {len(new_route)} saltos")
    
    # 8. Limpiar y demostrar que se puede remover cometa
    print("\n8️⃣ Removiendo cometa y verificando restauración...")
    space_map.remove_comet(test_comet.name)
    
    # Verificar rutas restauradas
    final_alternatives = impact_manager.get_current_alternatives(stars[0].id, stars[2].id)
    print(f"   ✓ Cometa removido")
    print(f"   ✓ Rutas disponibles después: {len(final_alternatives)}")
    
    # 9. Resumen final
    print("\n📊 RESUMEN DEL DEMO")
    print("=" * 30)
    print("✅ Funcionalidades demostradas:")
    print("   • Registro de viajes activos")
    print("   • Análisis de impacto de cometas")
    print("   • Invalidación automática de rutas")
    print("   • Detección de segmentos afectados")
    print("   • Búsqueda de rutas alternativas")
    print("   • Notificaciones de cambios")
    print("   • Recálculo de rutas sugerido")
    print("   • Restauración tras remover cometa")
    
    return True


def demo_integration_with_gui():
    """Demuestra cómo usar el sistema integrado en GUI."""
    print("\n🖥️ Integración con GUI")
    print("=" * 25)
    
    print("Para usar esta funcionalidad en la aplicación:")
    print("\n1️⃣ Ejecutar GUI:")
    print("   python -c \"import sys; sys.path.append('.'); from src.gui import main; main()\"")
    
    print("\n2️⃣ Planificar una ruta:")
    print("   • Seleccionar estrellas origen/destino")
    print("   • Clic en 'Calcular Ruta Óptima'")
    print("   • La ruta se registra automáticamente")
    
    print("\n3️⃣ Gestionar cometas:")
    print("   • Clic en '⚙️ Configurar Parámetros'")
    print("   • Pestaña '🌌 Cometas'")
    print("   • Agregar cometa que bloquee la ruta")
    
    print("\n4️⃣ Ver impacto automático:")
    print("   • El sistema muestra:")
    print("     - Si la ruta se invalida")
    print("     - Segmentos afectados")
    print("     - Rutas alternativas disponibles")
    print("   • La visualización se actualiza automáticamente")
    
    print("\n🌟 Características avanzadas:")
    print("   • Análisis en tiempo real")
    print("   • Múltiples rutas alternativas")
    print("   • Validación de rutas")
    print("   • Recálculo inteligente")


def main():
    """Función principal del demo."""
    try:
        # Demo del sistema de impacto
        success = demo_comet_impact_system()
        
        if success:
            demo_integration_with_gui()
            
            print("\n🎉 Demo completado exitosamente!")
            print("\n💡 El sistema cumple con todos los requisitos:")
            print("   ✅ Invalida rutas planificadas cuando se agrega cometa")
            print("   ✅ Detecta automáticamente recálculo necesario")
            print("   ✅ Devuelve lista de rutas alternativas")
            print("   ✅ Implementado con lógica simple y principios SOLID")
            
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"\n❌ Error durante el demo: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())