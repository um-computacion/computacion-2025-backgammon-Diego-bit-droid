import unittest
from core.clases.board import Board

class TestBoard(unittest.TestCase):
    
    def test_preparar_tablero(self):
        board = Board()
        board.preparar_tablero()
        
        #posicion jugador 1
        self.assertEqual(board.__posiciones__[0], ['X', 'X'])
        self.assertEqual(board.__posiciones__[11], ['X', 'X', 'X', 'X', 'X'])
        self.assertEqual(board.__posiciones__[16], ['X', 'X', 'X'])
        self.assertEqual(board.__posiciones__[18], ['X', 'X', 'X', 'X', 'X'])
        
        #posiciones jugador 2
        self.assertEqual(board.__posiciones__[23], ['O', 'O'])
        self.assertEqual(board.__posiciones__[12], ['O', 'O', 'O', 'O', 'O'])
        self.assertEqual(board.__posiciones__[7], ['O', 'O', 'O'])
        self.assertEqual(board.__posiciones__[5], ['O', 'O', 'O', 'O', 'O'])
        
        
    
    def test_mostrar_board(self):
        board = Board()
        board.preparar_tablero()
        
        try:
            board.mostrar_board()
        except Exception as e:
            self.fail(f"mostrar_board() falló: {e}")
    
    
if __name__ == "__main__":
    unittest.main()