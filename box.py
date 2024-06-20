from OpenGL.GL import *

class Box:
    def __init__(self, x, y, cell_size):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        self.color = (0.0, 1.0, 0.0)

    def draw(self):
        glColor3f(*self.color)
        glBegin(GL_QUADS)
        glVertex2f(self.x * self.cell_size, self.y * self.cell_size)
        glVertex2f((self.x + 1) * self.cell_size, self.y * self.cell_size)
        glVertex2f((self.x + 1) * self.cell_size, (self.y + 1) * self.cell_size)
        glVertex2f(self.x * self.cell_size, (self.y + 1) * self.cell_size)
        glEnd()
