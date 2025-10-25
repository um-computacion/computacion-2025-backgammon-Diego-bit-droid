"""
Pruebas unitarias para la clase Checker del juego Backgammon.
"""
import unittest
from core.clases.checker import Checker


class TestChecker(unittest.TestCase):
    """Suite de pruebas para la clase Checker."""

    def test_simbolo(self):
        """Verifica que el símbolo se guarde y acceda correctamente."""
        ficha_x = Checker("X")
        ficha_o = Checker("O")
        self.assertEqual(ficha_x.get_simbolo(), "X")
        self.assertEqual(ficha_o.get_simbolo(), "O")

    def test_str(self):
        """Verifica que str() devuelva el símbolo correcto."""
        ficha_x = Checker("X")
        ficha_o = Checker("O")
        self.assertEqual(str(ficha_x), "X")
        self.assertEqual(str(ficha_o), "O")

    def test_repr(self):
        """Verifica que repr() devuelva el símbolo correcto."""
        ficha_x = Checker("X")
        ficha_o = Checker("O")
        self.assertEqual(repr(ficha_x), "X")
        self.assertEqual(repr(ficha_o), "O")


if __name__ == "__main__":
    unittest.main()
