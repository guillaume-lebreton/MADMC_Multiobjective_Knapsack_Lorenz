import csv
import matplotlib.pyplot as plt
from comparaison import Resultats

def from_csv(path):
        res = Resultats()
        try:
            with open(path, "r", newline="") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    res.add(
                        int(row["n"]),
                        int(row["p"]),
                        float(row["t_ind"]),
                        float(row["t_dir"]),
                        int(row["pareto_count"]),
                        int(row["lorenz_ind_count"]),
                        int(row["lorenz_dir_count"]),
                    )
        except OSError as e:
            print(f"[ERREUR] Lecture CSV impossible: {e}")
            return None
        return res

def plot_temps_exec(results):
    '''
    Plot des temps d'exécution des 2 méthodes en fonction du nombre d'objets n
    pour chaque nombre d'objectifs p
    '''

    P = set(results.p)

    for p in P:
        ns = [results.n[i] for i in range(len(results.n)) if results.p[i] == p]
        t_inds = [results.t_ind[i] for i in range(len(results.t_ind)) if results.p[i] == p]
        t_dirs = [results.t_dir[i] for i in range(len(results.t_dir)) if results.p[i] == p]

        plt.figure()
        plt.plot(ns, t_inds, marker='o', label="Méthode Indirecte")
        plt.plot(ns, t_dirs, marker='o', label="Méthode Directe")
        plt.xlabel("Nombre d'objets (n)")
        plt.ylabel("Temps d'exécution (s)")
        plt.title(f"Temps d'exécution en fonction de n (p={p})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

def plot_points_count(results):
    '''
    Plot le nombre de points de Pareto de la méthode direct et le nombre de points de Lorenz pour les 
    2 méthodes en fonction du nombre d'objets n pour chaque nombre d'objectifs p
    '''

    P = set(results.p)

    for p in P:
        ns = [results.n[i] for i in range(len(results.n)) if results.p[i] == p]
        par_ind = [results.pareto_count[i] for i in range(len(results.pareto_count)) if results.p[i] == p]
        lor_ind = [results.lorenz_ind_count[i] for i in range(len(results.lorenz_ind_count)) if results.p[i] == p]
        lor_dir = [results.lorenz_dir_count[i] for i in range(len(results.lorenz_dir_count)) if results.p[i] == p]

        plt.figure()
        plt.plot(ns, par_ind, marker='o', label="Pareto Indirecte")
        plt.plot(ns, lor_ind, marker='o', label="Lorenz Indirecte")
        plt.plot(ns, lor_dir, marker='o', label="Lorenz Directe")
        plt.xlabel("Nombre d'objets (n)")
        plt.ylabel("Nombre de points non dominés")
        plt.title(f"Nombre de points non dominés en fonction de n (p={p})")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":

    path = "Resultats/benchmark.csv"

    results = from_csv(path)

    plot_temps_exec(results)

    plot_points_count(results)

    

