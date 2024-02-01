import pygame
from pygame.locals import DOUBLEBUF, OPENGL, QUIT

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def draw_slider(surface, rect, value, value_range):
    pygame.draw.rect(surface, (200, 200, 200), rect)  # Draw the slider background
    slider_width = int((value - value_range[0]) / (value_range[1] - value_range[0]) * rect.width)
    pygame.draw.rect(surface, (0, 0, 255), (rect.left, rect.top, slider_width, rect.height))  # Draw the slider knob

def setup():
    # Set the dimensions of the cube
    cube_size = 1.0

    # Set up the display
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Cube")

    # Set up the OpenGL perspective
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)

    # Create sliders for rotation angles
    slider_x_rect = pygame.Rect(10, 10, 200, 20)
    slider_y_rect = pygame.Rect(10, 40, 200, 20)
    slider_z_rect = pygame.Rect(10, 70, 200, 20)

    return screen, cube_size, slider_x_rect, slider_y_rect, slider_z_rect

def main():
    screen, cube_size, slider_x_rect, slider_y_rect, slider_z_rect = setup()

    # Main loop
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Get current values of sliders
        angle_x = (slider_x_rect.width / 200) * 360  # Map slider position to angle
        angle_y = (slider_y_rect.width / 200) * 360
        angle_z = (slider_z_rect.width / 200) * 360

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()
        glRotatef(angle_x, 1, 0, 0)
        glRotatef(angle_y, 0, 1, 0)
        glRotatef(angle_z, 0, 0, 1)

        # Draw the cube
        glBegin(GL_QUADS)
        glColor3f(1, 1, 1)  # Front face
        glVertex3f(-cube_size / 2, -cube_size / 2, cube_size / 2)
        glVertex3f(cube_size / 2, -cube_size / 2, cube_size / 2)
        glVertex3f(cube_size / 2, cube_size / 2, cube_size / 2)
        glVertex3f(-cube_size / 2, cube_size / 2, cube_size / 2)
        glEnd()

        glPopMatrix()

        # Draw sliders
        draw_slider(screen, slider_x_rect, angle_x, (0, 360))
        draw_slider(screen, slider_y_rect, angle_y, (0, 360))
        draw_slider(screen, slider_z_rect, angle_z, (0, 360))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
