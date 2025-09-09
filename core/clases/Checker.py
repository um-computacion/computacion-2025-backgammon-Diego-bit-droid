class Checker:
    def __init__(self, simbolo):
        self.simbolo = simbolo  # "X" o "O"

    def __str__(self):
        return self.simbolo # Imprime el símbolo de la ficha

    def __repr__(self):
        return self.simbolo  # Imprime el símbolo de la ficha en listas