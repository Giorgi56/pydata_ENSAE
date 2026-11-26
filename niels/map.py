# Cartographie de l'indice de performance environnementale (EPI) en 2022.
# Représentation statique et interactive des scores par pays.

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


# 1. Chargement des données EPI

df_original = pd.read_excel(
    "raw_data/2022-epi.xlsx",
    sheet_name="3_EPI_Results"
)

df = df_original[["iso", "country", "region", "EPI.new"]]


# 2. Chargement des données géographiques

# Données issues de Natural Earth (échelle 1:50 millions).
# Ce dataset fournit les frontières des pays (geometry), leurs noms (ADMIN)
# et leurs codes à trois lettres (ADM0_A3).


url = (
    "https://naturalearth.s3.amazonaws.com/"
    "50m_cultural/ne_50m_admin_0_countries.zip"
)

world = gpd.read_file(url)


# Sauvegarde
#world.to_file("carte/world.geojson", driver="GeoJSON")

# 3. Jointure des données EPI et géographiques

# On associe les frontières des pays (geometry) à leurs scores (EPI.new)
# grâce aux codes ISO à trois lettres.
# La jointure à gauche conserve tous les territoires de Natural Earth,
# y compris ceux sans score EPI correspondant (NaN).
# On obtient un GeoDataFrame 

carte = world.merge(
    df,
    left_on="ADM0_A3",
    right_on="iso",
    how="left"
)


# Vérification des valeurs manquantes :
# La version initiale de Natural Earth qu'on utilisait (1:110 millions) ne représentait pas
# certains petits pays évalués par l'EPI, comme Singapour et Malte, ce qui entraînait des correspondances manquantes.
# Le passage à l'échelle 1:50 millions permet de représenter les 180 pays EPI.
# Les 62 valeurs manquantes restantes correspondent à des territoires
# supplémentaires de Natural Earth, sans score EPI dans notre fichier (carte["EPI.new"].isna().sum()).
# Ils sont conservés sur la carte et affichés en gris.


# 4. Préparation des données pour la cartographie par région

# Calcul du score EPI moyen par région
moyennes_regions = (
    df.groupby("region")["EPI.new"]
    .mean()
)

# Association des moyennes régionales aux pays
carte2 = carte.copy()

carte2["EPI_moyen_region"] = (
    carte2["region"].map(moyennes_regions)
)

# Conservation des valeurs manquantes pour les territoires sans score EPI
carte2.loc[
    carte2["EPI.new"].isna(),
    "EPI_moyen_region"
] = float("nan")


# 5. Fonctions de création des cartes

def carte_statique_pays(carte):
    """
    Crée une carte statique des scores EPI par pays.
    Les territoires sans score sont représentés en gris.
    """

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

    return fig


def carte_interactive_pays(carte):
    """
    Crée une carte interactive permettant de zoomer, de se déplacer
    et de consulter le nom et le score EPI de chaque pays.
    """

    m = carte.explore(
        column="EPI.new",
        cmap="YlGn",
        legend=True,
        legend_kwds={"caption": "Score EPI"},
        tooltip=["ADMIN", "EPI.new"],
        tooltip_kwds={"aliases": ["Pays :", "Score EPI :"]},
        missing_kwds={"color": "lightgrey"}
    )

    return m


def carte_interactive_regions(carte2):
    """
    Crée une carte interactive représentant les scores EPI moyens
    par région et permet de consulter les scores individuels et régionaux.
    """

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

    return m2


# ===================
# Programme principal 
# ===================

# 1. Création de la carte statique par pays
fig = carte_statique_pays(carte)

# Sauvegarde
#fig.savefig("carte/carte_epi_statique_2022.png", dpi=300, bbox_inches="tight")


# 2. Création de la carte interactive par pays
m = carte_interactive_pays(carte)

# Sauvegarde
#m.save("carte/carte_epi_interactive_2022.html")


# 3. Création de la carte interactive par région
m2 = carte_interactive_regions(carte2)

# Sauvegarde
#m2.save("carte/carte_epi_interactive_regions_2022.html")