"""
Visualization module for displaying the space map and routes.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_agg import FigureCanvasAgg
from typing import List, Optional, Dict
from src.models import Star, Route, SpaceMap, BurroAstronauta
import json


class SpaceVisualizer:
    """Visualize the space map, routes, and donkey journey."""
    
    def __init__(self, space_map: SpaceMap):
        self.space_map = space_map
        self.star_colors = {
            'normal': '#FFFF44',
            'hypergiant': '#FF00FF'
        }
    
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
        
        # Plot routes first (so they appear behind stars)
        for route in self.space_map.routes:
            x1, y1 = route.from_star.x, route.from_star.y
            x2, y2 = route.to_star.x, route.to_star.y
            
            if route.blocked:
                # Blocked routes in red dashed
                ax.plot([x1, x2], [y1, y2], 'r--', alpha=0.3, linewidth=1)
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
            color = self.star_colors['hypergiant'] if star.hypergiant else self.star_colors['normal']
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
        
        # Create legend
        legend_elements = [
            mpatches.Patch(color='#FFFF44', label='Estrella Normal'),
            mpatches.Patch(color='#FF00FF', label='Hipergigante'),
            plt.Line2D([0], [0], color='green', label='Ruta Segura (Peligro 1)'),
            plt.Line2D([0], [0], color='yellow', label='Ruta Moderada (Peligro 2)'),
            plt.Line2D([0], [0], color='orange', label='Ruta Peligrosa (Peligro 3)'),
            plt.Line2D([0], [0], color='red', label='Ruta Extrema (Peligro 4+)'),
        ]
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
