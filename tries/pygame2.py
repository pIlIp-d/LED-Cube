import pygame
import sys
import numpy as np
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

# Randomly generated textures for each face
cube_faces = [
    np.random.randint(2, size=(8, 8), dtype=np.uint8),
    np.random.randint(2, size=(8, 8), dtype=np.uint8),
    np.random.randint(2, size=(8, 8), dtype=np.uint8),
    np.random.randint(2, size=(8, 8), dtype=np.uint8),
    np.random.randint(2, size=(8, 8), dtype=np.uint8),
    np.random.randint(2, size=(8, 8), dtype=np.uint8)
]

textures = []
for face in cube_faces:
    face_color = np.stack([face, face, face, np.ones_like(face) * 255], axis=-1)
    texture = pygame.image.frombuffer(face_color.tobytes(), (8, 8), 'RGBA')
    textures.append(pygame.image.tostring(texture, 'RGBA', 1))
    width, height = texture.get_width(), texture.get_height()
    textures[-1] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textures[-1])
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textures[-1])
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
            vertex_index = (j + 1) % 4
            glVertex3fv(vertices[vertex_index + i * 2])
            glTexCoord2fv(tex_coords[i][j * 2: j * 2 + 2])
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