# Manual de Usuario: Galaxias

## Introducción
Galaxias es un simulador interactivo de rutas espaciales protagonizado por un burro astronauta. Permite planificar, visualizar y analizar viajes entre estrellas, gestionando recursos y enfrentando eventos dinámicos como cometas. Este manual te guiará en el uso de la aplicación, tanto en modo gráfico (GUI) como en modo consola (CLI) y demostración.

---

## Requisitos Previos
- Python 3.8 o superior
- Instalar dependencias:
  ```bash
  pip install matplotlib numpy networkx Pillow
  ```

---

## Instalación y Ejecución
1. Clona el repositorio:
   ```bash
   git clone https://github.com/imjarvy/Galaxias.git
   cd Galaxias
   ```
2. Instala las dependencias (ver arriba).
3. Ejecuta el sistema según el modo deseado:
   - **Interfaz gráfica (GUI):**
     ```bash
     python main.py
     ```
   - **Modo consola (CLI):**
     ```bash
     python main.py --cli
     ```
   - **Demostración automática:**
     ```bash
     python main.py --demo
     ```

---

## Uso de la Interfaz Gráfica (GUI)
Al ejecutar `python main.py` se abrirá la interfaz gráfica. Desde aquí puedes:
- Visualizar el mapa estelar y las constelaciones.
- Planificar rutas entre estrellas seleccionando origen y destino.
- Consultar el estado del burro astronauta (energía, pasto, salud, edad).
- Optimizar rutas para visitar el máximo de estrellas.
- Visualizar reportes y métricas del viaje.
- Editar parámetros científicos y de simulación desde el editor integrado.

### Paneles principales:
- **Panel de estado:** Muestra los recursos y salud del burro.
- **Panel de rutas:** Permite seleccionar estrellas y calcular rutas.
- **Panel de visualización:** Muestra el mapa y rutas resaltadas.
- **Panel de reportes:** Presenta métricas y resultados del viaje.

---

## Uso en Modo Consola (CLI)
Al ejecutar `python main.py --cli`:
1. Se mostrarán las estrellas disponibles y el estado inicial del burro.
2. Elige entre:
   - Calcular ruta directa entre dos estrellas.
   - Optimizar ruta para comer el máximo número de estrellas.
3. Ingresa los números de las estrellas según se solicite.
4. Se mostrarán los resultados, recursos necesarios y la ruta calculada.
5. Puedes generar una visualización del mapa resultante.

---

## Archivos de Configuración
- `data/constellations.json`: Define las estrellas, rutas y sus propiedades.
- `data/spaceship_config.json`: Configuración inicial del burro astronauta y parámetros globales.

Puedes editar estos archivos para personalizar el universo simulado.

---

## Consejos y Solución de Problemas
- Si la GUI no abre, verifica que tienes todas las dependencias instaladas y que usas Python 3.8+.
- Si modificas los archivos JSON, asegúrate de mantener el formato correcto.
- Los reportes y visualizaciones se guardan en la carpeta `assets/`.
- Consulta la documentación técnica en `docs/` para detalles avanzados.

---

