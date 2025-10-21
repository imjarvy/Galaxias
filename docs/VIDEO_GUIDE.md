# Video Descriptivo - Galaxias

## Guion para Video Demostrativo

### Introducción (0:00 - 0:30)

**Narración:**
"Bienvenidos a Galaxias, un sistema interactivo de simulación de rutas espaciales entre estrellas de constelaciones cercanas en la Vía Láctea. Acompañado por nuestro protagonista, el Burro Astronauta, exploraremos el cosmos calculando rutas óptimas y gestionando recursos vitales."

**Pantalla:**
- Logo de Galaxias con animación de estrellas
- Título: "Sistema Interactivo de Rutas Espaciales"
- Subtítulo: "🫏 Burro Astronauta 🚀"

### Demostración de Características (0:30 - 5:00)

#### 1. Visualización del Mapa Estelar (0:30 - 1:15)

**Narración:**
"El sistema incluye un mapa interactivo que muestra estrellas de cuatro constelaciones: Orión, Canis Major, Ursa Major y Lyra. Cada estrella está coloreada según su tipo estelar."

**Pantalla:**
- Mostrar mapa completo con todas las estrellas
- Zoom en diferentes constelaciones
- Resaltar diferentes tipos de estrellas:
  - Gigantes rojas (rojo)
  - Gigantes azules (azul)
  - Supergigantes azules (azul oscuro)
  - Secuencia principal (amarillo)

#### 2. Cálculo de Rutas Óptimas (1:15 - 2:30)

**Narración:**
"Usando el algoritmo de Dijkstra, el sistema calcula la ruta óptima entre cualquier par de estrellas, considerando distancia y nivel de peligro."

**Pantalla:**
- Abrir interfaz gráfica
- Seleccionar Betelgeuse como origen
- Seleccionar Sirius como destino
- Hacer clic en "Calcular Ruta Óptima"
- Mostrar ruta calculada resaltada en cyan
- Mostrar estadísticas: distancia, saltos, peligro, recursos necesarios

#### 3. Gestión del Burro Astronauta (2:30 - 3:15)

**Narración:**
"Nuestro Burro Astronauta tiene cuatro recursos vitales: salud, combustible, comida y oxígeno. Cada viaje consume recursos según la distancia y el peligro."

**Pantalla:**
- Mostrar panel de estado del burro
- Resaltar cada métrica:
  - Salud: 100/100
  - Combustible: 1000
  - Comida: 50
  - Oxígeno: 100
- Iniciar viaje
- Mostrar consumo de recursos en tiempo real
- Llegar al destino
- Mostrar estado final

#### 4. Sistema de Cometas (3:15 - 4:00)

**Narración:**
"Los cometas pueden bloquear rutas espaciales, forzando al sistema a calcular caminos alternativos."

**Pantalla:**
- Agregar cometa "Halley"
- Especificar ruta a bloquear
- Mostrar ruta bloqueada en rojo punteado
- Recalcular ruta al mismo destino
- Mostrar nueva ruta alternativa (más larga)
- Comparar estadísticas antes y después

#### 5. Parámetros Científicos (4:00 - 4:30)

**Narración:**
"El sistema incluye parámetros científicos configurables como la constante gravitacional, velocidad de la luz, y tasas de consumo de recursos."

**Pantalla:**
- Abrir ventana de parámetros científicos
- Mostrar parámetros físicos
- Mostrar tasas de consumo
- Mostrar factor de curvatura y eficiencia de escudos

#### 6. Reportes Visuales (4:30 - 5:00)

**Narración:**
"Al finalizar un viaje, el sistema genera reportes visuales completos con estadísticas, recursos consumidos y el estado del Burro Astronauta."

**Pantalla:**
- Generar reporte visual
- Mostrar las 4 secciones:
  1. Información de ruta
  2. Gráfico de recursos
  3. Historial de viaje
  4. Indicadores de estado

### Modos de Uso (5:00 - 6:00)

**Narración:**
"Galaxias ofrece tres modos de uso para diferentes necesidades."

**Pantalla:**

#### GUI Mode
- Mostrar interfaz completa
- Texto: `python main.py`

#### CLI Mode
- Mostrar terminal con interacción
- Texto: `python main.py --cli`

#### Demo Mode
- Mostrar ejecución automática
- Texto: `python main.py --demo`

### Tecnologías Utilizadas (6:00 - 6:30)

**Narración:**
"Galaxias está construido completamente en Python, utilizando bibliotecas robustas y ampliamente usadas."

**Pantalla:**
- Python 3.8+
- matplotlib - Visualizaciones
- numpy - Cálculos numéricos
- networkx - Algoritmos de grafos
- tkinter - Interfaz gráfica

### Instalación y Uso (6:30 - 7:00)

**Narración:**
"La instalación es simple y rápida. Solo necesitas Python y pip."

**Pantalla:**
```bash
# Clonar repositorio
git clone https://github.com/imjarvy/Galaxias.git

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

### Conclusión (7:00 - 7:30)

**Narración:**
"Galaxias combina algoritmos de grafos, visualización de datos y gestión de recursos en un sistema interactivo y educativo. Explora el cosmos con el Burro Astronauta y descubre rutas óptimas entre las estrellas de la Vía Láctea."

**Pantalla:**
- Montaje de imágenes del mapa estelar
- Logo final de Galaxias
- GitHub: github.com/imjarvy/Galaxias
- Texto: "¡Gracias por explorar Galaxias!"

## Notas de Producción

### Elementos Visuales Requeridos

1. **Capturas de pantalla:**
   - Mapa estelar completo
   - Interfaz GUI con todos los paneles
   - Ruta calculada resaltada
   - Panel de estado del burro
   - Ventana de parámetros científicos
   - Reporte visual completo

2. **Animaciones:**
   - Transición entre estrellas
   - Consumo de recursos (barras descendiendo)
   - Aparición de cometa bloqueando ruta
   - Recálculo de ruta

3. **Efectos de sonido (opcional):**
   - Sonido espacial de fondo
   - "Beep" al calcular ruta
   - Sonido de viaje al iniciar
   - Alerta al agregar cometa

### Configuración de Grabación

- **Resolución:** 1920x1080 (Full HD)
- **Frame rate:** 30 fps
- **Duración:** 7-8 minutos
- **Formato:** MP4 (H.264)

### Software Recomendado

- **Grabación de pantalla:** OBS Studio, Camtasia
- **Edición:** DaVinci Resolve, Adobe Premiere
- **Narración:** Audacity para audio

## Script de Demostración Automatizada

Para grabar el video, usa este script:

```bash
# 1. Iniciar con demo
python main.py --demo

# 2. Abrir GUI
python main.py

# 3. Seguir pasos del guion
# - Calcular ruta Betelgeuse -> Sirius
# - Iniciar viaje
# - Agregar cometa Halley
# - Recalcular ruta
# - Ver parámetros
# - Generar reporte
```

## Puntos Clave a Destacar

1. ✅ **Algoritmo de Dijkstra** para rutas óptimas
2. ✅ **Gestión de recursos** realista
3. ✅ **Sistema de bloqueo** con cometas
4. ✅ **Visualizaciones** profesionales con matplotlib
5. ✅ **Interfaz intuitiva** con tkinter
6. ✅ **Múltiples modos** de uso (GUI, CLI, Demo)
7. ✅ **Configuración flexible** con JSON
8. ✅ **Código abierto** y extensible

---

Este documento sirve como guía para crear un video descriptivo profesional del sistema Galaxias.
