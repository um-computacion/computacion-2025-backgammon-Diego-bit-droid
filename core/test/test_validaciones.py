"""
Módulo de pruebas unitarias para las validaciones del juego.
"""
import unittest
from core.clases.player import Player
from core.clases.board import Board
from core.clases.checker import Checker
from core.clases.validaciones import (
    regla_bar,
    regla_salida_final,
    MovimientoInvalidoError
)


class TestReglasValidacion(unittest.TestCase):
    """Clase de pruebas para validar las reglas de movimiento del juego."""

    def setUp(self):
        """Configura el tablero y jugadores de prueba antes de cada test."""
        self.board = Board()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")

    def test_regla_bar_no_lanza_excepcion_si_mueve_desde_bar(self):
        """Verifica que no se lance excepción al mover correctamente desde el bar."""
        self.board.set_bar("player1", 2)
        movimientos = [("bar", 3)]
        dados = [3]

        try:
            regla_bar(self.jugador1, movimientos, dados, self.board)
        except MovimientoInvalidoError:
            self.fail(
                "regla_bar lanzó excepción aunque el movimiento era desde el bar"
            )

    def test_regla_bar_no_lanza_excepcion_si_no_hay_fichas_en_bar(self):
        """Verifica que no se lance excepción si no hay fichas en el bar."""
        self.board.set_bar("player1", 0)
        movimientos = [(5, 7)]
        dados = [2]

        try:
            regla_bar(self.jugador1, movimientos, dados, self.board)
        except MovimientoInvalidoError:
            self.fail(
                "regla_bar lanzó excepción aunque no había fichas en el bar"
            )

    def test_regla_salida_final_no_lanza_excepcion_si_puede_sacar(self):
        """Verifica que no se lance excepción al sacar fichas correctamente."""
        for i in range(24):
            self.board.set_posiciones(i, [])
        self.board.set_posiciones(22, [Checker("X")])
        movimientos = [(22, "fuera")]
        dados = [1]
        try:
            regla_salida_final(self.jugador1, movimientos, dados, self.board)
        except MovimientoInvalidoError:
            self.fail(
                "regla_salida_final lanzó excepción aunque el jugador podía sacar fichas"
            )

    def test_regla_salida_final_no_lanza_si_no_es_movimiento_fuera(self):
        """Verifica que no se valide si el movimiento no es hacia fuera."""
        self.board.set_posiciones(3, [Checker("X")])
        movimientos = [(3, 5)]
        dados = [2]
        try:
            regla_salida_final(self.jugador1, movimientos, dados, self.board)
        except MovimientoInvalidoError:
            self.fail(
                "regla_salida_final lanzó excepción en movimiento normal"
            )
