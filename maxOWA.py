from gurobipy import Model, GRB, quicksum

def maxOWA(nb_projects, nb_scenarios, costs, utilities, budget, weights, verbose=True):
    """
    Résoudre le problème de maxOWA
    """

    # trier les poids en ordre décroissant
    sorted_weights = sorted(weights, reverse=True)

    # transformer les poids w'_k = (w_k - w_{k+1}) pour k = 1 à n-1 (linéarisation)
    w_prime = [sorted_weights[i] - sorted_weights[i + 1] if i < len(weights) - 1 else sorted_weights[i]
               for i in range(len(weights))]
    # ajouter 0 à la première position pour des raisons de calcul et d'indexation
    w_prime.insert(0, 0)

    # initialisation du modèle
    m = Model("maxOWA")

    # declaration des variables de decision, x_j = 1 si le projet j est sélectionné, 0 sinon
    x = [m.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(nb_projects)]

    # variable rk (variables duales) 
    rk = [m.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(nb_scenarios)]

    # variable b_ik (variables de linéarisation)
    b = [[m.addVar(vtype=GRB.CONTINUOUS, name=f"b_{i}_{k}") for k in range(nb_scenarios)] for i in range(nb_scenarios)]

    # Variables auxiliaires pour z trié
    z = [quicksum(utilities[i][j] * x[j] for j in range(nb_projects)) for i in range(nb_scenarios)]
    z_sorted = [m.addVar(vtype=GRB.CONTINUOUS, name=f"z_sorted_{i}") for i in range(nb_scenarios)]

    # maj du modèle pour intégrer les nouvelles variables
    m.update()

    # definition de l'ojectif (maximiser ∑(k=1 to n) w'_k * (k * r_k - ∑(i=1 to n) b_ik))
    # on fait k in range(1, n+1) car on fait k * r_k!!!
    m.setObjective(
        quicksum(w_prime[k] * (k * rk[k-1] - quicksum(b[i][k-1] for i in range(nb_scenarios))) for k in range(1, nb_scenarios + 1)),
        GRB.MAXIMIZE
    )

    # contraintes de budget
    m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")

    # Contraintes pour tri des z en ordre croissant
    for i in range(nb_scenarios):
        m.addConstr(z_sorted[i] >= z[i], name=f"SortingConstraint_{i}_greater")
        m.addConstr(z_sorted[i] <= quicksum(z[j] for j in range(i + 1)), name=f"SortingConstraint_{i}_less")

    # contrainte pour s'assurer que rk dans chaque scenario est calculé correctement
    for k in range(nb_scenarios):
        m.addConstr(
            rk[k] <= z_sorted[k],
            name=f"UtilityConstraint_{k}"
        )

    # Contraintes pour les variables duales r_k et les variables de linéarisation b_ik
    for k in range(nb_scenarios):
        for i in range(nb_scenarios):
            # r_k - b_ik <= z_sorted[i]
            m.addConstr(rk[k] - b[i][k] <= z_sorted[i], name=f"AuxiliaryConstraint_{i}_{k}")
            # b_ik >= 0 
            m.addConstr(b[i][k] >= 0, name=f"NonNeg_b_{i}_{k}")

    # Resolution 
    m.optimize()

    if verbose:
        print("\nSolution optimale:")
        for j in range(nb_projects):
            print(f"x{j + 1} = {x[j].x}")
        print("\nValeur de la fonction objectif:", m.objVal)

        # valeurs des r_k dans chaque scénario
        r_values = [rk[k].x for k in range(nb_scenarios)]
        print("Valeurs des r_k dans chaque scénario:", r_values)
        
        print("w'_k:", w_prime)
        print("b_ik:", [[b[i][k].x for k in range(nb_scenarios)] for i in range(nb_scenarios)])
    return
