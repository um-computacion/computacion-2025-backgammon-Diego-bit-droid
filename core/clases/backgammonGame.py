
class BackgammonGame:
    def __init__(self,board,dice,jugador1,jugador2):
        self.__board__ = board
        self.__dice__ = dice
        self.__turno__ = 0
        self.__movimientos_restantes__ = 0
        self.__jugador1__ = jugador1
        self.__jugador2__ = jugador2
    def calcular_movimientos_totales(self,dado1,dado2):
         if dado1 == dado2:  
            return [dado1] * 4
         else:
            return [dado1, dado2]
    def mostrar_movimientos_disponibles(self, dado1, dado2):
        movimientos = self.calcular_movimientos_totales(dado1, dado2)
        print(f"Movimientos disponibles: {movimientos}")
        
    def get_jugador_por_nombre(self, nombre):
        if nombre == self.__jugador1__.get_nombre():
            return self.__jugador1__
        elif nombre == self.__jugador2__.get_nombre():
            return self.__jugador2__
        return None

    def quien_empieza(self):
        # lanza los dados para decidir quien empieza la partida
        while True:
            dado1, _ = self.__dice__.lanzar_dados()
            dado2, _ = self.__dice__.lanzar_dados()

            print(f"{self.__jugador1__.get_nombre()} saco {dado1}")
            print(f"{self.__jugador2__.get_nombre()} saco {dado2}")

            if dado1 > dado2:
                self.__turno__ = 1  # asigna turno al jugador 1
                print(f"empieza {self.__jugador1__.get_nombre()}")
                return 1
            elif dado2 > dado1:
                self.__turno__ = 2  # asigna turno al jugador 2
                print(f"empieza {self.__jugador2__.get_nombre()}")
                return 2
            else:
                print("empate se vuelve a lanzar")  # repite si hay empate

    def iniciar_partida(self):
        # inicia la partida llamando a quien_empieza y lanzando los dados
        print("iniciando partida")
        self.quien_empieza()
        self.lanzar_dados()

    def get_jugador_actual(self):
        # devuelve el jugador al que le toca jugar segun el turno actual
        if self.__turno__ == 1:
            return self.__jugador1__
        elif self.__turno__ == 2:
            return self.__jugador2__
        else:
            raise ValueError("turno no inicializado")

    def cambiar_turno(self):
        # cambia el turno al otro jugador y lanza los dados
        self.__turno__ = 2 if self.__turno__ == 1 else 1
        jugador = self.get_jugador_actual()
        print(f"turno cambiado ahora le toca a {jugador.get_nombre()} con ficha {jugador.get_simbolo()}")
        self.lanzar_dados()

    def lanzar_dados(self):
        # lanza los dados y actualiza los movimientos disponibles
        dado1, dado2 = self.__dice__.lanzar_dados()
        self.__movimientos_restantes__ = 4 if dado1 == dado2 else 2
        print(f"{self.get_jugador_actual().get_nombre()} lanzo {dado1} y {dado2} movimientos disponibles {self.__movimientos_restantes__}")
        return dado1, dado2

    def mover_ficha(self, movimientos, dado1, dado2):
        # ejecuta los movimientos del jugador actual usando los dados
        jugador = self.get_jugador_actual()
        resultado = self.__board__.mover_ficha(jugador, movimientos, dado1, dado2)

        usados = len(resultado["dados_usados"])
        self.__movimientos_restantes__ -= usados

        for linea in resultado["log"]:
            print(linea)  # muestra cada accion realizada

        if self.__movimientos_restantes__ <= 0:
            self.cambiar_turno()  # cambia turno si ya no hay movimientos

        return resultado  # devuelve resultado del movimiento

    def hay_ganador(self):
        # verifica si algun jugador tiene 15 fichas fuera del tablero
        fuera = self.__board__.get_tablero()["fuera"]
        for jugador in [self.__jugador1__, self.__jugador2__]:
            if jugador.fichas_sacadas(fuera) == 15:
                print(f"{jugador.get_nombre()} ha ganado la partida")
                return True
        return False

    def get_tablero(self):
        # devuelve el estado completo del tablero
        return self.__board__.get_tablero()

    def get_jugador_por_nombre(self, nombre):
        # busca y devuelve un jugador por su nombre
        return self.__jugadores__.get(nombre)

    def get_fichas_en_tablero(self, player):
        # cuenta cuantas fichas tiene el jugador en las posiciones del tablero
        posiciones = self.__board__.get_tablero()["posiciones"]
        return player.fichas_en_tablero(posiciones)

    def get_fichas_en_bar(self, player):
        # cuenta cuantas fichas tiene el jugador en el bar
        bar = self.__board__.get_tablero()["bar"]
        return player.fichas_en_bar(bar)

    def get_fichas_sacadas(self, player):
        # cuenta cuantas fichas tiene el jugador fuera del juego
        fuera = self.__board__.get_tablero()["fuera"]
        return player.fichas_sacadas(fuera)

    def estado_turno(self):
        # imprime quien tiene el turno actual y que ficha esta usando
        jugador = self.get_jugador_actual()
        print(f"turno actual de {jugador.get_nombre()} con ficha {jugador.get_simbolo()}")
    def get_movimientos_totales(self, dado1, dado2):
        """
        Entrada:
            dado1 (int): valor del primer dado
            dado2 (int): valor del segundo dado
        Salida:
            list: lista de movimientos disponibles según los dados
        """
        return self.calcular_movimientos_totales(dado1, dado2)