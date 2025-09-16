from core.clases.checker import Checker

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
    def mover_ficha(self, jugador, movimientos, dado1, dado2):
        """ movimientos: lista de tuplas (desde, hasta)
        dado1, dado2: valores de los dados lanzados

        Retorna:
            - resultados: lista de True/False por cada movimiento
            - dados_usados: lista de dados que se usaron
            - dados_restantes: lista de dados que no se usaron
            - log: lista explicando cada acción
        """
        dados = self.calcular_movimientos_totales(dado1, dado2)
        resultados = []
        dados_usados = []
        log = []

        for desde, hasta in movimientos:
            distancia = self.calcular_distancia(desde, hasta, jugador)


            if distancia not in dados:
                resultados.append(False)
                log.append(f"No se puede usar dado {distancia} para mover de {desde} a {hasta}.")
                continue

            # Validación previa
            if not self.validar_movimiento(desde, hasta, jugador):
                resultados.append(False)
                log.append(f"Movimiento inválido de {desde} a {hasta} para jugador {jugador.ficha}.")
                continue

            # Comer ficha enemiga si corresponde
            ficha_comida = False
            if self.puede_comer(hasta, jugador):
                self.__posiciones__[hasta].pop()
                self.__bar__[jugador.oponente()] += 1
                ficha_comida = True

            # Ejecutar movimiento
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
            dados.remove(distancia)
            dados_usados.append(distancia)

        return {
            "resultados": resultados,
            "dados_usados": dados_usados,
            "dados_restantes": dados,
            "log": log}
    def calcular_movimientos_totales(self,dado1,dado2):
         if dado1 == dado2:  
            return [dado1] * 4
         else:
            return [dado1, dado2]
    def calcular_distancia(self, desde, hasta, jugador):
        """
        Calcula la distancia entre dos puntos según el sentido del jugador.
        Si el movimiento es desde el 'bar' o hacia 'fuera', se traduce a posición numérica.
        """
        if desde == "bar":
            desde = 0 if jugador.ficha== "X" else 23
        if hasta == "fuera":
            hasta = 23 if jugador.ficha == "X" else 0

        if not isinstance(desde, int) or not isinstance(hasta, int):
            raise ValueError(f"Desde y hasta deben ser enteros o palabras clave válidas ('bar', 'fuera'). Recibido: desde={desde}, hasta={hasta}")

        # Sentido de movimiento
        if jugador.ficha == "X":
            return hasta - desde
        else:
            return desde - hasta
            
    
    