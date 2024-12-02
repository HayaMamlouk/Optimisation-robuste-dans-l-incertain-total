
# Projet de Résolution de Problèmes d'Optimisation

Ce projet contient des implémentations pour résoudre différents problèmes d'optimisation tels que le problème MaxMin, le problème MinMax Regret, ainsi que des calculs de temps de résolution pour ces problèmes. Le projet inclut également des résolutions pour des problèmes MaxOWA, MinOWA et de recherche de chemins les plus rapides pour deux instances.

## Prérequis

Avant d'exécuter le programme, assurez-vous d'avoir installé Python sur votre machine. Vous pouvez télécharger Python depuis [le site officiel](https://www.python.org/downloads/).

Le projet nécessite également les modules suivants :

- `gurobipy` : Interface Python pour Gurobi, le solveur d'optimisation. Vous pouvez l'installer à l'aide de la commande suivante :
  ```bash
  pip install gurobipy
  ```
  Assurez-vous également que vous disposez d'une licence valide pour Gurobi. Si vous n'en avez pas, vous pouvez obtenir une licence académique gratuite sur [le site de Gurobi](https://www.gurobi.com/downloads/).


## Exécution du Programme

Le programme principal est contenu dans le fichier `main.py`. Pour exécuter le programme, ouvrez un terminal et lancez la commande suivante :

```bash
python main.py
```

Cela lancera le programme et affichera un menu interactif où vous pourrez choisir quel problème résoudre. Vous serez invité à entrer un numéro pour sélectionner l'option souhaitée (par exemple, pour résoudre le problème MaxMin, entrez `1`).

### 3. Interface Utilisateur

Une fois que vous avez exécuté le script, vous verrez un menu affiché dans le terminal comme suit :

```
Sélectionnez le problème à résoudre :
1. Problème MaxMin
2. Problème MinMax Regret
3. Problème MaxMin : Calculer le temps de résolution
4. Problème MinMax Regret : Calculer le temps de résolution
5. Problème MaxOWA
6. Problème MinOWA
7. Problème MaxOWA : Calculer le temps de résolution
8. Problème MinOWA : Calculer le temps de résolution
9. Problème du chemin le plus rapide : Résoudre Instance 1
10. Problème du chemin le plus rapide : Résoudre Instance 2
```

Entrez un numéro entre `1` et `10` pour sélectionner un problème à résoudre. Le programme exécutera ensuite l'option choisie et affichera les résultats correspondants.

## Description des Fichiers du Projet

### 1. `main.py`

C'est le fichier principal du programme qui contient le menu interactif. Ce fichier permet à l'utilisateur de sélectionner différents problèmes à résoudre et appelle les fonctions appropriées pour chaque problème. Il gère également l'affichage des résultats dans le terminal.

### 2. `maxmin.py`

Ce fichier contient l'implémentation de l'algorithme MaxMin, qui est utilisé pour résoudre le problème MaxMin, une méthode d'optimisation dans les scénarios avec des coûts et des utilités pour différents projets.

### 3. `minmaxRegret.py`

Ce fichier contient l'implémentation de l'algorithme MinMax Regret, qui permet de résoudre le problème d'optimisation en minimisant le regret maximal. Cela permet de prendre des décisions en fonction des scénarios les plus défavorables.

### 4. `utils.py`

Ce fichier contient la fonction `calcul_tps_resol`, qui est utilisée pour calculer le temps de résolution pour les différentes combinaisons de paramètres du problème. Cette fonction est utilisée pour les problèmes MaxMin, MinMax Regret, MaxOWA, et MinOWA. Le fichier contient également la fonction `z_star`, qui est utilisée pour calculer le problème de maximisation pour un scénario donné. Cette fonction est utilisée pour les problèmes MinMax Regret et MinOWA.

Ce fichier contient l'implémentation de l'algorithme MaxOWA, une méthode d'optimisation basée sur les moyennes pondérées opérées sur les scénarios. Il permet de résoudre le problème MaxOWA.

### 6. `minOWA.py`

Ce fichier contient l'implémentation de l'algorithme MinOWA, similaire à MaxOWA, mais avec un objectif de minimisation plutôt que de maximisation. Il est utilisé pour résoudre le problème MinOWA.

### 7. `cheminPlusRapide.py`

Ce fichier contient l'implémentation du problème du chemin le plus rapide, résolvant des instances où vous devez trouver le chemin optimal entre deux points dans un graphe donné. Il est utilisé pour résoudre les problèmes de chemin dans deux instances distinctes.

### 8. `myData.py`

Ce fichier contient les données nécessaires pour résoudre les problèmes, comme les projets, les scénarios, les coûts, les utilités, et les autres paramètres associés aux différents problèmes d'optimisation. Ce fichier définit également les valeurs de départ utilisées dans le programme.
