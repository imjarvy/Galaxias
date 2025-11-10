# Sistema de Ruta de Menor Gasto Posible

## 📋 Descripción

He implementado exitosamente la nueva lógica de **"Ruta con menor gasto posible"** sin afectar el sistema existente de "máximo estrellas visitadas". Este nuevo sistema implementa reglas específicas y criterios de optimización diferentes.

## 🎯 Criterios y Reglas Implementados

### ✅ **Condición para Comer**
- **Regla:** Solo puede comer si `energía < 50%`
- **Implementación:** Verificación automática en cada estrella
- **Resultado:** Conserva recursos cuando no los necesita

### ✅ **Bonificación por Estado de Salud**
- **Excelente:** +5% energía por kg de pasto
- **Regular:** +3% energía por kg de pasto  
- **Malo:** +2% energía por kg de pasto
- **Implementación:** Función `_get_health_bonus()`

### ✅ **División de Tiempo en Estrella**
- **50% comer:** `time_eating = star.time_to_eat * 0.5`
- **50% investigar:** `time_researching = star.time_to_eat * 0.5`
- **Implementación:** Cálculo automático en cada estrella

### ✅ **Consumo por Investigación**
- **Formula:** `energy_consumed = research_time * 2.0`
- **Implementación:** Siempre investiga, consume energía base

### ✅ **Una Visita por Estrella**
- **Control:** Set de estrellas visitadas
- **Garantía:** Ninguna estrella se visita dos veces

### ✅ **Objetivo: Menor Gasto**
- **Algoritmo:** Optimización de costos en lugar de máximo estrellas
- **Criterio:** `base_cost = travel_distance + energy_cost * 2`
- **Beneficios:** Descuentos por estrellas que permiten comer

## 🗂️ Archivos Creados/Modificados

### **Nuevos Archivos:**
1. **`src/min_cost_route.py`** - Módulo principal del nuevo sistema
2. **`test_min_cost_system.py`** - Script de pruebas comparativas

### **Archivos Modificados:**
1. **`src/route_calculator.py`** - Agregado método `find_min_cost_route_from_json()`
2. **`src/gui.py`** - Agregado botón y método `calculate_min_cost_route()`

## 🚀 Cómo Usar

### **1. Línea de Comandos:**
```bash
python src/min_cost_route.py --start 13
```

### **2. Interfaz Gráfica:**
1. Abrir GUI: `python -c "import sys; sys.path.append('.'); from src.gui import main; main()"`
2. Seleccionar estrella origen
3. Clic en **"Ruta Menor Gasto Posible"** (botón morado)
4. Confirmar reglas específicas
5. Ver resultados detallados

### **3. Programáticamente:**
```python
from src.min_cost_route import MinCostRouteCalculator
from src.models import SpaceMap

space_map = SpaceMap('data/constellations.json')
calculator = MinCostRouteCalculator(space_map)
result = calculator.calculate_min_cost_route('13')
```

## 📊 Resultados Detallados

### **Información Proporcionada:**
- **Ruta propuesta:** Secuencia de estrellas optimizada
- **Acciones por estrella:**
  - Energía al llegar
  - Si puede/debe comer (energía < 50%)
  - Kg de pasto consumido
  - Energía ganada comiendo
  - Tiempo usado comiendo/investigando
  - Energía consumida por investigación
  - Energía final en la estrella

- **Resumen total:**
  - Consumo total de pasto (kg)
  - Energía restante al final (%)
  - Tiempo de vida restante (años)
  - Distancia total recorrida
  - Tiempo de vida consumido

## 🔄 Comparación con Sistema Existente

| **Aspecto** | **Máximo Estrellas** | **Menor Gasto** |
|-------------|---------------------|------------------|
| **Objetivo** | Maximizar estrellas visitadas | Minimizar gasto total |
| **Decisión comer** | Siempre que llega | Solo si energía < 50% |
| **Tiempo en estrella** | Solo viaje | 50% comer + 50% investigar |
| **Consumo investigación** | No existe | 2% energía por tiempo |
| **Criterio optimización** | Más estrellas > menor distancia | Menor costo total |
| **Bonificación salud** | No aplica | +5%/+3%/+2% según salud |

## 🧪 Resultados de Pruebas

### **Desde Gama23 (ID: 13):**

**Máximo Estrellas:**
- ✅ 10 estrellas visitadas
- 📏 739 años luz  
- ⏱️ 492.67 años vida

**Menor Gasto:**
- ✅ 4 estrellas visitadas
- 📏 262 años luz
- ⏱️ 174.67 años vida  
- 🌱 0 kg pasto (no comió - energía > 50%)
- 🔋 64% energía final
- 💫 3380 años vida restante

## ✅ Verificación de Implementación

### **Reglas Específicas Funcionando:**
- ✅ Decisión de comer basada en energía < 50%
- ✅ Bonificación por estado de salud  
- ✅ División tiempo: 50% comer / 50% investigar
- ✅ Consumo energía por investigación
- ✅ Una visita por estrella
- ✅ Objetivo: MENOR GASTO total

### **Coexistencia con Sistema Existente:**
- ✅ Sistema de máximo estrellas intacto
- ✅ Ambos sistemas disponibles en GUI
- ✅ Métodos independientes en RouteCalculator
- ✅ Scripts independientes funcionales

## 🎯 Estado Final

**La nueva lógica de "menor gasto posible" está completamente implementada y funcionando según todas las especificaciones solicitadas, manteniendo la funcionalidad existente del sistema de "máximo estrellas visitadas".**

**Ambos sistemas coexisten perfectamente y pueden ser usados según las necesidades específicas del usuario.**