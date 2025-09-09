
class Player:
    def __init__(self, nombre, ficha):
        
        self.__nombre__ = nombre                
        self.__ficha__ = ficha             
         # Contadores de fichas de cada jugador
        self.__fichas_en_tablero__ = 15         
        self.__fichas_en_bar__ = 0             
        self.__fichas_sacadas__ = 0    
    
    def get_nombre(self):
        return self.__nombre__

    def get_ficha(self):
        return self.__ficha__

    def fichas_en_tablero(self, posiciones):
        cantidad = sum(pos.count(self.__ficha__) for pos in posiciones)
        self.__fichas_en_tablero__ = cantidad
        return cantidad

    def fichas_en_bar(self, fichas_en_bar):
        cantidad = fichas_en_bar.count(self.__ficha__)
        self.__fichas_en_bar__ = cantidad
        return cantidad

    def fichas_sacadas(self, fichas_fuera):
        cantidad = fichas_fuera.count(self.__ficha__)
        self.__fichas_sacadas__ = cantidad
        return cantidad

    def estado_jugador(self):
        return {
            "nombre": self.__nombre__,
            "ficha": self.__ficha__,
            "en_tablero": self.__fichas_en_tablero__,
            "en_bar": self.__fichas_en_bar__,
            "sacadas": self.__fichas_sacadas__,
            "total": self.__fichas_en_tablero__ + self.__fichas_en_bar__ + self.__fichas_sacadas__
        }    
    def ficha_va_al_bar(self):

        pass
          
    def ficha_sale_del_bar(self):
        pass
      
    def ficha_sale_del_juego(self):
        pass
        
    
    

#cuando se necesite relacionar con tablero usar getters en backgamongame