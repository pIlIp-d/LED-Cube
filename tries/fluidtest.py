import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
grid_size = 30
time_steps = 50
dt = 0.1
acceleration_vector = np.array([1, 0])  # Change this as needed
cube_size = 8

# Initialize density and velocity fields
density = np.zeros((grid_size, grid_size))
velocity = np.zeros((grid_size, grid_size, 2))

# Initialize cube position
cube_position = np.array([grid_size // 2, grid_size // 2])

def apply_acceleration(velocity, acceleration):
    velocity += acceleration * dt

def advect(field, velocity):
    for i in range(grid_size):
        for j in range(grid_size):
            x, y = i - velocity[i, j, 0], j - velocity[i, j, 1]
            x = max(0, min(grid_size - 1, x))
            y = max(0, min(grid_size - 1, y))
            field[i, j] = density[int(x), int(y)]

def diffuse(field, diffusion_rate):
    # Implement simple diffusion
    for _ in range(5):
        field[1:-1, 1:-1] = (field[1:-1, 1:-1] + diffusion_rate * (
            field[:-2, 1:-1] + field[2:, 1:-1] +
            field[1:-1, :-2] + field[1:-1, 2:]
        )) / (1 + 4 * diffusion_rate)

def move_cube():
    # Move the cube in a sinusoidal pattern
    global cube_position
    cube_position[0] += np.sin(dt) * 2
    cube_position[1] += np.cos(dt) * 2

def update_cube_density():
    # Update the density within the cube
    density[
        int(cube_position[0] - cube_size // 2):int(cube_position[0] + cube_size // 2),
        int(cube_position[1] - cube_size // 2):int(cube_position[1] + cube_size // 2)
    ] += 1

def enforce_boundary_conditions(field):
    # Simple reflecting boundaries
    field[:, 0] = field[:, 1]
    field[:, -1] = field[:, -2]
    field[0, :] = field[1, :]
    field[-1, :] = field[-2, :]

# Main simulation loop
for _ in range(time_steps):
    apply_acceleration(velocity, acceleration_vector)
    move_cube()
    update_cube_density()
    advect(density, velocity)
    diffuse(density, diffusion_rate=0.1)
    enforce_boundary_conditions(density)

# Visualization with highlighted cube region
plt.imshow(density, cmap='viridis', origin='lower', extent=[0, grid_size, 0, grid_size])
plt.colorbar()
plt.title('Fluid Simulation with Moving Cube')
plt.plot(
    [cube_position[1] - cube_size // 2, cube_position[1] + cube_size // 2, cube_position[1] + cube_size // 2, cube_position[1] - cube_size // 2, cube_position[1] - cube_size // 2],
    [cube_position[0] - cube_size // 2, cube_position[0] - cube_size // 2, cube_position[0] + cube_size // 2, cube_position[0] + cube_size // 2, cube_position[0] - cube_size // 2],
    color='red', linewidth=2
)
plt.show()
