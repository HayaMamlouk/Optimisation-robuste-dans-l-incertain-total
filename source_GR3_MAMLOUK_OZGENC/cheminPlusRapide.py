from gurobipy import Model, GRB, quicksum

def chemin_plus_rapide(nodes, transitions, start, end, scenario):
    """
    Resoudre le problème du chemin le plus rapide pour un scénario donné.
    """
    # les coûts des arcs pour le scénario donné
    weights = {arc: costs[scenario] for arc, costs in transitions.items()}

    # initialiser le modèle
    m = Model("ShortestPath")
    m.setParam("OutputFlag", 0)  

    # declaration des variables de décision x_ij = 1 si l'arc (i, j) est sélectionné, 0 sinon
    x = m.addVars(transitions.keys(), vtype=GRB.BINARY, name="x")

    # definition de l'objectif (minimiser le coût total)
    m.setObjective(quicksum(weights[arc] * x[arc] for arc in transitions), GRB.MINIMIZE)

    # contraintes de flot
    # sommet de départ
    m.addConstr(
        quicksum(x[(start, j)] for j in nodes if (start, j) in transitions) -
        quicksum(x[(i, start)] for i in nodes if (i, start) in transitions) == 1,
        "flow_source"
    )

    # sommet de destination
    m.addConstr(
        quicksum(x[(end, j)] for j in nodes if (end, j) in transitions) -
        quicksum(x[(i, end)] for i in nodes if (i, end) in transitions) == -1,
        "flow_destination"
    )

    # contraintes de flot pour les autres sommets
    for v in nodes:
        if v != start and v != end:
            m.addConstr(
                quicksum(x[(v, j)] for j in nodes if (v, j) in transitions) -
                quicksum(x[(i, v)] for i in nodes if (i, v) in transitions) == 0,
                f"flow_{v}"
            )

    # Resolution
    m.optimize()

    # extraire la solution
    if m.status == GRB.OPTIMAL:
        selected_arcs = [arc for arc in transitions if x[arc].x > 0.5]
        solution = {
            "path": selected_arcs,
            "cost": m.objVal
        }
        return solution
    else:
        return {"message": "No optimal solution found."}

