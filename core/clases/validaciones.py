class MovimientoInvalidoError(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje

def regla_bar(jugador, movimientos, dados, board):
    nombre = jugador.get_nombre()
    fichas_en_bar = board.get_bar(nombre)
    if fichas_en_bar > 0 and any(m[0] != "bar" for m in movimientos):
        raise MovimientoInvalidoError(f"{nombre} tiene fichas en el bar. Debe moverlas antes de usar otras.")

def regla_salida_final(jugador, movimientos, dados, board):
    nombre = jugador.get_nombre()
    for desde, hasta in movimientos:
        if hasta == "fuera" and not board.puede_sacar(jugador):
            raise MovimientoInvalidoError(f"{nombre} no puede sacar fichas aún. Todas deben estar en el cuadrante final.")