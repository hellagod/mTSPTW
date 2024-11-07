import numpy as np
import csv
import ast
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def load_csv_matrix(csv_name):
    with open(csv_name, mode='r') as file:
        reader = csv.reader(file)
        matrix_loaded = []

        for row in reader:
            row_parsed = [ast.literal_eval(cell) if ',' in cell else float(cell) for cell in row]
            matrix_loaded.append(row_parsed)
        return matrix_loaded


def plot_2d(matr_timings, plot_title='', x_axis='x', y_axis='y',
            legend_1='1', legend_2='2', is_matrix=True):
    first_model_values = [pair[0] for row in matr_timings for pair in row] if is_matrix else matr_timings[0]
    second_model_values = [pair[1] for row in matr_timings for pair in row] if is_matrix else matr_timings[1]

    plt.figure(figsize=(9, 7))
    plt.plot(first_model_values, label=legend_1, marker='o')
    plt.plot(second_model_values, label=legend_2, marker='o')
    plt.title(plot_title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.legend()
    plt.grid()

    manager = plt.get_current_fig_manager()
    manager.resize(2000, 1400)

    return plt


def plot_3d_interpolation(matr_timings, plot_title='',
                          x_title='x', y_title='y', z_title='z',
                          subtitle_1_1='1_1', subtitle_2_1='2_1', subtitle_1_2='1_2', subtitle_2_2='2_2'):
    x_vals, y_vals, z1_vals, z2_vals = [], [], [], []

    for i, row in enumerate(matr_timings):
        for j, val in enumerate(row):
            x_vals.append(i)
            y_vals.append(j)
            z1_vals.append(val[0])
            z2_vals.append(val[1])

    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    z1_vals = np.array(z1_vals)
    z2_vals = np.array(z2_vals)

    grid_x, grid_y = np.meshgrid(np.linspace(x_vals.min(), x_vals.max(), 50),
                                 np.linspace(y_vals.min(), y_vals.max(), 50))

    grid_z1 = griddata((x_vals, y_vals), z1_vals, (grid_x, grid_y), method='cubic')
    grid_z2 = griddata((x_vals, y_vals), z2_vals, (grid_x, grid_y), method='cubic')

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x_vals, y_vals, z1_vals, color='b', label=subtitle_1_1, marker='o')
    ax.scatter(x_vals, y_vals, z2_vals, color='r', label=subtitle_2_1, marker='o')

    ax.plot_surface(grid_x, grid_y, grid_z1, color='blue', alpha=1, label=subtitle_1_2,
                    antialiased=False, rstride=1, cstride=1, linewidth=0.5)
    ax.plot_surface(grid_x, grid_y, grid_z2, color='red', alpha=1, label=subtitle_2_2,
                    antialiased=False, rstride=1, cstride=1, linewidth=0.5)

    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_zlabel(z_title)
    ax.set_title(plot_title)
    ax.legend()

    manager = plt.get_current_fig_manager()
    manager.resize(2000, 1400)

    return plt
