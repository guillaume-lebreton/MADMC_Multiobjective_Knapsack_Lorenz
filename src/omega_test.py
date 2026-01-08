'''
Test l'influence du jeu de poids omega sur le temps de calcul dans la méthode direct
'''

from instance import read_instance
from direct import enumerate_lorenz
import time
import math
import numpy as np

def normalize(omega):
    '''
    normalise les poids omega -> somme = 1
    '''
    s = sum(omega)
    return [w / s for w in omega]

def omega_exp(p, lamb):
    """
    exp(-lambda * k-1)
    0 < lambda < 1
    lambda près de 0 -> poids equilibré
    lmabda près de 1 -> gros poids sur le premier puis decroissant
    """
    omega = [math.exp(-lamb * k) for k in range(p)]
    return normalize(omega)


def test_omega(instance, OMEGA):
    '''
    Execute la méthode direct sur l'instance avec tout les poids dans OMEGA (liste de omega)
    '''

    T = [] # listes des durées de résolution pour chaque oméga

    for i, omega in enumerate(OMEGA):
        t = []
        for _ in range(3):  # on fait une moyenne 
            # print(f"{omega = }")
            start = time.perf_counter()
            dir,lor = enumerate_lorenz(instance, omega, verbose=False)
            temps = time.perf_counter() - start
            t.append(temps)
        temps_moyen = np.mean(t)
        K = len(lor)
        print(f"Lambda {i} -> Temps : {temps_moyen:.3f}s, {K} vecteurs")
        T.append(temps)
        
    return T

if __name__ == "__main__":

    P = [2,4,6]
    N = [[100,150,175], [25,40,50], [20,25,30]] #On prend des plus petites instance pour des p plus grand
    lambdas = [0.01, 0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 1]
    res = {}

    print(f"On va tester les lambdas suivant : {lambdas}")

    for i, p in enumerate(P):
        print("---"*15)
        print(f"{p = }")
        print("---"*15)
        omegas = []
        for j,l in enumerate(lambdas):
            omega = omega_exp(p,l)
            omegas.append(omega)
            print(f"Lamba {j} = {l} -> omega = {[round(o,3) for o in omega]}")
            print("---"*15)
        for n in N[i]:
            print("---"*15)
            print(f"{n = }")
            print("---"*15)
            instance = read_instance("Data/2KP200-TA-0.dat", n, p)
            T = test_omega(instance, omegas)
            res[p , n] = T

    print("---"*15)
    print("RESULTATS")
    print("---"*15)
    for p,n in res.keys():
        print(f"{p=}, {n=} -> meilleur lambda = {lambdas[np.argmin(res[p,n])]}")

    #plot
    
        