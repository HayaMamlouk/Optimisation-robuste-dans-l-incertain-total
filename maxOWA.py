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

    # maj du modele pour integrer les nouvelles variables
    m.update()

    # definition de l'ojectif (maximiser ∑(k=1 to n) w'_k * (k * r_k - ∑(i=1 to n) b_ik))
    # on fait k in range(1, n+1) car on fait k * r_k!!!
    m.setObjective(
        quicksum(w_prime[k] * (k * rk[k-1] - quicksum(b[i][k-1] for i in range(nb_scenarios))) for k in range(1, nb_scenarios+1)),
        GRB.MAXIMIZE
    )

    # contraintes de budget
    m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")

    # vecteur z_i(x) = ∑(j=1 to n) u_ij * x_j
    z = [quicksum(utilities[i][j] * x[j] for j in range(nb_projects)) for i in range(nb_scenarios)]

    # variable z_sorted pour trier z
    z_sorted = [m.addVar(vtype=GRB.CONTINUOUS, name=f"z_sorted_{i}") for i in range(nb_scenarios)]

    # contraintes pour trier z
    for i in range(1, nb_scenarios):
        m.addConstr(z_sorted[i] >= z_sorted[i-1], name=f"OrderConstraint_{i}")

    # contraintes d'égalité pour z_sorted = z
    for i in range(nb_scenarios):
        m.addConstr(z_sorted[i] == z[i], name=f"EqualityConstraint_{i}")
 

    for k in range(nb_scenarios):
        for i in range(nb_scenarios):
            # rk - b_ik <= z_i(x) = ∑(j=1 to n) u_kj * x_j
            m.addConstr(
            rk[k] - b[i][k] <= z_sorted[i],
            name=f"AuxiliaryConstraint_{i}_{k}"
        )
            # b_ik >= 0 
            m.addConstr(b[i][k] >= 0, name=f"NonNeg_b_{i}_{k}")


    # Solve the model
    m.optimize()

    if verbose:
        print("w_prime : ", w_prime)
        print("z_sorted : ", [z_sorted[i].x for i in range(nb_scenarios)])
        print("\nSolution optimale:")
        for j in range(nb_projects):
            print(f"x{j+1} = {x[j].x}")
        print("\nValeur de la fonction objectif:", m.objVal)

        # valeurs de r_k dans chaque scénario
        r_values = [rk[k].x for k in range(nb_scenarios)]
        print("Valeurs de r_k dans chaque scénario:", r_values)


    return
