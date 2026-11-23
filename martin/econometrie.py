# partie econometrie : est-ce que l'EPI c'est juste la richesse du pays ?
import numpy as np
import statsmodels.formula.api as smf
from chargement import charger_donnees, CATEGORIES

df = charger_donnees()
df["log_pib"] = np.log(df["pib_hab"])  # en log sinon le Qatar, le Luxembourg etc écrasent tout

# --- 1) MCO simple EPI ~ log(pib/hab)
# HC1 = ecarts types robustes (l'equivalent du ", robust" sous Stata)
reg1 = smf.ols("EPI ~ log_pib", data=df).fit(cov_type="HC1")
print(reg1.summary())

# residu = EPI observé - EPI prédit par la richesse
# => en gros ca mesure l'effort environnemental du pays a richesse donnée (c'est ça qui est intéressant)
df["residu"] = reg1.resid
colonnes = ["country", "pib_hab", "EPI", "residu"]
print("moins bien que ce que leur richesse prédit :")
print(df.sort_values("residu")[colonnes].head(10))
print("mieux que prévu :")
print(df.sort_values("residu")[colonnes].tail(10))

# --- 2) dans l'autre sens : log(pib) sur les 11 categories
# pas causal du tout, c'est juste pour voir quel profil ont les pays riches
# rq : statsmodels vire tout seul les pays sans score de peche (pays sans littoral) -> N = 127
# on avait essayé avec les 40 indicateurs mais trop de variables pour trop peu de pays, ça marchait pas
reg2 = smf.ols("log_pib ~ " + " + ".join(CATEGORIES), data=df).fit(cov_type="HC1")
print(reg2.summary())
