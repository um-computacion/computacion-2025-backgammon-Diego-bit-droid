import unittest
from core.clases.BackgammonGame import BackgammonGame

class TestBackgammonGame(unittest.TestCase):

    def test_quien_empieza_jugador1(self):
        game = BackgammonGame()
        valores = iter([6, 3])

        def lanzar_dado():
            return next(valores)


        game.lanzar_dado = lanzar_dado
        turno = game.quien_empieza()
        self.assertEqual(turno, 1)

    def test_quien_empieza_jugador2(self):
        game = BackgammonGame()
        valores = iter([2, 5])

        def lanzar_dado():
            return next(valores)

        game.lanzar_dado = lanzar_dado
        turno = game.quien_empieza()
        self.assertEqual(turno, 2)

    def test_quien_empieza_con_empate_y_reintento(self):
        game = BackgammonGame()
        valores = iter([4, 4, 2, 6])

        def lanzar_dado():
            return next(valores)

        game.lanzar_dado = lanzar_dado
        turno = game.quien_empieza()
        self.assertEqual(turno, 2)
