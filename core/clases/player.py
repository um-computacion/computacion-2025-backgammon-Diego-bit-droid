class Player:
    def __init__(self, nombre, ficha):
        self.__nombre__ = nombre  
        self.__ficha__ = ficha    
    def get_nombre(self):
        """devuelve el nombre del jugador
        """
        return self.__nombre__

    def get_ficha(self):
        """ devuelve la ficha que usa el jugador
        """
        return self.__ficha__

    def fichas_en_tablero(self, posiciones):
        """
        cuenta cuantas fichas tiene el jugador en el tablero
        revisa todas las posiciones y suma las que tienen su ficha
        """
        return sum(
            1 for pos in posiciones
            for checker in pos
            if checker.simbolo == self.__ficha__
        )

    def fichas_en_bar(self, bar):
        """
        cuenta cuantas fichas tiene el jugador en el bar
        busca en el diccionario usando su nombre
        """
        return bar.get(self.__nombre__, 0)

    def fichas_sacadas(self, fuera):
        """
        str: cuenta cuantas fichas tiene el jugador fuera del juego
        busca en el diccionario usando su nombre
        """
        return fuera.get(self.__nombre__, 0)

    def estado_jugador(self, posiciones, bar, fuera):
        """devuelve un resumen del estado del jugador
        incluye el nombre la ficha que usa y cuantas fichas tiene en cada zona
        tambien muestra el total sumando todas
        """
        en_tablero = self.fichas_en_tablero(posiciones)
        en_bar = self.fichas_en_bar(bar)
        sacadas = self.fichas_sacadas(fuera)

        return {
            "nombre": self.__nombre__,
            "ficha": self.__ficha__,
            "en_tablero": en_tablero,
            "en_bar": en_bar,
            "sacadas": sacadas,
            "total": en_tablero + en_bar + sacadas
        }