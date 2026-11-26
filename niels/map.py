import matplotlib.pyplot as plt


# Cartographie de l'indice de performance environnementale (EPI) en 2022.

# La version initiale de Natural Earth qu'on utilisait (1:110 millions) ne représentait pas
# certains petits pays évalués par l'EPI, comme Singapour et Malte, ce qui entraînait des correspondances manquantes.
# Le passage à l'échelle 1:50 millions permet de représenter les 180 pays EPI.


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
