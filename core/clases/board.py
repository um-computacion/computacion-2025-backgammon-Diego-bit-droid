from core.clases.checker import Checker
from core.clases.backgammonGame import BackgammonGame

class Board:
    def __init__(self):
        # 24 posiciones del tablero de backgammon (0-23)
        self.__posiciones__ = self.preparar_tablero()
        # bar (fichas comidas)
        self.__bar__ = {'player1': 0, 'player2': 0}
        # fichas fuera del juego
        self.__fuera__ = {'player1': 0, 'player2': 0}

    def get_tablero(self):
        return {
            "posiciones": [list(pos) for pos in self.__posiciones__],
            "bar": dict(self.__bar__),
            "fuera": dict(self.__fuera__)
        }

    
    def preparar_tablero(self):
        self.__posiciones__ = [[] for _ in range(24)]
                #fichas jugador1
        self.__posiciones__[0] = [Checker("X") for i in range(2)] # 2 fichas en posición 0
        self.__posiciones__[11] = [Checker("X") for i in range(5)]  # 5 fichas en posición 11
        self.__posiciones__[16] = [Checker("X") for i in range(3)]  # 3 fichas en posición 16
        self.__posiciones__[18] = [Checker("X") for i in range(5)]  # 5 fichas en posición 18

        #fichas jugador2
        self.__posiciones__[23] = [Checker("O") for i in range(2)]  # 2 fichas en posición 23
        self.__posiciones__[12] = [Checker("O") for i in range(5)]  # 5 fichas en posición 12
        self.__posiciones__[7] = [Checker("O") for i in range(3)]   # 3 fichas en posición 7
        self.__posiciones__[5] = [Checker("O") for i in range(5)]   # 5 fichas en posición 5
        return self.__posiciones__
    def mostrar_board(self):
        print("="*60)
        
        print(f"BAR P1: {self.__bar__['player1']} fichas | BAR P2: {self.__bar__['player2']} fichas")
        print()
        
        
        print("Posiciones 0-23:")
        print("-" * 50)
       
        header_top = ""
        for i in range(12, 24):
            header_top += f"{i:2d} "
        print(header_top)
        
        
        max_height_top = 0
        for i in range(12, 24):
            if len(self.__posiciones__[i]) > max_height_top:
                max_height_top = len(self.__posiciones__[i])

        for height in range(max_height_top):
            line = ""
            for i in range(12, 24):
                if height < len(self.__posiciones__[i]):
                    line += f" {self.__posiciones__[i][height]} "
                else:
                    line += "   "
            print(line)
                
        print("-" * 50)
        print()
        
    
        max_height_bottom = 0
        for i in range(11, -1, -1):
            if len(self.__posiciones__[i]) > max_height_bottom:
                max_height_bottom = len(self.__posiciones__[i])
        
        
        for height in range(max_height_bottom - 1, -1, -1): 
            line = []
            for i in range(11, -1, -1):  
                if height < len(self.__posiciones__[i]):
                    line.append(f" {self.__posiciones__[i][height]} ")
                else:
                    line.append("   ")
            print("".join(line))  


        header_bottom = ""
        for i in range(11, -1, -1):
            header_bottom += f"{i:2d} "
        print(header_bottom)
        
        print("-" * 50)
        print()
    
        print(f"FUERA P1: {self.__fuera__['player1']} fichas | FUERA P2: {self.__fuera__['player2']} fichas")
        print("="*60)
        #implementar a la hora de mostrar el tablero que se muestre el estado de cada jugador
    def mover_ficha(self, jugador, movimientos, dados_disponibles):
        """
        Aplica una lista de movimientos sobre el tablero, usando los dados disponibles.

        Args:
            jugador (Player): jugador que realiza los movimientos.
            movimientos (list): lista de tuplas (desde, hasta) indicando los movimientos deseados.
            dados_disponibles (list): lista de valores de dados que se pueden usar.

        Returns:
            dict: contiene:
                - resultados (list): True/False por cada movimiento.
                - dados_usados (list): dados que se usaron.
                - dados_restantes (list): dados que no se usaron.
                - log (list): mensajes explicando cada acción realizada.
    """
        resultados = []
        dados_usados = []
        log = []

        for desde, hasta in movimientos:
            distancia = self.calcular_distancia(desde, hasta, jugador)

            if distancia not in dados_disponibles:
                resultados.append(False)
                log.append(f"No se puede usar dado {distancia} para mover de {desde} a {hasta}.")
                continue
            if not self.validar_movimiento(desde, hasta, jugador):
                resultados.append(False)
                log.append(f"Movimiento inválido de {desde} a {hasta} para jugador {jugador.ficha}.")
                continue

            ficha_comida = False
            if self.puede_comer(hasta, jugador):
                self.__posiciones__[hasta].pop()
                self.__bar__[jugador.oponente()] += 1
                ficha_comida = True

            if desde == "bar":
                self.__bar__[jugador.nombre] -= 1
            else:
                self.__posiciones__[desde].pop()

            if hasta == "fuera":
                self.__fuera__[jugador.nombre] += 1
                log.append(f"{jugador.ficha} sacó ficha desde {desde} usando dado {distancia}.")
            else:
                self.__posiciones__[hasta].append(Checker(jugador.ficha))
                log.append(f"{jugador.ficha} movió de {desde} a {hasta} usando dado {distancia}." +
                           (" Comió ficha enemiga." if ficha_comida else ""))

            resultados.append(True)
            dados_disponibles.remove(distancia)
            dados_usados.append(distancia)

        return {
            "resultados": resultados,
            "dados_usados": dados_usados,
            "dados_restantes": dados_disponibles,
            "log": log
        }

    def calcular_distancia(self, desde, hasta, jugador):
        """
        Calcula la distancia entre dos posiciones según el sentido de movimiento del jugador.

        Args:
            desde (int or str): posición inicial o 'bar'.
            hasta (int or str): posición final o 'fuera'.
            jugador (Player): jugador que realiza el movimiento.

        Returns:
            int: distancia entre las posiciones, positiva si es válida.
        """
        if desde == "bar":
            desde = 0 if jugador.ficha == "X" else 23
        if hasta == "fuera":
            hasta = 23 if jugador.ficha == "X" else 0
        return hasta - desde if jugador.ficha == "X" else desde - hasta

    def validar_movimiento(self, desde, hasta, jugador):
        """
        Verifica si el movimiento es válido:
        - La posición de origen debe tener fichas.
        - La ficha superior debe pertenecer al jugador.

        Args:
            desde (int or str): posición inicial.
            hasta (int): posición destino.
            jugador (Player): jugador que realiza el movimiento.

        Returns:
            bool: True si el movimiento es válido, False si no.
        """
        if desde != "bar" and desde in self.__posiciones__:
            if not self.__posiciones__[desde]:
                return False
            return self.__posiciones__[desde][-1].ficha == jugador.get_ficha()
        return True

    def puede_comer(self, hasta, jugador):
        """
        Determina si el jugador puede comer una ficha enemiga en la posición destino.

        Args:
            hasta (int): posición destino.
            jugador (Player): jugador que realiza el movimiento.

        Returns:
            bool: True si puede comer (hay una sola ficha enemiga), False si no.
        """
        pila = self.__posiciones__[hasta]
        return len(pila) == 1 and pila[-1].get_simbolo() != jugador.get_ficha()