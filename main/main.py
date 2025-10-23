from main.cli import BackgammonCLI

def main():
    """Función principal para iniciar el CLI."""
    cli = BackgammonCLI()
    try:
        cli.main
    except KeyboardInterrupt:
        print("\n\n¡Juego interrumpido! Hasta pronto.")
    except Exception as e:
        print(f"\n\nError inesperado: {e}")
