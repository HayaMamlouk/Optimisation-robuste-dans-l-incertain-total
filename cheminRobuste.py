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
    model.setObjective(z, GRB.MINIMIZE)

    # Flow constraints
    # Source node
    for node in nodes:
        inflow = quicksum(x[(i, node)] for i in nodes if (i, node) in arcs)
        outflow = quicksum(x[(node, j)] for j in nodes if (node, j) in arcs)
        if node == start:
            model.addConstr(outflow - inflow == 1, name=f"flow_{node}")
        elif node == end:
            model.addConstr(inflow - outflow == 1, name=f"flow_{node}")
        else:
            model.addConstr(inflow - outflow == 0, name=f"flow_{node}")

    # for i in range(nb_scenarios):
    #     m.addConstr(t <= quicksum(utilities[i][j] * x[j] for j in range(nb_projects)), "scenario_%d" % (i + 1))

    # Contraintes pour z
    for s in range(scenarios):
        # Extract weights for the selected scenario
        weights = {arc: costs[s] for arc, costs in arcs.items()}
        # weights_negative = {key: value * -1 for key, value in weights.items()}
        model.addConstr(z >= quicksum(weights[arc] * x[arc] for arc in arcs), f"time_scenario_{s}")

    # Résolution du modèle
    model.optimize()

    # Extraction du chemin optimal
    
    if model.status == GRB.OPTIMAL:
    # Access variable values
        selected_arcs = [arc for arc in arcs if x[arc].x > 0.5]
        return selected_arcs, z.x  # Retourner la valeur positive du temps
    else:
        print(f"Optimization was unsuccessful. Status code: {model.status}")
        return None, None
    

def robust_shortest_path_minmax_regret(nodes, arcs, start, end, scenarios):
    """
    Résout le problème de chemin le plus court Min-Max Regret robuste.

    Paramètres :
    - nodes : Liste des nœuds du graphe.
    - arcs : Dictionnaire {(i, j): [t_s1, t_s2, ...]} avec les temps de trajet pour chaque arc sous chaque scénario.
    - start : Nœud de départ.
    - end : Nœud de destination.
    - scenarios : Nombre de scénarios.

    Retourne :
    - Le chemin optimal minimisant le regret maximal et la valeur de regret correspondante.
    """

    
    # Étape 1 : Calculer les coûts du chemin optimal pour chaque scénario
    z_star = []
    for s in range(scenarios):
        result = chemin_plus_rapide(nodes, arcs, start, end, s)
        cost = result['cost']
        z_star.append(cost)

    # print("Les coûts des chemins les plus courts pour chaque scénario sont :")
    # print(z_star)
    # print()
    
    # Étape 2 : Résoudre le problème Min-Max Regret
    model = gp.Model("MinMax_Regret_Shortest_Path")
    model.setParam('OutputFlag', 0)

    x = model.addVars(arcs.keys(), vtype=GRB.BINARY, name="x")
    regret_max = model.addVar(vtype=GRB.CONTINUOUS, name="regret_max")
    model.setObjective(regret_max, GRB.MINIMIZE)
    
    # Contraintes de regret pour chaque scénario

    for s in range(scenarios):
        weights = {arc: costs[s] for arc, costs in arcs.items()}
        regret = quicksum(weights[arc] * x[arc] for arc in arcs) - z_star[s]
        model.addConstr(regret_max >= regret, name=f"regret_scenario_{s}")
    
    # Contraintes de conservation du flux
    for node in nodes:
        inflow = quicksum(x[(i, node)] for i in nodes if (i, node) in arcs)
        outflow = quicksum(x[(node, j)] for j in nodes if (node, j) in arcs)
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
        raise ValueError("Chemin robuste optimal non trouvé.")

def robust_shortest_path_maxOWA(nodes, transitions, start, end, scenarios, weights):
    """
    Résoudre le problème de chemin robuste en utilisant MaxOWA.

    Paramètres :
    - nodes : liste des nœuds du graphe.
    - transitions : dictionnaire {(i, j): (t_s1, t_s2, ...)} représentant les temps de trajet pour chaque arc et chaque scénario.
    - start : nœud de départ.
    - end : nœud d'arrivée.
    - scenarios : nombre de scénarios.
    - weights : vecteur de pondération pour MaxOWA (e.g., [k, 1]).

    Retourne :
    - Le chemin robuste optimal et sa valeur de fonction objectif.
    """
    # Trier les poids en ordre décroissant
    sorted_weights = sorted(weights, reverse=True)

    # Transformer les poids w'_k = (w_k - w_{k+1}) pour k = 1 à n-1
    w_prime = [sorted_weights[i] - sorted_weights[i + 1] if i < len(weights) - 1 else sorted_weights[i] for i in range(len(weights))]

    # Initialisation du modèle
    model = Model("RobustShortestPath_MaxOWA")
    model.setParam('OutputFlag', 0)  # Désactiver les logs de Gurobi

    # Variables de décision : x_ij = 1 si l'arc (i, j) est sélectionné, 0 sinon
    x = model.addVars(transitions.keys(), vtype=GRB.BINARY, name="x")

    # Variables rk (variables duales) (n variables)
    rk = [model.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(scenarios)]

    # Variables b_ik (variables de linéarisation) (n^2 variables)
    b = [[model.addVar(vtype=GRB.CONTINUOUS, name=f"b_{i}_{k}") for k in range(scenarios)] for i in range(scenarios)]

    # Mise à jour du modèle pour intégrer les nouvelles variables
    model.update()

    # Définition de l'objectif : maximiser ∑(k=1 to n) w'_k * (k * r_k - ∑(i=1 to n) b_ik)
    model.setObjective(
        quicksum((w_prime[k] * ((k + 1) * rk[k] - quicksum(b[i][k] for i in range(scenarios))))
                 for k in range(scenarios)),
        GRB.MAXIMIZE
    )

    # Contraintes de flux pour assurer un chemin valide
    # Source node
    for node in nodes:
        inflow = quicksum(x[(i, node)] for i in nodes if (i, node) in transitions)
        outflow = quicksum(x[(node, j)] for j in nodes if (node, j) in transitions)
        if node == start:
            model.addConstr(outflow - inflow == 1, name=f"flow_{node}")
        elif node == end:
            model.addConstr(inflow - outflow == 1, name=f"flow_{node}")
        else:
            model.addConstr(inflow - outflow == 0, name=f"flow_{node}")

    # Contraintes pour les variables rk et b_ik
    for k in range(scenarios):
        for i in range(scenarios):
            # rk - b_ik <= -z_i(x)
            model.addConstr(
                rk[k] - b[i][k] <= quicksum(transitions[arc][i] * x[arc] for arc in transitions),
                name=f"AuxiliaryConstraint_{i}_{k}"
            )
            # b_ik >= 0
            model.addConstr(b[i][k] >= 0, name=f"NonNeg_b_{i}_{k}")

    # Résolution
    model.optimize()

    if model.status == GRB.OPTIMAL:
        selected_arcs = [arc for arc in transitions if x[arc].x > 0.5]
        print("\nSolution optimale:")
        print(f"Chemin sélectionné: {selected_arcs}")
        print(f"Valeur de la fonction objectif: {model.objVal}")

        # Valeurs des rk
        r_values = [rk[k].x for k in range(scenarios)]
        print("Valeurs des rk:", r_values)

        return selected_arcs, model.objVal
    else:
        print(f"Optimization was unsuccessful. Status code: {model.status}")
        return None, None

def robust_shortest_path_minOWA(nodes, transitions, start, end, scenarios, weights):
    """
    Résoudre le problème de chemin robuste en utilisant minOWA pour les regrets.

    Paramètres :
    - nodes : liste des nœuds du graphe.
    - transitions : dictionnaire {(i, j): (t_s1, t_s2, ...)} représentant les temps de trajet pour chaque arc et chaque scénario.
    - start : nœud de départ.
    - end : nœud d'arrivée.
    - scenarios : nombre de scénarios.
    - weights : vecteur de pondération pour minOWA.

    Retourne :
    - Le chemin robuste optimal et sa valeur de fonction objectif.
    """
    # Étape 1 : Calcul de z_star pour chaque scénario (chemin optimal par scénario)
    z_star = []
    paths = []

    for s in range(scenarios):
        result = chemin_plus_rapide(nodes, transitions, start, end, s)
        cost = result['cost']
        z_star.append(cost)

    # Étape 2 : Résolution du problème minOWA des regrets
    # Transformation des poids w'_k
    sorted_weights = sorted(weights, reverse=True)
    w_prime = [sorted_weights[i] - sorted_weights[i + 1] if i < len(weights) - 1 else sorted_weights[i]
               for i in range(len(weights))]

    # Initialisation du modèle minOWA
    model = Model("minOWA_of_regrets")
    model.setParam('OutputFlag', 0)

    # Variables de décision : x_ij = 1 si l'arc (i, j) est sélectionné, 0 sinon
    x = model.addVars(transitions.keys(), vtype=GRB.BINARY, name="x")

    # Variables rk (variables duales) (n variables)
    rk = [model.addVar(vtype=GRB.CONTINUOUS, name=f"r_{k}") for k in range(scenarios)]

    # Variables b_ik (variables de linéarisation) (n^2 variables)
    b = [[model.addVar(vtype=GRB.CONTINUOUS, name=f"b_{i}_{k}") for k in range(scenarios)] for i in range(scenarios)]

    # Définition de l'objectif : minimiser l'OWA des regrets
    model.setObjective(
        quicksum((w_prime[k] * ((k + 1) * rk[k] + quicksum(b[i][k] for i in range(scenarios))))
                 for k in range(scenarios)),
        GRB.MINIMIZE
    )

    # Contraintes de flux pour assurer un chemin valide
    for node in nodes:
        inflow = quicksum(x[(i, node)] for i in nodes if (i, node) in transitions)
        outflow = quicksum(x[(node, j)] for j in nodes if (node, j) in transitions)
        if node == start:
            model.addConstr(outflow - inflow == 1, name=f"flow_{node}")
        elif node == end:
            model.addConstr(inflow - outflow == 1, name=f"flow_{node}")
        else:
            model.addConstr(inflow - outflow == 0, name=f"flow_{node}")

    # Contraintes sur les regrets et linéarisation
    for k in range(scenarios):
        for i in range(scenarios):
            model.addConstr(
                rk[k] - b[i][k] >= z_star[i] - quicksum(transitions[arc][i] * x[arc] for arc in transitions),
                name=f"AuxiliaryConstraint_{i}_{k}"
            )
            model.addConstr(b[i][k] >= 0, name=f"Neg_b_{i}_{k}")

    # Résolution
    model.optimize()

    if model.status == GRB.OPTIMAL:
        selected_arcs = [arc for arc in transitions if x[arc].x > 0.5]
        print("\nSolution optimale:")
        print(f"Chemin sélectionné: {selected_arcs}")
        print(f"Valeur de la fonction objectif: {model.objVal}")

        # Valeurs des rk
        r_values = [rk[k].x for k in range(scenarios)]
        print("Valeurs des rk:", r_values)
        return selected_arcs, model.objVal
    else:
        print(f"Optimization failed. Status code: {model.status}")
        return None, None

