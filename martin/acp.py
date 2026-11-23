# ACP sur les 11 categories
# les poids de l'EPI sont choisis par des experts -> et si on laissait les données choisir ?
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from chargement import charger_donnees, CATEGORIES

df = charger_donnees()
X = df[CATEGORIES].fillna(df[CATEGORIES].mean())  # meme astuce que pour le kmeans (NaN de la peche)

# ACP normée (on centre-réduit, comme en cours) sinon les categories qui varient beaucoup prennent tout
Z = StandardScaler().fit_transform(X)
acp = PCA().fit(Z)

# eboulis des valeurs propres : combien d'axes il faut pour résumer les pays ?
plt.bar(range(1, 12), acp.explained_variance_ratio_ * 100)
plt.xlabel("axe")
plt.ylabel("% de variance expliquée")
plt.title("Eboulis des valeurs propres")
plt.show()
print("variance expliquée par les axes 1 et 2 :", acp.explained_variance_ratio_[:2].round(2))

# poids officiels d'une categorie = son poids x le poids de son objectif (feuille 6)
w = pd.read_excel("raw_data/2022-epi.xlsx", sheet_name="6_EPI_Weights").set_index("Abbreviation")
poids = pd.DataFrame(index=CATEGORIES)
poids["officiel"] = [w.loc[c, "Weight"] * w.loc[w.loc[c, "NextLevel"], "Weight"] for c in CATEGORIES]

# poids "ACP" = coefficients de l'axe 1 ramenés à une somme de 1
# (le signe d'un axe est arbitraire, on le retourne si besoin pour que ce soit positif)
axe1 = acp.components_[0] * np.sign(acp.components_[0].sum())
poids["acp"] = axe1 / axe1.sum()
print(poids.round(3))

# nouvel indice avec les poids de l'ACP, puis on compare les classements
df["epi_acp"] = X @ poids["acp"]
df["rang_officiel"] = df["EPI"].rank(ascending=False)
df["rang_acp"] = df["epi_acp"].rank(ascending=False)
df["places_gagnees"] = df["rang_officiel"] - df["rang_acp"]
print("corrélation des rangs :", round(df["rang_officiel"].corr(df["rang_acp"]), 2))
colonnes = ["country", "EPI", "rang_officiel", "rang_acp", "places_gagnees"]
print(df.sort_values("places_gagnees")[colonnes].head(10))  # ceux qui perdent le plus
print(df.sort_values("places_gagnees")[colonnes].tail(10))  # ceux qui gagnent le plus

# plan factoriel (axes 1 et 2), en couleur les groupes du kmeans (memes reglages que clustering.py)
groupes = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(X)
coord = acp.transform(Z)
plt.scatter(coord[:, 0], coord[:, 1], c=groupes, cmap="tab10")
for pays in ["FRA", "USA", "CHN", "IND", "QAT", "SAU", "TUR", "DNK", "BRA", "NER"]:
    i = df.index.get_loc(pays)
    plt.annotate(pays, (coord[i, 0], coord[i, 1]))
plt.xlabel("axe 1 (" + str(round(acp.explained_variance_ratio_[0] * 100)) + " %)")
plt.ylabel("axe 2 (" + str(round(acp.explained_variance_ratio_[1] * 100)) + " %)")
plt.title("Plan factoriel, couleur = groupe kmeans")
plt.show()
