import unittest
from core.clases.dice import Dice  

class TestDice(unittest.TestCase):

    def test_valores_en_rango(self):
        dice = Dice()
        for _ in range(100):  
            dado1, dado2 = dice.lanzar_dados()
            self.assertIn(dado1, range(1, 7))
            self.assertIn(dado2, range(1, 7))