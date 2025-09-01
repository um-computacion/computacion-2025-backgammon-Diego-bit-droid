from core.clases.board import Board  
from core.clases.Dice import Dice

class BackgammonGame:
    def __init__(self):
        self.__turno__ = 0
        self.__movimientos_restantes__ = 0 #usar en lanzar dados y mover ficha
        self.__board__ = Board()
   
    def quien_empieza(self):
        while True:
            jugador1 = self.lanzar_dado()
            jugador2 = self.lanzar_dado()

            print(f"Jugador 1 sacó: {jugador1}")
            print(f"Jugador 2 sacó: {jugador2}")

            if jugador1 > jugador2:
                self.__turno__ = 1
                print("Jugador 1 empieza")
                return 1
            elif jugador2 > jugador1:
                self.__turno__ = 2
                print("Jugador 2 empieza")
                return 2
            else:
                print("Empate, se vuelve a lanzar")

            

    #def get_tablero(self):
        # obtiene el tablero de la clase tablero
        pass

    #def mover_ficha(self):
        pass
        # idea para reglas futuro:hacer if si la ficha sale del tablero    
    #def hay_ganador(self):
        pass

   # def hay_ganador(self):
        pass
        # Regla en la cual se define el ganador todavia falta Aclaracion:ver video

    
    #def cambiar_turno(self):
        pass
        #cambia turno 0 igual a un jugador 1 igual a otro se ve cuando cree la clase jugador
        