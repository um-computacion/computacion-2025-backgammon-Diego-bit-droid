"""Módulo que define la clase Checker para representar fichas de Backgammon."""

class Checker:
    """Representa una ficha de Backgammon, identificada por un símbolo ('X' o 'O')."""

    def __init__(self, simbolo):
        """
        Inicializa una ficha con el símbolo dado.

        Args:
            simbolo (str): símbolo que representa al jugador, como 'X' o 'O'.
        """
        self.__simbolo__ = simbolo

    def get_simbolo(self):
        """
        Devuelve el símbolo que representa la ficha.

        Returns:
            str: símbolo de la ficha, como 'X' o 'O'.
        """
        return self.__simbolo__

    def __str__(self):
        """
        Representación informal del objeto, usada por print().

        Returns:
            str: símbolo de la ficha.
        """
        return self.__simbolo__

    def __repr__(self):
        """
        Representación formal del objeto, usada en depuración.

        Returns:
            str: símbolo de la ficha.
        """
        return self.__simbolo__
