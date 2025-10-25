"""Módulo que define reglas de validación para movimientos en el juego de Backgammon."""

class MovimientoInvalidoError(Exception):
    """Excepción lanzada cuando un movimiento no cumple con las reglas del juego."""

    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje

def regla_bar(jugador, movimientos,_dados,board):
    """
    Valida que el jugador mueva primero las fichas del bar si las tiene.

    Args:
        jugador: instancia de Player.
        movimientos: lista de tuplas (desde, hasta).
        dados: lista de dados disponibles (no se usa aquí).
        board: instancia de Board.

    Raises:
        MovimientoInvalidoError: si el jugador tiene fichas en el bar y no las mueve primero.
    """
    nombre = jugador.get_nombre()
    fichas_en_bar = board.get_bar(nombre)
    if fichas_en_bar > 0 and any(desde != "bar" for desde, _ in movimientos):
        raise MovimientoInvalidoError(
            f"{nombre} tiene fichas en el bar. Debe moverlas antes de usar otras."
        )

def regla_salida_final(jugador, movimientos,_dados,board):
    """
    Valida que el jugador solo saque fichas si todas están en el cuadrante final.

    Args:
        jugador: instancia de Player.
        movimientos: lista de tuplas (desde, hasta).
        dados: lista de dados disponibles (no se usa aquí).
        board: instancia de Board.

    Raises:
        MovimientoInvalidoError: si intenta sacar fichas sin tener todas en el cuadrante final.
    """
    nombre = jugador.get_nombre()
    for _, hasta in movimientos:
        if hasta == "fuera" and not board.puede_sacar(jugador):
            raise MovimientoInvalidoError(
                f"{nombre} no puede sacar fichas aún. Todas deben estar en el cuadrante final."
            )
