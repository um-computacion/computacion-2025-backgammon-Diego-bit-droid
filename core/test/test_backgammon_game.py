"""
Pruebas integradas para BackgammonGame: validan lógica de turnos,
movimientos, reglas y estado.
"""
import unittest
from core.clases.backgammon_game import BackgammonGame
from core.clases.board import Board
from core.clases.dice import Dice
from core.clases.player import Player
from core.clases.excepciones import (
    JuegoNoInicializadoError,
    SinMovimientosDisponiblesError,
    ValorDadoInvalidoError,
    TurnoJugadorInvalidoError
)

from core.clases.validaciones import MovimientoInvalidoError


def regla_invalida(_jugador, _movimientos, _dados, _board):
    """Regla de prueba que siempre invalida el movimiento."""
    raise MovimientoInvalidoError("Movimiento inválido por regla")


class TestBackgammonGameIntegrado(unittest.TestCase):
    """
    Suite de pruebas integradas para BackgammonGame, cubriendo lógica
    completa de juego y validaciones.
    """
    # pylint: disable=too-many-public-methods

    def setUp(self):
        """
        Inicializa el entorno de prueba creando el tablero, dados,
        jugadores y la instancia del juego.
        También fuerza el turno y los movimientos restantes para
        simular una partida en curso.
        """
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")
        self.game = BackgammonGame(
            self.board, self.dice, self.jugador1, self.jugador2
        )
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 2

    def test_fichas_en_tablero(self):
        """
        Simula un estado del tablero con fichas en posiciones específicas.
        No realiza aserciones; sirve como base para pruebas de estado
        visual o lógica de conteo.
        """
        self.game.__board__.get_tablero = lambda: {
            "posiciones": [
                ["player1"], [], ["player2"], ["player1", "player1"]
            ],
            "bar": {"player1": 0, "player2": 0},
            "fuera": {"player1": 0, "player2": 0}
        }

    def test_fichas_en_bar(self):
        """
        Simula fichas en el bar y verifica que get_fichas_en_bar
        retorne correctamente la cantidad.
        """
        self.game.__board__.get_tablero = lambda: {
            "posiciones": [],
            "bar": {"player1": 2, "player2": 1},
            "fuera": {"player1": 0, "player2": 0}
        }
        self.jugador1.fichas_en_bar = lambda bar: bar["player1"]
        fichas = self.game.get_fichas_en_bar(self.jugador1)
        self.assertEqual(fichas, 2)

    def test_fichas_sacadas(self):
        """
        Simula fichas fuera del tablero y verifica que get_fichas_sacadas
        retorne correctamente la cantidad.
        """
        self.game.__board__.get_tablero = lambda: {
            "posiciones": [],
            "bar": {"player1": 0, "player2": 0},
            "fuera": {"player1": 7, "player2": 4}
        }
        self.jugador1.fichas_sacadas = lambda fuera: fuera["player1"]
        fichas = self.game.get_fichas_sacadas(self.jugador1)
        self.assertEqual(fichas, 7)

    def test_estado_jugador(self):
        """
        Verifica que el estado del jugador incluya nombre, ficha
        y total de fichas (15).
        """
        estado = self.jugador1.estado_jugador(self.board)
        self.assertEqual(estado["nombre"], "player1")
        self.assertEqual(estado["ficha"], "X")
        self.assertEqual(estado["total"], 15)

    def test_get_fichas_en_bar(self):
        """
        Establece fichas en el bar y verifica que el método del jugador
        las retorne correctamente.
        """
        self.board.set_bar("player1", 3)
        self.assertEqual(self.jugador1.fichas_en_bar(self.board), 3)

    def test_get_fichas_sacadas(self):
        """
        Establece fichas fuera del tablero y verifica que el método
        del jugador las retorne correctamente.
        """
        self.board.set_fuera("player1", 5)
        self.assertEqual(self.jugador1.fichas_sacadas(self.board), 5)

    def test_get_fichas_en_tablero(self):
        """
        Verifica que el jugador tenga 15 fichas en el tablero al
        inicio de la partida.
        """
        total = self.jugador1.fichas_en_tablero(self.board)
        self.assertEqual(total, 15)

    def test_hay_ganador_true(self):
        """
        Simula que el jugador ha sacado 15 fichas y verifica que
        el juego detecte la victoria.
        """
        self.board.set_fuera("player1", 15)
        self.assertTrue(self.game.hay_ganador())

    def test_hay_ganador_false(self):
        """
        Simula que ningún jugador ha sacado 15 fichas y verifica
        que no haya ganador.
        """
        self.board.set_fuera("player1", 10)
        self.board.set_fuera("player2", 14)
        self.assertFalse(self.game.hay_ganador())

    def test_calcular_movimientos_totales_normal(self):
        """
        Verifica que el cálculo de movimientos con dados distintos
        retorne ambos valores como lista.
        """
        movimientos = self.game.calcular_movimientos_totales(3, 5)
        self.assertEqual(movimientos, [3, 5])

    def test_calcular_movimientos_totales_dobles(self):
        """
        Verifica que el cálculo de movimientos con dados iguales
        retorne cuatro repeticiones del mismo valor.
        """
        movimientos = self.game.calcular_movimientos_totales(4, 4)
        self.assertEqual(movimientos, [4, 4, 4, 4])

    def test_calcular_movimientos_totales_dado_invalido(self):
        """
        Verifica que se lance ValorDadoInvalidoError si algún dado
        está fuera del rango permitido.
        """
        with self.assertRaises(ValorDadoInvalidoError):
            self.game.calcular_movimientos_totales(0, 5)

    def test_get_jugador_por_nombre_valido(self):
        """
        Verifica que get_jugador_por_nombre retorne correctamente
        el jugador solicitado.
        """
        jugador = self.game.get_jugador_por_nombre("player1")
        self.assertEqual(jugador.get_ficha(), "X")

    def test_get_jugador_por_nombre_invalido_primera_vez(self):
        """
        Verifica que se lance TurnoJugadorInvalidoError si el nombre
        del jugador no existe.
        """
        with self.assertRaises(TurnoJugadorInvalidoError):
            self.game.get_jugador_por_nombre("desconocido")

    def test_mostrar_movimientos_disponibles(self):
        """
        Ejecuta mostrar_movimientos_disponibles con dados válidos.
        No realiza aserciones; valida que no se produzcan errores.
        """
        self.game.mostrar_movimientos_disponibles(2, 5)

    def test_quien_empieza_asigna_turno(self):
        """
        Verifica que quien_empieza retorne 1 o 2 y que el turno
        interno se actualice correctamente.
        """
        self.game.__turno__ = 0
        turno = self.game.quien_empieza()
        self.assertIn(turno, [1, 2])
        self.assertIn(self.game.__turno__, [1, 2])

    def test_quien_empieza_asigna_turno_jugador_uno(self):
        """
        Fuerza el turno inicial para jugador uno y verifica que
        quien_empieza lo asigne correctamente.
        """
        self.game.__turno__ = 0
        turno = 0
        while turno != 1:
            turno = self.game.quien_empieza()
        self.assertEqual(turno, 1)

    def test_quien_empieza_asigna_turno_jugador_dos(self):
        """
        Fuerza el turno inicial para jugador dos y verifica que
        quien_empieza lo asigne correctamente.
        """
        self.game.__turno__ = 0
        turno = 0
        while turno != 2:
            turno = self.game.quien_empieza()
        self.assertEqual(turno, 2)

    def test_iniciar_partida_valido(self):
        """
        Ejecuta iniciar_partida y verifica que el turno se asigne
        correctamente (1 o 2).
        """
        self.game.__turno__ = 0
        self.game.iniciar_partida()
        self.assertIn(self.game.__turno__, [1, 2])

    def test_get_movimientos_totales_valido(self):
        """
        Verifica que get_movimientos_totales retorne correctamente
        los valores de los dados como lista.
        """
        movimientos = self.game.get_movimientos_totales(3, 6)
        self.assertEqual(movimientos, [3, 6])

    def test_lanzar_dados_valido(self):
        """
        Lanza los dados y verifica que movimientos_restantes se
        asigne correctamente: 4 si hay dobles, 2 si son distintos.
        """
        self.game.__turno__ = 1
        dado1, dado2 = self.game.lanzar_dados()
        esperados = 4 if dado1 == dado2 else 2
        self.assertEqual(
            self.game.__movimientos_restantes__, esperados
        )

    def test_get_jugador_actual_valido(self):
        """
        Fuerza el turno a jugador dos y verifica que get_jugador_actual
        retorne el jugador correcto.
        """
        self.game.__turno__ = 2
        jugador = self.game.get_jugador_actual()
        self.assertEqual(jugador.get_nombre(), "player2")

    def test_estado_turno_ejecucion(self):
        """
        Fuerza el turno a jugador uno y ejecuta estado_turno.
        Verifica que el método se ejecute sin errores y muestre
        el estado actual del turno.
        """
        self.game.__turno__ = 1
        self.game.estado_turno()

    def test_cambiar_turno_de_2_a_1(self):
        """
        Inicializa la partida, fuerza el turno a jugador dos y
        ejecuta cambiar_turno. Verifica que el turno se actualice
        correctamente a jugador uno.
        """
        self.game.__turno__ = 0
        self.game.iniciar_partida()

        self.game.__turno__ = 2
        self.game.cambiar_turno()
        self.assertEqual(self.game.__turno__, 1)

    def test_dado_fuera_de_rango_lanza_error(self):
        """
        Verifica que calcular_movimientos_totales lance
        ValorDadoInvalidoError cuando se proporciona un dado fuera
        del rango permitido (0).
        """
        with self.assertRaises(ValorDadoInvalidoError):
            self.game.calcular_movimientos_totales(0, 5)

    def test_get_jugador_por_nombre_invalido_segunda_vez(self):
        """
        Verifica que get_jugador_por_nombre lance
        TurnoJugadorInvalidoError cuando se solicita un jugador
        con nombre inexistente.
        """
        with self.assertRaises(TurnoJugadorInvalidoError):
            self.game.get_jugador_por_nombre("inexistente")

    def test_get_jugador_actual_sin_turno_lanza_error(self):
        """
        Verifica que get_jugador_actual lance JuegoNoInicializadoError
        cuando el turno no ha sido asignado.
        """
        self.game.__turno__ = 0
        with self.assertRaises(JuegoNoInicializadoError):
            self.game.get_jugador_actual()

    def test_cambiar_turno_sin_turno_lanza_error(self):
        """
        Verifica que cambiar_turno lance JuegoNoInicializadoError
        cuando el turno no ha sido asignado.
        """
        self.game.__turno__ = 0
        with self.assertRaises(JuegoNoInicializadoError):
            self.game.cambiar_turno()

    def test_mover_ficha_sin_movimientos_lanza_error(self):
        """
        Fuerza turno válido pero sin movimientos restantes.
        Verifica que mover_ficha lance SinMovimientosDisponiblesError.
        """
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 0
        with self.assertRaises(SinMovimientosDisponiblesError):
            self.game.mover_ficha([(0, 1)], 3, 4)

    def test_hay_ganador_false_verificacion(self):
        """
        Verifica que hay_ganador retorne False cuando ningún jugador
        ha sacado 15 fichas.
        """
        self.assertFalse(self.game.hay_ganador())

    def test_mover_ficha_valida(self):
        """
        Simula un movimiento válido en el tablero.
        Verifica que los resultados, dados usados y log sean correctos.
        """
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 2
        self.board.mover_ficha = lambda jugador, movimientos, dados: {
            "resultados": [True],
            "dados_usados": [3],
            "dados_restantes": [4],
            "log": ["Movimiento exitoso"]
        }
        resultado = self.game.mover_ficha([(0, 1)], 3, 4)
        self.assertTrue(all(resultado["resultados"]))
        self.assertEqual(resultado["dados_usados"], [3])
        self.assertEqual(resultado["dados_restantes"], [4])
        self.assertIn("Movimiento exitoso", resultado["log"])

    def test_mover_ficha_agota_movimientos_y_cambia_turno(self):
        """
        Simula un movimiento que agota los movimientos restantes.
        Verifica que el turno se actualice automáticamente al
        jugador contrario.
        """
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 1
        self.board.mover_ficha = lambda jugador, movimientos, dados: {
            "resultados": [True],
            "dados_usados": [3],
            "dados_restantes": [],
            "log": ["Movimiento exitoso"]
        }
        self.game.mover_ficha([(0, 1)], 3, 4)
        self.assertEqual(self.game.__turno__, 2)

    def test_get_jugador_por_nombre_valido_player2(self):
        """
        Verifica que get_jugador_por_nombre retorne correctamente
        el jugador dos y que su ficha sea 'O'.
        """
        jugador = self.game.get_jugador_por_nombre("player2")
        self.assertEqual(jugador.get_ficha(), "O")

    def test_mover_ficha_regla_invalida(self):
        """
        Simula una regla personalizada que invalida el movimiento.
        Verifica que el resultado sea False, sin dados usados, y que
        el log contenga el mensaje de error.
        """
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 2
        self.game.__reglas__ = [regla_invalida]
        resultado = self.game.mover_ficha([(0, 1)], 3, 4)
        self.assertEqual(resultado["resultados"], [False])
        self.assertEqual(resultado["dados_usados"], [])
        self.assertIn("Movimiento inválido por regla", resultado["log"][0])


if __name__ == '__main__':
    unittest.main()
