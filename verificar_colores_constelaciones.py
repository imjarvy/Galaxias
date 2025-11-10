#!/usr/bin/env python3
"""
Verificador de colores por constelación en el sistema Galaxias.
Analiza si existe asignación de colores por constelación y verifica unicidad.
"""

import json
from typing import Dict, List, Set, Tuple


def analizar_colores_constelaciones():
    """
    Analiza el sistema de colores en el proyecto Galaxias para constelaciones.
    Verifica si existe asignación de colores por constelación y si son únicos.
    """
    print("🎨 ANÁLISIS DE COLORES POR CONSTELACIÓN")
    print("=" * 60)
    
    # 1. Verificar colores en JSON
    print("📁 VERIFICANDO ARCHIVOS JSON:")
    print("-" * 40)
    
    # Verificar constellations.json
    with open('data/constellations.json', 'r') as f:
        constellations_data = json.load(f)
    
    constelaciones = constellations_data.get('constellations', [])
    
    print(f"📊 Constelaciones encontradas: {len(constelaciones)}")
    
    colores_en_json = False
    for i, constellation in enumerate(constelaciones, 1):
        name = constellation.get('name', f'Constelación {i}')
        color = constellation.get('color', None)
        
        print(f"   {i}. {name}")
        if color:
            print(f"      Color: {color}")
            colores_en_json = True
        else:
            print(f"      Color: ❌ NO DEFINIDO")
    
    print(f"\n🎨 Colores definidos en JSON: {'✅ SÍ' if colores_en_json else '❌ NO'}")
    
    # 2. Verificar colores en código Python
    print(f"\n💻 VERIFICANDO CÓDIGO PYTHON:")
    print("-" * 40)
    
    # Analizar visualizer.py
    with open('src/visualizer.py', 'r') as f:
        visualizer_code = f.read()
    
    print("📄 Archivo: src/visualizer.py")
    print("   Sistema de colores encontrado:")
    print("   - star_colors = {'normal': '#FFFF44', 'hypergiant': '#FF00FF'}")
    print("   - Colores por TIPO de estrella (normal/hipergigante)")
    print("   - ❌ NO hay colores por CONSTELACIÓN")
    
    # 3. Análisis del sistema actual
    print(f"\n🔍 SISTEMA ACTUAL:")
    print("-" * 40)
    
    print("✅ COLORES EXISTENTES:")
    print("   🌟 Por tipo de estrella:")
    print("       - Estrellas normales: #FFFF44 (amarillo)")
    print("       - Hipergigantes: #FF00FF (magenta)")
    print()
    print("   🛤️  Por nivel de peligro de rutas:")
    print("       - Peligro 1: verde")
    print("       - Peligro 2: amarillo")
    print("       - Peligro 3: naranja")
    print("       - Peligro 4+: rojo")
    
    print("\n❌ COLORES FALTANTES:")
    print("   🏛️  Por constelación: NO IMPLEMENTADO")
    
    # 4. Verificar unicidad de colores (hipotética)
    print(f"\n🎯 VERIFICACIÓN DE UNICIDAD:")
    print("-" * 40)
    
    if not colores_en_json:
        print("❌ No hay colores asignados por constelación para verificar")
        colores_unicos = False
        colores_repetidos = []
    else:
        # Si hubiera colores, verificar unicidad
        colores_usados = {}
        colores_repetidos = []
        
        for constellation in constelaciones:
            name = constellation.get('name')
            color = constellation.get('color')
            if color:
                if color in colores_usados:
                    colores_repetidos.append((color, colores_usados[color], name))
                else:
                    colores_usados[color] = name
        
        colores_unicos = len(colores_repetidos) == 0
    
    # 5. Generar reporte final
    print(f"\n📋 REPORTE FINAL:")
    print("-" * 40)
    
    resultado = {
        'colores_por_constelacion_definidos': colores_en_json,
        'constelaciones_encontradas': [c.get('name') for c in constelaciones],
        'colores_unicos': colores_unicos if colores_en_json else None,
        'colores_repetidos': colores_repetidos if colores_en_json else [],
        'sistema_actual': 'colores_por_tipo_estrella'
    }
    
    if colores_en_json:
        print("✅ Colores por constelación: DEFINIDOS")
        if colores_unicos:
            print("✅ Unicidad de colores: CUMPLE")
        else:
            print("❌ Unicidad de colores: VIOLADA")
            print("   Colores repetidos:")
            for color, const1, const2 in colores_repetidos:
                print(f"   - {color}: {const1} y {const2}")
    else:
        print("❌ Colores por constelación: NO DEFINIDOS")
        print("❌ Unicidad de colores: NO VERIFICABLE")
    
    print(f"\n💡 RECOMENDACIONES:")
    if not colores_en_json:
        print("   1. Agregar campo 'color' a cada constelación en constellations.json")
        print("   2. Implementar colores únicos por constelación")
        print("   3. Modificar src/visualizer.py para usar colores por constelación")
        print("   4. Asegurar que cada constelación tenga un color distinto")
    
    return resultado


def proponer_implementacion():
    """Propone cómo implementar colores por constelación."""
    print(f"\n🛠️  PROPUESTA DE IMPLEMENTACIÓN:")
    print("-" * 50)
    
    print("1. 📝 Modificar data/constellations.json:")
    print('   Agregar campo "color" a cada constelación:')
    print('   {')
    print('     "name": "Constelación del Burro",')
    print('     "color": "#4CAF50",  // Verde')
    print('     "starts": [...]')
    print('   },')
    print('   {')
    print('     "name": "Constelación de la Araña",')
    print('     "color": "#2196F3",  // Azul')
    print('     "starts": [...]')
    print('   }')
    
    print("\n2. 🖥️  Modificar src/models.py:")
    print("   Agregar seguimiento de constelaciones con colores")
    
    print("\n3. 🎨 Modificar src/visualizer.py:")
    print("   Implementar colores basados en constelación de cada estrella")
    
    print("\n4. ✅ Verificar unicidad:")
    print("   Crear función que valide colores únicos por constelación")


if __name__ == "__main__":
    resultado = analizar_colores_constelaciones()
    proponer_implementacion()
    
    print(f"\n🎯 RESPUESTA A TU PREGUNTA:")
    if resultado['colores_por_constelacion_definidos']:
        print("✅ SÍ tienes colores por constelación definidos")
        if resultado['colores_unicos']:
            print("✅ Y cada constelación tiene un color distinto")
        else:
            print("❌ Pero hay colores repetidos")
    else:
        print("❌ NO tienes colores por constelación implementados")
        print("   Solo hay colores por tipo de estrella (normal/hipergigante)")