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
    def test_movimientos_dados_distintos(self):
        board = Board()
        movimientos = board.calcular_movimientos_totales(3, 5)
        self.assertEqual(movimientos, [3, 5])
        self.assertEqual(len(movimientos), 2)

    def test_movimientos_doble(self):
        board = Board()
        movimientos = board.calcular_movimientos_totales(4, 4)
        self.assertEqual(movimientos, [4, 4, 4, 4])
        self.assertEqual(len(movimientos), 4)
    def test_movimiento_valido_sin_comer(self):
        board = Board()
        board.preparar_tablero()
        jugador = Player("jugador1", "X")

        # Aseguramos que haya fichas en la posición 0
        board.__posiciones__[0] = [Checker("X")]
        resultado = board.mover_ficha(jugador, [(0, 3)], 3, 5)

        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(resultado["dados_usados"], [3])
        self.assertEqual([c.simbolo for c in board.__posiciones__[3]], ['X'])

    def test_movimiento_valido_con_comer(self):
        board = Board()
        jugador = Player("jugador1", "X")
        oponente = Player("jugador2", "O")

        board.__posiciones__[0] = [Checker("X")]
        board.__posiciones__[3] = [Checker("O")]  # ficha enemiga sola
        board.__bar__["jugador2"] = 0

        resultado = board.mover_ficha(jugador, [(0, 3)], 3, 5)

        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(board.__bar__["jugador2"], 1)
        self.assertEqual([c.simbolo for c in board.__posiciones__[3]], ['X'])

    def test_movimiento_con_dado_invalido(self):
        board = Board()
        jugador = Player("jugador1", "X")
        board.__posiciones__[0] = [Checker("X")]

        resultado = board.mover_ficha(jugador, [(0, 6)], 3, 5)

        self.assertEqual(resultado["resultados"], [False])
        self.assertEqual(resultado["dados_usados"], [])
        self.assertIn("No se puede usar dado 6", resultado["log"][0])

    def test_movimiento_invalido_por_regla(self):
        board = Board()
        jugador = Player("jugador1", "X")
        board.__posiciones__[0] = [Checker("X")]

        # Forzamos que validar_movimiento devuelva False
        board.validar_movimiento = lambda d, h, j: False

        resultado = board.mover_ficha(jugador, [(0, 3)], 3, 5)

        self.assertEqual(resultado["resultados"], [False])
        self.assertIn("Movimiento inválido", resultado["log"][0])

    def test_sacar_ficha_fuera(self):
        board = Board()
        jugador = Player("jugador1", "X")
        board.__posiciones__[18] = [Checker("X")]
        board.__fuera__["jugador1"] = 0

        resultado = board.mover_ficha(jugador, [(18, "fuera")], 6, 6)

        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(board.__fuera__["jugador1"], 1)
        self.assertIn("sacó ficha", resultado["log"][0])
    
    
if __name__ == "__main__":
    unittest.main()