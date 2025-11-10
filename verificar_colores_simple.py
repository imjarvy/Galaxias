#!/usr/bin/env python3
"""
Verificador simple de colores por constelación.
"""

import json
from typing import Dict, List, Optional


def verificar_colores_constelaciones() -> Dict:
    """
    Verifica si hay colores asignados por constelación y si son únicos.
    
    Returns:
        Dict con el análisis de colores por constelación
    """
    print("🎨 ANÁLISIS DE COLORES POR CONSTELACIÓN - SISTEMA GALAXIAS")
    print("=" * 65)
    
    # Cargar datos de constelaciones
    with open('data/constellations.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    constelaciones = data.get('constellations', [])
    
    print(f"📊 CONSTELACIONES ENCONTRADAS: {len(constelaciones)}")
    print("-" * 45)
    
    colores_definidos = []
    constelaciones_info = []
    
    for i, constellation in enumerate(constelaciones, 1):
        name = constellation.get('name', f'Constelación {i}')
        color = constellation.get('color', None)
        
        info = {
            'nombre': name,
            'color': color,
            'tiene_color': color is not None
        }
        constelaciones_info.append(info)
        
        print(f"   {i}. {name}")
        if color:
            print(f"      🎨 Color: {color}")
            colores_definidos.append(color)
        else:
            print(f"      ❌ Color: NO DEFINIDO")
    
    # Verificar unicidad de colores
    colores_unicos = len(colores_definidos) == len(set(colores_definidos))
    colores_repetidos = []
    
    if colores_definidos:
        # Encontrar colores repetidos
        colores_vistos = {}
        for i, info in enumerate(constelaciones_info):
            if info['color']:
                if info['color'] in colores_vistos:
                    colores_repetidos.append({
                        'color': info['color'],
                        'constelacion1': colores_vistos[info['color']],
                        'constelacion2': info['nombre']
                    })
                else:
                    colores_vistos[info['color']] = info['nombre']
    
    # Resultado del análisis
    resultado = {
        'tiene_colores_por_constelacion': len(colores_definidos) > 0,
        'total_constelaciones': len(constelaciones),
        'constelaciones_con_color': len(colores_definidos),
        'colores_unicos': colores_unicos,
        'colores_repetidos': colores_repetidos,
        'constelaciones': constelaciones_info
    }
    
    # Mostrar resultado
    print(f"\n🎯 RESULTADO DEL ANÁLISIS:")
    print("-" * 30)
    
    if resultado['tiene_colores_por_constelacion']:
        print("✅ Colores por constelación: DEFINIDOS")
        print(f"   📊 {resultado['constelaciones_con_color']}/{resultado['total_constelaciones']} constelaciones con color")
        
        if resultado['colores_unicos']:
            print("✅ Unicidad: CUMPLE - Cada constelación tiene color distinto")
        else:
            print("❌ Unicidad: VIOLADA - Hay colores repetidos:")
            for repeticion in resultado['colores_repetidos']:
                print(f"      • Color {repeticion['color']}: {repeticion['constelacion1']} y {repeticion['constelacion2']}")
    else:
        print("❌ Colores por constelación: NO DEFINIDOS")
        print("   Solo hay colores por tipo de estrella:")
        print("   • Estrellas normales: #FFFF44 (amarillo)")
        print("   • Hipergigantes: #FF00FF (magenta)")
    
    print(f"\n📋 SISTEMA ACTUAL:")
    print("   🌟 Estrellas se colorean por TIPO, no por CONSTELACIÓN")
    print("   🛤️  Rutas se colorean por NIVEL DE PELIGRO")
    print("   🏛️  Constelaciones: SIN COLORES ESPECÍFICOS")
    
    return resultado


if __name__ == "__main__":
    resultado = verificar_colores_constelaciones()
    
    print(f"\n🎯 RESPUESTA DIRECTA:")
    if resultado['tiene_colores_por_constelacion']:
        if resultado['colores_unicos']:
            print("✅ SÍ tienes colores por constelación y son únicos")
        else:
            print("⚠️  Tienes colores por constelación pero hay repetidos")
    else:
        print("❌ NO tienes colores por constelación implementados")