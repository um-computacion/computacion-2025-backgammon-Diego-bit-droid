# Changelog

Todas las modificaciones notables a este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).


## [1.3.2] - 2025-09-30

### Corregido
- Se corrigió la validación del cuadrante final para cada jugador: ahora `player1` debe tener todas sus fichas entre las posiciones 18 y 23, y `player2` entre las posiciones 0 y 5 para poder sacar fichas.

### Agregado
- Se agregó una validación que impide capturar múltiples fichas enemigas en una sola posición.
- Se ajustaron los mensajes de log para reflejar correctamente los motivos de movimientos inválidos.