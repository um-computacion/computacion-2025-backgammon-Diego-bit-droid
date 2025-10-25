"""
Tests para BackgammonCLI.
Prueba la lógica del CLI sin interacción del usuario.
"""
import unittest
from main.cli import BackgammonCLI


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

    def test_parsear_movimiento_formato_espacio(self):
        """Prueba parseo con formato 'desde hasta'."""
        desde, hasta = self.cli.parsear_movimiento("10 15")
        self.assertEqual(desde, 10)
        self.assertEqual(hasta, 15)

    def test_parsear_movimiento_formato_guion(self):
        """Prueba parseo con formato 'desde-hasta'."""
        desde, hasta = self.cli.parsear_movimiento("10-15")
        self.assertEqual(desde, 10)
        self.assertEqual(hasta, 15)

    def test_parsear_movimiento_desde_bar(self):
        """Prueba parseo desde bar."""
        desde, hasta = self.cli.parsear_movimiento("bar 5")
        self.assertEqual(desde, "bar")
        self.assertEqual(hasta, 5)

    def test_parsear_movimiento_hacia_fuera(self):
        """Prueba parseo para sacar ficha."""
        desde, hasta = self.cli.parsear_movimiento("20 fuera")
        self.assertEqual(desde, 20)
        self.assertEqual(hasta, "fuera")

    def test_parsear_movimiento_case_insensitive(self):
        """Verifica que el parseo no sea sensible a mayúsculas."""
        desde, hasta = self.cli.parsear_movimiento("BAR 5")
        self.assertEqual(desde, "bar")
        self.assertEqual(hasta, 5)

        desde, hasta = self.cli.parsear_movimiento("20 FUERA")
        self.assertEqual(desde, 20)
        self.assertEqual(hasta, "fuera")

    def test_parsear_movimiento_con_espacios_extra(self):
        """Verifica que se manejen espacios adicionales."""
        desde, hasta = self.cli.parsear_movimiento("  10   15  ")
        self.assertEqual(desde, 10)
        self.assertEqual(hasta, 15)

    def test_parsear_movimiento_formato_invalido(self):
        """Verifica error con formato inválido."""
        with self.assertRaises(ValueError) as context:
            self.cli.parsear_movimiento("10")
        self.assertIn("Formato inválido", str(context.exception))

    def test_parsear_movimiento_origen_invalido(self):
        """Verifica error con posición de origen no numérica."""
        with self.assertRaises(ValueError) as context:
            self.cli.parsear_movimiento("abc 15")
        self.assertIn("Posición de origen inválida", str(context.exception))

    def test_parsear_movimiento_destino_invalido(self):
        """Verifica error con posición de destino no numérica."""
        with self.assertRaises(ValueError) as context:
            self.cli.parsear_movimiento("10 xyz")
        self.assertIn("Posición de destino inválida", str(context.exception))

    def test_parsear_posiciones_limite(self):
        """Verifica parseo de posiciones límite."""
        desde1, hasta1 = self.cli.parsear_movimiento("0 5")
        desde2, hasta2 = self.cli.parsear_movimiento("23 18")
        self.assertEqual(desde1, 0)
        self.assertEqual(hasta1, 5)
        self.assertEqual(desde2, 23)
        self.assertEqual(hasta2, 18)

    def test_parsear_bar_con_guion(self):
        """Verifica parseo desde bar con guión."""
        desde, hasta = self.cli.parsear_movimiento("bar-5")
        self.assertEqual(desde, "bar")
        self.assertEqual(hasta, 5)

    def test_parsear_fuera_con_guion(self):
        """Verifica parseo hacia fuera con guión."""
        desde, hasta = self.cli.parsear_movimiento("20-fuera")
        self.assertEqual(desde, 20)
        self.assertEqual(hasta, "fuera")


class TestBackgammonCLIParsearMultiples(unittest.TestCase):
    """Tests para parsear múltiples movimientos."""

    def setUp(self):
        """Configura el CLI para cada test."""
        self.cli = BackgammonCLI()

    def test_parsear_dos_movimientos(self):
        """Verifica parseo de dos movimientos separados por coma."""
        movimientos_str = "10 15, 5 10"
        movimientos = []
        for mov_str in movimientos_str.split(','):
            movimientos.append(self.cli.parsear_movimiento(mov_str))
        self.assertEqual(len(movimientos), 2)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], (5, 10))

    def test_parsear_movimientos_mixtos(self):
        """Verifica parseo de movimientos de diferentes tipos."""
        movimientos_str = "10 15, bar 5, 20 fuera"
        movimientos = []
        for mov_str in movimientos_str.split(','):
            movimientos.append(self.cli.parsear_movimiento(mov_str))
        self.assertEqual(len(movimientos), 3)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], ("bar", 5))
        self.assertEqual(movimientos[2], (20, "fuera"))

    def test_parsear_con_guiones_y_comas(self):
        """Verifica parseo de movimientos con formato de guión."""
        movimientos_str = "10-15, bar-5"
        movimientos = []
        for mov_str in movimientos_str.split(','):
            movimientos.append(self.cli.parsear_movimiento(mov_str))
        self.assertEqual(len(movimientos), 2)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], ("bar", 5))

    def test_parsear_cuatro_movimientos(self):
        """Verifica parseo de cuatro movimientos (dobles)."""
        movimientos_str = "0 5, 5 10, 10 15, 15 20"
        movimientos = []
        for mov_str in movimientos_str.split(','):
            movimientos.append(self.cli.parsear_movimiento(mov_str))
        self.assertEqual(len(movimientos), 4)

    def test_parsear_con_espacios_irregulares(self):
        """Verifica parseo con espacios extra alrededor de las comas."""
        movimientos_str = "10 15 ,  bar 5  ,20 fuera"
        movimientos = []
        for mov_str in movimientos_str.split(','):
            movimientos.append(self.cli.parsear_movimiento(mov_str))
        self.assertEqual(len(movimientos), 3)


class TestBackgammonCLIEstado(unittest.TestCase):
    """Tests para verificar el estado del CLI."""

    def test_estado_inicial(self):
        """Verifica todos los atributos en estado inicial."""
        cli = BackgammonCLI()
        self.assertIsNone(cli.juego)
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)

    def test_modificar_dados_actuales(self):
        """Verifica que se puedan modificar los dados actuales."""
        cli = BackgammonCLI()
        cli.dados_actuales = (3, 4)
        self.assertEqual(cli.dados_actuales, (3, 4))

    def test_modificar_dados_lanzados(self):
        """Verifica que se pueda modificar el estado de dados_lanzados."""
        cli = BackgammonCLI()
        cli.dados_lanzados = True
        self.assertTrue(cli.dados_lanzados)

    def test_reiniciar_estado(self):
        """Verifica que se pueda reiniciar el estado del CLI."""
        cli = BackgammonCLI()
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True
        cli.juego = None
        cli.dados_actuales = None
        cli.dados_lanzados = False
        self.assertIsNone(cli.juego)
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)


class TestBackgammonCLIParsearCasosEspeciales(unittest.TestCase):
    """Tests para casos especiales de parseo."""

    def setUp(self):
        """Configura el CLI para cada test."""
        self.cli = BackgammonCLI()

    def test_parsear_bar_mayusculas(self):
        """Verifica que BAR se convierta a minúsculas."""
        desde, _ = self.cli.parsear_movimiento("BAR 5")
        self.assertEqual(desde, "bar")

    def test_parsear_fuera_mayusculas(self):
        """Verifica que FUERA se convierta a minúsculas."""
        _, hasta = self.cli.parsear_movimiento("20 FUERA")
        self.assertEqual(hasta, "fuera")

    def test_parsear_bar_diferentes_posiciones(self):
        """Verifica parseo desde bar a diferentes destinos."""
        _, hasta1 = self.cli.parsear_movimiento("bar 0")
        _, hasta2 = self.cli.parsear_movimiento("bar 23")
        self.assertEqual(hasta1, 0)
        self.assertEqual(hasta2, 23)

    def test_parsear_fuera_diferentes_origenes(self):
        """Verifica parseo hacia fuera desde diferentes orígenes."""
        desde1, _ = self.cli.parsear_movimiento("18 fuera")
        desde2, _ = self.cli.parsear_movimiento("23 fuera")
        self.assertEqual(desde1, 18)
        self.assertEqual(desde2, 23)

    def test_parsear_movimiento_tres_partes(self):
        """Verifica error con tres partes."""
        with self.assertRaises(ValueError):
            self.cli.parsear_movimiento("10 15 20")

    def test_parsear_movimiento_vacio(self):
        """Verifica error con entrada vacía."""
        with self.assertRaises(ValueError):
            self.cli.parsear_movimiento("")

    def test_parsear_solo_espacios(self):
        """Verifica error con solo espacios."""
        with self.assertRaises(ValueError):
            self.cli.parsear_movimiento("   ")

    def test_parsear_numeros_negativos(self):
        """Verifica que se acepten números negativos como strings."""
        with self.assertRaises(ValueError):
            self.cli.parsear_movimiento("-5 10")


if __name__ == "__main__":
    unittest.main()
