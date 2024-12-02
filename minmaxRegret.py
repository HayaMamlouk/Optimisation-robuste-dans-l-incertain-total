#!/usr/bin/python

from gurobipy import *

def minmaxRegret(nb_projects, nb_scenarios, costs, utilities, budget, verbose=True) :
    # Etape 1: trouver z*_i pour chaque scénario i
    z_star = []
    x_values = []

    for i in range(nb_scenarios):
        # initialisation du modèle
        m = Model("maximize_scenario_%d" % (i + 1))
        m.setParam('OutputFlag', 0)  # Désactiver les logs de Gurobi
        
        # declaration des variables de decision, x_j = 1 si le projet j est sélectionné, 0 sinon
        x = []
        for j in range(nb_projects):
            x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

        # definition de l'ojectif (maximiser z_i(x))
        m.setObjective(quicksum(utilities[i][j] * x[j] for j in range(nb_projects)), GRB.MAXIMIZE)

        # definition des contraintes
        m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "budget_constraint")

        # Resolution
        m.optimize()

        # Stocker la valeur optimale de z_i
        z_star.append(m.objVal)
        # stocker les valeurs des variables x
        x_values.append([x[j].x for j in range(nb_projects)])

    # etape 2: résoudre le problème de minimisation du regret
    m = Model("minmax_regret")
    m.setParam('OutputFlag', 0)  # Désactiver les logs de

    # declaration des variables de decision
    x = []
    for j in range(nb_projects):
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

    # variable t pour représenter le regret maximal
    t = m.addVar(vtype=GRB.CONTINUOUS, name="max_regret")

    # definition de l'ojectif (minimiser t)
    m.setObjective(t, GRB.MINIMIZE)

    # definition des contraintes
    # contrainte t est la valeur maximale de z*_i - z_i(x) pour tous les scénarios i
    for i in range(nb_scenarios):
        regret = z_star[i] - quicksum(utilities[i][j] * x[j] for j in range(nb_projects))
        m.addConstr(t >= regret, "regret_constraint_%d" % (i + 1))

    # contrainte de budget
    m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "budget_constraint")

    # Resolution
    m.optimize()

    if verbose:
        print("")
        print("z*_i pour chaque scénario i:", z_star)
        print("Valeurs des variables x dans chaque scénario:", x_values)

        print("Solution optimale:")
        for j in range(nb_projects):
            print("x%d = %d" % (j + 1, x[j].x))

        print("")
        print("Valeur de la fonction objective (minmax regret) :", t.x)

        # calcule des utilités dans les scénarios
        z = [sum(utilities[i][j] * x[j].x for j in range(nb_projects)) for i in range(nb_scenarios)]
        print("Utilités dans les scénarios:", z)

        # calcule des regrets dans les scénarios
        regrets = [z_star[i] - z[i] for i in range(nb_scenarios)]
        print("Regrets dans les scénarios:", regrets)

    return 
