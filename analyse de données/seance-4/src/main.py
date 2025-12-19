#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats as stats
import os

#https://docs.scipy.org/doc/scipy/reference/stats.html


dist_names = ['norm', 'beta', 'gamma', 'pareto', 't', 'lognorm', 'invgamma', 'invgauss',  'loggamma', 'alpha', 'chi', 'chi2', 'bradford', 'burr', 'burr12', 'cauchy', 'dweibull', 'erlang', 'expon', 'exponnorm', 'exponweib', 'exponpow', 'f', 'genpareto', 'gausshyper', 'gibrat', 'gompertz', 'gumbel_r', 'pareto', 'pearson3', 'powerlaw', 'triang', 'weibull_min', 'weibull_max', 'bernoulli', 'betabinom', 'betanbinom', 'binom', 'geom', 'hypergeom', 'logser', 'nbinom', 'poisson', 'poisson_binom', 'randint', 'zipf', 'zipfian']

print(dist_names)

OUTPUT_DIR = "img_seance4"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def visualize_discrete_distributions():
    """Visualise les distributions statistiques discrètes demandées."""
    print("--- Question 1 ---")

    distributions = {
        "Uniforme Discrète (randint)": stats.randint(low=1, high=7),
        "Binomiale (binom)": stats.binom(n=10, p=0.5),
        "Poisson (poisson)": stats.poisson(mu=3),
    }

    x_max = 12
    x = np.arange(x_max)

    fig, axes = plt.subplots(len(distributions), 1, figsize=(10, 4 * len(distributions)))
    fig.suptitle("Distributions Statistiques Discrètes (PMF)", fontsize=16)

    for i, (name, dist) in enumerate(distributions.items()):
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))
        pmf_values = dist.pmf(x)
        ax.bar(x, pmf_values, label=name, color=f'C{i}')
        ax.set_title(f"Distribution Discrète: {name}")
        ax.set_xlabel("Valeurs (k)")
        ax.set_ylabel("Probabilité P(X=k)")
        ax.grid(True, linestyle='--', alpha=0.6)

        filename = os.path.join(OUTPUT_DIR, f"{name}_PMF.png")
        plt.savefig(filename)
        print(f"Figure enregistrée : {filename}")
        plt.close(fig)

def visualize_continuous_distributions():
    """Visualise les distributions statistiques continues demandées."""
    print("\n--- 2. Visualisation des Distributions Continues ---")

    distributions = {
        "Normale (norm)": stats.norm(loc=0, scale=1),
        "Log-Normale (lognorm)": stats.lognorm(s=0.95, loc=0, scale=np.exp(0)),
        "Uniforme (uniform)": stats.uniform(loc=0, scale=10),
        "Chi-Carré (chi2)": stats.chi2(df=5),
        "Pareto (pareto)": stats.pareto(b=2.5),
    }

    x = np.linspace(0, 10, 500)

    fig, axes = plt.subplots(len(distributions), 1, figsize=(10, 4 * len(distributions)))
    fig.suptitle("Distributions Statistiques Continues (PDF)", fontsize=16)

    for i, (name, dist) in enumerate(distributions.items()):
        fig, ax = plt.subplots(1, 1, figsize=(8, 5))
        pdf_values = dist.pdf(x)
        ax.plot(x, pdf_values, label=name, color=f'C{i}')
        ax.fill_between(x, pdf_values, alpha=0.3, color=f'C{i}')
        ax.set_title(f"Distribution Continue: {name}")
        ax.set_xlabel("Valeurs (x)")
        ax.set_ylabel("Densité de Probabilité f(x)")
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_ylim(bottom=0)

        filename = os.path.join(OUTPUT_DIR, f"{name}_PDF.png")
        plt.savefig(filename)
        print(f"Figure enregistrée : {filename}")
        plt.close(fig)

#Question 2

def calculate_stats(dist_name, dist_params, is_continuous=True):
    """Calcule et affiche la moyenne et l'écart type pour une distribution scipy.stats donnée."""
    
    try:
        dist = getattr(stats, dist_name)(*dist_params)
    except AttributeError:
        print(f"Erreur: Distribution '{dist_name}' non trouvée dans scipy.stats.")
        return

    mean, var = dist.stats(moments='mv')
    std_dev = np.sqrt(var)

    dist_type = "Continue" if is_continuous else "Discrète"
    print(f"\n--- Statistiques pour la loi {dist_name.upper()} ({dist_type}) ---")
    print(f"Paramètres: {dist_params}")
    print(f"Moyenne (E[X]): {mean:.4f}")
    print(f"Écart Type (σ): {std_dev:.4f}")
    
    return mean, std_dev

def run_stats_calculations():
    """Lance les calculs de statistiques pour les distributions demandées."""
    print("\n\n#################################################################")
    print("--- 3. Calculs de Moyenne et d'Écart Type pour les Distributions ---")
    print("#################################################################")

    # Distributions Discrètes
    calculate_stats("randint", (1, 7), is_continuous=False) # Uniforme Discrète [1, 6]
    calculate_stats("binom", (10, 0.5), is_continuous=False) # Binomiale n=10, p=0.5
    calculate_stats("poisson", (3,), is_continuous=False) # Poisson mu=3
    # Dirac: Sa moyenne est son unique valeur, l'écart-type est 0. Non directement dans stats.
    # Zipf-Mandelbrot: Complexe, souvent implémentée via des fonctions personnalisées.

    # Distributions Continues
    calculate_stats("norm", (0, 1), is_continuous=True) # Normale mu=0, sigma=1
    calculate_stats("lognorm", (0.95, 0, np.exp(0)), is_continuous=True) # Log-Normale
    calculate_stats("uniform", (0, 10), is_continuous=True) # Uniforme [0, 10]
    calculate_stats("chi2", (5,), is_continuous=True) # Chi-Carré df=5
    calculate_stats("pareto", (2.5,), is_continuous=True) # Pareto b=2.5


# --- EXÉCUTION DU SCRIPT ---

if __name__ == "__main__":
    # Point 1 : Visualiser les distributions
    visualize_discrete_distributions()
    visualize_continuous_distributions()

    # Point 2 : Calculer la moyenne et l'écart type
    run_stats_calculations()
    
    print("\n*** Fin de l'exercice 2.2 de la Séance 4. ***")