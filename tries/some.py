import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import glfw

class CubeApp:
    def __init__(self):
        self.width, self.height = 800, 600
        self.cube_size = 1.0
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.generate_images()

        # Initialize GLFW
        if not glfw.init():
            return

        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(self.width, self.height, "OpenGL Cube", None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        # Set up key callback
        glfw.set_key_callback(self.window, self.key_callback)

        # Set up off-screen rendering context
        self.init_offscreen_rendering()

    def generate_images(self):
        self.front_image = self.generate_image(100, 255)
        self.back_image = self.generate_image(100, 0)
        self.left_image = self.generate_image(100, 100)
        self.right_image = self.generate_image(100, 150)
        self.top_image = self.generate_image(100, 200)
        self.bottom_image = self.generate_image(100, 50)

    def generate_image(self, size, color):
        return np.ones((size, size, 3), dtype=np.uint8) * color

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)

    def init_offscreen_rendering(self):
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        self.render_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.render_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.width, self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.render_texture, 0)

        self.depth_renderbuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depth_renderbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, self.width, self.height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, self.depth_renderbuffer)

        glBindFramebuffer(GL_FRAMEBUFFER, 0)

    def draw_cube(self):
        # Render to the off-screen framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / self.height, 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5)
        glRotatef(self.angle_x, 1, 0, 0)
        glRotatef(self.angle_y, 0, 1, 0)
        glRotatef(self.angle_z, 0, 0, 1)

        self.draw_face(self.front_image, self.cube_size / 2, 0, 0, self.cube_size / 2, self.cube_size / 2, self.cube_size / 2)
        self.draw_face(self.back_image, -self.cube_size / 2, 0, 0, -self.cube_size / 2, self.cube_size / 2, self.cube_size / 2)
        self.draw_face(self.left_image, 0, -self.cube_size / 2, 0, -self.cube_size / 2, 0, self.cube_size / 2)
        self.draw_face(self.right_image, 0, self.cube_size / 2, 0, self.cube_size / 2, 0, self.cube_size / 2)
        self.draw_face(self.top_image, 0, 0, self.cube_size / 2, self.cube_size / 2, self.cube_size / 2, 0)
        self.draw_face(self.bottom_image, 0, 0, -self.cube_size / 2, -self.cube_size / 2, -self.cube_size / 2, 0)

        # Read pixels from the framebuffer to the CPU
        glReadBuffer(GL_COLOR_ATTACHMENT0)
        pixels = glReadPixels(0, 0, self.width, self.height, GL_RGB, GL_UNSIGNED_BYTE)

        # Create an OpenCV image from the pixel data
        opencv_image = np.frombuffer(pixels, dtype=np.uint8).reshape((self.height, self.width, 3))[::-1, :]

        # Bind the default framebuffer
        glBindFramebuffer(GL_FRAMEBUFFER, 0)

        # Display the OpenCV image
        cv2.imshow("Rendered Cube", opencv_image)
        cv2.waitKey(1)

    def draw_face(self, image, x1, y1, z1, x2, y2, z2):
        glEnable(GL_TEXTURE_2D)
        texture = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, texture.shape[1], texture.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, texture)

        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(1, 0)
        glVertex3f(x2, y1, z1)
        glTexCoord2f(1, 1)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(0, 1)
        glVertex3f(x1, y2, z2)
        glEnd()

        glDeleteTextures(1, [texture_id])
        glDisable(GL_TEXTURE_2D)

    def run(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)

        while not glfw.window_should_close(self.window):
            self.angle_x += 1
            self.angle_y += 1
            self.angle_z += 1

            self.draw_cube()

        glfw.terminate()

if __name__ == "__main__":
    cube_app = CubeApp()
    cube_app.run()
