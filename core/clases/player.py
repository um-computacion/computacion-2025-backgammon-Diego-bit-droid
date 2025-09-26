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

    def fichas_en_bar(self, bar):
        """
        Entrada:
            bar (list): lista de fichas en el bar
        Salida:
            int: cantidad de fichas del jugador en el bar
        """
        return sum(1 for ficha in bar if ficha.get_simbolo() == self.__ficha__)

    def fichas_sacadas(self, fuera):
        """
        Entrada:
            fuera (list): lista de fichas fuera del tablero
        Salida:
            int: cantidad de fichas del jugador fuera del juego
        """
        return sum(1 for ficha in fuera if ficha.get_simbolo() == self.__ficha__)

    def estado_jugador(self, posiciones, bar, fuera):
        """
        Entrada:
            posiciones (list): lista de pilas en el tablero
            bar (list): lista de fichas en el bar
            fuera (list): lista de fichas fuera del tablero
        Salida:
            dict: resumen del estado del jugador
        """
        en_tablero = self.fichas_en_tablero(posiciones)
        en_bar = self.fichas_en_bar(bar)
        sacadas = self.fichas_sacadas(fuera)
        total = en_tablero + en_bar + sacadas

        return {
            "nombre": self.get_nombre(),
            "ficha": self.get_ficha(),
            "en_tablero": en_tablero,
            "en_bar": en_bar,
            "sacadas": sacadas,
            "total": total
        }