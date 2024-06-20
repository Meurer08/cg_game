from OpenGL.GL import *


def draw_matrix(matrix_size, cell_size):
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    for i in range(matrix_size + 1):
        glVertex2f(i * cell_size, 0)
        glVertex2f(i * cell_size, matrix_size * cell_size)
        glVertex2f(0, i * cell_size)
        glVertex2f(matrix_size * cell_size, i * cell_size)
    glEnd()
