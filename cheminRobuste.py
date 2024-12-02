from gurobipy import Model, GRB, quicksum
from cheminPlusRapide import chemin_plus_rapide

def chemin_robuste(nodes, transitions, start, end, weights, k_values, function="maximin"):
    """
    Solves the robust path problem using different robust functions.
    """
    scenarios = len(next(iter(transitions.values())))  # Number of scenarios
    costs = {arc: transitions[arc] for arc in transitions}

    # Precompute optimal paths per scenario for minimax regret
    shortest_paths = []
    for scenario in range(scenarios):
        sp_result = chemin_plus_rapide(nodes, transitions, start, end, scenario)
        shortest_paths.append(sp_result["cost"] if "cost" in sp_result else float("inf"))

    # Create Gurobi model
    model = Model("RobustPath")
    model.setParam("OutputFlag", 0)  # Suppress Gurobi output

    # Decision variables: x[i, j] = 1 if arc (i, j) is in the solution, 0 otherwise
    x = model.addVars(transitions.keys(), vtype=GRB.BINARY, name="x")

    if function == "maximin":
        # Maximin: Minimize the maximum cost across all scenarios
        z = model.addVar(vtype=GRB.CONTINUOUS, name="z")
        model.setObjective(z, GRB.MINIMIZE)
        for s in range(scenarios):
            model.addConstr(z >= quicksum(costs[arc][s] * x[arc] for arc in transitions), f"Maximin_{s}")

    elif function == "minimax_regret":
        # Minimax Regret: Minimize the maximum regret
        z = model.addVar(vtype=GRB.CONTINUOUS, name="z")
        model.setObjective(z, GRB.MINIMIZE)
        for s in range(scenarios):
            regret = quicksum(costs[arc][s] * x[arc] for arc in transitions) - shortest_paths[s]
            model.addConstr(z >= regret, f"MinimaxRegret_{s}")

    elif function == "owa":
        # OWA: Minimize the weighted sum of sorted costs
        r = [model.addVar(vtype=GRB.CONTINUOUS, name=f"r_{s}") for s in range(scenarios)]
        z_sorted = [model.addVar(vtype=GRB.CONTINUOUS, name=f"z_sorted_{s}") for s in range(scenarios)]
        model.setObjective(quicksum(weights[k] * z_sorted[k] for k in range(scenarios)), GRB.MINIMIZE)

        # Calculate costs for each scenario
        for s in range(scenarios):
            model.addConstr(r[s] == quicksum(costs[arc][s] * x[arc] for arc in transitions), f"OWA_Cost_{s}")

        # Sorting constraints to link z_sorted with r
        for i in range(scenarios - 1):
            model.addConstr(z_sorted[i] >= z_sorted[i + 1], f"Sorting_{i}")
        for i in range(scenarios):
            model.addConstr(z_sorted[i] <= r[i], f"LinkSorted_{i}")

    elif function == "weighted_sum":
        # Weighted Sum: Minimize the weighted sum of costs
        model.setObjective(
            quicksum(weights[s] * quicksum(costs[arc][s] * x[arc] for arc in transitions) for s in range(scenarios)),
            GRB.MINIMIZE
        )

    # Flow constraints
    model.addConstr(
        quicksum(x[(start, j)] for j in nodes if (start, j) in transitions) -
        quicksum(x[(i, start)] for i in nodes if (i, start) in transitions) == 1,
        "flow_source"
    )
    model.addConstr(
        quicksum(x[(end, j)] for j in nodes if (end, j) in transitions) -
        quicksum(x[(i, end)] for i in nodes if (i, end) in transitions) == -1,
        "flow_destination"
    )
    for v in nodes:
        if v != start and v != end:
            model.addConstr(
                quicksum(x[(v, j)] for j in nodes if (v, j) in transitions) -
                quicksum(x[(i, v)] for i in nodes if (i, v) in transitions) == 0,
                f"flow_{v}"
            )

    # Solve the model
    model.optimize()

    # Extract the solution
    if model.status == GRB.OPTIMAL:
        selected_arcs = [arc for arc in transitions if x[arc].x > 0.5]
        solution = {
            "path": selected_arcs,
            "cost": model.objVal
        }
        return solution
    else:
        return {"message": "No optimal solution found."}

    
# Define Instances
nodes1 = ['a', 'b', 'c', 'd', 'e', 'f']
transitions1 = {
    ('a', 'b'): (4, 3), ('a', 'c'): (5, 1),
    ('b', 'c'): (2, 1), ('b', 'd'): (1, 4), ('b', 'e'): (2, 2), ('b', 'f'): (7, 5),
    ('c', 'd'): (5, 1), ('c', 'e'): (2, 7),
    ('d', 'f'): (3, 2), 
    ('e', 'f'): (5, 2)
}
start1 = 'a'
end1 = 'f'

# Define weights for OWA and Weighted Sum
weights = [2, 1]  # Example weights for OWA
k_values = [2, 4, 8, 16]  # Different k values to test

# Test Maximin
print("\n=== Maxmin Approach ===")
result_maximin = chemin_robuste(nodes1, transitions1, start1, end1, weights, k_values, function="maximin")
print(f"Path: {result_maximin.get('path', 'No solution')}")
print(f"Cost: {result_maximin.get('cost', 'N/A')}")

# Test Minimax Regret
print("\n=== Minmax Regret Approach ===")
result_minimax = chemin_robuste(nodes1, transitions1, start1, end1, weights, k_values, function="minimax_regret")
print(f"Path: {result_minimax.get('path', 'No solution')}")
print(f"Cost: {result_minimax.get('cost', 'N/A')}")

# Test OWA with different k-values
print("\n=== OWA Approach ===")
for k in k_values:
    current_weights = [k, 1]  # OWA weights
    result_owa = chemin_robuste(nodes1, transitions1, start1, end1, current_weights, k_values, function="owa")
    print(f"k = {k}:")
    print(f"  Path: {result_owa.get('path', 'No solution')}")
    print(f"  Cost: {result_owa.get('cost', 'N/A')}")

# Test Weighted Sum
print("\n=== Weighted Sum Approach ===")
result_weighted_sum = chemin_robuste(nodes1, transitions1, start1, end1, weights, k_values, function="weighted_sum")
print(f"Path: {result_weighted_sum.get('path', 'No solution')}")
print(f"Cost: {result_weighted_sum.get('cost', 'N/A')}")

