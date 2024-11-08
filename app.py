import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageTk
import ttkthemes
from juego import Juego

class JuegoInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Verdad o Reto")
        self.root.geometry("600x500")
        self.root.config(bg="#f7f7f7")

        # Usar un tema moderno
        style = ttkthemes.ThemedStyle(root)
        style.set_theme("arc")  # Elegir el tema 'arc' para un diseño moderno

        self.juego = Juego()
        self.turno_actual = 0
        self.crear_widgets()

    def crear_widgets(self):
        # Título
        self.titulo_label = tk.Label(self.root, text="¡Bienvenidos al Juego de Verdad o Reto!", font=("Helvetica", 20, "bold"), bg="#4CAF50", fg="white")
        self.titulo_label.pack(pady=20, fill=tk.X)

        # Frame para agregar jugadores
        self.frame_jugadores = tk.Frame(self.root, bg="#f7f7f7")
        self.frame_jugadores.pack(pady=10)

        self.nombre_label = tk.Label(self.frame_jugadores, text="Ingrese el nombre del jugador:", font=("Helvetica", 14), bg="#f7f7f7")
        self.nombre_label.pack(padx=10, side=tk.LEFT)

        self.nombre_entry = tk.Entry(self.frame_jugadores, font=("Helvetica", 14))
        self.nombre_entry.pack(padx=10, side=tk.LEFT)

        self.agregar_button = ttk.Button(self.frame_jugadores, text="Agregar Jugador", command=self.agregar_jugador)
        self.agregar_button.pack(pady=10, side=tk.LEFT)

        # Botón de finalizar y iniciar
        self.fin_button = ttk.Button(self.root, text="Terminar de Agregar Jugadores", command=self.terminar_agregar_jugadores)
        self.fin_button.pack(pady=10)

        self.iniciar_button = ttk.Button(self.root, text="Iniciar Juego", command=self.iniciar_juego, state=tk.DISABLED)
        self.iniciar_button.pack(pady=10)

        # Frame para los botones de aceptar/rechazar
        self.frame_acciones = tk.Frame(self.root, bg="#f7f7f7")
        self.frame_acciones.pack(pady=20)

        # Botón de reinicio siempre activo, ubicado al final
        self.reiniciar_button = ttk.Button(self.root, text="Reiniciar Juego", command=self.reiniciar_juego)
        self.reiniciar_button.pack(pady=20, side=tk.BOTTOM)

        # Recuadro donde aparecerá el turno y la carta
        self.carta_frame = tk.Frame(self.root, bg="#f7f7f7")
        self.carta_frame.pack(pady=20)

        # Crear un canvas para la "carta" redondeada
        self.canvas = tk.Canvas(self.carta_frame, width=500, height=250, bg="#ffffff", bd=0, highlightthickness=0)
        self.canvas.pack()

        # Redondear el rectángulo con la función de PIL
        self.redondear_rectangulo()

        # Label para mostrar los mensajes del juego
        self.mensaje_label = tk.Label(self.canvas, text="Esperando jugadores...", font=("Helvetica", 14), wraplength=400, justify="center", bg="#ffffff", fg="#333333")
        self.mensaje_label.place(relx=0.5, rely=0.3, anchor="center")

        # Botones de Aceptar y Rechazar dentro del recuadro
        self.aceptar_button = ttk.Button(self.canvas, text="Aceptar", command=lambda: self.responder_reto(True), state=tk.DISABLED)
        self.aceptar_button.place(relx=0.3, rely=0.7, anchor="center")

        self.rechazar_button = ttk.Button(self.canvas, text="Rechazar", command=lambda: self.responder_reto(False), state=tk.DISABLED)
        self.rechazar_button.place(relx=0.7, rely=0.7, anchor="center")

    def redondear_rectangulo(self):
        """Dibuja un rectángulo redondeado en el canvas."""
        # Crear una imagen en blanco
        image = Image.new('RGBA', (500, 250), (255, 255, 255, 255))  # Ajustar tamaño para todo el contenido
        draw = ImageDraw.Draw(image)
        
        # Dibujar el rectángulo redondeado con PIL
        draw.rounded_rectangle([(10, 10), (480, 240)], radius=20, fill="#ffffff", outline="#4CAF50", width=2)

        # Convertir la imagen a un formato que pueda ser usado en Tkinter
        self.img = ImageTk.PhotoImage(image)

        # Mostrar la imagen en el canvas
        self.canvas.create_image(0, 0, image=self.img, anchor=tk.NW)

    def agregar_jugador(self):
        nombre = self.nombre_entry.get()
        if nombre:
            self.juego.agregar_jugador(nombre)
            self.nombre_entry.delete(0, tk.END)
            self.actualizar_mensaje(f"{nombre} ha sido agregado al juego.")
            if len(self.juego.jugadores) > 1:
                self.iniciar_button.config(state=tk.NORMAL)
            self.fin_button.config(state=tk.NORMAL)  # Activar el botón para terminar de agregar
        else:
            self.actualizar_mensaje("El nombre no puede estar vacío.")
    
    def terminar_agregar_jugadores(self):
        if len(self.juego.jugadores) > 1:
            self.iniciar_button.config(state=tk.NORMAL)
            self.fin_button.config(state=tk.DISABLED)
            self.actualizar_mensaje("Jugadores agregados, ¡listos para jugar!")
        else:
            self.actualizar_mensaje("Se necesitan al menos dos jugadores para comenzar.")

    def iniciar_juego(self):
        if len(self.juego.jugadores) < 2:
            self.actualizar_mensaje("Se necesitan al menos dos jugadores.")
            return
        
        self.actualizar_mensaje(f"El juego ha comenzado...")
        self.jugar_turno()

    def jugar_turno(self):
        if not self.juego.cartas:
            self.actualizar_mensaje("¡El juego ha terminado!")
            self.mostrar_resultado()
            return

        jugador = self.juego.jugadores[self.turno_actual]
        carta = self.juego.obtener_siguiente_carta()

        # Actualizar el mensaje con el jugador actual y la carta jugada
        self.actualizar_mensaje(f"Es el turno de:\n{jugador.nombre}\nCarta: {carta.tipo}\n{carta.descripcion}")
        
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

    def reiniciar_juego(self):
        self.juego = Juego()  # Reiniciar el objeto del juego
        self.turno_actual = 0  # Restablecer el turno
        self.iniciar_button.config(state=tk.DISABLED)
        self.reiniciar_button.config(state=tk.NORMAL)
        self.actualizar_mensaje("Juego reiniciado. ¡Esperando jugadores...")

# Ejecución de la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    juego_interfaz = JuegoInterfaz(root)
    root.mainloop()
