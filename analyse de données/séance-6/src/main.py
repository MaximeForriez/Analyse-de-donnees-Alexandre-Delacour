#coding:utf8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import math

#Fonction pour ouvrir les fichiers
def ouvrirUnFichier(nom):
    with open(nom, "r") as fichier:
        contenu = pd.read_csv(fichier)
    return contenu

#Fonction pour convertir les données en données logarithmiques
def conversionLog(liste):
    log = []
    for element in liste:
        log.append(math.log(element))
    return log

#Fonction pour trier par ordre décroissant les listes (îles et populations)
def ordreDecroissant(liste):
    liste.sort(reverse = True)
    return liste

#Fonction pour obtenir le classement des listes spécifiques aux populations
def ordrePopulation(pop, etat):
    ordrepop = []
    for element in range(0, len(pop)):
        if np.isnan(pop[element]) == False:
            ordrepop.append([float(pop[element]), etat[element]])
    ordrepop = ordreDecroissant(ordrepop)
    for element in range(0, len(ordrepop)):
        ordrepop[element] = [element + 1, ordrepop[element][1]]
    return ordrepop

#Fonction pour obtenir l'ordre défini entre deux classements (listes spécifiques aux populations)
def classementPays(ordre1, ordre2):
    classement = []
    if len(ordre1) <= len(ordre2):
        for element1 in range(0, len(ordre2) - 1):
            for element2 in range(0, len(ordre1) - 1):
                if ordre2[element1][1] == ordre1[element2][1]:
                    classement.append([ordre1[element2][0], ordre2[element1][0], ordre1[element2][1]])
    else:
        for element1 in range(0, len(ordre1) - 1):
            for element2 in range(0, len(ordre2) - 1):
                if ordre2[element2][1] == ordre1[element1][1]:
                    classement.append([ordre1[element1][0], ordre2[element2][0], ordre1[element][1]])
    return classement

#Partie sur les îles
iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))

#Attention ! Il va falloir utiliser des fonctions natives de Python dans les fonctions locales que je vous propose pour faire l'exercice. Vous devez caster l'objet Pandas en list().

#Partie sur les populations des États du monde
#Source. Depuis 2007, tous les ans jusque 2025, M. Forriez a relevé l'intégralité du nombre d'habitants dans chaque États du monde proposé par un numéro hors-série du monde intitulé États du monde. Vous avez l'évolution de la population et de la densité par année.
monde = pd.DataFrame(ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv"))

print("="*80)
print("PARTIE 1 : ANALYSE DES ÎLES")
print("="*80)

# 2. Ouvrir le fichier island-index.csv
iles = pd.DataFrame(ouvrirUnFichier("./data/island-index.csv"))
print("\n1. Fichier des îles chargé avec succès")

# Afficher les colonnes disponibles pour diagnostic
print("\nColonnes disponibles dans le fichier :")
for i, col in enumerate(iles.columns):
    print(f"   {i}: '{col}'")

# 3. Isoler la colonne "Surface (km2)" - gestion robuste du nom
# On cherche la colonne qui contient "Surface"
colonne_surface = None
for col in iles.columns:
    if 'Surface' in col or 'surface' in col:
        colonne_surface = col
        break

if colonne_surface is None:
    print("\nERREUR : Impossible de trouver la colonne des surfaces")
    print("Veuillez vérifier le nom exact de la colonne dans le fichier CSV")
    exit()

print(f"\nColonne de surface trouvée : '{colonne_surface}'")

# Extraire les surfaces
surfaces = list(iles[colonne_surface].values)
# Conversion en float (en gérant les valeurs potentiellement manquantes)
surfaces_clean = []
for s in surfaces:
    try:
        if not pd.isna(s):
            surfaces_clean.append(float(s))
    except:
        pass

surfaces = surfaces_clean
print(f"Nombre de surfaces valides extraites : {len(surfaces)}")

# Ajout des continents
surfaces.append(float(85545323))  # Asie / Afrique / Europe
surfaces.append(float(37856841))  # Amérique
surfaces.append(float(7768030))   # Antarctique
surfaces.append(float(7605049))   # Australie

print(f"\n2. Total après ajout des continents : {len(surfaces)} éléments")

# 4. Ordonner la liste par ordre décroissant
surfaces_ordonnees = ordreDecroissant(surfaces.copy())
print(f"\n3. Liste ordonnée par ordre décroissant")
print(f"   Plus grande surface : {surfaces_ordonnees[0]:,.0f} km²")
print(f"   Plus petite surface : {surfaces_ordonnees[-1]:,.0f} km²")

# 5. Visualiser la loi rang-taille (version normale - illisible)
rangs = list(range(1, len(surfaces_ordonnees) + 1))

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.plot(rangs, surfaces_ordonnees, 'bo-', linewidth=2, markersize=3)
plt.xlabel('Rang', fontsize=12)
plt.ylabel('Surface (km²)', fontsize=12)
plt.title('Loi rang-taille - Échelle normale\n(Graphique illisible)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

# 6. Conversion en logarithme pour meilleure lisibilité
rangs_log = conversionLog(rangs)
surfaces_log = conversionLog(surfaces_ordonnees)

plt.subplot(1, 2, 2)
plt.plot(rangs_log, surfaces_log, 'ro-', linewidth=2, markersize=4)
plt.xlabel('Log(Rang)', fontsize=12)
plt.ylabel('Log(Surface)', fontsize=12)
plt.title('Loi rang-taille - Échelle logarithmique\n(Graphique lisible)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('loi_rang_taille_iles.png', dpi=300, bbox_inches='tight')
print("\n4. Graphiques sauvegardés : loi_rang_taille_iles.png")
plt.close()

# 7. Réponse sur la possibilité de faire un test sur les rangs
"""
Question 7 : Est-il possible de faire un test sur les rangs ?

Réponse : NON, il n'est pas possible de faire un test de corrélation des rangs 
(Spearman ou Kendall) dans ce cas précis.

Raisons :
- Ces tests nécessitent DEUX classements différents à comparer
- Ici, nous n'avons qu'UN SEUL classement (surfaces ordonnées)
- Les tests de Spearman et Kendall mesurent la concordance entre deux ordres différents
- Pour appliquer ces tests, il faudrait avoir une deuxième variable ordinale à comparer
  (par exemple : comparer le classement par surface avec un classement par population,
  ou par longueur de côte, etc.)

La loi rang-taille visualisée ici permet d'observer la distribution des surfaces,
mais ne constitue pas une analyse de corrélation entre deux variables.
"""
print("\n5. Réponse question 7 : Test sur les rangs impossible (voir commentaires dans le code)")

# ============================================================================
# PARTIE 2 : ANALYSE DES POPULATIONS MONDIALES
# ============================================================================

print("\n" + "="*80)
print("PARTIE 2 : ANALYSE DES POPULATIONS MONDIALES")
print("="*80)

# 9. Ouvrir le fichier des populations
try:
    monde = pd.DataFrame(ouvrirUnFichier("./data/Le-Monde-HS-Etats-du-monde-2007-2025.csv"))
    print("\n1. Fichier des populations chargé avec succès")
    print(f"   Nombre d'États : {len(monde)}")
    
    # Afficher les colonnes disponibles
    print("\nColonnes disponibles dans le fichier :")
    for i, col in enumerate(monde.columns):
        print(f"   {i}: '{col}'")
    
    # 10. Isoler les colonnes nécessaires avec gestion des noms
    etats = list(monde['État'].values)
    pop_2007 = list(monde['Pop 2007'].values)
    pop_2025 = list(monde['Pop 2025'].values)
    densite_2007 = list(monde['Densité 2007'].values)
    densite_2025 = list(monde['Densité 2025'].values)
    
    print("\n2. Colonnes extraites : État, Pop 2007, Pop 2025, Densité 2007, Densité 2025")
    
    # 11. Ordonner les listes
    ordre_pop_2007 = ordrePopulation(pop_2007, etats)
    ordre_pop_2025 = ordrePopulation(pop_2025, etats)
    ordre_densite_2007 = ordrePopulation(densite_2007, etats)
    ordre_densite_2025 = ordrePopulation(densite_2025, etats)
    
    print(f"\n3. Classements calculés pour population et densité (2007 et 2025)")
    print(f"   Pays dans classement Pop 2007 : {len(ordre_pop_2007)}")
    print(f"   Pays dans classement Pop 2025 : {len(ordre_pop_2025)}")
    print(f"   Pays dans classement Densité 2007 : {len(ordre_densite_2007)}")
    print(f"   Pays dans classement Densité 2025 : {len(ordre_densite_2025)}")
    
    # Afficher le top 10 des populations 2025
    print("\nTop 10 des pays par population en 2025 :")
    for i in range(min(10, len(ordre_pop_2025))):
        print(f"   {ordre_pop_2025[i][0]:3d}. {ordre_pop_2025[i][1]}")
    
    # 12 & 13. Préparer la comparaison Population 2007 vs 2025
    classement_pop = classementPays(ordre_pop_2007, ordre_pop_2025)
    classement_pop.sort()
    
    # Isoler les deux colonnes de rangs
    rangs_pop_2007 = [item[0] for item in classement_pop]
    rangs_pop_2025 = [item[1] for item in classement_pop]
    
    print(f"\n4. Comparaison Population 2007 vs 2025 : {len(classement_pop)} pays communs")
    
    # Préparer la comparaison Densité 2007 vs 2025
    classement_densite = classementPays(ordre_densite_2007, ordre_densite_2025)
    classement_densite.sort()
    
    rangs_densite_2007 = [item[0] for item in classement_densite]
    rangs_densite_2025 = [item[1] for item in classement_densite]
    
    print(f"   Comparaison Densité 2007 vs 2025 : {len(classement_densite)} pays communs")
    
    # 14. Calcul des coefficients de corrélation et concordance
    print("\n5. ANALYSE DES CORRÉLATIONS DE RANGS")
    print("-" * 80)
    
    # Pour la population
    spearman_pop, pvalue_spearman_pop = scipy.stats.spearmanr(rangs_pop_2007, rangs_pop_2025)
    kendall_pop, pvalue_kendall_pop = scipy.stats.kendalltau(rangs_pop_2007, rangs_pop_2025)
    
    print("\nA) POPULATION (2007 vs 2025)")
    print(f"   • Coefficient de corrélation de Spearman : {spearman_pop:.6f}")
    print(f"     (p-value : {pvalue_spearman_pop:.2e})")
    print(f"   • Coefficient de concordance de Kendall : {kendall_pop:.6f}")
    print(f"     (p-value : {pvalue_kendall_pop:.2e})")
    
    # Pour la densité
    spearman_densite, pvalue_spearman_densite = scipy.stats.spearmanr(rangs_densite_2007, rangs_densite_2025)
    kendall_densite, pvalue_kendall_densite = scipy.stats.kendalltau(rangs_densite_2007, rangs_densite_2025)
    
    print("\nB) DENSITÉ (2007 vs 2025)")
    print(f"   • Coefficient de corrélation de Spearman : {spearman_densite:.6f}")
    print(f"     (p-value : {pvalue_spearman_densite:.2e})")
    print(f"   • Coefficient de concordance de Kendall : {kendall_densite:.6f}")
    print(f"     (p-value : {pvalue_kendall_densite:.2e})")
    
    # Visualisation des résultats
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique Population
    ax = axes[0]
    ax.scatter(rangs_pop_2007, rangs_pop_2025, alpha=0.5, s=30)
    ax.plot([0, max(rangs_pop_2007)], [0, max(rangs_pop_2007)], 'r--', alpha=0.5, label='Parfaite concordance')
    ax.set_xlabel('Rang Population 2007', fontsize=12)
    ax.set_ylabel('Rang Population 2025', fontsize=12)
    ax.set_title(f'Classements Population\nSpearman: {spearman_pop:.4f} | Kendall: {kendall_pop:.4f}', 
                 fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Graphique Densité
    ax = axes[1]
    ax.scatter(rangs_densite_2007, rangs_densite_2025, alpha=0.5, s=30, color='green')
    ax.plot([0, max(rangs_densite_2007)], [0, max(rangs_densite_2007)], 'r--', alpha=0.5, label='Parfaite concordance')
    ax.set_xlabel('Rang Densité 2007', fontsize=12)
    ax.set_ylabel('Rang Densité 2025', fontsize=12)
    ax.set_title(f'Classements Densité\nSpearman: {spearman_densite:.4f} | Kendall: {kendall_densite:.4f}', 
                 fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comparaison_rangs_population_densite.png', dpi=300, bbox_inches='tight')
    print("\n   Graphique sauvegardé : comparaison_rangs_population_densite.png")
    plt.close()
    
    
    print("="*80)
    print("ANALYSE TERMINÉE AVEC SUCCÈS")
    print("="*80)
    print("\nFichiers générés :")
    print("  1. loi_rang_taille_iles.png")
    print("  2. comparaison_rangs_population_densite.png")

except Exception as e:
    print(f"\nERREUR lors de l'analyse des populations : {str(e)}")
    print("Vérifiez que le fichier existe et que les noms de colonnes sont corrects")
    import traceback
    traceback.print_exc()