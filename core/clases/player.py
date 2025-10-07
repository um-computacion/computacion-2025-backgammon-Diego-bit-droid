class Player:
    def __init__(self, nombre, ficha):
        self.__nombre__ = nombre
        self.__ficha__ = ficha

    def get_nombre(self):
        """
        Entrada:
            None
        Salida:
            str: nombre del jugador
        """
        return self.__nombre__

    def get_ficha(self):
        """
        Entrada:
            None
        Salida:
            str: símbolo de ficha del jugador
        """
        return self.__ficha__

    def fichas_en_tablero(self, posiciones):
        """
        Entrada:
            posiciones (list): lista de pilas de fichas en el tablero
        Salida:
            int: cantidad de fichas del jugador en el tablero
        """
        return sum(1 for pila in posiciones for ficha in pila if ficha.get_simbolo() == self.__ficha__)

    def fichas_en_bar(self, board):
        return board.get_fichas_en_bar(self)

    def fichas_sacadas(self, board):
        return board.get_fichas_sacadas(self)


    def estado_jugador(self, board):
        """
        Entrada:
            board (Board): instancia del tablero que contiene la información del juego.
        Salida:
            dict: resumen del estado actual del jugador.

        """
        en_tablero = board.get_fichas_en_tablero(self)
        en_bar = board.get_fichas_en_bar(self)
        sacadas = board.get_fichas_sacadas(self)
        total = en_tablero + en_bar + sacadas

        return {
            "nombre": self.get_nombre(),
            "ficha": self.get_ficha(),
            "en_tablero": en_tablero,
            "en_bar": en_bar,
            "sacadas": sacadas,
            "total": total
        }
