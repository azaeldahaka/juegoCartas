import random

class Carta:
    def __init__(self, tipo, descripcion):
        self.tipo = tipo  # 'Verdad' o 'Reto'
        self.descripcion = descripcion

    def __str__(self):
        return f"{self.tipo}: {self.descripcion}"

def generar_cartas():
    # Cartas de ejemplo, puedes agregar más
    cartas = [
        Carta("Verdad", "¿Cuál es tu mayor miedo?"),
        Carta("Verdad", "¿A quién le contarías tus secretos más oscuros?"),
        Carta("Reto", "Baila durante 30 segundos sin música."),
        Carta("Reto", "Imita a un animal hasta que alguien adivine cuál es.")
    ]
    random.shuffle(cartas)
    return cartas

class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puntos = 0

    def ganar_punto(self):
        self.puntos += 1

    def __str__(self):
        return f"{self.nombre} (Puntos: {self.puntos})"

class Juego:
    def __init__(self):
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
