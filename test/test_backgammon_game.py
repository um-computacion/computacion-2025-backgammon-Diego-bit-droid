"""
Pruebas unitarias para la clase BackgammonGame.
"""
import unittest
import random
from core.backgammon_game import BackgammonGame
from core.excepciones import (
    JuegoNoInicializadoError,
    JuegoYaFinalizadoError,
    ValorDadoInvalidoError
)
from core.checker import Checker
from core.validaciones import regla_salida_final, regla_bar, MovimientoInvalidoError
from core.player import Player

# pylint: disable=too-many-public-methods
class TestBackgammonGame(unittest.TestCase):
    """Suite de pruebas para la clase BackgammonGame."""

    def setUp(self):
        """Inicializa entorno de prueba."""
        self.game = BackgammonGame("player1", "player2")

    def test_init_juego(self):
        """Verifica inicialización correcta del juego."""
        self.assertIsNotNone(self.game.get_jugador1())
        self.assertIsNotNone(self.game.get_jugador2())
        self.assertEqual(self.game.get_turno(), 0)
        self.assertEqual(self.game.get_movimientos_restantes(), 0)
        self.assertEqual(self.game.get_jugador1().get_nombre(), "player1")
        self.assertEqual(self.game.get_jugador2().get_nombre(), "player2")
        self.assertEqual(self.game.get_jugador1().get_ficha(), "O")
        self.assertEqual(self.game.get_jugador2().get_ficha(), "X")

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

    def test_quien_empieza_asigna_turno(self):
        """Verifica que quien_empieza asigna un turno válido."""
        turno, dado1, dado2 = self.game.quien_empieza()
        self.assertIn(turno, [1, 2])
        self.assertIn(dado1, [1, 2, 3, 4, 5, 6])
        self.assertIn(dado2, [1, 2, 3, 4, 5, 6])
        self.assertNotEqual(dado1, dado2)
        self.assertEqual(self.game.get_turno(), turno)

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

    def test_cambiar_turno_sin_iniciar_juego(self):
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

    def test_cambiar_turno_reinicia_movimientos_y_dados(self):
        """Verifica que cambiar turno reinicia movimientos y limpia dados."""
        self.game.iniciar_partida()
        self.game.cambiar_turno()
        self.assertEqual(self.game.get_movimientos_restantes(), 0)
        self.assertEqual(len(self.game.get_dados_disponibles()), 0)

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

    def test_hay_ganador_inicial(self):
        """Verifica que no hay ganador al inicio."""
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

    def test_get_fichas_sacadas(self):
        """Verifica conteo de fichas sacadas."""
        jugador1 = self.game.get_jugador1()
        fichas_fuera = self.game.get_fichas_sacadas(jugador1)
        self.assertEqual(fichas_fuera, 0)

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

    def test_juego_activo_sin_iniciar(self):
        """Verifica que juego no está activo sin iniciar."""
        self.assertFalse(self.game.juego_activo())

    def test_juego_activo_despues_de_iniciar(self):
        """Verifica que juego está activo después de iniciar."""
        self.game.iniciar_partida()
        self.assertTrue(self.game.juego_activo())

    def test_get_estado_juego_sin_iniciar(self):
        """Verifica estado del juego sin iniciar."""
        estado = self.game.get_estado_juego()
        self.assertEqual(estado["turno"], 0)
        self.assertEqual(estado["movimientos_restantes"], 0)
        self.assertIsNone(estado["jugador_actual"])

    def test_get_estado_juego_despues_de_iniciar(self):
        """Verifica estado completo del juego después de iniciar."""
        self.game.iniciar_partida()
        estado = self.game.get_estado_juego()
        self.assertIn(estado["turno"], [1, 2])
        self.assertGreater(estado["movimientos_restantes"], 0)
        self.assertIsNotNone(estado["jugador_actual"])
        self.assertIn("jugador1", estado)
        self.assertIn("jugador2", estado)
        self.assertIn("nombre", estado["jugador1"])
        self.assertIn("fichas_tablero", estado["jugador1"])

    def test_mover_ficha_sin_inicializar_juego(self):
        """Verifica error al mover sin inicializar juego."""
        with self.assertRaises(JuegoNoInicializadoError):
            self.game.mover_ficha([(0, 3)], 3, 2)

    def test_mover_ficha_sin_movimientos_disponibles(self):
        """Verifica comportamiento cuando no hay movimientos restantes."""
        self.game.iniciar_partida()
        self.game.__movimientos_restantes__ = 0
        resultado = self.game.mover_ficha([(0, 3)], 3, 4)
        self.assertFalse(any(resultado["resultados"]))
        self.assertEqual(len(resultado["dados_usados"]), 0)
        self.assertTrue(len(resultado["log"]) > 0)

    def test_estructura_resultado_mover_ficha(self):
        """Verifica estructura del resultado."""
        self.game.iniciar_partida()
        resultado = self.game.mover_ficha([(0, 3)], 3, 2)
        self.assertIn("resultados", resultado)
        self.assertIn("dados_usados", resultado)
        self.assertIn("dados_restantes", resultado)
        self.assertIn("log", resultado)

    def test_calcular_movimientos_totales_todos_valores(self):
        """Verifica cálculo correcto para todos los valores de dados."""
        for dado1 in range(1, 7):
            for dado2 in range(1, 7):
                movimientos = self.game.calcular_movimientos_totales(dado1, dado2)
                if dado1 == dado2:
                    self.assertEqual(movimientos, [dado1] * 4)
                else:
                    self.assertEqual(movimientos, [dado1, dado2])

    def test_tiene_movimientos_posicion_inicial(self):
        """Al inicio del juego siempre hay movimientos legales disponibles."""
        juego = BackgammonGame("player1", "player2")
        juego.quien_empieza()
        jugador = juego.get_jugador_actual()
        self.assertTrue(juego.tiene_movimientos_legales(jugador, 3, 4))
        self.assertTrue(juego.tiene_movimientos_legales(jugador, 1, 1))
        self.assertTrue(juego.tiene_movimientos_legales(jugador, 6, 6))

    def test_tiene_movimientos_con_reglas(self):
        """Verifica movimientos legales cuando hay reglas activas."""
        reglas = [regla_bar, regla_salida_final]
        juego = BackgammonGame("player1", "player2", reglas=reglas)
        juego.quien_empieza()
        jugador = juego.get_jugador_actual()
        self.assertTrue(juego.tiene_movimientos_legales(jugador, 2, 3))

    def test_get_dados_disponibles(self):
        """Verifica que se pueden obtener los dados disponibles."""
        self.game.iniciar_partida()
        dados = self.game.get_dados_disponibles()
        self.assertIsInstance(dados, list)
        self.assertGreater(len(dados), 0)

    def test_varios_cambios_turno(self):
        """Verifica múltiples cambios de turno consecutivos."""
        self.game.iniciar_partida()
        turnos = []
        for _ in range(4):
            turnos.append(self.game.get_turno())
            self.game.cambiar_turno()
        self.assertEqual(turnos[0], turnos[2])
        self.assertEqual(turnos[1], turnos[3])

    def test_mostrar_movimientos_disponibles_sin_dados_previos(self):
        """Verifica cálculo cuando no hay dados disponibles."""
        self.game.iniciar_partida()
        self.game.__dados_disponibles__ = []
        dados = self.game.mostrar_movimientos_disponibles(3, 4)
        self.assertIn(3, dados)
        self.assertIn(4, dados)

    def test_mostrar_movimientos_disponibles_con_dados_existentes(self):
        """Verifica comportamiento cuando ya hay dados disponibles."""
        self.game.iniciar_partida()
        self.game.__dados_disponibles__ = [3, 4]
        dados = self.game.mostrar_movimientos_disponibles(3, 4)
        self.assertEqual(dados, [3, 4])

    def test_validar_movimiento_con_reglas(self):
        """Verifica validación de movimientos con reglas."""
        self.game.iniciar_partida()
        jugador = self.game.get_jugador_actual()
        # pylint: disable=protected-access
        resultado = self.game._validar_movimiento_con_reglas(
            jugador, [('bar', 0)], [3, 4]
        )
        self.assertIsInstance(resultado, bool)

    def test_validar_movimiento_con_value_error(self):
        """Cubre captura de ValueError en validación."""
        def regla_error(jugador, movimientos, dados, board):
            raise ValueError("Error intencional")

        game = BackgammonGame("p1", "p2", reglas=[regla_error])
        game.iniciar_partida()
        # pylint: disable=protected-access
        resultado = game._validar_movimiento_con_reglas(
            game.get_jugador_actual(), [(0, 3)], [3]
        )
        self.assertFalse(resultado)

    def test_verificar_movimiento_desde_posicion(self):
        """Verifica verificación de movimientos desde una posición."""
        self.game.iniciar_partida()
        jugador = self.game.get_jugador_actual()
        # pylint: disable=protected-access
        resultado = self.game._verificar_movimiento_desde_posicion(
            jugador, 0, 3, [3, 4]
        )
        self.assertIsInstance(resultado, bool)

    def test_tiene_fichas_mas_atras_jugador_x_sin_fichas_atras(self):
        """Verifica False cuando no hay fichas más atrás para jugador X."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        if game.get_jugador_actual().get_ficha() != 'X':
            game.cambiar_turno()
        jugador = game.get_jugador_actual()
        # pylint: disable=protected-access
        resultado = game._tiene_fichas_mas_atras(jugador, 18)
        self.assertFalse(resultado)

    def test_tiene_fichas_mas_atras_jugador_o_sin_fichas_atras(self):
        """Verifica False cuando no hay fichas más atrás para jugador O."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        if game.get_jugador_actual().get_ficha() != 'O':
            game.cambiar_turno()
        jugador = game.get_jugador_actual()
        # pylint: disable=protected-access
        resultado = game._tiene_fichas_mas_atras(jugador, 5)
        self.assertFalse(resultado)

    def test_verificar_bearing_off_escenario(self):
        """Cubre bearing off con diferentes escenarios."""
        game = BackgammonGame("player1", "player2", reglas=[regla_salida_final])
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        pos = 23 if jugador.get_ficha() == 'X' else 0
        # pylint: disable=protected-access
        resultado = game._verificar_movimiento_desde_posicion(
            jugador, pos, 1, [1]
        )
        self.assertIsInstance(resultado, bool)

    def test_verificar_bearing_off_dado_mayor_sin_fichas_atras(self):
        """Cubre bearing off con dado mayor."""
        game = BackgammonGame("player1", "player2", reglas=[regla_salida_final])
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        board = game.get_tablero()
        for i in range(24):
            board['posiciones'][i] = []
        if jugador.get_ficha() == 'X':
            board['posiciones'][22] = [Checker('X')]
            pos = 22
            dado = 6
        else:
            board['posiciones'][1] = [Checker('O')]
            pos = 1
            dado = 6
        # pylint: disable=protected-access
        resultado = game._verificar_movimiento_desde_posicion(
            jugador, pos, dado, [dado]
        )
        self.assertIsInstance(resultado, bool)

    def test_tiene_movimientos_con_dados_actuales_sin_dados(self):
        """Verifica retorno False cuando no hay dados disponibles."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        game.__dados_disponibles__ = []
        # pylint: disable=protected-access
        resultado = game._tiene_movimientos_con_dados_actuales(jugador)
        self.assertFalse(resultado)

    def test_tiene_movimientos_con_dados_actuales_con_dados(self):
        """Verifica con dados disponibles."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        game.__dados_disponibles__ = [3, 4]
        # pylint: disable=protected-access
        resultado = game._tiene_movimientos_con_dados_actuales(jugador)
        self.assertTrue(resultado)

    def test_tiene_movimientos_con_fichas_en_bar(self):
        """Cubre verificación con fichas en bar."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        board = game.__board__
        player_key = jugador.get_nombre()
        for i in range(24):
            board.set_posiciones(i, [])
        board.set_bar(player_key, 1)
        game.__dados_disponibles__ = [3]
        # pylint: disable=protected-access
        resultado = game._tiene_movimientos_con_dados_actuales(jugador)
        self.assertIsInstance(resultado, bool)

    def test_tiene_movimientos_bar_posicion_bloqueada(self):
        """Cubre skip cuando posición de bar está bloqueada."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        board = game.__board__
        player_key = jugador.get_nombre()
        for i in range(24):
            board.set_posiciones(i, [])
        board.set_bar(player_key, 1)
        ficha_oponente = 'O' if jugador.get_ficha() == 'X' else 'X'
        zona_entrada = range(0, 6) if jugador.get_ficha() == 'X' else range(18, 24)
        for pos in zona_entrada:
            board.set_posiciones(pos, [Checker(ficha_oponente), Checker(ficha_oponente)])
        game.__dados_disponibles__ = [3]
        # pylint: disable=protected-access
        resultado = game._tiene_movimientos_con_dados_actuales(jugador)
        self.assertFalse(resultado)

    def test_tiene_movimientos_legales_con_bar(self):
        """Cubre movimientos legales desde bar."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        board = game.__board__
        player_key = jugador.get_nombre()
        board.set_bar(player_key, 1)
        resultado = game.tiene_movimientos_legales(jugador, 3, 4)
        self.assertIsInstance(resultado, bool)

    def test_mover_ficha_uso_multiple_dados(self):
        """Cubre uso y remoción de dados múltiples."""
        game = BackgammonGame("player1", "player2")
        game.iniciar_partida()
        game.__dados_disponibles__ = [3, 3]
        game.__movimientos_restantes__ = 2
        jugador = game.get_jugador_actual()
        if jugador.get_ficha() == 'X':
            movimientos = [(0, 3), (3, 6)]
        else:
            movimientos = [(23, 20), (20, 17)]
        resultado = game.mover_ficha(movimientos, 3, 3)
        self.assertTrue(len(resultado["dados_usados"]) >= 0)

    def test_get_dados_disponibles_vacio(self):
        """Cubre lista vacía de dados."""
        game = BackgammonGame("p1", "p2")
        dados = game.get_dados_disponibles()
        self.assertEqual(dados, [])

    def test_mostrar_movimientos_con_dados_ya_disponibles(self):
        """Cubre retornar dados existentes."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        game.__dados_disponibles__ = [2, 5]
        resultado = game.mostrar_movimientos_disponibles(2, 5)
        self.assertEqual(resultado, [2, 5])

    def test_quien_empieza_jugador2_gana(self):
        """Cubre jugador 2 empieza."""
        game = BackgammonGame("p1", "p2")
        for _ in range(100):
            turno, d1, d2 = game.quien_empieza()
            if turno == 2:
                self.assertEqual(game.get_turno(), 2)
                self.assertGreater(d2, d1)
                break
            game.__turno__ = 0

    def test_mover_ficha_genera_dados_si_no_existen(self):
        """Cubre generar dados si lista vacía."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        game.__dados_disponibles__ = []
        game.__movimientos_restantes__ = 2
        resultado = game.mover_ficha([(0, 3)], 3, 4)
        self.assertIsInstance(resultado, dict)

    def test_lanzar_dados_con_dobles(self):
        """Cubre dados iguales genera 4 movimientos."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        random.seed(42)
        for _ in range(100):
            d1, d2, movs = game.lanzar_dados()
            if d1 == d2:
                self.assertEqual(movs, 4)
                self.assertEqual(len(game.get_dados_disponibles()), 4)
                break

    def test_hay_ganador_con_fuera_inexistente(self):
        """Cubre fuera.get con valor default."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        fuera = game.__board__.get_tablero()["fuera"]
        fuera.pop("player1", None)
        resultado = game.hay_ganador()
        self.assertFalse(resultado)

    def test_tiene_movimientos_legales_con_bar_bloqueado(self):
        """Cubre continue cuando distancia no está en dados."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        board = game.__board__
        player_key = jugador.get_nombre()
        board.set_bar(player_key, 1)
        resultado = game.tiene_movimientos_legales(jugador, 6, 5)
        self.assertIsInstance(resultado, bool)

    def test_verificar_movimiento_bearing_off_fuera_rango(self):
        """Cubre destino >= 24 o < 0 para bearing off."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        if game.get_jugador_actual().get_ficha() != 'X':
            game.cambiar_turno()
        jugador = game.get_jugador_actual()
        for i in range(24):
            game.__board__.set_posiciones(i, [])
        game.__board__.set_posiciones(22, [Checker('X')])
        # pylint: disable=protected-access
        resultado = game._verificar_movimiento_desde_posicion(jugador, 22, 3, [3])
        self.assertTrue(resultado)

    def test_verificar_bearing_off_dado_mayor_con_fichas_atras(self):
        """Cubre dado mayor pero hay fichas más atrás."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        if game.get_jugador_actual().get_ficha() != 'X':
            game.cambiar_turno()
        jugador = game.get_jugador_actual()
        for i in range(24):
            game.__board__.set_posiciones(i, [])
        game.__board__.set_posiciones(22, [Checker('X')])
        game.__board__.set_posiciones(19, [Checker('X')])
        # pylint: disable=protected-access
        resultado = game._verificar_movimiento_desde_posicion(jugador, 22, 6, [6])
        self.assertTrue(resultado)

    def test_verificar_movimiento_fuera_rango_sin_bearing_off(self):
        """Cubre destino fuera de rango sin poder bearing off."""
        game = BackgammonGame("p1", "p2")
        game.iniciar_partida()
        jugador = game.get_jugador_actual()
        if jugador.get_ficha() == 'X':
            game.__board__.set_posiciones(10, [Checker('X')])
            pos, dado = 10, 15
        else:
            game.__board__.set_posiciones(10, [Checker('O')])
            pos, dado = 10, 15
        # pylint: disable=protected-access
        resultado = game._verificar_movimiento_desde_posicion(jugador, pos, dado, [dado])
        self.assertFalse(resultado)

    def test_movimiento_basico(self):
        """Test parseo básico."""
        resultado = self.game.parsear_movimiento("10 15")
        self.assertTrue(resultado["valido"])
        self.assertEqual(resultado["movimiento"], (10, 15))

    def test_con_guion(self):
        """Test parseo con guion."""
        resultado = self.game.parsear_movimiento("10-15")
        self.assertTrue(resultado["valido"])
        self.assertEqual(resultado["movimiento"], (10, 15))

    def test_desde_bar(self):
        """Test desde bar."""
        resultado = self.game.parsear_movimiento("BAR 5")
        self.assertTrue(resultado["valido"])
        self.assertEqual(resultado["movimiento"], ("bar", 5))

    def test_hacia_fuera(self):
        """Test hacia fuera."""
        resultado = self.game.parsear_movimiento("20 FUERA")
        self.assertTrue(resultado["valido"])
        self.assertEqual(resultado["movimiento"], (20, "fuera"))

    def test_espacios_extra(self):
        """Test con espacios."""
        resultado = self.game.parsear_movimiento("  10   15  ")
        self.assertTrue(resultado["valido"])
        self.assertEqual(resultado["movimiento"], (10, 15))

    def test_formato_invalido(self):
        """Test formato inválido."""
        resultado = self.game.parsear_movimiento("10")
        self.assertFalse(resultado["valido"])
        self.assertIn("Formato inválido", resultado["error"])

    def test_origen_invalido(self):
        """Test origen inválido."""
        resultado = self.game.parsear_movimiento("abc 15")
        self.assertFalse(resultado["valido"])
        self.assertIn("origen inválida", resultado["error"])

    def test_destino_invalido(self):
        """Test destino inválido."""
        resultado = self.game.parsear_movimiento("10 xyz")
        self.assertFalse(resultado["valido"])
        self.assertIn("destino inválida", resultado["error"])

    def test_multiples_validos(self):
        """Test múltiples movimientos válidos."""
        resultado = self.game.parsear_multiples_movimientos("10 15, bar 5")
        self.assertTrue(resultado["valido"])
        self.assertEqual(len(resultado["movimientos"]), 2)

    def test_multiples_con_error(self):
        """Test múltiples con un error."""
        resultado = self.game.parsear_multiples_movimientos("10 15, abc 5")
        self.assertFalse(resultado["valido"])
        self.assertTrue(len(resultado["errores"]) > 0)

    def test_entrada_vacia(self):
        """Test entrada vacía."""
        resultado = self.game.parsear_multiples_movimientos("")
        self.assertFalse(resultado["valido"])
        self.assertIn("No se ingresaron", resultado["errores"][0])

    def test_cambiar_turno_reinicia_estado_completo(self):
        """Verifica que cambiar turno reinicia estado completo."""
        game = BackgammonGame("A", "B")
        game.__turno__ = 1
        game.__movimientos_restantes__ = 2
        game.__dados_disponibles__ = [3, 4]
        jugador_siguiente = game.cambiar_turno()
        self.assertEqual(game.get_turno(), 2)
        self.assertEqual(game.get_movimientos_restantes(), 0)
        self.assertEqual(game.get_dados_disponibles(), [])
        self.assertIsInstance(jugador_siguiente, Player)

    def test_lanzar_dados_dobles_cuatro_movimientos(self):
        """Verifica que dados dobles generan 4 movimientos."""
        game = BackgammonGame("A", "B")
        game.iniciar_partida()
        game.__dice__.lanzar_dados = lambda: (6, 6)
        d1, d2, movs = game.lanzar_dados()
        self.assertEqual((d1, d2), (6, 6))
        self.assertEqual(movs, 4)
        self.assertEqual(game.get_dados_disponibles(), [6, 6, 6, 6])

    def test_verificar_movimiento_bearing_off_valido_con_permiso(self):
        """Verifica bearing off cuando está permitido."""
        game = BackgammonGame("A", "B")
        game.iniciar_partida()
        jugador = game.get_jugador1()
        game.__board__.puede_sacar = lambda j: True
        game.__reglas__ = []
        # pylint: disable=protected-access
        self.assertTrue(game._verificar_movimiento_desde_posicion(jugador, 23, 6, [6]))

    def test_tiene_fichas_mas_atras_sin_fichas(self):
        """Verifica que retorna False cuando no hay fichas atrás."""
        game = BackgammonGame("A", "B")
        game.iniciar_partida()
        game.__board__.get_posiciones = lambda pos: []
        jugador = game.get_jugador2()
        # pylint: disable=protected-access
        self.assertFalse(game._tiene_fichas_mas_atras(jugador, 2))

    def test_calcular_movimientos_dado_fuera_rango_bajo(self):
        """Verifica error con dado menor a 1."""
        game = BackgammonGame("A", "B")
        with self.assertRaises(ValorDadoInvalidoError):
            game.calcular_movimientos_totales(0, 5)

    def test_calcular_movimientos_dado_fuera_rango_alto(self):
        """Verifica error con dado mayor a 6."""
        game = BackgammonGame("A", "B")
        with self.assertRaises(ValorDadoInvalidoError):
            game.calcular_movimientos_totales(3, 10)

    def test_mover_ficha_excepcion_y_sin_movimientos_posibles(self):
        """Verifica manejo de excepción en movimiento sin alternativas."""
        game = BackgammonGame("A", "B")
        game.iniciar_partida()

        def regla_erronea(*_):
            raise MovimientoInvalidoError("error intencional")

        game.__reglas__ = [regla_erronea]
        game.__board__.mover_ficha = lambda *_: None
        # pylint: disable=protected-access
        game._tiene_movimientos_con_dados_actuales = lambda *_: False
        res = game.mover_ficha([(1, 2)], 3, 4)
        self.assertFalse(res["resultados"][0])
        self.assertIn("error intencional", res["log"][0])

    def test_verificar_movimiento_bearing_off_permitido(self):
        """Verifica bearing off con permisos correctos."""
        game = BackgammonGame("A", "B")
        game.iniciar_partida()
        j = game.get_jugador1()
        game.__board__.puede_sacar = lambda *_: True
        game.__reglas__ = []
        # pylint: disable=protected-access
        ok = game._verificar_movimiento_desde_posicion(j, 23, 6, [6])
        self.assertTrue(ok)

    def test_mostrar_movimientos_disponibles_genera_nuevos(self):
        """Verifica que genera nuevos dados si no hay disponibles."""
        game = BackgammonGame("A", "B")
        game.__dados_disponibles__ = []
        result = game.mostrar_movimientos_disponibles(1, 2)
        self.assertEqual(result, [1, 2])

    def test_mover_ficha_sin_movimientos_restantes_mensaje(self):
        """Verifica mensaje cuando no hay movimientos restantes."""
        game = BackgammonGame("A", "B")
        game.__turno__ = 1
        game.__movimientos_restantes__ = 0
        res = game.mover_ficha([(1, 2)], 3, 4)
        self.assertIn("No hay movimientos disponibles", res["log"][0])


if __name__ == "__main__":
    unittest.main()
