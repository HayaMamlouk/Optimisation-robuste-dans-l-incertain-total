#!/usr/bin/python

from gurobipy import *

# Number of projects and scenarios
n_projects = 10
n_scenarios = 2

# Costs of the projects
costs = [60, 10, 15, 20, 25, 20, 5, 15, 20, 60]

# Utilities of the projects in each scenario
utilities = [
    [70, 18, 16, 14, 12, 10, 8, 6, 4, 2],  # Scenario 1
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 70]   # Scenario 2
]

# Budget constraint
budget = 100

# Step 1: Find z*_i for each scenario
z_star = []

for i in range(n_scenarios):
    model = Model("maximize_scenario_%d" % (i + 1))
    
    # Decision variables
    x = []
    for j in range(n_projects):
        x.append(model.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

    # Objective: Maximize utility in scenario i
    model.setObjective(quicksum(utilities[i][j] * x[j] for j in range(n_projects)), GRB.MAXIMIZE)

    # Budget constraint
    model.addConstr(quicksum(costs[j] * x[j] for j in range(n_projects)) <= budget, "budget_constraint")

    # Solve the model
    model.optimize()

    # Record z*_i
    z_star.append(model.objVal)

# Step 2: Minimize max regret
model = Model("minmax_regret")

# Decision variables
x = []
for j in range(n_projects):
    x.append(model.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

# Auxiliary variable for max regret
t = model.addVar(vtype=GRB.CONTINUOUS, name="max_regret")

# Objective: Minimize t
model.setObjective(t, GRB.MINIMIZE)

# Regret constraints
for i in range(n_scenarios):
    regret = z_star[i] - quicksum(utilities[i][j] * x[j] for j in range(n_projects))
    model.addConstr(t >= regret, "regret_constraint_%d" % (i + 1))

# Budget constraint
model.addConstr(quicksum(costs[j] * x[j] for j in range(n_projects)) <= budget, "budget_constraint")

# Solve the model
model.optimize()

# Print the solution
print("")
print("Solution optimale:")
for j in range(n_projects):
    print("x%d = %d" % (j + 1, x[j].x))

print("")
print("Valeur de la fonction objective (minmax regret) :", t.x)

# Compute the resulting utilities z(x) in each scenario
z = [sum(utilities[i][j] * x[j].x for j in range(n_projects)) for i in range(n_scenarios)]
print("Utilités dans les scénarios:", z)

# Compute regrets for each scenario
regrets = [z_star[i] - z[i] for i in range(n_scenarios)]
print("Regrets dans les scénarios:", regrets)
