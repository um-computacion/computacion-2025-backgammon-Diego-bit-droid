import unittest
from core.clases.backgammonGame import BackgammonGame
from core.clases.board import Board
from core.clases.dice import Dice
from core.clases.player import Player
from core.clases.excepciones import JuegoNoInicializadoError, SinMovimientosDisponiblesError, ValorDadoInvalidoError, TurnoJugadorInvalidoError, JuegoYaFinalizadoError
from core.clases.validaciones import MovimientoInvalidoError
def regla_invalida(jugador, movimientos, dados, board):
        raise MovimientoInvalidoError("Movimiento inválido por regla")
class TestBackgammonGameIntegrado(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.dice = Dice()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")
        self.game = BackgammonGame(self.board, self.dice, self.jugador1, self.jugador2)
        self.game.__turno__ = 0
        self.game.__movimientos_restantes__ = 2
    def test_fichas_en_tablero(self):
        
        self.game.__board__.get_tablero = lambda: {
            "posiciones": [["player1"], [], ["player2"], ["player1", "player1"]],
            "bar": {"player1": 0, "player2": 0},
            "fuera": {"player1": 0, "player2": 0}
        }
    
    def test_fichas_en_bar(self):
        self.game.__board__.get_tablero = lambda: {
            "posiciones": [],
            "bar": {"player1": 2, "player2": 1},
            "fuera": {"player1": 0, "player2": 0}
        }

        self.jugador1.fichas_en_bar = lambda bar: bar["player1"]
        fichas = self.game.get_fichas_en_bar(self.jugador1)
        self.assertEqual(fichas, 2)

    def test_fichas_sacadas(self):
        self.game.__board__.get_tablero = lambda: {
            "posiciones": [],
            "bar": {"player1": 0, "player2": 0},
            "fuera": {"player1": 7, "player2": 4}
        }

        self.jugador1.fichas_sacadas = lambda fuera: fuera["player1"]
        fichas = self.game.get_fichas_sacadas(self.jugador1)
        self.assertEqual(fichas, 7)
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
        turno=1
        turno = self.game.quien_empieza()
        self.assertIn(turno, [1, 2])
        self.assertIn(self.game.__turno__, [1, 2])
    def test_quien_empieza_asigna_turno_jugador_uno(self):
        self.game._BackgammonGame__turno__ = 0
        turno = 0
        while turno != 1:
            turno = self.game.quien_empieza()
        self.assertEqual(turno, 1)
    def test_quien_empieza_asigna_turno_jugador_uno(self):
        self.game.__turno__ = 0
        turno = 0
        while turno != 2:
            turno = self.game.quien_empieza()
        self.assertEqual(turno, 2)
    
    def test_iniciar_partida_valido(self):
        self.game.__turno__ = 0
        self.game.iniciar_partida()
        self.assertIn(self.game.__turno__, [1, 2])
    def test_get_movimientos_totales_valido(self):
        movimientos = self.game.get_movimientos_totales(3, 6)
        self.assertEqual(movimientos, [3, 6])
    def test_lanzar_dados_valido(self):
        # Forzamos turno válido para evitar errores
        self.game.__turno__ = 1

        # Llamamos directamente a lanzar_dados
        dado1, dado2 = self.game.lanzar_dados()

        # Verificamos que movimientos_restantes se asigna correctamente
        esperados = 4 if dado1 == dado2 else 2
        self.assertEqual(self.game.__movimientos_restantes__, esperados)
    def test_get_jugador_actual_valido(self):
        self.game.__turno__ = 2
        jugador = self.game.get_jugador_actual()
        self.assertEqual(jugador.get_nombre(), "player2")

    def test_estado_turno_ejecucion(self):
        self.game.__turno__ = 1
     
        self.game.estado_turno()

    def test_cambiar_turno_de_2_a_1(self):
        self.game.iniciar_partida()
        self.game.__turno__ = 2
        self.game.cambiar_turno()
        self.assertEqual(self.game.__turno__, 1)
    def test_dado_fuera_de_rango_lanza_error(self):
        with self.assertRaises(ValorDadoInvalidoError):
            self.game.calcular_movimientos_totales(0, 5)
    def test_get_jugador_por_nombre_invalido(self):
        with self.assertRaises(TurnoJugadorInvalidoError):
            self.game.get_jugador_por_nombre("inexistente")
    def test_get_jugador_actual_sin_turno_lanza_error(self):
        with self.assertRaises(JuegoNoInicializadoError):
            self.game.get_jugador_actual()
    def test_cambiar_turno_sin_turno_lanza_error(self):
        with self.assertRaises(JuegoNoInicializadoError):
            self.game.cambiar_turno()
    def test_mover_ficha_sin_movimientos_lanza_error(self):
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 0
        with self.assertRaises(SinMovimientosDisponiblesError):
            self.game.mover_ficha([(0, 1)], 3, 4)
    def test_hay_ganador_false(self):
        self.assertFalse(self.game.hay_ganador())
    def test_mover_ficha_valida(self):
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 2

        # Simula que el tablero acepta el movimiento
        self.board.mover_ficha = lambda jugador, movimientos, dados: {
            "resultados": [True],
            "dados_usados": [3],
            "dados_restantes": [4],
            "log": ["Movimiento exitoso"]
        }

        resultado = self.game.mover_ficha([(0, 1)], 3, 4)
        self.assertTrue(all(resultado["resultados"]))
        self.assertEqual(resultado["dados_usados"], [3])
        self.assertEqual(resultado["dados_restantes"], [4])
        self.assertIn("Movimiento exitoso", resultado["log"])


    def test_mover_ficha_agota_movimientos_y_cambia_turno(self):
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 1

        self.board.mover_ficha = lambda jugador, movimientos, dados: {
            "resultados": [True],
            "dados_usados": [3],
            "dados_restantes": [],
            "log": ["Movimiento exitoso"]
        }

        self.game.mover_ficha([(0, 1)], 3, 4)
        self.assertEqual(self.game.__turno__, 2)  

    def test_get_jugador_por_nombre_valido_player2(self):
        jugador = self.game.get_jugador_por_nombre("player2")
        self.assertEqual(jugador.get_ficha(), "O")
    def test_mover_ficha_regla_invalida(self):
        self.game.__turno__ = 1
        self.game.__movimientos_restantes__ = 2
        self.game.__reglas__ = [regla_invalida]

        resultado = self.game.mover_ficha([(0, 1)], 3, 4)
        self.assertEqual(resultado["resultados"], [False])  
        self.assertEqual(resultado["dados_usados"], [])
        self.assertIn("Movimiento inválido por regla", resultado["log"][0])


                    
if __name__ == '__main__':
    unittest.main()