from maxmin import maxmin
from minmaxRegret import minmaxRegret
from tps_resol import calcul_tps_resol
from maxOWA import maxOWA
from myData import *




# Résoudre le problème de maxmin
# maxmin(n_projects, n_scenarios, costs, utilities, budget)

# Résoudre le problème de minimisation du regret maximal
# minmaxRegret(n_projects, n_scenarios, costs, utilities, budget, False)

# Probleme maxmin : Calculer le temps de résolution pour les différentes combinaisons de n et p
# calcul_tps_resol(maxmin, n_values, p_values, nb_instances)

# Probleme minmaxRegret : Calculer le temps de résolution pour les différentes combinaisons de n et p
# calcul_tps_resol(minmaxRegret, n_values, p_values, nb_instances)

maxOWA(n_projects, n_scenarios, costs, utilities, budget, weights)

