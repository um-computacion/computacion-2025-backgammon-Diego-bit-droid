from core.clases.BackgammonGame import BackgammonGame
def test_quien_empieza_jugador1(self):
    game = BackgammonGame()
    game.lanzar_dado = lambda: 6  # Jugador 1
    game.lanzar_dado = lambda: 3  # Jugador 2 (esto sobrescribe el anterior, ver abajo para mejora)
    result = game.quien_empieza()
    self.assertEqual(game._BackgammonGame__turno__, 1)
    self.assertTrue(result)

def test_quien_empieza_jugador2(self):
    game = BackgammonGame()
    game.lanzar_dado = lambda: 2  # Jugador 1
    game.lanzar_dado = lambda: 5  # Jugador 2
    result = game.quien_empieza()
    self.assertEqual(game._BackgammonGame__turno__, 2)
    self.assertTrue(result)