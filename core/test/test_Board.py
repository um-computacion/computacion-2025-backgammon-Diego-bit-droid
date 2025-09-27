import unittest
from core.clases.checker import Checker
from core.clases.player import Player 
from core.clases.board import Board
class TestBoard(unittest.TestCase):
    def test_preparar_tablero(self):
        board = Board()
        ## jugador 1
        self.assertEqual([c.simbolo for c in board.__posiciones__[0]], ['X', 'X'])
        self.assertEqual([c.simbolo for c in board.__posiciones__[11]], ['X', 'X', 'X', 'X', 'X'])
        self.assertEqual([c.simbolo for c in board.__posiciones__[16]], ['X', 'X', 'X'])
        self.assertEqual([c.simbolo for c in board.__posiciones__[18]], ['X', 'X', 'X', 'X', 'X'])

        # jugador 2
        self.assertEqual([c.simbolo for c in board.__posiciones__[23]], ['O', 'O'])
        self.assertEqual([c.simbolo for c in board.__posiciones__[12]], ['O', 'O', 'O', 'O', 'O'])
        self.assertEqual([c.simbolo for c in board.__posiciones__[7]], ['O', 'O', 'O'])
        self.assertEqual([c.simbolo for c in board.__posiciones__[5]], ['O', 'O', 'O', 'O', 'O'])

            
    
    def test_mostrar_board(self):
        board = Board()
        board.preparar_tablero()
        
        try:
            board.mostrar_board()
        except Exception as e:
            self.fail(f"mostrar_board() falló: {e}")

    def test_valido_sin_comer(self):
        board = Board()
        board.__posiciones__[0] = [Checker("X")]
        jugador = Player("jugador1", "X")

        resultado = board.mover_ficha(jugador, [(0, 3)], 3, 5)

        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(resultado["dados_usados"], [3])
        self.assertEqual([c.simbolo for c in board.__posiciones__[3]], ["X"])

    def test_valido_con_comer(self):
        board = Board()
        board.__posiciones__[0] = [Checker("X")]
        board.__posiciones__[3] = [Checker("O")]
        jugador = Player("jugador1", "X")

        resultado = board.mover_ficha(jugador, [(0, 3)], 3, 5)

        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(board.__bar__["jugador2"], 1)
        self.assertEqual([c.simbolo for c in board.__posiciones__[3]], ["X"])
        self.assertIn("Comió ficha enemiga", resultado["log"][0])

    def test_dado_invalido(self):
        board = Board()
        board.__posiciones__[0] = [Checker("X")]
        jugador = Player("jugador1", "X")

        resultado = board.mover_ficha(jugador, [(0, 6)], 3, 5)

        self.assertEqual(resultado["resultados"], [False])
        self.assertEqual(resultado["dados_usados"], [])
        self.assertIn("No se puede usar dado 6", resultado["log"][0])

    def test_movimiento_invalido(self):
        board = Board()
        board.__posiciones__[0] = [Checker("X")]
        jugador = Player("jugador1", "X")
        board.validar_movimiento = lambda d, h, j: False

        resultado = board.mover_ficha(jugador, [(0, 3)], 3, 5)

        self.assertEqual(resultado["resultados"], [False])
        self.assertIn("Movimiento inválido", resultado["log"][0])

    def test_sacar_fuera(self):
        board = Board()
        board.__posiciones__[18] = [Checker("X")]
        jugador = Player("jugador1", "X")

        resultado = board.mover_ficha(jugador, [(18, "fuera")], 6, 6)

        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(board.__fuera__["jugador1"], 1)
        self.assertIn("sacó ficha", resultado["log"][0])

    def test_entrada_desde_bar(self):
        board = Board()
        board.__bar__["jugador1"] = 1
        jugador = Player("jugador1", "X")

        resultado = board.mover_ficha(jugador, [("bar", 3)], 3, 4)

        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(board.__bar__["jugador1"], 0)
        self.assertIn("movió de bar a 3", resultado["log"][0])

    
if __name__ == "__main__":
    unittest.main()