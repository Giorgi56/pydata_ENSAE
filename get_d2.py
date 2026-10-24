"""First method of data retrieval. Unfortunately, the website doesn't give the necessary permission"""
import os
import requests
import earthaccess

print('\n')


# 1. Login
earthaccess.login()

# 2. Search
results = earthaccess.search_data(
    short_name='',
    bounding_box=(-180, 180, 90, -55),  # Only include files in area of interest...
    temporal=("1950-01-01T00:00:00.000Z", "2022-12-31T00:00:00.000Z"),  # ...and time period of interest.
    entry_title="2022-epi-raw-data-time-series-na-csv.zip",
    count=10
)

# 3. Access
files = earthaccess.download(results, "/home/giorgi/Documents/py_datasci/pydata_ENSAE")

print('\n')

