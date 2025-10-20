from core.clases.validaciones import  MovimientoInvalidoError
from core.clases.excepciones import (JuegoNoInicializadoError,
    TurnoJugadorInvalidoError,
    JuegoYaFinalizadoError,
    SinMovimientosDisponiblesError,
    ValorDadoInvalidoError
)

class BackgammonGame:
    def __init__(self, board, dice, jugador1, jugador2, reglas=None):
        self.__board__ = board
        self.__dice__ = dice
        self.__turno__ = 0
        self.__movimientos_restantes__ = 0
        self.__jugador1__ = jugador1
        self.__jugador2__ = jugador2
        self.__reglas__ = reglas if reglas else []

    def calcular_movimientos_totales(self, dado1, dado2):
        if not (1 <= dado1 <= 6) or not (1 <= dado2 <= 6):
            raise ValorDadoInvalidoError(dado1 if not (1 <= dado1 <= 6) else dado2)
        return [dado1] * 4 if dado1 == dado2 else [dado1, dado2]

    def mostrar_movimientos_disponibles(self, dado1, dado2):
        movimientos = self.calcular_movimientos_totales(dado1, dado2)
        print(f"Movimientos disponibles: {movimientos}")

    def get_jugador_por_nombre(self, nombre):
        if nombre == self.__jugador1__.get_nombre():
            return self.__jugador1__
        elif nombre == self.__jugador2__.get_nombre():
            return self.__jugador2__
        raise TurnoJugadorInvalidoError(nombre)

    def quien_empieza(self):
        while True:
            dado1, _ = self.__dice__.lanzar_dados()
            dado2, _ = self.__dice__.lanzar_dados()

            print(f"{self.__jugador1__.get_nombre()} sacó {dado1}")
            print(f"{self.__jugador2__.get_nombre()} sacó {dado2}")

            if dado1 > dado2:
                self.__turno__ = 1
                print(f"Empieza {self.__jugador1__.get_nombre()}")
                return 1
            elif dado2 > dado1:
                self.__turno__ = 2
                print(f"Empieza {self.__jugador2__.get_nombre()}")
                return 2
            else:
                print("Empate, se vuelve a lanzar")

    def iniciar_partida(self):
        if self.__turno__ != 0:
            raise JuegoYaFinalizadoError()
        print("Iniciando partida")
        self.quien_empieza()
        self.lanzar_dados()

    def get_jugador_actual(self):
        if self.__turno__ == 1:
            return self.__jugador1__
        elif self.__turno__ == 2:
            return self.__jugador2__
        raise JuegoNoInicializadoError()

    def cambiar_turno(self):
        if self.__turno__ not in [1, 2]:
            raise JuegoNoInicializadoError()
        self.__turno__ = 2 if self.__turno__ == 1 else 1
        jugador = self.get_jugador_actual()
        print(f"Turno cambiado, ahora le toca a {jugador.get_nombre()} con ficha {jugador.get_ficha()}")
        self.lanzar_dados()

    def lanzar_dados(self):
        dado1, dado2 = self.__dice__.lanzar_dados()
        self.__movimientos_restantes__ = 4 if dado1 == dado2 else 2
        print(f"{self.get_jugador_actual().get_nombre()} lanzó {dado1} y {dado2}, movimientos disponibles: {self.__movimientos_restantes__}")
        return dado1, dado2

    def mover_ficha(self, movimientos, dado1, dado2):
        jugador = self.get_jugador_actual()
        if self.__movimientos_restantes__ <= 0:
            raise SinMovimientosDisponiblesError(jugador.get_nombre())

        dados_disponibles = self.calcular_movimientos_totales(dado1, dado2)

        try:
            for regla in self.__reglas__:
                regla(jugador, movimientos, dados_disponibles, self.__board__)
        except MovimientoInvalidoError as e:
            print(e.mensaje)
            return {
                "resultados": [False] * len(movimientos),
                "dados_usados": [],
                "dados_restantes": dados_disponibles,
                "log": [e.mensaje]
            }

        resultado = self.__board__.mover_ficha(jugador, movimientos, dados_disponibles)
        self.__movimientos_restantes__ -= len(resultado["dados_usados"])

        for linea in resultado["log"]:
            print(linea)

        if self.__movimientos_restantes__ <= 0:
            self.cambiar_turno()

        return resultado

    def hay_ganador(self):
        fuera = self.__board__.get_tablero()["fuera"]
        for jugador in [self.__jugador1__, self.__jugador2__]:
            nombre = jugador.get_nombre()
            if fuera[nombre] == 15:
                print(f"{nombre} ha ganado la partida")
                return True
        return False

    def get_tablero(self):
        return self.__board__.get_tablero()

    def get_fichas_en_tablero(self, player):
        posiciones = self.__board__.get_tablero()["posiciones"]
        return player.fichas_en_tablero(posiciones)

    def get_fichas_en_bar(self, player):
        bar = self.__board__.get_tablero()["bar"]
        return player.fichas_en_bar(bar)

    def get_fichas_sacadas(self, player):
        fuera = self.__board__.get_tablero()["fuera"]
        return player.fichas_sacadas(fuera)

    def estado_turno(self):
        jugador = self.get_jugador_actual()
        print(f"Turno actual de {jugador.get_nombre()} con ficha {jugador.get_ficha()}")

    def get_movimientos_totales(self, dado1, dado2):
        return self.calcular_movimientos_totales(dado1, dado2)
