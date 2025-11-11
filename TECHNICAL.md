# Manual Técnico

## Galaxias: Simulador Interactivo de Rutas Espaciales
**Versión:** 1.0.0  
**Fecha de publicación:** 11/11/2025  
**Autor:** imjarvy / U. de Caldas

---

## Índice
1. [Introducción](#introducción)
2. [Especificaciones técnicas](#especificaciones-técnicas)
3. [Instalación y configuración](#instalación-y-configuración)
4. [Descripción funcional](#descripción-funcional)
5. [Procedimientos operativos](#procedimientos-operativos)
6. [Mantenimiento](#mantenimiento)
7. [Solución de problemas](#solución-de-problemas)
8. [Glosario](#glosario)
9. [Anexos](#anexos)
10. [Control de versiones](#control-de-versiones)

---


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


**Propósito:** Documentar la arquitectura, uso y mantenimiento del sistema Galaxias.

**Alcance:** Simulación, visualización y análisis de rutas espaciales entre estrellas, con gestión de recursos y eventos dinámicos.

**Público objetivo:** Desarrolladores, docentes, estudiantes y usuarios técnicos interesados en simulación y visualización científica.

**Descripción breve:** Galaxias es un sistema modular en Python para simular viajes espaciales, optimizar rutas y analizar recursos, usando algoritmos avanzados y una interfaz gráfica interactiva.

---

## 2. Especificaciones técnicas
**Requisitos de hardware:**
- CPU dual-core, 2GB RAM, 200MB disco

**Requisitos de software:**
- Python 3.8 o superior
- pip
- SO: Windows, Linux o MacOS

**Tecnologías utilizadas:**
- Python, tkinter, matplotlib, numpy, networkx, Pillow

**Arquitectura:**
- Modular, orientada a objetos, estructura por carpetas (ver README)
- Archivos de configuración en JSON

---

## 3. Instalación y configuración
1. Clona el repositorio:
	```bash
	git clone https://github.com/imjarvy/Galaxias.git
	cd Galaxias
	```
2. Instala dependencias:
	```bash
	pip install matplotlib numpy networkx Pillow
	```
3. Configura archivos en `data/` si deseas personalizar estrellas o parámetros.
4. (Opcional) Ajusta variables de entorno si usas rutas personalizadas.

---

## 4. Descripción funcional
**Módulos principales:**
- `main.py`: Punto de entrada, orquesta modos GUI, CLI y demo.
- `src/algorithms/`: Algoritmos de rutas y optimización.
- `src/core/`: Modelos, lógica central, validadores científicos.
- `src/gui/`: Interfaz gráfica, paneles y controladores.
- `src/parameter_editor_simple/`: Editor de parámetros científicos.
- `src/presentation/`: Visualización avanzada y reportes.
- `src/route_tools/`: Herramientas de rutas especializadas.
- `src/utils/`: Constantes, validadores y utilidades.

**Interacción entre módulos:**
- `main.py` inicializa modelos y selecciona modo de operación.
- Los algoritmos y validadores se comunican vía objetos y servicios.
- La GUI consume servicios y muestra resultados en paneles.

**Diagramas:**
> Ver anexos para diagramas de arquitectura y flujo.

---

## 5. Procedimientos operativos
**Ejecución:**
- GUI: `python main.py`

**Entradas y salidas:**
- Entradas: Archivos JSON, selección de estrellas, parámetros por GUI/CLI
- Salidas: Visualizaciones (`assets/`), reportes, métricas en consola

**Ejemplo de uso:**
```bash
python main.py 
# Selecciona estrellas, calcula rutas, genera visualización
```

---

## 6. Mantenimiento
- Revisar y actualizar dependencias periódicamente
- Realizar respaldos de archivos en `data/` y `assets/`
- Para actualizar el sistema, hacer pull del repositorio y reinstalar dependencias si es necesario
- Restaurar archivos de configuración desde respaldos ante errores

---

## 7. Solución de problemas
**Errores comunes:**
- "No module named ...": Verifica dependencias instaladas
- "JSONDecodeError": Revisa formato de archivos en `data/`
- GUI no abre: Verifica versión de Python y dependencias

**Diagnóstico:**
- Ejecuta en consola y revisa mensajes de error
- Usa archivos de ejemplo originales para descartar errores de configuración

---

## 8. Glosario
- **Burro Astronauta**: Personaje principal, gestiona recursos y realiza viajes
- **Constelación**: Grupo de estrellas conectadas
- **Cometa**: Evento que bloquea rutas
- **GUI**: Interfaz gráfica de usuario
- **CLI**: Interfaz de línea de comandos
- **Presets**: Configuraciones predefinidas

---

## 9. Anexos
- Diagramas de arquitectura y flujo (ver carpeta `docs/`)
- Ejemplos de archivos JSON de configuración (`data/`)
- Referencias: [README.md](./README.md)

---

## 10. Control de versiones
| Versión | Fecha       | Responsable | Descripción                |
|---------|-------------|-------------|----------------------------|
| 1.0.0   | 11/11/2025  | imjarvy     | Versión inicial del manual |
