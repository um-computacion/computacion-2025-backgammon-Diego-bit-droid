"""
Pruebas unitarias para la clase BackgammonGame.
Valida la lógica completa del controlador del juego de Backgammon.
"""
import unittest
from unittest.mock import patch
from core.clases.backgammon_game import BackgammonGame
from core.clases.excepciones import (
    JuegoNoInicializadoError,
    TurnoJugadorInvalidoError,
    JuegoYaFinalizadoError,
    ValorDadoInvalidoError
)
class TestBackgammonGame(unittest.TestCase):
    """Suite de pruebas para la clase BackgammonGame."""
    # pylint: disable=too-many-public-methods

    def setUp(self):
        """Inicializa entorno de prueba."""
        self.game = BackgammonGame("player1", "player2")

    def test_init_juego(self):
        """Verifica inicialización correcta del juego."""
        self.assertIsNotNone(self.game.get_board())
        self.assertIsNotNone(self.game.get_jugador1())
        self.assertIsNotNone(self.game.get_jugador2())
        self.assertEqual(self.game.get_turno(), 0)
        self.assertEqual(self.game.get_movimientos_restantes(), 0)
        self.assertEqual(self.game.get_jugador1().get_nombre(), "player1")
        self.assertEqual(self.game.get_jugador2().get_nombre(), "player2")
        self.assertEqual(self.game.get_jugador1().get_ficha(), "X")
        self.assertEqual(self.game.get_jugador2().get_ficha(), "O")

    def test_calcular_movimientos_totales_normal(self):
        """Verifica cálculo de movimientos con dados diferentes."""
        movimientos = self.game.calcular_movimientos_totales(3, 5)
        self.assertEqual(movimientos, [3, 5])

    def test_calcular_movimientos_totales_dobles(self):
        """Verifica cálculo de movimientos con dados iguales (dobles)."""
        movimientos = self.game.calcular_movimientos_totales(4, 4)
        self.assertEqual(movimientos, [4, 4, 4, 4])

    def test_calcular_movimientos_totales_dado1_invalido(self):
        """Verifica error cuando primer dado está fuera de rango."""
        with self.assertRaises(ValorDadoInvalidoError):
            self.game.calcular_movimientos_totales(0, 5)

    def test_calcular_movimientos_totales_dado2_invalido(self):
        """Verifica error cuando segundo dado está fuera de rango."""
        with self.assertRaises(ValorDadoInvalidoError):
            self.game.calcular_movimientos_totales(3, 7)

    def test_calcular_movimientos_totales_ambos_invalidos(self):
        """Verifica error cuando ambos dados están fuera de rango."""
        with self.assertRaises(ValorDadoInvalidoError):
            self.game.calcular_movimientos_totales(-1, 8)

    def test_mostrar_movimientos_disponibles(self):
        """Verifica que mostrar_movimientos_disponibles no lanza error."""
        self.game.mostrar_movimientos_disponibles(2, 5)

    def test_get_jugador_por_nombre_jugador1(self):
        """Verifica obtención del jugador 1 por nombre."""
        jugador = self.game.get_jugador_por_nombre("player1")
        self.assertEqual(jugador.get_nombre(), "player1")
        self.assertEqual(jugador.get_ficha(), "X")

    def test_get_jugador_por_nombre_jugador2(self):
        """Verifica obtención del jugador 2 por nombre."""
        jugador = self.game.get_jugador_por_nombre("player2")
        self.assertEqual(jugador.get_nombre(), "player2")
        self.assertEqual(jugador.get_ficha(), "O")

    def test_get_jugador_por_nombre_invalido(self):
        """Verifica error cuando el jugador no existe."""
        with self.assertRaises(TurnoJugadorInvalidoError):
            self.game.get_jugador_por_nombre("Charlie")

    def test_quien_empieza_asigna_turno(self):
        """Verifica que quien_empieza asigna un turno válido."""
        turno, dado1, dado2 = self.game.quien_empieza()
        self.assertIn(turno, [1, 2])
        self.assertIn(dado1, [1, 2, 3, 4, 5, 6])
        self.assertIn(dado2, [1, 2, 3, 4, 5, 6])
        self.assertNotEqual(dado1, dado2)
        self.assertEqual(self.game.get_turno(), turno)

    def test_quien_empieza_multiple_veces(self):
        """Verifica que quien_empieza puede ejecutarse múltiples veces."""
        turnos = set()
        for _ in range(10):
            game = BackgammonGame("player1", "player2")
            turno, _, _ = game.quien_empieza()
            turnos.add(turno)
        self.assertTrue(1 in turnos or 2 in turnos)

    def test_iniciar_partida_asigna_turno(self):
        """Verifica que iniciar_partida asigna turno y lanza dados."""
        self.game.iniciar_partida()
        self.assertIn(self.game.get_turno(), [1, 2])
        self.assertGreater(self.game.get_movimientos_restantes(), 0)

    def test_iniciar_partida_ya_iniciada(self):
        """Verifica error al intentar iniciar partida ya iniciada."""
        self.game.iniciar_partida()
        with self.assertRaises(JuegoYaFinalizadoError):
            self.game.iniciar_partida()

    def test_get_jugador_actual_sin_iniciar(self):
        """Verifica error al obtener jugador actual sin iniciar juego."""
        with self.assertRaises(JuegoNoInicializadoError):
            self.game.get_jugador_actual()

    def test_get_jugador_actual_despues_de_iniciar(self):
        """Verifica obtención correcta de jugador actual."""
        self.game.iniciar_partida()
        jugador = self.game.get_jugador_actual()
        self.assertIn(jugador.get_nombre(), ["player1", "player2"])

    def test_cambiar_turno_sin_iniciar(self):
        """Verifica error al cambiar turno sin iniciar juego."""
        with self.assertRaises(JuegoNoInicializadoError):
            self.game.cambiar_turno()

    def test_cambiar_turno_alterna_jugadores(self):
        """Verifica que cambiar turno alterna entre jugadores."""
        self.game.iniciar_partida()
        jugador1 = self.game.get_jugador_actual()
        self.game.cambiar_turno()
        jugador2 = self.game.get_jugador_actual()
        self.assertNotEqual(jugador1.get_nombre(), jugador2.get_nombre())

    def test_cambiar_turno_reinicia_movimientos(self):
        """Verifica que cambiar turno reinicia movimientos restantes a 0."""
        self.game.iniciar_partida()
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_movimientos_restantes(), 0)

    def test_cambiar_turno_ciclo_completo(self):
        """Verifica ciclo completo de cambio de turno."""
        self.game.iniciar_partida()
        turno_inicial = self.game.get_turno()
        self.game.cambiar_turno()
        turno_cambiado = self.game.get_turno()
        self.game.cambiar_turno()
        turno_final = self.game.get_turno()
        self.assertNotEqual(turno_inicial, turno_cambiado)
        self.assertEqual(turno_inicial, turno_final)

    def test_lanzar_dados_valores_validos(self):
        """Verifica que lanzar_dados devuelve valores válidos."""
        self.game.iniciar_partida()
        dado1, dado2, movimientos = self.game.lanzar_dados()
        self.assertIn(dado1, [1, 2, 3, 4, 5, 6])
        self.assertIn(dado2, [1, 2, 3, 4, 5, 6])
        self.assertIn(movimientos, [2, 4])

    def test_lanzar_dados_actualiza_movimientos(self):
        """Verifica que lanzar_dados actualiza movimientos restantes."""
        self.game.iniciar_partida()
        dado1, dado2, _ = self.game.lanzar_dados()
        esperados = 4 if dado1 == dado2 else 2
        self.assertEqual(self.game.get_movimientos_restantes(), esperados)

    def test_mover_ficha_sin_movimientos_disponibles(self):
        """Verifica comportamiento al mover sin movimientos disponibles."""
        self.game.iniciar_partida()
        self.game.__movimientos_restantes__ = 0
        resultado = self.game.mover_ficha([(0, 3)], 3, 4)
        self.assertFalse(any(resultado["resultados"]))
        self.assertEqual(resultado["dados_usados"], [])
        self.assertIn("No hay movimientos disponibles", resultado["log"][0])

    def test_hay_ganador_inicial(self):
        """Verifica que no hay ganador al inicio."""
        self.assertFalse(self.game.hay_ganador())

    def test_hay_ganador_jugador1_gana(self):
        """Verifica detección de victoria del jugador 1."""
        self.game.get_board().set_fuera("player1", 15)
        self.assertTrue(self.game.hay_ganador())

    def test_hay_ganador_jugador2_gana(self):
        """Verifica detección de victoria del jugador 2."""
        self.game.get_board().set_fuera("player2", 15)
        self.assertTrue(self.game.hay_ganador())

    def test_hay_ganador_sin_victoria_completa(self):
        """Verifica que no hay ganador sin 15 fichas fuera."""
        self.game.get_board().set_fuera("player1", 14)
        self.assertFalse(self.game.hay_ganador())

    def test_get_tablero(self):
        """Verifica obtención del estado del tablero."""
        tablero = self.game.get_tablero()
        self.assertIn("posiciones", tablero)
        self.assertIn("bar", tablero)
        self.assertIn("fuera", tablero)
        self.assertEqual(len(tablero["posiciones"]), 24)

    def test_get_fichas_en_tablero(self):
        """Verifica conteo de fichas en tablero."""
        jugador1 = self.game.get_jugador1()
        fichas = self.game.get_fichas_en_tablero(jugador1)
        self.assertEqual(fichas, 15)

    def test_get_fichas_en_bar(self):
        """Verifica conteo de fichas en bar."""
        jugador1 = self.game.get_jugador1()
        fichas_bar = self.game.get_fichas_en_bar(jugador1)
        self.assertEqual(fichas_bar, 0)
        self.game.get_board().set_bar("player1", 3)
        fichas_bar = self.game.get_fichas_en_bar(jugador1)
        self.assertEqual(fichas_bar, 3)

    def test_get_fichas_sacadas(self):
        """Verifica conteo de fichas sacadas."""
        jugador1 = self.game.get_jugador1()
        fichas_fuera = self.game.get_fichas_sacadas(jugador1)
        self.assertEqual(fichas_fuera, 0)
        self.game.get_board().set_fuera("player1", 5)
        fichas_fuera = self.game.get_fichas_sacadas(jugador1)
        self.assertEqual(fichas_fuera, 5)

    def test_estado_turno(self):
        """Verifica que estado_turno no lanza error."""
        self.game.iniciar_partida()
        self.game.estado_turno()

    def test_get_jugador1(self):
        """Verifica obtención del jugador 1."""
        jugador1 = self.game.get_jugador1()
        self.assertEqual(jugador1.get_nombre(), "player1")
        self.assertEqual(jugador1.get_ficha(), "X")

    def test_get_jugador2(self):
        """Verifica obtención del jugador 2."""
        jugador2 = self.game.get_jugador2()
        self.assertEqual(jugador2.get_nombre(), "player2")
        self.assertEqual(jugador2.get_ficha(), "O")

    def test_get_board(self):
        """Verifica obtención de la instancia del tablero."""
        board = self.game.get_board()
        self.assertIsNotNone(board)

    def test_get_turno(self):
        """Verifica obtención del número de turno."""
        self.assertEqual(self.game.get_turno(), 0)
        self.game.iniciar_partida()
        self.assertIn(self.game.get_turno(), [1, 2])

    def test_get_movimientos_restantes(self):
        """Verifica obtención de movimientos restantes."""
        self.assertEqual(self.game.get_movimientos_restantes(), 0)
        self.game.iniciar_partida()
        self.assertGreater(self.game.get_movimientos_restantes(), 0)

    def test_mostrar_tablero(self):
        """Verifica que mostrar_tablero devuelve estado."""
        resultado = self.game.mostrar_tablero()
        self.assertIsNotNone(resultado)
        self.assertIn("posiciones", resultado)
        self.assertIn("bar", resultado)
        self.assertIn("fuera", resultado)

    def test_juego_activo_sin_iniciar(self):
        """Verifica que juego no está activo sin iniciar."""
        self.assertFalse(self.game.juego_activo())

    def test_juego_activo_despues_de_iniciar(self):
        """Verifica que juego está activo después de iniciar."""
        self.game.iniciar_partida()
        self.assertTrue(self.game.juego_activo())

    def test_juego_activo_con_ganador(self):
        """Verifica que juego no está activo cuando hay ganador."""
        self.game.iniciar_partida()
        self.game.get_board().set_fuera("player1", 15)
        self.assertFalse(self.game.juego_activo())

    def test_get_estado_juego_sin_iniciar(self):
        """Verifica estado del juego sin iniciar."""
        estado = self.game.get_estado_juego()
        self.assertEqual(estado["turno"], 0)
        self.assertEqual(estado["movimientos_restantes"], 0)
        self.assertIsNone(estado["jugador_actual"])
        self.assertIn("tablero", estado)
        self.assertIn("jugador1", estado)
        self.assertIn("jugador2", estado)

    def test_get_estado_juego_despues_de_iniciar(self):
        """Verifica estado completo del juego después de iniciar."""
        self.game.iniciar_partida()
        estado = self.game.get_estado_juego()
        self.assertIn(estado["turno"], [1, 2])
        self.assertGreater(estado["movimientos_restantes"], 0)
        self.assertIsNotNone(estado["jugador_actual"])
        self.assertEqual(estado["jugador1"]["nombre"], "player1")
        self.assertEqual(estado["jugador1"]["ficha"], "X")
        self.assertEqual(estado["jugador2"]["nombre"], "player2")
        self.assertEqual(estado["jugador2"]["ficha"], "O")

    def test_get_estado_juego_estructura_completa(self):
        """Verifica estructura completa del estado del juego."""
        estado = self.game.get_estado_juego()
        self.assertIn("turno", estado)
        self.assertIn("movimientos_restantes", estado)
        self.assertIn("jugador_actual", estado)
        self.assertIn("tablero", estado)
        self.assertIn("jugador1", estado)
        self.assertIn("jugador2", estado)
        self.assertIn("nombre", estado["jugador1"])
        self.assertIn("ficha", estado["jugador1"])
        self.assertIn("fichas_tablero", estado["jugador1"])
        self.assertIn("fichas_bar", estado["jugador1"])
        self.assertIn("fichas_sacadas", estado["jugador1"])

    def test_calcular_movimientos_totales_todos_valores(self):
        """Verifica cálculo correcto para todos los valores de dados."""
        for d1 in range(1, 7):
            for d2 in range(1, 7):
                movimientos = self.game.calcular_movimientos_totales(d1, d2)
                if d1 == d2:
                    self.assertEqual(movimientos, [d1] * 4)
                else:
                    self.assertEqual(movimientos, [d1, d2])

    def test_mover_ficha_cambia_turno_automaticamente(self):
        """Verifica que mover ficha cambia turno cuando se agotan movimientos."""
        self.game.iniciar_partida()
        turno_inicial = self.game.get_turno()

        with patch.object(self.game.get_board(), 'mover_ficha') as mock_mover:
            mock_mover.return_value = {
                "resultados": [True],
                "dados_usados": [3],
                "dados_restantes": [4],
                "log": ["Movimiento exitoso"]
            }

            self.game.__movimientos_restantes__ = 1
            self.game.mover_ficha([(0, 3)], 3, 4)

            turno_final = self.game.get_turno()
            self.assertNotEqual(turno_inicial, turno_final)

    def test_varios_cambios_turno(self):
        """Verifica múltiples cambios de turno consecutivos."""
        self.game.iniciar_partida()
        turnos = []
        for _ in range(4):
            turnos.append(self.game.get_turno())
            self.game.cambiar_turno()
        self.assertEqual(turnos[0], turnos[2])
        self.assertEqual(turnos[1], turnos[3])

    def test_hay_ganador_ambos_sin_ganar(self):
        """Verifica que no hay ganador cuando ambos tienen menos de 15."""
        self.game.get_board().set_fuera("player1", 10)
        self.game.get_board().set_fuera("player2", 10)
        self.assertFalse(self.game.hay_ganador())


if __name__ == "__main__":
    unittest.main()
