from instance import read_instance, plot_2d_points
from indirecte import methode_indirecte
from direct import enumerate_lorenz
from omega_test import omega_exp
import time

def test_comp(n,p,omega, verbose=True, file="Data/2KP200-TA-0.dat"):

    instance = read_instance(file, n, p)

    print("---"*15)
    print(f"Test sur une instance de {n} objet et {p} objectifs")
    print(f"Omega = {[round(o,3) for o in omega]}")
    print("---"*15)

    print("Méthode indirecte :")
    start = time.time()
    par, ind = methode_indirecte(instance, verbose)
    temps_indirecte = time.time() - start
    print(f"On trouve {len(par)} points Pareto et {len(ind)} points Lorenz en {temps_indirecte:.2f}s")
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
        print("On a trouvé les mêmes points objectifs avec les 2 méthodes")
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

    while True:
        try:
            n = int(input("n (nombre d'objets): ").strip())
            if n < 1 or n > 200:
                print("Merci de saisir un entier entre 1 et 200.")
                continue
            break
        except ValueError:
            print("Entree invalide, merci de saisir un entier.")

    while True:
        try:
            p = int(input("p (nombre d'objectifs): ").strip())
            if p < 2 or p > 6:
                print("Merci de saisir un entier entre 2 et 6.")
                continue
            break
        except ValueError:
            print("Entree invalide, merci de saisir un entier.")

    while True:
        raw = input("Omega (p valeurs, ex: 0.2,0.5,0.9) ou auto: ").strip()
        if raw == "" or raw.lower() in {"auto", "a"}:
            omega = omega_exp(p, 0.5)
            break
        parts = [s.strip() for s in raw.replace(";", ",").split(",") if s.strip() != ""]
        if len(parts) != p:
            print(f"Merci de fournir exactement {p} valeurs.")
            continue
        try:
            omega = [float(x) for x in parts]
        except ValueError:
            print("Entree invalide, merci de saisir des nombres.")
            continue
        break

    test_comp(n, p, omega, verbose=True)
