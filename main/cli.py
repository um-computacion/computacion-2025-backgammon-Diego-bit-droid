"""
CLI interactivo para jugar Backgammon.
Se comunica únicamente con la clase BackgammonGame.
NO maneja excepciones ni lógica de negocio.
"""
from core.clases.backgammon_game import BackgammonGame


class BackgammonCLI:
    """Interfaz de línea de comandos para Backgammon."""
    # pylint: disable=too-many-branches,too-many-statements

    def __init__(self):  # pragma: no cover
        """Inicializa el CLI sin crear el juego todavía."""
        self.juego = None
        self.dados_actuales = None
        self.dados_lanzados = False

    def mostrar_menu_principal(self):  # pragma: no cover
        """Muestra el menú principal del juego."""
        print("\n" + "="*60)
        print("BACKGAMMON - Menú Principal")
        print("="*60)
        print("1. Nueva Partida")
        print("2. Salir")
        print("="*60)

    def mostrar_menu_juego(self):  # pragma: no cover
        """Muestra el menú durante una partida."""
        print("\n" + "-"*60)
        print("Opciones:")
        print("1. Ver tablero")
        print("2. Ver estado del juego")
        print("3. Lanzar dados")
        print("4. Mover fichas")
        print("5. Pasar turno")
        print("6. Volver al menú principal")
        print("-"*60)

    def iniciar_nueva_partida(self):  # pragma: no cover
        """Crea y configura una nueva partida."""
        print("\n" + "="*60)
        print("NUEVA PARTIDA")
        print("="*60)

        nombre1 = input("Nombre del Jugador 1 (fichas X): ").strip()
        if not nombre1:
            nombre1 = "player1"

        nombre2 = input("Nombre del Jugador 2 (fichas O): ").strip()
        if not nombre2:
            nombre2 = "player2"

        self.juego = BackgammonGame(nombre1, nombre2)

        print("\nDeterminando quién comienza...")
        _, dado1, dado2 = self.juego.quien_empieza()
        jugador_actual = self.juego.get_jugador_actual()

        print(f"\n{jugador_actual.get_nombre()} comienza la partida!")
        print(f"Dados iniciales: {dado1} y {dado2}")

        dado1, dado2, _ = self.juego.lanzar_dados()
        self.dados_actuales = (dado1, dado2)
        self.dados_lanzados = True
        self.juego.mostrar_movimientos_disponibles(dado1, dado2)

    def ver_tablero(self):  # pragma: no cover
        """Muestra el estado visual del tablero."""
        if not self.juego:
            print("No hay partida en curso.")
            return

        self.juego.mostrar_tablero()

    def ver_estado(self):  # pragma: no cover
        """Muestra el estado completo del juego."""
        if not self.juego:
            print("No hay partida en curso.")
            return

        estado = self.juego.get_estado_juego()

        print("\n" + "="*60)
        print("ESTADO DEL JUEGO")
        print("="*60)

        if estado["jugador_actual"]:
            print(f"Turno actual: {estado['jugador_actual']}")
            print(f"Movimientos restantes: {estado['movimientos_restantes']}")
        else:
            print("Juego no iniciado")

        if self.dados_actuales:
            d1, d2 = self.dados_actuales
            print(f"Dados actuales: {d1} y {d2}")

        print("\n--- Jugador 1 ---")
        print(f"Nombre: {estado['jugador1']['nombre']}")
        print(f"Ficha: {estado['jugador1']['ficha']}")
        print(f"Fichas en tablero: {estado['jugador1']['fichas_tablero']}")
        print(f"Fichas en bar: {estado['jugador1']['fichas_bar']}")
        print(f"Fichas sacadas: {estado['jugador1']['fichas_sacadas']}")

        print("\n--- Jugador 2 ---")
        print(f"Nombre: {estado['jugador2']['nombre']}")
        print(f"Ficha: {estado['jugador2']['ficha']}")
        print(f"Fichas en tablero: {estado['jugador2']['fichas_tablero']}")
        print(f"Fichas en bar: {estado['jugador2']['fichas_bar']}")
        print(f"Fichas sacadas: {estado['jugador2']['fichas_sacadas']}")
        print("="*60)

    def lanzar_dados(self):  # pragma: no cover
        """Lanza los dados para el turno actual."""
        if not self.juego:
            print("No hay partida en curso.")
            return

        if self.dados_lanzados:
            print("Los dados ya fueron lanzados en este turno.")
            print("Complete sus movimientos o pase el turno.")
            return

        jugador = self.juego.get_jugador_actual()
        dado1, dado2, _ = self.juego.lanzar_dados()
        self.dados_actuales = (dado1, dado2)
        self.dados_lanzados = True

        print(f"\n{jugador.get_nombre()} lanzó los dados: {dado1} y {dado2}")
        self.juego.mostrar_movimientos_disponibles(dado1, dado2)

    def parsear_movimiento(self, texto):
        """
        Convierte una entrada de texto en un movimiento válido.

        Formatos aceptados:
        - "bar 5" o "bar-5" para mover desde el bar
        - "10 15" o "10-15" para mover de posición a posición
        - "20 fuera" o "20-fuera" para sacar una ficha

        Returns:
            tuple: (desde, hasta) donde desde/hasta pueden ser int o str
        """
        texto = texto.strip().lower()

        if '-' in texto:
            partes = texto.split('-')
        else:
            partes = texto.split()

        if len(partes) != 2:
            raise ValueError(
                "Formato inválido. Use: 'desde hasta' o 'desde-hasta'"
            )

        desde_str, hasta_str = partes[0].strip(), partes[1].strip()

        if desde_str == "bar":
            desde = "bar"
        else:
            try:
                desde = int(desde_str)
            except ValueError as exc:
                raise ValueError(
                    f"Posición de origen inválida: {desde_str}"
                ) from exc

        if hasta_str == "fuera":
            hasta = "fuera"
        else:
            try:
                hasta = int(hasta_str)
            except ValueError as exc:
                raise ValueError(
                    f"Posición de destino inválida: {hasta_str}"
                ) from exc

        return (desde, hasta)

    def mover_fichas(self):  # pragma: no cover
        """Solicita y ejecuta movimientos de fichas."""
        if not self.juego:
            print("No hay partida en curso.")
            return

        if not self.dados_actuales:
            print("Debe lanzar los dados primero.")
            return

        if not self.dados_lanzados:
            print("Debe lanzar los dados primero.")
            return

        print("\n" + "="*60)
        print("TABLERO ACTUAL")
        print("="*60)
        self.juego.mostrar_tablero()

        jugador_inicial = self.juego.get_jugador_actual()
        nombre = jugador_inicial.get_nombre()
        ficha = jugador_inicial.get_ficha()
        print(f"\n--- Turno de {nombre} (ficha {ficha}) ---")

        if jugador_inicial.get_ficha() == "X":
            print("Dirección: De posiciones BAJAS (0) a ALTAS (23)")
            print("Ejemplo: 0 -> 5, 10 -> 15")
        else:
            print("Dirección: De posiciones ALTAS (23) a BAJAS (0)")
            print("Ejemplo: 23 -> 18, 15 -> 10")

        d1, d2 = self.dados_actuales
        print(f"\nDados: {d1} y {d2}")

        while True:
            jugador_actual = self.juego.get_jugador_actual()
            if jugador_actual.get_nombre() != jugador_inicial.get_nombre():
                print("\nTodos los movimientos completados.")
                print("Cambiando de jugador...")
                self.dados_actuales = None
                self.dados_lanzados = False
                break

            movimientos_restantes = self.juego.get_movimientos_restantes()

            if movimientos_restantes == 0:
                print("\nTodos los movimientos completados.")
                print("Cambiando de jugador...")
                self.dados_actuales = None
                self.dados_lanzados = False
                break

            print(f"\nMovimientos restantes: {movimientos_restantes}")

            print("\nFormatos válidos:")
            print("  - Para mover: '10 15' o '10-15'")
            print("  - Desde bar: 'bar 5' o 'bar-5'")
            print("  - Sacar ficha: '20 fuera' o '20-fuera'")
            print("  - Múltiples movimientos: separe con comas '10 15, 15 20'")
            print("  - Escriba 'pasar' para pasar turno")

            entrada = input("\nIngrese movimiento(s): ").strip()

            if entrada.lower() == 'pasar':
                print("\nPasando turno...")
                self.juego.cambiar_turno()
                self.dados_actuales = None
                self.dados_lanzados = False
                break

            movimientos = []
            error_parseo = False
            for mov_str in entrada.split(','):
                try:
                    movimiento = self.parsear_movimiento(mov_str)
                    movimientos.append(movimiento)
                except ValueError as e:
                    print(f"Error al parsear '{mov_str}': {e}")
                    error_parseo = True
                    break

            if error_parseo:
                continue

            if not movimientos:
                print("No se ingresaron movimientos válidos.")
                continue

            resultado = self.juego.mover_ficha(
                movimientos,
                self.dados_actuales[0],
                self.dados_actuales[1]
            )

            if not any(resultado.get("resultados", [])):
                print("\n" + "="*60)
                print("TABLERO ACTUAL")
                print("="*60)
                self.juego.mostrar_tablero()
                d1, d2 = self.dados_actuales
                print(f"\nDados: {d1} y {d2}")
                continue

            if self.juego.hay_ganador():
                print("\n" + "="*60)
                print("TABLERO FINAL")
                print("="*60)
                self.juego.mostrar_tablero()
                print("\nPARTIDA TERMINADA")
                self.juego = None
                self.dados_actuales = None
                self.dados_lanzados = False
                return

            jugador_actual = self.juego.get_jugador_actual()
            if jugador_actual.get_nombre() != jugador_inicial.get_nombre():
                print("\n" + "="*60)
                print("TABLERO FINAL")
                print("="*60)
                self.juego.mostrar_tablero()
                print("\nTodos los movimientos completados.")
                print("Cambiando de jugador...")
                self.dados_actuales = None
                self.dados_lanzados = False
                break

            print("\n" + "="*60)
            print("TABLERO ACTUALIZADO")
            print("="*60)
            self.juego.mostrar_tablero()
            d1, d2 = self.dados_actuales
            print(f"\nDados: {d1} y {d2}")

    def pasar_turno(self):  # pragma: no cover
        """Pasa el turno al siguiente jugador."""
        if not self.juego:
            print("No hay partida en curso.")
            return

        jugador_anterior = self.juego.get_jugador_actual()
        jugador_nuevo = self.juego.cambiar_turno()
        self.dados_actuales = None
        self.dados_lanzados = False

        print(f"\nTurno pasado de {jugador_anterior.get_nombre()} "
              f"a {jugador_nuevo.get_nombre()}")

    def ejecutar(self):  # pragma: no cover
        """Ejecuta el bucle principal del CLI."""
        # pylint: disable=too-many-branches
        print("\nBienvenido a BACKGAMMON!")

        while True:
            if not self.juego:
                self.mostrar_menu_principal()
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    self.iniciar_nueva_partida()
                elif opcion == "2":
                    print("\nGracias por jugar!")
                    break
                else:
                    print("Opción inválida.")

            else:
                self.mostrar_menu_juego()
                opcion = input("Seleccione una opción: ").strip()

                if opcion == "1":
                    self.ver_tablero()
                elif opcion == "2":
                    self.ver_estado()
                elif opcion == "3":
                    self.lanzar_dados()
                elif opcion == "4":
                    self.mover_fichas()
                elif opcion == "5":
                    self.pasar_turno()
                elif opcion == "6":
                    print("\nVolviendo al menú principal...")
                    self.juego = None
                    self.dados_actuales = None
                    self.dados_lanzados = False
                else:
                    print("Opción inválida.")


def main():  # pragma: no cover
    """Punto de entrada principal del CLI."""
    cli = BackgammonCLI()
    try:
        cli.ejecutar()
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido! Hasta luego.")


if __name__ == "__main__":  # pragma: no cover
    main()
