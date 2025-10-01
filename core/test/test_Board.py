import unittest
from core.clases.checker import Checker
from core.clases.player import Player
from core.clases.board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")

    def test_preparar_tablero(self):
        tablero = self.board.get_tablero()["posiciones"]
        self.assertEqual([c.get_simbolo() for c in tablero[0]], ['X', 'X'])
        self.assertEqual([c.get_simbolo() for c in tablero[11]], ['X'] * 5)
        self.assertEqual([c.get_simbolo() for c in tablero[16]], ['X'] * 3)
        self.assertEqual([c.get_simbolo() for c in tablero[18]], ['X'] * 5)
        self.assertEqual([c.get_simbolo() for c in tablero[23]], ['O', 'O'])
        self.assertEqual([c.get_simbolo() for c in tablero[12]], ['O'] * 5)
        self.assertEqual([c.get_simbolo() for c in tablero[7]], ['O'] * 3)
        self.assertEqual([c.get_simbolo() for c in tablero[5]], ['O'] * 5)

    def test_mostrar_board(self):
        try:
            self.board.mostrar_board()
        except Exception as e:
            self.fail(f"mostrar_board() falló: {e}")

    def test_valido_sin_comer(self):
        self.board.set_posiciones(0, [Checker("X")])
        dados = [3, 5]
        resultado = self.board.mover_ficha(self.jugador1, [(0, 3)], dados)
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(resultado["dados_usados"], [3])
        self.assertEqual([c.get_simbolo() for c in self.board.get_posiciones(3)], ["X"])

    def test_valido_con_comer(self):
        self.board.set_posiciones(0, [Checker("X")])
        self.board.set_posiciones(3, [Checker("O")])
        dados = [3, 5]
        resultado = self.board.mover_ficha(self.jugador1, [(0, 3)], dados)
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(self.board.get_bar("player2"), 1)
        self.assertEqual([c.get_simbolo() for c in self.board.get_posiciones(3)], ["X"])
        self.assertIn("Comió ficha enemiga", resultado["log"][0])

    def test_dado_invalido(self):
        self.board.set_posiciones(0, [Checker("X")])
        dados = [3, 5]
        resultado = self.board.mover_ficha(self.jugador1, [(0, 6)], dados)
        self.assertEqual(resultado["resultados"], [False])
        self.assertEqual(resultado["dados_usados"], [])
        self.assertIn("No se puede usar dado 6", resultado["log"][0])

    def test_movimiento_invalido(self):
        self.board.set_posiciones(0, [Checker("X")])
        self.board.validar_movimiento = lambda d, h, j: False
        dados = [3, 5]
        resultado = self.board.mover_ficha(self.jugador1, [(0, 3)], dados)
        self.assertEqual(resultado["resultados"], [False])
        self.assertIn("Movimiento inválido", resultado["log"][0])

    def test_sacar_fuera(self):
        self.board.set_posiciones(22, [Checker("X")])
        dados = [1, 1]
        resultado = self.board.mover_ficha(self.jugador1, [(22, "fuera")], dados)
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(self.board.get_fuera("player1"), 1)
        self.assertIn("sacó ficha", resultado["log"][0])

    def test_entrada_desde_bar(self):
        self.board.set_bar("player1", 1)
        dados = [3, 4]
        resultado = self.board.mover_ficha(self.jugador1, [("bar", 3)], dados)
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(self.board.get_bar("player1"), 0)
        self.assertIn("movió de bar a 3", resultado["log"][0])

if __name__ == "__main__":
    unittest.main()