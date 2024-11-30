from gurobipy import Model, GRB, quicksum

# Data from Example 1
n_projects = 10
n_scenarios = 2

# Costs of projects
costs = [60, 10, 15, 20, 25, 20, 5, 15, 20, 60]

# Utilities in each scenario
utilities = [
    [70, 18, 16, 14, 12, 10, 8, 6, 4, 2],  # Scenario 1
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 70]   # Scenario 2
]

# Budget constraint
budget = 100

# OWA weights
w = [2, 1]  # Example weights
w_prime = [w[k] - w[k+1] if k < len(w) - 1 else w[k] for k in range(len(w))]

# Model setup
model = Model("OWA_optimization")

# Decision variables
x = [model.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(n_projects)]
r = [model.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(n_scenarios)]
b = [[model.addVar(vtype=GRB.CONTINUOUS, name=f"b_{i}_{k}") for k in range(n_scenarios)] for i in range(n_scenarios)]

# Update model
model.update()

# Objective: Maximize OWA
objective = quicksum(w_prime[k] * ((k+1) * r[k] - quicksum(b[i][k] for i in range(n_scenarios))) for k in range(n_scenarios))
model.setObjective(objective, GRB.MAXIMIZE)

# Constraints
for i in range(n_scenarios):
    for k in range(n_scenarios):
        model.addConstr(r[k] - b[i][k] <= quicksum(utilities[i][j] * x[j] for j in range(n_projects)),
                        name=f"constraint_r_{k}_b_{i}")

for i in range(n_scenarios):
    for k in range(n_scenarios):
        model.addConstr(b[i][k] >= 0, name=f"b_nonnegative_{i}_{k}")

# Budget constraint
model.addConstr(quicksum(costs[j] * x[j] for j in range(n_projects)) <= budget, "budget_constraint")

# Solve the model
model.optimize()

# Print the solution
print("\nSolution optimale:")
for j in range(n_projects):
    print(f"x_{j + 1} = {x[j].x}")

print("\nValeurs de r_k:")
for k in range(n_scenarios):
    print(f"r_{k + 1} = {r[k].x}")

print("\nValeur de la fonction objective (OWA) :", model.objVal)
