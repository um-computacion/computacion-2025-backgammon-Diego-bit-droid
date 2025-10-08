from core.clases.checker import Checker

from core.clases.checker import Checker

class Board:
    def __init__(self):
        self.__posiciones__ = self.preparar_tablero()
        self.__bar__ = {'player1': 0, 'player2': 0}
        self.__fuera__ = {'player1': 0, 'player2': 0}

    def get_tablero(self):
        return {
            "posiciones": [list(pos) for pos in self.__posiciones__],
            "bar": dict(self.__bar__),
            "fuera": dict(self.__fuera__)
        }

    def preparar_tablero(self):
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
        if not isinstance(movimientos, list):
            raise TypeError("Los movimientos deben ser una lista de tuplas (desde, hasta).")
        for movimiento in movimientos:
            if not isinstance(movimiento, tuple) or len(movimiento) != 2:
                raise ValueError("Cada movimiento debe ser una tupla con dos elementos.")

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
        if desde == "bar":
            desde = 0 if jugador.get_ficha() == "X" else 23
        if hasta == "fuera":
            hasta = 23 if jugador.get_ficha() == "X" else 0
        return hasta - desde if jugador.get_ficha() == "X" else desde - hasta

    def validar_movimiento(self, desde, hasta, jugador):
        if isinstance(desde, int) and not (0 <= desde < 24):
            raise IndexError("Posición 'desde' fuera de rango.")
        if desde != "bar" and isinstance(desde, int):
            if not self.__posiciones__[desde]:
                return False
            return self.__posiciones__[desde][-1].get_simbolo() == jugador.get_ficha()
        return True

    def puede_comer(self, hasta, jugador):
        if not isinstance(hasta, int) or not (0 <= hasta < 24):
            return False
        pila = self.__posiciones__[hasta]
        return len(pila) == 1 and pila[-1].get_simbolo() != jugador.get_ficha()

    def set_posiciones(self, index, fichas):
        self.__posiciones__[index] = fichas

    def get_posiciones(self, index):
        if not isinstance(index, int) or not (0 <= index < 24):
            raise IndexError("Índice fuera de rango. Debe estar entre 0 y 23.")
        return self.__posiciones__[index]

    def set_bar(self, jugador, cantidad):
        self.__bar__[jugador] = cantidad

    def get_bar(self, jugador):
        return self.__bar__[jugador]

    def set_fuera(self, jugador, cantidad):
        self.__fuera__[jugador] = cantidad

    def get_fuera(self, jugador):
        return self.__fuera__[jugador]

    def movimientos_validos(self, Player, dado1, dado2):
        simbolo = Player.get_simbolo()
        nombre = Player.get_nombre()
        movimientos = []
        dados = [dado1, dado2] if dado1 != dado2 else [dado1] * 4

        if self.__bar__[nombre] > 0:
            for dado in dados:
                desde = "bar"
                hasta = dado - 1 if simbolo == "X" else 24 - dado
                if self.es_destino_valido(hasta, simbolo):
                    movimientos.append((desde, hasta))
            return movimientos

        for i, pila in enumerate(self.__posiciones__):
            if pila and pila[-1].get_simbolo() == simbolo:
                for dado in dados:
                    hasta = i + dado if simbolo == "X" else i - dado
                    if 0 <= hasta < 24 and self.es_destino_valido(hasta, simbolo):
                        movimientos.append((i, hasta))

        return movimientos