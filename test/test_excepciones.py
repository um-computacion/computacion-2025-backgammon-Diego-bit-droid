"""Test unitarios para la clase Excepciones"""
import unittest
from core.excepciones import (
    ErrorBackgammon,
    ErrorJuego,
    JuegoNoInicializadoError,
    JuegoYaFinalizadoError,
    MovimientoInvalidoError,
    ErrorTablero,
    PuntoInvalidoError,
    MovimientoMalFormadoError,
    ErrorDados,
    ValorDadoInvalidoError
)


class TestErrorBackgammon(unittest.TestCase):
    """Pruebas para la excepción base ErrorBackgammon."""

    def test_error_backgammon_se_puede_lanzar(self):
        """Verifica que se pueda lanzar y capturar la excepción base."""
        with self.assertRaises(ErrorBackgammon):
            raise ErrorBackgammon("Error genérico de Backgammon")


class TestErrorJuegoBase(unittest.TestCase):
    """Pruebas para la excepción base ErrorJuego."""

    def test_error_juego_se_puede_lanzar(self):
        """Verifica que se pueda lanzar y capturar la excepción base ErrorJuego."""
        with self.assertRaises(ErrorJuego):
            raise ErrorJuego("Error de juego genérico")

    def test_jerarquia_juego_no_inicializado(self):
        """Verifica que JuegoNoInicializadoError hereda de ErrorJuego."""
        with self.assertRaises(ErrorJuego):
            raise JuegoNoInicializadoError("Test herencia")


class TestErrorJuego(unittest.TestCase):
    """Pruebas para las excepciones relacionadas con el estado del juego."""

    def test_juego_no_inicializado_error(self):
        """Verifica que JuegoNoInicializadoError funcione correctamente."""
        with self.assertRaises(JuegoNoInicializadoError):
            raise JuegoNoInicializadoError("El juego no está inicializado")

    def test_juego_ya_finalizado_error(self):
        """Verifica que JuegoYaFinalizadoError funcione correctamente."""
        with self.assertRaises(JuegoYaFinalizadoError):
            raise JuegoYaFinalizadoError("El juego ya terminó")

    def test_movimiento_invalido_error(self):
        """Verifica que MovimientoInvalidoError funcione correctamente."""
        with self.assertRaises(MovimientoInvalidoError):
            raise MovimientoInvalidoError("Movimiento no permitido")


class TestErrorTableroBase(unittest.TestCase):
    """Pruebas para la excepción base ErrorTablero."""

    def test_error_tablero_base(self):
        """Verifica que ErrorTablero se puede lanzar."""
        with self.assertRaises(ErrorTablero):
            raise ErrorTablero("Error de tablero genérico")

    def test_jerarquia_punto_invalido(self):
        """Verifica que PuntoInvalidoError hereda de ErrorTablero."""
        with self.assertRaises(ErrorTablero):
            raise PuntoInvalidoError("Test herencia")


class TestErrorTablero(unittest.TestCase):
    """Pruebas para las excepciones relacionadas con el tablero."""

    def test_punto_invalido_error(self):
        """Verifica que PuntoInvalidoError funcione correctamente."""
        with self.assertRaises(PuntoInvalidoError):
            raise PuntoInvalidoError("Posición fuera de rango")

    def test_movimiento_mal_formado_error(self):
        """Verifica que MovimientoMalFormadoError funcione correctamente."""
        with self.assertRaises(MovimientoMalFormadoError):
            raise MovimientoMalFormadoError("Formato de movimiento inválido")


class TestErrorDadosBase(unittest.TestCase):
    """Pruebas para la excepción base ErrorDados."""

    def test_error_dados_base(self):
        """Verifica que ErrorDados se puede lanzar."""
        with self.assertRaises(ErrorDados):
            raise ErrorDados("Error de dados genérico")

    def test_jerarquia_valor_dado_invalido(self):
        """Verifica que ValorDadoInvalidoError hereda de ErrorDados."""
        with self.assertRaises(ErrorDados):
            raise ValorDadoInvalidoError(7)


class TestErrorDados(unittest.TestCase):
    """Pruebas para las excepciones relacionadas con los dados."""

    def test_valor_dado_invalido_error(self):
        """Verifica que ValorDadoInvalidoError funcione correctamente."""
        with self.assertRaises(ValorDadoInvalidoError):
            raise ValorDadoInvalidoError(7)


class TestJerarquiaExcepciones(unittest.TestCase):
    """Pruebas para verificar la correcta jerarquía de excepciones."""

    def test_todas_excepciones_juego_heredan_error_backgammon(self):
        """Verifica que todas las excepciones de juego heredan de ErrorBackgammon."""
        with self.assertRaises(ErrorBackgammon):
            raise JuegoNoInicializadoError("Test")

    def test_todas_excepciones_tablero_heredan_error_backgammon(self):
        """Verifica que todas las excepciones de tablero heredan de ErrorBackgammon."""
        with self.assertRaises(ErrorBackgammon):
            raise PuntoInvalidoError("Test")

    def test_todas_excepciones_dados_heredan_error_backgammon(self):
        """Verifica que todas las excepciones de dados heredan de ErrorBackgammon."""
        with self.assertRaises(ErrorBackgammon):
            raise ValorDadoInvalidoError(7)

    def test_error_juego_hereda_de_error_backgammon(self):
        """Verifica que ErrorJuego hereda de ErrorBackgammon."""
        with self.assertRaises(ErrorBackgammon):
            raise ErrorJuego("Test")

    def test_error_tablero_hereda_de_error_backgammon(self):
        """Verifica que ErrorTablero hereda de ErrorBackgammon."""
        with self.assertRaises(ErrorBackgammon):
            raise ErrorTablero("Test")

    def test_error_dados_hereda_de_error_backgammon(self):
        """Verifica que ErrorDados hereda de ErrorBackgammon."""
        with self.assertRaises(ErrorBackgammon):
            raise ErrorDados("Test")


if __name__ == "__main__":
    unittest.main()
