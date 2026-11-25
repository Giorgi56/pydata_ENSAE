## Structure du projet (partie niels)

```text
pydata_ENSAE/
├── carte/
│   ├── carte_epi_interactive_2022.html
│   ├── carte_epi_interactive_regions_2022.html
│   ├── carte_epi_statique_2022.png
│   └── world.geojson
│
├── epi(historique)/
│   ├── epi_historique.csv
│   ├── epi_historique_nettoye_na.csv
│   ├── epi_historique_nettoye.csv
│   └── epi_historique_final.csv
│
├── graphique(dynamique)/
│   ├── classement_variation_epi_par_pays.png
│   ├── evolution_classement_par_region.png
│   ├── evolution_epi_mondial.png
│   └── evolution_epi_par_region.png
│
├── niels/
│   ├── clear_indices.xlsx
│   ├── dynamique.py
│   ├── dynamique_graphique.py
│   └── map.py
└── requirements.txt



### Description des dossiers et fichiers

- `carte/` : cartes statiques et interactives de l'EPI 2022.
- `epi(historique)/` : bases de données historiques aux différentes étapes du traitement.
- `graphique(dynamique)/` : graphiques de l'analyse dynamique du nouvel EPI entre 1995 et 2022.
- `niels/` : fichiers relatifs à la construction et à l'analyse du nouvel EPI.
  - `clear_indices.xlsx` : nouvelles pondérations des 26 indicateurs retenus.
  - `dynamique.py` : construction de la base historique, traitement des valeurs manquantes et calcul du nouvel EPI.
  - `dynamique_graphique.py` : fonctions de visualisation de l'évolution du nouvel EPI.
  - `map.py` : génération des cartes statiques et interactives.
- `raw_data/` : données sources de l'EPI.
- `requirements.txt` : dépendances Python
```