from models.base_model import MTSPTWModel
from models.updated_model import MTSPTWShortModel
from utils.utils import create_test_data, timing

test = create_test_data(9, 6)
model1 = MTSPTWModel(timelimit=10, **test)
model2 = MTSPTWShortModel(timelimit=10, **test)
t1, r1 = timing(model1.solve)
t2, r2 = timing(model2.solve)
output1 = model1.output()
output2 = model2.output()

print(t1)
print(output1)

print(t2)
print(output2)