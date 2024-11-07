from plot import load_csv_matrix, plot_2d, plot_3d_interpolation
import json

matr_timings = load_csv_matrix("result_data/time_matrix_n_4-6_m_2-7.csv")

# 2d график времени для точного решения (небольшая размерность данных)
plt_0 = plot_2d(matr_timings, plot_title='Время счета',
                x_axis='Размерность входных данных (число клиентов (n) + число коммивояжеров (m) )',
                y_axis='Время (в секундах)',
                legend_2='Результаты модели с общим графом коммивояжеров',
                legend_1='Результаты модели с отдельными графами коммивояжеров')

# plt_0.show()

# 3d график времени для точного решения (небольшая размерность данных)
plt_1 = plot_3d_interpolation(matr_timings,
                              plot_title='3D-график времени счета первой и второй моделей (с интерполяцией)',
                              x_title='Число клиентов (n)', y_title='Число коммивояжеров (m)',
                              z_title='Время счета (в секундах)',
                              subtitle_2_1='Результаты модели с общим графом коммивояжеров',
                              subtitle_1_1='Результаты модели с отдельными графами коммивояжеров',
                              subtitle_2_2='Интерполированная поверхность для модели с общим графом',
                              subtitle_1_2='Интерполированная поверхность для модели с отдельными графами')
# plt_1.show()

constr_matrix = load_csv_matrix("result_data/constr_num_n_7-25_m_4-20.csv")
var_matrix = load_csv_matrix("result_data/var_num_n_7-25_m_4-20.csv")

plt_2 = plot_3d_interpolation(constr_matrix,
                              plot_title='Число ограничений в первой и второй моделях (с интерполяцией)',
                              x_title='Число клиентов (n)', y_title='Число коммивояжеров (m)',
                              z_title='Число ограничений ',
                              subtitle_2_1='Результаты модели с общим графом коммивояжеров',
                              subtitle_1_1='Результаты модели с отдельными графами коммивояжеров',
                              subtitle_2_2='Интерполированная поверхность для модели с общим графом',
                              subtitle_1_2='Интерполированная поверхность для модели с отдельными графами')
# plt_2.show()

plt_3 = plot_3d_interpolation(var_matrix,
                              plot_title='Число переменных в первой и второй моделях (с интерполяцией)',
                              x_title='Число клиентов (n)', y_title='Число коммивояжеров (m)',
                              z_title='Число переменных ',
                              subtitle_2_1='Результаты модели с общим графом коммивояжеров',
                              subtitle_1_1='Результаты модели с отдельными графами коммивояжеров',
                              subtitle_2_2='Интерполированная поверхность для модели с общим графом',
                              subtitle_1_2='Интерполированная поверхность для модели с отдельными графами')
# plt_3.show()

total_dim_matrix = []
for row1, row2 in zip(var_matrix, constr_matrix):
    total_dims = []
    for (x1, y1), (x2, y2) in zip(row1, row2):
        total_dims.append((x1 + x2, y1 + y2))
    total_dim_matrix.append(total_dims)

plt_4 = plot_3d_interpolation(total_dim_matrix,
                              plot_title='Размерность в первой и второй моделях (с интерполяцией)',
                              x_title='Число клиентов (n)', y_title='Число коммивояжеров (m)',
                              z_title='Число переменных \n+ число ограничений',
                              subtitle_2_1='Результаты модели с общим графом коммивояжеров',
                              subtitle_1_1='Результаты модели с отдельными графами коммивояжеров',
                              subtitle_2_2='Интерполированная поверхность для модели с общим графом',
                              subtitle_1_2='Интерполированная поверхность для модели с отдельными графами')
# plt_4.show()

with open('result_data/timelimited_results_n_7-15_m_7-15.json', 'r') as f:
    data = json.load(f)
n = range(7, 15)
m = range(7, 15)
matrix_obj = [[(0, 0)] * len(m) for _ in range(len(n))]
for idx_n in n:
    for idx_m in m:
        key = f"({idx_n}, {idx_m})"
        if key in data:
            obj1 = data[key]['obj1']
            obj2 = data[key]['obj2']
            matrix_obj[idx_n - n[0]][idx_m - m[0]] = (obj1, obj2)

plt_5 = plot_2d(matrix_obj, plot_title='Значение ц.ф. при ограничении на вычисление в 20 сек.',
                x_axis='Размерность входных данных (число клиентов (n) + число коммивояжеров (m) )',
                y_axis='Целевая функция',
                legend_2='Результаты модели с общим графом коммивояжеров',
                legend_1='Результаты модели с отдельными графами коммивояжеров')

# plt_5.show()

plt_6 = plot_3d_interpolation(matrix_obj,
                              plot_title='Значение ц.ф. первой и второй моделей за 20 сек. (с интерполяцией)',
                              x_title='Число клиентов (n)', y_title='Число коммивояжеров (m)',
                              z_title='Целевая функция',
                              subtitle_2_1='Результаты модели с общим графом коммивояжеров',
                              subtitle_1_1='Результаты модели с отдельными графами коммивояжеров',
                              subtitle_2_2='Интерполированная поверхность для модели с общим графом',
                              subtitle_1_2='Интерполированная поверхность для модели с отдельными графами')
plt_6.show()
