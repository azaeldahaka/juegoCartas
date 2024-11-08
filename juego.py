import random

# Definimos las cartas genéricas
def generar_cartas():
    cartas = [
        {'tipo': 'verdad', 'descripcion': '¿Cuál es tu mayor miedo?'},
        {'tipo': 'reto', 'descripcion': 'Haz 10 saltos de tijera'},
        {'tipo': 'verdad', 'descripcion': '¿Qué harías si fueras invisible por un día?'},
        {'tipo': 'reto', 'descripcion': 'Canta una canción a todo pulmón'},
        {'tipo': 'verdad', 'descripcion': '¿Qué es lo más vergonzoso que te ha pasado?'},
        {'tipo': 'reto', 'descripcion': 'Haz una imitación de alguien famoso'},
    ]
    random.shuffle(cartas)  # Barajamos las cartas
    return cartas

# Definimos la clase Jugador
class Jugador:
    def _init_(self, nombre):
        self.nombre = nombre
        self.puntos = 0

    def ganar_punto(self):
        self.puntos += 1

# Definimos la clase Juego
class Juego:
    def _init_(self):
        self.jugadores = []
        self.cartas = generar_cartas()
        self.turno_actual = 0

    def agregar_jugador(self, nombre):
        self.jugadores.append(Jugador(nombre))

    def obtener_siguiente_jugador(self):
        jugador = self.jugadores[self.turno_actual]
        self.turno_actual = (self.turno_actual + 1) % len(self.jugadores)
        return jugador

    def obtener_siguiente_carta(self):
        return self.cartas.pop() if self.cartas else None

    def jugar(self):
        while self.cartas:
            jugador = self.obtener_siguiente_jugador()
            carta = self.obtener_siguiente_carta()

            print(f"\nEs el turno de {jugador.nombre}!")
            print(f"Carta: {carta['tipo'].capitalize()} - {carta['descripcion']}")

            respuesta = input(f"{jugador.nombre}, ¿quieres aceptar el reto/verdad? (sí/no): ").strip().lower()

            if respuesta == 'sí':
                jugador.ganar_punto()
                print(f"¡{jugador.nombre} ha ganado un punto!")
            else:
                print(f"{jugador.nombre} ha decidido no participar en esta carta.")

            print(f"--- Puntos de {jugador.nombre}: {jugador.puntos} ---")

        # Al final del juego
        self.mostrar_resultados()

    def mostrar_resultados(self):
        print("\nEl juego ha terminado. Resultados finales:")
        for jugador in self.jugadores:
            print(f"{jugador.nombre}: {jugador.puntos} puntos")
        ganador = max(self.jugadores, key=lambda j: j.puntos)
        print(f"¡{ganador.nombre} ha ganado el juego!")