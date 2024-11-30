import random
import time
import pandas as pd
from maxmin import maxmin
from gurobipy import Model, GRB, quicksum
from myData import n_values, p_values, nb_instances

def calcul_tps_resol(func, n_values, p_values, nb_instances):
    # Store results
    results = []

    # Loop over n and p values
    for n in n_values:
        for p in p_values:
            times = []
            
            for _ in range(nb_instances):
                # Generate random costs and utilities
                costs = [random.randint(1, 100) for _ in range(p)]
                utilities = [[random.randint(1, 100) for _ in range(p)] for _ in range(n)]
                
                # Define budget as 50% of the total cost
                budget = int(0.5 * sum(costs))
                
                # Start timing
                start_time = time.time()
                
                # Create the model
                func(p, n, costs, utilities, budget, verbose=False)

                # Record the resolution time
                times.append(time.time() - start_time)

            # Calculate average time for this (n, p) combination
            average_time = sum(times) / len(times) if times else None
            results.append({
                "n": n,
                "p": p,
                "average_resolution_time": average_time
            })

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Save results to a CSV file
    results_df.to_csv("knapsack_resolution_times.csv", index=False)

    # Display the results
    print(results_df)
    return results_df

calcul_tps_resol(maxmin, n_values, p_values, nb_instances)