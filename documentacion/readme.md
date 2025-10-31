# Backgammon - Guía de Inicio Rápido
Alumno: Diego Aubone
Carrera: Ingeneria Informatica
Legajo: 64210
Fecha: Octubre 2025

## Instalación

### 1. Crear entorno virtual

# Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# Windows:
python -m venv 
venv\Scripts\activate

### 2. Instalar dependencias

pip install -r requirements.txt


## Modo Testing

### Ejecutar todos los tests

python -m unittest discover -s core/test 

### Tests específicos

# Solo tests de la lógica del juego:
python -m unittest core.test.test_backgammon_game

# Solo tests del CLI:
python -m unittest core.test.test_cli 

### Análisis de código (pylint)

pylint core 

## Modo Juego

### Opción 1: Interfaz de Línea de Comandos (CLI)


python -m cli.main

### Opción 2: Interfaz Gráfica (Pygame)


python -m ui.Pygame_UI

## Estructura del Proyecto

backgammon/
├── core/
│   └──clases/              # Lógica del juego
├── test/                # Tests unitarios
├── cli/
│   └── main.py              # Interfaz CLI
├── pygame_ui/
│   └── main.py              # Interfaz Pygame
└── requirements.txt
