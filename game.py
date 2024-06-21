import pygame
import random
from OpenGL.GL import *
from player import Player
from box import Box
from utils import draw_matrix

# Definição de constantes para representar diferentes estados na matriz
EMPTY = 0
BOX = 1
PLAYER = 2

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        pygame.display.set_mode((self.screen_width, self.screen_height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.matrix_size = 10
        self.cell_size = screen_height // self.matrix_size
        self.boxes = []
        self.player = Player(self.matrix_size, self.cell_size)
        self.clock = pygame.time.Clock()
        self.is_jumping = False
        self.jump_velocity = 0.4
        self.gravity = 0.05
        self.jump_peak_reached = False
        self.matrix = []
        self.game_over = False
        self.box_drop_interval = 500
        self.box_drop_timer = pygame.time.get_ticks()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 50)
        self.menu_font = pygame.font.SysFont('Arial', 40)
        self.selected_option = 0
        self.menu_options = ["Iniciar", "Sair"]
        print(f"Janela criada com dimensões: {self.screen_width}x{self.screen_height}")

    def generate_random_box(self):
        x = random.randint(0, self.matrix_size - 1)
        y = 0
        new_box = Box(x, y, self.cell_size)
        self.boxes.append(new_box)

    def update_boxes(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.box_drop_timer > self.box_drop_interval:
            for box in self.boxes:
                if box.y < self.matrix_size - 1 and self.matrix[box.y + 1][box.x] != BOX:
                    if not (box.x == self.player.x and box.y + 1 == int(self.player.y)):
                        box.y += 1
                    else:
                        self.game_over = True
            self.box_drop_timer = current_time

    def matrixRender(self):
        self.matrix = [[EMPTY for _ in range(self.matrix_size)] for _ in range(self.matrix_size)]

        for i in self.boxes:
            self.matrix[i.y][i.x] = BOX
            i.draw()
        aux = self.player.y

        self.matrix[int(aux)][self.player.x] = PLAYER

    def init_gl(self):
        glViewport(0, 0, self.screen_width, self.screen_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.screen_width, self.screen_height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(0.0, 0.0, 0.0, 1.0)

    def detect_collision(self):
        for box in self.boxes:
            if box.x == self.player.x and box.y == int(self.player.y):
                print("Colisão detectada")
                self.game_over = True

        if self.player.y >= 9:
            return False
        else:
            resto = self.player.y % 1
            playery = self.player.y - resto
            if (self.matrix[int(playery + 1)][self.player.x] == BOX and self.is_jumping):
                self.is_jumping = False
                self.jump_peak_reached = False
                self.player.y = playery

    def show_game_over(self):
        print("Chamando show_game_over.")
        pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame_surface = pygame.display.get_surface()
        pygame_surface.fill((0, 0, 0))
        text_surface = self.font.render('Game Over', True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        pygame_surface.blit(text_surface, text_rect)

        continue_surface = self.menu_font.render('Pressione Enter para voltar ao menu', True, (255, 255, 255))
        continue_rect = continue_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        pygame_surface.blit(continue_surface, continue_rect)

        pygame.display.flip()
        print(f"Texto 'Game Over' desenhado na posição: {text_rect.topleft}")

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    waiting = False

    def show_menu(self):
        pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame_surface = pygame.display.get_surface()
        pygame_surface.fill((0, 0, 0))

        title_surface = self.font.render('Menu', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        pygame_surface.blit(title_surface, title_rect)

        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i != self.selected_option else (255, 0, 0)
            option_surface = self.menu_font.render(option, True, color)
            option_rect = option_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + i * 50))
            pygame_surface.blit(option_surface, option_rect)

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                        self.show_menu()
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                        self.show_menu()
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:  # Iniciar
                            waiting = False
                        elif self.selected_option == 1:  # Sair
                            pygame.quit()
                            exit()

    def run(self):
        self.show_menu()
        pygame.display.set_mode((self.screen_width, self.screen_height), pygame.OPENGL | pygame.DOUBLEBUF)
        self.init_gl()
        self.boxes = []
        self.player = Player(self.matrix_size, self.cell_size)
        self.game_over = False

        box_timer = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left(self.boxes)
                        self.is_jumping = True
                        self.jump_velocity = 0.4
                        self.jump_peak_reached = True
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right(self.boxes)
                        self.is_jumping = True
                        self.jump_velocity = 0.4
                        self.jump_peak_reached = True
                    elif event.key == pygame.K_SPACE and not self.is_jumping:
                        self.is_jumping = True
                        self.jump_velocity = 0.4
                        self.jump_peak_reached = False

            if self.is_jumping:
                future_y = self.player.y - self.jump_velocity if not self.jump_peak_reached else self.player.y + self.gravity
                if not self.jump_peak_reached:
                    self.player.jump(self.jump_velocity)
                    self.jump_velocity -= self.gravity
                    if self.jump_velocity <= 0:
                        self.jump_peak_reached = True
                else:
                    self.player.jump(-self.gravity)
                    if self.player.y >= self.player.ground_y:
                        self.is_jumping = False
                        self.player.y = self.player.ground_y
                        self.player.jump_offset = 0

            self.clear_complete_lines()

            box_timer += 1
            if box_timer >= 120:
                self.generate_random_box()
                box_timer = 0

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            draw_matrix(self.matrix_size, self.cell_size)
            self.player.draw()

            self.matrixRender()
            self.detect_collision()
            if self.game_over:
                print("Game Over no loop")
                self.show_game_over()
                self.show_menu()
                self.run()
                return
            self.update_boxes()
            pygame.display.flip()
            self.clock.tick(60)

    def clear_complete_lines(self):
        max_y = max(box.y for box in self.boxes) if self.boxes else 0

        for y in range(max_y + 1):
            if self.is_line_complete(y):
                self.remove_line(y)
                self.move_boxes_down(y)

    def is_line_complete(self, y):
        line_boxes = [box for box in self.boxes if box.y == y]
        return len(line_boxes) == self.matrix_size

    def remove_line(self, y):
        self.boxes = [box for box in self.boxes if box.y != y]
        self.is_jumping = True
        self.jump_peak_reached = True

    def move_boxes_down(self, y):
        for box in self.boxes:
            if box.y < y:
                box.y += 1
