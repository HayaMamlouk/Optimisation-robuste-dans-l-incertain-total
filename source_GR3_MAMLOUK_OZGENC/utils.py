import random
import time
import pandas as pd
from gurobipy import Model, GRB, quicksum

def calcul_tps_resol(func, n_values, p_values, nb_instances, OWA=False):
    # stocker les résultats
    results = []

    # itérer sur les différentes combinaisons de n et p
    for n in n_values:
        for p in p_values:
            times = []
            
            for _ in range(nb_instances):
                # generer aleatoirement les couts et les utilités entre 1 et 100
                costs = [random.randint(1, 100) for _ in range(p)]
                utilities = [[random.randint(1, 100) for _ in range(p)] for _ in range(n)]
                
                # budget = 50% du cout total
                budget = int(0.5 * sum(costs))

                # generer aleatoirement les poids entre 1 et le nombre de scenarios
                if OWA:
                    weights = [random.randint(1, n+1) for _ in range(n)]

                # start timing
                start_time = time.time()
                
                if OWA:
                    # Resolution du problème de OWA
                    func(p, n, costs, utilities, budget, weights, verbose=False)
                else:
                    # appel de la fonction
                    func(p, n, costs, utilities, budget, verbose=False)

                # stocker le temps de résolution
                times.append(time.time() - start_time)

            # Calculer le temps moyen de résolution
            average_time = sum(times) / len(times) if times else None
            results.append({
                "n": n,
                "p": p,
                "average_resolution_time": average_time
            })

   
    results_df = pd.DataFrame(results)
    print(results_df)
    return 

def z_star(nb_projects, nb_scenarios, costs, utilities, budget):
    """
    Résoudre le problème de maximisation de l'utilité pour chaque scénario i
    et retourner les valeurs optimales z*_i et les valeurs des variables x_j
    pour chaque scénario i.
    
       """
    # trouver z*_i pour chaque scénario i
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
    return z_star, x_values
