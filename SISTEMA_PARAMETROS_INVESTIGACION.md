# 🔬 Sistema de Parámetros de Investigación - Documentación Completa

## 📋 Resumen de Funcionalidades

El sistema de parámetros de investigación permite personalizar los valores de ganancia/pérdida de tiempo de vida y energía por investigación para cada estrella antes de iniciar el recorrido.

### ✅ Características Implementadas

#### 1. **Editor Modular de Parámetros**
- **Ubicación**: `src/parameter_editor_simple/`
- **Estructura organizada**:
  - `models.py`: Definición de `ResearchParameters`
  - `editor.py`: Interfaz principal del editor
  - `presets.py`: Configuraciones predefinidas
  - `star_config.py`: Configuración específica por estrella
  - `preview.py`: Vista previa de cambios

#### 2. **Parámetros Configurables**

##### Parámetros Globales:
- **Consumo de Energía**: % de energía por unidad de tiempo (defecto: 2.0%)
- **Tiempo de Investigación**: % del tiempo dedicado a investigación (defecto: 50%)
- **Bonus Tiempo de Vida**: Años adicionales ganados por estrella (defecto: 0.0)
- **Bonus Energía**: % de energía adicional por estrella (defecto: 0.0%)

##### Configuración Específica por Estrella:
- **Tasa de Energía Personalizada**: Consumo específico para cada estrella
- **Bonus de Tiempo**: Años de vida ganados/perdidos específicos
- **Bonus de Energía**: % de energía específico por estrella

#### 3. **Integración con GUI**

##### Botón Inteligente:
```
⚙️ Configurar Parámetros    → Estado inicial (naranja)
✅ Parámetros Configurados  → Con configuraciones activas (verde)
```

##### Flujo de Trabajo:
1. **Abrir Editor**: Clic en "⚙️ Configurar Parámetros"
2. **Configurar**: Ajustar parámetros globales y específicos por estrella
3. **Confirmar**: Aplicar cambios y cerrar editor
4. **Recalcular**: Opción automática de recálculo de rutas
5. **Visualizar**: Actualización automática de resultados

#### 4. **Recálculo Automático**

Cuando se confirman nuevos parámetros, el sistema ofrece:
- **Ruta de Menor Gasto**: Recálculo con nuevos parámetros
- **Ruta de Máximas Visitas**: Recálculo optimizado
- **Optimización para Comer Estrellas**: Estrategia actualizada
- **Visualización Actualizada**: Gráficos con nuevos resultados

#### 5. **Configuraciones Predefinidas (Presets)**

- **Investigador Intensivo**: Alta investigación, alto consumo energético
- **Conservador de Energía**: Baja investigación, bajo consumo
- **Equilibrado**: Balance entre investigación y eficiencia energética

## 🚀 Cómo Usar el Sistema

### Paso 1: Acceder al Editor
1. Abrir la GUI principal: `python src/gui.py`
2. Hacer clic en "⚙️ Configurar Parámetros"

### Paso 2: Configurar Parámetros Globales
```
• Consumo Energía: Ajustar entre 0.1% - 5.0%
• Tiempo Investigación: Ajustar entre 10% - 100%
• Bonus Tiempo Vida: Ajustar entre -2.0 a +5.0 años
• Bonus Energía: Ajustar entre -10.0% a +20.0%
```

### Paso 3: Configurar Estrellas Específicas
1. Seleccionar estrella de la lista desplegable
2. Habilitar configuración personalizada
3. Ajustar valores específicos para esa estrella
4. Repetir para otras estrellas según necesidad

### Paso 4: Previsualizar y Aplicar
1. Ver vista previa de todos los cambios
2. Usar presets si es necesario
3. Hacer clic en "Aplicar Configuración"
4. Elegir si recalcular rutas automáticamente

## 📊 Ejemplos de Configuración

### Ejemplo 1: Exploradores Agresivos
```python
ResearchParameters(
    energy_consumption_rate=1.0,    # Consumo bajo
    time_percentage=0.8,            # 80% investigación
    life_time_bonus=1.0,           # +1 año por estrella
    energy_bonus_per_star=5.0      # +5% energía por estrella
)
```

### Ejemplo 2: Estrellas Especializadas
```python
custom_star_settings = {
    "13": {  # Gama23 (Hipergigante)
        "energy_rate": 0.5,      # Muy eficiente
        "time_bonus": 2.0,       # +2 años de vida
        "energy_bonus": 15.0     # +15% energía
    },
    "3": {   # Alpha53 (Hipergigante)
        "energy_rate": 0.3,      # Super eficiente
        "time_bonus": 1.5,       # +1.5 años
        "energy_bonus": 12.0     # +12% energía
    }
}
```

## 🔧 Archivos Modificados

### Archivos Principales:
- `src/gui.py` - Integración con interfaz principal
- `src/parameter_editor_simple/` - Módulo completo del editor

### Scripts de Demostración:
- `demo_complete_parameter_system.py` - Demostración completa
- `test_parameter_editor.py` - Pruebas del editor
- `demo_configurable_parameters.py` - Demo existente actualizada

## 🎯 Resultados y Beneficios

### Antes de la Implementación:
- Parámetros fijos e inmutables
- Sin personalización por estrella
- Cálculos estáticos únicos

### Después de la Implementación:
- **Flexibilidad Total**: Ajuste de todos los parámetros de investigación
- **Configuración Específica**: Valores únicos para cada estrella
- **Recálculo Dinámico**: Actualización automática de rutas
- **Interfaz Intuitiva**: Editor gráfico fácil de usar
- **Presets Útiles**: Configuraciones predefinidas para casos comunes

### Casos de Uso Resueltos:
1. **Estrellas Hipergigantes**: Configuración especial para estrellas de alta energía
2. **Rutas Eficientes**: Optimización específica según objetivos
3. **Experimentación**: Prueba rápida de diferentes estrategias
4. **Análisis Comparativo**: Evaluación de diferentes configuraciones

## 📈 Impacto en el Sistema

### Mejoras de Rendimiento:
- Rutas más optimizadas según preferencias del usuario
- Mayor flexibilidad en estrategias de exploración
- Personalización completa de parámetros de investigación

### Mejoras de Usabilidad:
- Interfaz gráfica intuitiva
- Configuraciones guardadas automáticamente
- Vista previa de cambios antes de aplicar
- Recálculo automático opcional

### Arquitectura del Código:
- Módulos organizados y mantenibles
- Separación clara de responsabilidades
- Fácil extensión para nuevos parámetros
- Integración limpia con el sistema existente

## 🏁 Conclusión

El sistema de parámetros de investigación representa una mejora significativa en la funcionalidad del simulador Galaxias, proporcionando:

✅ **Personalización Completa** de parámetros de investigación  
✅ **Interfaz Intuitiva** para configuración avanzada  
✅ **Recálculo Automático** de rutas optimizadas  
✅ **Configuración por Estrella** para máxima flexibilidad  
✅ **Integración Perfecta** con el sistema existente  

La implementación permite a los usuarios experimentar con diferentes estrategias de exploración, optimizar rutas según objetivos específicos, y obtener resultados más precisos y personalizados para sus misiones espaciales.

---
*Desarrollado como parte del proyecto Galaxias - Sistema de Rutas del Burro Astronauta*