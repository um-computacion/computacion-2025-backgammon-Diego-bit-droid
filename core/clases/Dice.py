import random 

class Dice:
    def __init__(self):
        self.__dado1__ = 0
        self.__dado2__ = 0
        
    def lanzar_dados(self):
        self.__dado1__ = random.randint(1, 6)
        self.__dado2__ = random.randint(1, 6)
        return self.__dado1__, self.__dado2__