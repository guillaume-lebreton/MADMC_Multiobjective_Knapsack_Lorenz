# Sac à dos multi-objectifs – Génération des solutions Lorenz non dominées

Ce projet porte sur la résolution du problème du sac à dos multi-objectifs et sur la génération
de l’ensemble des solutions non dominées au sens de Lorenz. Deux méthodes sont implémentées :
une méthode indirecte basée sur la programmation dynamique et une méthode directe reposant sur
la résolution itérative d’un modèle OWA.

---

## Organisation du projet


### Implémentation 
- `instance.py`  
    Lecture et représentation des instances du problème (poids, valeurs, capacité).

- `indirecte.py`  
    Implémentation de la méthode indirecte (programmation dynamique + filtrage Pareto et Lorenz).  


- `direct.py`  
    Implémentation de la méthode directe basée sur un modèle OWA résolu avec Gurobi.

### Tests
- `test.py`  
    Script de comparaison expérimentale entre les deux méthodes (temps de calcul et nombre de solutions).

        python test.py
    
    On choisis les paramètres de l'instance :  
        - un un nombre d'objectifs, p entre 2 et 6  
        - un nombre d'objets, n <= 200  
        - les poids oméga pour la méthode direct  
    Exécute et compare les 2 méthodes sur l'instance généré (à partir du fichier dans Data)

<br>
  
- `omega_test.py`  Benchmark des jeux de poids pour la méthode direct. 

        python omega_test.py 
    
    p = {2,4,6} / N adaptés au p / lambda = {0.01, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 1}  
    omega générés avec une méthode exponentielle : exp(-lambda * k) for k in range(p)  
    On éxécute 3 runs pour chaque paramètres afin de comparer les temps d'éxécutions en fonction du lambda

    Résultats dans `Resultats/Omega/results_omega.csv`  
    Plots de l'évolution des temps d'éxacution en fonction des lambdas (1 graphe par p)

<br>

- `comparaison.py`  Comparaison complètes des 2 méthodes.  

        python comparaison.py

    p = {2,3,4,5,6}, N adapté pour garder des temps d'éxécutions raisonables, lambda = 0.5
    Temps d'éxécution / #points de Pareto / #points de Lorenz
    Resultats dans `Resultats/comparaison.csv`

<br>

- `analyse_results.py` Affichage des résultats de comparaison.py.

        python analyse_resultats.py  

    Affiche pour chaque p:
        - graphe de l'evolution du temps d'éxécution des 2 méthodes en fonction de n  
        - graphe de l'evolution du nombre de points de Pareto et de Lorenz en fonction de n


### Données
- `Data/`  
    Dossier contenant les fichiers d’instances.

- `Resultats/`  
  Dossier contenant les différents csv et plots généré lors des tests (oméga ou comparaison).

---

## Prérequis

Le projet est implémenté en **Python**.

Les bibliothèques suivantes sont nécessaires :
- `numpy`
- `matplotlib` (pour la génération des figures)
- `gurobipy` (pour la méthode directe)

Le solveur **Gurobi** doit être installé et une licence valide doit être disponible pour utiliser la méthode directe.
