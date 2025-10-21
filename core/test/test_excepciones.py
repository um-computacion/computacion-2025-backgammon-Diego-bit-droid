"""
Módulo de pruebas unitarias para las excepciones del juego de Backgammon.
Verifica la correcta jerarquía y funcionamiento de todas las excepciones personalizadas.
"""
import unittest
from core.clases.excepciones import (
    ExcepcionSalirDelJuego,
    ErrorBackgammon,
    JuegoNoInicializadoError,
    TurnoJugadorInvalidoError,
    JuegoYaFinalizadoError,
    MovimientoInvalidoError,
    SinMovimientosDisponiblesError,
    PuntoInvalidoError,
    ComerMultipleFichasError,
    SacarFueraDesdePosicionInvalidaError,
    MovimientoMalFormadoError,
    DadosNoLanzadosError,
    ValorDadoInvalidoError
)


class TestExcepcionSalirDelJuego(unittest.TestCase):
    """Pruebas para la excepción ExcepcionSalirDelJuego."""

    def test_excepcion_salir_se_puede_lanzar(self):
        """Verifica que se pueda lanzar y capturar la excepción."""
        with self.assertRaises(ExcepcionSalirDelJuego):
            raise ExcepcionSalirDelJuego("El usuario decidió salir")


class TestErrorBackgammon(unittest.TestCase):
    """Pruebas para la excepción base ErrorBackgammon."""

    def test_error_backgammon_se_puede_lanzar(self):
        """Verifica que se pueda lanzar y capturar la excepción base."""
        with self.assertRaises(ErrorBackgammon):
            raise ErrorBackgammon("Error genérico de Backgammon")


class TestErrorJuego(unittest.TestCase):
    """Pruebas para las excepciones relacionadas con el estado del juego."""

    def test_juego_no_inicializado_error(self):
        """Verifica que JuegoNoInicializadoError funcione correctamente."""
        with self.assertRaises(JuegoNoInicializadoError):
            raise JuegoNoInicializadoError("El juego no está inicializado")

    def test_turno_jugador_invalido_error(self):
        """Verifica que TurnoJugadorInvalidoError funcione correctamente."""
        with self.assertRaises(TurnoJugadorInvalidoError):
            raise TurnoJugadorInvalidoError("No es tu turno")

    def test_juego_ya_finalizado_error(self):
        """Verifica que JuegoYaFinalizadoError funcione correctamente."""
        with self.assertRaises(JuegoYaFinalizadoError):
            raise JuegoYaFinalizadoError("El juego ya terminó")

    def test_movimiento_invalido_error(self):
        """Verifica que MovimientoInvalidoError funcione correctamente."""
        with self.assertRaises(MovimientoInvalidoError):
            raise MovimientoInvalidoError("Movimiento no permitido")

    def test_sin_movimientos_disponibles_error(self):
        """Verifica que SinMovimientosDisponiblesError funcione correctamente."""
        with self.assertRaises(SinMovimientosDisponiblesError):
            raise SinMovimientosDisponiblesError("No hay movimientos disponibles")


class TestErrorTablero(unittest.TestCase):
    """Pruebas para las excepciones relacionadas con el tablero."""

    def test_punto_invalido_error(self):
        """Verifica que PuntoInvalidoError funcione correctamente."""
        with self.assertRaises(PuntoInvalidoError):
            raise PuntoInvalidoError("Posición fuera de rango")

    def test_comer_multiple_fichas_error(self):
        """Verifica que ComerMultipleFichasError funcione correctamente."""
        with self.assertRaises(ComerMultipleFichasError):
            raise ComerMultipleFichasError("No se puede comer múltiples fichas")

    def test_sacar_fuera_desde_posicion_invalida_error(self):
        """Verifica que SacarFueraDesdePosicionInvalidaError funcione correctamente."""
        with self.assertRaises(SacarFueraDesdePosicionInvalidaError):
            raise SacarFueraDesdePosicionInvalidaError(
                "No se puede sacar desde esta posición"
            )

    def test_movimiento_mal_formado_error(self):
        """Verifica que MovimientoMalFormadoError funcione correctamente."""
        with self.assertRaises(MovimientoMalFormadoError):
            raise MovimientoMalFormadoError("Formato de movimiento inválido")


class TestErrorDados(unittest.TestCase):
    """Pruebas para las excepciones relacionadas con los dados."""

    def test_dados_no_lanzados_error(self):
        """Verifica que DadosNoLanzadosError funcione correctamente."""
        with self.assertRaises(DadosNoLanzadosError):
            raise DadosNoLanzadosError("Los dados no han sido lanzados")

    def test_valor_dado_invalido_error(self):
        """Verifica que ValorDadoInvalidoError funcione correctamente."""
        with self.assertRaises(ValorDadoInvalidoError):
            raise ValorDadoInvalidoError("Valor de dado fuera de rango")
if __name__ == "__main__":
    unittest.main()
