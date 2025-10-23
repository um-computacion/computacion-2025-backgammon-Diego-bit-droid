"""Backgammon game logic module."""
from core.clases.board import Board
from core.clases.dice import Dice
from core.clases.player import Player
from core.clases.validaciones import MovimientoInvalidoError
from core.clases.excepciones import (
    JuegoNoInicializadoError,
    TurnoJugadorInvalidoError,
    JuegoYaFinalizadoError,
    ValorDadoInvalidoError
)


class BackgammonGame:  # pylint: disable=too-many-public-methods
    """Main Backgammon game controller class."""

    def __init__(self, jugador1, jugador2, reglas=None):
        """
        Inicializa una nueva partida de Backgammon.

        Args:
            jugador1: primer jugador.
            jugador2: segundo jugador.
            reglas: lista opcional de funciones de validación.
        """
        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__turno__ = 0
        self.__movimientos_restantes__ = 0
        self.__jugador1__ = Player(nombre=jugador1, ficha='X')
        self.__jugador2__ = Player(nombre=jugador2, ficha='O')
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
        """Determina aleatoriamente qué jugador comienza la partida."""
        while True:
            dado1, _ = self.__dice__.lanzar_dados()
            dado2, _ = self.__dice__.lanzar_dados()
            if dado1 > dado2:
                self.__turno__ = 1
                return (1, dado1, dado2)
            if dado2 > dado1:
                self.__turno__ = 2
                return (2, dado1, dado2)

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
        """Cambia el turno al otro jugador."""
        if self.__turno__ not in [1, 2]:
            raise JuegoNoInicializadoError()
        self.__turno__ = 2 if self.__turno__ == 1 else 1
        self.__movimientos_restantes__ = 0
        return self.get_jugador_actual()

    def lanzar_dados(self):
        """Lanza los dados y actualiza movimientos disponibles."""
        dado1, dado2 = self.__dice__.lanzar_dados()
        self.__movimientos_restantes__ = 4 if dado1 == dado2 else 2
        return dado1, dado2, self.__movimientos_restantes__

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
            print("No hay movimientos disponibles en este turno.")
            return {
                "resultados": [False] * len(movimientos),
                "dados_usados": [],
                "dados_restantes": [],
                "log": ["No hay movimientos disponibles en este turno."]
            }

        dados_disponibles = self.calcular_movimientos_totales(dado1, dado2)

        try:
            for regla in self.__reglas__:
                regla(jugador, movimientos, dados_disponibles, self.__board__)
        except MovimientoInvalidoError as e:
            print(e.mensaje)
            print("Movimiento inválido, ingrese otro.")
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
        if not any(resultado["resultados"]):
            print("Movimiento inválido, ingrese otro.")

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
            if fuera['player1' if jugador == self.__jugador1__ else 'player2'] == 15:
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
        return player.fichas_en_tablero(self.__board__)

    def get_fichas_en_bar(self, player):
        """
        Devuelve la cantidad de fichas del jugador en el bar.

        Args:
            player: instancia del jugador.

        Returns:
            int: cantidad de fichas en el bar.
        """
        return player.fichas_en_bar(self.__board__)

    def get_fichas_sacadas(self, player):
        """
        Devuelve la cantidad de fichas del jugador que fueron sacadas del juego.

        Args:
            player: instancia del jugador.

        Returns:
            int: cantidad de fichas fuera del tablero.
        """
        return player.fichas_sacadas(self.__board__)

    def estado_turno(self):
        """
        Muestra por consola el estado actual del turno.

        Incluye el nombre del jugador activo y el símbolo de su ficha.
        """
        jugador = self.get_jugador_actual()
        print(f"Turno actual de {jugador.get_nombre()} con ficha {jugador.get_ficha()}")

    def get_jugador1(self):
        """Devuelve la instancia del jugador 1."""
        return self.__jugador1__

    def get_jugador2(self):
        """Devuelve la instancia del jugador 2."""
        return self.__jugador2__

    def get_board(self):
        """Devuelve la instancia del tablero."""
        return self.__board__

    def get_turno(self):
        """
        Devuelve el número del turno actual.

        Returns:
            int: 0 si no ha iniciado, 1 para jugador1, 2 para jugador2
        """
        return self.__turno__

    def get_movimientos_restantes(self):
        """
        Devuelve la cantidad de movimientos restantes en el turno actual.

        Returns:
            int: número de movimientos disponibles
        """
        return self.__movimientos_restantes__

    def mostrar_tablero(self):
        """
        Muestra el tablero en consola (delegación al board).

        Returns:
            dict: estado del tablero
        """
        return self.__board__.mostrar_board()

    def juego_activo(self):
        """
        Verifica si el juego está en curso (iniciado pero no terminado).

        Returns:
            bool: True si está activo, False si no
        """
        return self.__turno__ != 0 and not self.hay_ganador()

    def get_estado_juego(self):
        """
        Devuelve un diccionario con el estado completo del juego.

        Returns:
            dict: información completa del estado actual
        """
        jugador_actual = None
        try:
            jugador_actual = self.get_jugador_actual()
        except JuegoNoInicializadoError:
            jugador_actual = None
        return {
            "turno": self.__turno__,
            "movimientos_restantes": self.__movimientos_restantes__,
            "jugador_actual": jugador_actual.get_nombre() if jugador_actual else None,
            "tablero": self.get_tablero(),
            "jugador1": {
                "nombre": self.__jugador1__.get_nombre(),
                "ficha": self.__jugador1__.get_ficha(),
                "fichas_tablero": self.get_fichas_en_tablero(self.__jugador1__),
                "fichas_bar": self.get_fichas_en_bar(self.__jugador1__),
                "fichas_sacadas": self.get_fichas_sacadas(self.__jugador1__)
            },
            "jugador2": {
                "nombre": self.__jugador2__.get_nombre(),
                "ficha": self.__jugador2__.get_ficha(),
                "fichas_tablero": self.get_fichas_en_tablero(self.__jugador2__),
                "fichas_bar": self.get_fichas_en_bar(self.__jugador2__),
                "fichas_sacadas": self.get_fichas_sacadas(self.__jugador2__)
            }
        }
