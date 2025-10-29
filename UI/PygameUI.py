"""
Backgammon con Pygame - Versión Corregida
Tablero con disposición correcta de puntos y fichas
"""
import pygame
from core.clases.backgammon_game import BackgammonGame

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
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Dimensiones
MARGIN = 50
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
    """Juego principal"""
    
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
        self.dice_values = None
        self.dice_rolled = False
        self.winner = None
        
        self.message = ""
        self.message_timer = 0
        self.player1_name = ""
        self.player2_name = ""
        self.current_input = 1
        self.input_text = ""
        
        self.buttons = self.create_buttons()
        self.dt = 0
        
        # Calcular posición del tablero centrado
        self.board_x = (WIDTH - BOARD_WIDTH - 300) // 2
        self.board_y = (HEIGHT - BOARD_HEIGHT) // 2
    
    def create_buttons(self):
        return {
            'new_game': Button(WIDTH//2 - 100, 350, 200, 50, "Nueva Partida"),
            'quit': Button(WIDTH//2 - 100, 430, 200, 50, "Salir"),
            'roll_dice': Button(WIDTH - 280, 250, 220, 50, "Lanzar Dados"),
            'menu': Button(WIDTH - 280, 320, 220, 50, "Menu")
        }
    
    def show_message(self, text, duration=3000):
        self.message = text
        self.message_timer = duration
    
    def update_message_timer(self):
        if self.message_timer > 0:
            self.message_timer -= self.dt
            if self.message_timer < 0:
                self.message_timer = 0
                self.message = ""
    
    def get_point_position(self, point_num):
        """
        Calcula posición de un punto en el tablero.
        Puntos 0-11: Parte inferior (jugador X)
        Puntos 12-23: Parte superior (jugador O)
        """
        # Cuadrante en el tablero
        if point_num < 6:
            # Cuadrante inferior derecho (0-5)
            # De derecha a izquierda: 0, 1, 2, 3, 4, 5
            x = self.board_x + BOARD_WIDTH - (point_num + 1) * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y + BOARD_HEIGHT
            direction = -1
        elif point_num < 12:
            # Cuadrante inferior izquierdo (6-11)
            # De derecha a izquierda: 6, 7, 8, 9, 10, 11
            offset_from_left = 11 - point_num  # 5, 4, 3, 2, 1, 0
            x = self.board_x + offset_from_left * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y + BOARD_HEIGHT
            direction = -1
        elif point_num < 18:
            # Cuadrante superior izquierdo (12-17)
            # De izquierda a derecha: 12, 13, 14, 15, 16, 17
            offset = point_num - 12  # 0, 1, 2, 3, 4, 5
            x = self.board_x + offset * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y
            direction = 1
        else:
            # Cuadrante superior derecho (18-23)
            # De izquierda a derecha: 18, 19, 20, 21, 22, 23
            offset = point_num - 18  # 0, 1, 2, 3, 4, 5
            x = self.board_x + BOARD_WIDTH // 2 + BAR_WIDTH // 2 + offset * POINT_WIDTH + POINT_WIDTH // 2
            y = self.board_y
            direction = 1
        
        return x, y, direction
    
    def get_clicked_point(self, pos):
        """Detecta qué punto fue clickeado"""
        mx, my = pos
        
        # Verificar bar
        bar_x = self.board_x + (BOARD_WIDTH - BAR_WIDTH) // 2
        if bar_x <= mx <= bar_x + BAR_WIDTH:
            if self.board_y <= my <= self.board_y + BOARD_HEIGHT:
                return "bar"
        
        # Verificar puntos
        for point_num in range(24):
            x, y, direction = self.get_point_position(point_num)
            
            # Área del triángulo
            if direction == 1:  # Superior
                if (x - POINT_WIDTH//2 <= mx <= x + POINT_WIDTH//2 and
                    y <= my <= y + POINT_HEIGHT):
                    return point_num
            else:  # Inferior
                if (x - POINT_WIDTH//2 <= mx <= x + POINT_WIDTH//2 and
                    y - POINT_HEIGHT <= my <= y):
                    return point_num
        
        return None
    
    # ==================== LÓGICA ====================
    
    def start_game(self):
        name1 = self.player1_name.strip() or "Jugador 1"
        name2 = self.player2_name.strip() or "Jugador 2"
        
        self.game = BackgammonGame(name1, name2)
        self.game.quien_empieza()
        
        self.state = "GAME"
        self.dice_rolled = False
        self.dice_values = None
        self.selected_point = None
        self.winner = None
        
        jugador = self.game.get_jugador_actual()
        self.show_message(f"{jugador.get_nombre()} comienza!")
    
    def roll_dice(self):
        if not self.game or self.dice_rolled:
            return
        
        d1, d2, _ = self.game.lanzar_dados()
        self.dice_values = [d1, d2]
        self.dice_rolled = True
        
        jugador = self.game.get_jugador_actual()
        
        if not self.game.tiene_movimientos_legales(jugador, d1, d2):
            self.show_message("Sin movimientos legales. Turno pasado.")
            self.game.cambiar_turno()
            self.dice_rolled = False
            self.dice_values = None
        else:
            self.show_message(f"Dados: {d1}, {d2}")
    
    def handle_board_click(self, pos):
        if not self.game or not self.dice_rolled:
            return
        
        clicked = self.get_clicked_point(pos)
        if clicked is None:
            return
        
        if self.selected_point is None:
            self.selected_point = clicked
            self.show_message(f"Seleccionado: {clicked}", 2000)
        else:
            self.try_move(self.selected_point, clicked)
            self.selected_point = None
    
    def try_move(self, origin, dest):
        try:
            movimientos = [(origin, dest)]
            resultado = self.game.mover_ficha(
                movimientos,
                self.dice_values[0],
                self.dice_values[1]
            )
            
            if any(resultado['resultados']):
                self.show_message("¡Movimiento exitoso!")
                
                if self.game.hay_ganador():
                    estado = self.game.get_estado_juego()
                    self.winner = estado['jugador_actual']
                    self.state = "WINNER"
                
                if self.game.get_movimientos_restantes() == 0:
                    self.dice_rolled = False
                    self.dice_values = None
            else:
                msg = resultado['log'][0] if resultado['log'] else "Movimiento inválido"
                self.show_message(msg, 3000)
        except Exception as e:
            self.show_message(f"Error: {str(e)}", 3000)
    
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
        
        # Alternar colores
        color = LIGHT_BEIGE if point_num % 2 == 0 else DARK_BEIGE
        
        if self.selected_point == point_num:
            color = HIGHLIGHT
        
        # Triángulo
        if direction == 1:  # Apunta hacia abajo
            points = [
                (x, y),
                (x - POINT_WIDTH // 2, y + POINT_HEIGHT),
                (x + POINT_WIDTH // 2, y + POINT_HEIGHT)
            ]
            num_y = y + POINT_HEIGHT + 15
        else:  # Apunta hacia arriba
            points = [
                (x, y),
                (x - POINT_WIDTH // 2, y - POINT_HEIGHT),
                (x + POINT_WIDTH // 2, y - POINT_HEIGHT)
            ]
            num_y = y - POINT_HEIGHT - 25
        
        pygame.draw.polygon(self.screen, color, points)
        pygame.draw.polygon(self.screen, BLACK, points, 2)
        
        # Número del punto
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
        """Dibuja todas las fichas"""
        if not self.game:
            return
        
        board_state = self.game.get_tablero()
        
        # Fichas en puntos
        for point_num, checkers in enumerate(board_state['posiciones']):
            if not checkers:
                continue
            
            x, y, direction = self.get_point_position(point_num)
            
            for i, checker in enumerate(checkers[:6]):
                offset = (CHECKER_RADIUS * 2 + 4) * i
                cy = y + direction * (CHECKER_RADIUS + offset)
                
                symbol = checker.get_simbolo() if hasattr(checker, 'get_simbolo') else str(checker)
                self.draw_checker(x, cy, symbol)
            
            # Contador si hay más de 6
            if len(checkers) > 6:
                offset = (CHECKER_RADIUS * 2 + 4) * 6
                cy = y + direction * (CHECKER_RADIUS + offset)
                self.draw_text_centered(f"+{len(checkers) - 6}", x, cy, self.font_small, WHITE)
        
        # Bar
        bar_x = self.board_x + (BOARD_WIDTH - BAR_WIDTH) // 2 + BAR_WIDTH // 2
        
        # Player 1 (X) abajo
        for i in range(min(board_state['bar']['player1'], 5)):
            cy = self.board_y + BOARD_HEIGHT - 40 - (i * 44)
            self.draw_checker(bar_x, cy, 'X')
        
        # Player 2 (O) arriba
        for i in range(min(board_state['bar']['player2'], 5)):
            cy = self.board_y + 40 + (i * 44)
            self.draw_checker(bar_x, cy, 'O')
    
    def draw_board(self):
        """Dibuja el tablero completo"""
        # Fondo del tablero
        pygame.draw.rect(self.screen, WOOD_BROWN, 
                        (self.board_x, self.board_y, BOARD_WIDTH, BOARD_HEIGHT))
        pygame.draw.rect(self.screen, BLACK, 
                        (self.board_x, self.board_y, BOARD_WIDTH, BOARD_HEIGHT), 4)
        
        # Bar central
        bar_x = self.board_x + (BOARD_WIDTH - BAR_WIDTH) // 2
        pygame.draw.rect(self.screen, DARK_BROWN, 
                        (bar_x, self.board_y, BAR_WIDTH, BOARD_HEIGHT))
        pygame.draw.line(self.screen, BLACK, 
                        (bar_x, self.board_y), 
                        (bar_x, self.board_y + BOARD_HEIGHT), 3)
        pygame.draw.line(self.screen, BLACK, 
                        (bar_x + BAR_WIDTH, self.board_y), 
                        (bar_x + BAR_WIDTH, self.board_y + BOARD_HEIGHT), 3)
        
        # Puntos
        for i in range(24):
            self.draw_point(i)
        
        # Fichas
        self.draw_checkers()
        
        # Texto "BAR"
        self.draw_text_centered("BAR", bar_x + BAR_WIDTH // 2, 
                               self.board_y + BOARD_HEIGHT // 2, 
                               self.font_small, WHITE)
    
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
    
    def draw_game_info(self):
        """Panel lateral de información"""
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
        
        # Dados - mostrar solo si están lanzados
        if self.dice_values and self.dice_rolled:
            self.draw_text("Dados:", px, y, self.font_medium, WHITE)
            y += 40
            
            dados_disp = self.game.calcular_movimientos_totales(
                self.dice_values[0], self.dice_values[1]
            )
            
            # Dibujar dados en una cuadrícula de 2x2
            for i, val in enumerate(dados_disp[:4]):
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
            s = pygame.Surface((700, 80))
            s.set_alpha(220)
            s.fill(BLACK)
            self.screen.blit(s, (WIDTH//2 - 350, HEIGHT - 120))
            self.draw_text_centered(self.message, WIDTH//2, HEIGHT - 80, self.font_medium, GOLD)
    
    def draw_game(self):
        """Pantalla de juego"""
        self.screen.fill(DARK_BROWN)
        self.draw_text_centered("BACKGAMMON", WIDTH//2, 30, self.font_large, GOLD)
        self.draw_board()
        self.draw_game_info()
        self.draw_message_overlay()
    
    def draw_winner(self):
        """Pantalla de victoria"""
        self.screen.fill(DARK_BROWN)
        self.draw_text_centered("¡Juego Terminado!", WIDTH//2, 200, self.font_large, GOLD)
        
        if self.winner:
            self.draw_text_centered(f"¡{self.winner} ha ganado!", WIDTH//2, 300, self.font_medium, GREEN)
        
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