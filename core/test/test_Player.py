import unittest
from core.clases.player import Player
from core.clases.board import Board
from core.clases.checker import Checker

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player1 = Player("player1", "X")
        self.player2 = Player("player2", "O")

        # Configurar estado personalizado
        self.board.set_bar("player1", 2)
        self.board.set_fuera("player1", 3)

    def test_get_nombre(self):
        self.assertEqual(self.player1.get_nombre(), "player1")

    def test_get_ficha(self):
        self.assertEqual(self.player1.get_ficha(), "X")

    def test_fichas_en_tablero(self):
        cantidad = self.player1.fichas_en_tablero(self.board)
        self.assertEqual(cantidad, 15)  # 2+5+3+5 según preparar_tablero

    def test_fichas_en_bar(self):
        self.assertEqual(self.player1.fichas_en_bar(self.board), 2)

    def test_fichas_sacadas(self):
        self.assertEqual(self.player1.fichas_sacadas(self.board), 3)

    def test_estado_jugador(self):
        estado = self.player1.estado_jugador(self.board)
        self.assertEqual(estado["en_tablero"], 15)
        self.assertEqual(estado["en_bar"], 2)
        self.assertEqual(estado["sacadas"], 3)
        self.assertEqual(estado["total"], 20)
        self.assertEqual(estado["nombre"], "player1")
        self.assertEqual(estado["ficha"], "X")
