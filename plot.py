import numpy as np
import csv
import ast
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


def load_csv_time_matrix(csv_name):
    with open(csv_name, mode='r') as file:
        reader = csv.reader(file)
        matrix_loaded = []

        for row in reader:
            row_parsed = [ast.literal_eval(cell) if ',' in cell else float(cell) for cell in row]
            matrix_loaded.append(row_parsed)
        return matrix_loaded

def plot_2d(matr_timings, plot_title='', x_axis='x', y_axis='y',
            legend_1='1', legend_2='2'):
    zero_index_values = [pair[0] for row in matr_timings for pair in row]
    first_index_values = [pair[1] for row in matr_timings for pair in row]

    plt.figure(figsize=(9, 7))
    plt.plot(zero_index_values, label=legend_1, marker='o')
    plt.plot(first_index_values, label=legend_2, marker='o')
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

    ax.plot_surface(grid_x, grid_y, grid_z1, color='blue', alpha=0.5, label=subtitle_1_2)
    ax.plot_surface(grid_x, grid_y, grid_z2, color='red', alpha=0.5, label=subtitle_2_2)

    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_zlabel(z_title)
    ax.set_title(plot_title)
    ax.legend()

    manager = plt.get_current_fig_manager()
    manager.resize(2000, 1400)

    return plt


matr_timings = load_csv_time_matrix("time_matrix_n_4-6_m_2-7.csv")

# 2d график времени для точного решения (небольшая размерность данных)
plt_0 = plot_2d(matr_timings, plot_title='Время счета',
                x_axis='Размерность входных данных (число клиентов (n) + число коммивояжеров (m) )',
                y_axis='Время (в секундах)',
                legend_1='Результаты модели с общим графом коммивояжеров',
                legend_2='Результаты модели с отдельными графами коммивояжеров')

plt_0.show()

# 3d график времени для точного решения (небольшая размерность данных)
plt_1 = plot_3d_interpolation(matr_timings,
                              plot_title='3D-график времени счета первой и второй моделей (с интерполяцией)',
                              x_title='Число клиентов (n)', y_title='Число коммивояжеров (m)',
                              z_title='Время счета (в секундах)',
                              subtitle_1_1='Результаты модели с общим графом коммивояжеров',
                              subtitle_2_1='Результаты модели с отдельными графами коммивояжеров',
                              subtitle_1_2='Интерполированная поверхность для модели с общим графом',
                              subtitle_2_2='Интерполированная поверхность для модели с отдельными графами')
plt_1.show()
