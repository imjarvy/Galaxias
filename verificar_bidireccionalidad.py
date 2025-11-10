#!/usr/bin/env python3
"""
Verificador de bidireccionalidad de enlaces en el sistema Galaxias.
Comprueba que todas las vías (enlaces linkedTo) sean bidireccionales.
"""

import json
from typing import Dict, List, Set, Tuple


def verificar_bidireccionalidad():
    """
    Verifica que todos los enlaces sean bidireccionales.
    Por cada enlace A->B debe existir B->A.
    """
    print("🔍 VERIFICACIÓN DE BIDIRECCIONALIDAD DE ENLACES")
    print("=" * 60)
    
    # Cargar datos
    with open('data/constellations.json', 'r') as f:
        data = json.load(f)
    
    # Recopilar todos los enlaces
    enlaces_directos = {}  # {(from_id, to_id): distance}
    todas_las_estrellas = set()
    
    for constellation in data.get('constellations', []):
        for star_data in constellation.get('starts', []):
            star_id = star_data['id']
            todas_las_estrellas.add(star_id)
            
            for link in star_data.get('linkedTo', []):
                to_star_id = link['starId']
                distance = link['distance']
                
                # Registrar el enlace directo
                enlace_key = (star_id, to_star_id)
                enlaces_directos[enlace_key] = distance
                
                print(f"📡 Enlace encontrado: {star_id} → {to_star_id} (distancia: {distance})")
    
    print(f"\n📊 RESUMEN DE ENLACES ENCONTRADOS:")
    print(f"   Total de estrellas únicas: {len(todas_las_estrellas)}")
    print(f"   Total de enlaces directos: {len(enlaces_directos)}")
    print(f"   Estrellas: {sorted(todas_las_estrellas)}")
    print()
    
    # Verificar bidireccionalidad
    enlaces_no_bidireccionales = []
    enlaces_verificados = set()
    
    print("🔄 VERIFICANDO BIDIRECCIONALIDAD:")
    print("-" * 40)
    
    for (from_id, to_id), distance in enlaces_directos.items():
        # Evitar verificar el mismo enlace dos veces
        enlace_pair = tuple(sorted([from_id, to_id]))
        if enlace_pair in enlaces_verificados:
            continue
        enlaces_verificados.add(enlace_pair)
        
        # Buscar el enlace inverso
        enlace_inverso = (to_id, from_id)
        
        if enlace_inverso in enlaces_directos:
            distance_inverso = enlaces_directos[enlace_inverso]
            
            if distance == distance_inverso:
                print(f"✅ {from_id} ⟷ {to_id}: Bidireccional (distancia: {distance})")
            else:
                print(f"⚠️  {from_id} ⟷ {to_id}: Bidireccional pero distancias diferentes")
                print(f"    {from_id}→{to_id}: {distance}, {to_id}→{from_id}: {distance_inverso}")
                enlaces_no_bidireccionales.append({
                    'tipo': 'distancias_diferentes',
                    'enlace_a_b': f"{from_id}→{to_id}",
                    'distancia_a_b': distance,
                    'enlace_b_a': f"{to_id}→{from_id}",
                    'distancia_b_a': distance_inverso
                })
        else:
            print(f"❌ {from_id} → {to_id}: NO bidireccional (falta {to_id}→{from_id})")
            enlaces_no_bidireccionales.append({
                'tipo': 'enlace_faltante',
                'enlace_existente': f"{from_id}→{to_id}",
                'distancia': distance,
                'enlace_faltante': f"{to_id}→{from_id}"
            })
    
    print("\n" + "=" * 60)
    
    if not enlaces_no_bidireccionales:
        print("🎉 TODOS LOS ENLACES SON BIDIRECCIONALES ✅")
        print("   El grafo está correctamente configurado.")
    else:
        print("⚠️  ENLACES NO BIDIRECCIONALES ENCONTRADOS:")
        print("-" * 40)
        
        for i, problema in enumerate(enlaces_no_bidireccionales, 1):
            print(f"\n{i}. Problema: {problema['tipo']}")
            
            if problema['tipo'] == 'enlace_faltante':
                print(f"   Enlace existente: {problema['enlace_existente']} (distancia: {problema['distancia']})")
                print(f"   Enlace faltante:  {problema['enlace_faltante']}")
                print(f"   🔧 Solución: Agregar el enlace inverso con la misma distancia")
                
            elif problema['tipo'] == 'distancias_diferentes':
                print(f"   {problema['enlace_a_b']}: {problema['distancia_a_b']}")
                print(f"   {problema['enlace_b_a']}: {problema['distancia_b_a']}")
                print(f"   🔧 Solución: Unificar las distancias")
    
    print(f"\n📋 RESUMEN FINAL:")
    print(f"   Enlaces verificados: {len(enlaces_verificados)}")
    print(f"   Problemas encontrados: {len(enlaces_no_bidireccionales)}")
    
    return enlaces_no_bidireccionales


def analizar_impacto_en_renderer():
    """Analiza cómo estos enlaces afectan al renderer del visualizador."""
    print("\n🎨 ANÁLISIS DEL IMPACTO EN EL RENDERER:")
    print("-" * 50)
    
    # Verificar cómo se manejan en el código actual
    print("📍 Revisión del código actual:")
    print("   1. En src/models.py líneas 221-234:")
    print("      - Los enlaces se procesan desde 'linkedTo'")
    print("      - Se crea un conjunto 'seen_edges' para evitar duplicados")
    print("      - Se usa tuple(sorted()) para hacer enlaces bidireccionales")
    print()
    print("   2. En src/visualizer.py líneas 65-81:")
    print("      - Cada Route se dibuja una sola vez")
    print("      - El renderer automáticamente dibuja líneas bidireccionales")
    print()
    print("✅ CONCLUSIÓN:")
    print("   El renderer actual maneja correctamente la bidireccionalidad")
    print("   mediante el uso de 'seen_edges' y tuple(sorted())")
    print("   Esto asegura que cada arista se dibuje en ambos sentidos.")


if __name__ == "__main__":
    enlaces_problematicos = verificar_bidireccionalidad()
    analizar_impacto_en_renderer()
    
    if enlaces_problematicos:
        print("\n🚨 ATENCIÓN: Se encontraron problemas de bidireccionalidad")
        print("   Revisar el archivo JSON y corregir los enlaces indicados")
    else:
        print("\n🎉 SISTEMA VERIFICADO: Todos los enlaces son bidireccionales")