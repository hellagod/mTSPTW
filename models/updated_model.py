import networkx as nx
import random
from matplotlib import pyplot as plt
from pyomo.environ import ConcreteModel, minimize, Binary, RangeSet, Objective, Var, Constraint, NonNegativeReals
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition

from models.base_model import MTSPTWModel
from utils.utils import generate_pair

SOLVER = 'glpk'
SOLVER_PATH = 'C:\\glpk-4.65\\w64\\glpsol.exe'


class MTSPTWShortModel(MTSPTWModel):

    def _init_vars(self):
        model = self.model
        model.V = RangeSet(0, self.n)
        model.K = RangeSet(1, self.m)
        model.x = Var(model.V, model.V, model.K, within=Binary)
        model.ul = Var(RangeSet(0, 1), model.K, within=NonNegativeReals)
        model.um = Var(RangeSet(1, self.n), within=NonNegativeReals)

    def _init_objective(self):
        model = self.model

        model.obj = Objective(
            expr=sum(model.ul[1, k] - model.ul[0, k] for k in model.K),
            sense=minimize
        )

    def _init_constraints(self):
        model = self.model

        def depot_departure_constraint(mod, k):
            return sum(mod.x[0, j, k] for j in mod.V if j != 0) <= 1

        def node_visit_constraint(mod, i):
            return sum(mod.x[i, j, k] for j in mod.V for k in mod.K if i != j) == 1

        def flow_conservation_constraint(mod, i, k):
            return sum(mod.x[i, j, k] for j in mod.V if j != i) == sum(mod.x[j, i, k] for j in mod.V if j != i)

        def time_sequencing_constraint_0(mod, j, k):
            return mod.ul[0, k] - mod.um[j] + self.big_M * mod.x[0, j, k] <= self.big_M - self.times[0][j]

        def time_sequencing_constraint(mod, i, j, k):
            if i != j:
                return mod.um[i] - mod.um[j] + self.big_M * mod.x[i, j, k] <= self.big_M - self.times[i][j]
            return Constraint.Skip

        def depot_return_time_constraint(mod, i, k):
            return mod.um[i] - mod.ul[1, k] + self.big_M * mod.x[
                i, 0, k] <= self.big_M - self.times[i][0]

        def time_window_constraint_1(mod, i):
            return self.time_windows[i][0] <= mod.um[i]

        def time_window_constraint_2(mod, i):
            return mod.um[i] <= self.time_windows[i][1]

        def depot_start_constraint(mod, k):
            return mod.ul[0, k] <= self.big_M * sum(mod.x[0, j, k] for j in mod.V if j != 0)

        model.depot_departure = Constraint(model.K, rule=depot_departure_constraint)
        model.node_visit = Constraint(model.V - {0}, rule=node_visit_constraint)
        model.flow_conservation = Constraint(model.V - {0}, model.K, rule=flow_conservation_constraint)
        model.time_sequencing_0 = Constraint( model.V - {0}, model.K, rule=time_sequencing_constraint_0)
        model.time_sequencing = Constraint(model.V - {0}, model.V - {0}, model.K, rule=time_sequencing_constraint)
        model.depot_return_time = Constraint(model.V - {0}, model.K, rule=depot_return_time_constraint)
        model.time_windows_1 = Constraint(model.V - {0}, rule=time_window_constraint_1)
        model.time_windows_2 = Constraint(model.V - {0}, rule=time_window_constraint_2)
        model.depot_start = Constraint(model.K, rule=depot_start_constraint)


if __name__ == "__main__":
    n = 5
    m = 5
    gen = generate_pair(1, 50)
    costs = {(i, j): random.randint(1, 100) for i in range(n + 1) for j in range(n + 1) if i != j}
    times = [[random.randint(1, 100) if i != j else 0 for j in range(n + 1)] for i in range(n + 1)]
    delta = random.randint(1, 35)
    time_windows = [None, *[(times[0][i + 1] + next(gen), times[0][i + 1] + next(gen) + delta) for i in range(n)]]
    big_M = 10000

    routing_model = MTSPTWShortModel(n, m, costs, times, time_windows, big_M)
    routing_model.solve()
    print(routing_model.model.ul.extract_values())
    output = routing_model.output()
    print(output)
    routing_model.plot()
