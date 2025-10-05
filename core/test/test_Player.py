from core.clases.player import Player
from core.clases.checker import Checker
import unittest

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("player1", "X")
        self.player2 = Player("player2", "O")
        self.posiciones = [[Checker("X")], [], [Checker("O")], [Checker("X")]]
        self.bar = {"player1": 2, "player2": 0}
        self.fuera = {"player1": 3, "player2": 0}

    def test_fichas_en_bar(self):
        self.assertEqual(self.player1.fichas_en_bar(self.bar), 2)

    def test_fichas_sacadas(self):
        self.assertEqual(self.player1.fichas_sacadas(self.fuera), 3)

    def test_estado_jugador(self):
        estado1 = self.player1.estado_jugador(self.posiciones, self.bar, self.fuera)
        self.assertEqual(estado1["en_tablero"], 2)
        self.assertEqual(estado1["en_bar"], 2)
        self.assertEqual(estado1["sacadas"], 3)
        self.assertEqual(estado1["total"], 7)
if __name__ == "__main__":
    unittest.main()