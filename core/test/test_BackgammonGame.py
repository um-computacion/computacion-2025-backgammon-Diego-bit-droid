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
       #def test_puede_sacar_si_todas_en_cuadrante(self):
        
if __name__ == '__main__':
    unittest.main()
    