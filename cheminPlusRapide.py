from gurobipy import Model, GRB, quicksum
from myData import nodes1, transitions1, start1, end1, nodes2, transitions2, start2, end2

def chemin_plus_rapide(nodes, transitions, start, end, scenario):

    # Create a Gurobi model
    model = Model("ShortestPath")
    model.setParam("OutputFlag", 0)  # Suppress Gurobi output

    # Decision variables: x[i, j] = 1 if arc (i, j) is in the solution, 0 otherwise
    x = {}
    for (i, j) in transitions:
        x[i, j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")

    # Objective: Minimize the total cost for the given scenario
    model.setObjective(
        quicksum(transitions[i, j][scenario] * x[i, j] for (i, j) in transitions),
        GRB.MINIMIZE
    )

    # Constraints: Flow conservation
    for node in nodes:
        if node == start:
            model.addConstr(quicksum(x[node, j] for (node, j) in transitions if node == start) -
                            quicksum(x[i, node] for (i, node) in transitions if node == start) == 1)
        elif node == end:
            model.addConstr(quicksum(x[node, j] for (node, j) in transitions if node == end) -
                            quicksum(x[i, node] for (i, node) in transitions if node == end) == -1)
        else:
            model.addConstr(quicksum(x[node, j] for (node, j) in transitions if node == node) -
                            quicksum(x[i, node] for (i, node) in transitions if node == node) == 0)

    # Solve the model
    model.optimize()

    # Extract the solution
    if model.status == GRB.OPTIMAL:
        solution = {
            "path": [(i, j) for (i, j) in transitions if x[i, j].x > 0.5],
            "cost": model.objVal
        }
        return solution
    else:
        return {"message": "No optimal solution found."}

# Example Usage

# Instance 1
result1 = chemin_plus_rapide(nodes1, transitions1, start1, end1, scenario=0)
print("Instance 1, Scenario 0:", result1)

# Instance 2
result2 = chemin_plus_rapide(nodes2, transitions2, start2, end2, scenario=1)
print("Instance 2, Scenario 1:", result2)


# Instance 1
result1 = chemin_plus_rapide(nodes1, transitions1, start1, end1, scenario=0)
print("Instance 1, Scenario 0:", result1)

# Instance 2
result2 = chemin_plus_rapide(nodes2, transitions2, start2, end2, scenario=1)
print("Instance 2, Scenario 1:", result2)