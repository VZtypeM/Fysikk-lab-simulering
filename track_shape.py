import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline


def generate_track(
        horizontal_distance: int = 200,
        n_screws: int = 8,
        dx: float = 1,
        y_fixed_points: np.ndarray = None):

    x_fixed_points = np.linspace(
        0, n_screws-1, n_screws, dtype="int32") * horizontal_distance

    x_min = 0
    x_max = (len(x_fixed_points) - 1) * horizontal_distance  # 1400

    x = np.linspace(
        x_min,
        x_max,
        int(np.ceil((x_max - x_min)/dx+1)),  # One more than x_max if dx = 1
        dtype=("int32" if dx == 1 else "float64")
    )

    if y_fixed_points is None:
        y_fixed_points = np.zeros(8, dtype="float64")
        y_fixed_points[0] = 300
        y_fixed_points[1] = y_fixed_points[0] - np.random.randint(40, 60)
        y_fixed_points[2] = y_fixed_points[1] - np.random.randint(70, 90)
        y_fixed_points[3] = y_fixed_points[2] + np.random.randint(-30, 10)
        y_fixed_points[4] = y_fixed_points[3] + np.random.randint(30, 70)
        y_fixed_points[5] = y_fixed_points[4] + np.random.randint(-20, 20)
        y_fixed_points[6] = y_fixed_points[5] - np.random.randint(40, 80)
        y_fixed_points[7] = y_fixed_points[6] + np.random.randint(-40, 40)
    else:
        assert y_fixed_points.shape == x_fixed_points.shape

    cs = CubicSpline(x_fixed_points, y_fixed_points, bc_type='natural')

    y = cs(x)
    dy = cs(x, 1)
    d2y = cs(x, 2)

    return x, dx, y, dy, d2y, x_fixed_points, y_fixed_points


if __name__ == "__main__":
    x, dx, y, dy, d2y, x_fixed_points, y_fixed_points = generate_track()
    fontsize = 10

    baneform = plt.figure('y(x)', figsize=(8, 4))
    plt.plot(x, y, x_fixed_points, y_fixed_points, '*')
    plt.title('Banens form', fontsize=fontsize)
    plt.xlabel('$x$ (mm)', fontsize=fontsize)
    plt.ylabel('$y(x)$ (mm)', fontsize=fontsize)
    plt.text(10, 80, 'Skruehøyder (mm):', fontsize=fontsize)
    plt.text(-40, 50, int(y_fixed_points[0]), fontsize=fontsize)
    plt.text(160, 50, int(y_fixed_points[1]), fontsize=fontsize)
    plt.text(360, 50, int(y_fixed_points[2]), fontsize=fontsize)
    plt.text(560, 50, int(y_fixed_points[3]), fontsize=fontsize)
    plt.text(760, 50, int(y_fixed_points[4]), fontsize=fontsize)
    plt.text(960, 50, int(y_fixed_points[5]), fontsize=fontsize)
    plt.text(1160, 50, int(y_fixed_points[6]), fontsize=fontsize)
    plt.text(1360, 50, int(y_fixed_points[7]), fontsize=fontsize)
    plt.ylim(0, 300)
    plt.xlim(-50, 1450)
    plt.grid()
    plt.show()
    # Ta bort # hvis du ønsker å lagre grafen som pdf og/eller png.
    #baneform.savefig("baneform.pdf", bbox_inches='tight')
    #baneform.savefig("baneform.png", bbox_inches='tight')
