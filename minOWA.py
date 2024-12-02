from gurobipy import Model, GRB, quicksum

def minOWA(nb_projects, nb_scenarios, costs, utilities, budget, weights, verbose=True):
    """
    Résoudre le problème de minOWA des regrets en retournant les projets sélectionnés dans l'ordre initial.
    """

    # Step 1: Compute z*_i for each scenario
    z_star = []
    for i in range(nb_scenarios):
        model = Model(f"OptimalUtility_Scenario_{i}")
        x = [model.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(nb_projects)]
        model.setObjective(quicksum(utilities[i][j] * x[j] for j in range(nb_projects)), GRB.MAXIMIZE)
        model.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")
        model.optimize()
        if model.status == GRB.OPTIMAL:
            z_star.append(model.objVal)
        else:
            print(f"Failed to compute z* for scenario {i + 1}")
            return

    # Step 2: Solve minOWA of regrets problem
    model = Model("minOWA_of_regrets")

    # Variables de décision
    x = [model.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(nb_projects)]
    regrets = [model.addVar(vtype=GRB.CONTINUOUS, name=f"regret_{i}") for i in range(nb_scenarios)]
    a = [[model.addVar(vtype=GRB.CONTINUOUS, name=f"a_{i}_{k}") for k in range(nb_scenarios)] for i in range(nb_scenarios)]

    # Calculer w_k'
    w_prime = [weights[k] - weights[k + 1] if k < nb_scenarios - 1 else weights[k] for k in range(nb_scenarios)]

    # Définir la fonction objectif
    model.setObjective(
        quicksum(w_prime[k] * quicksum(a[i][k] * regrets[i] for i in range(nb_scenarios)) for k in range(nb_scenarios)),
        GRB.MINIMIZE
    )

    # Contraintes pour regrets
    for i in range(nb_scenarios):
        regret_expr = z_star[i] - quicksum(utilities[i][j] * x[j] for j in range(nb_projects))
        model.addConstr(regrets[i] >= regret_expr, f"RegretConstraint_{i}")

    # Contraintes pour linéarisation de L_k(r)
    for k in range(nb_scenarios):
        model.addConstr(quicksum(a[i][k] for i in range(nb_scenarios)) == k + 1, f"SumA_{k}")
        for i in range(nb_scenarios):
            model.addConstr(a[i][k] <= 1, f"UpperBoundA_{i}_{k}")
            model.addConstr(a[i][k] >= 0, f"NonNegA_{i}_{k}")

    # Contraintes de budget
    model.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")

    # Résolution
    model.optimize()

    if model.status == GRB.UNBOUNDED:
        print("Model is unbounded.")
        return
    if model.status == GRB.INFEASIBLE:
        print("Model is infeasible.")
        model.computeIIS()
        model.write("infeasible_model.ilp")
        return

    if verbose and model.status == GRB.OPTIMAL:
        print("\nValeur de la fonction objectif (minOWA):", model.objVal)

        # Sélectionner les projets dans l'ordre initial
        selected_projects = [j + 1 for j in range(nb_projects) if x[j].x > 0.5]

        print("\nProjets sélectionnés dans l'ordre initial:")
        print(selected_projects)

    return selected_projects, model.objVal

# Example data for 2 scenarios and 10 projects
nb_projects = 10
nb_scenarios = 2
costs = [60, 10, 15, 20, 25, 20, 5, 15, 20, 60]
utilities = [
    [70, 18, 16, 14, 12, 10, 8, 6, 4, 2],  # Scenario 1
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 70],  # Scenario 2
]
budget = 100
weights = [2, 1]  # OWA weights

# Solve minOWA of regrets
minOWA(nb_projects, nb_scenarios, costs, utilities, budget, weights)

