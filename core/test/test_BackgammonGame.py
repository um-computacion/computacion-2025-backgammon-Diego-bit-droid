import unittest
from core.clases.backgammonGame import BackgammonGame
from core.clases.board import Board
from core.clases.dice import Dice
from core.clases.player import Player
from core.clases.excepciones import JuegoNoInicializadoError, SinMovimientosDisponiblesError

class TestBackgammonGameIntegrado(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")
        self.game = BackgammonGame(self.board, self.dice, self.jugador1, self.jugador2)
        self.game._BackgammonGame__turno__ = 1
        self.game._BackgammonGame__movimientos_restantes__ = 2

    def test_estado_jugador(self):
        estado = self.jugador1.estado_jugador(self.board)
        self.assertEqual(estado["nombre"], "player1")
        self.assertEqual(estado["ficha"], "X")
        self.assertEqual(estado["total"], 15)

    def test_get_fichas_en_bar(self):
        self.board.set_bar("player1", 3)
        self.assertEqual(self.jugador1.fichas_en_bar(self.board), 3)

    def test_get_fichas_sacadas(self):
        self.board.set_fuera("player1", 5)
        self.assertEqual(self.jugador1.fichas_sacadas(self.board), 5)

    def test_get_fichas_en_tablero(self):
        total = self.jugador1.fichas_en_tablero(self.board)
        self.assertEqual(total, 15)

    def test_mover_ficha_sin_movimientos(self):
        self.game._BackgammonGame__turno__ = 1
        self.game._BackgammonGame__movimientos_restantes__ = 0
        with self.assertRaises(SinMovimientosDisponiblesError):
            self.game.mover_ficha([(0, 1)], 2, 3)


    def test_hay_ganador_true(self):
        self.board.set_fuera("player1", 15)
        self.assertTrue(self.game.hay_ganador())

    def test_hay_ganador_false(self):
        self.board.set_fuera("player1", 10)
        self.board.set_fuera("player2", 14)
        self.assertFalse(self.game.hay_ganador())
if __name__ == '__main__':
    unittest.main()