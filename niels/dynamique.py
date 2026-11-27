import pandas as pd
import os
# Construction de la base historique et calcul du nouvel EPI et de l'EPI officiel (1995-2022).

def construire_base_historique(dossier):
    """
    Fusionne les 40 fichiers CSV en une base historique par pays et par année.
    """
    df_global = None

    for fichier in sorted(os.listdir(dossier)):

        if not fichier.endswith("_ind_na.csv"):
            continue

        # Nom de l'indicateur (BCA, BHV, CDA...)
        indicateur = fichier.split("_")[0]

        df = pd.read_csv(dossier + "/" + fichier)

        # Transformation des années en lignes
        df = df.melt(
            id_vars=["code", "iso", "country"],
            var_name="year",
            value_name=indicateur
        )

        # Extraction de l'année
        df["year"] = df["year"].str.extract(r"(\d{4})").astype(int)

        # Jointure avec les indicateurs précédents
        if df_global is None:
            df_global = df
        else:
            df_global = pd.merge(
                df_global,
                df,
                on=["code", "iso", "country", "year"],
                how="outer"
            )

    return df_global

def ajouter_regions(df_global, chemin_excel):
    """
    Ajoute les régions à la base historique et conserve uniquement
    les pays présents dans l'EPI 2022, sans imputer les valeurs manquantes.
    """

    df_original = pd.read_excel(
        chemin_excel,
        sheet_name="3_EPI_Results"
    )
    
    # On conserve uniquement les codes ISO et les régions
    df_regions = df_original[["iso", "region"]]

    # Ajout de la région à chaque pays de notre base historique
    df_global = pd.merge(
        df_global,
        df_regions,
        on="iso",
        how="left",
        validate="many_to_one"
    )

    # On conserve uniquement les 180 pays présents dans l’EPI 2022
    df_etude_na = df_global[df_global["region"].notna()].copy()

    return df_etude_na

def imputer_valeurs_manquantes(df_etude_na):
    """
    Impute les valeurs manquantes de chaque indicateur par la moyenne
    régionale de l'année correspondante, sans modifier la base initiale.
    """

    df_etude = df_etude_na.copy()

    # Sélection des 40 indicateurs
    indicateurs = df_etude.columns.drop(
        ["code", "iso", "country", "year", "region"]
    )

    df_etude[indicateurs] = df_etude[indicateurs].fillna(
        df_etude.groupby(["region", "year"])[indicateurs].transform("mean")
    )

    return df_etude

def charger_ponderations_nouvelles(chemin_poids, chemin_excel):
    """
    Importe les nouvelles pondérations et la nomenclature officielle
    de l'EPI, puis extrait les poids finaux des 26 indicateurs retenus.
    """

    df_poids = pd.read_excel(chemin_poids)

    df_poids_officiels = pd.read_excel(
        chemin_excel,
        sheet_name="6_EPI_Weights"
    )

    df_poids = df_poids.merge(
        df_poids_officiels[
            ["Variable", "Abbreviation", "Type", "NextLevel"]
        ],
        on="Variable",
        how="left",
        validate="one_to_one"
    )
    poids = df_poids[df_poids["Type"] == "Indicator"].set_index(
        "Abbreviation"
    )["Final"]

    return poids

def charger_ponderations_officielles(chemin_excel):
    """
    Calcule les poids finaux officiels des 40 indicateurs
    à partir de la hiérarchie des pondérations de l'EPI 2022.
    """

    df = pd.read_excel(
        chemin_excel,
        sheet_name="6_EPI_Weights"
    ).set_index("Abbreviation")

    poids_finaux = {}

    for indicateur in df[df["Type"] == "Indicator"].index:

        categorie = df.loc[indicateur, "NextLevel"]
        objectif = df.loc[categorie, "NextLevel"]

        poids_finaux[indicateur] = (
            df.loc[indicateur, "Weight"]
            * df.loc[categorie, "Weight"]
            * df.loc[objectif, "Weight"]
        )

    return pd.Series(poids_finaux)

def calculer_epi(df_etude, poids, nom_colonne="EPI_new"):
    """
    Calcule un indice EPI pour chaque pays et chaque année
    par somme pondérée des indicateurs.
    """

    df_final = df_etude.copy()

    df_final[nom_colonne] = (
        df_final[poids.index] * poids
    ).sum(axis=1, skipna=False)

    return df_final


