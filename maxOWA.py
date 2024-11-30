from gurobipy import Model, GRB, quicksum

def maxOWA(nb_projects, nb_scenarios, costs, utilities, budget, weights, verbose=True):
    """
    Solve the maxOWA problem using linearization.
    """
    # Number of weights must match the number of scenarios
    assert len(weights) == nb_scenarios, "The number of weights must match the number of scenarios."

    # Sort weights in descending order
    sorted_weights = sorted(weights, reverse=True)

    # Transform weights for OWA linearization
    w_prime = [sorted_weights[i] - sorted_weights[i + 1] if i < len(weights) - 1 else sorted_weights[i]
               for i in range(len(weights))]

    # Initialize the model
    m = Model("maxOWA")

    # Decision variables: binary x_j for project selection
    x = [m.addVar(vtype=GRB.BINARY, name=f"x_{j}") for j in range(nb_projects)]

    # Regret variables r_k for ordered utilities
    rk = [m.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(nb_scenarios)]

    # Auxiliary variables b_ik for linearization
    b = [[m.addVar(vtype=GRB.CONTINUOUS, name=f"b_{i}_{k}") for k in range(nb_scenarios)] for i in range(nb_scenarios)]

    # Update model with variables
    m.update()

    # Objective function: maximize weighted sum of ordered utilities
    m.setObjective(
        quicksum(w_prime[k] * (k * rk[k] - quicksum(b[i][k] for i in range(nb_scenarios))) for k in range(nb_scenarios)),
        GRB.MAXIMIZE
    )

    # Constraints for budget
    m.addConstr(quicksum(costs[j] * x[j] for j in range(nb_projects)) <= budget, "Budget")

    # Constraints for utilities in scenarios
# Constraints for utilities in scenarios
    for k in range(nb_scenarios):
        m.addConstr(
            rk[k] <= quicksum(utilities[k][j] * x[j] for j in range(nb_projects)),
            name=f"UtilityConstraint_{k}"
        )
    for i in range(nb_scenarios):
        m.addConstr(
            rk[k] - b[i][k] <= quicksum(utilities[k][j] * x[j] for j in range(nb_projects)),
            name=f"AuxiliaryConstraint_{i}_{k}"
        )
        m.addConstr(b[i][k] >= 0, name=f"NonNeg_b_{i}_{k}")


    # Solve the model
    m.optimize()

    if verbose:
        # Print results
        print("Optimal solution found:")
        for j in range(nb_projects):
            print(f"Project {j + 1}: Selected" if x[j].x > 0.5 else f"Project {j + 1}: Not selected")
        print("Objective value (maxOWA):", m.objVal)

        # Calculate and print utilities in scenarios
        utilities_result = [sum(utilities[i][j] * x[j].x for j in range(nb_projects)) for i in range(nb_scenarios)]
        print("Utilities in scenarios:", utilities_result)

    return m.objVal