import unittest
from core.clases.player import Player
from core.clases.backgammonGame import BackgammonGame

class TestBackgammonGame(unittest.TestCase):

    def test_registro_de_jugadores(self):
        # verifica que los jugadores se registran correctamente y se accede por nombre
        j1 = Player("Diego", "X")
        j2 = Player("Lucia", "O")
        game = BackgammonGame()
        game.registrar_jugadores(j1, j2)

        self.assertIs(game.get_jugador_por_nombre("Diego"), j1)
        self.assertIs(game.get_jugador_por_nombre("Lucia"), j2)
        self.assertEqual(j1.get_ficha(), "X")
        self.assertEqual(j2.get_ficha(), "O")

    def test_get_tablero(self):
        # verifica que el tablero se puede obtener sin errores y contiene las claves esperadas
        game = BackgammonGame()
        estado = game.get_tablero()

        self.assertIn("posiciones", estado)
        self.assertIn("bar", estado)
        self.assertIn("fuera", estado)

    def test_quien_empieza_valido(self):
        # verifica que quien_empieza devuelve 1 o 2 segun el jugador que gana el sorteo
        game = BackgammonGame()
        game.registrar_jugadores(Player("A", "X"), Player("B", "O"))
        resultado = game.quien_empieza()
        self.assertIn(resultado, [1, 2])

    def test_estado_turno_inicial(self):
        # verifica que el turno inicial corresponde al jugador que gano el sorteo
        j1 = Player("A", "X")
        j2 = Player("B", "O")
        game = BackgammonGame()
        game.registrar_jugadores(j1, j2)
        quien = game.quien_empieza()
        actual = game.get_jugador_actual()
        esperado = j1 if quien == 1 else j2
        self.assertEqual(actual, esperado)

    def test_lanzar_dados_valores_validos(self):
        # verifica que lanzar_dados devuelve dos valores entre 1 y 6
        game = BackgammonGame()
        game.registrar_jugadores(Player("A", "X"), Player("B", "O"))
        game.quien_empieza()
        dado1, dado2 = game.lanzar_dados()
        self.assertIn(dado1, range(1, 7))
        self.assertIn(dado2, range(1, 7))

    def test_cambiar_turno_alterna_jugador(self):
        # verifica que cambiar_turno alterna correctamente entre jugador1 y jugador2
        j1 = Player("A", "X")
        j2 = Player("B", "O")
        game = BackgammonGame()
        game.registrar_jugadores(j1, j2)
        game.quien_empieza()
        actual = game.get_jugador_actual()
        game.cambiar_turno()
        nuevo = game.get_jugador_actual()
        self.assertNotEqual(actual, nuevo)

    def test_mover_ficha_valida(self):
        # verifica que mover_ficha funciona con una ficha valida del jugador actual
        j1 = Player("A", "X")
        j2 = Player("B", "O")
        game = BackgammonGame()
        game.registrar_jugadores(j1, j2)
        game.quien_empieza()
        dado1, dado2 = game.lanzar_dados()
        jugador = game.get_jugador_actual()
        ficha = jugador.get_ficha()

        tablero = game.get_tablero()["posiciones"]
        origen = None
        for i, pila in enumerate(tablero):
            if pila and pila[-1].ficha == ficha:
                origen = i
                break

        if origen is not None:
            destino = origen + dado1 if ficha == "X" else origen - dado1
            movimientos = [(origen, destino)]
            resultado = game.mover_ficha(movimientos, dado1, dado2)
            self.assertIn(True, resultado["resultados"])
        else:
            self.assertTrue(True)  # no hay fichas del jugador actual en el tablero

if __name__ == "__main__":
    unittest.main()