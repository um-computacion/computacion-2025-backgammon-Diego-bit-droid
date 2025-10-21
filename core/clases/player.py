"""Módulo que define la clase Player para representar a un jugador en Backgammon."""

class Player:
    """Representa a un jugador de Backgammon con nombre y símbolo de ficha."""

    def __init__(self, nombre, ficha):
        """Crea un jugador con un nombre y una ficha."""
        self.__nombre__ = nombre
        self.__ficha__ = ficha

    def get_nombre(self):
        """Devuelve el nombre del jugador."""
        return self.__nombre__

    def get_ficha(self):
        """Devuelve el símbolo de la ficha del jugador."""
        return self.__ficha__

    def fichas_en_tablero(self, board):
        """Cuenta cuántas fichas del jugador hay en el tablero."""
        posiciones = board.get_tablero()["posiciones"]
        return sum(
            1 for pila in posiciones for ficha in pila
            if ficha.get_simbolo() == self.__ficha__
        )

    def fichas_en_bar(self, board):
        """Devuelve cuántas fichas del jugador están en el bar."""
        return board.get_bar(self.get_nombre())

    def fichas_sacadas(self, board):
        """Devuelve cuántas fichas del jugador fueron sacadas del juego."""
        return board.get_fuera(self.get_nombre())

    def estado_jugador(self, board):
        """Devuelve un resumen del estado actual del jugador."""
        en_tablero = self.fichas_en_tablero(board)
        en_bar = self.fichas_en_bar(board)
        sacadas = self.fichas_sacadas(board)
        total = en_tablero + en_bar + sacadas

        return {
            "nombre": self.get_nombre(),
            "ficha": self.get_ficha(),
            "en_tablero": en_tablero,
            "en_bar": en_bar,
            "sacadas": sacadas,
            "total": total
        }
