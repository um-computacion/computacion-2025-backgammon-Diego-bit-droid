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
    # pylint: disable=too-many-public-methods, protected-access

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
        self.assertTrue(
            any("No hay fichas en la posición" in msg or
                "no te pertenecen" in msg
                for msg in resultado["log"])
        )

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
        self.assertTrue(
            any("posición bloqueada" in msg or
                "múltiples fichas enemigas" in msg or
                "Solo puedes comer una ficha enemiga solitaria" in msg
                for msg in resultado["log"])
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
        self.assertTrue(
            any("cuadrante final" in msg.lower() for msg in resultado["log"])
        )

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
            any("No hay fichas" in msg or "no te pertenecen" in msg
                for msg in resultado["log"])
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
        self.assertTrue(
            any("dado" in msg.lower() for msg in resultado["log"])
        )

    def test_sacar_fuera(self):
        """Verifica sacar ficha del tablero correctamente."""
        for i in range(24):
            self.board.set_posiciones(i, [])
        self.board.set_bar("player1", 0)
        self.board.set_bar("player2", 0)
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

        puede_sacar = self.board.puede_sacar(self.jugador1)

        self.assertTrue(puede_sacar)

    def test_puede_sacar_false(self):
        """Verifica detección correcta de no poder sacar fichas."""
        for i in range(24):
            self.board.set_posiciones(i, [])
        self.board.set_posiciones(10, [Checker("X")])

        puede_sacar = self.board.puede_sacar(self.jugador1)

        self.assertFalse(puede_sacar)

    def test_set_posiciones_valido(self):
        """Verifica establecer fichas en posición válida."""
        fichas = [Checker("X"), Checker("X")]

        self.board.set_posiciones(0, fichas)
        resultado = self.board.get_posiciones(0)

        self.assertEqual(resultado, fichas)

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
        cantidad = self.board.get_bar("player1")

        self.assertEqual(cantidad, 3)

    def test_set_fuera_y_get_fuera(self):
        """Verifica establecer y obtener fichas fuera del tablero."""
        self.board.set_fuera("player2", 5)
        cantidad = self.board.get_fuera("player2")

        self.assertEqual(cantidad, 5)

    def test_set_fuera_y_get_fuera_directo_player1(self):
        """Verifica establecer y obtener fichas de player1 fuera."""
        self.board.set_fuera("player1", 4)
        cantidad = self.board.get_fuera("player1")

        self.assertEqual(cantidad, 4)
    def test_movimiento_con_dado_incorrecto(self):
        """Verifica que no se pueda mover usando un dado no disponible."""
        self.board.set_posiciones(0, [Checker("X")])
        dados = [2]
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 5)], dados  # distancia 5, dado 2
        )
        self.assertFalse(resultado["resultados"][0])
        self.assertTrue(
            any("requiere dado" in msg.lower() for msg in resultado["log"])
        )

    def test_movimiento_hacia_atras_invalido_x(self):
        """Verifica movimiento hacia atrás inválido para jugador X."""
        self.board.set_posiciones(5, [Checker("X")])
        resultado = self.board.mover_ficha(
            self.jugador1, [(5, 0)], [5]
        )
        self.assertFalse(resultado["resultados"][0])
        self.assertTrue(
            any("hacia atrás" in msg.lower() for msg in resultado["log"])
        )

    def test_movimiento_hacia_adelante_invalido_o(self):
        """Verifica movimiento hacia adelante inválido para jugador O."""
        self.board.set_posiciones(20, [Checker("O")])
        resultado = self.board.mover_ficha(
            self.jugador2, [(20, 23)], [3]
        )
        self.assertFalse(resultado["resultados"][0])
        self.assertTrue(
            any("hacia adelante" in msg.lower() for msg in resultado["log"])
        )

    def test_movimiento_a_posicion_bloqueada(self):
        """Verifica que no se pueda mover a una posición bloqueada."""
        self.board.set_posiciones(0, [Checker("X")])
        self.board.set_posiciones(5, [Checker("O"), Checker("O")])
        resultado = self.board.mover_ficha(
            self.jugador1, [(0, 5)], [5]
        )
        self.assertFalse(resultado["resultados"][0])
        self.assertTrue(
            any("bloqueada" in msg.lower() for msg in resultado["log"])
        )

    def test_error_puede_comer_fuera_de_rango(self):
        """Verifica que se capture error de puede_comer fuera de rango."""
        datos = {
            'desde': 0,
            'hasta': 99,
            'jugador': self.jugador1,
            'distancia': 3,
            'dados_disponibles': [3],
            'dados_usados': [],
            'log': []
        }
        resultado = self.board._ejecutar_movimiento(datos)
        self.assertFalse(resultado)
        self.assertTrue(any("fuera de rango" in msg for msg in datos["log"]))

    def test_validar_movimiento_indice_fuera_rango(self):
        """Verifica error al validar movimiento con índice fuera de rango."""
        with self.assertRaises(PuntoInvalidoError):
            self.board.validar_movimiento(99, 10, self.jugador1)

    def test_puede_comer_indice_fuera_rango(self):
        """Verifica error al consultar puede_comer fuera de rango."""
        with self.assertRaises(PuntoInvalidoError):
            self.board.puede_comer(100, self.jugador1)

    def test_esta_en_cuadrante_final_valores_invalidos(self):
        """Verifica comportamiento de esta_en_cuadrante_final con valores no válidos."""
        self.assertFalse(self.board.esta_en_cuadrante_final("a", self.jugador1))
        self.assertFalse(self.board.esta_en_cuadrante_final(10, self.jugador1))
        self.assertFalse(self.board.esta_en_cuadrante_final("foo", self.jugador2))
        self.assertFalse(self.board.esta_en_cuadrante_final(15, self.jugador2))


if __name__ == "__main__":
    unittest.main()
