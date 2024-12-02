# Data
# Fichiers contenat les données pour les différents problèmes
##############################################################################################

# données de l'exemple 1
n_projects = 10  # nombre de projets
n_scenarios = 2  # nombre de scénarios

# coûts des projets
costs = [60, 10, 15, 20, 25, 20, 5, 15, 20, 60]

# utilités des projets dans chaque scénario
utilities = [
    [70, 18, 16, 14, 12, 10, 8, 6, 4, 2],  # Scenario 1
    [2, 4, 6, 8, 10, 12, 14, 16, 18, 70]   # Scenario 2
]

# budget maximal
budget = 100

##############################################################################################

# données pour l'evaluation du temps de résolution
n_values = [5, 10, 15]  # nombre de scénarios
p_values = [10, 15, 20] # nombre de projets
nb_instances = 10      # nombre d'instances à génére

##############################################################################################

# poids des objectifs pour OWA
weights = [2, 1]  # poids des objectifs pour OWA 

##############################################################################################

# données pour le problème du chemin le plus rapide : instance 1 et 2 avec 2 scénarios

# Instance 1
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


# Instance 2

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
