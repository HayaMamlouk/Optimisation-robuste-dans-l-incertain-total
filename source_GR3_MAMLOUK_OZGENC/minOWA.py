from gurobipy import Model, GRB, quicksum
import utils as ut

def minOWA(nb_projects, nb_scenarios, costs, utilities, budget, weights, verbose=True):
    """
    Résoudre le problème de minOWA des regrets en retournant les projets sélectionnés dans l'ordre initial.
    """
    # etape 1 : Calcul de z_star
    z_star, x_values = ut.z_star(nb_projects, nb_scenarios, costs, utilities, budget)

    # etape 2 : Résolution du problème minOWA des regrets
    sorted_weights = sorted(weights, reverse=True)
    w_prime = [sorted_weights[i] - sorted_weights[i + 1] if i < len(weights) - 1 else sorted_weights[i]
            for i in range(len(weights))]

    m = Model("minOWA_of_regrets")
    m.setParam('OutputFlag', 0)
    
    # declaration des variables de decision, x_j = 1 si le projet j est sélectionné, 0 sinon
    x = [m.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(nb_projects)]

    # variable rk (variables duales) (n variables)
    rk = [m.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(nb_scenarios)]

    # variable b_ik (variables de linéarisation) (n^2 variables)
    b = [[m.addVar(vtype=GRB.CONTINUOUS, name=f"b_{i}_{k}") for k in range(nb_scenarios)] for i in range(nb_scenarios)]


    # definition de l'objectif
    m.setObjective(
        quicksum((w_prime[k] * (((k+1) * rk[k]) + (quicksum(b[i][k] for i in range(nb_scenarios))))) 
                for k in range(nb_scenarios)), GRB.MINIMIZE
    )

    # contrainte du budget
    m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")

    

    # contraintes sur les regrets et linéarisation
    for k in range(nb_scenarios):
        for i in range(nb_scenarios):
            m.addConstr(rk[k] - b[i][k] >= (z_star[i] - quicksum(utilities[i][j] * x[j] for j in range(nb_projects))), name=f"AuxiliaryConstraint_{i}_{k}")
            m.addConstr(b[i][k] >= 0, name=f"Neg_b_{i}_{k}")

    # Resolution
    m.optimize()

    # affichage des resultats
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

