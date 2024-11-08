import tkinter as tk
from tkinter import font
from juego import Juego

class JuegoInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Verdad o Reto")
        self.root.geometry("600x500")
        self.root.config(bg="#f0f0f0")  # Color de fondo claro
        
        # Definir una fuente personalizada
        self.custom_font = font.Font(family="Helvetica", size=14, weight="bold")

        self.juego = Juego()
        self.turno_actual = 0  # Se añadirá un índice para controlar el turno
        self.crear_widgets()

    def crear_widgets(self):
        # Título
        self.titulo_label = tk.Label(self.root, text="¡Bienvenidos al Juego de Verdad o Reto!", font=("Arial", 20), bg="#ffcc00", fg="white")
        self.titulo_label.pack(pady=20, fill=tk.X)

        # Frame para agregar jugadores
        self.frame_jugadores = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_jugadores.pack(pady=10)

        self.nombre_label = tk.Label(self.frame_jugadores, text="Ingrese el nombre del jugador:", font=self.custom_font, bg="#f0f0f0")
        self.nombre_label.pack(padx=10, side=tk.LEFT)

        self.nombre_entry = tk.Entry(self.frame_jugadores, font=self.custom_font)
        self.nombre_entry.pack(padx=10, side=tk.LEFT)

        self.agregar_button = tk.Button(self.frame_jugadores, text="Agregar Jugador", command=self.agregar_jugador, font=self.custom_font, bg="#4CAF50", fg="white")
        self.agregar_button.pack(pady=10, side=tk.LEFT)

        # Botones de finalizar y iniciar
        self.fin_button = tk.Button(self.root, text="Terminar de Agregar Jugadores", command=self.terminar_agregar_jugadores, font=self.custom_font, state=tk.DISABLED, bg="#ff9800", fg="white")
        self.fin_button.pack(pady=10)

        self.iniciar_button = tk.Button(self.root, text="Iniciar Juego", command=self.iniciar_juego, font=self.custom_font, state=tk.DISABLED, bg="#2196F3", fg="white")
        self.iniciar_button.pack(pady=10)

        # Label para mostrar los mensajes del juego
        self.mensaje_label = tk.Label(self.root, text="Esperando jugadores...", font=("Arial", 14), wraplength=400, justify="left", bg="#f0f0f0")
        self.mensaje_label.pack(pady=20)

        # Frame para los botones de aceptar/rechazar
        self.frame_acciones = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_acciones.pack(pady=20)

        self.aceptar_button = tk.Button(self.frame_acciones, text="Aceptar", command=lambda: self.responder_reto(True), state=tk.DISABLED, font=self.custom_font, bg="#4CAF50", fg="white")
        self.aceptar_button.pack(padx=10, side=tk.LEFT)

        self.rechazar_button = tk.Button(self.frame_acciones, text="Rechazar", command=lambda: self.responder_reto(False), state=tk.DISABLED, font=self.custom_font, bg="#F44336", fg="white")
        self.rechazar_button.pack(padx=10, side=tk.LEFT)

    def agregar_jugador(self):
        nombre = self.nombre_entry.get()
        if nombre:
            self.juego.agregar_jugador(nombre)
            self.nombre_entry.delete(0, tk.END)
            self.actualizar_mensaje(f"{nombre} ha sido agregado al juego.")
            self.iniciar_button.config(state=tk.NORMAL)
        else:
            self.actualizar_mensaje("El nombre no puede estar vacío.")
    
    def terminar_agregar_jugadores(self):
        self.juego.agregar_jugador(self.nombre_entry.get())
        self.nombre_entry.delete(0, tk.END)
        self.fin_button.config(state=tk.DISABLED)
        self.iniciar_button.config(state=tk.NORMAL)
        self.actualizar_mensaje("Jugadores agregados, ¡listos para jugar!")

    def iniciar_juego(self):
        if len(self.juego.jugadores) < 2:
            self.actualizar_mensaje("Se necesitan al menos dos jugadores.")
            return
        
        self.actualizar_mensaje("El juego ha comenzado... ¡Es el primer turno!")
        self.jugar_turno()

    def jugar_turno(self):
        if not self.juego.cartas:
            self.actualizar_mensaje("¡El juego ha terminado!")
            self.mostrar_resultado()
            return

        # Obtener el jugador actual de acuerdo al turno
        jugador = self.juego.jugadores[self.turno_actual]
        carta = self.juego.obtener_siguiente_carta()

        # Actualizar el mensaje con el jugador actual
        self.actualizar_mensaje(f"Es el turno de {jugador.nombre}. Carta: {carta}")
        
        # Habilitar los botones de aceptar/rechazar
        self.aceptar_button.config(state=tk.NORMAL)
        self.rechazar_button.config(state=tk.NORMAL)

    def responder_reto(self, aceptar):
        jugador = self.juego.jugadores[self.turno_actual]
        if aceptar:
            jugador.ganar_punto()
            self.actualizar_mensaje(f"{jugador.nombre} ha ganado un punto.")
        else:
            self.actualizar_mensaje(f"{jugador.nombre} ha rechazado el reto.")
        
        # Pasar al siguiente jugador
        self.turno_actual = (self.turno_actual + 1) % len(self.juego.jugadores)

        # Deshabilitar botones hasta el siguiente turno
        self.aceptar_button.config(state=tk.DISABLED)
        self.rechazar_button.config(state=tk.DISABLED)

        self.jugar_turno()

    def actualizar_mensaje(self, mensaje):
        self.mensaje_label.config(text=mensaje)

    def mostrar_resultado(self):
        max_puntos = max(jugador.puntos for jugador in self.juego.jugadores)
        ganadores = [jugador for jugador in self.juego.jugadores if jugador.puntos == max_puntos]

        if len(ganadores) == 1:
            self.actualizar_mensaje(f"El ganador es {ganadores[0].nombre} con {ganadores[0].puntos} puntos.")
        else:
            resultado = "¡Es un empate entre los siguientes jugadores!\n"
            resultado += "\n".join([f"{ganador.nombre} con {ganador.puntos} puntos." for ganador in ganadores])
            self.actualizar_mensaje(resultado)

# Crear la ventana principal
if __name__ == "__main__":
    root = tk.Tk()
    juego_interfaz = JuegoInterfaz(root)
    root.mainloop()
