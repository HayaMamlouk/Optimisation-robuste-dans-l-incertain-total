from gurobipy import Model, GRB, quicksum

def chemin_plus_rapide(nodes, transitions, start, end, scenario):
    """
    Solves the shortest path problem for a single scenario using Gurobi.

    Parameters:
        nodes (list): List of nodes in the graph.
        transitions (dict): Dictionary where keys are edges (i, j) and values are tuples (t_s1, t_s2, ...).
        start (str): Starting node.
        end (str): Destination node.
        scenario (int): Scenario index to solve for.

    Returns:
        dict: Solution with selected path and total cost.
    """
    # Extract weights for the selected scenario
    weights = {arc: costs[scenario] for arc, costs in transitions.items()}

    # Create Gurobi model
    model = Model("ShortestPath")
    model.setParam("OutputFlag", 0)  # Suppress Gurobi output

    # Decision variables: x[i, j] = 1 if arc (i, j) is in the solution, 0 otherwise
    x = model.addVars(transitions.keys(), vtype=GRB.BINARY, name="x")

    # Objective function: Minimize total cost
    model.setObjective(quicksum(weights[arc] * x[arc] for arc in transitions), GRB.MINIMIZE)

    # Flow constraints
    # Source node
    model.addConstr(
        quicksum(x[(start, j)] for j in nodes if (start, j) in transitions) -
        quicksum(x[(i, start)] for i in nodes if (i, start) in transitions) == 1,
        "flow_source"
    )

    # Destination node
    model.addConstr(
        quicksum(x[(end, j)] for j in nodes if (end, j) in transitions) -
        quicksum(x[(i, end)] for i in nodes if (i, end) in transitions) == -1,
        "flow_destination"
    )

    # Flow conservation for intermediate nodes
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


# Example Usage

# Define Instance 1
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

# Solve Instance 1
print("Instance 1 Results:")
for scenario in range(2):  # Two scenarios
    result = chemin_plus_rapide(nodes1, transitions1, start1, end1, scenario)
    print(f"Instance 1, Scenario {scenario}:")
    if "cost" in result:
        print(f"Path: {result['path']}")
        print(f"Total Cost: {result['cost']}\n")
    else:
        print(result["message"])


# Define Instance 2
nodes2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
transitions2 = {
    ('a', 'b'): (5, 3), ('a', 'c'): (10, 4), ('a', 'd'): (2, 6),
    ('b', 'c'): (4, 2), ('b', 'd'): (1, 3), ('b', 'e'): (4, 6),
    ('c', 'e'): (3, 1), ('c', 'f'): (1, 2),
    ('d', 'c'): (1, 4), ('d', 'f'): (3, 5),
    ('e', 'g'): (1, 1),
    ('f', 'g'): (1, 1)
}
start2 = 'a'
end2 = 'g'

# Solve Instance 2
print("\nInstance 2 Results:")
for scenario in range(2):  # Two scenarios
    result = chemin_plus_rapide(nodes2, transitions2, start2, end2, scenario)
    print(f"Instance 2, Scenario {scenario}:")
    if "cost" in result:
        print(f"Path: {result['path']}")
        print(f"Total Cost: {result['cost']}\n")
    else:
        print(result["message"])
