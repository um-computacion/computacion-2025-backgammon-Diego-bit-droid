from juego.clases.board import Board  

class BackgammonGame:
    def __init__(self):
        self.__turno__ = 0
        self.__movimientos_restantes__ = 0 #usar en lanzar dados y mover ficha
        self.__board__ = Board()
   
    def quien_empieza(self):
        # el que saque el numero mas alto empieza de ambos jugadores 

    def get_tablero(self):
        # obtiene el tablero de la clase tablero
    
    def lanzar_dados(self):
        # valor se obtiene de otro metodo que existira en la clase dice
    
    def mover_ficha(self, desde, hasta):
        # idea para reglas futuro:hacer if si la ficha sale del tablero    
    def hay_ganador(self):
        # Regla en la cual se define el ganador todavia falta Aclaracion:ver video 
    
    def cambiar_turno(self):
        #cambia turno 0 igual a un jugador 1 igual a otro se ve cuando cree la clase jugador
