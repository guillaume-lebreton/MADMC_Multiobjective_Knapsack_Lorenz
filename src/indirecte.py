'''
Methode indirecte:

Procédure en 2 phases pour déterminer l'ensemble des points Lorenz non dominés
(1) déterminer l'ensemble des points Pareto non dominés
(2) filtrer cet ensemble de points afin de ne garder que les points Lorenz non dominés
'''

from instance import Instance, pareto_dominate, lorenz_dominate, read_instance, plot_2d_points

def pareto_filter(points):
    '''
    Renvoie les points Pareto non dominés d'un ensemble de points
    '''
    result = []
    for p in points:
        if not any(pareto_dominate(q,p) for q in points if q !=p):
            result.append(p)
    return result

# 1ère étape : Pareto non dominés 

def pareto_dp(instance):
    W = instance.capacity
    p = instance.p


    # dp[w] = liste des vecteurs objectifs Pareto non dominés avec poids w
    dp = [[] for _ in range(W+1)]

    dp[0] = [tuple([0]*p)]

    for i in range(instance.n):

        wi = instance.weights[i]
        vi = instance.values[i]

        # On créer une copie de dp pour eviter de reprendre un objet deja pris
        new_dp = [list(dp[w]) for w in range(W + 1)]

        # Pour chaque poids où on pourati prendre l'objet
        for w in range(W - wi, -1, -1): # implique w + wi <= W
            # pour toute les solutions pareto
            for v in dp[w]:
                v_new = tuple(v[j] + vi[j] for j in range(p))
                new_dp[w + wi].append(v_new)
                new_dp[w + wi] = pareto_filter(new_dp[w + wi])
        
        dp = new_dp #Toute les oltuions possible avec les objet de 1 à i

    # On filtre toute les solutions trouvées
    all_points = []
    for w in range(W + 1):
        all_points.extend(dp[w])

    pareto_points = pareto_filter(all_points)

    return pareto_points

#2ème étape : Filtre au sens de Lorenz

def lorenz_filter(points):
    result = []
    for p in points:
        if not any(lorenz_dominate(q,p) for q in points if q !=p):
            result.append(p)
    return result

def methode_indirect(instance):
    pareto_points = pareto_dp(instance)
    lorenz_points = lorenz_filter(pareto_points)
    return lorenz_points

# Tests
if __name__ == "__main__":

    n = 50
    p = 2
    instance = read_instance("2KP200-TA-0.dat", n, p)
    print(f"Test sur une instance de {n} objets et {p} objectifs")

    pareto_points = pareto_dp(instance)
    print(f"On obtient {len(pareto_points)} points Pareto non dominés")
    plot_2d_points(pareto_points)

    lorenz_points = lorenz_filter(pareto_points)
    print(f"On obtient {len(lorenz_points)} points Lorenz non dominés")
    print(lorenz_points)
    plot_2d_points(lorenz_points)