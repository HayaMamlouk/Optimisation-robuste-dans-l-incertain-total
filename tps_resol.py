import random
import time
import pandas as pd

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

