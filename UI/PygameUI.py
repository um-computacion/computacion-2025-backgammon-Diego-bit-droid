"""
Backgammon con Pygame - Versión Simple
Solo interfaz visual, toda la lógica está en BackgammonGame
"""
import pygame
from core.backgammon_game import BackgammonGame

pygame.init()

# Constantes
WIDTH = 1400
HEIGHT = 800
FPS = 60

# Colores
WOOD_BROWN = (139, 90, 43)
DARK_BROWN = (101, 67, 33)
LIGHT_BEIGE = (245, 222, 179)
DARK_BEIGE = (210, 180, 140)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
HIGHLIGHT = (255, 255, 100)
BUTTON_COLOR = (100, 150, 200)
BUTTON_HOVER = (130, 180, 230)
GOLD = (255, 215, 0)
GREEN = (50, 200, 50)
RED = (200, 50, 50)

# Dimensiones
BOARD_WIDTH = 840
BOARD_HEIGHT = 600
POINT_WIDTH = 60
CHECKER_RADIUS = 20
BAR_WIDTH = 60
POINT_HEIGHT = 220


class Button:
    """Botón clickeable"""
    def __init__(self, x, y, w, h, text, color=BUTTON_COLOR):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = BUTTON_HOVER
        self.hovered = False
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surf, font):
        col = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surf, col, self.rect, border_radius=10)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=10)
        text_surf = font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surf.blit(text_surf, text_rect)
    
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.hovered
        return False


class BackgammonPygame:
    """Juego principal - SOLO INTERFAZ"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Backgammon")
        self.clock = pygame.time.Clock()
        
        self.font_large = pygame.font.Font(None, 56)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 18)
        
        self.game = None
        self.state = "MENU"
        self.selected_point = None
        self.dados_actuales = None
        self.dados_lanzados = False
        
        self.message = ""
        self.message_timer = 0
        self.message_color = GOLD
        self.player1_name = ""
        self.player2_name = ""
        self.current_input = 1
        self.input_text = ""
        
        self.buttons = self.create_buttons()
        self.dt = 0
        
        self.board_x = (WIDTH - BOARD_WIDTH - 300) // 2
        self.board_y = (HEIGHT - BOARD_HEIGHT) // 2
    
    def create_buttons(self):
        return {
            'new_game': Button(WIDTH//2 - 100, 350, 200, 50, "Nueva Partida"),
            'quit': Button(WIDTH//2 - 100, 430, 200, 50, "Salir"),
            'roll_dice': Button(WIDTH - 280, 250, 220, 50, "Lanzar Dados"),
            'menu': Button(WIDTH - 280, 320, 220, 50, "Menu")
        }
    
    def show_message(self, text, duration=3000, color=GOLD):
        self.message = text
        self.message_timer = duration
        self.message_color = color
    
    def update_message_timer(self):
        if self.message_timer > 0:
            self.message_timer -= self.dt
            if self.message_timer < 0:
                self.message_timer = 0
                self.message = ""
    
    def get_point_position(self, point_num):
        """Calcula posición de un punto en el tablero"""
        if point_num < 6:
            x = self.board_x + BOARD_WIDTH - (point_num + 1) * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y + BOARD_HEIGHT
            direction = -1
        elif point_num < 12:
            offset_from_left = 11 - point_num
            x = self.board_x + offset_from_left * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y + BOARD_HEIGHT
            direction = -1
        elif point_num < 18:
            offset = point_num - 12
            x = self.board_x + offset * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y
            direction = 1
        else:
            offset = point_num - 18
            x = self.board_x + BOARD_WIDTH // 2 + BAR_WIDTH // 2 + offset * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y
            direction = 1
        
        return x, y, direction
    
    def get_clicked_point(self, pos):
        """Detecta qué punto fue clickeado"""
        mx, my = pos
        
        bear_off_x = self.board_x + BOARD_WIDTH + 10
        bear_off_width = 100
        
        if (bear_off_x <= mx <= bear_off_x + bear_off_width and
            self.board_y + BOARD_HEIGHT // 2 <= my <= self.board_y + BOARD_HEIGHT):
            return "bear_off_O"
        
        if (bear_off_x <= mx <= bear_off_x + bear_off_width and
            self.board_y <= my <= self.board_y + BOARD_HEIGHT // 2):
            return "bear_off_X"
        
        bar_x = self.board_x + (BOARD_WIDTH - BAR_WIDTH) // 2
        if bar_x <= mx <= bar_x + BAR_WIDTH:
            if self.board_y <= my <= self.board_y + BOARD_HEIGHT:
                return "bar"
        
        for point_num in range(24):
            x, y, direction = self.get_point_position(point_num)
            
            if direction == 1:
                if (x - POINT_WIDTH//2 <= mx <= x + POINT_WIDTH//2 and
                    y <= my <= y + POINT_HEIGHT):
                    return point_num
            else:
                if (x - POINT_WIDTH//2 <= mx <= x + POINT_WIDTH//2 and
                    y - POINT_HEIGHT <= my <= y):
                    return point_num
        
        return None
    
    # ==================== LÓGICA (DELEGADA A BACKGAMMONGAME) ====================
    
    def start_game(self):
        """Inicia partida - USA BackgammonGame.iniciar_partida()"""
        name1 = self.player1_name.strip() or "Jugador 1"
        name2 = self.player2_name.strip() or "Jugador 2"
        
        self.game = BackgammonGame(name1, name2)
        self.game.quien_empieza()
        d1, d2, _ = self.game.lanzar_dados()
        
        self.state = "GAME"
        self.dados_lanzados = True
        self.dados_actuales = (d1, d2)
        self.selected_point = None
        
        jugador = self.game.get_jugador_actual()
        self.show_message(f"{jugador.get_nombre()} comienza! Dados: {d1}, {d2}", 3000, GREEN)
    
    def roll_dice(self):
        """Lanza dados - USA BackgammonGame.lanzar_dados()"""
        if not self.game or self.dados_lanzados:
            if self.dados_lanzados:
                self.show_message("Ya lanzaste los dados", 2000, RED)
            return
        
        d1, d2, _ = self.game.lanzar_dados()
        self.dados_actuales = (d1, d2)
        self.dados_lanzados = True
        
        dados_disponibles = self.game.get_dados_disponibles()
        self.show_message(f"Dados: {d1}, {d2} | Disponibles: {dados_disponibles}", 3000, GREEN)
    
    def handle_board_click(self, pos):
        """Maneja clicks en el tablero"""
        if not self.game or not self.dados_lanzados:
            if not self.dados_lanzados:
                self.show_message("Primero debes lanzar los dados", 2000, RED)
            return
        
        clicked = self.get_clicked_point(pos)
        if clicked is None:
            return
        
        if self.selected_point is None:
            self.selected_point = clicked
            self.show_message(f"Origen: {clicked}", 2000, GOLD)
        else:
            self.try_move(self.selected_point, clicked)
            self.selected_point = None
    
    def try_move(self, origin, dest):
        """Intenta mover - USA BackgammonGame.mover_ficha()"""
        # Convertir bear_off a "fuera"
        if dest == "bear_off_X" or dest == "bear_off_O":
            dest = "fuera"
        
        if isinstance(origin, str) and origin.startswith("bear_off"):
            self.show_message("No puedes mover desde Bear Off", 2000, RED)
            return
        
        jugador_inicial = self.game.get_jugador_actual()
        
        # TODA LA LÓGICA está en BackgammonGame.mover_ficha()
        resultado = self.game.mover_ficha(
            [(origin, dest)],
            self.dados_actuales[0],
            self.dados_actuales[1]
        )
        
        # Mostrar resultado
        if any(resultado['resultados']):
            msg = resultado['log'][0] if resultado['log'] else "¡Movimiento exitoso!"
            self.show_message(msg, 2000, GREEN)
        else:
            msg = resultado['log'][0] if resultado['log'] else "Movimiento inválido"
            self.show_message(msg, 3000, RED)
        
        # Verificar ganador - USA BackgammonGame.hay_ganador()
        if self.game.hay_ganador():
            self.state = "WINNER"
            return
        
        # Verificar si cambió de turno
        jugador_actual = self.game.get_jugador_actual()
        if jugador_actual.get_nombre() != jugador_inicial.get_nombre():
            self.dados_lanzados = False
            self.dados_actuales = None
            self.show_message(f"Turno de {jugador_actual.get_nombre()}", 3000, GREEN)
        elif self.game.get_movimientos_restantes() == 0:
            self.dados_lanzados = False
            self.dados_actuales = None
    
    # ==================== EVENTOS ====================
    
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.state == "MENU":
            self.buttons['new_game'].update(mouse_pos)
            self.buttons['quit'].update(mouse_pos)
        elif self.state == "GAME":
            self.buttons['roll_dice'].update(mouse_pos)
            self.buttons['menu'].update(mouse_pos)
        elif self.state == "WINNER":
            self.buttons['new_game'].update(mouse_pos)
            self.buttons['quit'].update(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if self.state == "MENU":
                if self.buttons['new_game'].is_clicked(event):
                    self.state = "NAME_INPUT"
                    self.current_input = 1
                    self.input_text = ""
                elif self.buttons['quit'].is_clicked(event):
                    return False
            
            elif self.state == "NAME_INPUT":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.current_input == 1:
                            self.player1_name = self.input_text
                            self.current_input = 2
                            self.input_text = ""
                        else:
                            self.player2_name = self.input_text
                            self.start_game()
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        self.state = "MENU"
                    else:
                        if len(self.input_text) < 20 and event.unicode.isprintable():
                            self.input_text += event.unicode
            
            elif self.state == "GAME":
                if self.buttons['roll_dice'].is_clicked(event):
                    self.roll_dice()
                elif self.buttons['menu'].is_clicked(event):
                    self.state = "MENU"
                    self.game = None
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_board_click(event.pos)
            
            elif self.state == "WINNER":
                if self.buttons['new_game'].is_clicked(event):
                    self.state = "NAME_INPUT"
                    self.current_input = 1
                    self.input_text = ""
                    self.player1_name = ""
                    self.player2_name = ""
                elif self.buttons['quit'].is_clicked(event):
                    return False
        
        return True
    
    # ==================== RENDERIZADO ====================
    
    def draw_text_centered(self, text, x, y, font, color=WHITE):
        surf = font.render(str(text), True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)
    
    def draw_text(self, text, x, y, font, color=WHITE):
        surf = font.render(str(text), True, color)
        self.screen.blit(surf, (x, y))
    
    def draw_menu(self):
        self.screen.fill(DARK_BROWN)
        self.draw_text_centered("BACKGAMMON", WIDTH//2, 200, self.font_large, GOLD)
        self.buttons['new_game'].draw(self.screen, self.font_medium)
        self.buttons['quit'].draw(self.screen, self.font_medium)
    
    def draw_name_input(self):
        self.screen.fill(DARK_BROWN)
        self.draw_text_centered("BACKGAMMON", WIDTH//2, 150, self.font_large, GOLD)
        
        prompt = f"Jugador {self.current_input} ({'X' if self.current_input == 1 else 'O'}):"
        self.draw_text_centered(prompt, WIDTH//2, 300, self.font_medium, WHITE)
        
        input_rect = pygame.Rect(WIDTH//2 - 250, 370, 500, 60)
        pygame.draw.rect(self.screen, WHITE, input_rect, border_radius=5)
        pygame.draw.rect(self.screen, BLACK, input_rect, 3, border_radius=5)
        
        if self.input_text:
            self.draw_text(self.input_text, input_rect.x + 15, input_rect.y + 20, self.font_medium, BLACK)
        
        self.draw_text_centered("ENTER: continuar | ESC: volver", WIDTH//2, 500, self.font_small, LIGHT_BEIGE)
    
    def draw_point(self, point_num):
        """Dibuja un triángulo del tablero"""
        x, y, direction = self.get_point_position(point_num)
        
        color = LIGHT_BEIGE if point_num % 2 == 0 else DARK_BEIGE
        
        if self.selected_point == point_num:
            color = HIGHLIGHT
        
        if direction == 1:
            points = [
                (x - POINT_WIDTH // 2, y),
                (x + POINT_WIDTH // 2, y),
                (x, y + POINT_HEIGHT)
            ]
            num_y = y - 15
        else:
            points = [
                (x - POINT_WIDTH // 2, y),
                (x + POINT_WIDTH // 2, y),
                (x, y - POINT_HEIGHT)
            ]
            num_y = y + 25
        
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, BLACK, points, 2)
        self.draw_text_centered(str(point_num), x, num_y, self.font_tiny, WHITE)
    
    def draw_checker(self, x, y, symbol):
        """Dibuja una ficha"""
        if symbol == 'X':
            pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), CHECKER_RADIUS)
            pygame.draw.circle(self.screen, BLACK, (int(x), int(y)), CHECKER_RADIUS, 3)
        else:
            pygame.draw.circle(self.screen, BLACK, (int(x), int(y)), CHECKER_RADIUS)
            pygame.draw.circle(self.screen, WHITE, (int(x), int(y)), CHECKER_RADIUS, 3)
    
    def draw_checkers(self):
        """Dibuja todas las fichas - USA BackgammonGame.get_tablero()"""
        if not self.game:
            return
        
        board_state = self.game.get_tablero()
        
        for point_num, checkers in enumerate(board_state['posiciones']):
            if not checkers:
                continue
            
            x, y, direction = self.get_point_position(point_num)
            
            for i, checker in enumerate(checkers[:6]):
                offset = (CHECKER_RADIUS * 2 + 4) * i
                cy = y + direction * (CHECKER_RADIUS + offset)
                
                symbol = checker.get_simbolo() if hasattr(checker, 'get_simbolo') else str(checker)
                self.draw_checker(x, cy, symbol)
            
            if len(checkers) > 6:
                offset = (CHECKER_RADIUS * 2 + 4) * 6
                cy = y + direction * (CHECKER_RADIUS + offset)
                self.draw_text_centered(f"+{len(checkers) - 6}", x, cy, self.font_small, WHITE)
        
        bar_x = self.board_x + (BOARD_WIDTH - BAR_WIDTH) // 2 + BAR_WIDTH // 2
        
        for i in range(min(board_state['bar']['player1'], 5)):
            cy = self.board_y + BOARD_HEIGHT - 40 - (i * 44)
            self.draw_checker(bar_x, cy, 'X')
        
        for i in range(min(board_state['bar']['player2'], 5)):
            cy = self.board_y + 40 + (i * 44)
            self.draw_checker(bar_x, cy, 'O')
    
    def draw_board(self):
        """Dibuja el tablero completo"""
        pygame.draw.rect(self.screen, WOOD_BROWN, 
                        (self.board_x, self.board_y, BOARD_WIDTH, BOARD_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, 
                        (self.board_x, self.board_y, BOARD_WIDTH, BOARD_HEIGHT), 4)
        
        bar_x = self.board_x + (BOARD_WIDTH - BAR_WIDTH) // 2
        pygame.draw.rect(self.screen, DARK_BROWN, 
                        (bar_x, self.board_y, BAR_WIDTH, BOARD_HEIGHT))
        pygame.draw.line(self.screen, BLACK, 
                        (bar_x, self.board_y), 
                        (bar_x, self.board_y + BOARD_HEIGHT), 3)
        pygame.draw.line(self.screen, BLACK, 
                        (bar_x + BAR_WIDTH, self.board_y), 
                        (bar_x + BAR_WIDTH, self.board_y + BOARD_HEIGHT), 3)
        
        for i in range(24):
            self.draw_point(i)
        
        self.draw_checkers()
        
        self.draw_text_centered("BAR", bar_x + BAR_WIDTH // 2, 
                               self.board_y + BOARD_HEIGHT // 2, 
                               self.font_small, WHITE)
        
        self.draw_bear_off_zone()
    
    def draw_dice_face(self, x, y, value):
        """Dibuja un dado"""
        size = 50
        pygame.draw.rect(self.screen, WHITE, (x, y, size, size), border_radius=8)
        pygame.draw.rect(self.screen, BLACK, (x, y, size, size), 2, border_radius=8)
        
        dot_positions = {
            1: [(25, 25)],
            2: [(15, 15), (35, 35)],
            3: [(15, 15), (25, 25), (35, 35)],
            4: [(15, 15), (35, 15), (15, 35), (35, 35)],
            5: [(15, 15), (35, 15), (25, 25), (15, 35), (35, 35)],
            6: [(15, 15), (35, 15), (15, 25), (35, 25), (15, 35), (35, 35)]
        }
        
        for dx, dy in dot_positions[value]:
            pygame.draw.circle(self.screen, BLACK, (x + dx, y + dy), 4)
    
    def draw_bear_off_zone(self):
        """Dibuja la zona de bear off - USA BackgammonGame.get_estado_juego()"""
        if not self.game:
            return
        
        bear_off_x = self.board_x + BOARD_WIDTH + 10
        bear_off_width = 100
        
        estado = self.game.get_estado_juego()
        if not estado:
            return
        
        # Zona superior (Jugador X - Blancas)
        pygame.draw.rect(self.screen, LIGHT_BEIGE,
                        (bear_off_x, self.board_y, bear_off_width, BOARD_HEIGHT // 2 - 5))
        pygame.draw.rect(self.screen, WHITE,
                        (bear_off_x, self.board_y, bear_off_width, BOARD_HEIGHT // 2 - 5), 3)
        
        self.draw_text_centered("BEAR OFF", bear_off_x + bear_off_width // 2,
                               self.board_y + 30, self.font_tiny, WHITE)
        
        if 'jugador2' in estado:
            fichas_out = estado['jugador2']['fichas_sacadas']
            self.draw_text_centered(str(fichas_out), bear_off_x + bear_off_width // 2,
                                   self.board_y + 60, self.font_medium, WHITE)
            for i in range(min(fichas_out, 5)):
                cy = self.board_y + 90 + (i * 35)
                self.draw_checker(bear_off_x + bear_off_width // 2, cy, 'X')
        
        # Zona inferior (Jugador O - Negras)
        pygame.draw.rect(self.screen, DARK_BEIGE,
                        (bear_off_x, self.board_y + BOARD_HEIGHT // 2 + 5, 
                         bear_off_width, BOARD_HEIGHT // 2 - 5))
        pygame.draw.rect(self.screen, BLACK,
                        (bear_off_x, self.board_y + BOARD_HEIGHT // 2 + 5,
                         bear_off_width, BOARD_HEIGHT // 2 - 5), 3)
        
        self.draw_text_centered("BEAR OFF", bear_off_x + bear_off_width // 2,
                               self.board_y + BOARD_HEIGHT - 30, self.font_tiny, BLACK)
        
        if 'jugador1' in estado:
            fichas_out = estado['jugador1']['fichas_sacadas']
            self.draw_text_centered(str(fichas_out), bear_off_x + bear_off_width // 2,
                                   self.board_y + BOARD_HEIGHT - 60, self.font_medium, BLACK)
            for i in range(min(fichas_out, 5)):
                cy = self.board_y + BOARD_HEIGHT - 90 - (i * 35)
                self.draw_checker(bear_off_x + bear_off_width // 2, cy, 'O')
    def draw_game_info(self):
        """Panel lateral de información - USA BackgammonGame.get_estado_juego()"""
        if not self.game:
            return
        
        px = WIDTH - 270
        y = 100
        
        estado = self.game.get_estado_juego()
        
        # Información del turno
        if estado['jugador_actual']:
            self.draw_text("Turno:", px, y, self.font_medium, GOLD)
            y += 35
            self.draw_text(estado['jugador_actual'], px, y, self.font_small, GREEN)
            y += 30
            
            jugador = self.game.get_jugador_actual()
            ficha = jugador.get_ficha()
            
            if ficha == 'X':
                pygame.draw.circle(self.screen, WHITE, (px + 10, y + 10), 10)
                pygame.draw.circle(self.screen, BLACK, (px + 10, y + 10), 10, 2)
                self.draw_text("Blancas", px + 30, y, self.font_small, WHITE)
            else:
                pygame.draw.circle(self.screen, BLACK, (px + 10, y + 10), 10)
                pygame.draw.circle(self.screen, WHITE, (px + 10, y + 10), 10, 2)
                self.draw_text("Negras", px + 30, y, self.font_small, WHITE)
            
            y += 35
            mov = self.game.get_movimientos_restantes()
            self.draw_text(f"Movimientos: {mov}", px, y, self.font_small, WHITE)
            y += 50
        
        # Dados - USA BackgammonGame.get_dados_disponibles()
        if self.dados_actuales and self.dados_lanzados and self.game.get_movimientos_restantes() > 0:
            self.draw_text("Dados disponibles:", px, y, self.font_medium, WHITE)
            y += 40
            
            dados_disponibles = self.game.get_dados_disponibles()
            
            for i, val in enumerate(dados_disponibles[:4]):
                col = i % 2
                row = i // 2
                dice_x = px + col * 70
                dice_y = y + row * 70
                self.draw_dice_face(dice_x, dice_y, val)
            
            y += 150
        else:
            y += 60
        
        # Botones
        self.buttons['roll_dice'].rect.y = y
        self.buttons['roll_dice'].draw(self.screen, self.font_small)
        y += 70
        
        self.buttons['menu'].rect.y = y
        self.buttons['menu'].draw(self.screen, self.font_small)
        
        # Estadísticas
        y = HEIGHT - 220
        self.draw_text("Estadísticas:", px, y, self.font_medium, GOLD)
        y += 35
        
        p1 = estado['jugador1']
        pygame.draw.circle(self.screen, WHITE, (px + 5, y + 8), 8)
        pygame.draw.circle(self.screen, BLACK, (px + 5, y + 8), 8, 2)
        self.draw_text(f"{p1['nombre']}", px + 20, y, self.font_small, WHITE)
        y += 22
        self.draw_text(f"Tablero: {p1['fichas_tablero']}", px + 10, y, self.font_tiny, WHITE)
        y += 18
        self.draw_text(f"Fuera: {p1['fichas_sacadas']}", px + 10, y, self.font_tiny, WHITE)
        y += 30
        
        p2 = estado['jugador2']
        pygame.draw.circle(self.screen, BLACK, (px + 5, y + 8), 8)
        pygame.draw.circle(self.screen, WHITE, (px + 5, y + 8), 8, 2)
        self.draw_text(f"{p2['nombre']}", px + 20, y, self.font_small, WHITE)
        y += 22
        self.draw_text(f"Tablero: {p2['fichas_tablero']}", px + 10, y, self.font_tiny, WHITE)
        y += 18
        self.draw_text(f"Fuera: {p2['fichas_sacadas']}", px + 10, y, self.font_tiny, WHITE)
    
    def draw_message_overlay(self):
        """Mensaje temporal"""
        if self.message and self.message_timer > 0:
            s = pygame.Surface((900, 100))
            s.set_alpha(230)
            s.fill(BLACK)
            self.screen.blit(s, (WIDTH//2 - 450, HEIGHT - 130))
            
            # Dividir mensaje en líneas si es muy largo
            words = self.message.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                if len(test_line) > 60:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Dibujar líneas
            for i, line in enumerate(lines[:2]):  # Máximo 2 líneas
                self.draw_text_centered(line, WIDTH//2, HEIGHT - 95 + (i * 30), 
                                       self.font_small, self.message_color)
    
    def draw_game(self):
        """Pantalla de juego"""
        self.screen.fill(DARK_BROWN)
        self.draw_text_centered("BACKGAMMON", WIDTH//2, 30, self.font_large, GOLD)
        self.draw_board()
        self.draw_game_info()
        self.draw_message_overlay()
    
    def draw_winner(self):
        """Pantalla de victoria - USA BackgammonGame.get_estado_juego()"""
        self.screen.fill(DARK_BROWN)
        self.draw_text_centered("¡Juego Terminado!", WIDTH//2, 200, self.font_large, GOLD)
        
        estado = self.game.get_estado_juego()
        if estado and estado['jugador_actual']:
            self.draw_text_centered(f"¡{estado['jugador_actual']} ha ganado!", 
                                   WIDTH//2, 300, self.font_medium, GREEN)
        
        self.buttons['new_game'].draw(self.screen, self.font_medium)
        self.buttons['quit'].draw(self.screen, self.font_medium)

    def run(self):
        """Bucle principal"""
        running = True
        
        while running:
            self.dt = self.clock.get_time()
            
            running = self.handle_events()
            self.update_message_timer()
            
            if self.state == "MENU":
                self.draw_menu()
            elif self.state == "NAME_INPUT":
                self.draw_name_input()
            elif self.state == "GAME":
                self.draw_game()
            elif self.state == "WINNER":
                self.draw_winner()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()


def main():
    game = BackgammonPygame()
    game.run()


if __name__ == "__main__":
    main()