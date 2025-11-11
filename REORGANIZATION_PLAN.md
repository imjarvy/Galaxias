# 🏗️ REORGANIZACIÓN DE SRC/ - ARQUITECTURA LIMPIA

## 📊 ESTRUCTURA ACTUAL (Desordenada)

```
src/
├── gui/                           # ✅ Nueva arquitectura SOLID
├── comet_impact_system.py         # 🔄 Mover a core/
├── donkey_optimization.py         # 🔄 Mover a algorithms/
├── gui.py                         # 🔄 Deprecado, mantener por compatibilidad
├── gui_hypergiant_jump.py         # 🔄 Mover a gui/components/
├── gui_life_monitor.py            # 🔄 Mover a gui/components/
├── gui_new.py                     # ❌ Eliminar (redundante)
├── gui_refactored.py              # ❌ Eliminar (redundante)
├── hypergiant_jump.py             # 🔄 Mover a core/
├── life_monitor.py                # 🔄 Mover a core/
├── max_visit_route.py             # 🔄 Mover a algorithms/
├── min_cost_route.py              # 🔄 Mover a algorithms/
├── models.py                      # 🔄 Mover a core/
├── parameter_editor_simple/       # 🔄 Mover a gui/components/
├── research_impact_validator.py   # 🔄 Mover a core/
├── route_calculator.py            # 🔄 Mover a algorithms/
├── visualizer.py                  # 🔄 Mover a presentation/
└── __init__.py                    # 🔄 Actualizar imports
```

## 🎯 NUEVA ESTRUCTURA (Arquitectura Limpia)

```
src/
├── 📁 core/                       # Lógica de negocio central
│   ├── __init__.py
│   ├── models.py                  # Entidades principales (Star, Burro, etc.)
│   ├── life_monitor.py            # Monitoreo de vida
│   ├── hypergiant_jump.py         # Saltos hipergigantes
│   ├── research_impact_validator.py # Validación de impactos
│   └── comet_impact_system.py     # Sistema de cometas
│
├── 📁 algorithms/                 # Algoritmos de cálculo
│   ├── __init__.py
│   ├── route_calculator.py        # Dijkstra y cálculos básicos
│   ├── donkey_optimization.py     # Optimización del burro
│   ├── max_visit_route.py         # Máximas visitas
│   └── min_cost_route.py          # Menor costo
│
├── 📁 presentation/               # Visualización y reportes
│   ├── __init__.py
│   └── visualizer.py              # Matplotlib, gráficos
│
├── 📁 gui/                        # ✅ Arquitectura SOLID (ya creada)
│   ├── __init__.py
│   ├── main_gui.py
│   ├── interfaces/
│   ├── services/
│   ├── components/
│   │   ├── parameter_editor/      # Editor de parámetros
│   │   ├── hypergiant_gui.py     # GUI saltos hipergigantes
│   │   └── life_monitor_gui.py   # GUI monitoreo de vida
│   └── controllers/
│
├── 📁 utils/                      # Utilidades y helpers
│   ├── __init__.py
│   ├── config_loader.py           # Carga de configuraciones
│   ├── file_utils.py              # Utilidades de archivos
│   └── validation.py              # Validaciones comunes
│
├── 📁 scripts/                    # Scripts de línea de comandos
│   ├── __init__.py
│   ├── run_max_visit.py           # Ejecutar max visit
│   ├── run_min_cost.py            # Ejecutar min cost
│   └── run_optimization.py       # Ejecutar optimización
│
├── gui.py                         # Compatibilidad hacia atrás
└── __init__.py                    # Exports principales
```

## 🔄 BENEFICIOS DE LA REORGANIZACIÓN

### 1. **Separación de Responsabilidades**
- **core/**: Lógica de negocio pura
- **algorithms/**: Algoritmos de cálculo
- **presentation/**: Visualización 
- **gui/**: Interfaz de usuario
- **utils/**: Utilidades compartidas

### 2. **Principios de Arquitectura Limpia**
- **Independencia**: Cada capa es independiente
- **Testabilidad**: Fácil testing por separado
- **Mantenibilidad**: Cambios localizados
- **Escalabilidad**: Fácil agregar nuevas funcionalidades

### 3. **Imports Claros**
```python
# Lógica de negocio
from src.core.models import Star, BurroAstronauta
from src.core.life_monitor import LifeMonitor

# Algoritmos
from src.algorithms.route_calculator import RouteCalculator
from src.algorithms.donkey_optimization import DonkeyOptimizer

# Visualización
from src.presentation.visualizer import SpaceVisualizer

# GUI
from src.gui import GalaxiasGUI
```