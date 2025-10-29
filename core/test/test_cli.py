"""
Tests optimizados para BackgammonCLI.
Eliminando redundancias y simplificando verificaciones.
"""
import unittest
from unittest.mock import patch, Mock
from cli.main import BackgammonCLI


class TestBackgammonCLIInit(unittest.TestCase):
    """Tests para la inicialización del CLI."""

    def test_init_sin_juego(self):
        """Verifica que el CLI se inicialice sin juego activo."""
        cli = BackgammonCLI()
        self.assertIsNone(cli.juego)
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)


class TestBackgammonCLIParsearMovimiento(unittest.TestCase):
    """Tests para el parseo de movimientos."""

    def setUp(self):
        """Configura el CLI para cada test."""
        self.cli = BackgammonCLI()

    def test_parsear_movimiento_basico(self):
        """Verifica parseo básico de movimiento."""
        desde, hasta = self.cli.parsear_movimiento("10 15")
        self.assertEqual((desde, hasta), (10, 15))

    def test_parsear_con_guion(self):
        """Verifica parseo con guion."""
        desde, hasta = self.cli.parsear_movimiento("10-15")
        self.assertEqual((desde, hasta), (10, 15))

    def test_parsear_desde_bar(self):
        """Verifica parseo desde bar (case insensitive)."""
        desde, hasta = self.cli.parsear_movimiento("BAR 5")
        self.assertEqual((desde, hasta), ("bar", 5))

    def test_parsear_hacia_fuera(self):
        """Verifica parseo hacia fuera del tablero (case insensitive)."""
        desde, hasta = self.cli.parsear_movimiento("20 FUERA")
        self.assertEqual((desde, hasta), (20, "fuera"))

    def test_parsear_espacios_extra(self):
        """Verifica parseo con espacios extra."""
        desde, hasta = self.cli.parsear_movimiento("  10   15  ")
        self.assertEqual((desde, hasta), (10, 15))

    def test_parsear_formato_invalido(self):
        """Verifica que se lance error con formato inválido."""
        with self.assertRaises(ValueError):
            self.cli.parsear_movimiento("10")

    def test_parsear_origen_invalido(self):
        """Verifica que se lance error con origen inválido."""
        with self.assertRaises(ValueError):
            self.cli.parsear_movimiento("abc 15")

    def test_parsear_destino_invalido(self):
        """Verifica que se lance error con destino inválido."""
        with self.assertRaises(ValueError):
            self.cli.parsear_movimiento("10 xyz")


class TestBackgammonCLIAcciones(unittest.TestCase):
    """Tests para acciones del CLI."""

    @patch('builtins.print')
    def test_ver_tablero_sin_juego(self, mock_print):
        """Verifica ver tablero sin juego activo."""
        cli = BackgammonCLI()
        cli.ver_tablero()
        mock_print.assert_called_with("No hay partida en curso.")

    def test_ver_tablero_con_juego(self):
        """Verifica ver tablero con juego activo."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.ver_tablero()
        cli.juego.mostrar_tablero.assert_called_once()

    @patch('builtins.print')
    def test_ver_estado_sin_juego(self, mock_print):
        """Verifica ver estado sin juego activo."""
        cli = BackgammonCLI()
        cli.ver_estado()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_ver_estado_con_juego(self, mock_print):
        """Verifica ver estado con juego activo e iniciado."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        cli.juego.get_estado_juego.return_value = {
            'jugador_actual': 'player1',
            'movimientos_restantes': 2,
            'jugador1': {
                'nombre': 'player1',
                'ficha': 'X',
                'fichas_tablero': 15,
                'fichas_bar': 0,
                'fichas_sacadas': 0
            },
            'jugador2': {
                'nombre': 'player2',
                'ficha': 'O',
                'fichas_tablero': 15,
                'fichas_bar': 0,
                'fichas_sacadas': 0
            }
        }
        cli.ver_estado()
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    def test_ver_estado_sin_iniciar(self, mock_print):
        """Verifica ver estado cuando el juego no ha iniciado."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.juego.get_estado_juego.return_value = {
            'jugador_actual': None,
            'movimientos_restantes': 0,
            'jugador1': {
                'nombre': 'player1',
                'ficha': 'X',
                'fichas_tablero': 15,
                'fichas_bar': 0,
                'fichas_sacadas': 0
            },
            'jugador2': {
                'nombre': 'player2',
                'ficha': 'O',
                'fichas_tablero': 15,
                'fichas_bar': 0,
                'fichas_sacadas': 0
            }
        }
        cli.ver_estado()
        self.assertTrue(mock_print.called)


class TestBackgammonCLILanzarDados(unittest.TestCase):
    """Tests para lanzar dados."""

    @patch('builtins.print')
    def test_lanzar_dados_sin_juego(self, mock_print):
        """Verifica lanzar dados sin juego activo."""
        cli = BackgammonCLI()
        cli.lanzar_dados()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_lanzar_dados_ya_lanzados(self, mock_print):
        """Verifica que no se puedan lanzar dados dos veces."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = True
        cli.lanzar_dados()
        self.assertTrue(mock_print.called)

    @patch('builtins.print')
    def test_lanzar_dados_exitoso(self, _):
        """Verifica lanzamiento exitoso de dados."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = False
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.lanzar_dados.return_value = (3, 4, None)
        cli.juego.tiene_movimientos_legales.return_value = True

        cli.lanzar_dados()

        self.assertEqual(cli.dados_actuales, (3, 4))
        self.assertTrue(cli.dados_lanzados)

    @patch('builtins.print')
    def test_lanzar_dados_sin_movimientos(self, _):
        """Verifica lanzar dados sin movimientos legales disponibles."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = False
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador_nuevo = Mock()
        jugador_nuevo.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.lanzar_dados.return_value = (3, 4, None)
        cli.juego.tiene_movimientos_legales.return_value = False
        cli.juego.cambiar_turno.return_value = jugador_nuevo

        cli.lanzar_dados()

        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)


class TestBackgammonCLIVerificarMovimientos(unittest.TestCase):
    """Tests para verificar movimientos."""

    @patch('builtins.print')
    def test_verificar_sin_juego(self, mock_print):
        """Verifica verificación sin juego activo."""
        cli = BackgammonCLI()
        cli.verificar_movimientos_legales()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_verificar_sin_dados(self, mock_print):
        """Verifica verificación sin dados lanzados."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.verificar_movimientos_legales()
        mock_print.assert_called_with("Debe lanzar los dados primero.")

    @patch('builtins.print')
    def test_verificar_con_movimientos(self, _):
        """Verifica que existan movimientos legales."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = True

        cli.verificar_movimientos_legales()

    @patch('builtins.print')
    def test_verificar_sin_movimientos_disponibles(self, _):
        """Verifica cuando no hay movimientos legales."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = False

        cli.verificar_movimientos_legales()


class TestBackgammonCLIPasarTurno(unittest.TestCase):
    """Tests para pasar turno."""

    @patch('builtins.print')
    def test_pasar_turno_sin_juego(self, mock_print):
        """Verifica pasar turno sin juego activo."""
        cli = BackgammonCLI()
        cli.pasar_turno()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_pasar_turno_exitoso(self, _):
        """Verifica pasar turno exitosamente."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        jugador1 = Mock()
        jugador1.get_nombre.return_value = "player1"
        jugador2 = Mock()
        jugador2.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.return_value = jugador1
        cli.juego.cambiar_turno.return_value = jugador2

        cli.pasar_turno()

        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)


class TestBackgammonCLIIniciarPartida(unittest.TestCase):
    """Tests para iniciar partida."""

    @patch('cli.main.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_nombres_vacios(self, _, mock_input, mock_game_class):
        """Verifica inicio con nombres vacíos (usa nombres por defecto)."""
        mock_input.side_effect = ["", ""]
        mock_game = Mock()
        mock_game_class.return_value = mock_game
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        mock_game.quien_empieza.return_value = (jugador, 3, 4)
        mock_game.get_jugador_actual.return_value = jugador
        mock_game.lanzar_dados.return_value = (5, 6, None)

        cli = BackgammonCLI()
        cli.iniciar_nueva_partida()

        self.assertIsNotNone(cli.juego)
        self.assertTrue(cli.dados_lanzados)

    @patch('cli.main.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_iniciar_con_nombres_personalizados(self, _, mock_input, mock_game_class):
        """Verifica inicio de partida con nombres personalizados."""
        mock_input.side_effect = ["Alice", "Bob"]
        mock_game = Mock()
        mock_game_class.return_value = mock_game
        jugador = Mock()
        jugador.get_nombre.return_value = "Alice"
        mock_game.quien_empieza.return_value = (jugador, 3, 4)
        mock_game.get_jugador_actual.return_value = jugador
        mock_game.lanzar_dados.return_value = (5, 6, None)

        cli = BackgammonCLI()
        cli.iniciar_nueva_partida()

        mock_game_class.assert_called_once_with("Alice", "Bob")
        self.assertIsNotNone(cli.juego)
        self.assertEqual(cli.dados_actuales, (5, 6))


class TestBackgammonCLIMoverFichas(unittest.TestCase):
    """Tests para mover fichas."""

    @patch('builtins.print')
    def test_mover_sin_juego(self, _):
        """Verifica mover sin juego activo."""
        cli = BackgammonCLI()
        cli.mover_fichas()

    @patch('builtins.print')
    def test_mover_sin_dados(self, _):
        """Verifica mover sin dados lanzados."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_mover_sin_movimientos_legales(self, _, __):
        """Verifica cuando no hay movimientos legales disponibles."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        cli.dados_lanzados = True
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador_nuevo = Mock()
        jugador_nuevo.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = False
        cli.juego.cambiar_turno.return_value = jugador_nuevo

        cli.mover_fichas()

        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_mover_con_ganador(self, _, mock_input):
        """Verifica movimiento que resulta en victoria."""
        mock_input.return_value = "10 15"
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.return_value = 2
        cli.juego.mover_ficha.return_value = {"resultados": [True]}
        cli.juego.hay_ganador.return_value = True

        cli.mover_fichas()

        self.assertIsNone(cli.juego)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_mover_entrada_vacia(self, _, mock_input):
        """Verifica manejo de entrada vacía."""
        mock_input.side_effect = ["", "10 15"]
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.side_effect = [2, 1, 0]
        cli.juego.mover_ficha.return_value = {"resultados": [True]}
        cli.juego.hay_ganador.return_value = False

        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_mover_movimiento_fallido(self, _, mock_input):
        """Verifica manejo de movimiento que falla."""
        mock_input.side_effect = ["10 15", "5 10"]
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.side_effect = [2, 2, 1, 1, 0]
        cli.juego.mover_ficha.side_effect = [
            {"resultados": [False]},
            {"resultados": [True]}
        ]
        cli.juego.hay_ganador.return_value = False

        cli.mover_fichas()
        self.assertTrue(cli.juego.mostrar_tablero.call_count >= 2)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_mover_cambio_jugador(self, _, mock_input):
        """Verifica cambio de jugador durante movimientos."""
        mock_input.return_value = "10 15"
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador1 = Mock()
        jugador1.get_nombre.return_value = "player1"
        jugador1.get_ficha.return_value = "X"
        jugador2 = Mock()
        jugador2.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.side_effect = [jugador1, jugador1, jugador2]
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.return_value = 2
        cli.juego.mover_ficha.return_value = {"resultados": [True]}
        cli.juego.hay_ganador.return_value = False

        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)


class TestBackgammonCLIMetodosPrivados(unittest.TestCase):
    """Tests para métodos privados."""

    @patch('builtins.print')
    def test_mostrar_info_turno_x(self, _):
        """Verifica mostrar info para jugador X."""
        cli = BackgammonCLI()
        cli.dados_actuales = (3, 4)
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        # pylint: disable=protected-access
        cli._mostrar_info_turno(jugador)

    @patch('builtins.print')
    def test_mostrar_info_turno_o(self, _):
        """Verifica mostrar info para jugador O."""
        cli = BackgammonCLI()
        cli.dados_actuales = (5, 2)
        jugador = Mock()
        jugador.get_nombre.return_value = "player2"
        jugador.get_ficha.return_value = "O"
        # pylint: disable=protected-access
        cli._mostrar_info_turno(jugador)

    @patch('builtins.print')
    def test_mostrar_instrucciones(self, _):
        """Verifica mostrar instrucciones."""
        cli = BackgammonCLI()
        # pylint: disable=protected-access
        cli._mostrar_instrucciones()

    @patch('builtins.print')
    def test_procesar_entrada_valida(self, _):
        """Verifica procesamiento de entrada válida."""
        cli = BackgammonCLI()
        # pylint: disable=protected-access
        movimientos = cli._procesar_entrada_movimientos("10 15, bar 5")
        self.assertEqual(len(movimientos), 2)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], ("bar", 5))

    @patch('builtins.print')
    def test_procesar_entrada_invalida(self, _):
        """Verifica procesamiento de entrada inválida."""
        cli = BackgammonCLI()
        # pylint: disable=protected-access
        movimientos = cli._procesar_entrada_movimientos("10 abc")
        self.assertIsNone(movimientos)

    @patch('builtins.print')
    def test_finalizar_turno(self, _):
        """Verifica finalización de turno."""
        cli = BackgammonCLI()
        cli.dados_actuales = (3, 4)
        # pylint: disable=protected-access
        cli._finalizar_turno()
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)

    @patch('builtins.print')
    def test_mostrar_tablero_con_dados(self, _):
        """Verifica mostrar tablero con dados."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        # pylint: disable=protected-access
        cli._mostrar_tablero_con_dados()
        cli.juego.mostrar_tablero.assert_called_once()


class TestBackgammonCLIMenus(unittest.TestCase):
    """Tests para los menús del CLI."""

    @patch('builtins.print')
    def test_mostrar_menu_principal(self, _):
        """Verifica que se muestre el menú principal."""
        cli = BackgammonCLI()
        cli.mostrar_menu_principal()

    @patch('builtins.print')
    def test_mostrar_menu_juego(self, _):
        """Verifica que se muestre el menú de juego."""
        cli = BackgammonCLI()
        cli.mostrar_menu_juego()


class TestBackgammonCLIEjecutar(unittest.TestCase):
    """Tests para bucle principal."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_ejecutar_salir(self, _, mock_input):
        """Verifica salir del programa."""
        mock_input.return_value = "2"
        cli = BackgammonCLI()
        cli.ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_ejecutar_opcion_invalida_menu_principal(self, _, mock_input):
        """Verifica manejo de opción inválida en menú principal."""
        mock_input.side_effect = ["9", "2"]
        cli = BackgammonCLI()
        cli.ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_ejecutar_opcion_invalida_menu_juego(self, _, mock_input):
        """Verifica manejo de opción inválida en menú de juego."""
        mock_input.side_effect = ["1", "", "", "9", "6", "2"]
        cli = BackgammonCLI()
        with patch.object(cli, 'iniciar_nueva_partida'):
            cli.juego = Mock()
            cli.ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_ejecutar_volver_menu_principal(self, _, mock_input):
        """Verifica volver al menú principal desde el juego."""
        mock_input.side_effect = ["1", "", "", "6", "2"]
        cli = BackgammonCLI()
        with patch.object(cli, 'iniciar_nueva_partida'):
            cli.juego = Mock()
            cli.ejecutar()
        self.assertIsNone(cli.juego)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_ejecutar_opciones_menu_juego(self, _, mock_input):
        """Verifica navegación por opciones del menú de juego."""
        mock_input.side_effect = ["1", "1", "2", "3", "4", "5", "6", "2"]
        cli = BackgammonCLI()

        with patch.object(cli, 'iniciar_nueva_partida'):
            with patch.object(cli, 'ver_tablero'):
                with patch.object(cli, 'ver_estado'):
                    with patch.object(cli, 'lanzar_dados'):
                        with patch.object(cli, 'mover_fichas'):
                            with patch.object(cli, 'verificar_movimientos_legales'):
                                cli.juego = Mock()
                                cli.ejecutar()

        self.assertIsNone(cli.juego)


if __name__ == '__main__':
    unittest.main()
