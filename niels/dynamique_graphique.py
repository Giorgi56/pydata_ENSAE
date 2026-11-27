# Graphiques pour l'analyse dynamique du nouvel EPI et de l'EPI officiel entre 1995 et 2022.
#
# Les visualisations sont réalisées à partir de la base historique
# construite dans le fichier dynamique.py.

import pandas as pd
import matplotlib.pyplot as plt


# 1. Évolution de l'EPI moyen et médian mondial

def graphique_evolution_epi_moyen_median_mondial(
    df, nom_indice, colonne_epi="EPI_new"):

    epi_moyen = df.groupby("year")[colonne_epi].mean()
    epi_median = df.groupby("year")[colonne_epi].median()

    plt.figure(figsize=(12, 6))

    plt.plot(epi_moyen.index, epi_moyen.values, label="Moyenne")
    plt.plot(epi_median.index, epi_median.values, label="Médiane")

    plt.title(f"{nom_indice} : évolution mondiale (1995-2022)")
    plt.xlabel("Année")
    plt.ylabel("Score EPI")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# 2. Évolution de l'EPI moyen par région

def graphique_evolution_epi_moyen_par_region(
    df, nom_indice, colonne_epi="EPI_new"):

    # Calcul de l'EPI moyen par région et par année
    epi_regions = df.groupby(
        ["year", "region"]
    )[colonne_epi].mean().unstack()

    plt.figure(figsize=(12, 6))

    # Une courbe pour chaque région
    for region in epi_regions.columns:
        plt.plot(epi_regions.index, epi_regions[region], label=region)

    plt.title(f"{nom_indice} : évolution par région (1995-2022)")
    plt.xlabel("Année")
    plt.ylabel("Score EPI moyen")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()


# 3. Classement des pays ayant le plus et le moins progressé

def graphique_classement_variation_epi_par_pays(
    df, nom_indice, colonne_epi="EPI_new"):

    # Récupération des scores EPI par pays et par année
    epi_pays = df.pivot(
        index="country",
        columns="year",
        values=colonne_epi
    )

    # Calcul de la variation entre 1995 et 2022
    variation = (epi_pays[2022] - epi_pays[1995]).dropna()

    # Sélection des 10 meilleures et 10 moins bonnes évolutions
    top_10 = variation.nlargest(10)
    bottom_10 = variation.nsmallest(10)

    classement = pd.concat([top_10, bottom_10]).sort_values()

    # Récupération de la région de chaque pays
    regions = df.drop_duplicates("country").set_index("country")["region"]

    # Ajout de la région entre parenthèses
    labels = [
        f"{pays} ({regions[pays]})"
        for pays in classement.index
    ]

    # Couleur selon le signe de la variation
    couleurs = ["green" if v >= 0 else "red" for v in classement]

    plt.figure(figsize=(14, 8))

    plt.barh(labels, classement.values, color=couleurs)

    plt.axvline(0, color="black", linewidth=1)
    plt.title(
        f"{nom_indice} : meilleures et moins bonnes évolutions (1995-2022)"
    )
    plt.xlabel("Variation de l'EPI en points")
    plt.ylabel("Pays (région)")
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.show()


# 4. Évolution du classement international moyen par région

def graphique_evolution_classement_par_region(


    df, nom_indice, colonne_epi="EPI_new"):

    df_classement = df.copy()

    # Calcul du rang international de chaque pays pour chaque année
    df_classement["rang"] = df_classement.groupby("year")[colonne_epi].rank(
        ascending=False,
        method="min"
    )

    # Calcul du rang moyen par région et par année
    rang_regions = df_classement.groupby(
        ["year", "region"]
    )["rang"].mean().unstack()

    plt.figure(figsize=(12, 6))

    # Une courbe pour chaque région
    for region in rang_regions.columns:
        plt.plot(rang_regions.index, rang_regions[region], label=region)

    # Inversion de l'axe vertical pour placer les meilleurs rangs en haut
    plt.gca().invert_yaxis()

    plt.title(
        f"{nom_indice} : évolution du classement par région (1995-2022)"
    )
    plt.xlabel("Année")
    plt.ylabel("Rang international moyen")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()



# Tableau de synthèse des évolutions du classement par région

def tableau_synthese_evolution_par_region(df):
    '''
    Calcule les gains et pertes de places dans le classement
    international moyen de chaque région entre 1995 et 2022,
    selon l'EPI officiel et le nouvel EPI.
    '''
    df_rangs = df.copy()

    # Calcul des rangs internationaux pour les deux indices
    for indice in ["EPI_officiel", "EPI_new"]:
        df_rangs[f"rang_{indice}"] = (
            df_rangs.groupby("year")[indice].rank(
                ascending=False, method="min"
            )
        )

    # Calcul des rangs moyens par région et par année
    synthese = df_rangs.groupby(["region", "year"])[
        ["rang_EPI_officiel", "rang_EPI_new"]
    ].mean()

    # Sélection des années 1995 et 2022
    debut = synthese.xs(1995, level="year")
    fin = synthese.xs(2022, level="year")

    # Construction du tableau de synthèse
    tableau = pd.DataFrame({
        "Gain de places (EPI officiel)": debut["rang_EPI_officiel"] - fin["rang_EPI_officiel"],
        "Gain de places (nouvel EPI)": debut["rang_EPI_new"] - fin["rang_EPI_new"]
    })

    return tableau.round(2)