# 📋 Sistema de Máximo Alcance - Solo Valores del JSON

## 🎯 **Objetivo Alcanzado**

El sistema ahora calcula la ruta que permite visitar la **mayor cantidad de estrellas** usando **EXCLUSIVAMENTE** los valores iniciales definidos en `constellations.json`, sin permitir modificaciones externas.

---

## 📊 **Valores Utilizados del JSON**

### **Archivo: `data/constellations.json`**
```json
{
  "burroenergiaInicial": 100,    // Energía inicial (%)
  "estadoSalud": "Excelente",    // Estado de salud inicial
  "pasto": 300,                  // Pasto inicial (kg)
  "startAge": 12,                // Edad inicial (años)
  "deathAge": 3567               // Edad de muerte (años)
}
```

### **Archivo: `data/spaceship_config.json`**
```json
{
  "scientific_parameters": {
    "warp_factor": 1.5           // Factor de velocidad warp
  }
}
```

---

## 🚀 **Cómo Usar el Sistema**

### **1. Script CLI (Simplificado)**
```bash
# Solo requiere la estrella de inicio
python -m src.max_visit_route --start 1

# Todos los demás valores vienen automáticamente del JSON
```

### **2. GUI (Integrado)**
- Abrir la aplicación: `python main.py`
- Seleccionar estrella de origen
- Presionar **"Maximizar Estrellas Visitadas"**
- El sistema usa automáticamente los valores del JSON

### **3. Programático**
```python
from src.models import SpaceMap
from src.route_calculator import RouteCalculator

# Cargar mapa (carga automáticamente valores del JSON)
space_map = SpaceMap('data/constellations.json')
calculator = RouteCalculator(space_map, {})

# Buscar estrella de inicio
start_star = space_map.get_star('1')

# Calcular ruta óptima (usa valores del JSON automáticamente)
path, stats = calculator.find_max_visit_route_from_json(start=start_star)

print(f"Estrellas visitadas: {stats['stars_visited']}")
print(f"Valores del JSON usados: {stats['json_values_used']}")
```

---

## 📈 **Resultados del Test**

### **Test Ejecutado:**
```
🚀 Test del Sistema Simplificado (Solo Valores del JSON)

📋 VALORES CARGADOS DEL JSON:
- burroenergiaInicial: 100
- estadoSalud: Excelente  
- pasto: 300
- startAge: 12
- deathAge: 3567
- warp_factor: 1.5

🔄 COMPARANDO DIFERENTES PUNTOS DE INICIO:
- Alpha1 (ID: 1): 8 estrellas, 349.3 años
- Beta23 (ID: 2): 9 estrellas, 462.7 años  
- Alpha53 (ID: 3): 6 estrellas, 258.0 años
- Beta178 (ID: 12): 6 estrellas, 244.7 años
- Gama23 (ID: 13): 10 estrellas, 492.7 años ⭐ MEJOR

🏆 MEJOR PUNTO DE INICIO: Gama23 (ID: 13)
   Estrellas visitadas: 10
   Tiempo total: 492.7 años
```

---

## 🧠 **Lógica del Algoritmo**

### **Principios Fundamentales:**
1. **Recursos inmutables**: Energía y pasto NO se regeneran
2. **Costo energético**: `int(distancia * 0.1 * factor_edad)`
3. **Tiempo de viaje**: `distancia / warp_factor` años
4. **Objetivo**: Maximizar número de estrellas visitadas

### **Optimizaciones Implementadas:**
- ✅ **Heurísticas inteligentes** (prioriza más estrellas + conservar recursos)
- ✅ **Poda por profundidad** (máximo 15 niveles)
- ✅ **Poda por imposibilidad** (corta ramas sin futuro)
- ✅ **Limitación de ramificación** (máximo 8 vecinos por nodo)

### **Fórmulas Clave:**
```python
# Factor de edad (penalización por edad avanzada)
age_factor = max(1.0, (edad - 5) / 10.0)

# Costo energético por arista
energy_cost = int(distance * 0.1 * age_factor)

# Tiempo de viaje (con warp factor)
travel_time = distance / warp_factor

# Score heurístico
score = visited_count * 1000 + energy_bonus + life_bonus
```

---

## 📁 **Archivos Modificados**

### **1. `src/max_visit_route.py`**
- ✅ Función `compute_max_visits_from_json()` simplificada
- ✅ Solo requiere `start_id` + `space_map`
- ✅ CLI con argumentos mínimos
- ✅ Muestra resumen de valores JSON usados

### **2. `src/route_calculator.py`**
- ✅ Método `find_max_visit_route_from_json()` añadido
- ✅ Usa exclusivamente valores del `space_map.burro_data`
- ✅ Retorna estadísticas detalladas con valores JSON

### **3. `src/gui.py`**
- ✅ Botón **"Maximizar Estrellas Visitadas"** actualizado
- ✅ Interfaz muestra claramente que usa valores del JSON
- ✅ Información detallada de configuración usada

---

## 🔍 **Diferencias Clave vs Versión Anterior**

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Parámetros** | CLI permite override de todo | Solo `start_id` requerido |
| **Fuente de datos** | CLI, GUI, JSON (múltiples fuentes) | Solo JSON |
| **Energía** | Configurable externamente | Fijo: 100% (del JSON) |
| **Edad** | Configurable externamente | Fijo: 12 años (del JSON) |
| **Death age** | Override opcional | Fijo: 3567 años (del JSON) |
| **Complejidad** | Alta (muchos parámetros) | Baja (un solo parámetro) |
| **Consistencia** | Variable según parámetros | Consistente con JSON |

---

## ✅ **Ventajas del Sistema Actual**

1. **Simplicidad**: Solo necesitas especificar la estrella de inicio
2. **Consistencia**: Siempre usa los mismos valores base del JSON
3. **Trazabilidad**: Es claro de dónde vienen todos los valores
4. **Realismo**: Respeta la configuración inicial del juego
5. **Facilidad de uso**: Interfaz mínima y clara

---

## 🎮 **Ejemplo de Uso Completo**

```bash
# Ejecutar análisis completo
python test_json_only.py

# Resultado automático:
# ✅ Carga valores del JSON
# ✅ Calcula ruta óptima desde múltiples puntos
# ✅ Encuentra el mejor punto de inicio
# ✅ Muestra estadísticas detalladas
```

**Resultado esperado:**
- **Mejor inicio**: Gama23 (ID: 13)  
- **Máximo alcance**: 10 estrellas
- **Valores usados**: Exclusivamente del JSON
- **Tiempo consumido**: ~492 años de 3567 disponibles

---

El sistema está **listo para uso** y completamente **basado en los valores iniciales del JSON** como solicitaste. 🚀