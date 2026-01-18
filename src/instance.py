'''
Défini les fonctions pour lire/créer une instance du sac à dos multiobjectifs
et autre fonction utilitaire pour comparer ou tracer des solutions 
'''


import numpy as np
import matplotlib.pyplot as plt

def read_instance(filename, n, p):
    '''
    n: nombre d'objets
    p: nombre d'objectifs
    '''
    weights = []
    values = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line[0] != "i":
                continue
            data = line.split()
            weights.append(int(data[1]))
            values.append(tuple(map(int, data[2:2+p])))
            
            if len(weights) >= n:
                break

    capacity = sum(weights) // 2

    instance = Instance(weights, values, capacity)

    return instance

def random_instance(n, p, weight_range=(1, 100), value_range=(1, 100)):
    """
    Génère une instance aléatoire du sac à dos multiobjectifs
    n: nombre d'objets
    p: nombre d'objectifs
    """
    weights = np.random.randint(weight_range[0], weight_range[1]+1, size=n).tolist()
    values = [tuple(np.random.randint(value_range[0], value_range[1]+1, size=p).tolist()) for _ in range(n)]
    capacity = sum(weights) // 2

    instance = Instance(weights, values, capacity)

    return instance

class Instance:
    def __init__(self, weights, values, capacity):
        self.weights = weights
        self.values = values
        self.capacity = capacity
        self.n = len(weights)
        self.p = len(values[0])

    def eval(self, selec):
        '''
        selec: indices des objets séléctionnés
        évalue une selection d'objets d'une instance
        '''
        w_sum = 0
        val = np.zeros(self.p, dtype=int)
        for i in selec:
            w_sum += self.weights[i]
            val += self.values[i]   
        if w_sum > self.capacity:
            return False
        return tuple(val)
    

def pareto_dominate(u, v):
    '''
    return True si u domine v au sens de Pareto
    '''
    if len(u) != len(v):
        return False
    
    better_or_equal = True
    strictly_better = False

    for i in range(len(u)):
        if u[i] < v[i]:
            better_or_equal = False
            break
        if u[i] > v[i]:
            strictly_better = True

    return better_or_equal and strictly_better

def lorenz_vector(x):
    '''
    Renvoie le vecteur de Lorenz
    '''
    x_sorted = sorted(x)
    L = []
    cum = 0

    for v in x_sorted:
        cum += v
        L.append(cum)

    return tuple(L)

def lorenz_dominate(u, v):
    '''
    return True si u domine v au sens de Lorenz
    '''
    Lu = lorenz_vector(u)
    Lv = lorenz_vector(v)
    return pareto_dominate(Lu,Lv)

def plot_2d_points(points):
    '''
    Affiche un esemble de points dans l'espace des objectifs
    '''
    if len(points[0]) != 2:
        print("Les points données ne sont pas de dimension 2")
        return
    
    x = [p[0] for p in points]
    y = [p[1] for p in points]

    plt.figure()
    plt.scatter(x,y)
    plt.title("Images des points dans l'espace des objectifs")
    plt.xlabel("Objectif 1")
    plt.ylabel("Objectif 2")
    plt.grid(True)
    plt.show()    


if __name__ == "__main__":

    # # Pareto
    # assert pareto_dominate((3, 4), (2, 4)) is True
    # assert pareto_dominate((3, 4), (3, 4)) is False
    # assert pareto_dominate((2, 5), (3, 4)) is False

    # # Lorenz
    # u = (12, 13, 10)
    # v = (12, 10, 13)

    # assert lorenz_vector(u) == (10, 22, 35)
    # assert lorenz_vector(v) == (10, 22, 35)
    # assert lorenz_dominate(u, v) is False
    # assert lorenz_dominate(v, u) is False

    # w = (11, 11, 13)
    # assert lorenz_dominate(w, u) is True

    # print("Tests OK")

    instance = read_instance("Data/2KP200-TA-0.dat", 5, 3)

    print(instance.weights)
    print(instance.values)
    print("Capacité :", instance.capacity)

    instance2 = random_instance(5, 3)
    print(instance2.weights)
    print(instance2.values)
    print("Capacité :", instance2.capacity)