from OpenGL.GL import *  # Importa todas as funções da biblioteca OpenGL

class Player:
    def __init__(self, matrix_size, cell_size):
        self.x = matrix_size // 2  # Define a posição x inicial do jogador no centro da matriz
        self.y = matrix_size - 1  # Define a posição y inicial do jogador no topo da matriz
        self.ground_y = self.y  # Guarda a posição inicial do chão do jogador
        self.matrix_size = matrix_size  # Armazena o tamanho da matriz
        self.cell_size = cell_size  # Armazena o tamanho da célula
        self.color = (1.0, 0.0, 0.0)  # Define a cor do jogador como vermelho (RGB)
        self.jump_offset = 0  # Inicializa o offset de pulo do jogador como 0

    def draw(self):
        glColor3f(*self.color)  # Define a cor do jogador
        glBegin(GL_QUADS)  # Inicia o desenho de um quadrado
        glVertex2f(self.x * self.cell_size, self.y * self.cell_size)  # Define o vértice inferior esquerdo do quadrado
        glVertex2f((self.x + 1) * self.cell_size, self.y * self.cell_size)  # Define o vértice inferior direito do quadrado
        glVertex2f((self.x + 1) * self.cell_size, (self.y + 1) * self.cell_size)  # Define o vértice superior direito do quadrado
        glVertex2f(self.x * self.cell_size, (self.y + 1) * self.cell_size)  # Define o vértice superior esquerdo do quadrado
        glEnd()  # Finaliza o desenho do quadrado

    def move_left(self, boxes):
        prev_x = self.x  # Guarda a posição x anterior do jogador
        if self.x > 0:  # Verifica se o jogador não está na borda esquerda da matriz
            boxLeft = False  # Inicializa a variável para verificar a presença de uma caixa à esquerda
            for box in boxes:  # Itera sobre todas as caixas
                if self.x - 1 == box.x and self.y > box.y - 1 and self.y <= box.y:  # Verifica se há uma caixa diretamente à esquerda
                    boxLeft = box  # Armazena a caixa à esquerda
            if not boxLeft:  # Se não houver caixa à esquerda
                self.x -= 1  # Move o jogador uma posição para a esquerda
            else:  # Se houver uma caixa à esquerda
                mover = True  # Inicializa a variável para verificar se a caixa pode se mover
                for box in boxes:  # Itera sobre todas as caixas
                    if boxLeft.x == box.x + 1 and boxLeft.y == box.y:  # Verifica se há uma caixa à direita da caixa à esquerda
                        mover = False  # Define que a caixa não pode se mover
                if mover:  # Se a caixa pode se mover
                    if boxLeft.x > 0 and not (boxLeft.x - 1 == self.x - 1 and boxLeft.y == self.y):  # Verifica se a caixa não está na borda esquerda e não há colisão
                        boxLeft.x -= 1  # Move a caixa uma posição para a esquerda
                        self.x -= 1  # Move o jogador uma posição para a esquerda
        if prev_x != self.x:  # Se a posição do jogador mudou
            print(f"Moved left: Player({self.x}, {self.y}), Box({box.x}, {box.y})")  # Imprime a nova posição do jogador e da caixa

    def move_right(self, boxes):
        prev_x = self.x  # Guarda a posição x anterior do jogador
        if self.x < self.matrix_size - 1:  # Verifica se o jogador não está na borda direita da matriz
            boxRight = False  # Inicializa a variável para verificar a presença de uma caixa à direita
            for box in boxes:  # Itera sobre todas as caixas
                if self.x + 1 == box.x and self.y > box.y - 1 and self.y <= box.y :  # Verifica se há uma caixa diretamente à direita
                    boxRight = box  # Armazena a caixa à direita
            if not boxRight:  # Se não houver caixa à direita
                self.x += 1  # Move o jogador uma posição para a direita
            else:  # Se houver uma caixa à direita
                mover = True  # Inicializa a variável para verificar se a caixa pode se mover
                for box in boxes:  # Itera sobre todas as caixas
                    if boxRight.x == box.x - 1 and boxRight.y == box.y:  # Verifica se há uma caixa à esquerda da caixa à direita
                        mover = False  # Define que a caixa não pode se mover
                if mover:  # Se a caixa pode se mover
                    if boxRight.x < self.matrix_size - 1 and not (boxRight.x + 1 == self.x + 1 and boxRight.y == self.y):  # Verifica se a caixa não está na borda direita e não há colisão
                        boxRight.x += 1  # Move a caixa uma posição para a direita
                        self.x += 1  # Move o jogador uma posição para a direita
        if prev_x != self.x:  # Se a posição do jogador mudou
            print(f"Moved right: Player({self.x}, {self.y}), Box({box.x}, {box.y})")  # Imprime a nova posição do jogador e da caixa

    def jump(self, height):
        prev_y = self.y  # Guarda a posição y anterior do jogador
        #print(prev_y)  # Imprime a posição y anterior do jogador
        self.y -= height  # Ajusta a posição vertical do jogador
        if self.y < 0:  # Verifica se o jogador está abaixo do chão
            self.y = 0  # Impede que o jogador desça abaixo do chão
        #if prev_y != self.y:  # Se a posição do jogador mudou
        #    print(f"Jumping with height {height}, Player Y position: {self.y}")  # Imprime a nova posição y do jogador
