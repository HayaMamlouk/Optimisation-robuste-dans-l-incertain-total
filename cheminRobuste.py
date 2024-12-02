import gurobipy as gp
from gurobipy import *
from cheminPlusRapide import *

def robust_shortest_path_maxmin(nodes, arcs, start, end, scenarios):
    """
    Résout le problème du chemin robuste en utilisant l'approche MaxMin.

    Paramètres :
    - nodes : liste des nœuds du graphe.
    - arcs : dictionnaire {(i, j): [t_s1, t_s2, ...]} représentant les temps de trajet pour chaque arc et chaque scénario.
    - start : nœud de départ.
    - end : nœud d'arrivée.
    - scenarios : nombre de scénarios.

    Retourne :
    - Le chemin robuste optimal et sa durée maximale.
    """
    # Création du modèle
    model = gp.Model("RobustShortestPath_MaxMin")
    model.setParam('OutputFlag', 0)  # Désactiver les sorties de Gurobi

    # Variables de décision : x_ij = 1 si l'arc (i, j) est sélectionné, 0 sinon
    x = model.addVars(arcs.keys(), vtype=GRB.BINARY, name="x")

    # Variable t représentant la valeur minimale des temps de trajet négatifs
    z = model.addVar(vtype=GRB.CONTINUOUS, name="z")

    model.update()
    model.setObjective(z, GRB.MAXIMIZE)

    # Flow constraints
    # Source node
    model.addConstr(
        quicksum(x[(start, j)] for j in nodes if (start, j) in arcs) -
        quicksum(x[(i, start)] for i in nodes if (i, start) in arcs) == 1,
        "flow_source"
    )

    # Destination node
    model.addConstr(
        quicksum(x[(end, j)] for j in nodes if (end, j) in arcs) -
        quicksum(x[(i, end)] for i in nodes if (i, end) in arcs) == -1,
        "flow_destination"
    )

    # Flow conservation for intermediate nodes
    for v in nodes:
        if v != start and v != end:
            model.addConstr(
                quicksum(x[(v, j)] for j in nodes if (v, j) in arcs) -
                quicksum(x[(i, v)] for i in nodes if (i, v) in arcs) == 0,
                f"flow_{v}"
            )

    # Contraintes pour z
    for arc,_ in arcs.items():
        for s in range(scenarios):
            model.addConstr(z <= gp.quicksum(-arcs[i, j][s] * x[i, j] for i, j in arcs), f"time_scenario_{s}")

    # Résolution du modèle
    model.optimize()

    # Extraction du chemin optimal
    
    if model.status == GRB.OPTIMAL:
    # Access variable values
        selected_arcs = [arc for arc in arcs if x[arc].x > 0.5]
        return selected_arcs, -z.x  # Retourner la valeur positive du temps
    else:
        print(f"Optimization was unsuccessful. Status code: {model.status}")
        return None, None
    

def robust_shortest_path_minmax_regret(nodes, arcs, start, end, scenarios):
    """
    Solves the Min-Max Regret robust shortest path problem.

    Parameters:
    - nodes: List of nodes in the graph.
    - arcs: Dictionary {(i, j): [t_s1, t_s2, ...]} with travel times for each arc under each scenario.
    - start: Starting node.
    - end: Destination node.
    - scenarios: Number of scenarios.

    Returns:
    - Optimal path minimizing the maximum regret and the corresponding regret value.
    """
    # Step 1: Compute optimal path costs for each scenario
    z_star = []
    # for s in range(scenarios):
    #     result = chemin_plus_rapide(nodes, arcs, start, end, s)
    #     cost = result['cost']
    #     z_star.append(cost)

    print("The shortest path costs for each scenario are:")
    print(z_star)
    print()
    
    # Step 2: Solve the Min-Max Regret problem
    model = gp.Model("MinMax_Regret_Shortest_Path")
    model.setParam('OutputFlag', 0)

    x = model.addVars(arcs.keys(), vtype=GRB.BINARY, name="x")
    regret_max = model.addVar(vtype=GRB.CONTINUOUS, name="regret_max")
    model.setObjective(regret_max, GRB.MINIMIZE)

    # for i in range(nb_scenarios):
    #     regret = z_star[i] - quicksum(utilities[i][j] * x[j] for j in range(nb_projects))
    #     m.addConstr(t >= regret, "regret_constraint_%d" % (i + 1))
    
    # Regret constraints for each scenario
    for s in range(scenarios):
        regret = z_star[s] - quicksum(arcs[arc][s] * x[arc] for arc in arcs)
        model.addConstr(regret_max >= regret, name=f"regret_scenario_{s}")
    
    # Flow conservation constraints
    for node in nodes:
        inflow = quicksum(x[i, node] for i in nodes if (i, node) in arcs)
        outflow = quicksum(x[node, j] for j in nodes if (node, j) in arcs)
        if node == start:
            model.addConstr(outflow - inflow == 1, name=f"flow_{node}")
        elif node == end:
            model.addConstr(inflow - outflow == 1, name=f"flow_{node}")
        else:
            model.addConstr(inflow - outflow == 0, name=f"flow_{node}")
    
    model.optimize()
    
    if model.status == GRB.OPTIMAL:
        selected_arcs = [arc for arc in arcs if x[arc].x > 0.5]
        return selected_arcs, model.objVal
    else:
        raise ValueError("Optimal robust path not found.")



# Exemple d'utilisation
nodes = ['a', 'b', 'c', 'd', 'e', 'f']
arcs = {
    ('a', 'b'): [4, 3], ('a', 'c'): [5, 1],
    ('b', 'c'): [2, 1], ('b', 'd'): [1, 4], ('b', 'e'): [2, 2], ('b', 'f'): [7, 5],
    ('c', 'd'): [5, 1], ('c', 'e'): [2, 7],
    ('d', 'f'): [3, 2],
    ('e', 'f'): [5, 2]
}
start_node = 'a'
end_node = 'f'
num_scenarios = 2

path, max_time = robust_shortest_path_maxmin(nodes, arcs, start_node, end_node, num_scenarios)
print(f"Chemin robuste (MaxMin) : {path}")
print(f"Temps maximal sur le chemin : {max_time}")

# path, max_regret = robust_shortest_path_minmax_regret(nodes, arcs, start_node, end_node, num_scenarios)
# print(f"Chemin robuste (MinMax Regret) : {path}")
# print(f"Regret maximal sur le chemin : {max_regret}")
