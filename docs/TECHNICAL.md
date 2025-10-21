# Documentación Técnica - Galaxias

## Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────────────────────────────────────┐
│                   main.py                       │
│           (Punto de entrada)                    │
└────────────┬───────────────────────────────────┘
             │
   ┌─────────┴─────────┐
   │                   │
   ▼                   ▼
┌──────┐          ┌──────┐
│ CLI  │          │ GUI  │
└───┬──┘          └───┬──┘
    │                 │
    └────────┬────────┘
             │
    ┌────────┴────────────────────────┐
    │                                 │
    ▼                                 ▼
┌─────────┐                    ┌──────────────┐
│ Models  │◄───────────────────┤ Visualizer   │
└────┬────┘                    └──────────────┘
     │
     ▼
┌────────────────┐
│RouteCalculator │
└────────────────┘
```

## Módulos

### 1. models.py

Clases de datos y lógica de negocio.

#### Clase Star

```python
@dataclass
class Star:
    id: str
    name: str
    x: float
    y: float
    type: str
    distance_ly: float
```

**Responsabilidades**:
- Representar una estrella en el espacio
- Almacenar coordenadas y propiedades

**Métodos**:
- `__hash__()`: Permite usar Star en sets y como clave de diccionario
- `__eq__()`: Comparación de estrellas por ID

#### Clase Route

```python
@dataclass
class Route:
    from_star: Star
    to_star: Star
    distance: float
    danger_level: int
    blocked: bool = False
    blocked_by_comet: str = ""
```

**Responsabilidades**:
- Representar conexión entre estrellas
- Gestionar estado de bloqueo

**Métodos**:
- `calculate_cost()`: Calcula costo total considerando distancia y peligro

#### Clase SpaceshipDonkey

```python
@dataclass
class SpaceshipDonkey:
    name: str
    health: float
    fuel: float
    food: float
    oxygen: float
    current_location: Optional[Star]
    journey_history: List[Star]
```

**Responsabilidades**:
- Gestionar recursos del burro astronauta
- Rastrear ubicación y historial
- Simular consumo de recursos

**Métodos principales**:
- `consume_resources()`: Reduce recursos según viaje
- `is_alive()`: Verifica si puede continuar
- `can_travel()`: Verifica recursos suficientes
- `refuel()`: Recarga recursos
- `get_status()`: Obtiene estado actual

#### Clase SpaceMap

```python
class SpaceMap:
    stars: Dict[str, Star]
    routes: List[Route]
    comets: List[Comet]
```

**Responsabilidades**:
- Cargar y gestionar datos del mapa
- Administrar cometas y bloqueos
- Proporcionar acceso a estrellas y rutas

**Métodos principales**:
- `load_data()`: Carga desde JSON
- `get_star()`: Obtiene estrella por ID
- `get_routes_from()`: Obtiene rutas desde una estrella
- `add_comet()`: Agrega cometa y bloquea rutas
- `remove_comet()`: Remueve cometa y desbloquea rutas

### 2. route_calculator.py

Algoritmos de cálculo de rutas.

#### Clase RouteCalculator

**Algoritmo Principal: Dijkstra**

```python
def dijkstra(self, start: Star, end: Star) -> Tuple[Optional[List[Star]], float]:
```

**Pseudocódigo**:
```
1. Inicializar distancias a infinito
2. Distancia al origen = 0
3. Crear cola de prioridad con origen
4. Mientras cola no vacía:
   a. Extraer nodo con menor distancia
   b. Si es el destino, reconstruir camino
   c. Para cada vecino no visitado:
      - Calcular nuevo costo
      - Si menor que distancia actual:
        * Actualizar distancia
        * Actualizar nodo anterior
        * Agregar a cola
5. Retornar camino o None
```

**Complejidad**:
- Tiempo: O((V + E) log V) con heap binario
- Espacio: O(V) para estructuras de datos

**Métodos auxiliares**:
- `calculate_path_stats()`: Calcula estadísticas de un camino
- `find_all_reachable_stars()`: Encuentra estrellas alcanzables

### 3. visualizer.py

Sistema de visualización con matplotlib.

#### Clase SpaceVisualizer

**Métodos de visualización**:

1. **plot_space_map()**
   - Dibuja mapa completo
   - Resalta rutas y estrellas
   - Muestra ubicación del burro

2. **plot_resource_status()**
   - Gráfico de barras de recursos
   - Código de colores por tipo

3. **plot_journey_report()**
   - Reporte completo en 4 paneles
   - Información de viaje, recursos, historial, estado

**Paleta de colores**:
```python
star_colors = {
    'red_giant': '#FF4444',
    'blue_giant': '#4444FF',
    'blue_supergiant': '#2222CC',
    'main_sequence': '#FFFF44',
    'giant': '#FF8844'
}
```

### 4. gui.py

Interfaz gráfica con tkinter.

#### Clase GalaxiasGUI

**Estructura de UI**:
```
Root Window
├── Left Panel (Controls)
│   ├── Route Planning
│   ├── Spaceship Status
│   ├── Comet Management
│   ├── Scientific Parameters
│   └── Reports
└── Right Panel (Visualization)
    ├── Canvas (matplotlib)
    └── Info Text
```

**Flujo de eventos**:
1. Usuario selecciona estrellas
2. `calculate_route()` → Calcula ruta óptima
3. `update_visualization()` → Actualiza mapa
4. Usuario inicia viaje
5. `start_journey()` → Simula viaje
6. `update_status_display()` → Actualiza estado

## Formatos de Datos

### constellations.json

```json
{
  "constellations": [
    {
      "name": "string",
      "stars": [
        {
          "id": "string",
          "name": "string",
          "x": number,
          "y": number,
          "type": "string",
          "distance_ly": number
        }
      ]
    }
  ],
  "routes": [
    {
      "from": "string (star_id)",
      "to": "string (star_id)",
      "distance": number,
      "danger_level": number (1-5)
    }
  ]
}
```

### spaceship_config.json

```json
{
  "spaceship_donkey": {
    "name": "string",
    "initial_health": number,
    "initial_fuel": number,
    "initial_food": number,
    "initial_oxygen": number
  },
  "consumption_rates": {
    "fuel_per_unit_distance": number,
    "food_per_unit_distance": number,
    "oxygen_per_unit_distance": number,
    "health_decay_per_danger": number
  },
  "scientific_parameters": {
    "gravity_constant": number,
    "light_speed_km_s": number,
    "warp_factor": number,
    "shield_efficiency": number
  }
}
```

## Algoritmos y Complejidad

### Dijkstra Implementation

**Estructuras de datos**:
- Priority Queue (heapq): O(log n) insert/extract
- Dictionary para distancias: O(1) lookup
- Dictionary para nodos previos: O(1) lookup

**Optimizaciones**:
- Early termination al alcanzar destino
- Set de visitados para evitar reprocesamiento
- Cálculo de costo incorpora múltiples factores

### Cálculo de Costo

```python
def calculate_cost(distance, danger, fuel_rate, danger_penalty):
    base_cost = distance * fuel_rate
    danger_cost = danger * danger_penalty
    return base_cost + danger_cost
```

**Factores**:
- Distancia física (lineal)
- Nivel de peligro (multiplicador)
- Bloqueo (costo infinito)

## Extensibilidad

### Agregar Nuevas Estrellas

1. Editar `data/constellations.json`
2. Agregar entrada en array de stars
3. Agregar rutas correspondientes

### Agregar Nuevos Tipos de Recursos

1. Modificar clase `SpaceshipDonkey`
2. Actualizar `consume_resources()`
3. Actualizar visualizaciones
4. Modificar configuración JSON

### Implementar Nuevos Algoritmos

```python
class RouteCalculator:
    def a_star(self, start, end):
        # Implementar A* con heurística de distancia euclidiana
        pass
    
    def bellman_ford(self, start, end):
        # Para detectar ciclos negativos
        pass
```

## Testing

### Pruebas Unitarias Recomendadas

```python
def test_star_creation():
    star = Star("test_1", "Test", 0, 0, "main_sequence", 10)
    assert star.id == "test_1"

def test_route_cost_calculation():
    star1 = Star("s1", "S1", 0, 0, "main_sequence", 10)
    star2 = Star("s2", "S2", 100, 100, "main_sequence", 20)
    route = Route(star1, star2, 100, 2)
    cost = route.calculate_cost(2, 50)
    assert cost == 300  # 100*2 + 2*50

def test_dijkstra_simple_path():
    # Crear mapa de prueba
    # Verificar que encuentra ruta más corta
    pass
```

## Mejoras Futuras

1. **Persistencia de Estado**
   - Guardar/cargar partidas
   - Base de datos SQLite

2. **Multijugador**
   - Sistema de turnos
   - Competencia por recursos

3. **Eventos Aleatorios**
   - Encuentros con alienígenas
   - Descubrimientos científicos
   - Tormentas solares

4. **Mejoras de UI**
   - Animaciones de viaje
   - Efectos de sonido
   - Temas visuales personalizables

5. **Optimizaciones**
   - Cache de rutas calculadas
   - Índices espaciales para búsqueda rápida
   - Procesamiento paralelo para múltiples rutas

## Referencias

- Dijkstra's Algorithm: [Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- Matplotlib Documentation: [matplotlib.org](https://matplotlib.org/)
- Tkinter Tutorial: [docs.python.org](https://docs.python.org/3/library/tkinter.html)
- Graph Theory: Cormen et al., "Introduction to Algorithms"

---

Documentación generada para Galaxias v1.0
