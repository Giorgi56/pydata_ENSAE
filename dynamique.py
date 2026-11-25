import pandas as pd
import os

dossier = "raw_data/2022-epi-indicators-time-series-na"

df_global = None


# On parcourt les 40 fichiers CSV : pour chaque indicateur, on transforme
# les années en lignes avec melt(), puis on effectue une jointure sur
# les pays et les années afin de construire un DataFrame global (et surtout dynamique).
# Les valeurs manquantes (NaN) sont conservées pour être traitées ensuite.

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


# Récupération des régions depuis le fichier Excel EPI 2022
df_original = pd.read_excel(
    "raw_data/2022-epi.xlsx",
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

# Création d'une copie pour le traitement des valeurs manquantes
df_etude = df_etude_na.copy()

# Sélection des 40 indicateurs
indicateurs = df_etude.columns.drop(
    ["code", "iso", "country", "year", "region"]
)

# Imputation par la moyenne régionale pour chaque année pour les NA qui restent
df_etude[indicateurs] = df_etude[indicateurs].fillna(
    df_etude.groupby(["region", "year"])[indicateurs].transform("mean")
)

# Sauvegarde des deux bases de données
df_etude_na.to_csv("epi_historique_nettoye_na.csv", index=False)
df_etude.to_csv("epi_historique_nettoye.csv", index=False)

# Importation des nouvelles pondérations
df_poids = pd.read_excel("clear_indices.xlsx")


# Importation de la nomenclature officielle de l'EPI
df_poids_officiels = pd.read_excel(
    "raw_data/2022-epi.xlsx",
    sheet_name="6_EPI_Weights"
)

# Ajout des acronymes et de la structure hiérarchique
df_poids = df_poids.merge(
    df_poids_officiels[
        ["Variable", "Abbreviation", "Type", "NextLevel"]
    ],
    on="Variable",
    how="left",
    validate="one_to_one"
)

# Sélection des poids finaux des 26 indicateurs retenus
poids = df_poids[df_poids["Type"] == "Indicator"].set_index(
    "Abbreviation"
)["Final"]

# Calcul du nouvel EPI par somme pondérée des 26 indicateurs
# pour chaque pays et chaque année
df_etude["EPI_new"] = (
    df_etude[poids.index] * poids
).sum(axis=1, skipna=False)


# Sauvegarde de la base historique avec le nouvel EPI
df_etude.to_csv("epi_historique_final.csv", index=False)