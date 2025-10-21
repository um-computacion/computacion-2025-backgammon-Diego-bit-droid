"""Backgammon game logic module."""

from core.clases.validaciones import MovimientoInvalidoError
from core.clases.excepciones import (
    JuegoNoInicializadoError,
    TurnoJugadorInvalidoError,
    JuegoYaFinalizadoError,
    SinMovimientosDisponiblesError,
    ValorDadoInvalidoError
)


class BackgammonGame:
    """Main Backgammon game controller class."""

    # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-instance-attributes
    def __init__(self, board, dice, jugador1, jugador2, reglas=None):
        """
        Inicializa una nueva partida de Backgammon.

        Args:
            board: instancia del tablero.
            dice: instancia de los dados.
            jugador1: primer jugador.
            jugador2: segundo jugador.
            reglas: lista opcional de funciones de validación.
        """
        self.__board__ = board
        self.__dice__ = dice
        self.__turno__ = 0
        self.__movimientos_restantes__ = 0
        self.__jugador1__ = jugador1
        self.__jugador2__ = jugador2
        self.__reglas__ = reglas if reglas else []

    def calcular_movimientos_totales(self, dado1, dado2):
        """
        Calcula los movimientos disponibles según los valores de los dados.

        Args:
            dado1: valor del primer dado.
            dado2: valor del segundo dado.

        Returns:
            list: movimientos disponibles.

        Raises:
            ValorDadoInvalidoError: si algún dado está fuera del rango permitido.
        """
        if not 1 <= dado1 <= 6 or not 1 <= dado2 <= 6:
            invalid = dado1 if not 1 <= dado1 <= 6 else dado2
            raise ValorDadoInvalidoError(invalid)
        return [dado1] * 4 if dado1 == dado2 else [dado1, dado2]

    def mostrar_movimientos_disponibles(self, dado1, dado2):
        """
        Muestra por consola los movimientos disponibles según los dados.

        Args:
            dado1: valor del primer dado.
            dado2: valor del segundo dado.
        """
        movimientos = self.calcular_movimientos_totales(dado1, dado2)
        print(f"Movimientos disponibles: {movimientos}")

    def get_jugador_por_nombre(self, nombre):
        """
        Devuelve el jugador correspondiente al nombre proporcionado.

        Args:
            nombre: nombre del jugador.

        Returns:
            Player: instancia del jugador.

        Raises:
            TurnoJugadorInvalidoError: si el nombre no coincide con ningún jugador.
        """
        if nombre == self.__jugador1__.get_nombre():
            return self.__jugador1__
        if nombre == self.__jugador2__.get_nombre():
            return self.__jugador2__
        raise TurnoJugadorInvalidoError(nombre)

    def quien_empieza(self):
        """
        Determina aleatoriamente qué jugador comienza la partida.

        Returns:
            int: número de turno asignado (1 o 2).
        """
        while True:
            dado1, _ = self.__dice__.lanzar_dados()
            dado2, _ = self.__dice__.lanzar_dados()
            print(f"{self.__jugador1__.get_nombre()} sacó {dado1}")
            print(f"{self.__jugador2__.get_nombre()} sacó {dado2}")
            if dado1 > dado2:
                self.__turno__ = 1
                print(f"Empieza {self.__jugador1__.get_nombre()}")
                return 1
            if dado2 > dado1:
                self.__turno__ = 2
                print(f"Empieza {self.__jugador2__.get_nombre()}")
                return 2
            print("Empate, se vuelve a lanzar")

    def iniciar_partida(self):
        """
        Inicia la partida si aún no ha comenzado.

        Raises:
            JuegoYaFinalizadoError: si la partida ya fue iniciada.
        """
        if self.__turno__ != 0:
            raise JuegoYaFinalizadoError()
        print("Iniciando partida")
        self.quien_empieza()
        self.lanzar_dados()

    def get_jugador_actual(self):
        """
        Devuelve el jugador que tiene el turno actual.

        Returns:
            Player: jugador activo.

        Raises:
            JuegoNoInicializadoError: si el turno aún no fue asignado.
        """
        if self.__turno__ == 1:
            return self.__jugador1__
        if self.__turno__ == 2:
            return self.__jugador2__
        raise JuegoNoInicializadoError()

    def cambiar_turno(self):
        """
        Cambia el turno al otro jugador y lanza los dados.

        Raises:
            JuegoNoInicializadoError: si el turno actual es inválido.
        """
        if self.__turno__ not in [1, 2]:
            raise JuegoNoInicializadoError()
        self.__turno__ = 2 if self.__turno__ == 1 else 1
        jugador = self.get_jugador_actual()
        print(f"Turno cambiado le toca a {jugador.get_nombre()} con ficha {jugador.get_ficha()}")
        self.lanzar_dados()

    def lanzar_dados(self):
        """
        Lanza los dados y actualiza los movimientos disponibles.

        Returns:
            tuple: valores obtenidos en los dos dados.
        """
        dado1, dado2 = self.__dice__.lanzar_dados()
        self.__movimientos_restantes__ = 4 if dado1 == dado2 else 2
        nombre = self.get_jugador_actual().get_nombre()
        movs = self.__movimientos_restantes__
        print(f"{nombre} lanzó {dado1} y {dado2}, movimientos disponibles: {movs}")
        return dado1, dado2

    def mover_ficha(self, movimientos, dado1, dado2):
        """
        Realiza los movimientos indicados en el tablero si son válidos.

        Args:
            movimientos: lista de tuplas (desde, hasta).
            dado1: valor del primer dado.
            dado2: valor del segundo dado.

        Returns:
            dict: resultado del movimiento.
        """
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
        """
        Verifica si algún jugador ha ganado la partida.

        Returns:
            bool: True si hay ganador, False en caso contrario.
        """
        fuera = self.__board__.get_tablero()["fuera"]
        for jugador in [self.__jugador1__, self.__jugador2__]:
            if fuera[jugador.get_nombre()] == 15:
                print(f"{jugador.get_nombre()} ha ganado la partida")
                return True
        return False

    def get_tablero(self):
        """
        Devuelve el estado actual del tablero.

        Returns:
            dict: representación del tablero.
        """
        return self.__board__.get_tablero()

    def get_fichas_en_tablero(self, player):
        """
        Devuelve la cantidad de fichas del jugador en el tablero.

        Args:
            player: instancia del jugador.

        Returns:
            int: cantidad de fichas en el tablero.
        """
        posiciones = self.__board__.get_tablero()["posiciones"]
        return player.fichas_en_tablero(posiciones)

    def get_fichas_en_bar(self, player):
        """
        Devuelve la cantidad de fichas del jugador en el bar.

        Args:
            player: instancia del jugador.

        Returns:
            int: cantidad de fichas en el bar.
        """
        captured = self.__board__.get_tablero()["bar"]
        return player.fichas_en_bar(captured)

    def get_fichas_sacadas(self, player):
        """
        Devuelve la cantidad de fichas del jugador que fueron sacadas del juego.

        Args:
            player: instancia del jugador.

        Returns:
            int: cantidad de fichas fuera del tablero.
        """
        fuera = self.__board__.get_tablero()["fuera"]
        return player.fichas_sacadas(fuera)
    def estado_turno(self):
        """
        Muestra por consola el estado actual del turno.

        Incluye el nombre del jugador activo y el símbolo de su ficha.
        """
        jugador = self.get_jugador_actual()
        print(f"Turno actual de {jugador.get_nombre()} con ficha {jugador.get_ficha()}")

    def get_movimientos_totales(self, dado1, dado2):
        """
        Devuelve la lista de movimientos disponibles según los valores de los dados.

        Args:
            dado1: valor del primer dado.
            dado2: valor del segundo dado.

        Returns:
            list: movimientos disponibles, considerando dobles si corresponde.
        """
        return self.calcular_movimientos_totales(dado1, dado2)
