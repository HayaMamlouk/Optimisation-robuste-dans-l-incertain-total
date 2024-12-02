from maxmin import maxmin
from minmaxRegret import minmaxRegret
from utils import calcul_tps_resol
from maxOWA import maxOWA
from minOWA import minOWA
from cheminPlusRapide import chemin_plus_rapide
from cheminRobuste import robust_shortest_path_maxmin, robust_shortest_path_minmax_regret, robust_shortest_path_maxOWA, robust_shortest_path_minOWA
from myData import *

def main():
    # Afficher le menu avec les options
    print("Sélectionnez le problème à résoudre :")
    print("1. Problème MaxMin")
    print("2. Problème MinMax Regret")
    print("3. Problème MaxMin : Calculer le temps de résolution")
    print("4. Problème MinMax Regret : Calculer le temps de résolution")
    print("5. Problème MaxOWA")
    print("6. Problème MinOWA")
    print("7. Problème MaxOWA : Calculer le temps de résolution")
    print("8. Problème MinOWA : Calculer le temps de résolution")
    print("9. Problème du chemin le plus rapide : Résoudre Instance 1")
    print("10. Problème du chemin le plus rapide : Résoudre Instance 2")
    print("11. Chemin robuste (MaxMin)")
    print("12. Chemin robuste (MinMax Regret)")
    print("13. Chemin robuste (MaxOWA)")
    print("14. Chemin robuste (MinOWA)")

    # Demander à l'utilisateur de choisir un problème
    choix = input("Entrez le numéro de votre choix (1-14) : ")

    # Vérifier le choix et appeler la fonction correspondante
    if choix == "1":
        maxmin(n_projects, n_scenarios, costs, utilities, budget)
    elif choix == "2":
        minmaxRegret(n_projects, n_scenarios, costs, utilities, budget)
    elif choix == "3":
        calcul_tps_resol(maxmin, n_values, p_values, nb_instances)
    elif choix == "4":
        calcul_tps_resol(minmaxRegret, n_values, p_values, nb_instances)
    elif choix == "5":
        maxOWA(n_projects, n_scenarios, costs, utilities, budget, weights)
    elif choix == "6":
        minOWA(n_projects, n_scenarios, costs, utilities, budget, weights)
    elif choix == "7":
        calcul_tps_resol(maxOWA, n_values, p_values, nb_instances, OWA=True)
    elif choix == "8":
        calcul_tps_resol(minOWA, n_values, p_values, nb_instances, OWA=True)
    elif choix == "9":
        print("Résultats de l'Instance 1 :")
        for scenario in range(2):
            result = chemin_plus_rapide(nodes1, transitions1, start1, end1, scenario)
            print(f"Instance 1, Scénario {scenario}:")
            if "cost" in result:
                print(f"Chemin : {result['path']}")
                print(f"Coût total : {result['cost']}\n")
            else:
                print(result["message"])
    elif choix == "10":
        print("\nRésultats de l'Instance 2 :")
        for scenario in range(2):
            result = chemin_plus_rapide(nodes2, transitions2, start2, end2, scenario)
            print(f"Instance 2, Scénario {scenario}:")
            if "cost" in result:
                print(f"Chemin : {result['path']}")
                print(f"Coût total : {result['cost']}\n")
            else:
                print(result["message"])
    elif choix == "11":
        print("Test Chemin robuste (MaxMin) :")
        path, max_time = robust_shortest_path_maxmin(nodes1, transitions1, start1, end1, 2)
        print(f"Chemin robuste (MaxMin) : {path}")
        print(f"Temps maximal sur le chemin : {max_time}")
        path, max_time = robust_shortest_path_maxmin(nodes2, transitions2, start2, end2, 2)
        print(f"Chemin robuste (MaxMin) : {path}")
        print(f"Temps maximal sur le chemin : {max_time}")
    elif choix == "12":
        print("Test Chemin robuste (MinMax Regret) :")
        path, max_regret = robust_shortest_path_minmax_regret(nodes1, transitions1, start1, end1, 2)
        print(f"Chemin robuste (MinMax Regret) : {path}")
        print(f"Regret maximal sur le chemin : {max_regret}")
        path, max_regret = robust_shortest_path_minmax_regret(nodes2, transitions2, start2, end2, 2)
        print(f"Chemin robuste (MinMax Regret) : {path}")
        print(f"Regret maximal sur le chemin : {max_regret}")
    elif choix == "13":
        print("Test Chemin robuste (MaxOWA) :")
        for k in [2, 4, 8, 16]:
            w = [k, 1]
            print(f"\nRésultats pour k = {k}:")
            robust_shortest_path_maxOWA(nodes1, transitions1, start1, end1, 2, w)
        for k in [2, 4, 8, 16]:
            w = [k, 1]
            print(f"\nRésultats pour k = {k}:")
            robust_shortest_path_maxOWA(nodes2, transitions2, start2, end2, 2, w)
    elif choix == "14":
        print("Test Chemin robuste (MinOWA) :")
        for k in [2, 4, 8, 16]:
            w = [k, 1]
            print(f"\nRésultats pour k = {k}:")
            robust_shortest_path_minOWA(nodes1, transitions1, start1, end1, 2, w)
        for k in [2, 4, 8, 16]:
            w = [k, 1]
            print(f"\nRésultats pour k = {k}:")
            robust_shortest_path_minOWA(nodes2, transitions2, start2, end2, 2, w)
    else:
        print("Choix invalide ! Veuillez entrer un numéro entre 1 et 14.")

if __name__ == "__main__":
    main()
