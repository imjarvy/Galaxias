"""
Visualization module for displaying the space map and routes.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_agg import FigureCanvasAgg
from typing import List, Optional, Dict
from src.models import Star, Route, SpaceMap, SpaceshipDonkey
import json


class SpaceVisualizer:
    """Visualize the space map, routes, and spaceship journey."""
    
    def __init__(self, space_map: SpaceMap):
        self.space_map = space_map
        self.star_colors = {
            'red_giant': '#FF4444',
            'blue_giant': '#4444FF',
            'blue_supergiant': '#2222CC',
            'main_sequence': '#FFFF44',
            'giant': '#FF8844'
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
            donkey_location: Current location of the donkey spaceship
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
                # Normal routes
                alpha = 0.3 + (route.danger_level * 0.1)
                ax.plot([x1, x2], [y1, y2], 'gray', alpha=alpha, linewidth=1)
        
        # Highlight path if provided
        if highlight_path and len(highlight_path) > 1:
            for i in range(len(highlight_path) - 1):
                x1, y1 = highlight_path[i].x, highlight_path[i].y
                x2, y2 = highlight_path[i+1].x, highlight_path[i+1].y
                ax.plot([x1, x2], [y1, y2], 'cyan', linewidth=3, alpha=0.8)
                # Add arrow
                dx, dy = x2 - x1, y2 - y1
                ax.arrow(x1, y1, dx*0.8, dy*0.8, 
                        head_width=15, head_length=10, 
                        fc='cyan', ec='cyan', alpha=0.6)
        
        # Plot stars
        for star in self.space_map.get_all_stars_list():
            color = self.star_colors.get(star.type, '#FFFFFF')
            size = 200
            
            # Highlight if in path
            if highlight_path and star in highlight_path:
                size = 300
                ax.scatter(star.x, star.y, s=size, c=color, 
                          edgecolors='cyan', linewidth=3, zorder=5)
            else:
                ax.scatter(star.x, star.y, s=size, c=color, 
                          edgecolors='white', linewidth=1, zorder=5)
            
            # Add star name
            ax.annotate(star.name, (star.x, star.y), 
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=8, color='white',
                       bbox=dict(boxstyle='round,pad=0.3', 
                                facecolor='black', alpha=0.7))
        
        # Plot donkey location if provided
        if donkey_location:
            ax.scatter(donkey_location.x, donkey_location.y, 
                      s=400, marker='*', c='gold', 
                      edgecolors='orange', linewidth=2, zorder=10)
            ax.annotate('🫏 Burro Astronauta', 
                       (donkey_location.x, donkey_location.y),
                       xytext=(10, -20), textcoords='offset points',
                       fontsize=10, color='gold', fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.5', 
                                facecolor='darkblue', alpha=0.8))
        
        # Create legend
        legend_elements = [
            mpatches.Patch(color='#FF4444', label='Red Giant'),
            mpatches.Patch(color='#4444FF', label='Blue Giant'),
            mpatches.Patch(color='#2222CC', label='Blue Supergiant'),
            mpatches.Patch(color='#FFFF44', label='Main Sequence'),
            mpatches.Patch(color='#FF8844', label='Giant'),
        ]
        ax.legend(handles=legend_elements, loc='upper right', 
                 facecolor='black', edgecolor='white', 
                 labelcolor='white', framealpha=0.8)
        
        ax.set_facecolor('black')
        fig.patch.set_facecolor('#000033')
        ax.set_title('Galaxias - Mapa Estelar de la Vía Láctea', 
                    color='white', fontsize=16, fontweight='bold')
        ax.set_xlabel('Coordenada X (años luz)', color='white')
        ax.set_ylabel('Coordenada Y (años luz)', color='white')
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2, color='white')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, facecolor=fig.get_facecolor(), dpi=150)
        
        if show:
            plt.show()
        
        return fig
    
    def plot_resource_status(self, 
                            donkey: SpaceshipDonkey,
                            save_path: Optional[str] = None,
                            show: bool = True) -> plt.Figure:
        """Plot the current resource status of the spaceship donkey."""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        resources = ['Salud', 'Combustible', 'Comida', 'Oxígeno']
        values = [donkey.health, donkey.fuel/10, donkey.food, donkey.oxygen]
        colors = ['#FF4444', '#44FF44', '#FFAA44', '#4444FF']
        
        bars = ax.barh(resources, values, color=colors, edgecolor='white', linewidth=2)
        
        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            if i == 0:  # Health
                actual_value = value
            elif i == 1:  # Fuel
                actual_value = value * 10
            else:
                actual_value = value
            
            ax.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
                   f'{actual_value:.1f}',
                   va='center', color='white', fontweight='bold')
        
        ax.set_facecolor('#000033')
        fig.patch.set_facecolor('#000066')
        ax.set_title(f'Estado del Burro Astronauta: {donkey.name}',
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
                           donkey: SpaceshipDonkey,
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

Recursos Consumidos:
- Combustible: {path_stats.get('total_fuel_needed', 0):.2f}
- Comida: {path_stats.get('total_food_needed', 0):.2f}
- Oxígeno: {path_stats.get('total_oxygen_needed', 0):.2f}
- Pérdida de Salud: {path_stats.get('estimated_health_loss', 0):.2f}
        """
        
        ax1.text(0.05, 0.95, info_text, transform=ax1.transAxes,
                fontsize=10, verticalalignment='top',
                fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#000066', alpha=0.8))
        
        # Top right: Current resources bar chart
        ax2 = fig.add_subplot(gs[0, 1])
        resources = ['Salud', 'Combustible\n(×10)', 'Comida', 'Oxígeno']
        values = [donkey.health, donkey.fuel/10, donkey.food, donkey.oxygen]
        colors = ['#FF4444', '#44FF44', '#FFAA44', '#4444FF']
        
        bars = ax2.bar(resources, values, color=colors, edgecolor='white', linewidth=2)
        
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.1f}',
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
        if donkey.journey_history:
            for i, star in enumerate(donkey.journey_history, 1):
                history_text += f"{i}. {star.name} ({star.type})\n"
        else:
            history_text += "Sin historial de viaje aún."
        
        ax3.text(0.05, 0.95, history_text, transform=ax3.transAxes,
                fontsize=9, verticalalignment='top',
                fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#000066', alpha=0.8))
        
        # Bottom right: Status indicators
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis('off')
        
        status = "✅ Vivo" if donkey.is_alive() else "❌ Muerto"
        fuel_status = "✅" if donkey.fuel > 100 else "⚠️" if donkey.fuel > 50 else "❌"
        health_status = "✅" if donkey.health > 70 else "⚠️" if donkey.health > 30 else "❌"
        
        status_text = f"""
ESTADO DEL BURRO ASTRONAUTA
{'='*40}

Estado General: {status}

Indicadores:
{health_status} Salud: {donkey.health:.1f}%
{fuel_status} Combustible: {donkey.fuel:.1f}
{'✅' if donkey.oxygen > 50 else '⚠️'} Oxígeno: {donkey.oxygen:.1f}%
{'✅' if donkey.food > 20 else '⚠️'} Comida: {donkey.food:.1f}

Ubicación Actual:
{donkey.current_location.name if donkey.current_location else 'En tránsito'}
        """
        
        ax4.text(0.05, 0.95, status_text, transform=ax4.transAxes,
                fontsize=10, verticalalignment='top',
                fontfamily='monospace', color='white',
                bbox=dict(boxstyle='round', facecolor='#000066', alpha=0.8))
        
        fig.patch.set_facecolor('#000033')
        fig.suptitle('🫏 Galaxias - Reporte de Viaje Espacial 🚀',
                    color='white', fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, facecolor=fig.get_facecolor(), dpi=150)
        
        if show:
            plt.show()
        
        return fig
