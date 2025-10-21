"""
Módulo de pruebas unitarias para la clase Player.
"""
import unittest
from core.clases.player import Player
from core.clases.board import Board


class TestPlayer(unittest.TestCase):
    """Clase de pruebas para validar el comportamiento de la clase Player."""

    def setUp(self):
        """Configura el tablero y jugadores de prueba antes de cada test."""
        self.board = Board()
        self.player1 = Player("player1", "X")
        self.player2 = Player("player2", "O")

        # Configurar estado personalizado
        self.board.set_bar("player1", 2)
        self.board.set_fuera("player1", 3)

    def test_get_nombre(self):
        """Verifica que el nombre del jugador se obtenga correctamente."""
        self.assertEqual(self.player1.get_nombre(), "player1")

    def test_get_ficha(self):
        """Verifica que el tipo de ficha del jugador se obtenga correctamente."""
        self.assertEqual(self.player1.get_ficha(), "X")

    def test_fichas_en_tablero(self):
        """Verifica el conteo de fichas del jugador en el tablero."""
        cantidad = self.player1.fichas_en_tablero(self.board)
        self.assertEqual(cantidad, 15)  # 2+5+3+5 según preparar_tablero

    def test_fichas_en_bar(self):
        """Verifica el conteo de fichas del jugador en la barra."""
        self.assertEqual(self.player1.fichas_en_bar(self.board), 2)

    def test_fichas_sacadas(self):
        """Verifica el conteo de fichas sacadas del tablero."""
        self.assertEqual(self.player1.fichas_sacadas(self.board), 3)

    def test_estado_jugador(self):
        """Verifica que el estado completo del jugador se reporte correctamente."""
        estado = self.player1.estado_jugador(self.board)
        self.assertEqual(estado["en_tablero"], 15)
        self.assertEqual(estado["en_bar"], 2)
        self.assertEqual(estado["sacadas"], 3)
        self.assertEqual(estado["total"], 20)
        self.assertEqual(estado["nombre"], "player1")
        self.assertEqual(estado["ficha"], "X")
if __name__ == "__main__":
    unittest.main()
