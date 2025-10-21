"""
Módulo de pruebas unitarias para la clase Dice.
"""
import unittest
from core.clases.dice import Dice


class TestDice(unittest.TestCase):
    """Clase de pruebas para validar el comportamiento de la clase Dice."""

    def test_valores_en_rango(self):
        """Verifica que los valores de los dados estén en el rango válido (1-6)."""
        dice = Dice()
        for _ in range(100):
            dado1, dado2 = dice.lanzar_dados()
            self.assertIn(dado1, range(1, 7))
            self.assertIn(dado2, range(1, 7))

    def test_get_valores(self):
        """
        Verifica que el método get_valores devuelva correctamente los valores
        actuales de los dados sin realizar una nueva tirada.
        Se inicializan manualmente los valores internos y se comprueba que
        el método retorna la tupla esperada.
        """
        dados = Dice()
        dados.__dado1__ = 4
        dados.__dado2__ = 6
        resultado = dados.get_valores()
        self.assertEqual(resultado, (4, 6))
if __name__ == "__main__":
    unittest.main()
