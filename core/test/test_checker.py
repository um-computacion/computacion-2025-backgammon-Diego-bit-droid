import unittest
from core.clases.Player import Player
from core.clases.BackgammonGame import BackgammonGame
from core.clases.Checker import Checker

class TestChecker(unittest.TestCase):
    def test_get_nombre(self):
        jugador1 = Player("Diego", "X")
        jugador2 = Player("Bot", "O")
        backgammon = BackgammonGame()
        backgammon.registrar_jugadores(jugador1, jugador2)
        ficha = Checker("Diego", backgammon)

        try:
            nombre = ficha.get_nombre()
        except Exception as e:
            self.fail(f"get_nombre() falló: {e}")

        self.assertEqual(nombre, "Diego")

    def test_get_ficha(self):
        jugador1 = Player("Diego", "X")
        jugador2 = Player("Bot", "O")
        backgammon = BackgammonGame()
        backgammon.registrar_jugadores(jugador1, jugador2)
        ficha = Checker("Bot", backgammon)

        try:
            simbolo = ficha.get_ficha()
        except Exception as e:
            self.fail(f"get_ficha() falló: {e}")

        self.assertEqual(simbolo, "O")

if __name__ == '__main__':
    unittest.main()
