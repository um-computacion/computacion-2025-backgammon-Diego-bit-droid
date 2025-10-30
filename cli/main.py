"""
CLI interactivo para jugar Backgammon.
Se comunica únicamente con la clase BackgammonGame.
NO maneja excepciones ni lógica de negocio.
"""
from core.clases.backgammon_game import BackgammonGame


class BackgammonCLI:
    """Interfaz de línea de comandos para Backgammon."""
    # pylint: disable=too-many-branches,too-many-statements

    def __init__(self):
        """Inicializa el CLI sin crear el juego todavía."""
        self.juego = None
        self.dados_actuales = None
        self.dados_lanzados = False

    def mostrar_menu_principal(self):
        """Muestra el menú principal del juego."""
        print("\n" + "="*60)
        print("BACKGAMMON - Menú Principal")
        print("="*60)
        print("1. Nueva Partida")
        print("2. Salir")
        print("="*60)

    def mostrar_menu_juego(self):
        """Muestra el menú durante una partida."""
        print("\n" + "-"*60)
        print("Opciones:")
        print("1. Ver tablero")
        print("2. Ver estado del juego")
        print("3. Lanzar dados")
        print("4. Mover fichas")
        print("5. Verificar movimientos legales")
        print("6. Volver al menú principal")
        print("-"*60)

    def iniciar_nueva_partida(self):
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

    def ver_tablero(self):
        """Muestra el estado visual del tablero."""
        if not self.juego:
            print("No hay partida en curso.")
            return

        self.juego.mostrar_tablero()

    def ver_estado(self):
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
            dados_disponibles = self.juego.get_dados_disponibles()
            print(f"Dados lanzados: {d1} y {d2}")
            print(f"Dados disponibles: {dados_disponibles}")

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

    def lanzar_dados(self):
        """Lanza los dados para el turno actual."""
        if not self.juego:
            print("No hay partida en curso.")
            return

        if self.dados_lanzados:
            print("Los dados ya fueron lanzados en este turno.")
            print("Complete sus movimientos")
            return

        jugador = self.juego.get_jugador_actual()
        dado1, dado2, _ = self.juego.lanzar_dados()
        self.dados_actuales = (dado1, dado2)
        self.dados_lanzados = True

        print(f"\n{jugador.get_nombre()} lanzó los dados: {dado1} y {dado2}")
        self.juego.mostrar_movimientos_disponibles(dado1, dado2)

        tiene_movimientos = self.juego.tiene_movimientos_legales(
            jugador, dado1, dado2
        )

        if not tiene_movimientos:
            print("\n⚠ ADVERTENCIA: No hay movimientos legales disponibles.")
            print("El turno será automáticamente pasado.")
            jugador_anterior = jugador
            jugador_nuevo = self.juego.cambiar_turno()
            self.dados_actuales = None
            self.dados_lanzados = False
            print(f"\nTurno pasado de {jugador_anterior.get_nombre()} "
                  f"a {jugador_nuevo.get_nombre()}")

    def verificar_movimientos_legales(self):
        """Verifica si el jugador actual tiene movimientos legales disponibles."""
        if not self.juego:
            print("No hay partida en curso.")
            return
        if not self.dados_actuales:
            print("Debe lanzar los dados primero.")
            return
        jugador = self.juego.get_jugador_actual()
        dados_disponibles = self.juego.get_dados_disponibles()
        
        print("\n" + "="*60)
        print("VERIFICACIÓN DE MOVIMIENTOS LEGALES")
        print("="*60)
        print(f"Jugador: {jugador.get_nombre()} (ficha {jugador.get_ficha()})")
        print(f"Dados disponibles: {dados_disponibles}")
        print("-"*60)
        
        tiene_movimientos = self.juego._tiene_movimientos_con_dados_actuales(jugador)
        if tiene_movimientos:
            print("✓ HAY movimientos legales disponibles.")
            print("  Puede realizar al menos un movimiento válido.")
        else:
            print("✗ NO HAY movimientos legales disponibles.")
            print("  Todas las posiciones están bloqueadas o no hay jugadas válidas.")

        print("="*60)

    def parsear_movimiento(self, texto):
        """
        Delega el parseo al juego y devuelve el resultado.
        Ya no lanza excepciones, solo devuelve None e imprime errores.
        
        Returns:
            tuple: (desde, hasta) o None si hay error
        """
        if not self.juego:
            print("Error: No hay juego activo")
            return None
        
        resultado = self.juego.parsear_movimiento(texto)
        
        if not resultado["valido"]:
            print(f"Error: {resultado['error']}")
            return None
        
        return resultado["movimiento"]

    def _mostrar_info_turno(self, jugador):
        """Muestra información del turno actual."""
        print(f"\n--- Turno de {jugador.get_nombre()} (ficha {jugador.get_ficha()}) ---")

        if jugador.get_ficha() == "X":
            print("Dirección: De posiciones BAJAS (0) a ALTAS (23)")
            print("Ejemplo: 0 -> 5, 10 -> 15")
        else:
            print("Dirección: De posiciones ALTAS (23) a BAJAS (0)")
            print("Ejemplo: 23 -> 18, 15 -> 10")

    def _mostrar_instrucciones(self):
        """Muestra las instrucciones de formato de movimientos."""
        print("\nFormatos válidos:")
        print("  - Para mover: '10 15' o '10-15'")
        print("  - Desde bar: 'bar 5' o 'bar-5'")
        print("  - Sacar ficha: '20 fuera' o '20-fuera'")
        print("  - Múltiples movimientos: separe con comas '10 15, 15 20'")

    def _procesar_entrada_movimientos(self, entrada):
        """
        Procesa la entrada del usuario y devuelve lista de movimientos.
        Ya no lanza excepciones, solo devuelve None e imprime errores.
        """
        if not self.juego:
            print("Error: No hay juego activo")
            return None
        
        resultado = self.juego.parsear_multiples_movimientos(entrada)
        
        if not resultado["valido"]:
            for error in resultado["errores"]:
                print(f"Error al parsear: {error}")
            return None
        
        return resultado["movimientos"]
    def mover_fichas(self):
        # pylint: disable=too-many-branches,too-many-statements
        """Solicita y ejecuta movimientos de fichas."""
        if not self.juego or not self.dados_actuales or not self.dados_lanzados:
            print("Debe lanzar los dados primero." if self.juego else "No hay partida en curso.")
            return

        print("\n" + "="*60)
        print("TABLERO ACTUAL")
        print("="*60)
        self.juego.mostrar_tablero()

        jugador_inicial = self.juego.get_jugador_actual()
        self._mostrar_info_turno(jugador_inicial)

        if not self.juego.tiene_movimientos_legales(
            jugador_inicial, self.dados_actuales[0], self.dados_actuales[1]
        ):
            print("\n⚠ No hay movimientos legales disponibles.")
            print("Pasando automáticamente el turno...")
            jugador_nuevo = self.juego.cambiar_turno()
            self.dados_actuales = None
            self.dados_lanzados = False
            print(f"\nTurno pasado a {jugador_nuevo.get_nombre()}")
            return

        while True:
            jugador_actual = self.juego.get_jugador_actual()
            if jugador_actual.get_nombre() != jugador_inicial.get_nombre():
                print("\n" + "="*60)
                print("CAMBIO DE TURNO AUTOMÁTICO")
                print("="*60)
                print(f"Turno pasado a {jugador_actual.get_nombre()}")
                print("\nTodos los movimientos completados.")
                print("Cambiando de jugador...")
                self.dados_actuales = None
                self.dados_lanzados = False
                break

            if self.juego.get_movimientos_restantes() == 0:
                print("\nTodos los movimientos completados.")
                print("Cambiando de jugador...")
                self.dados_actuales = None
                self.dados_lanzados = False
                break

            dados_disponibles = self.juego.get_dados_disponibles()
            
            if dados_disponibles:
                tiene_movimientos = self.juego._tiene_movimientos_con_dados_actuales(jugador_inicial)
                if not tiene_movimientos:
                    print("\n" + "="*60)
                    print("SIN MOVIMIENTOS LEGALES")
                    print("="*60)
                    print(f"No hay movimientos legales con los dados: {dados_disponibles}")
                    print("Cambiando turno automáticamente...")
                    self.juego.cambiar_turno()
                    print("\nTodos los movimientos completados.")
                    print("Cambiando de jugador...")
                    self.dados_actuales = None
                    self.dados_lanzados = False
                    break
            
            print(f"\nMovimientos restantes: {self.juego.get_movimientos_restantes()}")
            print(f"Dados disponibles: {dados_disponibles}")
            self._mostrar_instrucciones()

            movimientos = self._procesar_entrada_movimientos(
                input("\nIngrese movimiento(s): ").strip()
            )

            if movimientos is None:
                continue

            if not movimientos:
                print("No se ingresaron movimientos válidos.")
                continue

            resultado = self.juego.mover_ficha(
                movimientos, self.dados_actuales[0], self.dados_actuales[1]
            )

            if resultado.get("log"):
                for msg in resultado["log"]:
                    print(f"  → {msg}")

            if not any(resultado.get("resultados", [])):
                jugador_despues = self.juego.get_jugador_actual()
                
                if jugador_despues.get_nombre() != jugador_inicial.get_nombre():
                    print("\n" + "="*60)
                    print("CAMBIO DE TURNO AUTOMÁTICO")
                    print("="*60)
                    print("No hay más movimientos legales disponibles.")
                    print(f"Turno pasado a {jugador_despues.get_nombre()}")
                    print("\nTodos los movimientos completados.")
                    print("Cambiando de jugador...")
                    self.dados_actuales = None
                    self.dados_lanzados = False
                    break

                if not self.juego._tiene_movimientos_con_dados_actuales(jugador_inicial):
                    print("\n" + "="*60)
                    print("SIN MOVIMIENTOS LEGALES RESTANTES")
                    print("="*60)
                    print("No hay más movimientos válidos con los dados disponibles.")
                    print("Cambiando turno automáticamente...")
                    self.juego.cambiar_turno()
                    print("\nTodos los movimientos completados.")
                    print("Cambiando de jugador...")
                    self.dados_actuales = None
                    self.dados_lanzados = False
                    break
                print("\n⚠ Movimiento inválido. Intente otro movimiento.")
                print("\n" + "="*60)
                print("TABLERO ACTUAL")
                print("="*60)
                self.juego.mostrar_tablero()
                dados_disponibles = self.juego.get_dados_disponibles()
                print(f"\nDados disponibles: {dados_disponibles}")
                continue

            if self.juego.hay_ganador():
                print("\n" + "="*60)
                print("¡PARTIDA TERMINADA!")
                print("="*60)
                self.juego.mostrar_tablero()
                ganador = jugador_inicial
                print(f"\n🏆 ¡{ganador.get_nombre()} ha ganado la partida!")
                self.juego = None
                self.dados_actuales = None
                self.dados_lanzados = False
                return

            # Verificar si cambió el turno automáticamente
            jugador_despues = self.juego.get_jugador_actual()
            if jugador_despues.get_nombre() != jugador_inicial.get_nombre():
                print("\n" + "="*60)
                print("CAMBIO DE TURNO AUTOMÁTICO")
                print("="*60)
                print("No quedan movimientos legales con los dados restantes.")
                print(f"Turno pasado a {jugador_despues.get_nombre()}")
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
            
            dados_disponibles = self.juego.get_dados_disponibles()
            print(f"\nDados disponibles: {dados_disponibles}")
            
            if dados_disponibles:
                tiene_movimientos = self.juego._tiene_movimientos_con_dados_actuales(jugador_inicial)
                if not tiene_movimientos:
                    print("\n" + "="*60)
                    print("SIN MOVIMIENTOS LEGALES RESTANTES")
                    print("="*60)
                    print(f"No hay movimientos legales con los dados: {dados_disponibles}")
                    print("Cambiando turno automáticamente...")
                    self.juego.cambiar_turno()
                    print("\nTodos los movimientos completados.")
                    print("Cambiando de jugador...")
                    self.dados_actuales = None
                    self.dados_lanzados = False
                    break

    def ejecutar(self):
        # pylint: disable=too-many-branches
        """Ejecuta el bucle principal del CLI."""
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
                    self.verificar_movimientos_legales()
                elif opcion == "6":
                    print("\nVolviendo al menú principal...")
                    self.juego = None
                    self.dados_actuales = None
                    self.dados_lanzados = False
                else:
                    print("Opción inválida.")


def main():
    """Punto de entrada principal del CLI."""
    cli = BackgammonCLI()
    try:
        cli.ejecutar()
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido! Hasta luego.")


if __name__ == "__main__":
    main()
