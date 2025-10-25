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

    def test_parsear_movimiento_desde_bar_espacio(self):
        """Prueba parseo desde bar con espacio."""
        desde, hasta = self.cli.parsear_movimiento("bar 5")
        self.assertEqual(desde, "bar")
        self.assertEqual(hasta, 5)

    def test_parsear_movimiento_desde_bar_guion(self):
        """Prueba parseo desde bar con guión."""
        desde, hasta = self.cli.parsear_movimiento("bar-5")
        self.assertEqual(desde, "bar")
        self.assertEqual(hasta, 5)

    def test_parsear_movimiento_hacia_fuera_espacio(self):
        """Prueba parseo para sacar ficha con espacio."""
        desde, hasta = self.cli.parsear_movimiento("20 fuera")
        self.assertEqual(desde, 20)
        self.assertEqual(hasta, "fuera")

    def test_parsear_movimiento_hacia_fuera_guion(self):
        """Prueba parseo para sacar ficha con guión."""
        desde, hasta = self.cli.parsear_movimiento("20-fuera")
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

    def test_parsear_movimiento_formato_invalido_una_parte(self):
        """Verifica error con formato de una sola parte."""
        with self.assertRaises(ValueError) as context:
            self.cli.parsear_movimiento("10")
        self.assertIn("Formato inválido", str(context.exception))

    def test_parsear_movimiento_formato_invalido_tres_partes(self):
        """Verifica error con formato de tres partes."""
        with self.assertRaises(ValueError) as context:
            self.cli.parsear_movimiento("10 15 20")
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

    def test_parsear_bar_case_variations(self):
        """Verifica que 'bar' funcione en diferentes formatos."""
        desde1, _ = self.cli.parsear_movimiento("Bar 5")
        desde2, _ = self.cli.parsear_movimiento("BAR-10")
        desde3, _ = self.cli.parsear_movimiento("bar 3")

        self.assertEqual(desde1, "bar")
        self.assertEqual(desde2, "bar")
        self.assertEqual(desde3, "bar")

    def test_parsear_fuera_case_variations(self):
        """Verifica que 'fuera' funcione en diferentes formatos."""
        _, hasta1 = self.cli.parsear_movimiento("20 Fuera")
        _, hasta2 = self.cli.parsear_movimiento("18-FUERA")
        _, hasta3 = self.cli.parsear_movimiento("23 fuera")

        self.assertEqual(hasta1, "fuera")
        self.assertEqual(hasta2, "fuera")
        self.assertEqual(hasta3, "fuera")

    def test_parsear_numeros_validos(self):
        """Verifica parseo de diferentes posiciones numéricas."""
        desde1, hasta1 = self.cli.parsear_movimiento("0 5")
        desde2, hasta2 = self.cli.parsear_movimiento("12-18")
        desde3, hasta3 = self.cli.parsear_movimiento("23 22")
        self.assertEqual(desde1, 0)
        self.assertEqual(hasta1, 5)
        self.assertEqual(desde2, 12)
        self.assertEqual(hasta2, 18)
        self.assertEqual(desde3, 23)
        self.assertEqual(hasta3, 22)

    def test_parsear_posicion_cero(self):
        """Verifica parseo de la posición 0."""
        desde, hasta = self.cli.parsear_movimiento("0 5")
        self.assertEqual(desde, 0)
        self.assertEqual(hasta, 5)

    def test_parsear_posicion_23(self):
        """Verifica parseo de la posición 23."""
        desde, hasta = self.cli.parsear_movimiento("23 18")
        self.assertEqual(desde, 23)
        self.assertEqual(hasta, 18)

    def test_parsear_bar_a_diferentes_posiciones(self):
        """Verifica parseo desde bar a diferentes posiciones."""
        desde1, hasta1 = self.cli.parsear_movimiento("bar 0")
        desde2, hasta2 = self.cli.parsear_movimiento("bar 23")
        desde3, hasta3 = self.cli.parsear_movimiento("bar 12")
        self.assertEqual(desde1, "bar")
        self.assertEqual(hasta1, 0)
        self.assertEqual(desde2, "bar")
        self.assertEqual(hasta2, 23)
        self.assertEqual(desde3, "bar")
        self.assertEqual(hasta3, 12)

    def test_parsear_diferentes_posiciones_a_fuera(self):
        """Verifica parseo de diferentes posiciones a fuera."""
        desde1, hasta1 = self.cli.parsear_movimiento("18 fuera")
        desde2, hasta2 = self.cli.parsear_movimiento("19 fuera")
        desde3, hasta3 = self.cli.parsear_movimiento("23 fuera")

        self.assertEqual(desde1, 18)
        self.assertEqual(hasta1, "fuera")
        self.assertEqual(desde2, 19)
        self.assertEqual(hasta2, "fuera")
        self.assertEqual(desde3, 23)
        self.assertEqual(hasta3, "fuera")


class TestBackgammonCLIParsearMultiplesMovimientos(unittest.TestCase):
    """Tests para parsear múltiples movimientos."""

    def setUp(self):
        """Configura el CLI para cada test."""
        self.cli = BackgammonCLI()

    def test_parsear_dos_movimientos_con_coma(self):
        """Verifica parseo de dos movimientos separados por coma."""
        movimientos_str = "10 15, 5 10"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 2)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], (5, 10))

    def test_parsear_tres_movimientos_diferentes_tipos(self):
        """Verifica parseo de movimientos de diferentes tipos."""
        movimientos_str = "10 15, bar 5, 20 fuera"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 3)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], ("bar", 5))
        self.assertEqual(movimientos[2], (20, "fuera"))

    def test_parsear_movimientos_con_guiones_y_comas(self):
        """Verifica parseo de movimientos con formato de guión."""
        movimientos_str = "10-15, bar-5, 20-fuera"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 3)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], ("bar", 5))
        self.assertEqual(movimientos[2], (20, "fuera"))

    def test_parsear_cuatro_movimientos_normales(self):
        """Verifica parseo de cuatro movimientos normales."""
        movimientos_str = "0 5, 5 10, 10 15, 15 20"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 4)
        self.assertEqual(movimientos[0], (0, 5))
        self.assertEqual(movimientos[1], (5, 10))
        self.assertEqual(movimientos[2], (10, 15))
        self.assertEqual(movimientos[3], (15, 20))

    def test_parsear_movimientos_con_espacios_extras(self):
        """Verifica parseo con espacios extra alrededor de las comas."""
        movimientos_str = "10 15 ,  bar 5  ,20 fuera"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 3)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], ("bar", 5))
        self.assertEqual(movimientos[2], (20, "fuera"))


class TestBackgammonCLIEstadoInicial(unittest.TestCase):
    """Tests para verificar el estado inicial del CLI."""

    def test_estado_inicial_completo(self):
        """Verifica todos los atributos en estado inicial."""
        cli = BackgammonCLI()

        self.assertIsNone(cli.juego)
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)

    def test_reinicio_estado(self):
        """Verifica que se pueda reiniciar el estado del CLI."""
        cli = BackgammonCLI()

        # Simular que hay un juego activo
        cli.dados_actuales = (5, 3)
        cli.dados_lanzados = True

        # Reiniciar
        cli.juego = None
        cli.dados_actuales = None
        cli.dados_lanzados = False

        # Verificar reinicio
        self.assertIsNone(cli.juego)
        self.assertIsNone(cli.dados_actuales)
        self.assertFalse(cli.dados_lanzados)

    def test_modificar_dados_actuales(self):
        """Verifica que se puedan modificar los dados actuales."""
        cli = BackgammonCLI()

        self.assertIsNone(cli.dados_actuales)

        cli.dados_actuales = (3, 4)
        self.assertEqual(cli.dados_actuales, (3, 4))

        cli.dados_actuales = (6, 6)
        self.assertEqual(cli.dados_actuales, (6, 6))

    def test_modificar_dados_lanzados(self):
        """Verifica que se pueda modificar el estado de dados_lanzados."""
        cli = BackgammonCLI()

        self.assertFalse(cli.dados_lanzados)

        cli.dados_lanzados = True
        self.assertTrue(cli.dados_lanzados)

        cli.dados_lanzados = False
        self.assertFalse(cli.dados_lanzados)


class TestBackgammonCLIParsearMovimientosCombinados(unittest.TestCase):
    """Tests para parsear combinaciones complejas de movimientos."""

    def setUp(self):
        """Configura el CLI para cada test."""
        self.cli = BackgammonCLI()

    def test_parsear_movimientos_mixtos_espacios_guiones(self):
        """Verifica parseo con mezcla de espacios y guiones."""
        movimientos_str = "10 15, bar-5, 20-fuera, 3 8"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 4)
        self.assertEqual(movimientos[0], (10, 15))
        self.assertEqual(movimientos[1], ("bar", 5))
        self.assertEqual(movimientos[2], (20, "fuera"))
        self.assertEqual(movimientos[3], (3, 8))

    def test_parsear_solo_bar_movimientos(self):
        """Verifica parseo de múltiples movimientos desde bar."""
        movimientos_str = "bar 5, bar 10, bar 15"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 3)
        self.assertEqual(movimientos[0], ("bar", 5))
        self.assertEqual(movimientos[1], ("bar", 10))
        self.assertEqual(movimientos[2], ("bar", 15))

    def test_parsear_solo_fuera_movimientos(self):
        """Verifica parseo de múltiples movimientos hacia fuera."""
        movimientos_str = "18 fuera, 19 fuera, 20 fuera"
        movimientos = []

        for mov_str in movimientos_str.split(','):
            movimiento = self.cli.parsear_movimiento(mov_str)
            movimientos.append(movimiento)

        self.assertEqual(len(movimientos), 3)
        self.assertEqual(movimientos[0], (18, "fuera"))
        self.assertEqual(movimientos[1], (19, "fuera"))
        self.assertEqual(movimientos[2], (20, "fuera"))


if __name__ == "__main__":
    unittest.main()
