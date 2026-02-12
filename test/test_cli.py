"""
Tests para BackgammonCLI
"""
import unittest
from unittest.mock import patch, Mock
from cli.main import BackgammonCLI
from cli.main import main


class TestLanzarDados(unittest.TestCase):
    """Tests para lanzar dados."""

    @patch('builtins.print')
    def test_sin_movimientos(self, _):
        """Test sin movimientos legales - CLI detecta cambio de turno."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = False
        jugador_antes = Mock()
        jugador_antes.get_nombre.return_value = "player1"
        jugador_despues = Mock()
        jugador_despues.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.side_effect = [
            jugador_antes,
            jugador_despues
        ]
        cli.juego.lanzar_dados.return_value = (3, 4, None)
        cli.lanzar_dados()
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)

class TestMoverFichas(unittest.TestCase):
    """Tests para mover fichas - CORREGIDOS."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_sin_movimientos_iniciales(self, _, __):
        """Test sin movimientos iniciales - Game ya cambió turno."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        cli.dados_lanzados = True
        jugador_inicial = Mock()
        jugador_inicial.get_nombre.return_value = "player1"
        jugador_nuevo = Mock()
        jugador_nuevo.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.return_value = jugador_nuevo
        cli.juego.tiene_movimientos_legales.return_value = False
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_sin_movimientos_con_dados(self, _, mock_input):
        """Test sin movimientos con dados - Game cambia turno automáticamente."""
        mock_input.return_value = "10 15"
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador_inicial = Mock()
        jugador_inicial.get_nombre.return_value = "player1"
        jugador_inicial.get_ficha.return_value = "X"
        jugador_nuevo = Mock()
        jugador_nuevo.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.side_effect = [
            jugador_inicial,
            jugador_inicial,
            jugador_nuevo
        ]
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.return_value = 2
        cli.juego.get_dados_disponibles.return_value = [3]
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": True,
            "movimientos": [(10, 15)]
        }
        cli.juego.mover_ficha.return_value = {
            "resultados": [False],
            "log": []
        }
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_fallido_sin_movimientos_legales(self, _, mock_input):
        """Test movimiento fallido - mover_ficha() cambió turno automáticamente."""
        mock_input.return_value = "10 15"
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador_inicial = Mock()
        jugador_inicial.get_nombre.return_value = "player1"
        jugador_nuevo = Mock()
        jugador_nuevo.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.side_effect = [
            jugador_inicial,
            jugador_inicial,
            jugador_nuevo
        ]
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.return_value = 2
        cli.juego.get_dados_disponibles.return_value = [5, 3]
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": True,
            "movimientos": [(10, 15)]
        }
        cli.juego.mover_ficha.return_value = {
            "resultados": [False],
            "log": []
        }
        cli.juego.hay_ganador.return_value = False
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_fallido_continuar(self, _, mock_input):
        """Test movimiento fallido pero puede continuar."""
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

        cli.juego.get_movimientos_restantes.side_effect = [2, 2, 1, 0, 0]
        cli.juego.get_dados_disponibles.side_effect = [[5, 3], [5, 3], [3], [], []]

        cli.juego.parsear_multiples_movimientos.side_effect = [
            {"valido": True, "movimientos": [(10, 15)]},
            {"valido": True, "movimientos": [(5, 10)]}
        ]

        cli.juego.mover_ficha.side_effect = [
            {"resultados": [False], "log": []},
            {"resultados": [True], "log": []}
        ]
        cli.juego.hay_ganador.return_value = False
        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_exitoso_con_tablero(self, _, mock_input):
        """Test movimiento exitoso con actualización de tablero."""
        mock_input.side_effect = ["10 15", "15 20"]
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 5)
        cli.dados_lanzados = True

        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"

        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.side_effect = [4, 3, 2, 1, 0]
        cli.juego.get_dados_disponibles.side_effect = [
            [5, 5, 5, 5],
            [5, 5, 5],
            [5, 5],
            [5]
        ]

        cli.juego.parsear_multiples_movimientos.side_effect = [
            {"valido": True, "movimientos": [(10, 15)]},
            {"valido": True, "movimientos": [(15, 20)]}
        ]

        cli.juego.mover_ficha.side_effect = [
            {"resultados": [True], "log": []},
            {"resultados": [True], "log": []}
        ]

        cli.juego.hay_ganador.return_value = False

        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

class TestVerificarMovimientos(unittest.TestCase):
    """Tests para verificar movimientos - usa métodos públicos."""

    @patch('builtins.print')
    def test_con_movimientos(self, _):
        """Test con movimientos - usa tiene_movimientos_legales() público."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)

        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"

        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.get_dados_disponibles.return_value = [3, 4]
        cli.juego.tiene_movimientos_legales.return_value = True

        cli.verificar_movimientos_legales()

    @patch('builtins.print')
    def test_sin_movimientos_disponibles(self, _):
        """Test sin movimientos disponibles."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)

        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"

        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.get_dados_disponibles.return_value = [3, 4]
        cli.juego.tiene_movimientos_legales.return_value = False

        cli.verificar_movimientos_legales()


class TestBackgammonCLIInit(unittest.TestCase):
    """Test inicialización."""

    def test_init(self):
        """Verifica inicialización del CLI."""
        cli = BackgammonCLI()
        self.assertIsNone(cli.juego)
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)


class TestParseoMovimientos(unittest.TestCase):
    """Tests para parseo de movimientos."""
    # pylint: disable=protected-access
    @patch('builtins.print')
    def test_procesar_multiples_sin_juego(self, mock_print):
        """Test procesar múltiples sin juego."""
        cli = BackgammonCLI()
        resultado = cli._procesar_entrada_movimientos("10 15")
        self.assertIsNone(resultado)
        mock_print.assert_called_with("Error: No hay juego activo")

    @patch('builtins.print')
    def test_procesar_multiples_validos(self, _):
        """Test procesar múltiples válidos."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": True,
            "movimientos": [(10, 15), (5, 10)]
        }
        resultado = cli._procesar_entrada_movimientos("10 15, 5 10")
        self.assertEqual(len(resultado), 2)

    @patch('builtins.print')
    def test_procesar_multiples_con_errores(self, _):
        """Test procesar múltiples con errores."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": False,
            "errores": ["Error 1", "Error 2"]
        }
        resultado = cli._procesar_entrada_movimientos("abc, xyz")
        self.assertIsNone(resultado)


class TestAccionesSinJuego(unittest.TestCase):
    """Tests para acciones sin juego activo."""

    @patch('builtins.print')
    def test_ver_tablero_sin_juego(self, mock_print):
        """Test ver tablero sin juego."""
        cli = BackgammonCLI()
        cli.ver_tablero()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_ver_estado_sin_juego(self, mock_print):
        """Test ver estado sin juego."""
        cli = BackgammonCLI()
        cli.ver_estado()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_lanzar_dados_sin_juego(self, mock_print):
        """Test lanzar dados sin juego."""
        cli = BackgammonCLI()
        cli.lanzar_dados()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_verificar_sin_juego(self, mock_print):
        """Test verificar movimientos sin juego."""
        cli = BackgammonCLI()
        cli.verificar_movimientos_legales()
        mock_print.assert_called_with("No hay partida en curso.")


class TestAccionesConJuego(unittest.TestCase):
    """Tests para acciones con juego activo."""

    def test_ver_tablero(self):
        """Test ver tablero con juego activo."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.ver_tablero()
        cli.juego.mostrar_tablero.assert_called_once()

    @patch('builtins.print')
    def test_ver_estado_completo(self, _):
        """Test ver estado completo."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        cli.juego.get_dados_disponibles.return_value = [3, 4]
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

    @patch('builtins.print')
    def test_ver_estado_sin_dados(self, _):
        """Test ver estado sin dados actuales."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = None
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


class TestLanzarDadosCompleto(unittest.TestCase):
    """Tests completos para lanzar dados."""

    @patch('builtins.print')
    def test_dados_ya_lanzados(self, _):
        """Test dados ya lanzados."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = True
        cli.lanzar_dados()

    @patch('builtins.print')
    def test_lanzar_exitoso(self, _):
        """Test lanzamiento exitoso."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = False
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.lanzar_dados.return_value = (3, 4, None)
        cli.lanzar_dados()
        self.assertEqual(cli.dados_actuales, (3, 4))
        self.assertTrue(cli.dados_lanzados)


class TestVerificarMovimientosCompleto(unittest.TestCase):
    """Tests completos para verificar movimientos."""

    @patch('builtins.print')
    def test_sin_dados(self, mock_print):
        """Test sin dados."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.verificar_movimientos_legales()
        mock_print.assert_called_with("Debe lanzar los dados primero.")


class TestIniciarPartida(unittest.TestCase):
    """Tests para iniciar partida."""

    @patch('cli.main.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_nombres_vacios(self, _, mock_input, mock_game_class):
        """Test nombres vacíos."""
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


class TestMoverFichasCompleto(unittest.TestCase):
    """Tests completos para mover fichas."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_sin_dados_lanzados(self, _, __):
        """Test sin dados."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = False
        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_cambio_jugador_automatico(self, _, mock_input):
        """Test cambio automático."""
        mock_input.return_value = "10 15"
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador1 = Mock()
        jugador1.get_nombre.return_value = "player1"
        jugador2 = Mock()
        jugador2.get_nombre.return_value = "player2"
        cli.juego.get_jugador_actual.side_effect = [jugador1, jugador2]
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.return_value = 2
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimientos_restantes_cero(self, _, mock_input):
        """Test movimientos = 0."""
        mock_input.return_value = "10 15"
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.return_value = 0
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_entrada_vacia(self, _, mock_input):
        """Test entrada vacía."""
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
        cli.juego.get_movimientos_restantes.side_effect = [2, 2, 0]
        cli.juego.get_dados_disponibles.return_value = [5, 3]
        cli.juego.parsear_multiples_movimientos.side_effect = [
            {"valido": False, "errores": ["No se ingresaron movimientos"]},
            {"valido": True, "movimientos": [(10, 15)]}
        ]
        cli.juego.mover_ficha.return_value = {"resultados": [True], "log": []}
        cli.juego.hay_ganador.return_value = False
        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimientos_lista_vacia(self, _, mock_input):
        """Test movimientos lista vacía."""
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
        cli.juego.get_movimientos_restantes.side_effect = [2, 2, 0]
        cli.juego.get_dados_disponibles.return_value = [5, 3]
        cli.juego.parsear_multiples_movimientos.side_effect = [
            {"valido": True, "movimientos": []},
            {"valido": True, "movimientos": [(10, 15)]}
        ]
        cli.juego.mover_ficha.return_value = {"resultados": [True], "log": []}
        cli.juego.hay_ganador.return_value = False
        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_con_ganador(self, _, mock_input):
        """Test con ganador."""
        mock_input.return_value = "10 15"
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.tiene_movimientos_legales.return_value = True
        cli.juego.get_movimientos_restantes.return_value = 2
        cli.juego.get_dados_disponibles.return_value = [5, 3]
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": True,
            "movimientos": [(10, 15)]
        }
        cli.juego.mover_ficha.return_value = {"resultados": [True], "log": []}
        cli.juego.hay_ganador.return_value = True
        cli.mover_fichas()
        self.assertIsNone(cli.juego)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_fallido_cambio_turno(self, _, mock_input):
        """Test movimiento fallido con cambio."""
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
        cli.juego.get_dados_disponibles.return_value = [5, 3]
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": True,
            "movimientos": [(10, 15)]
        }
        cli.juego.mover_ficha.return_value = {"resultados": [False], "log": []}
        cli.juego.hay_ganador.return_value = False
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)


class TestMetodosPrivados(unittest.TestCase):
    """Tests para métodos privados."""
    # pylint: disable=protected-access

    @patch('builtins.print')
    def test_mostrar_info_turno_x(self, _):
        """Test info turno X."""
        cli = BackgammonCLI()
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli._mostrar_info_turno(jugador)

    @patch('builtins.print')
    def test_mostrar_info_turno_o(self, _):
        """Test info turno O."""
        cli = BackgammonCLI()
        jugador = Mock()
        jugador.get_nombre.return_value = "player2"
        jugador.get_ficha.return_value = "O"
        cli._mostrar_info_turno(jugador)

    @patch('builtins.print')
    def test_mostrar_instrucciones(self, _):
        """Test mostrar instrucciones."""
        cli = BackgammonCLI()
        cli._mostrar_instrucciones()


class TestMenus(unittest.TestCase):
    """Tests para menús."""

    @patch('builtins.print')
    def test_menu_principal(self, _):
        """Test menú principal."""
        BackgammonCLI().mostrar_menu_principal()

    @patch('builtins.print')
    def test_menu_juego(self, _):
        """Test menú juego."""
        BackgammonCLI().mostrar_menu_juego()


class TestEjecutar(unittest.TestCase):
    """Tests para bucle principal."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_salir(self, _, mock_input):
        """Test salir."""
        mock_input.return_value = "2"
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_opcion_invalida_principal(self, _, mock_input):
        """Test opción inválida principal."""
        mock_input.side_effect = ["9", "2"]
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_opcion_invalida_juego(self, _, mock_input):
        """Test opción inválida juego."""
        mock_input.side_effect = ["1", "", "", "9", "6", "2"]
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_ver_tablero_desde_menu(self, _, mock_input):
        """Test ver tablero desde menú."""
        mock_input.side_effect = ["1", "", "", "1", "6", "2"]
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_ver_estado_desde_menu(self, _, mock_input):
        """Test ver estado desde menú."""
        mock_input.side_effect = ["1", "", "", "2", "6", "2"]
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_lanzar_dados_desde_menu(self, _, mock_input):
        """Test lanzar dados desde menú."""
        mock_input.side_effect = ["1", "", "", "3", "6", "2"]
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_verificar_movimientos_desde_menu(self, _, mock_input):
        """Test verificar desde menú."""
        mock_input.side_effect = ["1", "", "", "5", "6", "2"]
        cli = BackgammonCLI()
        cli.ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_volver_menu_principal(self, _, mock_input):
        """Test volver al menú principal."""
        mock_input.side_effect = ["1", "", "", "6", "2"]
        cli = BackgammonCLI()
        cli.ejecutar()
        self.assertIsNone(cli.juego)
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)


class TestMain(unittest.TestCase):
    """Tests para función main."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_main_normal(self, _, mock_input):
        """Test main normal."""
        mock_input.return_value = "2"
        main()

    @patch('cli.main.BackgammonCLI')
    @patch('builtins.print')
    def test_main_keyboard_interrupt(self, mock_print, mock_cli_class):
        """Test Ctrl+C."""
        mock_cli = Mock()
        mock_cli_class.return_value = mock_cli
        mock_cli.ejecutar.side_effect = KeyboardInterrupt()
        main()
        calls = [str(call) for call in mock_print.call_args_list]
        assert any("interrumpido" in str(call).lower() for call in calls)


if __name__ == '__main__':
    unittest.main()
