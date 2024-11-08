from juego import Juego

def main():
    juego = Juego()
    print("Bienvenidos al juego de 'Verdad o Reto'!")

    # Agregar jugadores
    while True:
        nombre = input("Ingresa el nombre del jugador (o escribe 'fin' para terminar): ").strip()
        if nombre.lower() == 'fin':
            break
        juego.agregar_jugador(nombre)

    if len(juego.jugadores) < 2:
        print("¡Necesitas al menos 2 jugadores para jugar!")
        return

    print("\n¡El juego está por comenzar!")
    input("Presiona Enter para empezar...")
    
    # Iniciar el juego
    juego.jugar()