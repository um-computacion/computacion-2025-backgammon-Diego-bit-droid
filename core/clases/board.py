"""
Módulo que maneja el tablero de Backgammon.
Incluye la lógica para mover fichas, validar movimientos y gestionar el estado del juego.
"""
from core.clases.checker import Checker
from core.clases.excepciones import (
    MovimientoInvalidoError,
    PuntoInvalidoError,
    MovimientoMalFormadoError,
)
# pylint: disable=too-many-return-statements,too-many-branches
class Board:
    """
    Representa el tablero de Backgammon con 24 posiciones,
    bar para fichas comidas y área para fichas fuera del juego.
    """
    def __init__(self):
        """
        Inicializa el tablero de backgammon:
        - 24 posiciones vacías.
        - Bar para fichas comidas.
        - Área para fichas fuera del juego.
        """
        self.__posiciones__ = self.preparar_tablero()
        self.__bar__ = {'player1': 0, 'player2': 0}
        self.__fuera__ = {'player1': 0, 'player2': 0}

    def get_tablero(self):
        """Devuelve el estado actual del tablero."""
        return {
            "posiciones": [list(pos) for pos in self.__posiciones__],
            "bar": dict(self.__bar__),
            "fuera": dict(self.__fuera__)
        }

    def preparar_tablero(self):
        """
        Configura las posiciones iniciales del tablero.

        Returns:
            list: lista de 24 pilas con fichas iniciales.
        """
        self.__posiciones__ = [[] for _ in range(24)]
        self.__posiciones__[0] = [Checker("X") for _ in range(2)]
        self.__posiciones__[11] = [Checker("X") for _ in range(5)]
        self.__posiciones__[16] = [Checker("X") for _ in range(3)]
        self.__posiciones__[18] = [Checker("X") for _ in range(5)]
        self.__posiciones__[23] = [Checker("O") for _ in range(2)]
        self.__posiciones__[12] = [Checker("O") for _ in range(5)]
        self.__posiciones__[7] = [Checker("O") for _ in range(3)]
        self.__posiciones__[5] = [Checker("O") for _ in range(5)]
        return self.__posiciones__

    def mostrar_board(self):
        """
        Muestra una representación visual del tablero en consola
        y devuelve el estado actual del tablero.

        Returns:
            dict: Estado completo del tablero con posiciones, bar y fuera
        """
        estado = self.get_tablero()
        print("="*60)

        bar_p1 = self.__bar__['player1']
        bar_p2 = self.__bar__['player2']
        print(f"BAR P1: {bar_p1} fichas | BAR P2: {bar_p2} fichas")
        print()

        print("Posiciones 0-23:")
        print("-" * 50)

        header_top = " ".join([f"{i:2d}" for i in range(12, 24)])
        print(header_top)

        max_height_top = max(
            (len(self.__posiciones__[i]) for i in range(12, 24)),
            default=0
        )

        for height in range(max_height_top - 1, -1, -1):
            line = ""
            for i in range(12, 24):
                if height < len(self.__posiciones__[i]):
                    simbolo = self.__posiciones__[i][height].get_simbolo()
                    line += f" {simbolo} "
                else:
                    line += "   "
            print(line)

        print("-" * 50)
        print()

        max_height_bottom = max(
            (len(self.__posiciones__[i]) for i in range(12)),
            default=0
        )

        for height in range(max_height_bottom - 1, -1, -1):
            line = []
            for i in range(11, -1, -1):
                if height < len(self.__posiciones__[i]):
                    simbolo = self.__posiciones__[i][height].get_simbolo()
                    line.append(f" {simbolo} ")
                else:
                    line.append("   ")
            print("".join(line))

        header_bottom = " ".join([f"{i:2d}" for i in range(11, -1, -1)])
        print(header_bottom)

        print("-" * 50)
        print()

        fuera_p1 = self.__fuera__['player1']
        fuera_p2 = self.__fuera__['player2']
        print(f"FUERA P1: {fuera_p1} fichas | FUERA P2: {fuera_p2} fichas")
        print("="*60)
        return estado

    def mover_ficha(self, jugador, movimientos, dados_disponibles):
        """
        Mueve fichas según los movimientos dados y valida cada uno.

        Args:
            jugador: objeto Player que realiza el movimiento
            movimientos: lista de tuplas (desde, hasta)
            dados_disponibles: lista de valores de dados disponibles

        Returns:
            dict: diccionario con resultados, dados usados y log
        """
        if not isinstance(movimientos, list):
            raise MovimientoMalFormadoError(
                "Los movimientos deben ser una lista de tuplas (desde, hasta)."
            )

        for movimiento in movimientos:
            if not isinstance(movimiento, tuple) or len(movimiento) != 2:
                raise MovimientoMalFormadoError(
                    "Cada movimiento debe ser una tupla con dos elementos."
                )

        resultados = []
        dados_usados = []
        log = []

        for desde, hasta in movimientos:
            movimiento_data = {
                'desde': desde,
                'hasta': hasta,
                'jugador': jugador,
                'dados_disponibles': dados_disponibles,
                'dados_usados': dados_usados,
                'log': log
            }
            resultado = self._procesar_movimiento_individual(movimiento_data)
            resultados.append(resultado)

        return {
            "resultados": resultados,
            "dados_usados": dados_usados,
            "dados_restantes": dados_disponibles,
            "log": log
        }

    def _procesar_movimiento_individual(self, movimiento_data):
        """
        Procesa un movimiento individual validándolo y ejecutándolo.

        Args:
            movimiento_data: dict con claves 'desde', 'hasta', 'jugador',
                        'dados_disponibles', 'dados_usados', 'log'

        Returns:
            bool: True si el movimiento fue exitoso, False si no
        """
        desde = movimiento_data['desde']
        hasta = movimiento_data['hasta']
        jugador = movimiento_data['jugador']
        dados_disponibles = movimiento_data['dados_disponibles']
        dados_usados = movimiento_data['dados_usados']
        log = movimiento_data['log']
        distancia = self.calcular_distancia(desde, hasta, jugador)

        # Validar fichas en bar
        if desde != "bar" and self.__bar__[jugador.get_nombre()] > 0:
            log.append(
                f"Debes primero sacar tus {self.__bar__[jugador.get_nombre()]} "
                f"ficha(s) del bar antes de mover otras fichas."
            )
            return False

        # Validar dado disponible
        if distancia not in dados_disponibles:
            # Mensaje personalizado según dirección
            if jugador.get_ficha() == "X":
                if distancia < 0:
                    log.append(
                        f"Movimiento inválido: intentas moverte "
                        f"{abs(distancia)} posiciones hacia atrás, "
                        f"pero como jugador X debes moverte hacia adelante "
                        f"(de 0 a 23). "
                        f"Dados disponibles: {dados_disponibles}"
                    )
                else:
                    log.append(
                        f"No hay dado con valor {distancia} disponible. "
                        f"Dados disponibles: {dados_disponibles}"
                    )
            else:
                if distancia < 0:
                    log.append(
                        f"Movimiento inválido: intentas moverte "
                        f"{abs(distancia)} posiciones hacia adelante, "
                        f"pero como jugador O debes moverte hacia atrás "
                        f"(de 23 a 0). "
                        f"Dados disponibles: {dados_disponibles}"
                    )
                else:
                    log.append(
                        f"No hay dado con valor {distancia} disponible. "
                        f"Dados disponibles: {dados_disponibles}"
                    )
            return False

        try:
            if not self.validar_movimiento(desde, hasta, jugador):
                log.append(
                    f"No hay fichas en la posición {desde} o no te pertenecen."
                )
                return False
        except (MovimientoInvalidoError, PuntoInvalidoError) as error:
            log.append(str(error))
            return False

        # Validar posición bloqueada
        if isinstance(hasta, int):
            pila_destino = self.__posiciones__[hasta]
            if pila_destino and \
            pila_destino[-1].get_simbolo() != jugador.get_ficha():
                if len(pila_destino) > 1:
                    log.append(
                        f"No se puede mover a {hasta}: posición bloqueada con "
                        f"{len(pila_destino)} fichas enemigas. "
                        f"Solo puedes comer una ficha enemiga solitaria."
                    )
                    return False

        # Validar bearing off
        if hasta == "fuera":
            if not self.puede_sacar(jugador):
                log.append(
                    f"No puedes sacar fichas todavía. "
                    f"Primero debes llevar todas tus fichas al cuadrante final "
                    f"({'18-23' if jugador.get_nombre() == 'player1' else '0-5'})."
                )
                return False

            if not self.esta_en_cuadrante_final(desde, jugador):
                log.append(
                    f"No se puede sacar ficha desde {desde}. "
                    f"Solo puedes sacar fichas del cuadrante final "
                    f"({'18-23' if jugador.get_nombre() == 'player1' else '0-5'})."
                )
                return False

        return self._ejecutar_movimiento({
            'desde': desde,
            'hasta': hasta,
            'jugador': jugador,
            'distancia': distancia,
            'dados_disponibles': dados_disponibles,
            'dados_usados': dados_usados,
            'log': log
        })

    def _ejecutar_movimiento(self, movimiento_data):
        """
        Ejecuta el movimiento físico de la ficha.

        Args:
            movimiento_data: dict con claves 'desde', 'hasta', 'jugador',
                           'distancia', 'dados_disponibles', 'dados_usados', 'log'

        Returns:
            bool: True si el movimiento se ejecutó correctamente
        """
        desde = movimiento_data['desde']
        hasta = movimiento_data['hasta']
        jugador = movimiento_data['jugador']
        distancia = movimiento_data['distancia']
        dados_disponibles = movimiento_data['dados_disponibles']
        dados_usados = movimiento_data['dados_usados']
        log = movimiento_data['log']
        ficha_comida = False

        try:
            if self.puede_comer(hasta, jugador):
                self.__posiciones__[hasta].pop()
                oponente = (
                    "player2" if jugador.get_nombre() == "player1"
                    else "player1"
                )
                self.__bar__[oponente] += 1
                ficha_comida = True
        except PuntoInvalidoError as error:
            log.append(str(error))
            return False

        if desde == "bar":
            self.__bar__[jugador.get_nombre()] -= 1
        else:
            self.__posiciones__[desde].pop()

        if hasta == "fuera":
            self.__fuera__[jugador.get_nombre()] += 1
            log.append(
                f"{jugador.get_ficha()} sacó ficha desde {desde} "
                f"usando dado {distancia}."
            )
        else:
            self.__posiciones__[hasta].append(Checker(jugador.get_ficha()))
            mensaje = (
                f"{jugador.get_ficha()} movió de {desde} a {hasta} "
                f"usando dado {distancia}."
            )
            if ficha_comida:
                mensaje += " Comió ficha enemiga."
            log.append(mensaje)

        dados_disponibles.remove(distancia)
        dados_usados.append(distancia)
        return True

    def calcular_distancia(self, desde, hasta, jugador):
        """
        Calcula la distancia entre dos posiciones según el sentido del jugador.

        Returns:
            int: distancia positiva.
        """
        if desde == "bar":
            desde = 0 if jugador.get_ficha() == "X" else 23
        if hasta == "fuera":
            hasta = 23 if jugador.get_ficha() == "X" else 0
        return (
            hasta - desde if jugador.get_ficha() == "X"
            else desde - hasta
        )

    def validar_movimiento(self, desde, _hasta, jugador):
        """
        Verifica si el movimiento es válido.

        Args:
            desde: posición origen (int o "bar")
            _hasta: posición destino (no usado, reservado para futuras validaciones)
            jugador: objeto Player que realiza el movimiento

        Returns:
            bool: True si es válido, False si no.
        """
        if isinstance(desde, int) and not 0 <= desde < 24:
            raise PuntoInvalidoError(f"Posición 'desde' fuera de rango: {desde}")

        if desde == "bar":
            if self.__bar__[jugador.get_nombre()] == 0:
                raise MovimientoInvalidoError(
                    f"No hay fichas en el bar para {jugador.get_nombre()}."
                )
        elif isinstance(desde, int):
            if not self.__posiciones__[desde]:
                return False
            if self.__posiciones__[desde][-1].get_simbolo() != \
               jugador.get_ficha():
                raise MovimientoInvalidoError(
                    f"La ficha en {desde} no pertenece al jugador."
                )
        return True

    def puede_comer(self, hasta, jugador):
        """
        Determina si el jugador puede comer una ficha enemiga.

        Returns:
            bool: True si hay una sola ficha enemiga, False si no.
        """
        if hasta == "fuera":
            return False
        if not isinstance(hasta, int) or not 0 <= hasta < 24:
            raise PuntoInvalidoError(
                f"Posición 'hasta' fuera de rango: {hasta}"
            )
        pila = self.__posiciones__[hasta]
        return (
            len(pila) == 1 and
            pila[-1].get_simbolo() != jugador.get_ficha()
        )

    def set_posiciones(self, index, fichas):
        """Establece fichas en una posición específica del tablero."""
        if not isinstance(index, int) or not 0 <= index < 24:
            raise PuntoInvalidoError(f"Índice fuera de rango: {index}")
        self.__posiciones__[index] = fichas

    def get_posiciones(self, index):
        """Devuelve las fichas en una posición específica del tablero."""
        if not isinstance(index, int) or not 0 <= index < 24:
            raise PuntoInvalidoError(f"Índice fuera de rango: {index}")
        return self.__posiciones__[index]

    def set_bar(self, jugador, cantidad):
        """Establece la cantidad de fichas en el bar para un jugador."""
        self.__bar__[jugador] = cantidad

    def get_bar(self, jugador):
        """Devuelve la cantidad de fichas en el bar para un jugador."""
        return self.__bar__[jugador]

    def set_fuera(self, jugador, cantidad):
        """Establece la cantidad de fichas fuera del tablero para un jugador."""
        self.__fuera__[jugador] = cantidad

    def get_fuera(self, jugador):
        """Devuelve la cantidad de fichas fuera del tablero para un jugador."""
        return self.__fuera__[jugador]

    def esta_en_cuadrante_final(self, posicion, jugador):
        """Verifica si una posición está en el cuadrante final del jugador."""
        if not isinstance(posicion, int):
            return False
        if jugador.get_nombre() == "player1":
            return 18 <= posicion <= 23
        return 0 <= posicion <= 5

    def puede_sacar(self, jugador):
        """Verifica si todas las fichas del jugador están en cuadrante final."""
        for i in range(24):
            pila = self.__posiciones__[i]
            if pila and pila[-1].get_simbolo() == jugador.get_ficha():
                if not self.esta_en_cuadrante_final(i, jugador):
                    return False
        return True
