from util import plt_function
import numpy as np
from track_shape import generate_track


# Defining constants:

x, dx, y, dy, d2y, x_fixed_points, y_fixed_points = generate_track(
    horizontal_distance=200,
    n_screws=8,
    dx=1,
    y_fixed_points=np.array(
        [300.0, 259.0, 189.0, 198.0, 266.0, 281.0, 226.0, 219.0]
    )
)

c = 2/5  # For a sphere
mass = 31  # g
radius = 11  # mm
moment_of_inertia = c*mass*radius**2
# mm/s**2 (In Oslo: 9825) (Standard: 9806.65) # The difference is negligible
g = 9825
static_friction_coeficcient = 0.4  # max value for friction/normal_force


# Make the assumption that the radius of the ball is much less than the radius of curvature,
# so that the shape of the center of mass follows the same path as the track, only shifted upwards

# Defining functions:

def velocity(x: int) -> np.float64:
    # The length of the velocity vector
    # Tangential to the track
    return np.sqrt(2*g*(y[0]-y[x])/(1+c))


def curvature(x: int) -> np.float64:
    # This is the inverse of the radius of curvature
    return d2y[x]/(np.power(1+dy[x]**2, 1.5))


def centripetal_acceleration(x: int) -> np.float64:
    # Orthogonal to the track
    return curvature(x)*velocity(x)**2


def inclitation_angle(x: int) -> np.float64:
    # Normally referred to as beta
    return np.arctan(dy[x])


def normal_force(x: int) -> np.float64:
    return mass*(g*np.cos(inclitation_angle(x)) + centripetal_acceleration(x))


def friction(x: int) -> np.float64:
    return (c/(c+1))*mass*g*np.sin(inclitation_angle(x))


def dt(x: int) -> np.float64:
    assert np.min(x) > 0
    return 2*dx/(velocity(x-1)*np.cos(inclitation_angle(x-1)) + velocity(x)*np.cos(inclitation_angle(x)))


# max_time = 0
# y_fixed_points_extreme = []
# for _ in range(10000):
#     x, dx, y, dy, d2y, x_fixed_points, y_fixed_points = generate_track(
#         horizontal_distance=200,
#         n_screws=8,
#         dx=1,
#         y_fixed_points=None
#     )
#     time = np.sum(dt(x[1:]))
#     if max_time < time:
#         max_time = time
#         y_fixed_points_extreme = y_fixed_points

# print(y_fixed_points_extreme)
# x, dx, y, dy, d2y, x_fixed_points, y_fixed_points = generate_track(
#     horizontal_distance=200,
#     n_screws=8,
#     dx=1,
#     y_fixed_points=y_fixed_points_extreme
# )

# Doing calculations:
assert np.max(np.abs(friction(x)/normal_force(x))
              ) < static_friction_coeficcient


print(f'Total time: {np.sum(dt(x[1:])):.3f} seconds')

plt_function(x, y, "Track shape", "$y(x)$ (mm)")
plt_function(x, inclitation_angle(x)*180/np.pi,
             "Inclitation angle", "$Beta$ (degrees)")
plt_function(x, curvature(x), "Curvature", "$K(x)$ (1/mm)")
plt_function(x, velocity(x), "Velocity", "$v(x)$ (mm/s)")
plt_function(x, [normal_force(x)/(mass*g), friction(x)/(mass*g)],
             "Normal force and Friction", "$N/mg, f/mg$")
plt_function(x, np.abs(friction(x)/normal_force(x)),
             "The ratio |f/N|", "$|f/N|$")
