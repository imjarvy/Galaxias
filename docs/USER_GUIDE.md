# Guía de Usuario - Galaxias

## Introducción

Bienvenido a Galaxias, un sistema interactivo que simula viajes espaciales entre estrellas de la Vía Láctea con tu compañero, el Burro Astronauta.

## Inicio Rápido

### 1. Instalación

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación

```bash
python main.py
```

## Usando la Interfaz Gráfica

### Panel de Planificación de Ruta

1. **Seleccionar Estrella Origen**: Elige la estrella desde donde comenzará el viaje
2. **Seleccionar Estrella Destino**: Elige tu destino final
3. **Calcular Ruta Óptima**: El sistema encontrará la mejor ruta
4. **Iniciar Viaje**: Comienza el viaje espacial

### Estado del Burro Astronauta

El panel muestra:
- **Salud**: Vida del burro (0-100)
- **Combustible**: Energía para viajar
- **Comida**: Provisiones
- **Oxígeno**: Aire respirable (0-100%)

### Gestión de Cometas

Los cometas pueden bloquear rutas espaciales:

1. **Agregar Cometa**:
   - Escribir nombre del cometa
   - Especificar ruta a bloquear (formato: `id_estrella1,id_estrella2`)
   - Hacer clic en "Agregar Cometa"

2. **Remover Cometa**:
   - Escribir nombre del cometa
   - Hacer clic en "Remover Cometa"

### Parámetros Científicos

Puedes ver y modificar:
- Constante gravitacional
- Velocidad de la luz
- Factor de curvatura (warp)
- Tasas de consumo de recursos

### Generar Reportes

El botón "Generar Reporte Visual" crea un informe completo con:
- Estadísticas del viaje
- Estado de recursos
- Historial de ubicaciones
- Indicadores de salud

## Modo Línea de Comandos

Para usuarios avanzados:

```bash
python main.py --cli
```

Sigue las instrucciones en pantalla:
1. Selecciona estrella de origen (número)
2. Selecciona estrella de destino (número)
3. Confirma el viaje
4. Genera visualizaciones

## Modo Demostración

Para ver todas las capacidades:

```bash
python main.py --demo
```

Esto ejecuta automáticamente:
- Cálculo de rutas
- Bloqueo con cometas
- Viaje completo
- Generación de reportes

## Consejos y Trucos

### Gestión de Recursos

- Mantén el combustible por encima de 200 para viajes largos
- La salud se pierde en rutas peligrosas
- Recarga recursos antes de viajes largos

### Optimización de Rutas

- Rutas con menor peligro consumen menos salud
- Considera el balance entre distancia y peligro
- Los cometas pueden forzar rutas más largas pero más seguras

### Estrategias de Viaje

1. **Explorador Cauteloso**: Prioriza rutas seguras
2. **Viajero Rápido**: Acepta más peligro por distancias cortas
3. **Planificador**: Calcula recursos antes de partir

## Solución de Problemas

### El Burro Astronauta No Puede Viajar

**Causa**: Recursos insuficientes
**Solución**: Haz clic en "Recargar Recursos"

### No Hay Ruta Disponible

**Causa**: Cometas bloqueando todos los caminos
**Solución**: Remueve algunos cometas

### La Aplicación No Inicia

**Causa**: Dependencias faltantes
**Solución**: Ejecuta `pip install -r requirements.txt`

## Preguntas Frecuentes

**P: ¿Qué pasa si el burro muere durante el viaje?**
R: El viaje se detiene en la última estrella alcanzada. Deberás reiniciar con recursos completos.

**P: ¿Puedo agregar mis propias estrellas?**
R: Sí, edita el archivo `data/constellations.json` siguiendo el formato existente.

**P: ¿Cómo cambio la dificultad?**
R: Modifica las tasas de consumo en `data/spaceship_config.json`.

**P: ¿Los datos estelares son reales?**
R: Las estrellas existen, pero las distancias y conexiones están simplificadas para el juego.

## Glosario

- **Año Luz**: Distancia que la luz viaja en un año
- **Gigante Roja**: Estrella en fase evolutiva avanzada
- **Secuencia Principal**: Estrella en su fase estable
- **Factor de Curvatura**: Velocidad de viaje supralumínica (warp)
- **Nivel de Peligro**: Riesgo de daño en una ruta (1-5)

## Contacto y Soporte

Para ayuda adicional:
- Revisa la documentación completa en `README.md`
- Reporta problemas en GitHub Issues
- Contribuye al proyecto con Pull Requests

---

¡Disfruta tu aventura espacial con el Burro Astronauta! 🫏🚀
