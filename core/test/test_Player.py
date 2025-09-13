import unittest
from core.clases.player import Player
from core.clases.checker import Checker

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player1 = Player("player1", "X")
        self.player2 = Player("player2", "O")

        # posiciones simuladas del tablero
        self.posiciones = [[] for _ in range(24)]
        self.posiciones[0] = [Checker("X"), Checker("X")]
        self.posiciones[5] = [Checker("O"), Checker("O"), Checker("O")]
        self.posiciones[11] = [Checker("X")]
        self.posiciones[12] = [Checker("O")]

        # bar y fuera simulados
        self.bar = {"player1": 2, "player2": 1}
        self.fuera = {"player1": 3, "player2": 0}

    def test_get_nombre(self):
        self.assertEqual(self.player1.get_nombre(), "player1")
        self.assertEqual(self.player2.get_nombre(), "player2")

    def test_get_ficha(self):
        self.assertEqual(self.player1.get_ficha(), "X")
        self.assertEqual(self.player2.get_ficha(), "O")

    def test_fichas_en_tablero(self):
        self.assertEqual(self.player1.fichas_en_tablero(self.posiciones), 3)
        self.assertEqual(self.player2.fichas_en_tablero(self.posiciones), 4)

    def test_fichas_en_bar(self):
        self.assertEqual(self.player1.fichas_en_bar(self.bar), 2)
        self.assertEqual(self.player2.fichas_en_bar(self.bar), 1)

    def test_fichas_sacadas(self):
        self.assertEqual(self.player1.fichas_sacadas(self.fuera), 3)
        self.assertEqual(self.player2.fichas_sacadas(self.fuera), 0)

    def test_estado_jugador(self):
        estado1 = self.player1.estado_jugador(self.posiciones, self.bar, self.fuera)
        estado2 = self.player2.estado_jugador(self.posiciones, self.bar, self.fuera)

        self.assertEqual(estado1["nombre"], "player1")
        self.assertEqual(estado1["ficha"], "X")
        self.assertEqual(estado1["en_tablero"], 3)
        self.assertEqual(estado1["en_bar"], 2)
        self.assertEqual(estado1["sacadas"], 3)
        self.assertEqual(estado1["total"], 8)

        self.assertEqual(estado2["nombre"], "player2")
        self.assertEqual(estado2["ficha"], "O")
        self.assertEqual(estado2["en_tablero"], 4)
        self.assertEqual(estado2["en_bar"], 1)
        self.assertEqual(estado2["sacadas"], 0)
        self.assertEqual(estado2["total"], 5)

if __name__ == "__main__":
    unittest.main()