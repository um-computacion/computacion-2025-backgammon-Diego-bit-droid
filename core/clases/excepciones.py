"""Módulo que define la jerarquía de excepciones para el juego de Backgammon."""

class ExcepcionSalirDelJuego(Exception):
    """Excepción lanzada cuando el usuario decide salir del juego."""


# Excepción base
class ErrorBackgammon(Exception):
    """Excepción base para todos los errores del juego de Backgammon."""


# Errores a nivel de juego
class ErrorJuego(ErrorBackgammon):
    """Excepción base para errores relacionados con el estado del juego."""


class JuegoNoInicializadoError(ErrorJuego):
    """Se lanza cuando se intenta realizar acciones sin haber iniciado el juego."""


class TurnoJugadorInvalidoError(ErrorJuego):
    """Se lanza cuando un jugador intenta jugar fuera de su turno."""


class JuegoYaFinalizadoError(ErrorJuego):
    """Se lanza cuando se intenta interactuar con una partida ya terminada."""


class MovimientoInvalidoError(ErrorJuego):
    """Se lanza al intentar realizar un movimiento inválido."""


class SinMovimientosDisponiblesError(ErrorJuego):
    """Se lanza cuando un jugador intenta mover sin movimientos restantes."""


# Errores a nivel de tablero
class ErrorTablero(ErrorBackgammon):
    """Excepción base para errores relacionados con el tablero."""


class PuntoInvalidoError(ErrorTablero):
    """Se lanza al acceder a una posición del tablero fuera del rango válido."""



class ComerMultipleFichasError(ErrorTablero):
    """Se lanza cuando se intenta comer más de una ficha enemiga en una posición."""


class SacarFueraDesdePosicionInvalidaError(ErrorTablero):
    """Se lanza cuando se intenta sacar una ficha desde fuera del cuadrante final."""


class MovimientoMalFormadoError(ErrorTablero):
    """Se lanza cuando un movimiento no está representado como una tupla válida (desde, hasta)."""


# Errores a nivel de dados
class ErrorDados(ErrorBackgammon):
    """Excepción base para errores relacionados con los dados."""


class DadosNoLanzadosError(ErrorDados):
    """Se lanza al intentar acceder a los valores de los dados antes de lanzarlos."""


class ValorDadoInvalidoError(ErrorDados):
    """Se lanza cuando los dados muestran valores fuera del rango permitido (1–6)."""
