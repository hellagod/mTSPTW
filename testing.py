from models.base_model import MTSPTWModel
from models.updated_model import MTSPTWShortModel, my_sort_route
from utils.utils import timing, create_test_data

import json
import csv
import numpy as np

n = (4,6)
m = (2,7)
matrix = [[(0, 0)] * (m[1] - m[0] + 1) for _ in range(n[0], n[1] + 1)]


def compute_for_pair(i, j, tl=None):
    test = create_test_data(i, j)
    model = MTSPTWModel(**test, timelimit=tl)
    short_model = MTSPTWShortModel(**test, timelimit=tl)
    try:
        t1, r1 = timing(model.solve)
        output1 = model.output()

        t2, r2 = timing(short_model.solve, sorting=my_sort_route)
        output2 = short_model.output()

        results = {
            'n': i,
            'm': j,
            't1': t1,
            't2': t2,
            'output1': output1,
            'output2': output2,
            'variables_model': model.result.problem[0]['Number of variables'],
            'variables_short_model': short_model.result.problem[0]['Number of variables'],
            'constraints_model': model.result.problem[0]['Number of constraints'],
            'constraints_short_model': short_model.result.problem[0]['Number of constraints'],
        }
        return results
    except Exception as e:
        return {'i': i, 'j': j, 'error': str(e)}


if __name__ == '__main__':
    results_dict = {}
    args = [(i, j) for j in range(m[0], m[1] + 1) for i in range(n[0], n[1] + 1)]

    for i, j in args:
        result = compute_for_pair(i, j)

        if 'error' in result:
            print(f"Error at ({i}, {j}): {result['error']}")
        else:
            print(f"\ni={i}\tj={j}")
            print(result['output1'])
            print(result['output2'])
            print(result['t1'], result['t2'])

            matrix[i - n[0]][j - m[0]] = (result['t1'], result['t2'])

            print(result['variables_model'])
            print(result['variables_short_model'])
            print(result['constraints_model'])
            print(result['constraints_short_model'])
            results_dict[f'({i}, {j})'] = result

    json_name = f'results_n_{n[0]}-{n[1]}_m_{m[0]}-{m[1]}.json'
    with open(json_name, 'w') as f:
        json.dump(results_dict, f, indent=4)

    csv_name = f'time_matrix_n_{n[0]}-{n[1]}_m_{m[0]}-{m[1]}.csv'
    with open(csv_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for row in matrix:
            row_str = [str(cell) for cell in row]
            writer.writerow(row_str)

print(matrix)
print(np.array_str(np.array(matrix), precision=2, suppress_small=True))
