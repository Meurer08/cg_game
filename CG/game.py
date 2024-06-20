import pygame
from OpenGL.GL import *
from player import Player
from box import Box
from utils import draw_matrix

EMPTY = 0
BOX = 1
PLAYER = 2

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.matrix_size = 10
        self.cell_size = screen_height // self.matrix_size
        self.boxes = [Box(self.matrix_size - 2, self.matrix_size - 1, self.cell_size), Box(self.matrix_size - 7, self.matrix_size - 1, self.cell_size)]  # Posiciona a caixa na última linha, penúltima coluna
        self.player = Player(self.matrix_size, self.cell_size)
        self.clock = pygame.time.Clock()
        self.is_jumping = False
        self.jump_velocity = 0.4  # Velocidade do pulo
        self.gravity = 0.05  # Gravidade
        self.jump_peak_reached = False
        self.matrix = [] # matriz para controle dos blocos

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
        if self.player.y >= 9:
            return False
        else:
            print(self.matrix[int(self.player.y + 1)][self.player.x])
            if (self.matrix[int(self.player.y + 1)][self.player.x] == BOX):
                self.is_jumping = False
                self.jump_peak_reached = False
                self.player.y = self.boxes[0].y - 1  # Coloca o jogador em cima da caixa
            
        #5 Checa se o jogador está colidindo com a caixa

    def run(self):
        self.init_gl()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left(self.boxes)
                        self.is_jumping = True
                        self.jump_velocity = 0.4  # Reinicia a velocidade do pulo
                        self.jump_peak_reached = True
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right(self.boxes)
                        self.is_jumping = True
                        self.jump_velocity = 0.4  # Reinicia a velocidade do pulo
                        self.jump_peak_reached = True
                    elif event.key == pygame.K_SPACE and not self.is_jumping:
                        self.is_jumping = True
                        self.jump_velocity = 0.4  # Reinicia a velocidade do pulo
                        self.jump_peak_reached = False

            if self.is_jumping:
                future_y = self.player.y - self.jump_velocity if not self.jump_peak_reached else self.player.y + self.gravity
                print("Future Y", future_y)
                if not self.jump_peak_reached:
                    self.player.jump(self.jump_velocity)
                    self.jump_velocity -= self.gravity  # Aplica gravidade
                    if self.jump_velocity <= 0:
                        self.jump_peak_reached = True
                else:
                    self.player.jump(-self.gravity)  # Desce com a gravidade
                    if self.player.y >= self.player.ground_y:
                        self.is_jumping = False
                        self.player.y = self.player.ground_y  # Garante que o jogador não passe do chão
                        self.player.jump_offset = 0  # Reseta o pulo

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            draw_matrix(self.matrix_size, self.cell_size)
            self.detect_collision()
            self.matrixRender()
            self.player.draw()

            pygame.display.flip()
            self.clock.tick(60)
 