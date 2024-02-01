import numpy as np

from cube import is_point_between_planes

if __name__ == '__main__':
    def is_point_between_planes_wrapper(p, n1, n2):
        return is_point_between_planes(p, (n1, p / np.linalg.norm(n1)), (n2, p / np.linalg.norm(n2)))


    assert is_point_between_planes_wrapper(np.array([0.5, 0.5, 0.5]), np.array([1, 1, 1]), np.array([0.1, 0.1, 0.1]))
    assert is_point_between_planes_wrapper(np.array([0.2, 0.2, 0.2]), np.array([1, 1, 1]), np.array([0.1, 0.1, 0.1]))

    assert is_point_between_planes_wrapper(np.array([0, 0, 0]), np.array([1, 1, 1]), np.array([-1, -1, -1]))
    assert not is_point_between_planes_wrapper(np.array([2, 2, 1]), np.array([1, 1, 1]), np.array([-1, -1, -1]))
    assert not is_point_between_planes_wrapper(np.array([-2, -2, -1]), np.array([1, 1, 1]), np.array([-1, -1, -1]))

    assert is_point_between_planes_wrapper(
        np.array([-1.72881461, -0.0690164, 0.08022954]),
        np.array([-1.72881461, -0.0690164, 0.08022954]),
        np.array([-1.18287315, -0.04722174, 0.05489389])
    )
    assert not is_point_between_planes_wrapper(
        np.array([0, 0, 0]), np.array([-1.72881461, -0.0690164, 0.08022954]),
        np.array([-1.18287315, -0.04722174, 0.05489389])
    )
