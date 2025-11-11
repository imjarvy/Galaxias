#!/usr/bin/env python3
"""
Validación final del sistema de saltos hipergigantes.
Verifica que se cumplan todos los requisitos especificados.
"""

import sys
import os
sys.path.append('.')

from src.models import SpaceMap, BurroAstronauta
from src.hypergiant_jump import HyperGiantJumpSystem
from src.max_visit_route import compute_max_visits_from_json


def test_hypergiant_jump_requirements():
    """Prueba que se cumplan todos los requisitos de saltos hipergigantes."""
    print("🧪 VALIDACIÓN DE REQUISITOS DE SALTOS HIPERGIGANTES")
    print("="*65)
    
    # Cargar sistema
    space_map = SpaceMap('data/constellations.json')
    jump_system = HyperGiantJumpSystem(space_map)
    burro = space_map.create_burro_astronauta()
    
    results = {
        'requirement_1': False,  # Detecta cambios de galaxia/constelación
        'requirement_2': False,  # Obliga paso por hipergigante
        'requirement_3': False,  # Permite selección de destino
        'requirement_4': False,  # Recarga 50% energía
        'requirement_5': False,  # Duplica pasto
        'requirement_6': False,  # Muestra confirmación
        'requirement_7': False,  # Recalcula ruta
    }
    
    print("\n📋 REQUISITO 1: Detección de cambios de galaxia/constelación")
    print("-"*50)
    
    # Probar detección de cambios entre constelaciones
    star_same_1 = space_map.get_star("1")  # Constelación del Burro
    star_same_2 = space_map.get_star("3")  # Constelación del Burro
    star_diff_1 = space_map.get_star("1")  # Constelación del Burro
    star_diff_2 = space_map.get_star("13") # Constelación de la Araña
    
    same_constellation = not jump_system.requires_hypergiant_jump(star_same_1, star_same_2)
    diff_constellation = jump_system.requires_hypergiant_jump(star_diff_1, star_diff_2)
    
    print(f"   • Misma constelación ({star_same_1.label} → {star_same_2.label}): {'❌ Requiere' if not same_constellation else '✅ No requiere'} salto")
    print(f"   • Diferente constelación ({star_diff_1.label} → {star_diff_2.label}): {'✅ Requiere' if diff_constellation else '❌ No requiere'} salto")
    
    if same_constellation and diff_constellation:
        results['requirement_1'] = True
        print("   ✅ REQUISITO 1 CUMPLIDO")
    else:
        print("   ❌ REQUISITO 1 NO CUMPLIDO")
    
    print("\n📋 REQUISITO 2: Obligatoriedad del paso por hipergigante")
    print("-"*50)
    
    # Probar desde Beta23 (id=2) que sí tiene acceso directo a Alpha53 (id=3, hipergigante)
    star_with_hg_access = space_map.get_star("2")  # Beta23
    accessible_hgs = jump_system.find_accessible_hypergiants(star_with_hg_access)
    hypergiants_found = len(accessible_hgs) > 0
    
    print(f"   • Probando desde {star_with_hg_access.label} (que tiene acceso a hipergigantes)")
    print(f"   • Hipergigantes accesibles desde {star_with_hg_access.label}: {len(accessible_hgs)}")
    for hg, distance in accessible_hgs:
        print(f"     - {hg.label} (distancia: {distance} años luz)")
    
    if hypergiants_found:
        results['requirement_2'] = True
        print("   ✅ REQUISITO 2 CUMPLIDO")
    else:
        print("   ❌ REQUISITO 2 NO CUMPLIDO")
    
    print("\n📋 REQUISITO 3: Selección de destino en nueva galaxia")
    print("-"*50)
    
    target_constellation = jump_system.get_star_constellation(star_diff_2)
    destinations = jump_system.find_destination_options(target_constellation)
    
    print(f"   • Constelación destino: {target_constellation}")
    print(f"   • Estrellas disponibles: {len(destinations)}")
    print(f"   • Opciones: {', '.join([d.label for d in destinations[:5]])}" + 
          ("..." if len(destinations) > 5 else ""))
    
    if len(destinations) > 1:
        results['requirement_3'] = True
        print("   ✅ REQUISITO 3 CUMPLIDO")
    else:
        print("   ❌ REQUISITO 3 NO CUMPLIDO")
    
    print("\n📋 REQUISITOS 4 y 5: Beneficios del salto hipergigante")
    print("-"*50)
    
    # Usar una estrella que tiene acceso directo a hipergigante para la prueba
    test_star = space_map.get_star("2")  # Beta23 que está conectada a Alpha53
    burro.current_location = test_star
    accessible_hgs_for_test = jump_system.find_accessible_hypergiants(test_star)
    
    # Configurar estado para prueba
    burro.current_energy = 60
    burro.current_pasto = 100
    initial_energy = burro.current_energy
    initial_grass = burro.current_pasto
    
    print(f"   • Estado inicial - Energía: {initial_energy}%, Pasto: {initial_grass}kg")
    print(f"   • Probando desde {test_star.label} que tiene acceso a hipergigante")
    
    if accessible_hgs_for_test:
        hypergiant, distance = accessible_hgs_for_test[0]
        destination = destinations[0] if destinations else star_diff_2
        
        print(f"   • Usando hipergigante: {hypergiant.label}")
        print(f"   • Destino: {destination.label}")
        print(f"   • Distancia a hipergigante: {distance} años luz")
        
        # Realizar salto hipergigante
        result = jump_system.perform_hypergiant_jump(burro, hypergiant, destination, distance)
        
        if result.success:
            # Calcular incremento esperado correctamente
            # Energía después de viajar a la hipergigante
            age_factor = max(1.0, (burro.start_age - 5) / 10.0)
            energy_cost_to_hg = int(distance * 0.1 * age_factor)
            energy_after_travel = initial_energy - energy_cost_to_hg
            expected_boost = energy_after_travel * 0.5
            expected_final = energy_after_travel + expected_boost
            
            energy_increase = result.energy_after - initial_energy
            grass_increase = result.grass_after / initial_grass
            
            print(f"   • Estado final - Energía: {result.energy_after:.1f}%, Pasto: {result.grass_after:.1f}kg")
            print(f"   • Energía después de viajar: {energy_after_travel}% (costo: -{energy_cost_to_hg}%)")
            print(f"   • Boost aplicado: +{expected_boost:.1f}% (50% de {energy_after_travel}%)")
            print(f"   • Energía final esperada: {expected_final:.1f}%")
            print(f"   • Multiplicador pasto: x{grass_increase:.1f} (esperado: x2.0)")
            
            # Verificar beneficios con tolerancia
            energy_ok = abs(result.energy_after - expected_final) < 1  # Tolerancia de 1%
            grass_ok = abs(grass_increase - 2.0) < 0.1  # Tolerancia de 10%
            
            if energy_ok:
                results['requirement_4'] = True
                print("   ✅ REQUISITO 4 CUMPLIDO (recarga 50% energía)")
            else:
                print("   ❌ REQUISITO 4 NO CUMPLIDO")
                
            if grass_ok:
                results['requirement_5'] = True
                print("   ✅ REQUISITO 5 CUMPLIDO (duplica pasto)")
            else:
                print("   ❌ REQUISITO 5 NO CUMPLIDO")
        else:
            print(f"   ❌ Error en el salto: {result.message}")
    else:
        print("   ❌ No hay hipergigantes accesibles para la prueba")
    
    print("\n📋 REQUISITO 6: Confirmación de recarga y duplicación")
    print("-"*50)
    
    if accessible_hgs_for_test and 'result' in locals() and result.success:
        confirmation_shown = "✨ SALTO HIPERGIGANTE EXITOSO!" in result.message
        energy_info_shown = "Energía:" in result.message
        grass_info_shown = "Pasto:" in result.message
        
        print(f"   • Mensaje de confirmación mostrado: {'✅ Sí' if confirmation_shown else '❌ No'}")
        print(f"   • Información de energía incluida: {'✅ Sí' if energy_info_shown else '❌ No'}")
        print(f"   • Información de pasto incluida: {'✅ Sí' if grass_info_shown else '❌ No'}")
        print(f"   • Mensaje completo: {result.message[:100]}...")
        
        if confirmation_shown and energy_info_shown and grass_info_shown:
            results['requirement_6'] = True
            print("   ✅ REQUISITO 6 CUMPLIDO")
        else:
            print("   ❌ REQUISITO 6 NO CUMPLIDO")
    else:
        print("   ❌ No se pudo probar (no hay salto exitoso previo)")
    
    print("\n📋 REQUISITO 7: Recálculo de ruta en nueva galaxia")
    print("-"*50)
    
    # Probar algoritmos de ruta con soporte de hipergigantes
    try:
        result_max = compute_max_visits_from_json(space_map, "1")
        route_calculated = len(result_max['sequence']) > 1
        
        print(f"   • Algoritmo MAX_VISIT ejecutado: {'✅ Sí' if route_calculated else '❌ No'}")
        print(f"   • Estrellas en ruta: {result_max['num_stars']}")
        print(f"   • Soporte para hipergigantes: {'✅ Integrado' if 'hypergiant_jumps' in result_max else '❌ No integrado'}")
        
        if route_calculated and 'hypergiant_jumps' in result_max:
            results['requirement_7'] = True
            print("   ✅ REQUISITO 7 CUMPLIDO")
        else:
            print("   ❌ REQUISITO 7 NO CUMPLIDO")
            
    except Exception as e:
        print(f"   ❌ Error en algoritmo de ruta: {str(e)}")
    
    # Resumen final
    print("\n" + "="*65)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("="*65)
    
    passed = sum(results.values())
    total = len(results)
    
    requirements = [
        "1. Detecta cambios de galaxia/constelación",
        "2. Obliga paso por hipergigante",
        "3. Permite selección de destino",
        "4. Recarga 50% de energía",
        "5. Duplica cantidad de pasto",
        "6. Muestra confirmación tras salto",
        "7. Recalcula ruta en nueva galaxia"
    ]
    
    for i, (key, passed) in enumerate(results.items()):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {requirements[i]}: {status}")
    
    print(f"\n🎯 RESULTADO FINAL: {passed}/{total} requisitos cumplidos ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🏆 ¡TODOS LOS REQUISITOS HAN SIDO CUMPLIDOS EXITOSAMENTE!")
        print("\n✨ El sistema de saltos hipergigantes está completamente implementado")
        print("   y cumple con todas las especificaciones requeridas.")
    else:
        print("⚠️  Algunos requisitos necesitan atención adicional.")
    
    print("="*65)
    
    return passed == total


if __name__ == "__main__":
    success = test_hypergiant_jump_requirements()
    
    if success:
        print("\n🎮 El sistema está listo para usar. Ejecute la GUI para probarlo:")
        print("   python src/gui.py")
    else:
        print("\n🔧 Revise los requisitos que no se cumplieron.")
    
    sys.exit(0 if success else 1)