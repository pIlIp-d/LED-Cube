import numpy as np
import pygame
from OpenGL.raw.GLU import gluPerspective
from pygame.locals import *
from OpenGL.GL import *
# working sample

# Function to draw a grid of black and white pixels
def draw_pixel_grid(grid):
    size = len(grid)
    for i in range(size):
        for j in range(size):
            color = grid[j][i]  # 1 if (i + j) % 2 == 0 else 0  # Alternate black and white
            glColor3f(color, color, color)
            glBegin(GL_QUADS)
            glVertex3f(i - size / 2, j - size / 2, 0.0)
            glVertex3f(i + 1 - size / 2, j - size / 2, 0.0)
            glVertex3f(i + 1 - size / 2, j + 1 - size / 2, 0.0)
            glVertex3f(i - size / 2, j + 1 - size / 2, 0.0)
            glEnd()


# Function to draw a 3D cube of grids
def draw_grid_cube(cube):
    for i, face in enumerate(cube):
        glPushMatrix()
        if i == 0:  # Top face
            glRotatef(90, 1, 0, 0)
            glTranslatef(0, 0, -len(face) / 2)
            draw_pixel_grid(face)
        elif i == 1:  # Bottom face
            glRotatef(90, 1, 0, 0)
            glTranslatef(0, 0, len(face) / 2)
            draw_pixel_grid(face)
        elif i == 2:  # Front face
            glTranslatef(0, 0, -len(face) / 2)
            draw_pixel_grid(face)
        elif i == 3:  # Back face
            glRotatef(180, 0, 1, 0)
            glTranslatef(0, 0, -len(face) / 2)
            draw_pixel_grid(face)
        elif i == 4:  # Left face
            glRotatef(90, 0, 1, 0)
            glTranslatef(0, 0, -len(face) / 2)
            draw_pixel_grid(face)
        elif i == 5:  # Right face
            glRotatef(90, 0, 1, 0)
            glTranslatef(0, 0, len(face) / 2)
            draw_pixel_grid(face)

        glPopMatrix()


# Function to handle rotations
def rotate_scene(angle_x, angle_y, angle_z):
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)


# Main function
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -25)

    grid_size = 8

    cube = [
        np.random.randint(2, size=(grid_size, grid_size), dtype=np.uint8)
        for _ in range(6)
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        rotate_scene(*[0.5]*3)

        draw_grid_cube(cube)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == '__main__':
    main()
