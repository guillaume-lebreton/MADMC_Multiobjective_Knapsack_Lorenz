'''
Methode directe:

- On obtient un point Lorenz non dominé en maximisant une fonction OWA
- Ajoute des contraintes pour trouvé tout les points Lorenz non dominés

'''

import gurobipy as gp
from gurobipy import GRB

from instance import read_instance, lorenz_vector

# OWA qui retourne un vecteur de Lorenz non dominé
# Pas utilisé -> equivalent à la 1ere itération de enumerate_lorenz (quand lorenz_vectors est vide)
def solve_owa(instance, omega):
    '''
    Resoud le PL OWA et retourne un point objectif Lorenz non dominé et son vecteur de Lorenz
    '''

    n = instance.n
    p = instance.p
    W = instance.capacity
    weights = instance.weights
    values = instance.values

    #Calcul des poids lambda
    lambdas = [omega[i] - omega[i+1] for i in range(p-1)] + [omega[p-1]]

    #Declaration du pb
    model = gp.Model("OWA_Lorenz")
    model.Params.OutputFlag = 0 

    # Variables
    x = model.addVars(n, vtype=GRB.BINARY, name="x")
    r = model.addVars(p, lb=-GRB.INFINITY, name="r")
    b = model.addVars(p, p, lb=0, name="b")

    # Fonction objectif OWA
    model.setObjective(gp.quicksum(lambdas[k] * ((k+1)*r[k] - gp.quicksum(b[k,i] for i in range(p))) for k in range(p)),GRB.MAXIMIZE) # k+1 car k de 1 à p mais de 0 à p-1 en python

    # Contraintes de linéarisation
    for k in range(p):
        for i in range(p):
            model.addConstr(r[k] - b[k,i] <= gp.quicksum(values[j][i] * x[j] for j in range(n)))

    # Contrainte de capacité
    model.addConstr(gp.quicksum(weights[j] * x[j] for j in range(n)) <= W)

    # Résolution
    model.optimize()

    if model.status != GRB.OPTIMAL:
        print("Pas de solution trouvée")
        return None, None

    # Récupération de la solution
    selected_items = [j for j in range(n) if x[j].X > 0.5]
    y = instance.eval(selected_items)
    L = lorenz_vector(y)

    return y, L

def enumerate_lorenz(instance, omega, verbose=True):
    '''
    Génère tous les vecteurs Lorenz non dominés
    '''
    n = instance.n #nb d'objets
    p = instance.p #nb d'objectifs
    W = instance.capacity
    weights = instance.weights
    values = instance.values

    #Calcul des poids lambda
    lambdas = [omega[i] - omega[i+1] for i in range(p-1)] + [omega[p-1]]

    lorenz_vectors = []  #Vecteurs de Lorenz
    objective_points = [] #Vecteurs objectifs associé

    while True:
        #On créer un nouveau PL à chaque itération
        model = gp.Model("OWA")
        model.Params.OutputFlag = 0

        # Variables
        x = model.addVars(n, vtype=GRB.BINARY, name="x")
        r = model.addVars(p, lb=-GRB.INFINITY, name="r")
        b = model.addVars(p, p, lb=0, name="b")

        # Fonction objectif
        model.setObjective(gp.quicksum(lambdas[k] * ((k+1)*r[k] - gp.quicksum(b[k,i] for i in range(p))) for k in range(p)), GRB.MAXIMIZE)

        #Contraintes
        for k in range(p):
            for i in range(p):
                # rk - bik <= sum vij*xj pour i,k de 1 à p
                model.addConstr( r[k] - b[k,i] <= gp.quicksum(values[j][i] * x[j] for j in range(n)))

        # sum wi*xi <= W -> contrainte de capacité
        model.addConstr(gp.quicksum(weights[j] * x[j] for j in range(n)) <= W)

        # Contraintes d'amélioration
        for s, Ls in enumerate(lorenz_vectors):
            z = model.addVars(p, vtype=GRB.BINARY, name=f"z_{s}")

            for k in range(p):
                # k*r[k] - sum b >= (Ls[k] + 1) si z[k]=1 / relaxé grace au big M sinon
                model.addConstr((k+1)*r[k] - gp.quicksum(b[k,i] for i in range(p)) >= (Ls[k] + 1)*z[k])

            model.addConstr(gp.quicksum(z[k] for k in range(p)) >= 1)

        model.optimize()

        if model.status != GRB.OPTIMAL:
            if verbose:
                print("Plus aucune solution !")
            break #plus de vecteurs Lorenz non dominé

        # Récupération des objets sélectionnés
        selected = [j for j in range(n) if x[j].X > 0.5]

        # Évaluation
        y = instance.eval(selected)
        L = lorenz_vector(y)

        if verbose:
            print(f"Solution trouvée : {y} -> {L}")

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

    y,vect = enumerate_lorenz(instance,omega, verbose=True)
    print(f"On obtient {len(y)} points Lorenz non dominés:")
    print(y)