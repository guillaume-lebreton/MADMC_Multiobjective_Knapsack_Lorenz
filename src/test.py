from instance import read_instance, plot_2d_points
from indirecte import methode_indirecte
from direct import enumerate_lorenz
import time

def test_comp(n,p,omega, verbose=True, file="Data/2KP200-TA-0.dat"):

    instance = read_instance(file, n, p)

    print("---"*15)
    print(f"Test sur une instance de {n} objet et {p} objectifs")
    print("---"*15)

    print("Méthode indirecte :")
    start = time.time()
    ind = methode_indirecte(instance, verbose)
    temps_indirecte = time.time() - start
    print(f"On trouve {len(ind)} points en {temps_indirecte:.2f}s")
    print(ind)

    print("---"*15)
    print("Méthode directe:")
    print(f"{omega = }")
    start = time.time()
    dir,lor = enumerate_lorenz(instance, omega, verbose)
    temps_directe = time.time() - start
    print(f"On trouve {len(dir)} points en {temps_directe:.2f}s")
    print(dir)
    
    print("---"*15)
    ind_set = set(ind)
    dir_set = set(dir)
    if ind_set == dir_set:
        print("On a trouvé les mêmes points avec les 2 méthodes")
    else:
        ind_only = ind_set - dir_set
        dir_only = dir_set - ind_set

        print("Différences entre les deux méthodes :")
        print(f"  -  {len(ind_only)} uniquement indirecte : {ind_only}")
        print(f"  - {len(dir_only)} uniquement directe : {dir_only}")
        print(f"  - Total différents  : {len(ind_only) + len(dir_only)} points")

    print("---"*15)

    if p == 2:

        ind_set = set(ind)
        dir_set = set(dir)
        tot = ind_set | dir_set
        tot = list(tot)
        plot_2d_points(tot)
    
if __name__ == "__main__":

    n = 20
    p = 3
    omega = [0.5, 0.3, 0.2]

    test_comp(n,p,omega, verbose=False)