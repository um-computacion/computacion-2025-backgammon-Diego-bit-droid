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
    def puede_comer(self, hasta, jugador):
        destino = self.__posiciones__[hasta]
        if len(destino) == 1 and destino[0].simbolo != jugador.simbolo:
            return True
        return False
    def mover_desde_bar(self, hasta, jugador):
        if self.__bar__[jugador.nombre] == 0:
            return False  # No hay fichas en el bar para mover

        if not self.puede_mover_a(hasta, jugador):
            return False  # No puede mover a esa posición (bloqueada)

        if self.puede_comer(hasta, jugador):
            self.__posiciones__[hasta].pop()  # Comer ficha enemiga
            self.__bar__[jugador.oponente()] += 1  # Enviar al bar del oponente

        self.__posiciones__[hasta].append(Checker(jugador.simbolo))
        self.__bar__[jugador.nombre] -= 1  # Sacar ficha del bar
        return True
    def mover_desde_posicion(self, desde, hasta, jugador):
        if self.__bar__[jugador.nombre] > 0:
            return False  # No puede mover otras fichas si tiene fichas en el bar

        if not self.puede_mover_a(hasta, jugador):
            return False  # Posición bloqueada

        if not self.__posiciones__[desde]:
            return False  # No hay fichas en la posición de origen

        ficha = self.__posiciones__[desde][-1]
        if ficha.simbolo != jugador.simbolo:
            return False  # La ficha no pertenece al jugador

        self.__posiciones__[desde].pop()  # Sacar ficha del origen

        if self.puede_comer(hasta, jugador):
            self.__posiciones__[hasta].pop()
            self.__bar__[jugador.oponente()] += 1

        self.__posiciones__[hasta].append(Checker(jugador.simbolo))
        return True
        # mover ficha desde cualquier lugar hacia cualquier lugar:
        # del bar  al tablero 
        # de una posición del tablero (desde = 0-23) a otra (hasta = 0-23)
        # del tablero (desde = 0-23) al fuera (hasta = "fuera")
        # incluye validación de movimiento inválido
        # retorna True si movimiento exitoso, False si inválido
        # incluye actualizacion en ficha  comidas cuando come una
        
        
        pass
    def mover_a_fuera(self, desde, jugador):
        if self.__bar__[jugador.nombre] > 0:
            return False  # No puede sacar fichas si tiene fichas en el bar

        if not self.__posiciones__[desde]:
            return False  # No hay fichas en la posición

        ficha = self.__posiciones__[desde][-1]
        if ficha.simbolo != jugador.simbolo:
            return False  # No es su ficha

        self.__posiciones__[desde].pop()
        self.__fuera__[jugador.nombre] += 1
        return True
    def calcular_movimientos_totales(self,dado1,dado2):
         if dado1 == dado2:  
            return [dado1] * 4
         else:
            return [dado1, dado2]
         
    def mover_ficha(self, desde, hasta, jugador):
        # Movimiento desde el bar al tablero
        if desde == "bar":
            return self.mover_desde_bar(hasta, jugador)

        # Movimiento desde el tablero hacia fuera
        if hasta == "fuera":
            return self.mover_a_fuera(desde, jugador)

        # Movimiento entre posiciones del tablero
        if isinstance(desde, int) and isinstance(hasta, int):
            return self.mover_desde_posicion(desde, hasta, jugador)

        # Movimiento inválido
        return False        