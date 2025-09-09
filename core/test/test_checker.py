import unittest
from core.clases.Checker import Checker

class TestChecker(unittest.TestCase):

    def test_simbolo(self):  # Verificamos que el atributo simbolo se guarda correctamente
        ficha_x = Checker("X")
        ficha_o = Checker("O")
        self.assertEqual(ficha_x.simbolo, "X")
        self.assertEqual(ficha_o.simbolo, "O")

    def test_str(self): # Verificamos que str() devuelve el símbolo correcto
        ficha_x = Checker("X")
        ficha_o = Checker("O")
        self.assertEqual(str(ficha_x), "X")
        self.assertEqual(str(ficha_o), "O")

    def test_repr(self):  # Verificamos que repr() devuelve el símbolo correcto
        ficha_x = Checker("X")
        ficha_o = Checker("O")
        self.assertEqual(repr(ficha_x), "X")
        self.assertEqual(repr(ficha_o), "O")

if __name__ == "__main__":
    unittest.main()