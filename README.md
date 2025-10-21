# Galaxias - Sistema Interactivo de Rutas Espaciales 🫏🚀

Sistema interactivo en Python que simula rutas espaciales entre estrellas de constelaciones cercanas en la Vía Láctea, con un burro astronauta como protagonista.

## Características Principales

### 🌟 Funcionalidades Implementadas

1. **Gestión de Rutas Espaciales**
   - Cálculo de rutas óptimas entre estrellas usando el algoritmo de Dijkstra
   - Visualización de conexiones entre estrellas de diferentes constelaciones
   - Métricas de distancia, peligro y costo de viaje

2. **Burro Astronauta**
   - Sistema de salud, combustible, comida y oxígeno
   - Consumo de recursos basado en distancia y nivel de peligro
   - Historial de viajes
   - Sistema de recarga de recursos

3. **Gestión de Cometas**
   - Bloqueo dinámico de rutas por cometas
   - Agregar y remover cometas en tiempo real
   - Recálculo automático de rutas alternativas

4. **Parámetros Científicos**
   - Constantes físicas configurables
   - Tasas de consumo de recursos ajustables
   - Factor de curvatura (warp) y eficiencia de escudos

5. **Visualizaciones**
   - Mapa estelar interactivo con matplotlib
   - Gráficos de estado de recursos
   - Reportes visuales completos de viajes
   - Colores específicos por tipo de estrella

6. **Interfaz Gráfica (GUI)**
   - Interfaz completa con tkinter
   - Visualización en tiempo real del mapa
   - Controles para planificación y navegación
   - Panel de estado del burro astronauta

7. **Múltiples Modos de Uso**
   - Modo GUI (interfaz gráfica)
   - Modo CLI (línea de comandos)
   - Modo DEMO (demostración automática)

## Estructura del Proyecto

```
Galaxias/
├── data/
│   ├── constellations.json      # Datos de constelaciones y estrellas
│   └── spaceship_config.json    # Configuración del burro astronauta
├── src/
│   ├── models.py                # Clases principales (Star, Route, SpaceshipDonkey)
│   ├── route_calculator.py     # Algoritmo de cálculo de rutas
│   ├── visualizer.py           # Visualizaciones con matplotlib
│   └── gui.py                  # Interfaz gráfica con tkinter
├── assets/                      # Imágenes y reportes generados
├── docs/                        # Documentación adicional
├── main.py                      # Punto de entrada principal
├── requirements.txt            # Dependencias Python
└── README.md                   # Este archivo
```

## Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone https://github.com/imjarvy/Galaxias.git
cd Galaxias

# Instalar dependencias
pip install -r requirements.txt
```

### Dependencias

- `matplotlib>=3.7.0` - Visualizaciones gráficas
- `numpy>=1.24.0` - Cálculos numéricos
- `networkx>=3.1` - Algoritmos de grafos
- `Pillow>=10.0.0` - Procesamiento de imágenes

## Uso

### Modo GUI (Recomendado)

```bash
python main.py
```

Esto abrirá la interfaz gráfica donde puedes:
- Seleccionar estrellas de origen y destino
- Calcular rutas óptimas
- Iniciar viajes
- Agregar/remover cometas
- Ver parámetros científicos
- Generar reportes visuales

### Modo CLI

```bash
python main.py --cli
```

Modo interactivo de línea de comandos para usuarios avanzados.

### Modo Demo

```bash
python main.py --demo
```

Ejecuta una demostración automática del sistema con:
- Cálculo de rutas
- Bloqueo de rutas con cometas
- Simulación de viaje completo
- Generación de visualizaciones

## Datos de Constelaciones

### Constelaciones Incluidas

1. **Orión** - 3 estrellas
   - Betelgeuse (gigante roja)
   - Rigel (supergigante azul)
   - Bellatrix (gigante azul)

2. **Canis Major** - 2 estrellas
   - Sirius (secuencia principal)
   - Adhara (gigante azul)

3. **Ursa Major** - 3 estrellas
   - Dubhe (gigante)
   - Merak (secuencia principal)
   - Alioth (secuencia principal)

4. **Lyra** - 1 estrella
   - Vega (secuencia principal)

### Formato JSON

Las estrellas se definen con:
- `id`: Identificador único
- `name`: Nombre de la estrella
- `x`, `y`: Coordenadas en el mapa
- `type`: Tipo estelar
- `distance_ly`: Distancia en años luz

Las rutas incluyen:
- `from`, `to`: IDs de estrellas conectadas
- `distance`: Distancia de viaje
- `danger_level`: Nivel de peligro (1-5)

## Configuración del Burro Astronauta

El archivo `spaceship_config.json` contiene:

### Recursos Iniciales
- Salud: 100
- Combustible: 1000
- Comida: 50
- Oxígeno: 100

### Tasas de Consumo
- Combustible: 2 unidades por unidad de distancia
- Comida: 0.1 unidades por unidad de distancia
- Oxígeno: 0.5 unidades por unidad de distancia
- Salud: 5 puntos por nivel de peligro

### Parámetros Científicos
- Constante gravitacional: 6.674×10⁻¹¹
- Velocidad de la luz: 299,792 km/s
- Factor de curvatura: 1.5
- Eficiencia de escudos: 0.8

## Algoritmo de Rutas

El sistema utiliza el **algoritmo de Dijkstra** para encontrar la ruta óptima entre estrellas, considerando:

1. **Distancia física** entre estrellas
2. **Nivel de peligro** de cada ruta
3. **Rutas bloqueadas** por cometas
4. **Consumo de recursos** del burro astronauta

### Función de Costo

```
Costo = (Distancia × Tasa_Combustible) + (Peligro × Penalización_Peligro)
```

## Visualizaciones

### Mapa Estelar

- Estrellas coloreadas según su tipo
- Rutas visualizadas como líneas grises
- Rutas bloqueadas en rojo punteado
- Ruta óptima resaltada en cyan
- Ubicación del burro astronauta marcada con estrella dorada

### Reporte de Viaje

Incluye:
- Información de la ruta recorrida
- Estadísticas del viaje
- Recursos consumidos
- Estado actual del burro astronauta
- Historial de ubicaciones visitadas

## Ejemplos de Uso

### Ejemplo 1: Calcular Ruta Simple

```python
from src.models import SpaceMap, SpaceshipDonkey
from src.route_calculator import RouteCalculator
import json

# Cargar configuración
with open('data/spaceship_config.json', 'r') as f:
    config = json.load(f)

# Inicializar mapa
space_map = SpaceMap('data/constellations.json')

# Obtener estrellas
betelgeuse = space_map.get_star('orion_1')
sirius = space_map.get_star('canis_1')

# Calcular ruta
calculator = RouteCalculator(space_map, config)
path, cost = calculator.dijkstra(betelgeuse, sirius)

print(f"Ruta: {' → '.join([s.name for s in path])}")
print(f"Costo: {cost:.2f}")
```

### Ejemplo 2: Agregar Cometa

```python
from src.models import Comet

# Crear cometa que bloquea una ruta
halley = Comet(name="Halley", blocked_routes=[('orion_2', 'canis_1')])
space_map.add_comet(halley)

# La ruta se recalculará automáticamente evitando el bloqueo
```

### Ejemplo 3: Simular Viaje

```python
# Crear burro astronauta
donkey = SpaceshipDonkey(
    name="Burro Astronauta",
    health=100,
    fuel=1000,
    food=50,
    oxygen=100
)

# Viajar por la ruta
for i in range(len(path) - 1):
    current = path[i]
    next_star = path[i + 1]
    
    # Encontrar ruta
    route = next((r for r in space_map.routes 
                  if (r.from_star == current and r.to_star == next_star) or
                     (r.to_star == current and r.from_star == next_star)), None)
    
    if route:
        donkey.consume_resources(route.distance, route.danger_level, config)
        donkey.current_location = next_star

print(f"Salud final: {donkey.health:.1f}")
```

## Control de Versiones

El proyecto utiliza Git para control de versiones. Commits importantes:

- Estructura inicial del proyecto
- Implementación de modelos de datos
- Algoritmo de cálculo de rutas
- Sistema de visualización
- Interfaz gráfica
- Documentación completa

## Video Descriptivo

Para ver una demostración en video del sistema, ejecute:

```bash
python main.py --demo
```

Esto generará visualizaciones que muestran:
1. Mapa estelar con rutas
2. Cálculo de ruta óptima
3. Bloqueo de rutas con cometas
4. Simulación de viaje
5. Estado final de recursos

## Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible para uso educativo y de investigación.

## Autor

**imjarvy** - Sistema Galaxias

## Agradecimientos

- Inspirado en la exploración espacial y la ciencia ficción
- Datos estelares basados en constelaciones reales de la Vía Láctea
- El burro astronauta representa la curiosidad y perseverancia en la exploración

## Contacto

Para preguntas, sugerencias o reportar problemas:
- Abrir un issue en GitHub
- Contribuir al proyecto

---

🫏 **¡Que el burro astronauta te acompañe en tus viajes espaciales!** 🚀