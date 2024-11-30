#!/usr/bin/python

from gurobipy import *

n_projects = 10  # nombre de projets
n_scenarios = 2  # nombre de scénarios

# coûts des projets
costs = [60, 10, 15, 20, 25, 20, 5, 15, 20, 60]

# utilités des projets dans chaque scénario
utilities = [
    [70, 18, 16, 14, 12, 10, 8, 6, 4, 2],  # Scenario 1
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 70]   # Scenario 2
]

# budget maximal
budget = 100

# Etape 1: trouver z*_i pour chaque scénario i
z_star = []
x_values = []

for i in range(n_scenarios):
    # initialisation du modèle
    m = Model("maximize_scenario_%d" % (i + 1))
    
    # declaration des variables de decision, x_j = 1 si le projet j est sélectionné, 0 sinon
    x = []
    for j in range(n_projects):
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

    # definition de l'ojectif (maximiser z_i(x))
    m.setObjective(quicksum(utilities[i][j] * x[j] for j in range(n_projects)), GRB.MAXIMIZE)

    # definition des contraintes
    m.addConstr(quicksum(costs[j] * x[j] for j in range(n_projects)) <= budget, "budget_constraint")

    # Resolution
    m.optimize()

    # Stocker la valeur optimale de z_i
    z_star.append(m.objVal)
    # stocker les valeurs des variables x
    x_values.append([x[j].x for j in range(n_projects)])

# etape 2: résoudre le problème de minimisation du regret
m = Model("minmax_regret")

# declaration des variables de decision
x = []
for j in range(n_projects):
    x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

# variable t pour représenter le regret maximal
t = m.addVar(vtype=GRB.CONTINUOUS, name="max_regret")

# definition de l'ojectif (minimiser t)
m.setObjective(t, GRB.MINIMIZE)

# definition des contraintes
# contrainte t est la valeur maximale de z*_i - z_i(x) pour tous les scénarios i
for i in range(n_scenarios):
    regret = z_star[i] - quicksum(utilities[i][j] * x[j] for j in range(n_projects))
    m.addConstr(t >= regret, "regret_constraint_%d" % (i + 1))

# contrainte de budget
m.addConstr(quicksum(costs[j] * x[j] for j in range(n_projects)) <= budget, "budget_constraint")

# Resolution
m.optimize()


print("")
print("z*_i pour chaque scénario i:", z_star)
print("Valeurs des variables x dans chaque scénario:", x_values)

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
