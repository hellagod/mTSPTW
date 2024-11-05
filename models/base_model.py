import networkx as nx
from matplotlib import pyplot as plt
from pyomo.environ import ConcreteModel, minimize, Binary, RangeSet, Objective, Var, Constraint, NonNegativeReals
from pyomo.opt import SolverFactory, SolverStatus, TerminationCondition
import random

from utils.utils import create_test_data

SOLVER = 'glpk'
SOLVER_PATH = 'C:\\glpk-4.65\\w64\\glpsol.exe'


class MTSPTWModel:
    def __init__(self, n, m, costs, times, time_windows, big_M, timelimit=False):
        self.solver = SolverFactory(SOLVER, tee=True, executable=SOLVER_PATH)
        if timelimit:
            self.solver.options = {'tmlim': timelimit, 'mipgap': 0.0001}
        self.n = n
        self.m = m
        self.costs = costs
        self.times = times
        self.time_windows = time_windows
        self.big_M = big_M

        self.graph = self._create_graph()
        self.model = ConcreteModel()

        self._init_vars()
        self._init_objective()
        self._init_constraints()

    def _create_graph(self):
        graph = nx.complete_graph(self.n + 1)
        for (i, j), cost in self.costs.items():
            graph.add_edge(i, j, weight=cost)
        return graph

    def _init_vars(self):
        model = self.model
        model.V = RangeSet(0, self.n)
        model.K = RangeSet(1, self.m)
        model.x = Var(model.V, model.V, model.K, within=Binary)
        model.u = Var(RangeSet(0, self.n + 1), model.K, within=NonNegativeReals)

    def _init_objective(self):
        model = self.model

        model.obj = Objective(
            expr=sum(model.u[self.n + 1, k] - model.u[0, k] for k in model.K),
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

        def time_sequencing_constraint(mod, i, j, k):
            if i != j and j != 0:
                return mod.u[i, k] - mod.u[j, k] + self.big_M * mod.x[i, j, k] <= self.big_M - self.times[i][j]
            return Constraint.Skip

        def depot_return_time_constraint(mod, i, k):
            return mod.u[i, k] - mod.u[self.n + 1, k] + self.big_M * mod.x[
                i, 0, k] <= self.big_M - self.times[i][0]

        def time_window_constraint_1(mod, i, k):
            return self.time_windows[i][0] <= mod.u[i, k]

        def time_window_constraint_2(mod, i, k):
            return mod.u[i, k] <= self.time_windows[i][1]

        def depot_start_constraint(mod, k):
            return mod.u[0, k] <= self.big_M * sum(mod.x[0, j, k] for j in mod.V if j != 0)

        model.depot_departure = Constraint(model.K, rule=depot_departure_constraint)
        model.node_visit = Constraint(model.V - {0}, rule=node_visit_constraint)
        model.flow_conservation = Constraint(model.V - {0}, model.K, rule=flow_conservation_constraint)
        model.time_sequencing = Constraint(model.V, model.V, model.K, rule=time_sequencing_constraint)
        model.depot_return_time = Constraint(model.V - {0}, model.K, rule=depot_return_time_constraint)
        model.time_windows_1 = Constraint(model.V - {0}, model.K, rule=time_window_constraint_1)
        model.time_windows_2 = Constraint(model.V - {0}, model.K, rule=time_window_constraint_2)
        model.depot_start = Constraint(model.K, rule=depot_start_constraint)

    def solve(self):
        self.result = self.solver.solve(self.model)
        if self.result.solver.termination_condition == TerminationCondition.infeasible:
            raise Exception(TerminationCondition.infeasible)
        self.routes = {k: [] for k in self.model.K}
        for k in self.model.K:
            for i in self.model.V:
                for j in self.model.V - {0}:
                    if i != j and self.model.x[i, j, k].value and self.model.x[i, j, k].value > 0.5:
                        self.routes[k].append((i, j))

    def output(self):
        return {
            'objective_value': self.model.obj(),
            'routes': self.routes
        }

    def plot(self):
        pos = nx.circular_layout(self.graph)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        colors = ["#" + ''.join([random.choice('789ABCDEF') for _ in range(6)]) for _ in range(self.m)]
        edge_colors = []

        for (i, j) in self.graph.edges():
            if any((i, j) in self.routes[k] or (j, i) in self.routes[k] for k in self.routes):
                for k, route in self.routes.items():
                    if (i, j) in route or (j, i) in route:
                        edge_colors.append(colors[k - 1])
            else:
                edge_colors.append('lightgray')

        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=500, edge_color=edge_colors,
                width=2)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        plt.title("Маршруты многокоммивояжеров")
        plt.show()


if __name__ == "__main__":
    test = create_test_data(5, 5)

    routing_model = MTSPTWModel(**test)
    routing_model.solve()
    output = routing_model.output()
    routing_model.plot()
