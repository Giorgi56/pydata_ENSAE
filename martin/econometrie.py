"""Économétrie : lien entre l'EPI et la richesse des pays (MCO)."""
import numpy as np
import statsmodels.formula.api as smf
from chargement import charger_donnees, CATEGORIES

df = charger_donnees()
df["log_pib"] = np.log(df["pib_hab"])  # log car le PIB par habitant est très asymétrique

# 1. L'EPI est-il expliqué par la richesse ?
# cov_type="HC1" = écarts-types robustes, comme ", robust" dans Stata
reg1 = smf.ols("EPI ~ log_pib", data=df).fit(cov_type="HC1")
print(reg1.summary())

# Résidu = EPI observé - EPI prédit par la richesse.
# Le résidu devient ainsi une mesure de l'effort environnemental à richesse donnée.
df["residu"] = reg1.resid
colonnes = ["country", "pib_hab", "EPI", "residu"]
print("Pays qui font moins bien que leur richesse le prédit :")
print(df.sort_values("residu")[colonnes].head(10))
print("Pays qui font mieux que leur richesse le prédit :")
print(df.sort_values("residu")[colonnes].tail(10))

# 2. Quel profil environnemental distingue les pays riches ?
# (descriptif, pas causal ; les pays sans score de pêche sont retirés automatiquement)
reg2 = smf.ols("log_pib ~ " + " + ".join(CATEGORIES), data=df).fit(cov_type="HC1")
print(reg2.summary())
