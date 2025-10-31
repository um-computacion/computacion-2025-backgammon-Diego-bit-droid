"""Backgammon game logic module."""
from core.board import Board
from core.dice import Dice
from core.player import Player
from core.validaciones import MovimientoInvalidoError
from core.excepciones import (
    JuegoNoInicializadoError,
    JuegoYaFinalizadoError,
    ValorDadoInvalidoError
)


class BackgammonGame:  # pylint: disable=too-many-public-methods,too-many-instance-attributes
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
        self.__jugador1__ = Player(nombre=jugador1, ficha='O')
        self.__jugador2__ = Player(nombre=jugador2, ficha='X')
        self.__reglas__ = reglas if reglas else []
        self.__dados_disponibles__ = []
        self.__valores_dados__ = (0, 0)

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

    def get_dados_disponibles(self):
        """
        Devuelve la lista de dados que aún están disponibles para usar.

        Returns:
            list: valores de dados disponibles
        """
        return self.__dados_disponibles__.copy()

    def mostrar_movimientos_disponibles(self, dado1, dado2):
        """
        Muestra por consola los movimientos disponibles según los dados.

        Args:
            dado1: valor del primer dado.
            dado2: valor del segundo dado.
        """
        dados_disponibles = self.get_dados_disponibles()
        if dados_disponibles:
            return dados_disponibles
        movimientos = self.calcular_movimientos_totales(dado1, dado2)
        return movimientos

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
        self.__dados_disponibles__ = []
        self.__valores_dados__ = (0, 0)
        return self.get_jugador_actual()

    def lanzar_dados(self):
        """
        Lanza los dados y actualiza movimientos disponibles.
        Cambia turno automáticamente si no hay movimientos legales.
        """
        dado1, dado2 = self.__dice__.lanzar_dados()
        self.__valores_dados__ = (dado1, dado2)
        self.__movimientos_restantes__ = 4 if dado1 == dado2 else 2
        self.__dados_disponibles__ = self.calcular_movimientos_totales(dado1, dado2)
        jugador_actual = self.get_jugador_actual()
        if not self.tiene_movimientos_legales(jugador_actual, dado1, dado2):
            self.cambiar_turno()
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
            return {
                "resultados": [False] * len(movimientos),
                "dados_usados": [],
                "dados_restantes": [],
                "log": ["No hay movimientos disponibles en este turno."]
            }

        if not self.__dados_disponibles__:
            self.__dados_disponibles__ = self.calcular_movimientos_totales(dado1, dado2)

        dados_disponibles = self.__dados_disponibles__.copy()

        try:
            for regla in self.__reglas__:
                regla(jugador, movimientos, dados_disponibles, self.__board__)
        except MovimientoInvalidoError as e:
            if not self._tiene_movimientos_con_dados_actuales(jugador):
                self.cambiar_turno()
            return {
                "resultados": [False] * len(movimientos),
                "dados_usados": [],
                "dados_restantes": self.__dados_disponibles__.copy(),
                "log": [str(e)]
            }

        resultado = self.__board__.mover_ficha(jugador, movimientos, dados_disponibles)

        if not any(resultado["resultados"]):
            if not self._tiene_movimientos_con_dados_actuales(jugador):
                self.cambiar_turno()
            return resultado

        for dado_usado in resultado["dados_usados"]:
            if dado_usado in self.__dados_disponibles__:
                self.__dados_disponibles__.remove(dado_usado)

        self.__movimientos_restantes__ -= len(resultado["dados_usados"])

        if self.__movimientos_restantes__ <= 0:
            self.cambiar_turno()
        elif not self._tiene_movimientos_con_dados_actuales(jugador):
            self.cambiar_turno()

        return resultado

    def _tiene_movimientos_con_dados_actuales(self, jugador):
        """
        Verifica si hay movimientos legales con los dados ACTUALMENTE disponibles.

        Args:
            jugador: instancia del jugador

        Returns:
            bool: True si hay movimientos legales
        """
        dados_disponibles = self.__dados_disponibles__.copy()
        if not dados_disponibles:
            return False
        if jugador.fichas_en_bar(self.__board__) > 0:
            zona_entrada = (list(range(0, 6)) if jugador.get_ficha() == 'O'
                          else list(range(18, 24)))
            for destino in zona_entrada:
                distancia = self.__board__.calcular_distancia('bar', destino, jugador)
                if distancia not in dados_disponibles:
                    continue

                pila_destino = self.__board__.get_posiciones(destino)
                if pila_destino and pila_destino[-1].get_simbolo() != jugador.get_ficha():
                    if len(pila_destino) > 1:
                        continue

                movimiento = [('bar', destino)]
                if self._validar_movimiento_con_reglas(jugador, movimiento,
                                                       dados_disponibles.copy()):
                    return True
            return False
        for pos in range(24):
            posicion = self.__board__.get_posiciones(pos)
            if posicion and posicion[-1].get_simbolo() == jugador.get_ficha():
                for dado in set(dados_disponibles):
                    if self._verificar_movimiento_desde_posicion(jugador, pos, dado,
                                                                 dados_disponibles.copy()):
                        return True
        return False

    def hay_ganador(self):
        """
        Verifica si algún jugador ha ganado la partida.

        Returns:
            bool: True si hay ganador, False en caso contrario.
        """
        fuera = self.__board__.get_tablero()["fuera"]
        if fuera.get('player1', 0) == 15:
            return True
        if fuera.get('player2', 0) == 15:
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

    def get_jugador1(self):
        """Devuelve la instancia del jugador 1."""
        return self.__jugador1__

    def get_jugador2(self):
        """Devuelve la instancia del jugador 2."""
        return self.__jugador2__

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
            "dados_disponibles": self.__dados_disponibles__.copy(),
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

    def tiene_movimientos_legales(self, jugador, dado1, dado2):
        # pylint: disable=too-many-branches,too-many-nested-blocks
        """
        Verifica si el jugador tiene algún movimiento legal disponible.

        Args:
            jugador: instancia del jugador.
            dado1: valor del primer dado.
            dado2: valor del segundo dado.

        Returns:
            bool: True si hay al menos un movimiento legal, False en caso contrario.
        """
        dados_disponibles = self.calcular_movimientos_totales(dado1, dado2)
        if jugador.fichas_en_bar(self.__board__) > 0:
            zona_entrada = (list(range(0, 6)) if jugador.get_ficha() == 'O'
                          else list(range(18, 24)))
            for destino in zona_entrada:
                distancia = self.__board__.calcular_distancia('bar', destino, jugador)
                if distancia not in dados_disponibles:
                    continue
                pila_destino = self.__board__.get_posiciones(destino)
                if pila_destino and pila_destino[-1].get_simbolo() != jugador.get_ficha():
                    if len(pila_destino) > 1:
                        continue
                movimiento = [('bar', destino)]
                if self._validar_movimiento_con_reglas(jugador, movimiento,
                                                       dados_disponibles.copy()):
                    return True
            return False
        for pos in range(24):
            posicion = self.__board__.get_posiciones(pos)
            if posicion and posicion[-1].get_simbolo() == jugador.get_ficha():
                for dado in set(dados_disponibles):
                    if self._verificar_movimiento_desde_posicion(jugador, pos, dado,
                                                                 dados_disponibles.copy()):
                        return True
        return False

    def _validar_movimiento_con_reglas(self, jugador, movimiento, dados_disponibles):
        """
        Valida un movimiento con las reglas del juego.

        Args:
            jugador: instancia del jugador
            movimiento: lista con tupla de movimiento
            dados_disponibles: lista de dados disponibles

        Returns:
            bool: True si el movimiento es válido
        """
        try:
            for regla in self.__reglas__:
                regla(jugador, movimiento, dados_disponibles.copy(), self.__board__)
            return True
        except (MovimientoInvalidoError, ValueError, TypeError):
            return False

    def _verificar_movimiento_desde_posicion(self, jugador, pos, dado, dados_disponibles):
        """
        Verifica si hay un movimiento legal desde una posición con un dado específico.

        Args:
            jugador: instancia del jugador
            pos: posición de origen
            dado: valor del dado
            dados_disponibles: lista de dados disponibles

        Returns:
            bool: True si hay un movimiento legal
        """
        destino = pos + dado if jugador.get_ficha() == 'O' else pos - dado
        es_movimiento_valido = False

        if 0 <= destino < 24:
            pila_destino = self.__board__.get_posiciones(destino)
            posicion_bloqueada = (pila_destino and
                                pila_destino[-1].get_simbolo() != jugador.get_ficha() and
                                len(pila_destino) > 1)

            if not posicion_bloqueada:
                movimiento = [(pos, destino)]
                es_movimiento_valido = self._validar_movimiento_con_reglas(
                    jugador, movimiento, dados_disponibles.copy()
                )
        else:
            puede_bearing_off = ((jugador.get_ficha() == 'O' and destino >= 24) or
                               (jugador.get_ficha() == 'X' and destino < 0))

            if puede_bearing_off and self.__board__.puede_sacar(jugador):
                distancia_exacta = 24 - pos if jugador.get_ficha() == 'O' else pos + 1
                if dado >= distancia_exacta:
                    movimiento = [(pos, 'fuera')]
                    es_movimiento_valido = self._validar_movimiento_con_reglas(
                        jugador, movimiento, dados_disponibles.copy()
                    )
        return es_movimiento_valido

    def _tiene_fichas_mas_atras(self, jugador, posicion):
        """
        Verifica si el jugador tiene fichas en posiciones más alejadas del objetivo.
        Args:
            jugador: instancia del jugador
            posicion: posición desde donde se quiere sacar         
        Returns:
            bool: True si hay fichas más atrás
        """
        if jugador.get_ficha() == 'O':
            for pos in range(18, posicion):
                pila = self.__board__.get_posiciones(pos)
                if pila and pila[-1].get_simbolo() == 'O':
                    return True
        else:
            for pos in range(posicion + 1, 6):
                pila = self.__board__.get_posiciones(pos)
                if pila and pila[-1].get_simbolo() == 'X':
                    return True
        return False

    def parsear_movimiento(self, texto):
        """
        Convierte una entrada de texto en un movimiento válido.
        
        Args:
            texto: string con el movimiento
            
        Returns:
            dict con:
                - "valido": bool
                - "movimiento": tuple (desde, hasta) si es válido
                - "error": str con mensaje de error si no es válido
        """
        texto = texto.strip().lower()
        if '-' in texto:
            partes = texto.split('-')
        else:
            partes = texto.split()
        if len(partes) != 2:
            return {
                "valido": False,
                "error": "Formato inválido. Use: 'desde hasta' o 'desde-hasta'"
            }
        desde_str, hasta_str = partes[0].strip(), partes[1].strip()
        if desde_str == "bar":
            desde = "bar"
        else:
            try:
                desde = int(desde_str)
            except ValueError:
                return {
                    "valido": False,
                    "error": f"Posición de origen inválida: {desde_str}"
                }
        if hasta_str == "fuera":
            hasta = "fuera"
        else:
            try:
                hasta = int(hasta_str)
            except ValueError:
                return {
                    "valido": False,
                    "error": f"Posición de destino inválida: {hasta_str}"
                }
        return {
            "valido": True,
            "movimiento": (desde, hasta)
        }

    def parsear_multiples_movimientos(self, entrada):
        """
        Parsea múltiples movimientos separados por comas.
        
        Args:
            entrada: string con uno o más movimientos
    
        Returns:
            dict con:
                - "valido": bool
                - "movimientos": lista de tuplas si es válido
                - "errores": lista de strings con errores
        """
        if not entrada or not entrada.strip():
            return {
                "valido": False,
                "errores": ["No se ingresaron movimientos"]
            }
        movimientos = []
        errores = []
        for mov_str in entrada.split(','):
            resultado = self.parsear_movimiento(mov_str)
            if resultado["valido"]:
                movimientos.append(resultado["movimiento"])
            else:
                errores.append(f"'{mov_str.strip()}': {resultado['error']}")
        if errores:
            return {
                "valido": False,
                "errores": errores
            }
        return {
            "valido": True,
            "movimientos": movimientos
        }
