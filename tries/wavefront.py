import numpy as np
from OpenGL.raw.GLU import gluPerspective
from pywavefront import Wavefront
from OpenGL.GL import *
from OpenGL.GLUT import *

# Function to load texture from a numpy array
def load_texture(texture_data):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture_data.shape[1], texture_data.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    return texture

# Function to create a cube with different textures for each face
def create_textured_cube(textures):
    cube = Wavefront("cube.obj")
    cube_textures = textures

    for face, texture in zip(cube.mesh_list[0].faces, cube_textures):
        face.material = "cube_material_" + str(cube_textures.index(texture))
        face.texture = load_texture(texture)

    return cube

# Function to render the cube
def render_cube(cube):
    glBegin(GL_QUADS)
    for face in cube.mesh_list[0].faces:
        for vertex, texture_coordinate in zip(face.vertices, face.texture_vertices):
            glTexCoord2f(*texture_coordinate)
            glVertex3f(*cube.mesh_list[0].vertices[vertex])
    glEnd()

# Function to generate image with a solid color
def generate_image(size, color):
    return np.ones((size, size, 3), dtype=np.uint8) * color

# OpenGL callback functions
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -5)

    glBindTexture(GL_TEXTURE_2D, 0)
    glEnable(GL_TEXTURE_2D)

    render_cube(cube)

    glutSwapBuffers()

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (width / height), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Textured Cube")

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)

    # Generate textures
    textures = [
        generate_image(100, [255, 255, 255]),
        generate_image(100, [0, 0, 0]),
        generate_image(100, [100, 100, 100]),
        generate_image(100, [150, 150, 150]),
        generate_image(100, [200, 200, 200]),
        generate_image(100, [50, 50, 50])
    ]

    global cube
    cube = create_textured_cube(textures)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)

    glutMainLoop()

if __name__ == "__main__":
    main()
