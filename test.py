from models.base_model import MTSPTWModel
from models.updated_model import MTSPTWShortModel, my_sort_route
from utils.utils import create_test_data, timing

tl = 60
for n in range(7, 15):
    for m in range(4, 10):
        print(f"\n n = {n} \t m = {m}")
        test = create_test_data(n, m)
        model1 = MTSPTWModel(timelimit=tl, **test)
        model2 = MTSPTWShortModel(timelimit=tl, **test)
        t1, _ = timing(model1.solve)
        t2, _ = timing(model2.solve, sorting=my_sort_route)
        res1 = model1.output()
        res2 = model2.output()
        obj1 = res1['objective_value']
        obj2 = res2['objective_value']
        print(f"t1 {t1:.4f} \t t2 {t2:.4f}")
        print(f"res1 = {res1}")
        print(f"res2 = {res1}")

test = create_test_data(9, 6)
model1 = MTSPTWModel(timelimit=10, **test)
model2 = MTSPTWShortModel(timelimit=10, **test)
t1, r1 = timing(model1.solve)
t2, r2 = timing(model2.solve, sorting=my_sort_route)
output1 = model1.output()
output2 = model2.output()

print(t1)
print(output1)

print(t2)
print(output2)

# tl = 60
# for n in range(7, 15):
#     for m in range(4, 15):
#         print(f" n = {n} \t m = {m}")
#         test = create_test_data(n, m)
#         model1 = MTSPTWModel(timelimit=tl, **test)
#         model2 = MTSPTWShortModel(timelimit=tl, **test)
#         model1.solve()
#         model2.solve(sorting=my_sort_route)
#         res1 = model1.output()
#         res2 = model2.output()
