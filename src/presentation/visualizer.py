"""
Visualization module for displaying the space map and routes.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_agg import FigureCanvasAgg
from typing import List, Optional, Dict, Set, Tuple
from ..core import Star, Route, SpaceMap, BurroAstronauta
import json
import hashlib


class SpaceVisualizer:
    """Visualize the space map, routes, and donkey journey."""
    
    def __init__(self, space_map: SpaceMap):
        self.space_map = space_map
        # Colores básicos para compatibilidad
        self.star_colors = {
            'normal': '#FFFF44',
            'hypergiant': '#FF00FF'
        }
        
        # Sistema avanzado de colores por constelación
        self.constellation_colors = self._generate_constellation_colors()
        self.shared_coordinates = self._find_shared_coordinates()
        
        # Color especial para estrellas compartidas
        self.shared_star_color = '#d62728'  # rojo intenso
    
    def _generate_constellation_color(self, name: str) -> str:
        """
        Genera un color único para una constelación basado en hash de su nombre.
        
        Args:
            name: Nombre de la constelación
            
        Returns:
            str: Color en formato hexadecimal (#RRGGBB)
        """
        # Normalizar nombre (minúsculas, sin espacios extra)
        normalized_name = name.lower().strip()
        
        # Crear hash del nombre
        hash_object = hashlib.md5(normalized_name.encode())
        hex_dig = hash_object.hexdigest()
        
        # Usar los primeros 6 caracteres como color, pero evitar colores reservados
        r = int(hex_dig[0:2], 16)
        g = int(hex_dig[2:4], 16) 
        b = int(hex_dig[4:6], 16)
        
        # Evitar colores muy oscuros (aumentar brillo mínimo)
        if r < 80: r += 80
        if g < 80: g += 80
        if b < 80: b += 80
        
        # Evitar colores muy parecidos a los reservados
        # Hipergigante: #FF00FF (magenta)
        # Compartida: #d62728 (rojo intenso)
        # Normal: #FFFF44 (amarillo)
        
        # Si es muy parecido al magenta hipergigante, ajustar
        if r > 200 and b > 200 and g < 100:
            g += 100  # Agregar verde
        
        # Si es muy parecido al rojo compartido, ajustar
        if r > 180 and g < 80 and b < 80:
            b += 100  # Agregar azul
        
        # Si es muy parecido al amarillo normal, ajustar
        if r > 200 and g > 200 and b < 100:
            r -= 50  # Reducir rojo
        
        # Limitar valores a rango válido
        r = min(255, max(0, r))
        g = min(255, max(0, g))
        b = min(255, max(0, b))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _generate_constellation_colors(self) -> Dict[str, str]:
        """
        Genera mapa de colores para todas las constelaciones en el JSON.
        
        Returns:
            Dict[str, str]: Mapeo de nombre_constelación -> color_hex
        """
        try:
            with open('data/constellations.json', 'r') as f:
                data = json.load(f)
            
            color_mapping = {}
            
            for constellation in data.get('constellations', []):
                name = constellation['name']
                color = self._generate_constellation_color(name)
                color_mapping[name] = color
            
            return color_mapping
        except Exception as e:
            print(f"Error generando colores de constelación: {e}")
            return {}
    
    def _find_shared_coordinates(self) -> Set[Tuple[float, float]]:
        """
        Identifica coordenadas que tienen múltiples estrellas (estrellas compartidas).
        
        Returns:
            Set[Tuple[float, float]]: Conjunto de coordenadas con estrellas compartidas
        """
        try:
            with open('data/constellations.json', 'r') as f:
                data = json.load(f)
            
            coordinate_counts = {}
            
            # Contar cuántas estrellas hay en cada coordenada
            for constellation in data.get('constellations', []):
                for star in constellation.get('starts', []):
                    x = star['coordenates']['x']
                    y = star['coordenates']['y']
                    coord = (x, y)
                    
                    coordinate_counts[coord] = coordinate_counts.get(coord, 0) + 1
            
            # Retornar coordenadas con más de una estrella
            return {coord for coord, count in coordinate_counts.items() if count > 1}
        except Exception as e:
            print(f"Error encontrando coordenadas compartidas: {e}")
            return set()
    
    def _get_star_constellation(self, star: Star) -> Optional[str]:
        """
        Obtiene el nombre de la constelación a la que pertenece una estrella.
        
        Args:
            star: La estrella a buscar
            
        Returns:
            Optional[str]: Nombre de la constelación o None si no se encuentra
        """
        try:
            with open('data/constellations.json', 'r') as f:
                data = json.load(f)
            
            for constellation in data.get('constellations', []):
                for star_data in constellation.get('starts', []):
                    if str(star_data['id']) == str(star.id):
                        return constellation['name']
            
            return None
        except Exception as e:
            print(f"Error obteniendo constelación de estrella {star.id}: {e}")
            return None
    
    def _determine_star_color(self, star: Star) -> str:
        """
        Determina el color de una estrella según las reglas de prioridad:
        1. Hipergigante: #FF00FF (máxima prioridad)
        2. Compartida: #d62728 (segunda prioridad)
        3. Constelación: color generado automáticamente (tercera prioridad)
        4. Default: #FFFF44 (última prioridad)
        
        Args:
            star: La estrella para la cual determinar el color
            
        Returns:
            str: Color en formato hexadecimal
        """
        # Prioridad 1: Hipergigante
        if star.hypergiant:
            return self.star_colors['hypergiant']
        
        # Prioridad 2: Estrella compartida (por coordenadas)
        star_coord = (star.x, star.y)
        if star_coord in self.shared_coordinates:
            return self.shared_star_color
        
        # Prioridad 3: Color de constelación
        constellation_name = self._get_star_constellation(star)
        if constellation_name and constellation_name in self.constellation_colors:
            return self.constellation_colors[constellation_name]
        
        # Prioridad 4: Default (normal)
        return self.star_colors['normal']
    
    def plot_space_map(self, 
                       highlight_path: Optional[List[Star]] = None,
                       donkey_location: Optional[Star] = None,
                       save_path: Optional[str] = None,
                       show: bool = True) -> plt.Figure:
        """
        Plot the entire space map with stars and routes.
        
        Args:
            highlight_path: Optional path to highlight
            donkey_location: Current location of the donkey
            save_path: If provided, save the figure to this path
            show: Whether to display the plot
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Configurar límites mínimos del tablero para cumplir requisitos de 200x200
        stars = self.space_map.get_all_stars_list()
        if stars:
            x_coords = [star.x for star in stars]
            y_coords = [star.y for star in stars]
            
            # Calcular rangos actuales
            min_x, max_x = min(x_coords), max(x_coords)
            min_y, max_y = min(y_coords), max(y_coords)
            range_x = max_x - min_x
            range_y = max_y - min_y
            
            # Asegurar mínimo 200x200 unidades centrado en las estrellas
            center_x = (min_x + max_x) / 2
            center_y = (min_y + max_y) / 2
            
            # Calcular límites finales
            final_width = max(200, range_x * 1.2)  # Al menos 200, o 20% más que el rango
            final_height = max(200, range_y * 1.2)
            
            half_width = final_width / 2
            half_height = final_height / 2
            
            # Establecer límites del tablero
            ax.set_xlim(center_x - half_width, center_x + half_width)
            ax.set_ylim(center_y - half_height, center_y + half_height)
        
        # Plot routes first (so they appear behind stars)
        blocked_routes = set()
        # Collect blocked routes from comets
        for comet in self.space_map.comets:
            for from_id, to_id in comet.blocked_routes:
                blocked_routes.add((from_id, to_id))
                blocked_routes.add((to_id, from_id))  # Bidirectional blocking
        
        for route in self.space_map.routes:
            x1, y1 = route.from_star.x, route.from_star.y
            x2, y2 = route.to_star.x, route.to_star.y
            
            # Check if route is blocked by comets
            route_key = (route.from_star.id, route.to_star.id)
            route_key_reverse = (route.to_star.id, route.from_star.id)
            is_blocked_by_comet = route_key in blocked_routes or route_key_reverse in blocked_routes
            
            if route.blocked or is_blocked_by_comet:
                # Blocked routes in red dashed with thicker lines for comet blocks
                line_style = 'r--'
                line_width = 3 if is_blocked_by_comet else 1
                alpha = 0.7 if is_blocked_by_comet else 0.3
                ax.plot([x1, x2], [y1, y2], line_style, alpha=alpha, linewidth=line_width)
            else:
                # Normal routes - color by danger level
                if route.danger_level <= 1:
                    color = 'green'
                elif route.danger_level <= 2:
                    color = 'yellow'
                elif route.danger_level <= 3:
                    color = 'orange'
                else:
                    color = 'red'
                
                alpha = 0.3 + (route.danger_level * 0.1)
                ax.plot([x1, x2], [y1, y2], color, alpha=alpha, linewidth=1)
        
        # Highlight path if provided
        if highlight_path and len(highlight_path) > 1:
            for i in range(len(highlight_path) - 1):
                x1, y1 = highlight_path[i].x, highlight_path[i].y
                x2, y2 = highlight_path[i+1].x, highlight_path[i+1].y
                ax.plot([x1, x2], [y1, y2], 'cyan', linewidth=3, alpha=0.8)
                # Add arrow
                dx, dy = x2 - x1, y2 - y1
                if abs(dx) > 1 or abs(dy) > 1:  # Only add arrow if significant distance
                    ax.arrow(x1, y1, dx*0.8, dy*0.8, 
                            head_width=8, head_length=6, 
                            fc='cyan', ec='cyan', alpha=0.6)
        
        # Plot stars
        for star in self.space_map.get_all_stars_list():
            # Usar el nuevo sistema de colores
            color = self._determine_star_color(star)
            size = max(100, star.radius * 300)  # Size based on radius
            
            # Highlight if in path
            if highlight_path and star in highlight_path:
                size *= 1.5
                ax.scatter(star.x, star.y, s=size, c=color, 
                          edgecolors='cyan', linewidth=3, zorder=5)
            else:
                ax.scatter(star.x, star.y, s=size, c=color, 
                          edgecolors='white', linewidth=1, zorder=5)
            
            # Add star label
            ax.annotate(f"{star.label}\nE:{star.amount_of_energy}", 
                       (star.x, star.y), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, color='white',
                       bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor='black', alpha=0.7))
        
        # Plot donkey location if provided
        if donkey_location:
            ax.scatter(donkey_location.x, donkey_location.y, 
                      s=400, marker='*', c='gold', 
                      edgecolors='orange', linewidth=2, zorder=10)
            ax.annotate('Burro Astronauta', 
                       (donkey_location.x, donkey_location.y),
                       xytext=(10, -20), textcoords='offset points',
                       fontsize=10, color='gold', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', 
                                facecolor='darkblue', alpha=0.8))
        
        # Plot comets and their blocked routes
        for i, comet in enumerate(self.space_map.comets):
            for from_id, to_id in comet.blocked_routes:
                from_star = self.space_map.get_star(from_id)
                to_star = self.space_map.get_star(to_id)
                
                if from_star and to_star:
                    # Calculate midpoint for comet position
                    mid_x = (from_star.x + to_star.x) / 2
                    mid_y = (from_star.y + to_star.y) / 2
                    
                    # Add small offset for multiple comets on same route
                    offset = i * 5
                    mid_x += offset
                    mid_y += offset
                    
                    # Draw comet as a special symbol
                    ax.scatter(mid_x, mid_y, s=300, marker='o', 
                             c='darkred', edgecolors='red', linewidth=2, zorder=8,
                             alpha=0.8)
                    
                    # Add comet label
                    ax.annotate(f"☄️ {comet.name}", 
                               (mid_x, mid_y),
                               xytext=(10, 10), textcoords='offset points',
                               fontsize=8, color='red', fontweight='bold',
                               bbox=dict(boxstyle='round,pad=0.3', 
                                        facecolor='black', alpha=0.8))
        
        # Create legend - Dinámico basado en constelaciones presentes
        legend_elements = []
        
        # Agregar colores por constelación
        for constellation_name, color in self.constellation_colors.items():
            legend_elements.append(mpatches.Patch(color=color, label=f'🌌 {constellation_name}'))
        
        # Separador visual
        if self.constellation_colors:
            legend_elements.append(mpatches.Patch(color='none', label='────────────'))
        
        # Colores especiales
        legend_elements.extend([
            mpatches.Patch(color='#FF00FF', label='⭐ Hipergigante'),
        ])
        
        # Solo agregar estrella compartida si existen coordenadas compartidas
        if self.shared_coordinates:
            legend_elements.append(mpatches.Patch(color='#d62728', label='🔗 Estrella Compartida'))
        
        # Colores de rutas
        legend_elements.extend([
            mpatches.Patch(color='none', label='────────────'),
            plt.Line2D([0], [0], color='green', label='🛣️ Ruta Segura (Peligro 1)'),
            plt.Line2D([0], [0], color='yellow', label='🛣️ Ruta Moderada (Peligro 2)'),
            plt.Line2D([0], [0], color='orange', label='🛣️ Ruta Peligrosa (Peligro 3)'),
            plt.Line2D([0], [0], color='red', label='🛣️ Ruta Extrema (Peligro 4+)'),
            plt.Line2D([0], [0], color='red', linestyle='--', linewidth=3, 
                      label='🚫 Ruta Bloqueada por Cometa'),
        ])
        
        # Add comet information if any comets exist
        if self.space_map.comets:
            legend_elements.extend([
                mpatches.Patch(color='none', label='────────────'),
                mpatches.Patch(color='darkred', label='☄️ Cometas Activos'),
            ])
            for comet in self.space_map.comets:
                blocked_count = len(comet.blocked_routes)
                legend_elements.append(
                    mpatches.Patch(color='red', alpha=0.6, 
                                 label=f"  • {comet.name} ({blocked_count} rutas)")
                )
        
        ax.legend(handles=legend_elements, loc='upper right', 
                 facecolor='black', edgecolor='white', 
                 labelcolor='white', framealpha=0.8)
        
        ax.set_facecolor('black')
        fig.patch.set_facecolor('#000033')
        ax.set_title('Galaxias - Mapa de Constelaciones', 
                    color='white', fontsize=16, fontweight='bold')
        ax.set_xlabel('Coordenada X', color='white')
        ax.set_ylabel('Coordenada Y', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, facecolor=fig.get_facecolor(), dpi=150)
        
        if show:
            plt.show()
        
        return fig
    
    def plot_resource_status(self, 
                            burro: BurroAstronauta,
                            save_path: Optional[str] = None,
                            show: bool = True) -> plt.Figure:
        """Plot the current resource status of the burro astronauta."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        resources = ['Energía', 'Pasto (kg)', 'Edad']
        values = [burro.current_energy, burro.current_pasto/10, burro.start_age*2]  # Scale for visibility
        colors = ['#FF4444', '#44FF44', '#4444FF']
        
        bars = ax.barh(resources, values, color=colors, edgecolor='white', linewidth=2)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            if i == 0:  # Energy
                actual_value = value
                unit = '%'
            elif i == 1:  # Grass
                actual_value = value * 10
                unit = 'kg'
            else:  # Age
                actual_value = value // 2
                unit = 'años'
            
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                   f'{actual_value:.0f}{unit}',
                   va='center', color='white', fontweight='bold')
        
        ax.set_facecolor('#000033')
        fig.patch.set_facecolor('#000066')
        ax.set_title(f'Estado del Burro Astronauta: {burro.name}',
                    color='white', fontsize=14, fontweight='bold')
        ax.set_xlabel('Cantidad', color='white')
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, facecolor=fig.get_facecolor(), dpi=150)
        
        if show:
            plt.show()
        
        return fig
    
    def plot_journey_report(self,
                           burro: BurroAstronauta,
                           path_stats: Dict,
                           save_path: Optional[str] = None,
                           show: bool = True) -> plt.Figure:
        """Generate a comprehensive journey report."""
        fig = plt.figure(figsize=(14, 8))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Top left: Path information
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.axis('off')
        
        info_text = f"""
        REPORTE DE VIAJE ESPACIAL
        {'='*40}

        Ruta Recorrida:
        {' → '.join(path_stats.get('path_stars', ['N/A']))}

        Estadísticas del Viaje:
        - Saltos Totales: {path_stats.get('num_jumps', 0)}
        - Distancia Total: {path_stats.get('total_distance', 0):.2f} unidades
        - Nivel de Peligro: {path_stats.get('total_danger', 0)}

        Recursos:
        - Energía Necesaria: {path_stats.get('total_energy_needed', 0):.2f}
        - Pasto Necesario: {path_stats.get('total_grass_needed', 0):.2f} kg
        - Energía Ganada: {path_stats.get('total_energy_gained', 0):.2f}
        - Balance Neto: {path_stats.get('net_energy', 0):.2f}
                """
        
        ax1.text(0.05, 0.95, info_text, transform=ax1.transAxes,
                fontsize=10, verticalalignment='top',
                fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#000066', alpha=0.8))
        
        # Top right: Current resources bar chart
        ax2 = fig.add_subplot(gs[0, 1])
        resources = ['Energía', 'Pasto\n(×10)', 'Edad']
        values = [burro.current_energy, burro.current_pasto/10, burro.start_age*2]
        colors = ['#FF4444', '#44FF44', '#4444FF']
        
        bars = ax2.bar(resources, values, color=colors, edgecolor='white', linewidth=2)
        
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar.get_height()
            if i == 0:  # Energy
                display_value = f'{value:.0f}%'
            elif i == 1:  # Grass
                display_value = f'{value*10:.0f}kg'
            else:  # Age
                display_value = f'{value//2:.0f}años'
            
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    display_value,
                    ha='center', va='bottom', color='white', fontweight='bold')
        
        ax2.set_facecolor('#000033')
        ax2.set_title('Recursos Actuales', color='white', fontweight='bold')
        ax2.set_ylabel('Cantidad', color='white')
        ax2.tick_params(colors='white')
        ax2.spines['bottom'].set_color('white')
        ax2.spines['top'].set_color('white')
        ax2.spines['left'].set_color('white')
        ax2.spines['right'].set_color('white')
        
        # Bottom left: Journey history
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.axis('off')
        
        history_text = "HISTORIAL DE VIAJE\n" + "="*40 + "\n\n"
        if burro.journey_history:
            for i, star in enumerate(burro.journey_history, 1):
                star_type = "⭐" if star.hypergiant else "✨"
                history_text += f"{i}. {star_type} {star.label}\n"
                history_text += f"   Energía: {star.amount_of_energy}, Radio: {star.radius:.1f}\n"
        else:
            history_text += "Sin historial de viaje aún."
        
        ax3.text(0.05, 0.95, history_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top',
                fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#000066', alpha=0.8))
        
        # Bottom right: Status indicators
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        
        # Status indicators
        energy_status = "EXCELENTE" if burro.current_energy > 75 else "BUENO" if burro.current_energy > 50 else "BAJO"
        grass_status = "SUFICIENTE" if burro.current_pasto > 100 else "ADVERTENCIA" if burro.current_pasto > 50 else "CRÍTICO"
        health_status = burro.estado_salud.upper()
        
        status_text = f"""
        ESTADO DEL BURRO ASTRONAUTA
        {'='*40}

        Estado General: {health_status}
        Energía: {burro.current_energy}% [{energy_status}]
        Pasto: {burro.current_pasto}kg [{grass_status}]
        Edad: {burro.start_age} años

        Capacidades:
        - Puede viajar: {'SÍ' if burro.current_energy > 10 else 'NO'}
        - Puede comer: {'SÍ' if burro.current_pasto > 5 else 'NO'}
        - Estado vital: {'VIVO' if burro.is_alive() else 'MUERTO'}

        Ubicación Actual:
        {burro.current_location.label if burro.current_location else 'Desconocida'}
                """
        
        ax4.text(0.05, 0.95, status_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='top',
                fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#000066', alpha=0.8))
        
        fig.patch.set_facecolor('#000033')
        fig.suptitle('Galaxias - Reporte de Viaje del Burro Astronauta',
                    color='white', fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, facecolor=fig.get_facecolor(), dpi=150)
        
        if show:
            plt.show()
        
        return fig
