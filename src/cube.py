import cProfile
import math

import numpy as np
from functools import lru_cache

from src.draw_cube import loop_check, draw_cube, calculate_downward_vector, draw_vector, frame_update, init

# most advanced version
# look into sand animation https://gist.github.com/witnessmenow/29192dd0e5dda61f50900e3422cedeab
# ?https://en.wikipedia.org/wiki/Navier%E2%80%93Stokes_equations

VISUALIZE = True

CUBE_SIZE = 2  # fixed to 2
GRID_SIZE = 8
RADIUS = math.sqrt(3) * CUBE_SIZE / 2

value_span_in_radius = np.linspace(-RADIUS, RADIUS, 20)

max_coord = CUBE_SIZE // 2
coord_vals = np.linspace(-max_coord, max_coord, GRID_SIZE)


def pixel_to_coord(size, side, x, y):
    match side:
        case 0:  # top
            return [coord_vals[y], max_coord, coord_vals[x]]
        case 1:  # bottom
            return [coord_vals[y], -max_coord, coord_vals[x]]
        case 2:  # back
            return [coord_vals[y], -coord_vals[size - x - max_coord], -max_coord]
        case 3:  # front
            return [coord_vals[size - y - max_coord], coord_vals[x], max_coord]
        case 4:  # left
            return [-max_coord, coord_vals[x], coord_vals[size - y - max_coord]]
        case 5:  # right
            return [max_coord, -coord_vals[size - x - max_coord], -coord_vals[y]]
        case _:
            raise ValueError()


def color_cube_squares(shape, direction):
    desired_sphere_volume = 11

    # add logic to convert from sensor values to vector
    directional_vector = direction

    second_plane = get_second_plane_of_segment(directional_vector, desired_sphere_volume)

    # cube is a 3d array of sides of grids of led-pixels (6 sides with square grids)
    cube = np.zeros(shape)

    plane1 = (directional_vector, np.linalg.norm(directional_vector) ** 2)
    plane2 = (second_plane, np.linalg.norm(second_plane))
    for side in range(shape[0]):
        for y in range(shape[1]):
            for x in range(shape[2]):
                point_to_check = pixel_to_coord(shape[1], side, x, y)
                is_between_planes = is_point_between_planes(np.array(point_to_check), plane1, plane2)
                cube[side, x, y] = int(is_between_planes)
    return cube


@lru_cache(maxsize=30)
def calculate_cap_volume(radius, height):
    #                    --------------
    #                ---                ---
    #            ----                      ----
    #         --    Volume of this part here    --
    #      -────────────────────────────────────────-
    #    -     .                                     -
    #   -      .                                      -
    #  -       . height                                -
    # -        .                                        -
    # -        .              X...........radius........-
    # -─────────────────────────────────────────────────-
    height = abs(height)
    if height >= radius:
        return (math.pi * radius ** 3 * 4) / 6  # half sphere
    else:
        return (1 / 3) * math.pi * height ** 2 * (3 * radius - height)


def get_second_plane_of_segment(first_plane_normal, target_volume):
    dist_for_first_cap = np.linalg.norm(first_plane_normal)
    volume_of_first = calculate_cap_volume(RADIUS, dist_for_first_cap)

    def get_volume_diff(x):
        # depending on a: both planes are on different sides of the sphere or b: they are on the same side
        if np.sign(dist_for_first_cap) != np.sign(x):
            volume_of_segment = calculate_cap_volume(RADIUS, x) + volume_of_first
        else:
            volume_of_segment = calculate_cap_volume(RADIUS, x) - volume_of_first
        return abs(target_volume - abs(volume_of_segment))

    fitting_distance_from_middle = min([val for val in value_span_in_radius], key=get_volume_diff)
    return (first_plane_normal / dist_for_first_cap) * fitting_distance_from_middle


def distance_point_to_plane(point, plane_normal):
    return np.dot(point - plane_normal, plane_normal) / np.linalg.norm(plane_normal)


def plane_direction(point, plane_normal):
    vector_to_plane = plane_normal - point
    return vector_to_plane + np.dot(vector_to_plane, plane_normal) * plane_normal


def closest_point_on_plane(point, plane):
    plane_normal, squared_plane_length = plane
    vector_to_point = point - plane_normal
    projection = vector_to_point - np.dot(vector_to_point, plane_normal) * plane_normal / squared_plane_length
    return plane_normal + projection


def in_between(x1, x2, x):
    return x1 <= x <= x2 or x1 >= x >= x2


def transform_z(point, x_angle, z_angle):
    x, y, z = point
    return z * math.cos(x_angle) + math.sin(x_angle) * (
            x * math.sin(z_angle) + y * math.cos(z_angle)
    )


def is_point_between_planes(point, plane1, plane2):
    # dist_to_plane1 = np.dot(point, plane1[0])
    # dist_to_plane2 = np.dot(point, plane2[0])
    # k = abs(dist_to_plane1 - dist_to_plane2)
    # c = abs(np.linalg.norm(plane1[0]) - np.linalg.norm(plane2[0]))
    # print(k)
    # print(c)
    # return k <= c
    #
    # print("d", dist_to_plane1, dist_to_plane2)
    # a = np.sign(dist_to_plane1 * np.sign(plane1[0])[0])
    # b = np.sign(dist_to_plane2 * np.sign(plane2[0])[0])
    # print(a)
    # print(b)
    # return a == b
    #
    # v, norm1 = plane1
    # x1, y1, z1 = 0 if norm1 == 0. else v / math.sqrt(norm1)
    # *_, norm2 = plane2
    # x_angle = 0 if y1 == 0 else math.atan(z1 / y1)
    # z_angle = 0 if x1 == 0 else math.atan(y1 / x1)
    #
    # transform = lambda p: transform_z(p, x_angle, z_angle)
    # z_point = transform(point)
    # z_point_1 = transform(plane1[0])
    # z_point_2 = transform(plane2[0])
    # print(x_angle, z_angle)
    # print(z_point, z_point_1, z_point_2)
    # print(z_point_1 <= z_point <= z_point_2 or z_point_1 >= z_point >= z_point_2)
    # return z_point_1 <= z_point <= z_point_2 or z_point_1 >= z_point >= z_point_2

    point_on_plane1 = closest_point_on_plane(point, plane1)
    point_on_plane2 = closest_point_on_plane(point, plane2)
    for i in range(3):  # Check along each axis (x, y, z)
        if not in_between(point_on_plane1[i], point_on_plane2[i], point[i]):
            return False
    return True


def limit_vector(v, length):
    v_length = np.linalg.norm(v)
    return v if v_length <= length else v * (length / v_length)


def main():
    cube = np.array([
        np.random.randint(2, size=(GRID_SIZE, GRID_SIZE), dtype=np.uint8)
        for _ in range(6)
    ])

    init()
    while True:
        loop_check()
        v = calculate_downward_vector()
        v = limit_vector(v, RADIUS)

        draw_cube(cube)
        draw_vector(v)

        cube = color_cube_squares(cube.shape, v)
        frame_update()


def profile(func):
    profiler = cProfile.Profile()
    profiler.enable()
    try:
        func()
    except Exception as e:
        print(e)

    profiler.disable()
    profiler.dump_stats("profile_data.prof")


if __name__ == '__main__':
    # main()
    profile(main)
