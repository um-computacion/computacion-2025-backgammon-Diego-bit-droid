import unittest
from core.clases.backgammonGame import BackgammonGame
from core.clases.player import Player
from core.clases.dice import Dice
from core.clases.checker import Checker
from core.clases.board import Board

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")
        self.game = BackgammonGame(self.board, self.dice, self.jugador1, self.jugador2)
        self.game.quien_empieza()
    def test_quien_empieza(self):
        turno = self.game.quien_empieza()
        self.assertIn(turno, [1, 2])

    def test_movimientos_totales_dobles(self):
        movimientos = self.game.get_movimientos_totales(3, 3)
        self.assertEqual(movimientos, [3, 3, 3, 3])

    def test_movimientos_totales_distintos(self):
        movimientos = self.game.get_movimientos_totales(2, 5)
        self.assertEqual(movimientos, [2, 5])

    def test_mover_ficha_desde_bar_obligatorio(self):
        self.game._BackgammonGame__turno__ = 1
        self.board.set_bar("player1", 1)
        movimientos = [("bar", 3), (0, 5)]  # segundo movimiento inválido
        resultado = self.game.mover_ficha(movimientos, 3, 5)
        self.assertFalse(resultado["resultados"][1])
        self.assertIn("bar", resultado["log"][0])

    def test_no_puede_sacar_si_no_esta_en_cuadrante(self):
        self.game._BackgammonGame__turno__ = 1
        movimientos = [(0, "fuera")]
        resultado = self.game.mover_ficha(movimientos, 6, 6)
        self.assertFalse(resultado["resultados"][0])
        self.assertIn("cuadrante final", resultado["log"][0])

    def test_cambiar_turno(self):
        self.game._BackgammonGame__turno__ = 1
        jugador_actual = self.game.get_jugador_actual()
        self.game.cambiar_turno()
        nuevo_jugador = self.game.get_jugador_actual()
        self.assertNotEqual(jugador_actual.get_nombre(), nuevo_jugador.get_nombre())

    def test_hay_ganador_true(self):
        self.board.set_fuera("player1", 15)
        self.assertTrue(self.game.hay_ganador())

    def test_hay_ganador_false(self):
        self.board.set_fuera("player1", 10)
        self.board.set_fuera("player2", 12)
        self.assertFalse(self.game.hay_ganador())
    def test_estado_turno(self):
        self.game._BackgammonGame__turno__ = 2
        try:
            self.game.estado_turno()
        except Exception as e:
            self.fail(f"estado_turno lanzó una excepción: {e}")    
    def test_get_jugador_por_nombre(self):
        jugador = self.game.get_jugador_por_nombre("player1")
        self.assertEqual(jugador.get_nombre(), "player1")
        self.assertIsNone(self.game.get_jugador_por_nombre("inexistente"))
    def test_get_tablero(self):
        tablero = self.game.get_tablero()
        self.assertIn("posiciones", tablero)
        self.assertIn("bar", tablero)
        self.assertIn("fuera", tablero)
    def test_get_fichas_en_bar(self):
        self.board.set_bar("player1", 3)
        cantidad = self.game.get_fichas_en_bar(self.jugador1)
        self.assertEqual(cantidad, 3)
    def test_get_fichas_sacadas(self):
        self.board.set_fuera("player2", 5)
        cantidad = self.game.get_fichas_sacadas(self.jugador2)
        self.assertEqual(cantidad, 5)

if __name__ == '__main__':
    unittest.main()
    