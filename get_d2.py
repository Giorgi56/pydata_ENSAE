"""First method of data retrieval. Unfortunately, the website doesn't give the necessary permission"""
import os
import requests
import earthaccess

print('\n')


# 1. Login
earthaccess.login()

# 2. Search
results = earthaccess.search_data(
    short_name='CIESIN_SEDAC_EPI_2022',
    # concept_id='C3540911446-ESDIS',
    # , S, , N
    #bounding_box=(180, -55, -180, 90), 
    #temporal=("1950-01-01T00:00:00.000Z", "2022-12-31T00:00:00.000Z"),  # ...and time period of interest.
    #entry_title="2022-epi-raw-data-time-series-na-csv.zip",
    #count=10
)

print(results)

# 3. Access
if results != []: # /home/giorgi/Documents/py_datasci/pydata_ENSAE
    files = earthaccess.download(results, "/home/giorgi/Documents/")
else:
    print("\nresults is empty\n")

print('\n')

# --------------------------------------------------------------------------------------------------------
# Interesting idea: spatial filter for data: quoting the EarthData data download website:
# "Use the spatial filters to limit search results to the specified area of interest.
# 
# To set the spatial area using a polygon, rectangle, point and radius, or circle, select an option from the menu and then draw on the map or manually enter coordinates.
# 
# Upload a shapefile (KML, KMZ, ESRI, etc.) to set the spatial area with a file."
