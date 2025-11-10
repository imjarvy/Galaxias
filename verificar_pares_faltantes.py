#!/usr/bin/env python3
"""
Verificador de bidireccionalidad que cumple con la expectativa:
- Lista vacía si todo OK
- Lista de pares faltantes si hay incumplimiento
"""

import json
from typing import List, Tuple


def verificar_bidireccionalidad_enlaces() -> List[Tuple[int, int]]:
    """
    Verifica la bidireccionalidad de enlaces y retorna pares faltantes.
    
    Returns:
        List[Tuple[int, int]]: Lista vacía si todo OK, 
                              lista de pares (from_id, to_id) faltantes si hay problemas
    """
    # Cargar datos del JSON
    with open('data/constellations.json', 'r') as f:
        data = json.load(f)
    
    # Recopilar todos los enlaces existentes
    enlaces_existentes = set()
    
    for constellation in data.get('constellations', []):
        for star_data in constellation.get('starts', []):
            star_id = star_data['id']
            
            for link in star_data.get('linkedTo', []):
                to_star_id = link['starId']
                enlaces_existentes.add((star_id, to_star_id))
    
    # Verificar qué enlaces inversos faltan
    pares_faltantes = []
    
    for (from_id, to_id) in enlaces_existentes:
        enlace_inverso = (to_id, from_id)
        if enlace_inverso not in enlaces_existentes:
            pares_faltantes.append(enlace_inverso)
    
    return pares_faltantes


def mostrar_resultado():
    """Muestra el resultado de la verificación de forma clara."""
    print("🔍 VERIFICACIÓN DE BIDIRECCIONALIDAD")
    print("=" * 50)
    
    pares_faltantes = verificar_bidireccionalidad_enlaces()
    
    if not pares_faltantes:
        print("✅ RESULTADO: Lista vacía - Todo OK")
        print("   Todos los enlaces son bidireccionales")
        return []
    else:
        print(f"❌ RESULTADO: {len(pares_faltantes)} pares faltantes encontrados")
        print("\n📋 LISTA DE PARES FALTANTES:")
        print("-" * 30)
        
        for i, (from_id, to_id) in enumerate(pares_faltantes, 1):
            print(f"{i:2d}. ({from_id}, {to_id})")
        
        return pares_faltantes


if __name__ == "__main__":
    resultado = mostrar_resultado()
    
    print(f"\n📊 FORMATO DE SALIDA ESPERADO:")
    print(f"   Tipo: List[Tuple[int, int]]")
    print(f"   Contenido: {resultado}")
    
    if not resultado:
        print(f"\n🎉 CUMPLE EXPECTATIVA: Lista vacía = Todo OK ✅")
    else:
        print(f"\n⚠️  CUMPLE EXPECTATIVA: Lista de pares faltantes ✅")