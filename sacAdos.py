import random
import time
import pandas as pd
from gurobipy import Model, GRB, quicksum

# Define n and p values
n_values = [5, 10, 15]
p_values = [10, 15, 20]
num_instances = 10

# Store results
results = []

# Loop over n and p values
for n in n_values:
    for p in p_values:
        times = []
        
        for _ in range(num_instances):
            # Generate random costs and utilities
            costs = [random.randint(1, 100) for _ in range(p)]
            utilities = [[random.randint(1, 100) for _ in range(p)] for _ in range(n)]
            
            # Define budget as 50% of the total cost
            budget = int(0.5 * sum(costs))
            
            # Start timing
            start_time = time.time()
            
            # Create the model
            try:
                model = Model("robust_knapsack")
                
                # Decision variables
                x = [model.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(p)]
                t = model.addVar(vtype=GRB.CONTINUOUS, name="max_regret")
                
                # Objective: Minimize max regret
                model.setObjective(t, GRB.MINIMIZE)
                
                # Regret constraints
                for i in range(n):
                    regret = max([utilities[i][j] for j in range(p)]) - quicksum(utilities[i][j] * x[j] for j in range(p))
                    model.addConstr(t >= regret, f"regret_constraint_{i}")
                
                # Budget constraint
                model.addConstr(quicksum(costs[j] * x[j] for j in range(p)) <= budget, "budget_constraint")
                
                # Solve the model
                model.optimize()
            except Exception as e:
                print(f"Error in solving instance: {e}")
                continue

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
