from core.clases.checker import Checker

class Board:
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
        """
        Devuelve el estado actual del tablero.

        Returns:
            dict: contiene posiciones, bar y fichas fuera.
        """
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
        Imprime el estado visual del tablero en consola.
        """
        print("="*60)
        print(f"BAR P1: {self.__bar__['player1']} fichas | BAR P2: {self.__bar__['player2']} fichas\n")
        print("Posiciones 0-23:")
        print("-" * 50)
        print("".join(f"{i:2d} " for i in range(12, 24)))

        max_height_top = max(len(self.__posiciones__[i]) for i in range(12, 24))
        for h in range(max_height_top):
            print("".join(f" {self.__posiciones__[i][h]} " if h < len(self.__posiciones__[i]) else "   " for i in range(12, 24)))

        print("-" * 50 + "\n")

        max_height_bottom = max(len(self.__posiciones__[i]) for i in range(11, -1, -1))
        for h in range(max_height_bottom - 1, -1, -1):
            print("".join(f" {self.__posiciones__[i][h]} " if h < len(self.__posiciones__[i]) else "   " for i in range(11, -1, -1)))

        print("".join(f"{i:2d} " for i in range(11, -1, -1)))
        print("-" * 50 + "\n")
        print(f"FUERA P1: {self.__fuera__['player1']} fichas | FUERA P2: {self.__fuera__['player2']} fichas")
        print("="*60)

    def mover_ficha(self, jugador, movimientos, dados_disponibles):
        """
        Aplica movimientos sobre el tablero usando los dados disponibles.

        Args:
            jugador (Player): jugador que mueve.
            movimientos (list): lista de tuplas (desde, hasta).
            dados_disponibles (list): dados disponibles.

        Returns:
            dict: resultados del turno.
        """
        resultados = []
        dados_usados = []
        log = []

        for desde, hasta in movimientos:
            distancia = self.calcular_distancia(desde, hasta, jugador)

            if distancia not in dados_disponibles:
                resultados.append(False)
                log.append(f"No se puede usar dado {distancia} para mover de {desde} a {hasta}.")
                continue

            if not self.validar_movimiento(desde, hasta, jugador):
                resultados.append(False)
                log.append(f"Movimiento inválido de {desde} a {hasta} para jugador {jugador.get_ficha()}.")
                continue

            ficha_comida = False
            if self.puede_comer(hasta, jugador):
                self.__posiciones__[hasta].pop()
                oponente = "player2" if jugador.get_nombre() == "player1" else "player1"
                self.__bar__[oponente] += 1
                ficha_comida = True

            if desde == "bar":
                self.__bar__[jugador.get_nombre()] -= 1
            else:
                self.__posiciones__[desde].pop()

            if hasta == "fuera":
                self.__fuera__[jugador.get_nombre()] += 1
                log.append(f"{jugador.get_ficha()} sacó ficha desde {desde} usando dado {distancia}.")
            else:
                self.__posiciones__[hasta].append(Checker(jugador.get_ficha()))
                log.append(f"{jugador.get_ficha()} movió de {desde} a {hasta} usando dado {distancia}." +
                           (" Comió ficha enemiga." if ficha_comida else ""))

            resultados.append(True)
            dados_disponibles.remove(distancia)
            dados_usados.append(distancia)

        return {
            "resultados": resultados,
            "dados_usados": dados_usados,
            "dados_restantes": dados_disponibles,
            "log": log
        }

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
        return hasta - desde if jugador.get_ficha() == "X" else desde - hasta

    def validar_movimiento(self, desde, hasta, jugador):
        """
        Verifica si el movimiento es válido.

        Returns:
            bool: True si es válido, False si no.
        """
        if desde != "bar" and isinstance(desde, int):
            if not self.__posiciones__[desde]:
                return False
            return self.__posiciones__[desde][-1].get_simbolo() == jugador.get_ficha()
        return True

    def puede_comer(self, hasta, jugador):
        """
        Determina si el jugador puede comer una ficha enemiga.

        Returns:
            bool: True si hay una sola ficha enemiga, False si no.
        """
        if isinstance(hasta, str):
            return False
        pila = self.__posiciones__[hasta]
        return len(pila) == 1 and pila[-1].get_simbolo() != jugador.get_ficha()

    def set_posiciones(self, index, fichas):
        """Establece fichas en una posición específica del tablero."""
        self.__posiciones__[index] = fichas

    def get_posiciones(self, index):
        """Devuelve las fichas en una posición específica del tablero."""
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
    def movimientos_validos(self, Player, dado1, dado2):
        simbolo =Player.get_simbolo()
        nombre = Player.get_nombre()
        movimientos = []
        dados = [dado1, dado2] if dado1 != dado2 else [dado1] * 4

        # Si hay fichas en el bar, solo se pueden mover esas
        if self.__bar__[nombre] > 0:
            for dado in dados:
                desde = "bar"
                hasta = dado - 1 if simbolo == "X" else 24 - dado
                if self.es_destino_valido(hasta, simbolo):
                    movimientos.append((desde, hasta))
            return movimientos

        # Buscar fichas en el tablero que puedan moverse
        for i, pila in enumerate(self.__posiciones__):
            if pila and pila[-1].get_simbolo() == simbolo:
                for dado in dados:
                    hasta = i + dado if simbolo == "X" else i - dado
                    if 0 <= hasta < 24 and self.es_destino_valido(hasta, simbolo):
                        movimientos.append((i, hasta))

        return movimientos
    def puede_sacar(self, jugador):
        """
        Verifica si el jugador puede comenzar a sacar fichas.
        Solo si todas sus fichas están en el cuadrante final y no hay fichas en el bar.
        """
        simbolo = jugador.get_ficha()
        nombre = jugador.get_nombre()
        posiciones = self.__posiciones__
        cuadrante = range(18, 24) if simbolo == "X" else range(0, 6)

        total_en_tablero = 0
        en_cuadrante = 0

        for i, pila in enumerate(posiciones):
            for ficha in pila:
                if ficha.get_simbolo() == simbolo:
                    total_en_tablero += 1
                    if i in cuadrante:
                        en_cuadrante += 1

        total_fuera = self.__fuera__[nombre]
        total_bar = self.__bar__[nombre]
        total_jugador = total_en_tablero + total_fuera + total_bar

        return (
            total_jugador == 15 and
            en_cuadrante == total_en_tablero and
            total_bar == 0
        )
    def get_fichas_en_tablero(self, jugador):
        ficha = jugador.get_ficha()
        return sum(1 for pila in self.__posiciones__ for f in pila if f.get_simbolo() == ficha)
    def get_fichas_en_bar(self, jugador):
        """
        Devuelve la cantidad de fichas del jugador en el bar.
        """
        return self.get_bar(jugador.get_nombre())

    def get_fichas_sacadas(self, jugador):
        """
        Devuelve la cantidad de fichas del jugador fuera del tablero.
        """
        return self.get_fuera(jugador.get_nombre())