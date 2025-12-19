#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import os

# Source des données : https://www.data.gouv.fr/datasets/election-presidentielle-des-10-et-24-avril-2022-resultats-definitifs-du-1er-tour/
with open("./data/resultats-elections-presidentielles-2022-1er-tour.csv","r") as fichier:
    contenu = pd.read_csv(fichier)
    contenu.columns = contenu.columns.str.strip()
    
print(contenu.columns)

colonnes_possibles = [
    "Libellé du département",
    "Libellé du Département",
    "Département",
    "departement"
]

colonne_departement = None
for col in colonnes_possibles:
    if col in contenu.columns:
        colonne_departement = col
        break

if colonne_departement is None:
    raise ValueError("❌ Aucune colonne département trouvée dans le fichier")

print(f"✅ Colonne département détectée : {colonne_departement}")

os.makedirs("images", exist_ok=True)

# Mettre dans un commentaire le numéro de la question
# Question 1
data = pd.DataFrame(contenu)
print(data)
print(len(data))

#Question 2

list(data.index)[:]
list(data.columns)[:]
#data.loc[index,colonne]
colonne_a_afficher = data.columns[0]
print(data.head(0))

#Question 3 

print("\n=== Types des variables ===")
types = contenu.dtypes
print(types)

# Création d'une liste simple des types
liste_types = [(col, str(contenu[col].dtype)) for col in contenu.columns]

#Question 8

print("\n=== Noms des colonnes ===")
print(contenu.columns)

#Question 9

if "Inscrits" in contenu.columns:
    print("\nTotal des inscrits :", contenu["Inscrits"].sum())

#Question 10

print("\n=== Effectifs des colonnes quantitatives ===")

effectifs = {}

for col in contenu.columns:
    if contenu[col].dtype in ["int64", "float64"]:
        effectifs[col] = contenu[col].sum()

for variable, valeur in effectifs.items():
    print(f"{variable} : {valeur}")

#Question 11

os.makedirs("images", exist_ok=True)

if {colonne_departement, "Inscrits", "Votants"}.issubset(contenu.columns):

    for dep in contenu[colonne_departement].unique():
        data_dep = contenu[contenu[colonne_departement] == dep]

        valeurs = [data_dep["Inscrits"].sum(), data_dep["Votants"].sum()]

        plt.figure()
        plt.bar(["Inscrits", "Votants"], valeurs)
        plt.title(f"Inscrits vs Votants – {dep}")
        plt.savefig(f"images/bar_{dep}.png")
        plt.close()

#Question 12

colonnes_votes = ["Blancs", "Nuls", "Exprimés", "Abstentions"]

if {colonne_departement, *colonnes_votes}.issubset(contenu.columns):

    for dep in contenu[colonne_departement].unique():
        data_dep = contenu[contenu[colonne_departement] == dep]

        valeurs = [data_dep[col].sum() for col in colonnes_votes]

        plt.figure()
        plt.pie(valeurs, labels=colonnes_votes, autopct="%1.1f%%")
        plt.title(f"Répartition des votes – {dep}")
        plt.savefig(f"images/pie_{dep}.png")
        plt.close()

#Question 13

if "Inscrits" in contenu.columns:
    plt.figure()
    plt.hist(contenu["Inscrits"], bins="sturges", density=True, edgecolor="black")
    plt.title("Distribution des inscrits")
    plt.xlabel("Inscrits")
    plt.ylabel("Densité")
    plt.savefig("images/hist_inscrits.png")
    plt.close()

#Bonus

colonnes_candidats = [col for col in contenu.columns if col.startswith("Voix_")]

# Par département
for dep in contenu[colonne_departement].unique():
    data_dep = contenu[contenu[colonne_departement] == dep]

    valeurs = [data_dep[col].sum() for col in colonnes_candidats]
    labels = [col.replace("Voix_", "") for col in colonnes_candidats]

    plt.figure()
    plt.pie(valeurs, labels=labels, autopct="%1.1f%%")
    plt.title(f"Répartition des voix par candidat – {dep}")

    plt.savefig(f"images/pie_candidats_{dep}.png")
    plt.close()

# France entière
valeurs = [contenu[col].sum() for col in colonnes_candidats]
labels = [col.replace("Voix_", "") for col in colonnes_candidats]

plt.figure()
plt.pie(valeurs, labels=labels, autopct="%1.1f%%")
plt.title("Répartition nationale des voix – France entière")

plt.savefig("images/pie_candidats_france.png")
plt.close()
