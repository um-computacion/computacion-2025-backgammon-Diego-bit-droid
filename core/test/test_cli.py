"""
Tests optimizados para BackgammonCLI - Sin duplicados, 100% cobertura
"""
import unittest
from unittest.mock import patch, Mock
from cli.main import BackgammonCLI
from cli.main import main

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

    @patch('builtins.print')
    def test_parseo_sin_juego(self, mock_print):
        """Test parseo sin juego activo - cubre líneas 203-204."""
        cli = BackgammonCLI()
        resultado = cli.parsear_movimiento("10 15")
        self.assertIsNone(resultado)
        mock_print.assert_called_with("Error: No hay juego activo")

    @patch('builtins.print')
    def test_parseo_valido(self, _):
        """Test parseo válido - cubre líneas 206-212."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.juego.parsear_movimiento.return_value = {
            "valido": True,
            "movimiento": (10, 15)
        }
        resultado = cli.parsear_movimiento("10 15")
        self.assertEqual(resultado, (10, 15))

    @patch('builtins.print')
    def test_parseo_invalido(self, mock_print):
        """Test parseo inválido - cubre líneas 208-210."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.juego.parsear_movimiento.return_value = {
            "valido": False,
            "error": "Formato inválido"
        }
        resultado = cli.parsear_movimiento("abc")
        self.assertIsNone(resultado)
        mock_print.assert_called_with("Error: Formato inválido")

    @patch('builtins.print')
    def test_procesar_multiples_sin_juego(self, mock_print):
        """Test procesar múltiples sin juego - cubre líneas 235-236."""
        cli = BackgammonCLI()
        # pylint: disable=protected-access
        resultado = cli._procesar_entrada_movimientos("10 15")
        self.assertIsNone(resultado)
        mock_print.assert_called_with("Error: No hay juego activo")

    @patch('builtins.print')
    def test_procesar_multiples_validos(self, _):
        """Test procesar múltiples válidos - cubre líneas 238-246."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": True,
            "movimientos": [(10, 15), (5, 10)]
        }
        # pylint: disable=protected-access
        resultado = cli._procesar_entrada_movimientos("10 15, 5 10")
        self.assertEqual(len(resultado), 2)

    @patch('builtins.print')
    def test_procesar_multiples_con_errores(self, _):
        """Test procesar múltiples con errores - cubre líneas 240-243."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.juego.parsear_multiples_movimientos.return_value = {
            "valido": False,
            "errores": ["Error 1", "Error 2"]
        }
        # pylint: disable=protected-access
        resultado = cli._procesar_entrada_movimientos("abc, xyz")
        self.assertIsNone(resultado)


class TestAccionesSinJuego(unittest.TestCase):
    """Tests para acciones sin juego activo."""

    @patch('builtins.print')
    def test_ver_tablero_sin_juego(self, mock_print):
        """Test ver tablero sin juego - cubre líneas 70-71."""
        cli = BackgammonCLI()
        cli.ver_tablero()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_ver_estado_sin_juego(self, mock_print):
        """Test ver estado sin juego - cubre líneas 78-79."""
        cli = BackgammonCLI()
        cli.ver_estado()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_lanzar_dados_sin_juego(self, mock_print):
        """Test lanzar dados sin juego - cubre líneas 117-118."""
        cli = BackgammonCLI()
        cli.lanzar_dados()
        mock_print.assert_called_with("No hay partida en curso.")

    @patch('builtins.print')
    def test_verificar_sin_juego(self, mock_print):
        """Test verificar movimientos sin juego - cubre líneas 150-151."""
        cli = BackgammonCLI()
        cli.verificar_movimientos_legales()
        mock_print.assert_called_with("No hay partida en curso.")


class TestAccionesConJuego(unittest.TestCase):
    """Tests para acciones con juego activo."""

    def test_ver_tablero(self):
        """Test ver tablero con juego activo - cubre líneas 73-74."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.ver_tablero()
        cli.juego.mostrar_tablero.assert_called_once()

    @patch('builtins.print')
    def test_ver_estado_completo(self, _):
        """Test ver estado completo - cubre líneas 81-110."""
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
        """Test ver estado sin dados actuales - cubre línea 91."""
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


class TestLanzarDados(unittest.TestCase):
    """Tests para lanzar dados."""

    @patch('builtins.print')
    def test_dados_ya_lanzados(self, _):
        """Test dados ya lanzados - cubre líneas 120-123."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = True
        cli.lanzar_dados()

    @patch('builtins.print')
    def test_lanzar_exitoso(self, _):
        """Test lanzamiento exitoso - cubre líneas 125-140."""
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
    def test_sin_movimientos(self, _):
        """Test sin movimientos legales - cubre líneas 133-147."""
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


class TestVerificarMovimientos(unittest.TestCase):
    """Tests para verificar movimientos."""

    @patch('builtins.print')
    def test_sin_dados(self, mock_print):
        """Test sin dados - cubre líneas 153-154."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.verificar_movimientos_legales()
        mock_print.assert_called_with("Debe lanzar los dados primero.")

    @patch('builtins.print')
    def test_con_movimientos(self, _):
        """Test con movimientos - cubre líneas 156-167."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.get_dados_disponibles.return_value = [3, 4]
        # pylint: disable=protected-access
        cli.juego._tiene_movimientos_con_dados_actuales.return_value = True
        cli.verificar_movimientos_legales()

    @patch('builtins.print')
    def test_sin_movimientos_disponibles(self, _):
        """Test sin movimientos disponibles - cubre líneas 168-171."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_actuales = (3, 4)
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli.juego.get_jugador_actual.return_value = jugador
        cli.juego.get_dados_disponibles.return_value = [3, 4]
        # pylint: disable=protected-access
        cli.juego._tiene_movimientos_con_dados_actuales.return_value = False
        cli.verificar_movimientos_legales()


class TestIniciarPartida(unittest.TestCase):
    """Tests para iniciar partida."""

    @patch('cli.main.BackgammonGame')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_nombres_vacios(self, _, mock_input, mock_game_class):
        """Test nombres vacíos - cubre líneas 47-67."""
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


class TestMoverFichas(unittest.TestCase):
    """Tests para mover fichas."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_sin_dados_lanzados(self, _, __):
        """Test sin dados - cubre líneas 249-251."""
        cli = BackgammonCLI()
        cli.juego = Mock()
        cli.dados_lanzados = False
        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_sin_movimientos_iniciales(self, _, __):
        """Test sin movimientos iniciales - cubre líneas 260-268."""
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

    @patch('builtins.input')
    @patch('builtins.print')
    def test_cambio_jugador_automatico(self, _, mock_input):
        """Test cambio automático - cubre líneas 282-292."""
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
        """Test movimientos = 0 - cubre líneas 294-299."""
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
    def test_sin_movimientos_con_dados(self, _, mock_input):
        """Test sin movimientos con dados - cubre líneas 301-317."""
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
        cli.juego.get_dados_disponibles.return_value = [3]
        # pylint: disable=protected-access
        cli.juego._tiene_movimientos_con_dados_actuales.return_value = False
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_entrada_vacia(self, _, mock_input):
        """Test entrada vacía - continúa loop - cubre línea 325."""
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
        """Test movimientos lista vacía - cubre líneas 327-329."""
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
        """Test con ganador - cubre líneas 352-359."""
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
        """Test movimiento fallido con cambio - cubre líneas 341-351."""
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

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_fallido_sin_movimientos_legales(self, _, mock_input):
        """Test movimiento fallido sin movimientos legales - cubre líneas 353-367."""
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
        cli.juego.mover_ficha.return_value = {"resultados": [False], "log": []}
        cli.juego.hay_ganador.return_value = False
        # pylint: disable=protected-access
        cli.juego._tiene_movimientos_con_dados_actuales.return_value = False
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_fallido_continuar(self, _, mock_input):
        """Test movimiento fallido pero puede continuar - cubre líneas 368-378."""
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
        cli.juego.get_movimientos_restantes.side_effect = [2, 2, 1, 0]
        cli.juego.get_dados_disponibles.side_effect = [[5, 3], [5, 3], [3], []]
        cli.juego.parsear_multiples_movimientos.side_effect = [
            {"valido": True, "movimientos": [(10, 15)]},
            {"valido": True, "movimientos": [(5, 10)]}
        ]
        cli.juego.mover_ficha.side_effect = [
            {"resultados": [False], "log": []},
            {"resultados": [True], "log": []}
        ]
        cli.juego.hay_ganador.return_value = False
        # pylint: disable=protected-access
        cli.juego._tiene_movimientos_con_dados_actuales.side_effect = [True, False]
        cli.mover_fichas()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_movimiento_exitoso_con_tablero(self, _, mock_input):
        """Test movimiento exitoso - cubre líneas 380-401."""
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
        cli.juego.get_dados_disponibles.side_effect = [[5, 5, 5, 5], [5, 5, 5], [5, 5], [5]]
        cli.juego.parsear_multiples_movimientos.side_effect = [
            {"valido": True, "movimientos": [(10, 15)]},
            {"valido": True, "movimientos": [(15, 20)]}
        ]
        cli.juego.mover_ficha.side_effect = [
            {"resultados": [True], "log": []},
            {"resultados": [True], "log": []}
        ]
        cli.juego.hay_ganador.return_value = False
        # pylint: disable=protected-access
        cli.juego._tiene_movimientos_con_dados_actuales.side_effect = [True, False]
        cli.mover_fichas()
        self.assertIsNone(cli.dados_actuales)


class TestMetodosPrivados(unittest.TestCase):
    """Tests para métodos privados."""

    @patch('builtins.print')
    def test_mostrar_info_turno_x(self, _):
        """Test info turno X - cubre líneas 214-220."""
        # pylint: disable=protected-access
        cli = BackgammonCLI()
        jugador = Mock()
        jugador.get_nombre.return_value = "player1"
        jugador.get_ficha.return_value = "X"
        cli._mostrar_info_turno(jugador)
    @patch('builtins.print')
    def test_mostrar_info_turno_o(self, _):
        # pylint: disable=protected-access
        """Test info turno O - cubre líneas 221-223."""
        cli = BackgammonCLI()
        jugador = Mock()
        jugador.get_nombre.return_value = "player2"
        jugador.get_ficha.return_value = "O"
        cli._mostrar_info_turno(jugador)

    @patch('builtins.print')
    def test_mostrar_instrucciones(self, _):
          # pylint: disable=protected-access
        """Test mostrar instrucciones - cubre líneas 225-230."""
        cli = BackgammonCLI()
        cli._mostrar_instrucciones()


class TestMenus(unittest.TestCase):
    """Tests para menús."""

    @patch('builtins.print')
    def test_menu_principal(self, _):
        """Test menú principal - cubre líneas 20-26."""
        BackgammonCLI().mostrar_menu_principal()

    @patch('builtins.print')
    def test_menu_juego(self, _):
        """Test menú juego - cubre líneas 28-37."""
        BackgammonCLI().mostrar_menu_juego()


class TestEjecutar(unittest.TestCase):
    """Tests para bucle principal."""

    @patch('builtins.input')
    @patch('builtins.print')
    def test_salir(self, _, mock_input):
        """Test salir - cubre línea 426."""
        mock_input.return_value = "2"
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_opcion_invalida_principal(self, _, mock_input):
        """Test opción inválida principal - cubre línea 432."""
        mock_input.side_effect = ["9", "2"]
        BackgammonCLI().ejecutar()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_opcion_invalida_juego(self, _, mock_input):
        """Test opción inválida juego - cubre línea 454."""
        mock_input.side_effect = ["1", "", "", "9", "6", "2"]
        BackgammonCLI().ejecutar()
    @patch('builtins.input')
    @patch('builtins.print')
    def test_ver_tablero_desde_menu(self, _, mock_input):
        """Test ver tablero desde menú - cubre línea 428."""
        mock_input.side_effect = ["1", "", "", "1", "6", "2"]
        BackgammonCLI().ejecutar()
    @patch('builtins.input')
    @patch('builtins.print')
    def test_ver_estado_desde_menu(self, _, mock_input):
        """Test ver estado desde menú - cubre línea 430."""
        mock_input.side_effect = ["1", "", "", "2", "6", "2"]
        BackgammonCLI().ejecutar()
    @patch('builtins.input')
    @patch('builtins.print')
    def test_lanzar_dados_desde_menu(self, _, mock_input):
        """Test lanzar dados desde menú - cubre línea 432."""
        mock_input.side_effect = ["1", "", "", "3", "6", "2"]
        BackgammonCLI().ejecutar()
    @patch('builtins.input')
    @patch('builtins.print')
    def test_verificar_movimientos_desde_menu(self, _, mock_input):
        """Test verificar desde menú - cubre línea 436."""
        mock_input.side_effect = ["1", "", "", "5", "6", "2"]
        cli = BackgammonCLI()
        cli.ejecutar()
    @patch('builtins.input')
    @patch('builtins.print')
    def test_volver_menu_principal(self, _, mock_input):
        """Test volver al menú principal - cubre líneas 438-442."""
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
