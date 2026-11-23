# Cartographie de l'indice de performance environnementale (EPI) en 2022.
# Représentation statique et interactive des scores par pays.

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# 1. Chargement des données EPI

# Lecture du fichier Excel contenant les résultats officiels de l'EPI 2022.
# On conserve les codes ISO, les noms des pays et leurs scores EPI.

df_original = pd.read_excel(
    "raw_data/2022-epi.xlsx",
    sheet_name="3_EPI_Results"
)

df = df_original[["iso", "country", "EPI.new"]]


# 2. Chargement des données géographiques

# Données issues de Natural Earth (échelle 1:50 millions).
# Ce dataset fournit les frontières des pays (geometry), leurs noms (ADMIN)
# et leurs codes à trois lettres (ADM0_A3).


url = (
    "https://naturalearth.s3.amazonaws.com/"
    "50m_cultural/ne_50m_admin_0_countries.zip"
)

world = gpd.read_file(url)


# Enregistrement du jeu de données géographiques en local
# world.to_file("raw_data/world.geojson", driver="GeoJSON")


# 3. Jointure des données EPI et géographiques

# On associe les frontières des pays (geometry) à leurs scores (EPI.new)
# grâce aux codes ISO à trois lettres.
# La jointure à gauche conserve tous les territoires de Natural Earth,
# y compris ceux sans score EPI correspondant (NaN).
# On obtient un GeoDataFrame associant les frontières des pays à leurs scores EPI.

carte = world.merge(
    df,
    left_on="ADM0_A3",
    right_on="iso",
    how="left"
)


# Vérification des valeurs manquantes :
# La version initiale de Natural Earth (1:110 millions) ne représentait pas
# certains petits pays évalués par l'EPI, comme Singapour et Malte.
# Le passage à l'échelle 1:50 millions permet de représenter les 180 pays EPI.
# Les 62 valeurs manquantes restantes correspondent à des territoires
# supplémentaires de Natural Earth, sans score EPI dans notre fichier (carte["EPI.new"].isna().sum()).
# Ils sont conservés sur la carte et affichés en gris.


# 4. Création de la carte statique

# Représentation des scores EPI par un dégradé allant du jaune (score faible)
# au vert foncé (score élevé). Les territoires sans score apparaissent en gris.


fig, ax = plt.subplots(figsize=(15, 8))

carte.plot(
    column="EPI.new",
    cmap="YlGn",
    legend=True,
    legend_kwds={"label": "Score EPI (sur 100)"},
    missing_kwds={"color": "lightgrey"},
    ax=ax
)

ax.set_title("Indice de performance environnementale (EPI) en 2022")
ax.set_axis_off()

plt.savefig("carte_epi_statique_2022.png", dpi=300, bbox_inches="tight")


# 5. Création de la carte interactive

# Carte interactive permettant de zoomer, de se déplacer et de consulter
# le nom et le score EPI de chaque pays au survol de la souris.
# Le dégradé de couleurs reste identique à celui de la carte statique.

m = carte.explore(
    column="EPI.new",
    cmap="YlGn",
    legend=True,
    legend_kwds={"caption": "Score EPI"},
    tooltip=["ADMIN", "EPI.new"],
    tooltip_kwds={"aliases": ["Pays :", "Score EPI :"]},
    missing_kwds={"color": "lightgrey"}
)

m.save("carte_epi_interactive_2022.html")


# Même raisonnement pour que la carte précèdente, sauf qu'on procède par régions


df2 = df_original[["iso", "country", "region", "EPI.new"]]


moyennes_regions = (
    df2.groupby("region")["EPI.new"]
    .mean()
)


carte2 = world.merge(
    df2,
    left_on="ADM0_A3",
    right_on="iso",
    how="left"
)


carte2["EPI_moyen_region"] = (
    carte2["region"].map(moyennes_regions)
)

carte2.loc[
    carte2["EPI.new"].isna(),
    "EPI_moyen_region"
] = float("nan")

m2 = carte2.explore(
    column="EPI_moyen_region",
    cmap="RdYlGn",
    vmin=0,
    vmax=100,
    legend=True,
    legend_kwds={
        "caption": "Score EPI moyen par région"
    },
    tooltip=[
        "ADMIN",
        "region",
        "EPI.new",
        "EPI_moyen_region"
    ],
    tooltip_kwds={
        "aliases": [
            "Pays :",
            "Région :",
            "Score EPI du pays :",
            "Score EPI moyen de la région :"
        ]
    },
    missing_kwds={"color": "lightgrey"}
)

m2.save("carte_epi_interactive_regions_2022.html")
