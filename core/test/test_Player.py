from core.clases.player import Player
from core.clases.checker import Checker
from core.clases.board import Board
import unittest

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("player1", "X")
        self.player2 = Player("player2", "O")
        self.board = Board()

        # Setear posiciones
        self.board.set_posiciones(0, [Checker("X")])
        self.board.set_posiciones(1, [])
        self.board.set_posiciones(2, [Checker("O")])
        self.board.set_posiciones(3, [Checker("X")])

        # Setear bar y fuera
        self.board.set_bar("player1", 2)
        self.board.set_fuera("player1", 3)
    def test_fichas_en_bar(self):
        self.assertEqual(self.player1.fichas_en_bar(self.board), 2)

    def test_fichas_sacadas(self):
        self.assertEqual(self.player1.fichas_sacadas(self.board), 3)
    def test_estado_jugador(self):
        estado1 = self.player1.estado_jugador(self.board)
        self.assertEqual(estado1["en_tablero"], 15)
        self.assertEqual(estado1["en_bar"], 2)
        self.assertEqual(estado1["sacadas"], 3)
        self.assertEqual(estado1["total"], 20)
if __name__ == "__main__":
    unittest.main()