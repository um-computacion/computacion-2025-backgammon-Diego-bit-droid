
class Player:
    def __init__(self, nombre, simbolo):
        
        self.__nombre__ = nombre                
        self.__simbolo__ = simbolo              
         # Contadores de fichas de cada jugador
        self.__fichas_en_tablero__ = 15         
        self.__fichas_en_bar__ = 0             
        self.__fichas_sacadas__ = 0    
    def get_nombre(self):
        
                
    def get_simbolo(self):
        
    
    def fichas_en_tablero(self):
        # retorna la cantidad de fichas en el tablero
    

    def fichas_en_bar(self):
        # retorna la cantidad de fichas en el bar relacionado con fichas comidas
        

    def fichas_sacadas(self):
        # retorna la cantidad de fichas sacadas de la mano con las condicion para ganar
        
    def estado_del_player(self):
        # retorna el estado del jugador nombre, símbolo y fichas (en fichas cantidad en el bar cantidad sacadas y cantidad en el tablero)
# estas clases cambian el estado las fichas     
    def ficha_va_al_bar(self):
          
    def ficha_sale_del_bar(self):
      
    def ficha_sale_del_juego(self):
        
    
    

#cuando se necesite relacionar con tablero usar getters en backgamongame