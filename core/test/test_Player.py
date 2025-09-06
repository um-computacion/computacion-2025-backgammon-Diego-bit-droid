import unittest
from core.clases.Player import Player
class TestPlayer(unittest.TestCase):
    def test_get_nombre_y_ficha(self):
        jugador = Player("Diego", "X")

        try:
            nombre = jugador.get_nombre()
            ficha = jugador.get_ficha()
        except Exception as e:
            self.fail(f"get_nombre() o get_ficha() falló: {e}")

        self.assertEqual(nombre, "Diego")
        self.assertEqual(ficha, "X")

if __name__ == '__main__':
    unittest.main()