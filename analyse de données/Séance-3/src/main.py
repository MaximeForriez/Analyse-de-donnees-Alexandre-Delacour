#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as f:
    df = pd.read_csv(f, sep=",")

#Question 5

quant_df = df.select_dtypes(include=[np.number]).copy()
if quant_df.shape[1] == 0:
    raise ValueError("Aucune colonne numérique trouvée dans le fichier CSV. Vérifie le séparateur et le format du fichier.")

# --- Fonction utilitaire pour arrondir les objets pandas proprement ---
def round_series_or_value(x, decimals=2):
    if isinstance(x, pd.Series):
        return x.round(decimals)
    try:
        return round(float(x), decimals)
    except Exception:
        return x

moyennes = quant_df.mean().round(2)
medianes = quant_df.median().round(2)
modes = quant_df.mode().iloc[0].round(2)
ecarts_type = quant_df.std().round(2)

ecarts_absolus = quant_df.apply(lambda col: np.abs(col - col.mean()).mean()).round(2)

etendue = (quant_df.max() - quant_df.min()).round(2)

#Question 6

print("\n--- PARAMÈTRES STATISTIQUES ---")
print("Moyennes :\n", moyennes)
print("Médianes :\n", medianes)
print("Modes :\n", modes)
print("Écarts type :\n", ecarts_type)
print("Écarts absolus à la moyenne :\n", ecarts_absolus)
print("Étendue :\n", etendue)

#Question 7

iqr = (quant_df.quantile(0.75) - quant_df.quantile(0.25)).round(2)
interdecile = (quant_df.quantile(0.90) - quant_df.quantile(0.10)).round(2)

print("\nDistance interquartile :\n", iqr)
print("\nDistance interdécile :\n", interdecile)

#Question 8

os.makedirs("img", exist_ok=True)

for col in quant_df.columns:
    plt.figure(figsize=(4, 6))
    plt.boxplot(quant_df[col].dropna(), vert=True)
    plt.title(f"Boîte de dispersion : {col}")
    plt.savefig(f"img/boxplot_{col}.png")
    plt.close()

#Question 9 probleme ici 

with open("./data/island-index.csv") as f2:
    island_df = pd.read_csv(f2, sep=",")

#Question 10

possible_names = [c for c in island_df.columns if "surface" in c.lower()]
if not possible_names:
    raise ValueError("La colonne 'Surface (km2)' n'a pas été trouvée dans island-index.csv")
surface_col = possible_names[0]

island_df[surface_col] = pd.to_numeric(island_df[surface_col], errors="coerce")

bins = [0, 10, 25, 50, 100, 2500, 5000, 10000, float("inf")]
labels = [
    "]0,10]",
    "]10,25]",
    "]25,50]",
    "]50,100]",
    "]100,2500]",
    "]2500,5000]",
    "]5000,10000]",
    "]10000,+∞["
]

island_df["Classe_surface"] = pd.cut(island_df[surface_col], bins=bins, labels=labels, right=True, include_lowest=False)
compte_classes = island_df["Classe_surface"].value_counts(sort=False)  # conserve l'ordre des labels

print("\n--- Catégorisation des îles (par surface) ---")
print(compte_classes.to_string())

#Bonus

resume = pd.DataFrame({
    "Moyenne": moyennes,
    "Mediane": medianes,
    "Mode": modes,
    "Ecart_type": ecarts_type,
    "Ecart_absolu": ecarts_absolus,
    "Etendue": etendue,
    "IQR": iqr,
    "Interdecile": interdecile
})

resume.to_csv("resultats_statistiques.csv", sep=";", encoding="utf-8")
resume.to_excel("resultats_statistiques.xlsx")