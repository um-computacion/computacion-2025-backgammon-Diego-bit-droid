class Board:
    def __init__(self):
        # 24 posiciones del tablero de backgammon (0-23)
        self.__posiciones__ = [[] for _ in range(24)]
        # Bar (fichas comidas)
        self.__bar__ = {'player1': 0, 'player2': 0}
        # Fichas fuera del juego
        self.__fuera__ = {'player1': 0, 'player2': 0}

    def preparar_tablero(self):
        # Colocar fichas en posiciones iniciles para preparar el tablero para el juego
      
    def mostrar_board(self):
        # Mostrar representación visual del tablero en consola
        

    def mover_ficha(self, desde, hasta, jugador):
        # mover ficha desde cualquier lugar hacia cualquier lugar:
        # del bar  al tablero 
        # de una posición del tablero (desde = 0-23) a otra (hasta = 0-23)
        # del tablero (desde = 0-23) al fuera (hasta = "fuera")
        # incluye validación de movimiento inválido
        # retorna True si movimiento exitoso, False si inválido
        # incluye actualizacion en ficha  comidas cuando come una
        
   