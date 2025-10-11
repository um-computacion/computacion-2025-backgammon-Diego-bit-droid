class Player:
    def __init__(self, nombre, ficha):
        self.__nombre__ = nombre
        self.__ficha__ = ficha

    def get_nombre(self):
        return self.__nombre__

    def get_ficha(self):
        return self.__ficha__

    def fichas_en_tablero(self, board):
        posiciones = board.get_tablero()["posiciones"]
        return sum(1 for pila in posiciones for ficha in pila if ficha.get_simbolo() == self.__ficha__)

    def fichas_en_bar(self, board):
        return board.get_bar(self.get_nombre())

    def fichas_sacadas(self, board):
        return board.get_fuera(self.get_nombre())

    def estado_jugador(self, board):
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