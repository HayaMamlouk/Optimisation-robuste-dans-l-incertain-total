#!/usr/bin/python

# Copyright 2024, Gurobi Optimization, Inc.

from gurobipy import *

# Number of projects and scenarios
nb_projects = 10
nb_scenarios = 2

# Costs of the projects
costs = [60, 10, 15, 20, 25, 20, 5, 15, 20, 60]

# Utilities of the projects in each scenario
utilities = [
    [70, 18, 16, 14, 12, 10, 8, 6, 4, 2],  # Scenario 1
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 70]   # Scenario 2
]

# Budget constraint
budget = 100

# Initialize the model
m = Model("maxmin_robust_optimization")

# Decision variables: x[j] is 1 if project j is selected, 0 otherwise
x = []
for j in range(nb_projects):
    x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

# Auxiliary variable t representing the minimum utility
t = m.addVar(vtype=GRB.CONTINUOUS, name="t")

# Update the model to integrate new variables
m.update()

# Objective: Maximize t
m.setObjective(t, GRB.MAXIMIZE)

# Constraints for t <= z_i(x) for all scenarios
for i in range(nb_scenarios):
    m.addConstr(t <= quicksum(utilities[i][j] * x[j] for j in range(nb_projects)), 
                "scenario_%d" % (i + 1))

# Budget constraint
m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "budget")

# Solve the model
m.optimize()

# Print the solution
print("")
print("Solution optimale:")
for j in range(nb_projects):
    print("x%d = %d" % (j + 1, x[j].x))
print("")
print("Valeur de la fonction objective (t) :", t.x)

# Compute the resulting utilities z(x) in each scenario
z = [sum(utilities[i][j] * x[j].x for j in range(nb_projects)) for i in range(nb_scenarios)]
print("Utilités dans les scénarios:", z)
