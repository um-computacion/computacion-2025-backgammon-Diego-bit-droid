import unittest
from core.clases.Player import Player
from core.clases.BackgammonGame import BackgammonGame

class TestBackgammonGame(unittest.TestCase):
    
    def test_registro_de_jugadores(self):
        j1 = Player("Diego", "X")
        j2 = Player("Lucía", "O")
        game = BackgammonGame()
        game.registrar_jugadores(j1, j2)

        self.assertIs(game.get_jugador_por_nombre("Diego"), j1)
        self.assertIs(game.get_jugador_por_nombre("Lucía"), j2)
        self.assertEqual(j1.get_ficha(), "X")
        self.assertEqual(j2.get_ficha(), "O")
    def test_get_tablero(self):
        game = BackgammonGame()
        game.get_tablero()

        try:
            estado = game.get_tablero()
        except Exception as e:
            self.fail(f"get_tablero() falló: {e}")

        self.assertIn("posiciones", estado)
        self.assertIn("bar", estado)
        self.assertIn("fuera", estado)
    

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
