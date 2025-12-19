#coding:utf8

import numpy as np
import pandas as pd
import math
import scipy
import scipy.stats as stats
import os

#C'est la partie la plus importante dans l'analyse de données. D'une part, elle n'est pas simple à comprendre tant mathématiquement que pratiquement. D'autre, elle constitue une application des probabilités. L'idée consiste à comparer une distribution de probabilité (théorique) avec des observations concrètes. De fait, il faut bien connaître les distributions vues dans la séance précédente afin de bien pratiquer cette comparaison. Les probabilités permettent de définir une probabilité critique à partir de laquelle les résultats ne sont pas conformes à la théorie probabiliste.
#Il n'est pas facile de proposer des analyses de données uniquement dans un cadre univarié. Vous utiliserez la statistique inférentielle principalement dans le cadre d'analyses multivariées. La statistique univariée est une statistique descriptive. Bien que les tests y soient possibles, comprendre leur intérêt et leur puissance d'analyse dans un tel cadre peut être déroutant.
#Peu importe dans quelle théorie vous êtes, l'idée de la statistique inférentielle est de vérifier si ce que vous avez trouvé par une méthode de calcul est intelligent ou stupide. Est-ce que l'on peut valider le résultat obtenu ou est-ce que l'incertitude qu'il présente ne permet pas de conclure ? Peu importe également l'outil, à chaque mesure statistique, on vous proposera un test pour vous aider à prendre une décision sur vos résultats. Il faut juste être capable de le lire.

#Par convention, on place les fonctions locales au début du code après les bibliothèques.

Z_CRITIQUE = 1.96 

FILE_ECHANTILLONS = ("./data/Echantillonnage-100-Echantillons.csv")
FILE_TEST_1 = ("./data/Loi-normale-Test-1.csv")
FILE_TEST_2 = ("./data/Loi-normale-Test-2.csv")

def ouvrirUnFichier(nom_fichier):
    try:
        with open(nom_fichier, "r") as fichier:
            contenu = pd.read_csv(fichier, sep=',')
        return contenu
    except FileNotFoundError:
        print(f"Erreur : Le fichier {nom_fichier} est introuvable. Assurez-vous qu'il est bien présent.")
        return pd.DataFrame()


# --- 1. THÉORIE DE L'ÉCHANTILLONNAGE (INTERVALLLES DE FLUCTUATION) ---

def theorie_echantillonnage():
    """Résout les exercices de la théorie de l'échantillonnage (Intervalle de fluctuation)."""
    print("\n\n#####################################################")
    print("--- 1. Théorie de l'Échantillonnage (Intervalle de Fluctuation) ---")
    print("#####################################################")
    
    POPULATION_MERE = {
        'Pour': 852,
        'Contre': 911,
        'Sans opinion': 422
    }
    N_POP = 2185

    freq_mere = {k: round(v / N_POP, 2) for k, v in POPULATION_MERE.items()}
    print(f"Fréquences réelles de la population mère (p) : {freq_mere}")

    donnees_ech = ouvrirUnFichier(FILE_ECHANTILLONS)
    if donnees_ech.empty:
        return

    moyennes_ech = donnees_ech.mean()
    moyennes_arrondies = moyennes_ech.round(0).astype(int)
    print(f"\nMoyennes des 100 échantillons (arrondies) :\n{moyennes_arrondies.to_string()}")

    somme_moyennes = moyennes_arrondies.sum()
    freq_ech = (moyennes_arrondies / somme_moyennes).round(2)
    print(f"\nFréquences moyennes des échantillons (observées, f) : {freq_ech.to_dict()}")

    n_ech = somme_moyennes
    print(f"\nIntervalle de Fluctuation (IF) au seuil de {Z_CRITIQUE} (95%) :")
    
    for opinion in POPULATION_MERE.keys():
        p_mere = POPULATION_MERE[opinion] / N_POP
        
        ME = Z_CRITIQUE * np.sqrt((p_mere * (1 - p_mere)) / n_ech)
        
        IF_min = p_mere - ME
        IF_max = p_mere + ME
        f_obs = freq_ech.loc[opinion]
        
        print(f"  - Opinion '{opinion}':")
        print(f"      - Fréquence mère (p) : {p_mere:.4f}")
        print(f"      - Fréquence observée (f) : {f_obs:.4f}")
        print(f"      - IF [Min; Max] : [{IF_min:.4f}; {IF_max:.4f}]")
        
        if IF_min <= f_obs <= IF_max:
            conclusion = "La fréquence observée est DANS l'IF."
        else:
            conclusion = "La fréquence observée est HORS de l'IF."
        print(f"      - Conclusion : {conclusion}")


# --- 2. THÉORIE DE L'ESTIMATION (INTERVALLLES DE CONFIANCE) ---

def theorie_estimation():
    """Résout les exercices de la théorie de l'estimation (Intervalle de confiance)."""
    print("\n\n#####################################################")
    print("--- 2. Théorie de l'Estimation (Intervalle de Confiance) ---")
    print("#####################################################")
    
    donnees_ech = ouvrirUnFichier(FILE_ECHANTILLONS)
    if donnees_ech.empty:
        return

    echantillon_1 = donnees_ech.iloc[0]
    
    liste_valeurs = list(echantillon_1)
    

    n_ech = sum(liste_valeurs)
    freq_ech = echantillon_1 / n_ech
    print(f"Taille du premier échantillon (n) : {n_ech}")
    print(f"Fréquences observées (f) de l'échantillon : {freq_ech.round(4).to_dict()}")

    # IC = [f - z_C * sqrt(f*(1-f)/n), f + z_C * sqrt(f*(1-f)/n)]

    print(f"\nIntervalle de Confiance (IC) au seuil de {Z_CRITIQUE} (95%) :")
    
    for opinion, f_obs in freq_ech.items():
        if f_obs == 0 or f_obs == 1:
            ME = 0
        else:
            ME = Z_CRITIQUE * np.sqrt((f_obs * (1 - f_obs)) / n_ech)
        
        IC_min = f_obs - ME
        IC_max = f_obs + ME
        
        print(f"  - Opinion '{opinion}':")
        print(f"      - Fréquence observée (f) : {f_obs:.4f}")
        print(f"      - IC [Min; Max] : [{IC_min:.4f}; {IC_max:.4f}]")


# --- 3. THÉORIE DE LA DÉCISION (TESTS D'HYPOTHÈSE) ---

def theorie_decision():
    """Résout les exercices de la théorie de la décision (Test de Shapiro-Wilks)."""
    print("\n\n#####################################################")
    print("--- 3. Théorie de la Décision (Tests d'Hypothèse) ---")
    print("#####################################################")

    fichiers_test = {
        "Test-1": FILE_TEST_1,
        "Test-2": FILE_TEST_2
    }
    
    for nom_test, fichier in fichiers_test.items():
        data = ouvrirUnFichier(fichier)
        if data.empty:
            continue

        series_data = data.iloc[:, 0]
        
        W, p_value = stats.shapiro(series_data)
        
        alpha = 0.05
        
        if p_value < alpha:
            decision = "Rejet de H0"
            conclusion = "La distribution NE suit PAS une loi normale."
        else:
            decision = "Non-rejet de H0"
            conclusion = "La distribution suit une loi normale."
        
        print(f"\n--- Résultats du Test de Shapiro-Wilks pour {nom_test} ({fichier}) ---")
        print(f"Statistique W : {W:.4f}")
        print(f"P-value : {p_value:.4f}")
        print(f"Décision (au seuil α={alpha}) : {decision}")
        print(f"Conclusion : {conclusion}")
        

# --- EXÉCUTION DU SCRIPT ---

if __name__ == "__main__":
    
    theorie_echantillonnage()
    theorie_estimation()
    theorie_decision()
    
    print("\n*** Fin des exercices de codage de la Séance 5 (Partie 2.2). ***")