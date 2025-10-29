# Justificación de Diseño - Backgammon

## 1. Resumen del Diseño General

El proyecto implementa el juego Backgammon siguiendo principios de programación orientada a objetos. La arquitectura se organizó en capas claramente definidas:

- **Capa de Dominio**: Contiene las entidades fundamentales del juego (Checker, Player, Board, Dice)
- **Capa de Lógica**: Coordina las reglas y el flujo del juego (BackgammonGame)
- **Capa de Presentación**: Maneja la interacción con el usuario (BackgammonCLI)
- **Capa de Validación**: Aplica reglas específicas del juego (validaciones.py)

Esta separación permite que cada componente tenga una responsabilidad específica y sea fácil de mantener o extender.

## 2. Justificación de Clases

### 2.1 Checker
**Responsabilidad**: Representar una ficha individual en el tablero.

**Justificación**: Aunque podría haberse usado simplemente un string ('X' o 'O'), crear una clase Checker permite:
- Extensibilidad futura (agregar color, jugador propietario, etc.)
- Encapsulamiento del símbolo
- Facilita el polimorfismo si en el futuro se necesitan diferentes tipos de fichas

### 2.2 Player
**Responsabilidad**: Representar a un jugador con su identidad y métodos para consultar su estado.

**Justificación**: Centraliza toda la información relacionada con un jugador específico. Los métodos como `fichas_en_tablero()`, `fichas_en_bar()` y `fichas_sacadas()` evitan que otras clases tengan que conocer la estructura interna del tablero para hacer estos cálculos. Esto sigue el principio de Tell, Don't Ask.

### 2.3 Board
**Responsabilidad**: Gestionar el estado físico del tablero y ejecutar movimientos.

**Justificación**: Es el componente más complejo porque contiene toda la lógica de movimiento y validación a nivel de tablero. Se decidió que Board sea responsable de:
- Verificar si un movimiento es físicamente posible
- Actualizar el estado del tablero
- Validar reglas específicas del tablero (comer fichas, bearing off, etc.)

Esta clase NO conoce las reglas del juego (como turnos o dados), solo la física del tablero.

### 2.4 Dice
**Responsabilidad**: Simular el lanzamiento de dados.

**Justificación**: Aunque simple, separar los dados en su propia clase permite:
- Testear comportamientos aleatorios de manera controlada
- Potencial para implementar dados cargados o determinísticos en testing
- Cumple con Single Responsibility Principle

### 2.5 BackgammonGame
**Responsabilidad**: Orquestar el flujo completo del juego.

**Justificación**: Actúa como controlador principal que coordina:
- Gestión de turnos
- Lanzamiento de dados y cálculo de movimientos disponibles
- Delegación de movimientos al Board
- Verificación de condiciones de victoria
- Aplicación de reglas del juego

Esta clase conoce las reglas de alto nivel pero delega la ejecución a las clases especializadas.

### 2.6 BackgammonCLI
**Responsabilidad**: Interfaz de usuario por línea de comandos.

**Justificación**: Completamente separada de la lógica del juego. Solo se encarga de:
- Mostrar menús y mensajes
- Capturar entrada del usuario
- Parsear comandos
- Llamar a BackgammonGame

Esta separación permite reemplazar fácilmente el CLI por una GUI sin tocar la lógica del juego.

## 3. Justificación de Atributos

### Board
```python
self.__posiciones__ = []        # Las 24 posiciones del tablero
self.__bar__ = {}               # Fichas capturadas por jugador
self.__fuera__ = {}             # Fichas que salieron del juego
```

**Justificación**:
- `__posiciones__`: Lista de 24 listas (pilas) que representa cada punto del tablero. Permite operaciones O(1) para acceder a cualquier posición.
- `__bar__` y `__fuera__`: Diccionarios indexados por nombre de jugador para acceso directo.
- Todos privados (doble underscore) para proteger la integridad del estado del tablero.

### BackgammonGame
```python
self.__board__ = Board()                    # Gestiona estado físico del tablero
self.__dice__ = Dice()                      # Genera valores aleatorios
self.__turno__ = 0                          # 0: no iniciado, 1: jugador1, 2: jugador2
self.__movimientos_restantes__ = 0         # Movimientos disponibles en turno actual
self.__jugador1__ = Player(nombre, 'X')    # Primer jugador (mueve 0→23)
self.__jugador2__ = Player(nombre, 'O')    # Segundo jugador (mueve 23→0)
self.__reglas__ = reglas if reglas else [] # Validaciones customizables
```

**Justificación**:
- `__board__`: Composición en lugar de herencia. Game orquesta pero no ES un tablero.
- `__dice__`: Separado permite testear con dados determinísticos si fuera necesario.
- `__turno__`: Usar 0 como estado "no iniciado" evita tener un booleano adicional y permite validaciones claras.
- `__movimientos_restantes__`: Crucial para saber cuándo cambiar de turno automáticamente. Se actualiza dinámicamente según dados.
- `__jugador1__` y `__jugador2__`: Referencias directas a objetos Player evitan búsquedas repetitivas.
- `__reglas__`: Lista de funciones callable permite estrategia de validación flexible sin modificar código base (OCP).

### Player
```python
self.__nombre__ = nombre
self.__ficha__ = ficha    # 'X' o 'O'
```

**Justificación**: Mínimos atributos necesarios. El jugador no guarda su propio estado de fichas porque eso lo gestiona el Board. Esto evita duplicación y mantiene una única fuente de verdad.

## 4. Decisiones de Diseño Relevantes

### 4.1 Uso de "bar" y "fuera" como Strings
En lugar de usar posiciones especiales (-1, 24), usamos strings literales:
```python
desde = "bar"
hasta = "fuera"
```

**Ventajas**:
- Más legible en el código
- Evita confusiones con índices negativos
- Facilita el parseo de comandos del usuario
- Type hints más claros

### 4.2 Movimientos como Lista de Tuplas
```python
movimientos = [(desde, hasta), (desde, hasta), ...]
```

**Justificación**: Permite mover múltiples fichas en una sola llamada, lo cual es necesario cuando se sacan dobles (4 movimientos). Es más eficiente que hacer 4 llamadas separadas.

### 4.3 Validación en Dos Niveles
1. **BackgammonGame**: Valida reglas de alto nivel (turnos, dados disponibles)
2. **Board**: Valida reglas físicas del tablero

Esta separación evita que Board tenga que conocer sobre turnos o dados, manteniendo las responsabilidades claras.

### 4.4 Método `_procesar_movimiento_individual`
Movimiento complejo dividido en:
```python
mover_ficha() -> _procesar_movimiento_individual() -> _ejecutar_movimiento()
```

**Justificación**: Cada método tiene una responsabilidad única:
- Validar formato general
- Validar movimiento individual
- Ejecutar físicamente el movimiento

### 4.5 Sistema de Log
Cada movimiento genera un log explicativo:
```python
return {
    "resultados": [True, False],
    "dados_usados": [3, 5],
    "dados_restantes": [],
    "log": ["X movió de 0 a 3", "Movimiento inválido..."]
}
```

**Justificación**: Permite al CLI informar al usuario exactamente qué pasó sin que Board o Game tengan que imprimir directamente. Cumple con Separation of Concerns.

## 5. Excepciones y Manejo de Errores

### Jerarquía de Excepciones

```
ErrorBackgammon (base)
├── ErrorJuego
│   ├── JuegoNoInicializadoError
│   ├── TurnoJugadorInvalidoError
│   ├── JuegoYaFinalizadoError
│   ├── MovimientoInvalidoError
│   └── SinMovimientosDisponiblesError
├── ErrorTablero
│   ├── PuntoInvalidoError
│   ├── MovimientoMalFormadoError
│   └── ... (otras específicas del tablero)
└── ErrorDados
    ├── ValorDadoInvalidoError
    └── DadosNoLanzadosError
```

**Justificación de la Jerarquía**:

La estructura jerárquica permite capturar excepciones a diferentes niveles de granularidad:

```python
try:
    juego.mover_ficha(...)
except ErrorTablero:
    # Manejar cualquier error de tablero
except ErrorJuego:
    # Manejar cualquier error de juego
```

### Excepciones Específicas

**JuegoNoInicializadoError**: Se lanza cuando se intenta acceder al turno actual sin haber iniciado el juego. Evita que el sistema opere en estado inconsistente.

**ValorDadoInvalidoError**: Protege contra valores de dados fuera del rango 1-6. Crítico para mantener la integridad del juego.

**MovimientoMalFormadoError**: Se lanza cuando el formato de entrada no es válido. Separa errores de entrada de errores lógicos.

**PuntoInvalidoError**: Previene accesos fuera de rango al tablero. Fundamental para la estabilidad del programa.

### Estrategia de Manejo

1. **Lanzar en capas bajas**: Las excepciones se lanzan donde se detecta el problema
2. **Capturar en capas altas**: El CLI captura y presenta mensajes amigables
3. **No silenciar**: Nunca se captura sin registrar o informar

## 6. Estrategias de Testing y Cobertura

### 6.1 Organización de Tests

Los tests se organizaron en clases según la funcionalidad probada:

```
TestBackgammonGameInit
TestBackgammonGameCalcularMovimientos
TestBackgammonGameJugadores
TestBoardInit
TestBoardValidarMovimiento
...
```

### 6.2 Tipos de Tests Implementados

**Tests Unitarios Puros**:
- Sin mocks ni dependencias externas
- Prueban comportamiento de clases individuales
- Ejemplo: `test_parsear_movimiento_formato_espacio()`

**Tests de Integración**:
- Prueban interacción entre componentes
- Ejemplo: `test_movimiento_valido_multiple()` prueba Game + Board + Player

**Tests de Casos Límite**:
- Valores extremos (dados 1-1, 6-6)
- Posiciones límite (0, 23)
- Listas vacías, strings especiales ("bar", "fuera")

### 6.3 Cobertura por Componente

**Checker (100%)**:
- Constructor
- Getters
- Métodos `__str__` y `__repr__`

**Player**:
- Creación con diferentes nombres
- Métodos de conteo de fichas
- Estado del jugador

**Dice**:
- Lanzamiento produce valores válidos
- Valores se almacenan correctamente

**Board (98%)**:
- Inicialización y preparación
- Validación de movimientos
- Cálculo de distancias
- Eating (comer fichas)
- Bearing off
- Casos de error

**BackgammonGame (96%)**:
- Inicialización
- Gestión de turnos
- Lanzamiento de dados
- Movimientos simples y complejos
- Detección de ganador
- Manejo de excepciones

**CLI**:
- Parseo de comandos
- Diferentes formatos de entrada
- Manejo de errores de formato

### 6.4 Tests de Comportamiento Aleatorio

Para `quien_empieza()` que es aleatorio:
```python
def test_quien_empieza_multiple_veces(self):
    turnos = set()
    for _ in range(10):
        game = BackgammonGame("player1", "player2")
        turno, _, _ = game.quien_empieza()
        turnos.add(turno)
    self.assertTrue(1 in turnos or 2 in turnos)
```

Ejecutamos múltiples veces y verificamos que al menos se produce algún resultado válido.

### 6.5 Tests de Regresión

Tests específicos para bugs encontrados:
```python
def test_cambio_turno_despues_movimientos(self):
    """Bug: el turno no cambiaba después de usar todos los movimientos"""
    ...
```
## 7. Principios SOLID

### 7.1 Single Responsibility Principle (SRP)

**Cumplimiento**:
- `Checker`: Solo representa una ficha
- `Player`: Solo gestiona identidad y consultas de estado del jugador
- `Board`: Solo gestiona el estado físico del tablero
- `Dice`: Solo genera números aleatorios
- `BackgammonGame`: Solo coordina el flujo del juego
- `BackgammonCLI`: Solo maneja interfaz de usuario

**Ejemplo de violación evitada**:
No pusimos lógica de impresión en Board o Game. Eso lo hace CLI.

### 7.2 Open/Closed Principle (OCP)

**Cumplimiento**:
- El parámetro `reglas` en BackgammonGame permite agregar reglas sin modificar la clase:
```python
def __init__(self, jugador1, jugador2, reglas=None):
    self.__reglas__ = reglas if reglas else []
```

- Nuevas validaciones se pueden agregar en `validaciones.py` sin tocar Board

**Extensibilidad**:
- Podríamos agregar un `BoardVisualizer` sin modificar Board
- Podríamos crear `BackgammonGUI` sin tocar BackgammonGame

### 7.3 Liskov Substitution Principle (LSP)

**Cumplimiento**:
Aunque no usamos herencia extensivamente, donde la usamos (excepciones) se respeta:
```python
class ErrorJuego(ErrorBackgammon):
    pass
```

Cualquier código que capture `ErrorBackgammon` funcionará correctamente con `ErrorJuego`.

### 7.4 Interface Segregation Principle (ISP)

**Cumplimiento**:
- Board expone solo los métodos necesarios para cada cliente
- CLI solo usa métodos públicos de Game, no accede directamente a Board
- Player no tiene métodos que no use nadie

**Evitamos interfaces gordas**:
No hay una clase `GameManager` con 50 métodos. Cada clase tiene una API mínima.

### 7.5 Dependency Inversion Principle (DIP)

**Cumplimiento Parcial**:
- CLI depende de la abstracción (interfaz pública) de Game, no de detalles internos
- Game depende de la interfaz de Board, no de cómo Board almacena las posiciones

**Mejora Posible**:
Podríamos haber usado interfaces abstractas (ABC) para Board y Dice, permitiendo inyectar implementaciones diferentes para testing.

## 8. Patrones de Diseño Identificables

### 8.1 Facade Pattern
`BackgammonGame` actúa como fachada que simplifica la interacción con Board, Dice, y Players. El CLI no necesita conocer la complejidad interna.

### 8.2 Strategy Pattern
El parámetro `reglas` permite inyectar diferentes estrategias de validación sin modificar el código base.

### 8.3 Template Method (implícito)
```python
mover_ficha() -> _procesar_movimiento_individual() -> _ejecutar_movimiento()
```
Define el esqueleto del algoritmo de mover fichas.

## 9. Anexos

### 9.1 Diagrama de Clases Simplificado

```
┌─────────────────┐
│ BackgammonCLI   │
│─────────────────│
│ + ejecutar()    │
│ + parsear_mov() │
└────────┬────────┘
         │ usa
         ▼
┌─────────────────────┐      ┌──────────┐
│ BackgammonGame      │──────│  Dice    │
│─────────────────────│  usa │──────────│
│ - board             │      │+ lanzar()│
│ - jugador1          │      └──────────┘
│ - jugador2          │
│ - turno             │
│─────────────────────│
│ + lanzar_dados()    │
│ + mover_ficha()     │
│ + cambiar_turno()   │
│ + hay_ganador()     │
└──────────┬──────────┘
           │ usa
           ▼
      ┌─────────┐        ┌──────────┐
      │  Board  │────────│  Checker │
      │─────────│ tiene  │──────────│
      │- pos[]  │        │- simbolo │
      │- bar    │        └──────────┘
      │- fuera  │
      │─────────│
      │+ mover()│
      └─────────┘
           △
           │ consulta
           │
      ┌─────────┐
      │  Player │
      │─────────│
      │- nombre │
      │- ficha  │
      └─────────┘
```

### 9.2 Flujo de un Movimiento

```
Usuario ingresa: "10 15"
         ↓
    [CLI.mover_fichas()]
         ↓
    Parsea: (10, 15)
         ↓
    [Game.mover_ficha([(10,15)], 3, 5)]
         ↓
    Valida: ¿Hay movimientos? ¿Dados disponibles?
         ↓
    [Board.mover_ficha(jugador, [(10,15)], [3,5])]
         ↓
    [_procesar_movimiento_individual()]
         ↓
    Valida: ¿Ficha propia? ¿Distancia correcta? ¿Bar vacío?
         ↓
    [_ejecutar_movimiento()]
         ↓
    Actualiza: posiciones, bar, fuera
         ↓
    Retorna: {resultados, dados_usados, log}
         ↓
    [Game] Actualiza movimientos_restantes
         ↓
    [CLI] Muestra resultado al usuario
```

### 9.3 Decisiones Técnicas Adicionales

**Uso de Listas vs Arrays**:
Elegimos listas de Python por simplicidad y porque el tablero es pequeño (24 posiciones). La diferencia de performance es negligible.

**Diccionarios para Bar y Fuera**:
Usar diccionarios con claves 'player1' y 'player2' es más legible que listas indexadas.

**Métodos Privados con Doble Underscore**:
Usamos `__atributo__` para true privacy. Python permite acceder con name mangling, pero indica clara intención de privacidad.

**No usar Type Hints**:
Decisión consciente para mantener compatibilidad con versiones anteriores de Python y evitar complejidad adicional en el código académico.

---

## Conclusión

El diseño presentado balancea simplicidad con extensibilidad. Cada decisión se tomó considerando:
1. Mantenibilidad del código
2. Facilidad de testing
3. Claridad para futuros desarrolladores
4. Adherencia a principios SOLID

El resultado es un sistema modular donde cada componente tiene responsabilidades claras y puede ser modificado o extendido sin afectar al resto del sistema.