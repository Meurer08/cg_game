from OpenGL.GL import *

class Player:
    def __init__(self, matrix_size, cell_size):
        self.x = matrix_size // 2
        self.y = matrix_size - 1
        self.ground_y = self.y  # Guarda a posição do chão
        self.matrix_size = matrix_size
        self.cell_size = cell_size
        self.color = (1.0, 0.0, 0.0)
        self.jump_offset = 0

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(self.x * self.cell_size, self.y * self.cell_size)
        glVertex2f((self.x + 1) * self.cell_size, self.y * self.cell_size)
        glVertex2f((self.x + 1) * self.cell_size, (self.y + 1) * self.cell_size)
        glVertex2f(self.x * self.cell_size, (self.y + 1) * self.cell_size)
        glEnd()

    def move_left(self, boxes):
        prev_x = self.x
        if self.x > 0:
            boxLeft = False
            for box in boxes:
                if (self.x - 1 == box.x and self.y == box.y):
                    boxLeft = box
            if not (boxLeft):
                self.x -= 1
            else:
                mover = True
                for box in boxes:
                    if (boxLeft.x == box.x + 1 and boxLeft.y == box.y):
                        mover = False
                if(mover):
                    if boxLeft.x > 0 and not (boxLeft.x - 1 == self.x - 1 and boxLeft.y == self.y):
                        boxLeft.x -= 1
                        self.x -= 1
        if prev_x != self.x:
            print(f"Moved left: Player({self.x}, {self.y}), Box({box.x}, {box.y})")

    #adaptando esse
    def move_right(self, boxes):
        prev_x = self.x
        if self.x < self.matrix_size - 1:
            boxRight = False
            for box in boxes:
                if (self.x + 1 == box.x and self.y == box.y):
                    boxRight = box
            if not (boxRight):
                self.x += 1
            else:
                mover = True
                for box in boxes:
                    if (boxRight.x == box.x - 1 and boxRight.y == box.y):
                        mover = False
                if(mover):
                    if boxRight.x < self.matrix_size - 1 and not (boxRight.x + 1 == self.x + 1 and boxRight.y == self.y):
                        boxRight.x += 1
                        self.x += 1
        if prev_x != self.x:
            print(f"Moved right: Player({self.x}, {self.y}), Box({box.x}, {box.y})")

    def jump(self, height):
        prev_y = self.y
        print(prev_y)
        self.y -= height  # Ajuste a posição vertical do jogador
        if self.y < 0:
            self.y = 0  # Impede que o jogador desça abaixo do chão
        if prev_y != self.y:
            print(f"Jumping with height {height}, Player Y position: {self.y}")
