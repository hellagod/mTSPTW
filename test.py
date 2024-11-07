from models.base_model import MTSPTWModel
from models.updated_model import MTSPTWShortModel, my_sort_route
from utils.utils import create_test_data, timing
import json


tl = 20
results_dict = {}
n1, m1 = 7, 7
for n in range(n1, 15):
    for m in range(m1, 15):
        print(f"\n n = {n} \t m = {m}")
        test = create_test_data(n, m)
        model1 = MTSPTWModel(**test, timelimit=tl)
        model2 = MTSPTWShortModel(**test, timelimit=tl)
        t1, _ = timing(model1.solve)
        t2, _ = timing(model2.solve, sorting=my_sort_route)
        res1 = model1.output()
        res2 = model2.output()
        obj1 = res1['objective_value']
        obj2 = res2['objective_value']
        print(f"t1 {t1:.4f} \t t2 {t2:.4f}")
        print(f"res1 = {res1}")
        print(f"res2 = {res2}")

        results_dict[f'({n}, {m})'] = {
            't1': t1,
            't2': t2,
            'res1': res1,
            'res2': res2,
            'obj1': obj1,
            'obj2': obj2
        }

json_name = f'result_data/timelimited_results_n_{n1}-{n+1}_m_{m1}-{m+1}.json'
with open(json_name, 'w') as f:
    json.dump(results_dict, f, indent=4)


# test = create_test_data(9, 6)
# model1 = MTSPTWModel(timelimit=10, **test)
# model2 = MTSPTWShortModel(timelimit=10, **test)
# t1, r1 = timing(model1.solve)
# t2, r2 = timing(model2.solve, sorting=my_sort_route)
# output1 = model1.output()
# output2 = model2.output()
#
# print(t1)
# print(output1)
#
# print(t2)
# print(output2)
