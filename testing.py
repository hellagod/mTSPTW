from random import randint

from models.base_model import MTSPTWModel
from models.updated_model import MTSPTWShortModel
from utils.utils import generate_pair

n = 5
m = 3
gen = generate_pair(1, 50)
costs = {(i, j): randint(1, 100) for i in range(n + 1) for j in range(n + 1) if i != j}
times = [[randint(1, 100) if i != j else 0 for j in range(n + 1)] for i in range(n + 1)]
delta = randint(1, 35)
time_windows = [None, *[(times[0][i + 1] + next(gen), times[0][i + 1] + next(gen) + delta) for i in range(n)]]
big_M = 10000

model = MTSPTWModel(n, m, costs, times, time_windows, big_M)
short_model = MTSPTWShortModel(n, m, costs, times, time_windows, big_M)
model.solve()
short_model.solve()
print(model.output())
print(short_model.output())
