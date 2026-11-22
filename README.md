Niels Souffir, Giorgi Kupradze, Martin Loup

# pydata_ENSAE
Projet du cours 'Python pour la Datascience' de l'ENSAE Paris

![Couverture faite par Lindsey Kernodle](cover.png)

Nous utilisons un dataset fourni par la NASA, intitulé **"2022 Environmental Performance Index (EPI)"**.
Lien vers le dataset: [EarthDATA/NASA/EPI](https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-epi-2022-2022.00)

## Comment faire tourner notre code?
1. Installer les dépendances en une commande:
```bash
pip install -r requirements.txt
```

2. Installer les données brutes du site [EarthDATA/NASA/EPI](https://www.earthdata.nasa.gov/data/catalog/sedac-ciesin-sedac-epi-2022-2022.00) dans ./raw_data/ (installer le fichier zip intitulé **2022-epi-raw-data-time-series-na-csv.zip**)

3. Extraire les données dans le même dossier

4. Faire tourner le fichier python principal:
```bash
python3 main.py
```

## Plan détaillé des tâches à réaliser:

- [x] Trouver le sujet et le dataset, télécharger les données CSV
- [x] Compléter le squelette de la branche main
- [x] Se partager les tâches et passer chacun sur sa branche
    -> Giorgi: 
            * [ ] Obtenir les résultats de l'article pour vérifier leur méthode
            * [ ] Ajuster la méthode de calcul pour synthétiser un indicateur de la qualité de vie pour les humains pour appréhender à quel point chaque pays fait des efforts pour rendre son pays plus vivable pour sa population humaine
            * [x] Récupération automatisée des données via un call API
    -> Niels:
            * [ ] Reproduire les résultats du classement des pays en fonction de leur EPI
            * [ ] Faire des graphiques illustratifs
    -> Martin:
            * [ ] Faire l'analyse des données avec la nouvelle méthode synthétisée
            * [ ] Faire une carte du monde avec geopandas, en utilisant un gradient de couleurs pour l'EPI
- [ ] Tout organiser sous la forme d'un notebook Jupyter, compléter le requirements.txt
- [ ] Envoyer le travail complété 

## Méthodologie de travail en équipe (workflow):
Une fois qu'on aura créé nos branches personnelles, nous allons faire des commits sur ces branches, avant de terminer des blocs utiles aux autres. Ces blocs (features, corrections d'erreur etc.) vont être mergés via des "Pull Requests" de Github. Le but est d'éviter de merger sa branche sur la main sans que quelqu'un d'autre ne l'ait vérifié.
[How to make a pull request on Github](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request#creating-the-pull-request)

## Nomenclature des commits
| Commit Message Start    | Meaning                         | Commit Message Body |
|-------------------------|---------------------------------|---------------------|
| fix(directory/to/file): | fixed a bug/mistake             |                     |
| doc(idem):              | updated documentation           | short description   | 
| feat(idem):             | added a new feature             | in a few words      |
| test(idem):             | modified/added/fixed tests      |                     | 
| misc(idem):             | miscellaneous/different changes |                     | 

## Sources utilisées pour ce travail
+ Édition Markdown: https://www.markdownlang.com/
+ Nested Pie Charts with Matplotlib: https://matplotlib.org/stable/gallery/pie_and_polar_charts/nested_pie.html
+ Docu générale de Matplotlib: https://matplotlib.org/stable/
