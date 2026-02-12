

---

## prompt utilizando copilot (no funcionaba el mio)

> Hola, quiero hacer tests unitarios en Python para la clase `Checker`. No quiero modificar el código original, solo probar que sus métodos funcionen bien. Estas son las funcionalidades que quiero testear:
>
> 1. Que `get_nombre()` devuelva el nombre correcto del jugador.
> 2. Que `get_ficha()` devuelva el símbolo de ficha del jugador registrado en el juego.
>

---

## Implementación de los tests

        #import unittes 
        class TestChecker(unittest.TestCase):
            def test_get_nombre(self):
                jugador1 = Player("Diego", "X")
                jugador2 = Player("Bot", "O")
                backgammon = BackgammonGame()
                backgammon.registrar_jugadores(jugador1, jugador2)
                ficha = Checker("Diego", backgammon)

                try:
                    nombre = ficha.get_nombre()
                except Exception as e:
                    self.fail(f"get_nombre() falló: {e}")

                self.assertEqual(nombre, "Diego")

            def test_get_ficha(self):
                jugador1 = Player("Diego", "X")
                jugador2 = Player("Bot", "O")
                backgammon = BackgammonGame()
                backgammon.registrar_jugadores(jugador1, jugador2)
                ficha = Checker("Bot", backgammon)

                try:
                    simbolo = ficha.get_ficha()
                except Exception as e:
                    self.fail(f"get_ficha() falló: {e}")

                self.assertEqual(simbolo, "O")

        if __name__ == '__main__':
            unittest.main()
#Aclarcion cambio la forma de usar checker despues de la consulta de hoy martes pero dejo este promp para no cambiar mi documentacion