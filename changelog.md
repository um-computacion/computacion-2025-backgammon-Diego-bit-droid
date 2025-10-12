# Changelog

Todas las modificaciones notables a este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/).


## [1.3.3] - 2025-10-12

### Agregado
- Se incorporaron excepciones personalizadas en español para validar errores de juego, dados, turnos y movimientos
- Se agregaron validaciones explícitas en `BackgammonGame` que lanzan estas excepciones en puntos críticos del flujo.
- Se implementaron pruebas unitarias para verificar que las excepciones se lanzan correctamente y contienen los mensajes esperados.

### Mejorado
- Se refactorizó `BackgammonGame` para cumplir con los principios SOLID, especialmente SRP, OCP y DIP.