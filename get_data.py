"""This file gets the data from EarthDATA via an API call"""
import os
import requests

print('\n')

# API endpoint url

url = "https://search.earthdata.nasa.gov/search/granules?p=C3540911446-ESDIS&pg[0][v]=f&pg[0][gsk]=-start_date&g=G3550122302-ESDIS&lat=17.5&long=71.04477611940297&zoom=1.3780331967725128"

# send get request to endpoint
response = requests.get(url)

# print HTTP status code
print(f"Status Code: {response.status_code}")

# handle the response data
match response.status_code:
    case 200:
        print('\n')
        
        # log in
        user_name, user_pass = os.environ["USER_NAME"], os.environ["USER_PASS"]

        basic = requests.auth.HTTPBasicAuth(user_name, user_pass)
        requests.get(url, auth=basic)
        
        # Download the zip file
        url = "https://data.earthdata.nasa.gov/nasa-earth/human-dimensions/sedac-root/downloads/data/epi/epi-environmental-performance-index-2022/2022-epi-raw-data-time-series-na-csv.zip"
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        # unzip in the ./raw_data folder


print('\n')

# url = "https://search.earthdata.nasa.gov/search/granules?p=C3540911446-ESDIS&pg[0][v]=f&pg[0][gsk]=-start_date&g=G3550122302-ESDIS&lat=17.5&long=71.04477611940297&zoom=1.3780331967725128"
