
from core.clases.player import Player
import unittest
from core.clases.board import Board
from core.clases.checker import Checker
from core.clases.validaciones import regla_bar, regla_salida_final, MovimientoInvalidoError

class TestReglasValidacion(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")

    # regla_bar

    def test_regla_bar_lanza_excepcion_si_hay_fichas_en_bar(self):
        self.board.set_bar("player1", 2)
        movimientos = [(5, 7)]  # Movimiento fuera del bar
        dados = [2]

        with self.assertRaises(MovimientoInvalidoError) as contexto:
            regla_bar(self.jugador1, movimientos, dados, self.board)

        self.assertIn("tiene fichas en el bar", contexto.exception.mensaje)

    def test_regla_bar_no_lanza_excepcion_si_mueve_desde_bar(self):
        self.board.set_bar("player1", 2)
        movimientos = [("bar", 3)]
        dados = [3]

        try:
            regla_bar(self.jugador1, movimientos, dados, self.board)
        except MovimientoInvalidoError:
            self.fail("regla_bar lanzó excepción aunque el movimiento era desde el bar")

    # regla_salida_final

    def test_regla_salida_final_lanza_excepcion_si_no_puede_sacar(self):
        self.board.set_posiciones(3, [Checker("X")])  # fuera del cuadrante final
        movimientos = [(3, "fuera")]
        dados = [5]

        with self.assertRaises(MovimientoInvalidoError) as contexto:
            regla_salida_final(self.jugador1, movimientos, dados, self.board)

        self.assertIn("no puede sacar fichas", contexto.exception.mensaje)

    def test_regla_salida_final_no_lanza_excepcion_si_puede_sacar(self):
        # Vaciar todas las posiciones y dejar una ficha en el cuadrante final
        for i in range(24):
            self.board.set_posiciones(i, [])
        self.board.set_posiciones(22, [Checker("X")])  # dentro del cuadrante final
        movimientos = [(22, "fuera")]
        dados = [1]

        try:
            regla_salida_final(self.jugador1, movimientos, dados, self.board)
        except MovimientoInvalidoError:
            self.fail("regla_salida_final lanzó excepción aunque el jugador podía sacar fichas")
