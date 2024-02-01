import cv2
import numpy as np

SIZE = 8
IMAGE_SIZE = 100

cx, cy, fx, fy = IMAGE_SIZE // 2, IMAGE_SIZE // 2, 50, 50

cam = [
    [cx, 0, fx],
    [0, cy, fy],
    [0, 0, 1]
]

defaut_cube = [
    [],
    [],
]


def project_image(img_path, x1, x2, x3, x4):
    # Load the image
    img = cv2.imread(img_path)

    # Define the source and destination points
    src_points = np.float32([[0, 0], [img.shape[1] - 1, 0], [0, img.shape[0] - 1], [img.shape[1] - 1, img.shape[0] - 1]])
    dst_points = np.float32([x1, x2, x3, x4])

    # Get the perspective transformation matrix
    matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    # Apply the perspective transformation
    return cv2.warpPerspective(img, matrix, (img.shape[1], img.shape[0]))


def generate_colored_image(color, size=(IMAGE_SIZE, IMAGE_SIZE)):
    return np.full((size[0], size[1], 3), color, dtype=np.uint8)


def render_cube(colors, rotation_angles):
    cube_size = max(color.shape[0] for color in colors)
    canvas = np.zeros((cube_size * 3, cube_size * 4, 3), dtype=np.uint8)

    # Arrange the colored images on the canvas
    canvas[cube_size:cube_size * 2, cube_size:cube_size * 2] = colors[0]  # Front
    canvas[:cube_size, cube_size:cube_size * 2] = cv2.rotate(colors[1], cv2.ROTATE_180)  # Top
    canvas[cube_size * 2:, cube_size:cube_size * 2] = cv2.rotate(colors[2], cv2.ROTATE_180)  # Bottom
    canvas[cube_size:cube_size * 2, cube_size * 2:] = cv2.rotate(colors[3], cv2.ROTATE_90_CLOCKWISE)  # Left
    canvas[cube_size:cube_size * 2, :cube_size] = cv2.rotate(colors[4], cv2.ROTATE_90_COUNTERCLOCKWISE)  # Right
    canvas[cube_size:cube_size * 2, cube_size * 3:] = colors[5]  # Back

    # Apply rotation based on slider values
    rotation_matrix_x = cv2.getRotationMatrix2D((cube_size * 2, cube_size), rotation_angles[0], 1)
    rotation_matrix_y = cv2.getRotationMatrix2D((cube_size * 2, cube_size), rotation_angles[1], 1)
    rotation_matrix_z = cv2.getRotationMatrix2D((cube_size * 2, cube_size), rotation_angles[2], 1)

    canvas = cv2.warpAffine(canvas, rotation_matrix_x, (canvas.shape[1], canvas.shape[0]))
    canvas = cv2.warpAffine(canvas, rotation_matrix_y, (canvas.shape[1], canvas.shape[0]))
    canvas = cv2.warpAffine(canvas, rotation_matrix_z, (canvas.shape[1], canvas.shape[0]))

    cv2.imshow('3D Cube', canvas)
    cv2.waitKey(1)  # Adjust the delay time if needed


# Callback function for trackbars
def on_trackbar_change(value, slider_index):
    rotation_angles[slider_index] = value
    render_cube(colors, rotation_angles)


# Initialize rotation angles and colors
rotation_angles = [0, 0, 0]
colors = [generate_colored_image((255, 0, 0)),  # Red for Front
          generate_colored_image((0, 255, 0)),  # Green for Top
          generate_colored_image((0, 0, 255)),  # Blue for Bottom
          generate_colored_image((255, 255, 0)),  # Yellow for Left
          generate_colored_image((0, 255, 255)),  # Cyan for Right
          generate_colored_image((255, 0, 255))]  # Magenta for Back

cv2.namedWindow('3D Cube')
# Create trackbars for rotation angles
cv2.createTrackbar('X Rotation', '3D Cube', rotation_angles[0], 360, lambda x: on_trackbar_change(x, 0))
cv2.createTrackbar('Y Rotation', '3D Cube', rotation_angles[1], 360, lambda x: on_trackbar_change(x, 1))
cv2.createTrackbar('Z Rotation', '3D Cube', rotation_angles[2], 360, lambda x: on_trackbar_change(x, 2))


def main():
    cube = [range(0, SIZE) for _ in range(0, SIZE)]

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # Press 'Esc' to exit
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
