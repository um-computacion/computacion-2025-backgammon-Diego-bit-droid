"""Módulo que define la clase Dice para simular lanzamientos de dados en Backgammon."""

import random


class Dice:
    """Representa un par de dados de seis caras para el juego de Backgammon."""

    def __init__(self):
        """Inicializa los valores de los dados en cero."""
        self.__dado1__ = 0
        self.__dado2__ = 0

    def lanzar_dados(self):
        """
        Simula el lanzamiento de dos dados de seis caras.

        Returns:
            tuple: una tupla con dos enteros entre 1 y 6, representando los valores de los dados.
        """
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)
        return self.__dado1__, self.__dado2__
    def get_valores(self):
        """
        Devuelve los valores actuales de los dados sin lanzar nuevos.

        Returns:
            tuple: valores actuales de dado1 y dado2.
        """
        return self.__dado1__, self.__dado2__
