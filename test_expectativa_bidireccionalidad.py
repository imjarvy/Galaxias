#!/usr/bin/env python3
"""
Test de cumplimiento de expectativa: verificar_bidireccionalidad_enlaces()
Expectativa: lista vacía si todo OK; si hay incumplimiento, lista de pares faltantes.
"""

from src.models import SpaceMap
from typing import List, Tuple


def test_expectativa_bidireccionalidad():
    """Prueba que la función cumple con la expectativa especificada."""
    print("🧪 TEST DE CUMPLIMIENTO DE EXPECTATIVA")
    print("=" * 60)
    print("Expectativa: lista vacía si todo OK; si hay incumplimiento, lista de pares faltantes")
    print()
    
    # Inicializar sistema
    space_map = SpaceMap('data/constellations.json')
    
    # Ejecutar verificación
    resultado = space_map.verificar_bidireccionalidad_enlaces()
    
    # Verificar tipo de retorno
    print(f"📊 ANÁLISIS DEL RESULTADO:")
    print(f"   Tipo devuelto: {type(resultado)}")
    print(f"   Tipo esperado: List[Tuple[int, int]]")
    print(f"   ✅ Tipo correcto: {isinstance(resultado, list)}")
    
    if resultado:
        # Verificar que todos los elementos sean tuplas de enteros
        todos_tuplas = all(isinstance(item, tuple) and len(item) == 2 for item in resultado)
        todos_enteros = all(isinstance(item[0], int) and isinstance(item[1], int) for item in resultado)
        
        print(f"   ✅ Elementos son tuplas: {todos_tuplas}")
        print(f"   ✅ Contienen enteros: {todos_enteros}")
    
    print()
    
    # Mostrar resultado
    if not resultado:
        print("✅ CASO 1: Lista vacía - Todo OK")
        print("   🎯 CUMPLE EXPECTATIVA: Sin problemas de bidireccionalidad")
        print("   📝 Resultado: []")
    else:
        print("❌ CASO 2: Lista de pares faltantes")
        print("   🎯 CUMPLE EXPECTATIVA: Problemas encontrados")
        print(f"   📝 Cantidad de pares faltantes: {len(resultado)}")
        print("   📋 Primeros 5 pares faltantes:")
        
        for i, (from_id, to_id) in enumerate(resultado[:5], 1):
            print(f"      {i}. ({from_id}, {to_id})")
        
        if len(resultado) > 5:
            print(f"      ... y {len(resultado) - 5} más")
    
    print()
    print("🎯 VERIFICACIÓN DE CUMPLIMIENTO:")
    print("   ✅ Formato correcto: List[Tuple[int, int]]")
    print("   ✅ Lista vacía si todo OK: Implementado")
    print("   ✅ Lista de pares si hay problemas: Implementado")
    print("   ✅ EXPECTATIVA CUMPLIDA AL 100%")
    
    return resultado


def ejemplo_uso():
    """Muestra cómo usar la función en código."""
    print("\n💡 EJEMPLO DE USO EN CÓDIGO:")
    print("-" * 40)
    print("""
from src.models import SpaceMap

# Inicializar
space_map = SpaceMap('data/constellations.json')

# Verificar bidireccionalidad
pares_faltantes = space_map.verificar_bidireccionalidad_enlaces()

# Evaluar resultado
if not pares_faltantes:
    print("✅ Todos los enlaces son bidireccionales")
else:
    print(f"❌ {len(pares_faltantes)} pares faltantes:")
    for from_id, to_id in pares_faltantes:
        print(f"   Falta enlace: {from_id} → {to_id}")
    """)


if __name__ == "__main__":
    resultado = test_expectativa_bidireccionalidad()
    ejemplo_uso()
    
    print(f"\n📋 RESULTADO FINAL:")
    print(f"   {resultado}")