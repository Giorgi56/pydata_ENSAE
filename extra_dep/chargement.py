# chargement des donnees EPI 2022
# les fichiers sont deja dans raw_data/ donc pas besoin de passer par get_d2.py
import pandas as pd

# codes des 11 categories (cf feuille 6 de l'excel)
CATEGORIES = ["BDH", "ECS", "FSH", "ACD", "AGR", "WRS", "AIR", "H2O", "HMT", "WMG", "CCH"]


def charger_donnees():
    """une ligne par pays : region, EPI, les 11 categories et le PIB/hab de 2020"""
    epi = pd.read_excel("raw_data/2022-epi.xlsx", sheet_name="3_EPI_Results").set_index("iso")
    # .new = score 2022 (.old c'est l'annee de reference, on s'en sert pas ici)
    colonnes = ["EPI", "HLT", "ECO", "PCC"] + CATEGORIES  # HLT ECO PCC = les 3 objectifs
    df = epi[["country", "region"] + [c + ".new" for c in colonnes]].copy()
    df.columns = ["country", "region"] + colonnes

    # pib par hab, on prend 2020 car c'est la derniere annee dispo dans GPC
    pib = pd.read_csv("raw_data/2022-epi-raw-data-time-series-na/GPC_raw_na.csv").set_index("iso")
    df["pib_hab"] = pib["GPC.raw.2020"]
    return df
