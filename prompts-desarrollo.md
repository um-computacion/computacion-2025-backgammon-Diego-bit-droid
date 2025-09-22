#Promp1 como puedo hacer que las fichas se generen primero y despues los espacios en blanco
#respueta dada que use  print("".join(line)) 


#2 prompt

**como puedo hacer que en cada turno solo el jugador activo pueda mover sus propias fichas en un juego de backgammon en python**

---

# respuesta

para garantizar que en cada turno solo el jugador activo pueda mover sus propias fichas se recomienda estructurar la logica en tres niveles separados respetando el diseño orientado a objetos

## 1 control de turno en la clase backgammongame

la clase `backgammongame` debe mantener una variable interna que indique a quien le toca jugar por ejemplo `__turno__ = 1` para jugador1 y `__turno__ = 2` para jugador2

se debe implementar un metodo `get_jugador_actual()` que devuelva el jugador correspondiente segun el turno actual

```python
def get_jugador_actual(self):
    if self.__turno__ == 1:
        return self.__jugador1__
    elif self.__turno__ == 2:
        return self.__jugador2__


