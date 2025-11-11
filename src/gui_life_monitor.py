"""
Sistema de alertas GUI para el monitoreo de vida del Burro Astronauta.

Implementa alertas visuales y sonoras integradas con tkinter para 
mostrar información sobre el tiempo de vida restante.
"""
import tkinter as tk
from tkinter import messagebox
import threading
from typing import Optional
from src.life_monitor import IAlertSystem, ISoundManager, LifeEvent, ILifeObserver


class TkinterAlertSystem(IAlertSystem):
    """Sistema de alertas usando tkinter messagebox."""
    
    def __init__(self, parent_window: Optional[tk.Tk] = None):
        """
        Inicializa el sistema de alertas.
        
        Args:
            parent_window: Ventana padre de tkinter (opcional)
        """
        self.parent = parent_window
    
    def show_warning(self, title: str, message: str):
        """Muestra una advertencia usando messagebox."""
        messagebox.showwarning(title, message, parent=self.parent)
    
    def show_error(self, title: str, message: str):
        """Muestra un error usando messagebox.""" 
        messagebox.showerror(title, message, parent=self.parent)
    
    def show_info(self, title: str, message: str):
        """Muestra información usando messagebox."""
        messagebox.showinfo(title, message, parent=self.parent)


class GuiLifeStatusWidget:
    """Widget visual para mostrar el estado de vida en la GUI con contador decremental."""
    
    def __init__(self, parent_frame: tk.Frame):
        """
        Inicializa el widget de estado de vida.
        
        Args:
            parent_frame: Frame padre donde colocar el widget
        """
        self.parent = parent_frame
        self.is_counting_down = False
        self.countdown_job = None
        
        # Frame contenedor
        self.frame = tk.Frame(parent_frame, bg='#001122', relief=tk.RAISED, bd=2)
        
        # Título con indicador de countdown
        self.title_label = tk.Label(self.frame,
                                   text="⏱️ Contador de Vida",
                                   font=('Arial', 10, 'bold'),
                                   bg='#001122', fg='#FFD700')
        self.title_label.pack(pady=5)
        
        # Contador principal (grande y prominente)
        self.countdown_label = tk.Label(self.frame,
                                       text="-- años",
                                       font=('Digital', 14, 'bold'),
                                       bg='#001122', fg='#00FF00')
        self.countdown_label.pack(pady=5)
        
        # Edad actual
        self.age_label = tk.Label(self.frame,
                                 text="Edad: -- años",
                                 font=('Arial', 9),
                                 bg='#001122', fg='white')
        self.age_label.pack(pady=2)
        
        # Estado visual del countdown
        self.status_indicator = tk.Label(self.frame,
                                        text="⭕ ESTABLE",
                                        font=('Arial', 9, 'bold'),
                                        bg='#001122', fg='#00FF00')
        self.status_indicator.pack(pady=2)
        
        # Barra de progreso de vida
        self.progress_frame = tk.Frame(self.frame, bg='#001122')
        self.progress_frame.pack(pady=5, padx=10, fill=tk.X)
        
        tk.Label(self.progress_frame, text="Vida:", 
                bg='#001122', fg='white', font=('Arial', 8)).pack(side=tk.LEFT)
        
        self.progress_canvas = tk.Canvas(self.progress_frame, 
                                       height=20, bg='#333333',
                                       highlightthickness=0)
        self.progress_canvas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5,0))
        
        # Porcentaje de vida
        self.percentage_label = tk.Label(self.frame,
                                        text="---%",
                                        font=('Arial', 8),
                                        bg='#001122', fg='#CCCCCC')
        self.percentage_label.pack(pady=2)
        
        # Total consumido
        self.consumed_label = tk.Label(self.frame,
                                      text="Consumido: -- años",
                                      font=('Arial', 8),
                                      bg='#001122', fg='#CCCCCC')
        self.consumed_label.pack(pady=2)
        
        # Variables para el contador decremental
        self.current_life_remaining = 0.0
        self.last_update_time = 0
        self.countdown_speed = 1.0  # años por segundo en tiempo real
        
    def start_countdown(self, initial_life: float, speed: float = 0.1):
        """
        Inicia el contador decremental en tiempo real.
        
        Args:
            initial_life: Vida inicial para el countdown
            speed: Velocidad del countdown (años por segundo)
        """
        self.current_life_remaining = initial_life
        self.countdown_speed = speed
        self.is_counting_down = True
        self.last_update_time = self.frame.tk.call('clock', 'seconds')
        self._update_countdown()
    
    def stop_countdown(self):
        """Detiene el contador decremental."""
        self.is_counting_down = False
        if self.countdown_job:
            self.frame.after_cancel(self.countdown_job)
            self.countdown_job = None
    
    def _update_countdown(self):
        """Actualiza el contador decremental en tiempo real."""
        if not self.is_counting_down:
            return
        
        current_time = self.frame.tk.call('clock', 'seconds')
        time_elapsed = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Decrementar vida
        self.current_life_remaining -= (self.countdown_speed * time_elapsed)
        self.current_life_remaining = max(0, self.current_life_remaining)
        
        # Actualizar display
        self._update_countdown_display()
        
        # Verificar si llegó a cero
        if self.current_life_remaining <= 0:
            self._trigger_death_alert()
            self.stop_countdown()
            return
        
        # Programar siguiente actualización
        self.countdown_job = self.frame.after(100, self._update_countdown)  # Actualizar cada 100ms
    
    def _update_countdown_display(self):
        """Actualiza la visualización del contador."""
        life = self.current_life_remaining
        
        # Formatear tiempo restante
        if life >= 1:
            time_text = f"{life:.1f} años"
        elif life >= 0.1:
            time_text = f"{life*12:.1f} meses"
        elif life > 0:
            time_text = f"{life*365:.0f} días"
        else:
            time_text = "0.0 años"
        
        # Actualizar contador principal
        self.countdown_label.config(text=time_text)
        
        # Cambiar colores según nivel crítico
        if life <= 0:
            self.countdown_label.config(fg='#FF0000')  # Rojo - muerto
            self.status_indicator.config(text="💀 MUERTO", fg='#FF0000')
        elif life <= 1:
            self.countdown_label.config(fg='#FF4444')  # Rojo - crítico
            self.status_indicator.config(text="🚨 CRÍTICO", fg='#FF4444')
        elif life <= 5:
            self.countdown_label.config(fg='#FFAA00')  # Amarillo - advertencia
            self.status_indicator.config(text="⚠️ PELIGRO", fg='#FFAA00')
        else:
            self.countdown_label.config(fg='#00FF00')  # Verde - estable
            self.status_indicator.config(text="⭕ ESTABLE", fg='#00FF00')
    
    def _trigger_death_alert(self):
        """Dispara alerta cuando el contador llega a cero."""
        import winsound
        try:
            # Sonido de sistema de Windows para muerte
            winsound.MessageBeep(winsound.MB_ICONHAND)
            # Reproducir múltiples beeps para simular "BRAY-YYYY"
            for _ in range(3):
                winsound.Beep(400, 500)  # 400Hz por 500ms
        except:
            # Fallback para sistemas sin winsound
            print("💀 *SONIDO DE MUERTE DE BURRO: BRAY-YYYY...*")
        
        # Actualizar visual
        self.countdown_label.config(text="0.0 años", fg='#FF0000', 
                                   font=('Digital', 16, 'bold'))
        self.status_indicator.config(text="💀 MUERTO", fg='#FF0000')
        
    def update_status(self, burro_status: dict):
        """
        Actualiza el widget con el estado actual del burro.
        
        Args:
            burro_status: Diccionario con el estado del burro
        """
        edad_actual = burro_status.get('edad_actual', 0)
        vida_restante = burro_status.get('vida_restante', 0)
        vida_consumida = burro_status.get('vida_consumida', 0)
        life_percentage = burro_status.get('life_percentage', 100)
        
        # Actualizar etiquetas básicas
        self.age_label.config(text=f"Edad: {edad_actual:.1f} años")
        self.consumed_label.config(text=f"Consumido: {vida_consumida:.1f} años")
        self.percentage_label.config(text=f"{life_percentage:.1f}%")
        
        # Actualizar contador principal
        self.current_life_remaining = vida_restante
        self._update_countdown_display()
        
        # Iniciar countdown si no está activo y hay vida
        if vida_restante > 0 and not self.is_counting_down:
            # Velocidad del countdown basada en actividad (simulación)
            # En modo normal: muy lento, en modo viaje: más rápido
            speed = 0.01 if vida_restante > 100 else 0.1
            self.start_countdown(vida_restante, speed)
        elif vida_restante <= 0:
            self.stop_countdown()
            self._trigger_death_alert()
        
        # Actualizar barra de progreso
        self._update_progress_bar(life_percentage)
        
        # Cambiar colores según el estado
        if vida_restante <= 0:
            # Muerto
            color = '#AA0000'
            self.age_label.config(fg='#FF4444')
        elif life_percentage <= 10:
            # Crítico
            color = '#FF4444'
            self.age_label.config(fg='#FF4444')
        elif life_percentage <= 25:
            # Advertencia
            color = '#FFAA00'
            self.age_label.config(fg='#FFAA00')
        else:
            # Normal
            color = '#44FF44'
            self.age_label.config(fg=color)
    
    def _update_progress_bar(self, percentage: float):
        """Actualiza la barra de progreso visual."""
        self.progress_canvas.delete("all")
        
        canvas_width = self.progress_canvas.winfo_width()
        canvas_height = self.progress_canvas.winfo_height()
        
        if canvas_width <= 1:  # Canvas no ha sido dibujado aún
            self.progress_canvas.after(100, lambda: self._update_progress_bar(percentage))
            return
        
        # Fondo gris
        self.progress_canvas.create_rectangle(0, 0, canvas_width, canvas_height,
                                            fill='#333333', outline='#666666')
        
        # Barra de progreso
        progress_width = (percentage / 100) * canvas_width
        
        if percentage > 50:
            color = '#44FF44'  # Verde
        elif percentage > 25:
            color = '#FFAA00'  # Amarillo
        elif percentage > 10:
            color = '#FF6600'  # Naranja
        else:
            color = '#FF4444'  # Rojo
        
        if progress_width > 0:
            self.progress_canvas.create_rectangle(0, 0, progress_width, canvas_height,
                                                fill=color, outline=color)
        
        # Texto del porcentaje
        text_color = 'white' if percentage < 50 else 'black'
        self.progress_canvas.create_text(canvas_width//2, canvas_height//2,
                                       text=f"{percentage:.0f}%",
                                       fill=text_color, font=('Arial', 8, 'bold'))
    
    def pack(self, **kwargs):
        """Pack el widget."""
        self.frame.pack(**kwargs)
    
    def grid(self, **kwargs):
        """Grid el widget."""
        self.frame.grid(**kwargs)
    
    def simulate_travel_countdown(self, travel_distance: float, warp_factor: float = 1.5):
        """
        Simula un viaje con countdown acelerado en tiempo real.
        
        Args:
            travel_distance: Distancia del viaje
            warp_factor: Factor warp para conversión
        """
        life_cost = travel_distance / warp_factor
        
        # Acelerar countdown para mostrar el efecto (1 segundo real = 1 año de vida)
        self.start_countdown(self.current_life_remaining, life_cost)
        
        # Mostrar mensaje de viaje
        self.status_indicator.config(text="🚀 VIAJANDO...", fg='#00AAFF')
        
        # Programar finalización del viaje
        travel_duration_ms = int(life_cost * 1000)  # 1 segundo por año
        self.frame.after(travel_duration_ms, self._finish_travel_simulation)
    
    def _finish_travel_simulation(self):
        """Finaliza la simulación de viaje."""
        if self.current_life_remaining > 0:
            self.status_indicator.config(text="✅ VIAJE COMPLETO", fg='#00FF00')
            # Volver a countdown normal después de 2 segundos
            self.frame.after(2000, lambda: self.start_countdown(self.current_life_remaining, 0.01))
        else:
            self.status_indicator.config(text="💀 MURIÓ EN VIAJE", fg='#FF0000')


class TravelDistanceAnalyzer:
    """Analizador de distancias de viaje con alertas de tiempo de vida."""
    
    def __init__(self, parent_window: tk.Tk):
        """
        Inicializa el analizador.
        
        Args:
            parent_window: Ventana padre de tkinter
        """
        self.parent = parent_window
        self.current_burro = None
    
    def set_burro(self, burro):
        """Configura el burro astronauta actual."""
        self.current_burro = burro
    
    def show_travel_preview(self, distance: float, route_description: str = ""):
        """
        Muestra una vista previa del costo de vida de un viaje.
        
        Args:
            distance: Distancia total del viaje
            route_description: Descripción opcional de la ruta
        """
        if not self.current_burro:
            messagebox.showwarning("Sin Burro", "No hay burro astronauta configurado")
            return
        
        # Calcular costo de vida
        life_cost = self.current_burro.calculate_travel_life_cost(distance)
        remaining_life = self.current_burro.get_remaining_life()
        life_after_travel = remaining_life - life_cost
        
        # Crear ventana de preview
        preview_window = tk.Toplevel(self.parent)
        preview_window.title("Análisis de Viaje - Costo de Vida")
        preview_window.geometry("400x300")
        preview_window.configure(bg='#001122')
        preview_window.resizable(False, False)
        
        # Hacer modal
        preview_window.transient(self.parent)
        preview_window.grab_set()
        
        # Título
        title_label = tk.Label(preview_window,
                              text="⏱️ Análisis de Tiempo de Vida",
                              font=('Arial', 14, 'bold'),
                              bg='#001122', fg='#FFD700')
        title_label.pack(pady=10)
        
        # Información del viaje
        info_frame = tk.Frame(preview_window, bg='#001122')
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # Detalles
        details = [
            f"📍 Ruta: {route_description or 'Viaje espacial'}",
            f"📏 Distancia: {distance:.2f} unidades espaciales",
            f"⏰ Tiempo de vida requerido: {life_cost:.2f} años",
            f"",
            f"👤 Edad actual: {self.current_burro.current_age:.1f} años",
            f"💫 Vida restante: {remaining_life:.1f} años",
            f"🎯 Vida después del viaje: {life_after_travel:.1f} años"
        ]
        
        for detail in details:
            if detail == "":
                continue
            label = tk.Label(info_frame, text=detail,
                            font=('Arial', 10),
                            bg='#001122', fg='white',
                            justify=tk.LEFT)
            label.pack(anchor=tk.W, pady=2)
        
        # Estado del viaje
        status_frame = tk.Frame(preview_window, bg='#001122')
        status_frame.pack(pady=10, padx=20, fill=tk.X)
        
        if life_after_travel <= 0:
            status_text = "💀 ¡VIAJE MORTAL!"
            status_desc = "Este viaje causará la muerte del Burro Astronauta"
            status_color = '#FF4444'
        elif life_after_travel < 5:
            status_text = "🚨 VIAJE CRÍTICO"
            status_desc = f"Quedará muy poca vida: {life_after_travel:.1f} años"
            status_color = '#FFAA00'
        elif life_cost > remaining_life * 0.5:
            status_text = "⚠️ VIAJE COSTOSO"
            status_desc = f"Consumirá {(life_cost/remaining_life)*100:.1f}% de la vida restante"
            status_color = '#FFAA00'
        else:
            status_text = "✅ VIAJE SEGURO"
            status_desc = f"Impacto moderado en el tiempo de vida"
            status_color = '#44FF44'
        
        status_label = tk.Label(status_frame, text=status_text,
                               font=('Arial', 12, 'bold'),
                               bg='#001122', fg=status_color)
        status_label.pack(pady=5)
        
        desc_label = tk.Label(status_frame, text=status_desc,
                             font=('Arial', 9),
                             bg='#001122', fg='white',
                             wraplength=350)
        desc_label.pack(pady=2)
        
        # Botones
        button_frame = tk.Frame(preview_window, bg='#001122')
        button_frame.pack(pady=20)
        
        close_button = tk.Button(button_frame, text="Cerrar",
                                command=preview_window.destroy,
                                font=('Arial', 10),
                                bg='#003366', fg='white',
                                padx=20, pady=5)
        close_button.pack()
        
        # Centrar ventana
        preview_window.update_idletasks()
        x = (preview_window.winfo_screenwidth() // 2) - (preview_window.winfo_width() // 2)
        y = (preview_window.winfo_screenheight() // 2) - (preview_window.winfo_height() // 2)
        preview_window.geometry(f"+{x}+{y}")


class LifeEventLogger(ILifeObserver):
    """Logger de eventos de vida que mantiene historial visible en GUI."""
    
    def __init__(self, max_events: int = 50):
        """
        Inicializa el logger.
        
        Args:
            max_events: Número máximo de eventos a mantener
        """
        self.events = []
        self.max_events = max_events
        self.listeners = []  # Callbacks para notificar cambios
    
    def handle_life_event(self, event: LifeEvent):
        """Maneja un evento de vida agregándolo al historial."""
        self.events.append(event)
        
        # Mantener solo los eventos más recientes
        if len(self.events) > self.max_events:
            self.events = self.events[-self.max_events:]
        
        # Notificar a listeners
        for listener in self.listeners:
            try:
                listener(event)
            except Exception as e:
                print(f"Error notificando listener: {e}")
    
    def add_listener(self, callback):
        """Agrega un callback para notificaciones de eventos."""
        self.listeners.append(callback)
    
    def get_recent_events(self, count: int = 10) -> list:
        """Obtiene los eventos más recientes."""
        return self.events[-count:] if self.events else []
    
    def clear_events(self):
        """Limpia el historial de eventos."""
        self.events.clear()