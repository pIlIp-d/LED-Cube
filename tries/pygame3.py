import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Pygame setup
screen = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Rotating 3D Cube")
clock = pygame.time.Clock()

glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0.0, 0.0, -5)

# Set up cube vertices
vertices = [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

# Texture coordinates for each face
tex_coords = [
    [1, 0, 1, 1, 0, 1, 0, 0],  # Right
    [1, 0, 1, 1, 0, 1, 0, 0],  # Left
    [1, 0, 1, 1, 0, 1, 0, 0],  # Top
    [1, 0, 1, 1, 0, 1, 0, 0],  # Bottom
    [1, 0, 1, 1, 0, 1, 0, 0],  # Front
    [1, 0, 1, 1, 0, 1, 0, 0]   # Back
]

# Load textures for each face
textures = [
    pygame.image.load('texture_right.png'),
    pygame.image.load('texture_left.png'),
    pygame.image.load('texture_top.png'),
    pygame.image.load('texture_bottom.png'),
    pygame.image.load('texture_front.png'),
    pygame.image.load('texture_back.png')
]

for i in range(len(textures)):
    textures[i] = pygame.image.tostring(textures[i], 'RGBA', 1)
    width, height = textures[i].get_width(), textures[i].get_height()
    textures[i] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textures[i])
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textures[i])
    glBindTexture(GL_TEXTURE_2D, 0)

# Initial rotation angles
rotation_angles = [0, 0, 0]

def draw_cube():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0, 0, -5)
    glRotatef(rotation_angles[0], 1, 0, 0)
    glRotatef(rotation_angles[1], 0, 1, 0)
    glRotatef(rotation_angles[2], 0, 0, 1)

    for i in range(6):
        glBindTexture(GL_TEXTURE_2D, textures[i])

        glBegin(GL_QUADS)
        for j in range(4):
            glTexCoord2fv(tex_coords[i][j * 2: j * 2 + 2])
            glVertex3fv(vertices[(j + 1) % 4 + i * 2])
        glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)

    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation angles based on user input or any other logic
    rotation_angles[0] += 1  # Rotate around X-axis
    rotation_angles[1] += 1  # Rotate around Y-axis
    rotation_angles[2] += 1  # Rotate around Z-axis

    draw_cube()

    clock.tick(FPS)

pygame.quit()
sys.exit()


if __name__ == '__main__':
    pass