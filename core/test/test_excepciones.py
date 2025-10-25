"""
Módulo de pruebas unitarias para las excepciones del juego de Backgammon.
Verifica la correcta jerarquía y funcionamiento de todas las excepciones personalizadas.
"""
import unittest
from core.clases.excepciones import (
    ExcepcionSalirDelJuego,
    ErrorBackgammon,
    ErrorJuego,
    JuegoNoInicializadoError,
    TurnoJugadorInvalidoError,
    JuegoYaFinalizadoError,
    MovimientoInvalidoError,
    SinMovimientosDisponiblesError,
    ErrorTablero,
    PuntoInvalidoError,
    ComerMultipleFichasError,
    SacarFueraDesdePosicionInvalidaError,
    MovimientoMalFormadoError,
    FichasEnBarError,
    BearingOffNoPermitidoError,
    PosicionBloqueadaError,
    ErrorDados,
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

    def test_fichas_en_bar_error(self):
        """Verifica que FichasEnBarError funcione correctamente."""
        with self.assertRaises(FichasEnBarError):
            raise FichasEnBarError("Debe mover fichas del bar primero")

    def test_bearing_off_no_permitido_error(self):
        """Verifica que BearingOffNoPermitidoError funcione correctamente."""
        with self.assertRaises(BearingOffNoPermitidoError):
            raise BearingOffNoPermitidoError("Fichas fuera del cuadrante final")

    def test_posicion_bloqueada_error(self):
        """Verifica que PosicionBloqueadaError funcione correctamente."""
        with self.assertRaises(PosicionBloqueadaError):
            raise PosicionBloqueadaError("Posición bloqueada por el oponente")


class TestErrorDadosBase(unittest.TestCase):
    """Pruebas para la excepción base ErrorDados."""

    def test_error_dados_base(self):
        """Verifica que ErrorDados se puede lanzar."""
        with self.assertRaises(ErrorDados):
            raise ErrorDados("Error de dados genérico")

    def test_jerarquia_dados_no_lanzados(self):
        """Verifica que DadosNoLanzadosError hereda de ErrorDados."""
        with self.assertRaises(ErrorDados):
            raise DadosNoLanzadosError("Test herencia")


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
            raise DadosNoLanzadosError("Test")

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
