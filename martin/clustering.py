# clustering des pays avec k-means sur les 11 categories
# idée : voir s'il y a des "profils" de pays et si ça colle avec les continents
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from chargement import charger_donnees, CATEGORIES

df = charger_donnees()

# kmeans plante s'il y a des NaN -> on remplace par la moyenne de la colonne
# (c'est surtout FSH, la peche, qui manque pour les 44 pays sans acces a la mer. pas parfait mais bon)
X = df[CATEGORIES].fillna(df[CATEGORIES].mean())
# pas de standardisation, tout est deja entre 0 et 100

# methode du coude pour choisir k
inerties = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X)
    inerties.append(km.inertia_)
plt.plot(range(1, 11), inerties, marker="o")
plt.xlabel("nombre de groupes k")
plt.ylabel("inertie (distance des pays au centre de leur groupe)")
plt.title("Méthode du coude")
plt.show()
# ça se casse vers k=4 donc on part là dessus

df["groupe"] = KMeans(n_clusters=4, n_init=10, random_state=0).fit_predict(X)

# moyenne de chaque categorie par groupe, c'est ce qui permet de comprendre qui est qui
profils = df.groupby("groupe")[CATEGORIES + ["EPI", "pib_hab"]].mean().round(0)
print(profils.to_string())

# est ce qu'on retrouve les regions ?
print(pd.crosstab(df["region"], df["groupe"]))

for g in range(4):
    print("Groupe", g, ":", ", ".join(df[df["groupe"] == g]["country"]))

# heatmap des profils (lignes = groupes, colonnes = categories)
plt.imshow(profils[CATEGORIES], cmap="Greens")
plt.xticks(range(len(CATEGORIES)), CATEGORIES)
plt.yticks(range(4), ["groupe " + str(g) for g in range(4)])
plt.colorbar(label="score moyen (0-100)", shrink=0.5)
plt.title("Profil moyen de chaque groupe")
plt.show()

# carte du monde
# contours des pays = natural earth, lu direct en ligne
# le /vsizip/vsicurl/ devant c'est parce que sur mon mac python refusait l'url (erreur de certificat SSL)
monde = gpd.read_file("/vsizip/vsicurl/https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip")
monde = monde[monde["ADM0_A3"] != "ATA"]  # pas besoin de l'antarctique
# merge sur le code pays. attention prendre ADM0_A3 et pas ISO_A3 (France et Norvege y sont a -99 !)
monde = monde.merge("groupe " + df["groupe"].astype(str), left_on="ADM0_A3", right_index=True, how="left")
ax = monde.plot(color="white", edgecolor="lightgrey", figsize=(12, 6))  # en blanc = pas noté dans l'EPI
monde.dropna(subset=["groupe"]).plot(column="groupe", categorical=True, cmap="tab10", legend=True, ax=ax)
ax.set_title("Groupes K-means des pays (11 catégories de l'EPI)")
ax.set_axis_off()
plt.show()
