# Registro de Prompt - Coverage CLI

## Modelo / Herramienta usada
Claude
```
como hago para que el coverage solo incluya el testo de logica del cli no mensajes
```

## Respuesta/resultado completo devuelto por la IA

La IA proporcionó dos estrategias principales:

### Opción 1 : Excluir el CLI del reporte
- Configuración en `.coveragerc` para omitir `main/cli.py`
- Configuración alternativa en `pyproject.toml`
- Comando: `pytest --cov=core --cov-report=term-missing`

### Opción 2: Mover lógica del CLI a core
- Extraer validaciones y lógica de negocio a módulos en `core/`
- Dejar solo UI (print, input) en el CLI

### Opción 3: Uso de `# pragma: no cover`
- Marcar funciones individuales con el comentario
- Marcar bloques completos
- Combinación con configuración

### Salida final aplicada
Uso de `# pragma: no cover` en cada método de cli deje sin marcar el unico metodo que utilizaba pura logica

### Métodos marcados con `# pragma: no cover`:
- `__init__()`
- `mostrar_menu_principal()`
- `mostrar_menu_juego()`
- `iniciar_nueva_partida()`
- `ver_tablero()`
- `ver_estado()`
- `lanzar_dados()`
- `mover_fichas()`
- `pasar_turno()`
- `ejecutar()`
- `main()`
- Bloque `if __name__ == "__main__":`

### Método NO marcado (testeable):
- `parsear_movimiento()` - Contiene lógica pura