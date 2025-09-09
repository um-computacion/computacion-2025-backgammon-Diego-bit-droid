import unittest
from core.clases.Player import Player
class TestPlayer(unittest.TestCase):
    def test_estado_jugador_total_15(self):
        jugador = Player("Diego", "X")

        
        jugador._Player__fichas_en_tablero__ = 7
        jugador._Player__fichas_en_bar__ = 3
        jugador._Player__fichas_sacadas__ = 5

        estado = jugador.estado_jugador()

        self.assertEqual(estado["en_tablero"], 7)
        self.assertEqual(estado["en_bar"], 3)
        self.assertEqual(estado["sacadas"], 5)
        self.assertEqual(estado["total"], 15)
    def test_fichas_en_tablero(self):
        jugador = Player("Diego", "X")
        posiciones = [
            ['X', 'O'], ['X'], [], ['O'], ['X', 'X'], ['X'], ['X'], [], [], [], [], [],
            [], [], [], [], [], [], [], [], [], [], [], []
        ]
        resultado = jugador.fichas_en_tablero(posiciones)
        self.assertEqual(resultado, 6)
        self.assertEqual(jugador.estado_jugador()["en_tablero"], 6)

    def test_fichas_en_bar(self):
        jugador = Player("Diego", "X")
        bar = ['X', 'O', 'X']
        resultado = jugador.fichas_en_bar(bar)
        self.assertEqual(resultado, 2)
        self.assertEqual(jugador.estado_jugador()["en_bar"], 2)

    def test_fichas_sacadas(self):
        jugador = Player("Diego", "X")
        fuera = ['X', 'X', 'O', 'X']
        resultado = jugador.fichas_sacadas(fuera)
        self.assertEqual(resultado, 3)
        self.assertEqual(jugador.estado_jugador()["sacadas"], 3)
    def test_get_nombre_y_ficha(self):
        jugador = Player("Diego", "X")

        try:
            nombre = jugador.get_nombre()
            ficha = jugador.get_ficha()
        except Exception as e:
            self.fail(f"get_nombre() o get_ficha() falló: {e}")

        self.assertEqual(nombre, "Diego")
        self.assertEqual(ficha, "X")

if __name__ == '__main__':
    unittest.main()