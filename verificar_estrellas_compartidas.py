#!/usr/bin/env python3
"""
Verificar qué estrellas aparecen en múltiples constelaciones (por coordenadas).
"""
import json

def verificar_estrellas_compartidas():
    """Verifica qué estrellas aparecen en múltiples constelaciones basándose en coordenadas."""
    
    with open('data/constellations.json', 'r') as f:
        data = json.load(f)
    
    # Diccionario para agrupar estrellas por coordenadas
    estrellas_por_coordenadas = {}
    
    print("=== ANÁLISIS DE ESTRELLAS COMPARTIDAS ===\n")
    
    # Recopilar todas las estrellas con sus coordenadas
    for constellation in data.get('constellations', []):
        constellation_name = constellation['name']
        print(f"📍 Constelación: {constellation_name}")
        
        for star in constellation.get('starts', []):
            star_id = star['id']
            star_label = star['label']
            x = star['coordenates']['x']
            y = star['coordenates']['y']
            coordenada = (x, y)
            
            print(f"   ⭐ {star_label} (ID: {star_id}) -> ({x}, {y})")
            
            # Agrupar por coordenadas
            if coordenada not in estrellas_por_coordenadas:
                estrellas_por_coordenadas[coordenada] = []
            
            estrellas_por_coordenadas[coordenada].append({
                'id': star_id,
                'label': star_label,
                'constellation': constellation_name,
                'hypergiant': star.get('hypergiant', False)
            })
    
    print("\n" + "="*50)
    print("🔍 RESULTADOS DEL ANÁLISIS:")
    print("="*50)
    
    # Identificar estrellas compartidas
    estrellas_compartidas = []
    estrellas_unicas = []
    
    for coordenada, estrellas_en_coordenada in estrellas_por_coordenadas.items():
        if len(estrellas_en_coordenada) > 1:
            print(f"\n🚨 ESTRELLA COMPARTIDA en coordenada {coordenada}:")
            for estrella in estrellas_en_coordenada:
                print(f"   ⭐ {estrella['label']} (ID: {estrella['id']}) - {estrella['constellation']}")
                estrellas_compartidas.append(estrella)
        else:
            estrellas_unicas.extend(estrellas_en_coordenada)
    
    if not estrellas_compartidas:
        print("\n✅ NO hay estrellas compartidas entre constelaciones.")
        print("   Todas las estrellas tienen coordenadas únicas.")
    
    print(f"\n📊 RESUMEN:")
    print(f"   • Estrellas únicas: {len(estrellas_unicas)}")
    print(f"   • Estrellas compartidas: {len(estrellas_compartidas)}")
    print(f"   • Total de posiciones únicas: {len(estrellas_por_coordenadas)}")
    
    # Mostrar constelaciones disponibles
    constelaciones = [c['name'] for c in data.get('constellations', [])]
    print(f"\n🌌 Constelaciones encontradas: {len(constelaciones)}")
    for i, nombre in enumerate(constelaciones, 1):
        print(f"   {i}. {nombre}")
    
    return estrellas_compartidas, estrellas_unicas, constelaciones

if __name__ == "__main__":
    estrellas_compartidas, estrellas_unicas, constelaciones = verificar_estrellas_compartidas()