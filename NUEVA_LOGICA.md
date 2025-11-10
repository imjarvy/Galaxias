# Documentación de la Nueva Lógica de Galaxias

## 🔄 Cambios Realizados

El proyecto Galaxias ha sido completamente actualizado para funcionar con la nueva estructura de datos JSON. A continuación se detallan todos los cambios realizados:

## 📋 Estructura de Datos JSON

### Archivo `constellations.json`
```json
{
  "constellations": [
    {
      "name": "Constelación del Burro",
      "starts": [
        {
          "id": 1,
          "label": "Alpha1",
          "linkedTo": [{"starId": 2, "distance": 120}],
          "radius": 0.4,
          "timeToEat": 3,
          "amountOfEnergy": 1,
          "coordenates": {"x": 25, "y": 34},
          "hypergiant": false
        }
      ]
    }
  ],
  "burroenergiaInicial": 100,
  "estadoSalud": "Excelente",
  "pasto": 300,
  "startAge": 12,
  "deathAge": 3567
}
```

### Archivo `spaceship_config.json`
```json
{
  "consumption_rates": {
    "fuel_per_unit_distance": 2,
    "food_per_unit_distance": 0.1,
    "oxygen_per_unit_distance": 0.5,
    "health_decay_per_danger": 5
  },
  "scientific_parameters": {
    "gravity_constant": 6.674e-11,
    "light_speed_km_s": 299792,
    "warp_factor": 1.5,
    "shield_efficiency": 0.8
  }
}
```

## 🏗️ Nuevas Clases y Estructuras

### 1. Clase `Star`
```python
@dataclass
class Star:
    id: str
    label: str
    x: float
    y: float
    radius: float
    time_to_eat: int
    amount_of_energy: int
    hypergiant: bool
    linked_to: List[Dict]
```

**Cambios principales:**
- `name` → `label`
- Añadido `radius`, `time_to_eat`, `amount_of_energy`
- Añadido `hypergiant` para identificar hipergigantes
- `linked_to` contiene las conexiones con otras estrellas

### 2. Clase `BurroAstronauta`
```python
@dataclass
class BurroAstronauta:
    name: str
    energia_inicial: int
    estado_salud: str
    pasto: int
    start_age: int
    death_age: int
    current_location: Optional[Star]
    journey_history: List[Star]
    current_energy: int
    current_pasto: int
```

**Funcionalidades principales:**
- `consume_resources_eating_star()`: Consume pasto y gana energía
- `consume_resources_traveling()`: Consume energía al viajar
- `can_eat_star()`: Verifica si puede comer una estrella
- `can_travel()`: Verifica si puede viajar cierta distancia
- `is_alive()`: Verifica si el burro está vivo

### 3. Sistema de Recursos

#### Comer Estrellas
```python
def consume_resources_eating_star(self, star: Star):
    # Consume pasto basado en tiempo de comida
    grass_consumed = star.time_to_eat * 5  # 5 kg por unidad de tiempo
    
    # Gana energía basada en la energía de la estrella
    energy_gained = star.amount_of_energy * 10
    energy_bonus = int(star.radius * 5)  # Bonus por tamaño
```

#### Viajar Entre Estrellas
```python
def consume_resources_traveling(self, distance: float):
    # Energía consumida por distancia y edad
    age_factor = max(1, (self.start_age - 5) / 10)
    energy_consumed = int(distance * 0.1 * age_factor)
```

## 🧭 Sistema de Rutas

### Carga de Rutas
- Las rutas se generan automáticamente desde las conexiones `linkedTo`
- Cada conexión tiene un `starId` y `distance`
- Se evitan duplicados usando un conjunto de aristas vistas

### Cálculo de Peligro
```python
def _calculate_danger_level(self, distance: float) -> int:
    if distance < 50: return 1
    elif distance < 100: return 2
    elif distance < 150: return 3
    else: return 4
```

## 🎯 Optimización de Rutas

### Clase `DonkeyRouteOptimizer`
```python
def simulate_journey(self, start_star: Star, burro: BurroAstronauta):
    # 1. Intenta comer la estrella actual si es beneficioso
    # 2. Encuentra la siguiente mejor estrella
    # 3. Calcula costo del viaje
    # 4. Verifica si puede hacer el viaje
    # 5. Repite hasta que no pueda continuar
```

### Criterios de Optimización
- **Beneficio de comer estrella**: `(energía_ganada + bonus_radio) - costo_pasto`
- **Scoring de estrellas**: `beneficio_comer - costo_viajar`
- **Bonus especiales**:
  - +20 por estrellas hipergigantes
  - +10 por distancias cortas (<50)
  - +5 por distancias moderadas (<100)
  - -10 por viajes muy largos (>150)

## 🖥️ Interfaz Gráfica Actualizada

### Nuevas Funcionalidades
1. **Botón "Optimizar Ruta para Comer Estrellas"**
2. **Información detallada de estrellas** en combos
3. **Estado del burro** con energía, pasto y edad
4. **Visualización mejorada** con colores por tipo de estrella

### Estado del Burro
```
BURRO ASTRONAUTA
================
Nombre: Burro Astronauta
Ubicación: Alpha1

RECURSOS:
  Energía:     100% / 100%
  Pasto:       300 kg
  Edad:        12 años

ESTADO:
  Salud:       EXCELENTE
  Viajes:      0
  Estado:      ✅ VIVO

DATOS JSON:
  BurroEnergía:    100%
  Estado Salud:    excelente
```

## 📊 Visualización

### Mapa Espacial
- **Estrellas normales**: Amarillo (✨)
- **Hipergigantes**: Magenta (⭐)
- **Tamaño**: Basado en el radio de la estrella
- **Información**: Etiqueta + energía disponible

### Rutas
- **Verde**: Peligro nivel 1
- **Amarillo**: Peligro nivel 2  
- **Naranja**: Peligro nivel 3
- **Rojo**: Peligro nivel 4+
- **Rojo discontinuo**: Rutas bloqueadas

## 🎮 Modos de Uso

### 1. Interfaz Gráfica
```bash
python main.py
```

### 2. Línea de Comandos
```bash
python main.py --cli
```

### 3. Demostración
```bash
python main.py --demo
```

### 4. Ejemplo de Nueva Lógica
```bash
python example_new_logic.py
```

## 🔧 Configuración

### Estados de Salud
- **Excelente**: 76-100% energía
- **Buena**: 51-75% energía
- **Mala**: 26-50% energía
- **Moribundo**: 1-25% energía
- **Muerto**: 0% energía

### Factor de Edad
- **< 5 años**: Energía x1.2 (jóvenes)
- **5-15 años**: Energía x1.0 (adultos)
- **15-25 años**: Energía x0.8 (mayores)
- **> 25 años**: Energía x0.6 (ancianos)

## 🚀 Ejemplos de Uso

### Crear Burro desde JSON
```python
space_map = SpaceMap('data/constellations.json')
burro = space_map.create_burro_astronauta()
```

### Optimizar Ruta
```python
optimizer = DonkeyRouteOptimizer(space_map)
path, stats = optimizer.optimize_route_from_json_data('1')
print(f"Estrellas visitadas: {stats['stars_visited']}")
```

### Simular Comer Estrella
```python
star = space_map.get_star('1')
if burro.can_eat_star(star):
    burro.consume_resources_eating_star(star)
```

### Simular Viaje
```python
if burro.can_travel(distance):
    burro.consume_resources_traveling(distance)
```

## 🎯 Objetivos del Sistema

1. **Maximizar estrellas visitadas**: El objetivo principal es visitar el mayor número de estrellas posible
2. **Gestión de recursos**: Balancear energía y pasto para sobrevivir
3. **Optimización inteligente**: Encontrar rutas eficientes considerando beneficios vs costos
4. **Realismo**: Factor de edad y estado de salud afectan el rendimiento

## 🔄 Migración de Datos

### Mapeo de Campos Antiguos → Nuevos
- `name` → `label`
- `type` → `hypergiant` (bool)
- `health`, `fuel`, `food`, `oxygen` → `current_energy`, `current_pasto`
- Sistema de combustible → Sistema de energía/pasto
- Nave espacial → Burro astronauta

## 📝 Notas Importantes

1. **JSON no modificado**: Los archivos JSON originales no se modifican
2. **Compatibilidad**: El sistema detecta automáticamente la estructura JSON
3. **Escalabilidad**: Fácil agregar nuevas constelaciones y estrellas
4. **Flexibilidad**: Parámetros configurables para diferentes escenarios

---

**🌟 El sistema está completamente actualizado y listo para usar con la nueva lógica JSON!**