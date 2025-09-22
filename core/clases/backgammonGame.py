from core.clases.board import Board
from core.clases.dice import Dice  

class BackgammonGame:
    def __init__(self):
        self.__turno__ = 0
        self.__movimientos_restantes__ = 0 #usar en lanzar dados y mover ficha
        self.__board__ = Board()
        self.__jugadores__ = {}
        self.__dice__ = Dice()
   
    def get_fichas_en_tablero(self, player):
        posiciones = self.__board__.get_tablero()["posiciones"]
        return player.fichas_en_tablero(posiciones)

    def get_fichas_en_bar(self, player):
        bar = self.__board__.get_tablero()["bar"]
        return player.fichas_en_bar(bar)

    def get_fichas_sacadas(self, player):
        fuera = self.__board__.get_tablero()["fuera"]
        return player.fichas_sacadas(fuera)
    def registrar_jugadores(self, jugador1, jugador2):
        self.__jugadores__[jugador1.get_nombre()] = jugador1
        self.__jugadores__[jugador2.get_nombre()] = jugador2
    
    def get_jugador_por_nombre(self, nombre):
        return self.__jugadores__.get(nombre)
    
    def quien_empieza(self):
        while True:
            dado1, _ = self.__dice__.lanzar_dados()
            dado2, _ = self.__dice__.lanzar_dados()

            print(f"Jugador 1 sacó: {dado1}")
            print(f"Jugador 2 sacó: {dado2}")

            if dado1 > dado2:
                self.__turno__ = 1
                print("Jugador 1 empieza")
                return 1
            elif dado2 > dado1:
                self.__turno__ = 2
                print("Jugador 2 empieza")
                return 2
            else:
                print("Empate, se vuelve a lanzar")
    def get_tablero(self):
        return self.__board__.get_tablero()
    def get_jugador_actual(self):
        return self.__jugadores__["jugador1"] if self.__turno__ == 1 else self.__jugadores__["jugador2"]


    #def mover_ficha(self):
        # idea para reglas futuro:hacer if si la ficha sale del tablero
        pass

    #def hay_ganador(self):
        pass

   # def hay_ganador(self):
        pass
        # Regla en la cual se define el ganador todavia falta Aclaracion:ver video

    
    #def cambiar_turno(self):
        pass
        #cambia turno 0 igual a un jugador 1 igual a otro se ve cuando cree la clase jugador
        