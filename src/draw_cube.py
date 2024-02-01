import pygame
from pygame.locals import *
from OpenGL.raw.GLU import gluPerspective
from OpenGL.GL import *
import numpy as np


def draw_pixel_grid(grid, side):
    size = len(grid)
    for i in range(size):
        for j in range(size):
            color = grid[j][i]  # 1 if (i + j) % 2 == 0 else 0  # Alternate black and white
            glColor3f(color, side / 6, 0)
            glBegin(GL_QUADS)
            glVertex3f(i - size / 2, j - size / 2, 0.0)
            glVertex3f(i + 1 - size / 2, j - size / 2, 0.0)
            glVertex3f(i + 1 - size / 2, j + 1 - size / 2, 0.0)
            glVertex3f(i - size / 2, j + 1 - size / 2, 0.0)
            glEnd()


def draw_grid_cube(cube):
    length = len(cube[0])
    for i, face in enumerate(cube):
        glPushMatrix()
        if i == 0:  # Top face
            glRotatef(90, 1, 0, 0)
            glTranslatef(0, 0, -length / 2)
        elif i == 1:  # Bottom face
            glRotatef(90, 1, 0, 0)
            glTranslatef(0, 0, length / 2)
        elif i == 2:  # Back face
            glRotatef(0, 0, 0, 0)
            glTranslatef(0, 0, -length / 2)
        elif i == 3:  # Front face
            glRotatef(180, 0, 1, 0)
            glTranslatef(0, 0, -length / 2)
        elif i == 4:  # Left face
            glRotatef(90, 0, 1, 0)
            glTranslatef(0, 0, -length / 2)
        elif i == 5:  # Right face
            glRotatef(90, 0, 1, 0)
            glTranslatef(0, 0, length / 2)
        draw_pixel_grid(face, i)
        glPopMatrix()


def rotate_scene(angle_x, angle_y, angle_z):
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)


def draw_vector(endpoint):
    glBegin(GL_LINES)
    glVertex3f(0, 0, 0)  # Start from the center of the cube
    glVertex3fv([x * 5 for x in endpoint])  # Endpoint of the vector
    glEnd()


def draw_plane(normal_vector, size=10):
    dist = np.linalg.norm(normal_vector)
    glBegin(GL_QUADS)
    glNormal3fv(normal_vector)
    glVertex3f(-size, -size, dist)
    glVertex3f(size, -size, dist)
    glVertex3f(size, size, dist)
    glVertex3f(-size, size, dist)
    glEnd()


def calculate_downward_vector():
    def get_modelview_matrix():
        modelview_matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        return np.array(modelview_matrix)

    # Create a downward vector in world space
    downward_vector_world = np.array([0, -1, 0, 0])
    return np.dot(get_modelview_matrix(), downward_vector_world)[:3]


def init():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -30)


def draw_cube(cube):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    rotate_scene(*[0.5] * 3)
    draw_grid_cube(cube)


def loop_check():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return


def frame_update():
    pygame.display.flip()
    pygame.time.wait(10)
