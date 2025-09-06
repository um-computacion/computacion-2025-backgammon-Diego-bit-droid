from core.clases.BackgammonGame import BackgammonGame
class Checker:
    def __init__(self, nombre_jugador, backgammon):
        self.__nombre_jugador__ = nombre_jugador
        self.__backgammon__ = backgammon

    def get_nombre(self):
        return self.__nombre_jugador__

    def get_ficha(self):
        jugador = self.__backgammon__.get_jugador_por_nombre(self.__nombre_jugador__)
        if jugador is None:
            raise ValueError(f"jugador '{self.__nombre_jugador__}' no está registrado en el juego")
        return jugador.get_ficha()
