import pygame  # Importa a biblioteca pygame para gerenciamento de eventos e gráficos
import random  # Importa a biblioteca random para geração de números aleatórios
from OpenGL.GL import *  # Importa todas as funções da biblioteca OpenGL
from player import Player  # Importa a classe Player do arquivo player.py
from box import Box  # Importa a classe Box do arquivo box.py
from utils import draw_matrix  # Importa a função draw_matrix do arquivo utils.py

# Definição de constantes para representar diferentes estados na matriz
EMPTY = 0
BOX = 1
PLAYER = 2

class Game:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width  # Armazena a largura da tela
        self.screen_height = screen_height  # Armazena a altura da tela
        self.matrix_size = 10  # Define o tamanho da matriz
        self.cell_size = screen_height // self.matrix_size  # Calcula o tamanho da célula com base na altura da tela
        # Inicializa a lista de caixas com duas caixas em posições específicas
        self.boxes = [Box(self.matrix_size - 2, self.matrix_size - 1, self.cell_size),
                      Box(self.matrix_size - 7, self.matrix_size - 1, self.cell_size)]
        self.player = Player(self.matrix_size, self.cell_size)  # Cria uma instância do jogador
        self.clock = pygame.time.Clock()  # Cria um objeto de relógio para controlar a taxa de atualização do jogo
        self.is_jumping = False  # Indica se o jogador está pulando
        self.jump_velocity = 0.4  # Define a velocidade inicial do pulo
        self.gravity = 0.05  # Define a gravidade aplicada ao jogador
        self.jump_peak_reached = False  # Indica se o pico do pulo foi alcançado
        self.matrix = []  # Inicializa a matriz de controle de blocos

    def generate_random_box(self):
        x = random.randint(0, self.matrix_size - 1)  # Gera uma posição X aleatória no topo da matriz
        y = 0  # A posição Y é sempre 0, pois a caixa cai do topo
        new_box = Box(x, y, self.cell_size)  # Cria uma nova caixa
        self.boxes.append(new_box)  # Adiciona a nova caixa à lista de caixas

    def update_boxes(self):
        for box in self.boxes:
            if box.y < self.matrix_size - 1 and self.matrix[box.y + 1][box.x] != BOX:  # Verifica se a caixa pode se mover para baixo
                box.y += 1  # Move a caixa para baixo

    def matrixRender(self):
        self.matrix = [[EMPTY for _ in range(self.matrix_size)] for _ in range(self.matrix_size)]  # Inicializa a matriz com valores EMPTY

        for i in self.boxes:
            self.matrix[i.y][i.x] = BOX  # Marca a posição das caixas na matriz
            i.draw()  # Desenha as caixas
        aux = self.player.y

        self.matrix[int(aux)][self.player.x] = PLAYER  # Marca a posição do jogador na matriz

    def init_gl(self):
        glViewport(0, 0, self.screen_width, self.screen_height)  # Define a área de visualização do OpenGL
        glMatrixMode(GL_PROJECTION)  # Define a matriz de projeção
        glLoadIdentity()  # Reseta a matriz de projeção
        glOrtho(0, self.screen_width, self.screen_height, 0, -1, 1)  # Define uma projeção ortográfica
        glMatrixMode(GL_MODELVIEW)  # Define a matriz de visualização do modelo
        glLoadIdentity()  # Reseta a matriz de visualização do modelo
        glClearColor(0.0, 0.0, 0.0, 1.0)  # Define a cor de fundo da tela

    def detect_collision(self):
        if self.player.y >= 9:  # Verifica se o jogador está no chão
            return False
        else:
            print(self.matrix[int(self.player.y + 1)][self.player.x])  # Imprime o estado da célula abaixo do jogador
            if (self.matrix[int(self.player.y + 1)][self.player.x] == BOX):  # Verifica se há uma caixa abaixo do jogador
                self.is_jumping = False  # Para o pulo do jogador
                self.jump_peak_reached = False  # Reseta o pico do pulo
                self.player.y = self.boxes[0].y - 1  # Coloca o jogador em cima da caixa

    def run(self):
        self.init_gl()  # Inicializa a configuração do OpenGL
        box_timer = 0  # Inicializa o temporizador para gerar novas caixas
        while True:
            for event in pygame.event.get():  # Lida com eventos do Pygame
                if event.type == pygame.QUIT:
                    pygame.quit()  # Encerra o Pygame
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.move_left(self.boxes)  # Move o jogador para a esquerda
                        self.is_jumping = True
                        self.jump_velocity = 0.4  # Reinicia a velocidade do pulo
                        self.jump_peak_reached = True
                    elif event.key == pygame.K_RIGHT:
                        self.player.move_right(self.boxes)  # Move o jogador para a direita
                        self.is_jumping = True
                        self.jump_velocity = 0.4  # Reinicia a velocidade do pulo
                        self.jump_peak_reached = True
                    elif event.key == pygame.K_SPACE and not self.is_jumping:
                        self.is_jumping = True
                        self.jump_velocity = 0.4  # Reinicia a velocidade do pulo
                        self.jump_peak_reached = False

            if self.is_jumping:
                future_y = self.player.y - self.jump_velocity if not self.jump_peak_reached else self.player.y + self.gravity
                if not self.jump_peak_reached:
                    self.player.jump(self.jump_velocity)  # Pula com a velocidade atual
                    self.jump_velocity -= self.gravity  # Aplica a gravidade
                    if self.jump_velocity <= 0:
                        self.jump_peak_reached = True
                else:
                    self.player.jump(-self.gravity)  # Desce com a gravidade
                    if self.player.y >= self.player.ground_y:
                        self.is_jumping = False
                        self.player.y = self.player.ground_y  # Garante que o jogador não passe do chão
                        self.player.jump_offset = 0  # Reseta o pulo

            self.update_boxes()  # Atualiza a queda das caixas
            self.clear_complete_lines()  # Limpa as linhas completas

            box_timer += 1  # Incrementa o temporizador
            if box_timer >= 120:  # Gera uma nova caixa a cada intervalo de tempo
                self.generate_random_box()
                box_timer = 0

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Limpa o buffer de cor e profundidade
            draw_matrix(self.matrix_size, self.cell_size)  # Desenha a matriz
            self.detect_collision()  # Detecta colisões
            self.matrixRender()  # Renderiza a matriz
            self.player.draw()  # Desenha o jogador

            pygame.display.flip()  # Atualiza a tela
            self.clock.tick(60)  # Limita a taxa de quadros para 60 FPS

    def clear_complete_lines(self):
        max_y = max(box.y for box in self.boxes) if self.boxes else 0  # Determina o y máximo (altura da matriz)

        for y in range(max_y + 1):  # Verifica cada linha até o y máximo
            if self.is_line_complete(y):  # Se a linha estiver completa
                self.remove_line(y)  # Remove a linha
                self.move_boxes_down(y)  # Move as caixas acima da linha para baixo

    def is_line_complete(self, y):
        line_boxes = [box for box in self.boxes if box.y == y]  # Obtém todas as caixas na linha y
        return len(line_boxes) == self.matrix_size  # Verifica se a linha está completa

    def remove_line(self, y):
        self.boxes = [box for box in self.boxes if box.y != y]  # Remove todas as caixas na linha y

    def move_boxes_down(self, y):
        for box in self.boxes:
            if box.y < y:  # Para cada caixa acima da linha y
                box.y += 1  # Move a caixa uma posição para baixo
