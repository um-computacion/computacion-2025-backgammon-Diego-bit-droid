# Changelog

Todas las modificaciones notables a este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

## [1.0.0] - 2025-08-27

### Agregado 
-Creacion de clases Checker,Board,Backgammon,Player,Dice
- Método `mostrarTabla` para visualizar la tabla en consola o interfaz.
- Método `prepararTabla` para inicializar o configurar los datos de la tabla.
- Método `lanzarDado` que simula una tirada de dado para el juego.
## [1.0.1] - 2025-08-29

### Agregado 
- Metodo calcular movimientos 
## [1.1.1] - 2025-08-29

### Agregado 
- Metodo lanzar dado
- Metodo y forma nueva para crear fichas y tablero
- Metodo obtener estado del jugador
## [1.1.2] - 2025-09-15

### Agregado 
- Metodo de mover fichas

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).

## [1.1.3] - 2025-09-15

### Agregado 
-Test mover ficha 
-Inicio de turnos 

## [1.1.4] - 2025-09-22

### Agregado 
-Implementacion de turnos 
## [1.2.0] - 2025-09-28

### Agregado
- Implementación de tests unitarios para la clase `Board`.
- Cobertura de casos como movimientos válidos, comer fichas, sacar fuera y entrada desde el bar.
# [1.3.0] - 2025-09-29

### Agregado
- Regla en `BackgammonGame`: si un jugador tiene fichas en el bar, debe moverlas antes de cualquier otra ficha.

## [1.3.1] - 2025-09-30

### Agregado
- Se agregó la regla que obliga a sacar fichas del bar antes de mover otras.
- Se implementó la lógica para permitir sacar fichas del tablero solo si todas están en el cuadrante final.
- Se muestra un mensaje cuando el jugador puede empezar a sacar fichas.
- Si no hay movimientos posibles con los dados, el turno se pasa automáticamente.

## [1.3.2] - 2025-09-30

### Corregido
- Se corrigió la validación del cuadrante final para cada jugador: ahora `player1` debe tener todas sus fichas entre las posiciones 18 y 23, y `player2` entre las posiciones 0 y 5 para poder sacar fichas.

### Agregado
- Se agregó una validación que impide capturar múltiples fichas enemigas en una sola posición.
- Se ajustaron los mensajes de log para reflejar correctamente los motivos de movimientos inválidos.
## [1.3.3] - 2025-10-12
### Agregado
- Se incorporaron excepciones personalizadas en español para validar errores de juego, dados, turnos y movimientos
- Se agregaron validaciones explícitas en `BackgammonGame` que lanzan estas excepciones en puntos críticos del flujo.
- Se implementaron pruebas unitarias para verificar que las excepciones se lanzan correctamente y contienen los mensajes esperados.

### Mejorado
- Se refactorizó `BackgammonGame` para cumplir con los principios SOLID, especialmente SRP, OCP y DIP.

## [1.3.4] - 2025-10-13

### Agregado
- Se incorporaron excepciones personalizadas para validar errores del board

## [1.4.0] - 2025-10-21

### Refactorizado
- Todas las clases del proyecto fueron reestructuradas para cumplir con los estándares de estilo y calidad de Pylint, alcanzando una calificación de 10/10.
- Se corrigieron líneas demasiado largas, indentación incorrecta, espacios finales, accesos a miembros protegidos y docstrings faltantes.
- Se eliminaron métodos duplicados y se reorganizaron las pruebas para mejorar la mantenibilidad y claridad.
## [1.5.0] - 2025-10-21

### Refactorizado
- Todas las clases del proyecto fueron reestructuradas para cumplir con los estándares de estilo y calidad de Pylint, alcanzando una calificación de 10/10.
### Implementacion
-Implementacion del cli
### Refactorizado
- Todas las clases del proyecto fueron reestructuradas para cumplir con los estándares de estilo y calidad de Pylint, alcanzando una calificación de 10/10.
### Implementacion
-Implementacion del cli
-Implementacion de nuevas excepciones 
-Implementacion de nuevos test
## [1.5.1] - 2025-10-28

### Implementacion
-Implementacion de mock en los test de cli y board
-Creacion parcial del pygame
-validacion de movientos legales y disponibles
## [1.6.0] - 2025-10-30

### Implementacion
-Finalizacion del pygame
-Creacion de justificacion
-Nueva implementacion de dados usados en backgammon
-Implementacion de nuevo metodos de verifcacion de movientos legales y de opciones en la partida 
-Implementacion de nuevo metodo en backgammon para evitar el uso de logica en cli
-cambio en la disposicion de archivos
## [1.6.1] - 2025-10-31

### Correciones
-Correcion en metodo hay gandor identificaba mal al jugador

### Implementacion 
-Implementacion de test para optima cobertura 
