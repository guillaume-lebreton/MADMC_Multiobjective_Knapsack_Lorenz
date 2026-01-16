"""
Benchmark expérimental : méthode indirecte vs méthode directe
- Temps de calcul
- nombre de points Pareto (indirecte)
- nombre de points Lorenz (indirecte + directe)
- Export CSV
"""

import csv
import time
import matplotlib.pyplot as plt

from instance import read_instance
from indirecte import methode_indirecte
from direct import enumerate_lorenz
from omega_test import omega_exp

class Resultats:
    def __init__(self):
        self.n = []
        self.p = []
        self.t_ind = []
        self.t_dir = []
        self.pareto_count = []
        self.lorenz_ind_count = []
        self.lorenz_dir_count = []

    def add(self, n, p, t_ind, t_dir, pareto_count, lorenz_ind_count, lorenz_dir_count):
        self.n.append(n)
        self.p.append(p)
        self.t_ind.append(round(t_ind,2))
        self.t_dir.append(round(t_dir,2))
        self.pareto_count.append(pareto_count)
        self.lorenz_ind_count.append(lorenz_ind_count)
        self.lorenz_dir_count.append(lorenz_dir_count)

    def to_csv(self, path):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["p", "n","t_ind", "t_dir","pareto_count", "lorenz_ind_count", "lorenz_dir_count"])
            for i in range(len(self.n)):
                writer.writerow([self.p[i], self.n[i],self.t_ind[i], self.t_dir[i],self.pareto_count[i], self.lorenz_ind_count[i], self.lorenz_dir_count[i]])

        print(f"CSV ecrit: {path} ({len(self.n)} lignes)")


def run(n,p,omega, verbose=False, file="Data/2KP200-TA-0.dat"):
    '''
    Exécute les 2 méthodes sur 1 instance
    return:
        - Temps d'éxécutions des 2 méthodes
        - nombre de points pareto non dominés et lorenz non dominé pour la méthode indirecte
        - nombre de points lorenz non dominé pour la méthode directe
    '''

    instance = read_instance(file, n, p)

    #Indirecte
    start = time.perf_counter()
    par, lor = methode_indirecte(instance, verbose)
    temps_indirecte = time.perf_counter() - start

    #Directe
    start = time.perf_counter()
    dir,_ = enumerate_lorenz(instance, omega, verbose)
    temps_directe = time.perf_counter() - start
    
    return temps_indirecte, temps_directe, len(par), len(lor), len(dir)

def benchmark(N, P, lamb, file="Data/2KP200-TA-0.dat", verbose=False):

    res = Resultats()

    for p in P:
        for n in N[p]:
            omega = omega_exp(p, lamb)
            temps_indirecte, temps_directe, par, lor, dir = run(n,p,omega)
            res.add(n, p, temps_indirecte, temps_directe, par, lor, dir)

            if verbose:
                print("--"*20)
                print(f"{p=}, {n=} : ")
                print(f"Methode indirecte : \n{par} de Pareto et {lor} de Lorenz en {temps_directe:.2f}s")
                print(f"Methode directe : \n{dir} de Lorenz en {temps_indirecte:.2f}s")
                
                if lor == dir:
                    print(f"Bilan : {lor} points de Lorenz non dominés pour les 2 méthodes")
                elif lor > dir:
                    print(f"Bilan : {lor-dir} points de plus trouvés avec la méthode indirecte")
                elif lor < dir:
                    print(f"Bilan : {dir-lor} points de plus trouvés avec la méthode directe") #normalement impossible
                print("--"*20)
            else:
                print(f"{p = }, {n = } ...")

    print("Fin du benchmark")

    return res


if __name__ == "__main__":

    #Param
    file = "Data/2KP200-TA-0.dat"
    lamb = 0.5

    P = [2,3,4,5,6]
    N = {
        2 : [50, 75, 100, 125, 150],
        3 : [30, 40, 50, 60, 65],
        4 : [20, 30, 40, 45, 50],
        5 : [15, 20, 30, 35, 40],
        6 : [10, 15, 20, 25, 30]
    }

    res = benchmark(N, P, lamb, file)

    res.to_csv("Resultats/comparaison.csv")