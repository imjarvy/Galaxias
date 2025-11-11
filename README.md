# Galaxias: Simulador Interactivo de Rutas Espaciales

## Resumen del Proyecto

Galaxias es un sistema interactivo en Python que simula rutas espaciales entre estrellas de constelaciones cercanas en la Vía Láctea, protagonizado por un burro astronauta. Permite planificar, visualizar y analizar viajes espaciales considerando recursos, peligros y eventos dinámicos como cometas.

## Objetivo

Facilitar la exploración y análisis de rutas óptimas entre estrellas, integrando visualización, gestión de recursos y eventos científicos en un entorno educativo y lúdico.

## Funcionalidad Principal
- Cálculo de rutas óptimas entre estrellas (Dijkstra)
- Visualización interactiva del mapa estelar
- Gestión de recursos del burro astronauta (salud, combustible, comida, oxígeno)
- Bloqueo dinámico de rutas por cometas
- Parámetros científicos configurables
- Interfaz gráfica (GUI) y modo línea de comandos (CLI)
- Reportes visuales y métricas de viaje

## Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Librerías principales sugeridas
- matplotlib (visualización)
- numpy (cálculos numéricos)
- networkx (algoritmos de grafos)
- Pillow (procesamiento de imágenes)

Instala las dependencias recomendadas con:
```bash
pip install matplotlib numpy networkx Pillow
```

## Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/imjarvy/Galaxias.git
   cd Galaxias
   ```
2. Instala las dependencias (ver arriba).
3. Ejecuta el sistema:
   ```bash
   python main.py
   ```

## Estructura de Carpetas

```text
Galaxias/
├── assets/                        # Imágenes y reportes generados
├── data/                          # Datos de constelaciones y configuración
│   ├── constellations.json            # Definición de estrellas y rutas
│   └── spaceship_config.json          # Configuración del burro astronauta
├── docs/                          # Documentación técnica y guías de usuario
│   ├── TECHNICAL.md
│   ├── USER_GUIDE.md
│   └── VIDEO_GUIDE.md
├── src/                           # Código fuente principal
│   ├── algorithms/                    # Algoritmos de rutas, saltos y optimización
│   │   ├── __init__.py
│   │   ├── donkey_optimization.py     # Optimización de rutas para máximo de estrellas visitadas
│   │   ├── hypergiant_jump.py         # Saltos hipergigantes entre constelaciones
│   │   └── route_calculator.py        # Algoritmos de cálculo de rutas y análisis de caminos
│   ├── core/    # Modelos y lógica central del sistema (estrellas, rutas, burro, cometas, validaciones e impacto de investigación)
│   │   ├── __init__.py
│   │   ├── models.py       # Clases principales: Star, Route, BurroAstronauta, Comet, SpaceMap
│   │   ├── comet_impact_system.py     # Gestión de impacto de cometas sobre rutas planificadas
│   │   └── research_impact_validator.py # Validación/modelado de impacto de investigación científica
│   ├── gui/                   # Interfaz gráfica, paneles, controladores y servicios
│   │   ├── __init__.py
│   │   ├── gui_init.py                # Inicialización de la interfaz gráfica
│   │   ├── main_gui.py                # Ciclo principal de la GUI
│   │   ├── gui_callbacks.py           # Callbacks y eventos de la GUI
│   │   ├── components/                # Paneles visuales reutilizables
│   │   │   ├── __init__.py
│   │   │   ├── burro_status_panel.py      # Panel de estado del burro astronauta
│   │   │   ├── reports_panel.py           # Panel de reportes y métricas
│   │   │   ├── route_planning_panel.py    # Panel de planificación de rutas
│   │   │   └── visualization_panel.py     # Panel de visualización gráfica
│   │   ├── controllers/               # Controladores de lógica de interacción
│   │   │   ├── __init__.py
│   │   │   ├── burro_controller.py        # Controlador del burro astronauta
│   │   │   ├── life_monitoring_controller.py # Controlador de monitoreo de vida
│   │   │   ├── route_controller.py        # Controlador de rutas
│   │   │   └── visualization_controller.py # Controlador de visualización
│   │   ├── interfaces/                # Interfaces abstractas para la GUI
│   │   │   ├── __init__.py
│   │   │   ├── component_interface.py     # Interfaz base para componentes visuales
│   │   │   ├── route_service_interface.py    # Interfaz para servicios de rutas
│   │   │   └── visualization_service_interface.py   # Interfaz para servicios de visualización
│   │   ├── services/                  # Servicios auxiliares para la GUI
│   │   │   ├── __init__.py
│   │   │   ├── burro_journey_service.py   # Servicio de gestión de viajes del burro
│   │   │   ├── configuration_service.py   # Servicio de configuración de la GUI
│   │   │   ├── route_service.py           # Servicio de cálculo de rutas
│   │   │   └── visualization_service.py   # Servicio de visualización y renderizado
│   ├── parameter_editor_simple/       # Editor para modificar parámetros científicos y de simulación
│   │   ├── __init__.py
│   │   ├── editor.py         # Interfaz principal del editor de parámetros científicos
│   │   ├── comet_manager.py           # Gestión de cometas que afectan rutas
│   │   ├── models.py                 # Modelos de datos para configuraciones y presets
│   │   ├── presets.py                 # Presets y configuraciones predefinidas
│   │   ├── preview.py                 # Vista previa de efectos de parámetros editados
│   │   └── star_config.py             # Editor de parámetros específicos de estrellas
│   ├── presentation/                  # Visualización y presentación de resultados
│   │   ├── gui_hypergiant_jump.py     # Interfaz gráfica para saltos hipergigantes
│   │   ├── gui_life_monitor.py      # Interfaz gráfica para monitoreo de vida/recursos
│   │   ├── life_monitor.py            # Lógica de monitoreo de vida
│   │   └── visualizer.py              # Utilidades de visualización de datos
│   ├── route_tools/                   # Herramientas de rutas (max visit, min cost)
│   │   ├── __init__.py                # Inicialización del módulo
│   │   ├── max_visit_route.py     # Ruta que maximiza el número de estrellas visitadas
│   │   └── min_cost_route.py          # Ruta de menor gasto posible
│   └── utils/                         # Utilidades, constantes y validadores
│       ├── __init__.py                # Inicialización del módulo
│       ├── constants.py               # Constantes globales del sistema
│       ├── json_handler.py            # Utilidades para manejo de archivos JSON
│       ├── validators.py              # Validadores y utilidades de validación
│       └── burro_utils/               # Utilidades especializadas para el burro astronauta
│           ├── __init__.py            # Inicialización del submódulo
│           ├── burro_math.py          # Cálculos de consumo, energía y efectos de acciones
│           └── journey_step.py        # Representación detallada de cada paso del viaje
├── main.py                        # Punto de entrada principal
├── README.md                      # Este archivo
```

### Descripción de Carpetas/Archivos
- **assets/**: Recursos gráficos y reportes generados por el sistema.
- **data/**: Archivos JSON con datos de constelaciones y configuración del burro astronauta.
- **docs/**: Documentación técnica, guías de usuario y video.
- **src/**: Todo el código fuente modularizado:
   - **algorithms/**: Algoritmos de rutas, saltos y optimización.
      - **donkey_optimization.py**: Implementa el sistema de optimización de rutas para el Burro Astronauta. Calcula la ruta que permite visitar la mayor cantidad de estrellas antes de que el burro muera, considerando recursos y beneficios de cada estrella. Incluye simulación de viajes, cálculo de beneficios netos al “comer” estrellas, y búsqueda de la mejor estrella siguiente en cada paso. Permite encontrar la mejor estrella para iniciar el viaje y provee una función de utilidad para optimizar rutas fácilmente.
      - **hypergiant_jump.py**: Gestiona la lógica de “saltos hipergigantes” entre constelaciones (cambios de galaxia). Detecta cuándo un viaje requiere pasar por una estrella hipergigante, fuerza el paso por ella y aplica beneficios especiales (recarga de energía, duplicación de pasto). Permite planificar rutas intergalácticas, encontrar hipergigantes accesibles y destinos posibles, y simular el salto con todos sus efectos. Incluye funciones para obtener estadísticas de hipergigantes y una demo ejecutable desde línea de comandos.
      - **route_calculator.py**: Contiene los algoritmos principales para calcular rutas óptimas entre estrellas usando Dijkstra y otras estrategias. Permite calcular distancias, peligros, energía y recursos necesarios para cada ruta. Incluye funciones para encontrar todas las estrellas alcanzables, secuencias óptimas de “comidas”, y rutas que maximizan visitas o minimizan el gasto, usando parámetros del JSON de configuración. Centraliza la lógica de análisis de caminos, heurísticas y restricciones de recursos.
   - **core/**: Modelos y lógica central del sistema (estrellas, rutas, burro, cometas, validaciones e impacto de investigación).
      - **models.py**: Define las clases principales del sistema: `Star` (estrella), `Route` (ruta entre estrellas), `BurroAstronauta` (burro astronauta con recursos, salud y lógica de viaje), `Comet` (cometa que puede bloquear rutas), y `SpaceMap` (mapa espacial que gestiona estrellas, rutas, cometas y la creación del burro). Incluye lógica para consumir recursos, monitorear vida, restaurar estado, verificar bidireccionalidad de rutas y cargar datos desde JSON.
      - **comet_impact_system.py**: Gestiona el impacto de cometas sobre rutas planificadas. Permite invalidar rutas, buscar segmentos afectados, calcular rutas alternativas y notificar a listeners sobre cambios. Incluye interfaces y clases para validación y cálculo de rutas, así como un gestor principal de impacto de cometas.
      - **research_impact_validator.py**: Valida y modela el impacto de la investigación científica sobre la salud y vida del burro astronauta para cada estrella. Permite configurar, calcular y exportar/importar los efectos de la investigación (salud, vida, eficiencia energética, riesgo) tanto por estrella como para rutas completas. Incluye una interfaz gráfica para editar y validar estos impactos.
   - **gui/**: Interfaz gráfica, paneles, controladores y servicios para la interacción visual del usuario.
      - **gui_init.py, main_gui.py, gui_callbacks.py**: Inicialización, ciclo principal y callbacks de la interfaz gráfica.
      - **components/**: Paneles visuales reutilizables de la GUI.
         - **burro_status_panel.py**: Panel de estado del burro astronauta.
         - **reports_panel.py**: Panel para mostrar reportes y métricas.
         - **route_planning_panel.py**: Panel para planificación y visualización de rutas.
         - **visualization_panel.py**: Panel de visualización gráfica del mapa estelar.
      - **controllers/**: Controladores que gestionan la lógica de interacción entre la GUI y el modelo de datos.
         - **burro_controller.py**: Controlador de acciones y estado del burro astronauta.
         - **life_monitoring_controller.py**: Controlador de monitoreo de vida y recursos.
         - **route_controller.py**: Controlador de planificación y cálculo de rutas.
         - **visualization_controller.py**: Controlador de visualización y actualización gráfica.
      - **interfaces/**: Interfaces abstractas para componentes y servicios de la GUI.
         - **component_interface.py**: Interfaz base para componentes visuales.
         - **route_service_interface.py**: Interfaz para servicios de rutas.
         - **visualization_service_interface.py**: Interfaz para servicios de visualización.
      - **services/**: Servicios auxiliares para la lógica de la GUI.
         - **burro_journey_service.py**: Servicio para gestionar los viajes del burro.
         - **configuration_service.py**: Servicio para configuración y parámetros de la GUI.
         - **route_service.py**: Servicio para cálculo y gestión de rutas desde la GUI.
         - **visualization_service.py**: Servicio para renderizado y actualización de visualizaciones.
   - **parameter_editor_simple/**: Editor para modificar parámetros científicos y de simulación.
      - **editor.py**: Interfaz principal del editor de parámetros científicos, permite modificar y guardar configuraciones que afectan la simulación.
      - **comet_manager.py**: Herramienta para gestionar la creación, edición y eliminación de cometas que afectan rutas.
      - **models.py**: Modelos de datos para representar configuraciones, presets y parámetros editables.
      - **presets.py**: Presets y configuraciones predefinidas para parámetros científicos y de simulación.
      - **preview.py**: Vista previa de los efectos de los parámetros editados antes de aplicarlos a la simulación.
      - **star_config.py**: Editor y gestor de parámetros específicos de estrellas (energía, tiempo de consumo, etc.).
  - **presentation/**: Visualización y presentación de resultados.
     - **gui_hypergiant_jump.py**: Implementa la interfaz gráfica para gestionar y visualizar los saltos hipergigantes, permitiendo al usuario interactuar con eventos espaciales de gran escala.
     - **gui_life_monitor.py**: Proporciona una interfaz gráfica para el monitoreo de vida y recursos, mostrando información crítica sobre el estado de la simulación o misión.
     - **life_monitor.py**: Contiene la lógica central para el monitoreo de vida, recursos y condiciones, sirviendo de backend para las interfaces gráficas relacionadas.
     - **visualizer.py**: Ofrece utilidades y funciones para la visualización de datos, gráficos y resultados, facilitando la interpretación visual de la información generada por el sistema.
  - **route_tools/**: Herramientas para cálculo de rutas específicas.
     - **max_visit_route.py**: Calcula la ruta que permite visitar el mayor número de estrellas posibles desde una estrella inicial, usando solo parámetros inmutables. Incluye lógica de saltos hipergigantes, beneficios de recursos y salida detallada en formato JSON.
     - **min_cost_route.py**: Sistema de optimización de rutas con el criterio de menor gasto posible, considerando reglas de consumo, salud, saltos hipergigantes y acciones detalladas en cada estrella. Permite analizar el recorrido más eficiente en recursos.
     - **__init__.py**: Inicialización del módulo de herramientas de rutas.
  - **utils/**: Funciones utilitarias, constantes y validadores.
     - **constants.py**: Centraliza todas las constantes y configuraciones globales del sistema (rutas, colores, parámetros de visualización, etc.).
     - **json_handler.py**: Utilidades para la carga y guardado de archivos JSON, con manejo de errores y funciones específicas para constelaciones y configuración de la nave.
     - **validators.py**: Proporciona funciones de validación para IDs, coordenadas y otros datos, lanzando excepciones personalizadas en caso de error.
     - **burro_utils/**: Utilidades especializadas para el burro astronauta:
        - **burro_math.py**: Funciones para calcular capacidad de consumo, energía obtenida al comer, y efectos de investigación sobre estrellas.
        - **journey_step.py**: Define la estructura y cálculos detallados de cada paso del viaje del burro, incluyendo recursos, bonificaciones y efectos de acciones.
        - **__init__.py**: Inicialización del submódulo de utilidades del burro.
     - **__init__.py**: Inicialización del módulo de utilidades.
- **main.py**: Script principal y punto de entrada del sistema. Permite iniciar la interfaz gráfica (GUI), ejecutar el sistema en modo línea de comandos (CLI) o lanzar una demostración completa. Gestiona la carga de configuraciones, inicialización de modelos, cálculo y optimización de rutas, visualización de mapas y recursos, y la integración de eventos como cometas. Ofrece:
   - `python main.py` para iniciar la GUI interactiva.
   - `python main.py --cli` para modo consola con selección de rutas y optimización.
   - `python main.py --demo` para ejecutar una demostración automatizada con generación de visualizaciones y reportes.
- **README.md**: Documentación principal del proyecto.

## Uso Básico
- Ejecuta `python main.py` para abrir la interfaz gráfica.
- Usa los paneles para planificar rutas, gestionar recursos y visualizar el mapa estelar.
- Consulta la documentación en `docs/` para detalles avanzados y ejemplos.

## Contribución
1. Haz un fork del repositorio.
2. Crea una rama para tu funcionalidad.
3. Realiza tus cambios y haz commit.
4. Abre un Pull Request.

## Licencia
Proyecto de código abierto para fines educativos e investigativos.

---
¡Que el burro astronauta te acompañe en tus viajes espaciales!