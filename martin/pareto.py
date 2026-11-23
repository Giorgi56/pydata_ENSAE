# classer les pays sans choisir de poids : fronts de Pareto sur les 3 objectifs (sante, ecosystemes, climat)
import matplotlib.pyplot as plt
from chargement import charger_donnees

df = charger_donnees()
obj = ["HLT", "ECO", "PCC"]


def domine(a, b):
    """a domine b si a fait au moins aussi bien partout et mieux sur au moins un objectif"""
    return (a >= b).all() and (a > b).any()


# front 1 = les pays que personne ne domine. on les enleve et on recommence -> front 2, etc
reste = df[obj]
f = 1
while len(reste) > 0:
    v = reste.values
    front = [reste.index[i] for i in range(len(v)) if not any(domine(v[j], v[i]) for j in range(len(v)))]
    df.loc[front, "front"] = f
    reste = reste.drop(front)
    f += 1

for f in [1, 2, 3]:
    print("front", f, ":", ", ".join(df[df["front"] == f]["country"]))
# si A est dans un meilleur front que B, A passe devant B quels que soient les poids choisis
print(df.loc[["FRA", "USA", "CHN", "IND", "QAT"], ["country", "EPI", "front"]])

# comparaison avec le classement EPI du papier
df["rang_epi"] = df["EPI"].rank(ascending=False, method="min")
df["rang_pareto"] = df["front"].rank(method="min")  # ex aequo : tout le front a le rang de son 1er pays
print("corrélation des rangs :", round(df["rang_epi"].corr(df["rang_pareto"], method="spearman"), 2))
# dans un meme front l'ordre EPI vient juste des poids (ex : front 4 va du 11e au 110e)
print(df.groupby("front")["rang_epi"].agg(["count", "min", "max"]))
# ecart > 0 : monte avec pareto (les "specialistes" bons sur un seul objectif)
# ecart < 0 : descend (les pays moyens partout)
df["ecart"] = df["rang_epi"] - df["rang_pareto"]
colonnes = ["country", "rang_epi", "front", "ecart"] + obj
print(df.sort_values("ecart")[colonnes].head(6))
print(df.sort_values("ecart")[colonnes].tail(6))

plt.scatter(df["HLT"], df["PCC"], c=df["front"], cmap="viridis_r")
plt.colorbar(label="front de Pareto")
plt.xlabel("santé environnementale (HLT)")
plt.ylabel("climat (PCC)")
plt.title("Fronts de Pareto (3e objectif, ECO, pas affiché)")
plt.show()
