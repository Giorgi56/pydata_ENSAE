"""Chargement des données EPI 2022 (déjà dans raw_data/, pas besoin de l'API)."""
import pandas as pd

# Les 11 catégories de l'EPI (codes de la feuille 6 de l'Excel)
CATEGORIES = ["BDH", "ECS", "FSH", "ACD", "AGR", "WRS", "AIR", "H2O", "HMT", "WMG", "CCH"]


def charger_donnees():
    """Renvoie un tableau avec une ligne par pays : région, EPI, 11 catégories, PIB par habitant 2020."""
    epi = pd.read_excel("raw_data/2022-epi.xlsx", sheet_name="3_EPI_Results").set_index("iso")
    # les colonnes ".new" sont les scores 2022
    colonnes = ["EPI"] + CATEGORIES
    df = epi[["country", "region"] + [c + ".new" for c in colonnes]].copy()
    df.columns = ["country", "region"] + colonnes

    # PIB par habitant (2020 = dernière année disponible)
    pib = pd.read_csv("raw_data/2022-epi-raw-data-time-series-na/GPC_raw_na.csv").set_index("iso")
    df["pib_hab"] = pib["GPC.raw.2020"]
    return df
