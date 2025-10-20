import unittest
from core.clases.backgammonGame import BackgammonGame
from core.clases.board import Board
from core.clases.dice import Dice
from core.clases.player import Player
from core.clases.excepciones import JuegoNoInicializadoError, SinMovimientosDisponiblesError, ValorDadoInvalidoError, TurnoJugadorInvalidoError, JuegoYaFinalizadoError

class TestBackgammonGameIntegrado(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")
        self.game = BackgammonGame(self.board, self.dice, self.jugador1, self.jugador2)
        self.game._BackgammonGame__turno__ = 1
        self.game._BackgammonGame__movimientos_restantes__ = 2

    def test_estado_jugador(self):
        estado = self.jugador1.estado_jugador(self.board)
        self.assertEqual(estado["nombre"], "player1")
        self.assertEqual(estado["ficha"], "X")
        self.assertEqual(estado["total"], 15)

    def test_get_fichas_en_bar(self):
        self.board.set_bar("player1", 3)
        self.assertEqual(self.jugador1.fichas_en_bar(self.board), 3)

    def test_get_fichas_sacadas(self):
        self.board.set_fuera("player1", 5)
        self.assertEqual(self.jugador1.fichas_sacadas(self.board), 5)

    def test_get_fichas_en_tablero(self):
        total = self.jugador1.fichas_en_tablero(self.board)
        self.assertEqual(total, 15)


    def test_hay_ganador_true(self):
        self.board.set_fuera("player1", 15)
        self.assertTrue(self.game.hay_ganador())

    def test_hay_ganador_false(self):
        self.board.set_fuera("player1", 10)
        self.board.set_fuera("player2", 14)
        self.assertFalse(self.game.hay_ganador())
    def test_calcular_movimientos_totales_normal(self):
        movimientos = self.game.calcular_movimientos_totales(3, 5)
        self.assertEqual(movimientos, [3, 5])

    def test_calcular_movimientos_totales_dobles(self):
        movimientos = self.game.calcular_movimientos_totales(4, 4)
        self.assertEqual(movimientos, [4, 4, 4, 4])

    def test_calcular_movimientos_totales_dado_invalido(self):
        with self.assertRaises(ValorDadoInvalidoError):
            self.game.calcular_movimientos_totales(0, 5)
    def test_get_jugador_por_nombre_valido(self):
        jugador = self.game.get_jugador_por_nombre("player1")
        self.assertEqual(jugador.get_ficha(), "X")

    def test_get_jugador_por_nombre_invalido(self):
        with self.assertRaises(TurnoJugadorInvalidoError):
            self.game.get_jugador_por_nombre("desconocido")
    def test_mostrar_movimientos_disponibles(self):
        self.game.mostrar_movimientos_disponibles(2, 5)
    def test_quien_empieza_asigna_turno(self):
        turno = self.game.quien_empieza()
        self.assertIn(turno, [1, 2])
        self.assertIn(self.game._BackgammonGame__turno__, [1, 2])
    def test_quien_empieza_asigna_turno_jugador_uno(self):
        self.game._BackgammonGame__turno__ = 0
        turno = 0
        while turno != 1:
            turno = self.game.quien_empieza()
        self.assertEqual(turno, 1)
    def test_quien_empieza_asigna_turno_jugador_uno(self):
        self.game._BackgammonGame__turno__ = 0
        turno = 0
        while turno != 2:
            turno = self.game.quien_empieza()
        self.assertEqual(turno, 2)
    #def test_cambiar_turno_valido(self):
    #def test iniciar_partida_valido(self):
    #def test_get_jugador_actual_valido(self):
    #def test_estado_turno_ejecucion(self):
    def test_get_movimientos_totales_valido(self):
        movimientos = self.game.get_movimientos_totales(3, 6)
        self.assertEqual(movimientos, [3, 6])
    def test_lanzar_dados_valido(self):
        self.game.iniciar_partida()
        dado1, dado2 = self.game.lanzar_dados()
        self.assertIn(dado1, range(1, 7))
        self.assertIn(dado2, range(1, 7))
        self.assertEqual(self.game._BackgammonGame__movimientos_restantes__, 4 if dado1 == dado2 else 2)

                
if __name__ == '__main__':
    unittest.main()