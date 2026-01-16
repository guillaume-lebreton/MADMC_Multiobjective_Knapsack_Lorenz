'''
Methode indirecte:

Procédure en 2 phases pour déterminer l'ensemble des points Lorenz non dominés
(1) déterminer l'ensemble des points Pareto non dominés
(2) filtrer cet ensemble de points afin de ne garder que les points Lorenz non dominés
'''

from instance import pareto_dominate, lorenz_dominate, read_instance, plot_2d_points, lorenz_vector
import numpy as np

def pareto_insert(points, new):
    '''
    Insère un point (new) dans un front de Pareto (points) et le met à jour
    '''
    # On vérifie déjà que le point n'est pas déjà dans le front
    points_set = set(points) #plus rapide avec un set
    if new in points_set:
        return points
    
    front = []

    for p in points:
        if pareto_dominate(p, new): #Le nouveau point est dominé -> on garde l'ancien front
            return points
        if not pareto_dominate(new, p): #On garde les points du front non dominé par le nouveau
            front.append(p)

    #Le nouveau point n'est dominé par aucun point du front -> on l'ajoute au front
    front.append(new)

    return front

# 1ère étape : Pareto non dominés 

def pareto_dp(instance, verbose=False):
    W = instance.capacity
    p = instance.p

    # dp[w] = liste des vecteurs objectifs Pareto non dominés avec poids w
    dp = [[] for _ in range(W+1)]
    dp[0] = [tuple([0]*p)]

    for i in range(instance.n):
        if verbose:
            print(f"Objet {i} -> {np.sum(len(dp[w]) for w in range(W+1))} points dans la table")

        wi = instance.weights[i]
        vi = instance.values[i]

        # Pour chaque poids où on pourrait prendre l'objet
        for w in range(W - wi, -1, -1): # implique w + wi <= W
            for v in dp[w]:
                v_new = tuple(v[j] + vi[j] for j in range(p))
                dp[w + wi] = pareto_insert(dp[w + wi], v_new)

    # On filtre toute les solutions trouvées
    pareto_points = []
    for w in range(W + 1): #pour tout les poids
        for v in dp[w]:
            pareto_points = pareto_insert(pareto_points, v)

    return pareto_points

#2ème étape : Filtre au sens de Lorenz

def lorenz_filter(points):
    '''
    Filtre les points pour ne garder que les Lorenz non dominés
    '''
    lorenz_front = []
    best_points = []

    # construction incrémentale du front de Lorenz
    for p in points:
        L = lorenz_vector(p)
        lorenz_front = pareto_insert(lorenz_front, L)

    # on garde les points dont le Lorenz est dans le front
    lorenz_set = set(lorenz_front)
    for p in points:
        if lorenz_vector(p) in lorenz_set:
            best_points.append(p)

    return best_points

def methode_indirecte(instance, verbose=True):
    pareto_points = pareto_dp(instance, verbose)
    lorenz_points = lorenz_filter(pareto_points)
    return pareto_points, lorenz_points

# Tests
if __name__ == "__main__":

    n = 150
    p = 2
    instance = read_instance("Data/2KP200-TA-0.dat", n, p)
    print(f"Test sur une instance de {n} objets et {p} objectifs")

    pareto_points, lorenz_points = methode_indirecte(instance, verbose=True)
    print(f"On obtient : \n - {len(pareto_points)} points Pareto non dominés")
    print(f" - {len(lorenz_points)} points Lorenz non dominés")
    plot_2d_points(pareto_points)
    plot_2d_points(lorenz_points)