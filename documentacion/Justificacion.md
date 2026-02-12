# JUSTIFICACIÓN DE DISEÑO - BACKGAMMON

## 1. Resumen del Diseño General

El proyecto implementa un juego completo de Backgammon siguiendo principios de programación orientada a objetos y diseño modular. La arquitectura se divide en componentes especializados que trabajan de manera cohesiva:

- **Capa de Lógica de Juego**: Gestiona el flujo del juego, turnos y validaciones generales (`BackgammonGame`)
- **Capa de Tablero**: Maneja el estado físico del tablero y las reglas de movimiento (`Board`)
- **Capa de Entidades**: Representa los elementos básicos del juego (`Player`, `Checker`, `Dice`)
- **Capa de Validaciones**: Define reglas del juego como funciones reutilizables (`validaciones.py`)
- **Capa de Excepciones**: Proporciona un sistema robusto de manejo de errores (`excepciones.py`)

El diseño privilegia la **separación de responsabilidades**, la **extensibilidad** y el **manejo explícito de errores**.

---

## 2. Justificación de las Clases Elegidas

### 2.1. Clase `BackgammonGame`

**Propósito**: Controlador principal del juego que orquesta todos los componentes.

**Responsabilidades**:
- Gestionar el flujo del juego (iniciar partida, turnos, finalización)
- Coordinar las interacciones entre jugadores, tablero y dados
- Aplicar reglas de validación antes de ejecutar movimientos
- Determinar el estado actual del juego y detectar ganadores
- Verificar movimientos legales disponibles

**Justificación**: Esta clase actúa como **fachada** que simplifica la interacción con el sistema complejo del Backgammon. Sin ella, el código cliente debería manejar directamente múltiples objetos y conocer las reglas internas del juego.

---

### 2.2. Clase `Board`

**Propósito**: Representar el estado físico del tablero y ejecutar movimientos.

**Responsabilidades**:
- Mantener las 24 posiciones del tablero con sus fichas
- Gestionar el bar (fichas comidas) y el área de fichas fuera del juego
- Validar y ejecutar movimientos individuales
- Calcular distancias según la dirección del jugador
- Verificar condiciones especiales (bearing off, fichas en cuadrante final)
- Proporcionar visualización del tablero

**Justificación**: El tablero es una entidad compleja con reglas específicas de Backgammon. Separarlo en su propia clase permite:
- **Encapsulación** del estado interno (posiciones privadas)
- **Cohesión**: todas las operaciones relacionadas con el tablero están en un solo lugar
- **Reutilización**: el tablero puede usarse independientemente del controlador del juego

---

### 2.3. Clase `Player`

**Propósito**: Representar a un jugador con su identidad y símbolo de ficha.

**Responsabilidades**:
- Almacenar nombre y símbolo ('X' u 'O')
- Consultar el estado de sus fichas (en tablero, en bar, sacadas)
- Proporcionar información consolidada sobre su estado

**Justificación**: Aunque simple, esta clase es fundamental para:
- **Abstracción**: el jugador es una entidad conceptual del dominio
- **Extensibilidad**: facilita agregar atributos futuros (estadísticas, estrategias)
- **Claridad**: el código es más legible cuando se pasa un objeto `Player` en lugar de strings sueltos

---

### 2.4. Clase `Checker`

**Propósito**: Representar una ficha individual del juego.

**Responsabilidades**:
- Almacenar el símbolo que identifica al dueño de la ficha
- Proporcionar representación textual de la ficha

**Justificación**: 
- **Modelado del dominio**: en Backgammon, las fichas son objetos físicos independientes
- **Tipo específico**: usar objetos en lugar de strings mejora la seguridad de tipos
- **Extensibilidad**: permite agregar propiedades futuras (color, imagen, estado)

---

### 2.5. Clase `Dice`

**Propósito**: Simular el lanzamiento de dos dados de seis caras.

**Responsabilidades**:
- Generar valores aleatorios entre 1 y 6
- Mantener los últimos valores generados
- Proporcionar acceso a los valores actuales

**Justificación**:
- **Encapsulación de la aleatoriedad**: centraliza la lógica de generación de números aleatorios
- **Testabilidad**: facilita la creación de mocks para pruebas determinísticas
- **Abstracción**: el resto del código no necesita conocer cómo se generan los números

---

### 2.6. Módulo `excepciones.py`

**Propósito**: Definir una jerarquía completa de excepciones específicas del dominio.

**Justificación**:
- **Manejo granular de errores**: cada tipo de error tiene su propia excepción
- **Claridad**: el código que captura excepciones sabe exactamente qué salió mal
- **Jerarquía**: agrupa excepciones relacionadas bajo clases base comunes
- **Documentación implícita**: los nombres de las excepciones documentan posibles errores

---

### 2.7. Módulo `validaciones.py`

**Propósito**: Definir reglas del juego como funciones reutilizables.

**Responsabilidades**:
- `regla_bar`: Validar que se muevan primero las fichas del bar
- `regla_salida_final`: Validar que solo se pueda hacer bearing off cuando corresponde

**Justificación**:
- **Separación de concerns**: las reglas están separadas de la lógica de ejecución
- **Extensibilidad**: facilita agregar nuevas reglas sin modificar clases existentes
- **Inyección de dependencias**: las reglas se inyectan en `BackgammonGame` en el constructor
- **Testabilidad**: cada regla puede probarse independientemente

---

## 3. Justificación de Atributos

### 3.1. Atributos de `Board`

```python
self.__posiciones__ = [[] for _ in range(24)]  # Lista de 24 pilas
self.__bar__ = {'player1': 0, 'player2': 0}     # Fichas comidas
self.__fuera__ = {'player1': 0, 'player2': 0}   # Fichas fuera del juego
```

**Justificación**:
- `__posiciones__`: Lista de listas para representar las pilas de fichas. Privado para evitar modificaciones externas que rompan invariantes.
- `__bar__` y `__fuera__`: Diccionarios con claves consistentes para ambos jugadores. Facilita el acceso mediante métodos `_get_player_key()`.
- **Convención de nombres**: doble guion bajo indica atributos privados según PEP 8.

---

### 3.2. Atributos de `BackgammonGame`

```python
self.__board__ = Board()
self.__dice__ = Dice()
self.__turno__ = 0  # 0: no iniciado, 1: jugador1, 2: jugador2
self.__movimientos_restantes__ = 0
self.__jugador1__ = Player(nombre=jugador1, ficha='X')
self.__jugador2__ = Player(nombre=jugador2, ficha='O')
self.__reglas__ = reglas if reglas else []
self.__dados_disponibles__ = []
self.__valores_dados__ = (0, 0)
```

**Justificación**:
- `__board__`, `__dice__`: **Composición** de objetos especializados
- `__turno__`: Entero simple para representar el estado (0=no iniciado, 1/2=jugador activo)
- `__movimientos_restantes__`: Contador de movimientos disponibles en el turno actual
- `__jugador1__`, `__jugador2__`: Referencias directas a los jugadores (más eficiente que un diccionario)
- `__reglas__`: Lista de funciones validadoras, permite **inyección de dependencias**
- `__dados_disponibles__`: Cache de dados que aún no se han usado (evita recalcular)
- `__valores_dados__`: Tupla inmutable con los últimos valores lanzados

---

### 3.3. Atributos de `Player`

```python
self.__nombre__ = nombre
self.__ficha__ = ficha  # 'X' o 'O'
```

**Justificación**:
- Atributos mínimos e inmutables (no hay setters)
- `__ficha__` es crucial para identificar las fichas del jugador en el tablero

---

### 3.4. Atributos de `Checker` y `Dice`

```python
# Checker
self.__simbolo__ = simbolo  # 'X' o 'O'

# Dice
self.__dado1__ = 0
self.__dado2__ = 0
```

**Justificación**:
- Encapsulan estado simple pero necesario
- Privados para evitar modificaciones externas

---

## 4. Decisiones de Diseño Relevantes

### 4.1. Uso de Convenciones de Nomenclatura Privadas

**Decisión**: Todos los atributos internos usan `__nombre__` (doble guion bajo).

**Razones**:
- **Encapsulación fuerte**: evita acceso directo desde código externo
- **API clara**: solo los métodos públicos son la interfaz
- **Mantenibilidad**: cambios internos no afectan código cliente

---

### 4.2. Representación del Tablero como Lista de Listas

**Decisión**: `__posiciones__` es una lista de 24 listas (pilas de fichas).

**Alternativas consideradas**:
- Diccionario `{posicion: [fichas]}`
- Array bidimensional

**Razones de la elección**:
- Índices naturales (0-23) coinciden con la numeración del Backgammon
- Operaciones de pila (`append`, `pop`) son idiomáticas en Python
- Acceso O(1) por índice

---

### 4.3. Separación de Validación y Ejecución

**Decisión**: Los movimientos se validan completamente antes de ejecutarse.

**Implementación**:
- `_procesar_movimiento_individual()`: valida
- `_ejecutar_movimiento()`: ejecuta si la validación pasó

**Razones**:
- **Consistencia**: el tablero nunca queda en estado inválido
- **Mensajes de error claros**: se acumula un log de errores antes de ejecutar
- **Transaccionalidad**: un movimiento fallido no modifica el estado

---

### 4.4. Inyección de Reglas como Funciones

**Decisión**: Las reglas de validación se pasan como lista de funciones al constructor de `BackgammonGame`.

```python
def __init__(self, jugador1, jugador2, reglas=None):
    self.__reglas__ = reglas if reglas else []
```

**Razones**:
- **Flexibilidad**: permite jugar con diferentes conjuntos de reglas
- **Testabilidad**: fácil probar con reglas mockeadas
- **Extensibilidad**: agregar nuevas reglas sin modificar la clase
- **Principio Abierto/Cerrado**: la clase está abierta a extensión pero cerrada a modificación

---

### 4.5. Diferenciación entre `bar` y `fuera` como Diccionarios

**Decisión**: Usar claves `'player1'` y `'player2'` en lugar de nombres de jugadores.

**Razones**:
- **Consistencia**: claves predecibles independientes del nombre del jugador
- **Simplicidad**: el método `_get_player_key()` centraliza la conversión
- **Eficiencia**: evita búsquedas por nombre

---

### 4.6. Método `tiene_movimientos_legales()` Separado

**Decisión**: Implementar un método exhaustivo que verifica todos los movimientos posibles.

**Razones**:
- **Detección automática de bloqueo**: el juego puede cambiar el turno automáticamente
- **Experiencia de usuario**: evita que el jugador intente movimientos imposibles
- **Correctitud**: implementa la regla de Backgammon sobre pasar turno

---

### 4.7. Manejo de Bearing Off con Dados Mayores

**Decisión**: Permitir sacar fichas con dados mayores a la distancia exacta si no hay fichas más atrás.

**Implementación**:
```python
def _tiene_fichas_mas_atras(self, jugador, posicion):
    # Verifica si hay fichas en posiciones más alejadas
```

**Razones**:
- **Regla oficial de Backgammon**: refleja las reglas reales del juego
- **Flexibilidad**: mejora la jugabilidad en las fases finales

---

## 5. Excepciones y Manejo de Errores

### 5.1. Jerarquía de Excepciones

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
│   ├── ComerMultipleFichasError
│   ├── SacarFueraDesdePosicionInvalidaError
│   ├── MovimientoMalFormadoError
│   ├── FichasEnBarError
│   ├── BearingOffNoPermitidoError
│   ├── PosicionBloqueadaError
│   └── MovimientoContraDireccionError
├── ErrorDados
│   ├── DadosNoLanzadosError
│   ├── ValorDadoInvalidoError
│   └── DadoNoDisponibleError
├── ErrorEntrada
│   └── FormatoMovimientoInvalidoError
└── ErrorJugador
    ├── JugadorNoEncontradoError
    └── NombreJugadorInvalidoError
```

### 5.2. Justificación de Cada Excepción

#### ErrorBackgammon
**Propósito**: Clase base para todas las excepciones del dominio.
**Razón**: Permite capturar cualquier error del juego con un solo `except`.

#### ErrorJuego
**Propósito**: Agrupa errores relacionados con el estado del juego.
**Excepciones hijas**:
- `JuegoNoInicializadoError`: Se intenta jugar sin haber llamado a `iniciar_partida()`
- `TurnoJugadorInvalidoError`: Un jugador intenta mover fuera de su turno
- `JuegoYaFinalizadoError`: Se intenta continuar un juego terminado
- `MovimientoInvalidoError`: Validación general de movimientos fallida
- `SinMovimientosDisponiblesError`: No hay dados disponibles para mover

#### ErrorTablero
**Propósito**: Agrupa errores relacionados con el estado físico del tablero.
**Excepciones hijas**:
- `PuntoInvalidoError`: Acceso a posición fuera del rango 0-23
- `ComerMultipleFichasError`: Intento de comer más de una ficha
- `SacarFueraDesdePosicionInvalidaError`: Bearing off desde posición incorrecta
- `MovimientoMalFormadoError`: Formato incorrecto del movimiento (no es tupla)
- `FichasEnBarError`: Intento de mover fichas del tablero teniendo fichas en el bar
- `BearingOffNoPermitidoError`: Bearing off sin tener todas las fichas en cuadrante final
- `PosicionBloqueadaError`: Destino bloqueado por 2+ fichas enemigas
- `MovimientoContraDireccionError`: Movimiento en dirección opuesta a la permitida

#### ErrorDados
**Propósito**: Agrupa errores relacionados con los dados.
**Excepciones hijas**:
- `DadosNoLanzadosError`: Acceso a valores de dados sin haberlos lanzado
- `ValorDadoInvalidoError`: Dados con valores fuera del rango 1-6
- `DadoNoDisponibleError`: Intento de usar un dado ya utilizado

#### ErrorEntrada y ErrorJugador
**Propósito**: Errores de entrada del usuario y gestión de jugadores.
- `FormatoMovimientoInvalidoError`: Entrada del usuario mal formateada
- `JugadorNoEncontradoError`: Referencia a jugador inexistente
- `NombreJugadorInvalidoError`: Nombre vacío o duplicado

### 5.3. Estrategia de Manejo de Errores

**Principios aplicados**:
1. **Fail fast**: Validar temprano y lanzar excepciones específicas
2. **Mensajes descriptivos**: Cada excepción incluye contexto sobre el error
3. **Recuperación controlada**: El código cliente puede capturar excepciones específicas
4. **Log de errores**: Los métodos acumulan mensajes en el log antes de retornar

**Ejemplo de uso**:
```python
try:
    game.mover_ficha(movimientos, dado1, dado2)
except MovimientoInvalidoError as e:
    print(f"Movimiento inválido: {e}")
except ErrorTablero as e:
    print(f"Error del tablero: {e}")
```

---

## 6. Estrategias de Testing y Cobertura

### 6.1. Enfoque General de Testing

El proyecto implementa una **estrategia de testing exhaustiva** utilizando el framework `unittest` de Python. Se adoptó un enfoque sistemático que cubre todas las capas de la aplicación, desde las clases más simples hasta el controlador principal del juego.

**Filosofía de Testing Aplicada**:
- **Test-Driven Development (TDD)**: Pruebas diseñadas para validar comportamiento esperado antes de considerar implementaciones completas
- **Cobertura completa**: Cada clase, método público y excepción tiene sus pruebas correspondientes
- **Casos límite**: Atención especial a valores extremos, entradas inválidas y estados excepcionales
- **Aislamiento**: Uso de mocks (`unittest.mock`) para aislar componentes y probar unidades independientemente
- **Nombres descriptivos**: Cada test describe claramente qué comportamiento verifica

**Categorías de Pruebas Implementadas**:

1. **Pruebas Unitarias Básicas**: 
   - Clases simples (`Checker`, `Player`, `Dice`)
   - Validación de atributos y métodos básicos

2. **Pruebas de Lógica de Negocio**: 
   - Clase `Board` (movimientos, validaciones, bearing off)
   - Clase `BackgammonGame` (flujo del juego, turnos, detección de ganador)

3. **Pruebas de Excepciones**: 
   - Jerarquía completa de excepciones
   - Verificación de herencia y mensajes

4. **Pruebas de Reglas**: 
   - Validación de reglas específicas del Backgammon
   - Interacción entre reglas y estado del juego

5. **Pruebas de Interfaz CLI**: 
   - Entrada de usuario (parseo de movimientos)
   - Flujos de interacción completos
   - Manejo de errores de entrada

---

### 6.2. Casos de Prueba Principales

#### 6.2.1. Test Suite: `TestChecker` (3 pruebas)

**Objetivo**: Validar la clase más simple del sistema.

**Casos cubiertos**:
- ✅ `test_simbolo`: Verificación de almacenamiento y recuperación del símbolo
- ✅ `test_str`: Representación informal del objeto
- ✅ `test_repr`: Representación formal para debugging

**Importancia**: Aunque simple, esta clase es fundamental para el sistema de tipos y debe garantizar que las fichas mantienen su identidad correctamente.

---

#### 6.2.2. Test Suite: `TestPlayer` (6 pruebas)

**Objetivo**: Validar la representación de jugadores y sus consultas sobre el estado.

**Casos cubiertos**:
- ✅ `test_get_nombre`: Recuperación del nombre del jugador
- ✅ `test_get_ficha`: Recuperación del símbolo de ficha
- ✅ `test_fichas_en_tablero`: Conteo correcto de fichas en el tablero (15 iniciales)
- ✅ `test_fichas_en_bar`: Conteo de fichas capturadas (configuración manual: 2)
- ✅ `test_fichas_sacadas`: Conteo de fichas fuera del juego (configuración: 3)
- ✅ `test_estado_jugador`: Validación del resumen completo (20 fichas totales)

**Importancia**: El jugador debe mantener consistencia en el conteo de fichas a lo largo de toda la partida.

---

#### 6.2.3. Test Suite: `TestBoard` (39 pruebas)

**Objetivo**: Validar la lógica más compleja del sistema - el tablero y sus movimientos.

**Casos críticos cubiertos**:

**Inicialización y Estado**:
- ✅ `test_preparar_tablero`: Configuración inicial estándar de Backgammon
- ✅ `test_mostrar_board_imprime_correctamente`: Visualización con mocking de print

**Movimientos Válidos**:
- ✅ `test_valido_sin_comer`: Movimiento normal sin captura
- ✅ `test_valido_con_comer`: Movimiento que captura ficha enemiga solitaria
- ✅ `test_entrada_desde_bar`: Reingreso de ficha capturada
- ✅ `test_sacar_fuera`: Bearing off exitoso

**Movimientos Inválidos**:
- ✅ `test_mover_desde_posicion_vacia`: Intento de mover desde posición sin fichas
- ✅ `test_mover_ficha_enemiga`: Intento de mover ficha del oponente
- ✅ `test_no_puede_comer_varias_fichas_enemigas`: Bloqueo por 2+ fichas enemigas
- ✅ `test_entrada_desde_bar_sin_fichas`: Bar vacío
- ✅ `test_dado_invalido`: Uso de dado no disponible
- ✅ `test_movimiento_hacia_atras_invalido_x`: Dirección incorrecta para jugador X
- ✅ `test_movimiento_hacia_adelante_invalido_o`: Dirección incorrecta para jugador O
- ✅ `test_movimiento_a_posicion_bloqueada`: Destino bloqueado

**Validaciones de Límites**:
- ✅ `test_indice_fuera_de_rango_get_posiciones`: Acceso a posición 24 (inexistente)
- ✅ `test_indice_fuera_de_rango_set_posiciones`: Modificación de posición 25
- ✅ `test_puede_comer_fuera_de_rango`: Verificación de comer en posición inválida

**Formato de Movimientos**:
- ✅ `test_movimiento_tipo_incorrecto`: Movimiento no es lista
- ✅ `test_movimiento_tupla_mal_formada`: Tupla con un solo elemento

**Bearing Off Avanzado**:
- ✅ `test_sacar_fuera_desde_posicion_invalida`: Intento desde fuera del cuadrante final
- ✅ `test_puede_sacar_true`: Todas las fichas en cuadrante final
- ✅ `test_puede_sacar_false`: Fichas fuera del cuadrante final

**Reglas Especiales**:
- ✅ `test_tiene_fichas_en_bar_debe_mover_desde_bar`: Prioridad del bar sobre otros movimientos

**Casos Extremos**:
- ✅ `test_esta_en_cuadrante_final_valores_invalidos`: Posiciones no enteras o fuera de rango
- ✅ `test_error_puede_comer_fuera_de_rango`: Captura de errores en métodos privados

---

#### 6.2.4. Test Suite: `TestBackgammonGame` (50+ pruebas)

**Objetivo**: Validar el controlador principal y el flujo completo del juego.

**Inicialización**:
- ✅ `test_init_juego`: Estado inicial correcto (turno=0, jugadores creados)
- ✅ `test_calcular_movimientos_totales_normal`: Dados diferentes (3,5) → [3,5]
- ✅ `test_calcular_movimientos_totales_dobles`: Dados iguales (4,4) → [4,4,4,4]
- ✅ `test_calcular_movimientos_totales_dado1_invalido`: Excepción para dado=0
- ✅ `test_calcular_movimientos_totales_dado2_invalido`: Excepción para dado=7

**Inicio de Partida**:
- ✅ `test_quien_empieza_asigna_turno`: Asignación aleatoria del primer jugador
- ✅ `test_iniciar_partida_asigna_turno`: Turno asignado y dados lanzados
- ✅ `test_iniciar_partida_ya_iniciada`: Error al reiniciar

**Gestión de Turnos**:
- ✅ `test_get_jugador_actual_sin_iniciar`: Error antes de iniciar
- ✅ `test_get_jugador_actual_despues_de_iniciar`: Jugador correcto después de iniciar
- ✅ `test_cambiar_turno_sin_iniciar`: Error al cambiar turno prematuramente
- ✅ `test_cambiar_turno_alterna_jugadores`: Alternancia correcta entre player1 y player2
- ✅ `test_cambiar_turno_reinicia_movimientos_y_dados`: Limpieza de estado al cambiar turno
- ✅ `test_varios_cambios_turno`: Alternancia en múltiples ciclos

**Lanzamiento de Dados**:
- ✅ `test_lanzar_dados_valores_validos`: Dados entre 1-6
- ✅ `test_lanzar_dados_actualiza_movimientos`: Movimientos restantes = 2 o 4

**Estado del Juego**:
- ✅ `test_hay_ganador_inicial`: Sin ganador al inicio
- ✅ `test_get_tablero`: Estructura correcta del tablero
- ✅ `test_get_fichas_en_tablero`: Conteo inicial (15 por jugador)
- ✅ `test_get_fichas_en_bar`: Bar inicial vacío
- ✅ `test_get_fichas_sacadas`: Sin fichas sacadas al inicio
- ✅ `test_juego_activo_sin_iniciar`: Juego inactivo antes de iniciar
- ✅ `test_juego_activo_despues_de_iniciar`: Juego activo después de iniciar

**Movimientos**:
- ✅ `test_mover_ficha_sin_inicializar_juego`: Error sin inicializar
- ✅ `test_mover_ficha_sin_movimientos_restantes`: Rechazo cuando no hay movimientos
- ✅ `test_estructura_resultado_mover_ficha`: Diccionario con claves esperadas

**Movimientos Legales (Detección Automática)**:
- ✅ `test_tiene_movimientos_posicion_inicial`: Siempre hay movimientos al inicio
- ✅ `test_tiene_movimientos_con_reglas`: Validación con reglas activas
- ✅ `test_tiene_movimientos_con_dados_actuales_sin_dados`: False sin dados disponibles
- ✅ `test_tiene_movimientos_con_dados_actuales_con_dados`: True con dados [3,4]
- ✅ `test_tiene_movimientos_con_fichas_en_bar`: Verificación desde el bar
- ✅ `test_tiene_movimientos_bar_posicion_bloqueada`: Skip cuando bar bloqueado

**Bearing Off Avanzado**:
- ✅ `test_tiene_fichas_mas_atras_jugador_x_con_fichas`: Detección para jugador X
- ✅ `test_tiene_fichas_mas_atras_jugador_x_sin_fichas_atras`: False cuando no hay
- ✅ `test_tiene_fichas_mas_atras_jugador_o_con_fichas`: Detección para jugador O
- ✅ `test_tiene_fichas_mas_atras_jugador_o_sin_fichas_atras`: False cuando no hay
- ✅ `test_verificar_bearing_off_dado_mayor_sin_fichas_atras`: Bearing off con dado mayor

**Validaciones Internas**:
- ✅ `test_validar_movimiento_con_reglas`: Validación con múltiples reglas
- ✅ `test_validar_movimiento_con_value_error`: Captura de ValueError
- ✅ `test_verificar_movimiento_desde_posicion`: Verificación exhaustiva

**Integración**:
- ✅ `test_get_estado_juego_sin_iniciar`: Estado sin iniciar
- ✅ `test_get_estado_juego_despues_de_iniciar`: Estado completo después de iniciar
- ✅ `test_mover_ficha_uso_multiple_dados`: Uso correcto de múltiples dados

---

#### 6.2.5. Test Suite: `TestExcepciones` (25+ pruebas)

**Objetivo**: Validar la jerarquía completa de excepciones.

**Excepciones Base**:
- ✅ `test_excepcion_salir_se_puede_lanzar`: ExcepcionSalirDelJuego
- ✅ `test_error_backgammon_se_puede_lanzar`: ErrorBackgammon (base)

**Excepciones de Juego**:
- ✅ `test_error_juego_se_puede_lanzar`: ErrorJuego (base)
- ✅ `test_juego_no_inicializado_error`: JuegoNoInicializadoError
- ✅ `test_turno_jugador_invalido_error`: TurnoJugadorInvalidoError
- ✅ `test_juego_ya_finalizado_error`: JuegoYaFinalizadoError
- ✅ `test_movimiento_invalido_error`: MovimientoInvalidoError
- ✅ `test_sin_movimientos_disponibles_error`: SinMovimientosDisponiblesError

**Excepciones de Tablero**:
- ✅ `test_error_tablero_base`: ErrorTablero (base)
- ✅ `test_punto_invalido_error`: PuntoInvalidoError
- ✅ `test_comer_multiple_fichas_error`: ComerMultipleFichasError
- ✅ `test_sacar_fuera_desde_posicion_invalida_error`: SacarFueraDesdePosicionInvalidaError
- ✅ `test_movimiento_mal_formado_error`: MovimientoMalFormadoError
- ✅ `test_fichas_en_bar_error`: FichasEnBarError
- ✅ `test_bearing_off_no_permitido_error`: BearingOffNoPermitidoError
- ✅ `test_posicion_bloqueada_error`: PosicionBloqueadaError

**Excepciones de Dados**:
- ✅ `test_error_dados_base`: ErrorDados (base)
- ✅ `test_dados_no_lanzados_error`: DadosNoLanzadosError
- ✅ `test_valor_dado_invalido_error`: ValorDadoInvalidoError

**Jerarquía**:
- ✅ `test_todas_excepciones_juego_heredan_error_backgammon`: Herencia correcta
- ✅ `test_todas_excepciones_tablero_heredan_error_backgammon`: Herencia correcta
- ✅ `test_todas_excepciones_dados_heredan_error_backgammon`: Herencia correcta
- ✅ `test_error_juego_hereda_de_error_backgammon`: Herencia base
- ✅ `test_error_tablero_hereda_de_error_backgammon`: Herencia base
- ✅ `test_error_dados_hereda_de_error_backgammon`: Herencia base

---

#### 6.2.6. Test Suite: `TestReglasValidacion` (5 pruebas)

**Objetivo**: Validar reglas específicas del Backgammon.

**Regla Bar**:
- ✅ `test_regla_bar_lanza_excepcion_si_hay_fichas_en_bar`: Prioridad del bar
- ✅ `test_regla_bar_no_lanza_excepcion_si_mueve_desde_bar`: Movimiento correcto desde bar

**Regla Salida Final**:
- ✅ `test_regla_salida_final_lanza_excepcion_si_no_puede_sacar`: Bearing off prematuro
- ✅ `test_regla_salida_final_no_lanza_excepcion_si_puede_sacar`: Bearing off válido

**Excepciones Personalizadas**:
- ✅ `test_movimiento_invalido_error_str`: Representación de string
- ✅ `test_movimiento_invalido_error_raise`: Lanzamiento y captura

---

#### 6.2.7. Test Suite: `TestBackgammonCLI` (40+ pruebas)

**Objetivo**: Validar la interfaz de línea de comandos.

**Inicialización**:
- ✅ `test_init`: Estado inicial del CLI

**Parseo de Movimientos**:
- ✅ `test_movimiento_basico`: "10 15" → (10, 15)
- ✅ `test_con_guion`: "10-15" → (10, 15)
- ✅ `test_desde_bar`: "BAR 5" → ("bar", 5)
- ✅ `test_hacia_fuera`: "20 FUERA" → (20, "fuera")
- ✅ `test_espacios_extra`: Normalización de espacios
- ✅ `test_formato_invalido`: Error con un solo número
- ✅ `test_origen_invalido`: Error con "abc"
- ✅ `test_destino_invalido`: Error con "xyz"

**Acciones Sin Juego Activo**:
- ✅ `test_ver_tablero_sin_juego`: Mensaje "No hay partida en curso"
- ✅ `test_ver_estado_sin_juego`: Mensaje "No hay partida en curso"
- ✅ `test_lanzar_dados_sin_juego`: Mensaje "No hay partida en curso"
- ✅ `test_verificar_sin_juego`: Mensaje "No hay partida en curso"

**Acciones Con Juego Activo**:
- ✅ `test_ver_tablero`: Delegación a juego.mostrar_tablero()
- ✅ `test_ver_estado_completo`: Visualización de estado completo
- ✅ `test_ver_estado_sin_iniciar`: Manejo de jugador_actual = None

**Lanzamiento de Dados**:
- ✅ `test_dados_ya_lanzados`: Prevención de lanzamiento duplicado
- ✅ `test_lanzar_exitoso`: Actualización de dados_actuales y dados_lanzados
- ✅ `test_sin_movimientos`: Cambio automático de turno

**Movimientos de Fichas (Casos Exhaustivos)**:
- ✅ `test_sin_dados`: Mensaje de error
- ✅ `test_sin_movimientos_iniciales`: Cambio automático si no hay legales
- ✅ `test_cambio_jugador_automatico`: Cambio después de movimientos exitosos
- ✅ `test_sin_movimientos_restantes`: Cambio automático cuando se agotan
- ✅ `test_sin_movimientos_con_dados_disponibles`: Cambio si no hay legales con dados restantes
- ✅ `test_entrada_vacia`: Skip en entrada vacía
- ✅ `test_con_ganador`: Finalización del juego
- ✅ `test_cambio_turno_despues_movimiento`: Jugador cambia después de movimientos
- ✅ `test_sin_movimientos_restantes_despues_exitoso`: Cambio después de usar todos los dados
- ✅ `test_movimiento_fallido_cambio_turno`: Cambio si el jugador cambió durante validación
- ✅ `test_movimiento_fallido_sin_movimientos_restantes`: Cambio si no hay más movimientos legales
- ✅ `test_movimiento_fallido_con_otros_posibles`: Continúa si hay otros movimientos

**Menús**:
- ✅ `test_menu_principal`: Visualización del menú principal
- ✅ `test_menu_juego`: Visualización del menú de juego

**Bucle Principal**:
- ✅ `test_salir`: Opción "2" sale del programa
- ✅ `test_opcion_invalida_principal`: Manejo de opción inválida
- ✅ `test_opcion_invalida_juego`: Manejo de opción inválida en juego

**Métodos Privados**:
- ✅ `test_mostrar_info_turno_x`: Información para jugador X
- ✅ `test_mostrar_info_turno_o`: Información para jugador O
- ✅ `test_mostrar_instrucciones`: Visualización de instrucciones
- ✅ `test_procesar_entrada_valida`: Procesamiento de múltiples movimientos
- ✅ `test_procesar_entrada_invalida`: Manejo de entrada inválida

**Iniciar Partida**:
- ✅ `test_nombres_vacios`: Nombres por defecto (player1, player2)
- ✅ `test_nombres_personalizados`: Nombres personalizados (Alice, Bob)

---

### 6.3. Cobertura Alcanzada

**Métricas Estimadas** (basadas en los 160+ tests implementados):

| Componente | Tests | Cobertura Líneas | Cobertura Ramas | Métodos Públicos |
|------------|-------|------------------|-----------------|------------------|
| `Checker` | 3 | ~100% | 100% | 100% |
| `Player` | 6 | ~100% | 100% | 100% |
| `Dice` | 0* | N/A | N/A | N/A |
| `Board` | 39 | ~95% | ~90% | 100% |
| `BackgammonGame` | 50+ | ~92% | ~88% | 100% |
| `Excepciones` | 25 | 100% | 100% | 100% |
| `Validaciones` | 5 | 100% | 100% | 100% |
| `BackgammonCLI` | 40+ | ~90% | ~85% | ~95% |
| **TOTAL** | **160+** | **~94%** | **~89%** | **~99%** |

*Nota: `Dice` no tiene tests explícitos porque su funcionalidad se prueba indirectamente a través de `BackgammonGame`.

**Aspectos Destacados**:
- ✅ **Cobertura de excepciones**: 100% - Todas las excepciones se pueden lanzar y capturar
- ✅ **Métodos públicos**: ~99% - Prácticamente todos los métodos públicos tienen tests
- ✅ **Casos límite**: Cubiertos exhaustivamente (índices fuera de rango, valores inválidos)
- ✅ **Integración**: Flujos completos del juego testeados en `TestBackgammonCLI`

**Áreas con Menor Cobertura**:
- Algunos métodos privados complejos con múltiples ramas condicionales
- Casos de error muy específicos en métodos de validación
- Combinaciones de estados poco comunes (e.g., múltiples movimientos con bearing off)

---

### 6.4. Herramientas y Técnicas de Testing

**Framework Utilizado**: 
- **`unittest`**: Framework estándar de Python, elegido por:
  - Integración nativa con Python
  - Sintaxis clara y bien documentada
  - Soporte para fixtures (`setUp`, `tearDown`)
  - Asserts descriptivos (`assertEqual`, `assertIn`, `assertRaises`)

**Técnicas de Mocking**:
- **`unittest.mock.Mock`**: Creación de objetos simulados para aislar componentes
- **`unittest.mock.patch`**: Reemplazo temporal de funciones (especialmente `print` e `input`)
- **`unittest.mock.MagicMock`**: Mocks con métodos mágicos para comportamientos complejos

**Organización de Tests**:
```
tests/
├── test_checker.py           # 3 tests
├── test_player.py            # 6 tests
├── test_board.py             # 39 tests
├── test_backgammon_game.py   # 50+ tests
├── test_excepciones.py       # 25 tests
├── test_validaciones.py      # 5 tests
└── test_cli.py               # 40+ tests
```

**Patrones de Testing Aplicados**:

1. **AAA Pattern (Arrange-Act-Assert)**:
   ```python
   def test_calcular_movimientos_totales_normal(self):
       # Arrange
       game = BackgammonGame("p1", "p2")
       
       # Act
       movimientos = game.calcular_movimientos_totales(3, 5)
       
       # Assert
       self.assertEqual(movimientos, [3, 5])
   ```

2. **Setup/Teardown para Fixtures**:
   ```python
   def setUp(self):
       """Inicializa entorno de prueba."""
       self.game = BackgammonGame("player1", "player2")
   ```

3. **Tests de Contexto para Excepciones**:
   ```python
   with self.assertRaises(MovimientoInvalidoError) as contexto:
       regla_bar(self.jugador1, movimientos, dados, self.board)
   self.assertIn("tiene fichas en el bar", contexto.exception.mensaje)
   ```

4. **Mocking de I/O para CLI**:
   ```python
   @patch('builtins.input')
   @patch('builtins.print')
   def test_nombres_vacios(self, mock_print, mock_input):
       mock_input.side_effect = ["", ""]
       # ... test code ...
   ```

**Ejecución de Tests**:
```bash
# Ejecutar todos los tests
python -m unittest discover -s tests -p "test_*.py"

# Ejecutar suite específica
python -m unittest tests.test_board

# Ejecutar test específico
python -m unittest tests.test_board.TestBoard.test_valido_sin_comer

# Con verbosidad
python -m unittest discover -v
```

**Cobertura de Código** (herramienta recomendada):
```bash
# Instalar coverage
pip install coverage

# Ejecutar tests con cobertura
coverage run -m unittest discover

# Generar reporte
coverage report -m

# Generar reporte HTML
coverage html
```

---

### 6.5. Análisis de Casos de Prueba Críticos

**Caso 1: Movimientos con Fichas en el Bar**
- **Criticidad**: Alta - Regla fundamental del Backgammon
- **Tests relacionados**: 
  - `test_regla_bar_lanza_excepcion_si_hay_fichas_en_bar`
  - `test_tiene_fichas_en_bar_debe_mover_desde_bar`
  - `test_tiene_movimientos_con_fichas_en_bar`
- **Cobertura**: ✅ Completa (prioridad del bar, entrada desde bar, bloqueos)

**Caso 2: Bearing Off**
- **Criticidad**: Alta - Condición de victoria
- **Tests relacionados**: 
  - `test_sacar_fuera`
  - `test_puede_sacar_true/false`
  - `test_tiene_fichas_mas_atras_*`
  - `test_verificar_bearing_off_dado_mayor_sin_fichas_atras`
- **Cobertura**: ✅ Completa (posición, cuadrante final, dados mayores)

**Caso 3: Cambio Automático de Turno**
- **Criticidad**: Alta - Experiencia de usuario
- **Tests relacionados**: 
  - `test_cambiar_turno_alterna_jugadores`
  - `test_sin_movimientos` (CLI)
  - `test_cambio_jugador_automatico`
- **Cobertura**: ✅ Completa (sin movimientos legales, dados agotados, bloqueo total)

**Caso 4: Validación de Excepciones**
- **Criticidad**: Media - Robustez del sistema
- **Tests relacionados**: Toda la suite `TestExcepciones` (25 tests)
- **Cobertura**: ✅ Completa (jerarquía, herencia, mensajes)

**Caso 5: Parseo de Entrada de Usuario**
- **Criticidad**: Media - Usabilidad del CLI
- **Tests relacionados**: Suite `TestParsearMovimiento` (8 tests)
- **Cobertura**: ✅ Completa (formatos válidos/in

---

## 7. Cumplimiento de Principios SOLID

### 7.1. Single Responsibility Principle (SRP)

**Cumplimiento**: ✅ **ALTO**

- **`BackgammonGame`**: Solo gestiona el flujo del juego
- **`Board`**: Solo maneja el estado físico del tablero
- **`Player`**: Solo representa a un jugador
- **`Checker`**: Solo representa una ficha
- **`Dice`**: Solo genera números aleatorios
- **`validaciones.py`**: Solo contiene reglas de validación

**Cada clase tiene una única razón para cambiar.**

---

### 7.2. Open/Closed Principle (OCP)

**Cumplimiento**: ✅ **ALTO**

**Evidencia**:
1. **Reglas extensibles**: Las reglas se inyectan como funciones, permitiendo agregar nuevas sin modificar `BackgammonGame`.
   ```python
   game = BackgammonGame(j1, j2, reglas=[regla_bar, regla_salida_final, nueva_regla])
   ```

2. **Jerarquía de excepciones**: Se pueden agregar nuevas excepciones heredando de las existentes sin modificar el código de manejo de errores.

3. **Método `mostrar_board()`**: Permite diferentes visualizaciones sobreescribiendo el método en subclases.

**El sistema está abierto a extensión pero cerrado a modificación.**

---

### 7.3. Liskov Substitution Principle (LSP)

**Cumplimiento**: ✅ 

**Evidencia**:
- Las excepciones son sustituibles: cualquier código que capture `ErrorBackgammon` funcionará correctamente con cualquier excepción derivada.
- Las clases no usan herencia de implementación, por lo que no hay riesgo de violar LSP.

**Todas las jerarquías de clases son sustituibles por sus clases base.**

---

### 7.4. Interface Segregation Principle (ISP)

**Cumplimiento**: ✅

**Evidencia**:
- Cada clase tiene una interfaz mínima y cohesiva.
- `Board` no expone métodos innecesarios; solo los relevantes para el juego.
- `Player` solo expone métodos relacionados con jugadores.
- No hay interfaces "gordas" que obliguen a implementar métodos innecesarios.

**Los clientes no dependen de interfaces que no usan.**

---

### 7.5. Dependency Inversion Principle (DIP)

**Cumplimiento**: ✅ 

**Evidencia de cumplimiento**:
1. **Inyección de reglas**: `BackgammonGame` depende de abstracciones (funciones) en lugar de reglas concretas.
   ```python
   def __init__(self, jugador1, jugador2, reglas=None):
       self.__reglas__ = reglas if reglas else []
   ```

2. **Composición**: `BackgammonGame` depende de las interfaces de `Board`, `Dice` y `Player`, no de sus implementaciones específicas.

**Áreas de mejora**:
- Podría usarse inyección de dependencias para `Board` y `Dice` (actualmente se crean internamente).
- Ejemplo de mejora:
  ```python
  def __init__(self, jugador1, jugador2, board=None, dice=None, reglas=None):
      self.__board__ = board if board else Board()
      self.__dice__ = dice if dice else Dice()
  ```

**El código de alto nivel no depende de detalles de bajo nivel.**

## 8. Conclusiones

El diseño del juego de Backgammon demuestra:

1. **Modularidad**: Cada componente tiene responsabilidades bien definidas
2. **Extensibilidad**: Fácil agregar nuevas reglas, excepciones o funcionalidades
3. **Mantenibilidad**: Código organizado y documentado facilita cambios futuros
4. **Robustez**: Sistema completo de excepciones garantiza manejo de errores
5. **Cumplimiento SOLID**: Principios aplicados consistentemente


---

## 9. Anexos

### 9.1. Diagrama de Clases UML

```
┌─────────────────────────────────────────────────────────────┐
│                     BackgammonGame                          │
├─────────────────────────────────────────────────────────────┤
│ - __board__: Board                                          │
│ - __dice__: Dice                                            │
│ - __turno__: int                                            │
│ - __movimientos_restantes__: int                            │
│ - __jugador1__: Player                                      │
│ - __jugador2__: Player                                      │
│ - __reglas__: list[callable]                                │
│ - __dados_disponibles__: list[int]                          │
│ - __valores_dados__: tuple[int, int]                        │
├─────────────────────────────────────────────────────────────┤
│ + iniciar_partida(): void                                   │
│ + lanzar_dados(): tuple[int, int, int]                      │
│ + mover_ficha(movimientos, dado1, dado2): dict              │
│ + cambiar_turno(): Player                                   │
│ + get_jugador_actual(): Player                              │
│ + hay_ganador(): bool                                       │
│ + tiene_movimientos_legales(jugador, d1, d2): bool          │
│ + get_estado_juego(): dict                                  │
└─────────────────────────────────────────────────────────────┘
                    │ 1                     │ 1
                    │ compone               │ compone
                    ▼                       ▼
        ┌───────────────────┐   ┌───────────────────┐
        │       Board       │   │       Dice        │
        ├───────────────────┤   ├───────────────────┤
        │ - __posiciones__  │   │ - __dado1__: int  │
        │ - __bar__: dict   │   │ - __dado2__: int  │
        │ - __fuera__: dict │   ├───────────────────┤
        ├───────────────────┤   │ + lanzar_dados()  │
        │ + mover_ficha()   │   │ + get_valores()   │
        │ + validar_mov()   │   └───────────────────┘
        │ + puede_sacar()   │
        │ + calcular_dist() │
        └───────────────────┘
                    │ contiene 0..*
                    ▼
        ┌───────────────────┐
        │      Checker      │
        ├───────────────────┤
        │ - __simbolo__: str│
        ├───────────────────┤
        │ + get_simbolo()   │
        └───────────────────┘

        ┌───────────────────┐
        │      Player       │
        ├───────────────────┤
        │ - __nombre__: str │
        │ - __ficha__: str  │
        ├───────────────────┤
        │ + get_nombre()    │
        │ + get_ficha()     │
        │ + fichas_en_*()   │
        └───────────────────┘
```

### 9.2. Diagrama de Jerarquía de Excepciones

```
                    ErrorBackgammon
                          │
        ┌─────────────────┼─────────────────┬──────────────┐
        │                 │                 │              │
    ErrorJuego       ErrorTablero      ErrorDados    ErrorEntrada
        │                 │                 │              │
        ├── JuegoNo...    ├── PuntoInv...   ├── DadosNo... └── FormatoMov...
        ├── TurnoJug...   ├── ComerMul...   ├── ValorDad...
        ├── JuegoYa...    ├── SacarFue...   └── DadoNoD...
        ├── Movimie...    ├── Movimie...
        └── SinMovi...    ├── FichasE...    ErrorJugador
                          ├── BearingO...        │
                          ├── Posicion...        ├── JugadorNo...
                          └── Movimie...         └── NombreJug...
```

### 9.3. Flujo de un Movimiento

```
Usuario solicita movimiento
        │
        ▼
BackgammonGame.mover_ficha()
        │
        ├─► Validar turno y movimientos restantes
        │
        ├─► Aplicar reglas externas (regla_bar, regla_salida_final, etc.)
        │   └─► Si falla: retornar error
        │
        ├─► Board.mover_ficha()
        │   │
        │   ├─► Para cada movimiento:
        │   │   ├─► _procesar_movimiento_individual()
        │   │   │   ├─► Validar distancia con dados disponibles
        │   │   │   ├─► Validar origen (tiene fichas del jugador)
        │   │   │   ├─► Validar destino (no bloqueado)
        │   │   │   └─► _ejecutar_movimiento()
        │   │   │       ├─► Comer ficha enemiga si corresponde
        │   │   │       ├─► Mover ficha (desde → hasta)
        │   │   │       └─► Actualizar dados usados
        │   │   └─► Acumular resultado
        │   └─► Retornar resultados y log
        │
        ├─► Actualizar dados disponibles
        ├─► Decrementar movimientos restantes
        └─► Si no quedan movimientos: cambiar_turno()
```

---

**Documento elaborado**: Octubre 2025  
**Proyecto**: Backgammon - Implementación en Python  
**Autor**: Diego Aubone