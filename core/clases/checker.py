class Checker:
    def __init__(self, simbolo):
        self.__simbolo__ = simbolo  # "X" o "O"

    def get_simbolo(self):
        """
        Entrada:
            None
        Salida:
            str: símbolo de la ficha
        """
        return self.__simbolo__

    def __str__(self):
        return self.__simbolo__

    def __repr__(self):
        return self.__simbolo__