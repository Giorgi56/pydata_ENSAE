"""Clustering K-means : regrouper les pays qui ont un profil environnemental proche (11 catégories)."""
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from chargement import charger_donnees, CATEGORIES

df = charger_donnees()

# K-means n'accepte pas les valeurs manquantes : on les remplace par la moyenne de la catégorie
# (surtout la pêche, absente pour les 44 pays sans littoral)
X = df[CATEGORIES].fillna(df[CATEGORIES].mean())
# Pas besoin de standardiser : toutes les catégories sont déjà notées de 0 à 100

# 1. Méthode du coude : on regarde à partir de quel k ajouter un groupe n'aide plus beaucoup
inerties = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    inerties.append(km.inertia_)
plt.plot(range(1, 11), inerties, marker="o")
plt.xlabel("nombre de groupes k")
plt.ylabel("inertie (distance des pays au centre de leur groupe)")
plt.title("Méthode du coude")
plt.show()

# 2. K-means avec 4 groupes
df["groupe"] = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(X)

# profil moyen de chaque groupe : c'est ce qui permet de leur donner un nom
profils = df.groupby("groupe")[CATEGORIES + ["EPI", "pib_hab"]].mean().round(0)
print(profils.to_string())

# les groupes recoupent-ils les régions du monde ?
print(pd.crosstab(df["region"], df["groupe"]))

for g in range(4):
    print("Groupe", g, ":", ", ".join(df[df["groupe"] == g]["country"]))

# 3. Carte de chaleur des profils : une ligne par groupe, une colonne par catégorie
plt.imshow(profils[CATEGORIES], cmap="Greens")
plt.xticks(range(len(CATEGORIES)), CATEGORIES)
plt.yticks(range(4), ["groupe " + str(g) for g in range(4)])
plt.colorbar(label="score moyen (0-100)", shrink=0.5)
plt.title("Profil moyen de chaque groupe")
plt.show()

# 4. Carte du monde colorée par groupe
# Contours des pays : Natural Earth (lu directement en ligne ; "/vsizip/vsicurl/" évite un souci de certificat SSL)
monde = gpd.read_file("/vsizip/vsicurl/https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")
# on relie les deux tableaux par le code pays à 3 lettres (ADM0_A3 dans Natural Earth, iso dans l'EPI)
monde = monde[monde["ADM0_A3"] != "ATA"]  # on retire l'Antarctique
monde = monde.merge("groupe " + df["groupe"].astype(str), left_on="ADM0_A3", right_index=True, how="left")
ax = monde.plot(color="white", edgecolor="lightgrey", figsize=(12, 6))  # fond blanc = pays non notés
monde.dropna(subset=["groupe"]).plot(column="groupe", categorical=True, cmap="tab10", legend=True, ax=ax)
ax.set_title("Groupes K-means des pays (11 catégories de l'EPI)")
ax.set_axis_off()
plt.show()
