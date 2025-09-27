class Checker:
    def __init__(self, simbolo):
        self.__simbolo__ = simbolo  # "X" o "O"

    def get_simbolo(self):
        """
        Devuelve el símbolo que representa la ficha.

        Returns:
            str: símbolo de la ficha, como "X" o "O".
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
        return self