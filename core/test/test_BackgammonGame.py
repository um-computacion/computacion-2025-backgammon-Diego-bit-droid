import unittest
from core.clases.player import Player
from core.clases.backgammonGame import BackgammonGame

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
    
    def test_quien_empieza_valido(self):
        game = BackgammonGame()
        resultado = game.quien_empieza()
        self.assertIn(resultado, [1, 2])
  

    def test_quien_empieza_con_empate(self):
        game = BackgammonGame()
        resultado = game.quien_empieza()
        self.assertIn(resultado, [1, 2])