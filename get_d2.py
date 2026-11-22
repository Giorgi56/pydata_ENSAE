"""First method of data retrieval. Unfortunately, the website doesn't give the necessary permission"""
import os
import requests
import earthaccess
from zipfile import ZipFile

print('\n')


# 1. Login
earthaccess.login()

# 2. Search
results = earthaccess.search_data(
    short_name='CIESIN_SEDAC_EPI_2022',
)

print(results)

# 3. Access
if results != []:
    cwd = os.getcwd()
    files = earthaccess.download(results, f"{cwd}/raw_data/")

    print('\n')
    
    # zip folders:
    # 2022-epi-indicators-time-series-csv.zip
    # 2022-epi-indicators-time-series-na-csv.zip
    # 2022-epi-raw-data-time-series-csv.zip
    # 2022-epi-raw-data-time-series-na-csv.zip
    # 2022-epi-xlsx.zip
    
    # WARNING: in raw_data/ we also have PDF files:
    # 2022-epi-report.pdf
    # 2022-epi-technical-appendix.pdf
    # 2022-epi-policymakers-summary.pdf
    
    # Unzip the zipped folders
    zfiles = ["2022-epi-indicators-time-series-csv.zip",
              "2022-epi-indicators-time-series-na-csv.zip",
              "2022-epi-raw-data-time-series-csv.zip",
              "2022-epi-raw-data-time-series-na-csv.zip",
              "2022-epi-xlsx.zip",
            ]
    for zf in zfiles:
        full_path = f"{cwd}/raw_data/{zf}"
        relative_path = f"raw_data/{zf}"
        with ZipFile(full_path, 'r') as zObject:
            zObject.extractall(path=f"{cwd}/raw_data/")
        zObject.close()
else:
    print("\nresults is empty\n")

# --------------------------------------------------------------------------------------------------------
# Interesting idea: spatial filter for data: quoting the EarthData data download website:
# "Use the spatial filters to limit search results to the specified area of interest.
# 
# To set the spatial area using a polygon, rectangle, point and radius, or circle, select an option from the menu and then draw on the map or manually enter coordinates.
# 
# Upload a shapefile (KML, KMZ, ESRI, etc.) to set the spatial area with a file."
