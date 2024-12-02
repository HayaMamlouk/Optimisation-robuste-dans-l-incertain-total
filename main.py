from maxmin import maxmin
from minmaxRegret import minmaxRegret
from tps_resol import calcul_tps_resol
from maxOWA import maxOWA
from minOWA import minOWA
from myData import *




# Résoudre le problème de maxmin
# maxmin(n_projects, n_scenarios, costs, utilities, budget)

# Résoudre le problème de minimisation du regret maximal
# minmaxRegret(n_projects, n_scenarios, costs, utilities, budget)

# Probleme maxmin : Calculer le temps de résolution pour les différentes combinaisons de n et p
# calcul_tps_resol(maxmin, n_values, p_values, nb_instances)

# Probleme minmaxRegret : Calculer le temps de résolution pour les différentes combinaisons de n et p
# calcul_tps_resol(minmaxRegret, n_values, p_values, nb_instances)

# Resolution du problème de maxOWA
# maxOWA(n_projects, n_scenarios, costs, utilities, budget, weights)

# Resolution du problème de minOWA
# minOWA(n_projects, n_scenarios, costs, utilities, budget, weights)

# Probleme maxOWA: Calculer le temps de résolution pour les différentes combinaisons de n et p
calcul_tps_resol(maxOWA, n_values, p_values, nb_instances, OWA=True)

# Probleme minOWA des regret : Calculer le temps de résolution pour les différentes combinaisons de n et p
calcul_tps_resol(minOWA, n_values, p_values, nb_instances, OWA=True)


