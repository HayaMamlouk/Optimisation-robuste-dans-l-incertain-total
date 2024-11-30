#!/usr/bin/python

# Copyright 2024, Gurobi Optimization, Inc.

from gurobipy import *

def maxmin(nb_projects, nb_scenarios, costs, utilities, budget, verbose=True) :
    """
    Résoudre le problème de maxmin
    """
    # initialisation du modèle
    m = Model("maxmin")

    # declaration des variables de decision, x_j = 1 si le projet j est sélectionné, 0 sinon
    x = []
    for j in range(nb_projects):
        x.append(m.addVar(vtype=GRB.BINARY, name="x%d" % (j + 1)))

    # variable t pour représenter la valeur minimale de z_i(x) 
    t = m.addVar(vtype=GRB.CONTINUOUS, name="t")

    # maj du modele pour integrer les nouvelles variables
    m.update()

    # definition de l'ojectif (maximiser t)
    m.setObjective(t, GRB.MAXIMIZE)

    # definition des contraintes
    # contrainte t est la valeur minimale de z_i(x) pour tous les scénarios i
    for i in range(nb_scenarios):
        m.addConstr(t <= quicksum(utilities[i][j] * x[j] for j in range(nb_projects)), 
                    "scenario_%d" % (i + 1))

    # contrainte de budget
    m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "budget")

    # Resolution
    m.optimize()

    if verbose:
        print("")
        print("Solution optimale:")
        for j in range(nb_projects):
            print("x%d = %d" % (j + 1, x[j].x))
        print("")
        print("Valeur de la fonction objective (t) :", t.x)

        # Utilités dans les scénarios
        z = [sum(utilities[i][j] * x[j].x for j in range(nb_projects)) for i in range(nb_scenarios)]
        print("Utilités dans les scénarios:", z)

    return
