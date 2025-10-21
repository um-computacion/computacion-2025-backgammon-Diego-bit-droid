"""
Pruebas unitarias para la clase Board del juego Backgammon.
"""
import unittest
from core.clases.checker import Checker
from core.clases.player import Player
from core.clases.board import Board
from core.clases.excepciones import (
    PuntoInvalidoError,
    MovimientoMalFormadoError
)


class TestBoard(unittest.TestCase):
    """Suite de pruebas para la clase Board."""
    # pylint: disable=too-many-public-methods

    def setUp(self):
        """Inicializa el tablero y jugadores para cada test."""
        self.board = Board()
        self.jugador1 = Player("player1", "X")
        self.jugador2 = Player("player2", "O")

    def test_preparar_tablero(self):
        """Verifica que el tablero se inicialice correctamente."""
        tablero = self.board.get_tablero()["posiciones"]
        self.assertEqual(
            [c.get_simbolo() for c in tablero[0]], ['X', 'X']
        )
        self.assertEqual(
            [c.get_simbolo() for c in tablero[11]], ['X'] * 5
        )
        self.assertEqual(
            [c.get_simbolo() for c in tablero[16]], ['X'] * 3
        )
        self.assertEqual(
            [c.get_simbolo() for c in tablero[18]], ['X'] * 5
        )
        self.assertEqual(
            [c.get_simbolo() for c in tablero[23]], ['O', 'O']
        )
        self.assertEqual(
            [c.get_simbolo() for c in tablero[12]], ['O'] * 5
        )
        self.assertEqual(
            [c.get_simbolo() for c in tablero[7]], ['O'] * 3
        )
        self.assertEqual(
            [c.get_simbolo() for c in tablero[5]], ['O'] * 5
        )

    def test_mostrar_board(self):
        """Verifica que mostrar_board no lance excepciones."""
        self.board.mostrar_board()

    def test_valido_sin_comer(self):
        """Verifica movimiento válido sin comer ficha enemiga."""
        self.board.set_posiciones(0, [Checker("X")])
        dados = [3, 5]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 3)], dados
        )
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(resultado["dados_usados"], [3])
        self.assertEqual(
            [c.get_simbolo() for c in self.board.get_posiciones(3)],
            ["X"]
        )

    def test_valido_con_comer(self):
        """Verifica movimiento válido que come ficha enemiga."""
        self.board.set_posiciones(0, [Checker("X")])
        self.board.set_posiciones(3, [Checker("O")])
        dados = [3, 5]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 3)], dados
        )
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(self.board.get_bar("player2"), 1)
        self.assertEqual(
            [c.get_simbolo() for c in self.board.get_posiciones(3)],
            ["X"]
        )
        self.assertIn("Comió ficha enemiga", resultado["log"][0])

    def test_entrada_desde_bar(self):
        """Verifica entrada de ficha desde el bar."""
        self.board.set_bar("player1", 1)
        dados = [3, 4]
        resultado = self.board.mover_ficha(
            self.jugador1, [("bar", 3)], dados
        )
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(self.board.get_bar("player1"), 0)
        self.assertIn("movió de bar a 3", resultado["log"][0])

    def test_mover_desde_posicion_vacia(self):
        """Verifica que no se pueda mover desde posición vacía."""
        self.board.set_posiciones(0, [])
        dados = [3]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 3)], dados
        )
        self.assertEqual(resultado["resultados"], [False])
        self.assertIn("Movimiento inválido", resultado["log"][0])

    def test_mover_ficha_enemiga(self):
        """Verifica que no se pueda mover ficha enemiga."""
        self.board.set_posiciones(0, [Checker("O")])
        dados = [3]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 3)], dados
        )
        self.assertEqual(resultado["resultados"], [False])
        self.assertIn(
            "La ficha en 0 no pertenece al jugador",
            resultado["log"][0]
        )

    def test_no_puede_comer_varias_fichas_enemigas(self):
        """Verifica que no se puedan comer múltiples fichas enemigas."""
        self.board.set_posiciones(0, [Checker("X")])
        self.board.set_posiciones(3, [Checker("O"), Checker("O")])
        dados = [3]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 3)], dados
        )
        self.assertEqual(resultado["resultados"], [False])
        self.assertIn(
            "no se puede comer múltiples fichas enemigas",
            resultado["log"][0]
        )

    def test_indice_fuera_de_rango_get_posiciones(self):
        """Verifica error al obtener posición fuera de rango."""
        with self.assertRaises(PuntoInvalidoError):
            self.board.get_posiciones(24)

    def test_indice_fuera_de_rango_set_posiciones(self):
        """Verifica error al establecer posición fuera de rango."""
        with self.assertRaises(PuntoInvalidoError):
            self.board.set_posiciones(25, [Checker("X")])

    def test_movimiento_tipo_incorrecto(self):
        """Verifica error cuando movimiento no es una lista."""
        with self.assertRaises(MovimientoMalFormadoError):
            self.board.mover_ficha(self.jugador1, "no es una lista", [3])

    def test_movimiento_tupla_mal_formada(self):
        """Verifica error cuando movimiento no es tupla válida."""
        with self.assertRaises(MovimientoMalFormadoError):
            self.board.mover_ficha(self.jugador1, [(0,)], [3])

    def test_entrada_desde_bar_sin_fichas(self):
        """Verifica que no se pueda entrar desde bar vacío."""
        self.board.set_bar("player1", 0)
        dados = [3]
        resultado = self.board.mover_ficha(
            self.jugador1, [("bar", 3)], dados
        )
        self.assertEqual(resultado["resultados"], [False])
        self.assertIn("No hay fichas en el bar", resultado["log"][0])

    def test_sacar_fuera_desde_posicion_invalida(self):
        """Verifica que no se pueda sacar desde fuera del cuadrante."""
        self.board.set_posiciones(10, [Checker("X")])
        dados = [13]
        resultado = self.board.mover_ficha(
            self.jugador1, [(10, "fuera")], dados
        )
        self.assertEqual(resultado["resultados"], [False])
        self.assertIn("fuera del cuadrante final", resultado["log"][0])

    def test_movimiento_invalido(self):
        """Verifica rechazo de movimiento inválido."""
        self.board.set_posiciones(0, [Checker("X")])
        self.board.validar_movimiento = lambda d, h, j: False
        dados = [3, 5]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 3)], dados
        )
        self.assertEqual(resultado["resultados"], [False])
        self.assertTrue(
            any("Movimiento inválido" in msg for msg in resultado["log"])
        )

    def test_dado_invalido(self):
        """Verifica que no se pueda usar dado no disponible."""
        self.board.set_posiciones(0, [Checker("X")])
        dados = [3, 5]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 6)], dados
        )
        self.assertEqual(resultado["resultados"], [False])
        self.assertEqual(resultado["dados_usados"], [])
        self.assertIn("No se puede usar dado", resultado["log"][0])

    def test_sacar_fuera(self):
        """Verifica sacar ficha del tablero correctamente."""
        for i in range(24):
            self.board.set_posiciones(i, [])
        self.board.__bar__["player1"] = 0
        self.board.__bar__["player2"] = 0
        self.board.set_posiciones(22, [Checker("X")])
        dados = [1]
        resultado = self.board.mover_ficha(
            self.jugador1, [(22, "fuera")], dados
        )
        self.assertEqual(resultado["resultados"], [True])
        self.assertEqual(self.board.get_fuera("player1"), 1)
        self.assertTrue(
            any("sacó ficha" in msg for msg in resultado["log"])
        )

    def test_puede_sacar_true(self):
        """Verifica detección correcta de poder sacar fichas."""
        for i in range(24):
            self.board.set_posiciones(i, [])
        self.board.set_posiciones(22, [Checker("X")])
        self.assertTrue(self.board.puede_sacar(self.jugador1))

    def test_puede_sacar_false(self):
        """Verifica detección correcta de no poder sacar fichas."""
        for i in range(24):
            self.board.set_posiciones(i, [])
        self.board.set_posiciones(10, [Checker("X")])
        self.assertFalse(self.board.puede_sacar(self.jugador1))

    def test_set_posiciones_valido(self):
        """Verifica establecer fichas en posición válida."""
        fichas = [Checker("X"), Checker("X")]
        self.board.set_posiciones(0, fichas)
        self.assertEqual(self.board.get_posiciones(0), fichas)

    def test_set_posiciones_fuera_de_rango(self):
        """Verifica error al establecer posición fuera de rango."""
        with self.assertRaises(PuntoInvalidoError):
            self.board.set_posiciones(24, [])

    def test_get_posiciones_valido(self):
        """Verifica obtener fichas de posición válida."""
        self.board.set_posiciones(5, [Checker("O")])
        fichas = self.board.get_posiciones(5)
        self.assertEqual(len(fichas), 1)
        self.assertEqual(fichas[0].get_simbolo(), "O")

    def test_get_posiciones_fuera_de_rango(self):
        """Verifica error al obtener posición fuera de rango."""
        with self.assertRaises(PuntoInvalidoError):
            self.board.get_posiciones(-1)

    def test_puede_comer_fuera_de_rango(self):
        """Verifica error al verificar comer en posición inválida."""
        with self.assertRaises(PuntoInvalidoError):
            self.board.puede_comer(24, self.jugador1)

    def test_set_bar_y_get_bar(self):
        """Verifica establecer y obtener fichas del bar."""
        self.board.set_bar("player1", 3)
        self.assertEqual(self.board.get_bar("player1"), 3)

    def test_set_fuera_y_get_fuera(self):
        """Verifica establecer y obtener fichas fuera del tablero."""
        self.board.set_fuera("player2", 5)
        self.assertEqual(self.board.get_fuera("player2"), 5)

    def test_set_fuera_y_get_fuera_directo_player1(self):
        """Verifica establecer y obtener fichas de player1 fuera."""
        self.board.set_fuera("player1", 4)
        cantidad = self.board.get_fuera("player1")
        self.assertEqual(cantidad, 4)


if __name__ == "__main__":
    unittest.main()
