'''
Methode directe:

- On obtient un point Lorenz non dominé en maximisant une fonction OWA
- Ajoute des contraintes pour trouvé tout les points Lorenz non dominés

'''

from instance import read_instance, lorenz_vector
import pulp

# OWA qui retourne un vecteur Lorenz non dominé 
# Pas utilisé -> équivalent à la 1ere instance de enumerate_lorenz lorsque lorenz_vectors est vide

def solve_owa(instance, omega):
    '''
    Resoud le PL OWA et retourne un point objectif Lorenz non dominé
    '''

    n = instance.n
    p = instance.p
    W = instance.capacity
    weights = instance.weights
    values = instance.values

    #Calcul des poids lambda
    lambdas = [omega[i] - omega[i+1] for i in range(p-1)] + [omega[p-1]]

    #Déclaration du pb de maximisation
    prob = pulp.LpProblem("OWA", pulp.LpMaximize)

    # Variables
    x = [pulp.LpVariable(f"x_{j}", cat="Binary") for j in range(n)]
    r = [pulp.LpVariable(f"r_{k}") for k in range(p)]
    b = [[pulp.LpVariable(f"b_{k}_{i}", lowBound=0) for i in range(p)] for k in range(p)]

    # Fonction objectif
    prob += pulp.lpSum(lambdas[k] * ((k+1)*r[k] - pulp.lpSum(b[k][i] for i in range(p))) for k in range(p))  # k+1 car k de 1 à p mais de 0 à p-1 en python

    #Contraintes
    for k in range(p):
        for i in range(p):
            prob += (r[k] - b[k][i] <= pulp.lpSum(values[j][i] * x[j] for j in range(n)))

    prob += pulp.lpSum(weights[j] * x[j] for j in range(n)) <= W

    #Résolution
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))

    #Calcul vecteur obj obtenu
    selected = [j for j in range(n) if x[j].value() == 1.0]
    y = instance.eval(selected)

    return y


def enumerate_lorenz(instance, omega, verbose=True):
    '''
    Generer toute les vecteurs Lorenz non dominés
    '''
    n = instance.n #nb d'objets
    p = instance.p #nb d'objectifs
    W = instance.capacity
    weights = instance.weights
    values = instance.values

    #Calcul des poids lambda
    lambdas = [omega[i] - omega[i+1] for i in range(p-1)] + [omega[p-1]]

    lorenz_vectors = [] #Vecteurs de Lorenz
    objective_points = [] #Vecteurs objectifs associé

    while True:
        #On créer un nouveau PL à chaque itération
        prob = pulp.LpProblem("OWA", pulp.LpMaximize)

        # Variables
        x = [pulp.LpVariable(f"x_{j}", cat="Binary") for j in range(n)]
        r = [pulp.LpVariable(f"r_{k}") for k in range(p)]
        b = [[pulp.LpVariable(f"b_{k}_{i}", lowBound=0) for i in range(p)] for k in range(p)]
            
        # Fonction objectif
        prob += pulp.lpSum(lambdas[k] * ((k+1)*r[k] - pulp.lpSum(b[k][i] for i in range(p))) for k in range(p))  # k+1 car k de 1 à p mais de 0 à p-1 en python

        #Contraintes
        for k in range(p):
            for i in range(p):
                # rk - bik <= sum vij*xj pour i,k de 1 à p
                prob += (r[k] - b[k][i] <= pulp.lpSum(values[j][i] * x[j] for j in range(n)))

        # sum wi*xi <= W -> contrainte de capacité
        prob += pulp.lpSum(weights[j] * x[j] for j in range(n)) <= W

        #Contrainte d'amélioration
        z_vars = [] #stocke tout les z, z=(nb vectors de lorenz)x(nb objectifs = taille du vecteur)

        for s, Ls in enumerate(lorenz_vectors):
            z = [pulp.LpVariable(f"z_{s}_{k}", cat="Binary") for k in range(p)]
            z_vars.append(z)

            for k in range(p):
                # k*r[k] - sum b >= (Ls[k] + 1)*z[k]
                prob += ((k+1)*r[k] - pulp.lpSum(b[k][i] for i in range(p))>= (Ls[k] + 1) * z[k])

            prob += pulp.lpSum(z[k] for k in range(p)) >= 1

        status = prob.solve(pulp.PULP_CBC_CMD(msg=False))

        if status != pulp.LpStatusOptimal:
            if verbose:
                print("Plus aucune solution !")
            break #plus de vecteurs Lorenz non dominé

        # Récupération des objets sélectionnés
        selected_items = [j for j in range(n) if x[j].value() == 1.0]

        # Évaluation
        y = instance.eval(selected_items)
        L = lorenz_vector(y)

        if verbose:
            print(f"Solution trouvé: {y} -> {L}")

        objective_points.append(y)
        lorenz_vectors.append(L)

    return objective_points, lorenz_vectors


if __name__ == "__main__":

    n = 50
    p = 3
    omega = [0.5, 0.33, 0.17]

    instance = read_instance("Data/2KP200-TA-0.dat", n, p)
    print(f"Test sur une instance de {n} objets et {p} objectifs")

    # y=solve_owa(instance, omega)
    # print(y)

    y,vect = enumerate_lorenz(instance,omega, verbose=False)
    print(f"On obtient {len(y)} points Lorenz non dominés:")
    print(y)
