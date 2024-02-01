import cv2
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import glfw
import imgui
from imgui.integrations.glfw import GlfwRenderer

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
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)

        # Initialize imgui
        imgui.create_context()
        self.imgui_renderer = GlfwRenderer(self.window)

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

    def mouse_callback(self, window, xpos, ypos):
        sensitivity = 0.1
        xpos *= sensitivity
        ypos *= sensitivity

        self.angle_y += xpos
        self.angle_x += ypos

        # Limit the rotation angle for X to avoid flipping
        self.angle_x = max(min(self.angle_x, 90), -90)

    def draw_cube(self):
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

        # Render ImGui UI directly on the main OpenGL window
        imgui.new_frame()
        imgui.text("Rotation Angles:")
        changed_x, self.angle_x = imgui.slider_float("X", self.angle_x, -180, 180)
        changed_y, self.angle_y = imgui.slider_float("Y", self.angle_y, -180, 180)
        changed_z, self.angle_z = imgui.slider_float("Z", self.angle_z, -180, 180)

        # Update the rotation angles only if the slider value has changed
        if changed_x or changed_y or changed_z:
            self.angle_x = max(min(self.angle_x, 90), -90)
        imgui.render()
        self.imgui_renderer.render(imgui.get_draw_data())

        glfw.swap_buffers(self.window)
        glfw.poll_events()

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
            self.draw_cube()

        glfw.terminate()

if __name__ == "__main__":
    cube_app = CubeApp()
    cube_app.run()
