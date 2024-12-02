from gurobipy import Model, GRB, quicksum

def minOWA(nb_projects, nb_scenarios, costs, utilities, budget, weights, verbose=True):
    """
    Résoudre le problème de minOWA des regrets en retournant les projets sélectionnés dans l'ordre initial.
    """
    # Étape 1 : Calcul de z_star
    z_star = []
    x_values = []

    for i in range(nb_scenarios):
        # Initialisation du modèle
        m = Model(f"OptimalUtility_Scenario_{i}")
        m.setParam('OutputFlag', 0)

        # Déclaration des variables
        x = [m.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(nb_projects)]

        # Définition de l'objectif
        m.setObjective(quicksum(utilities[i][j] * x[j] for j in range(nb_projects)), GRB.MAXIMIZE)

        # Contrainte du budget
        m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")

        # Résolution
        m.optimize()

        # Stocker la valeur optimale de z_i
        z_star.append(m.objVal)
        x_values.append([x[j].x for j in range(nb_projects)])

    # Étape 2 : Résolution du problème minOWA des regrets
    sorted_weights = sorted(weights, reverse=True)
    w_prime = [sorted_weights[i] - sorted_weights[i + 1] if i < len(weights) - 1 else sorted_weights[i]
            for i in range(len(weights))]

    m = Model("minOWA_of_regrets")
    m.setParam('OutputFlag', 0)

    # Déclaration des variables
    x = [m.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(nb_projects)]
    rk = [m.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(nb_scenarios)]
    b = [[m.addVar(vtype=GRB.CONTINUOUS, name=f"b_{i}_{k}") for k in range(nb_scenarios)] for i in range(nb_scenarios)]

    # Définition de l'objectif
    m.setObjective(
        quicksum((w_prime[k] * (((k+1) * rk[k]) + (quicksum(b[i][k] for i in range(nb_scenarios))))) 
                for k in range(nb_scenarios)), GRB.MINIMIZE
    )

    # Contrainte du budget
    m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")

    

    # Contraintes sur les regrets et linéarisation
    for k in range(nb_scenarios):
        for i in range(nb_scenarios):
            m.addConstr(rk[k] - b[i][k] >= (z_star[i] - quicksum(utilities[i][j] * x[j] for j in range(nb_projects))), name=f"AuxiliaryConstraint_{i}_{k}")
            m.addConstr(b[i][k] >= 0, name=f"Neg_b_{i}_{k}")

    # Résolution
    m.optimize()

    # Affichage des résultats
    if verbose:
        print("Solution optimale:")
        for j in range(nb_projects):
            print(f"x{j + 1} = {x[j].x}")
        print ("regrets:") 
        for i in range(nb_scenarios):
            print("z_star_", i + 1, "=", z_star[i])
            print(f"regret_{i + 1} = {z_star[i] - quicksum(utilities[i][j] * x[j].x for j in range(nb_projects))}") 
        print("\nValeur de la fonction objectif:", m.objVal)
        r_values = [rk[k].x for k in range(nb_scenarios)]
        print("Valeurs des r_k dans chaque scénario:", r_values)
        print("w'_k:", w_prime)
        print("b_ik:", [[b[i][k].x for k in range(nb_scenarios)] for i in range(nb_scenarios)])

