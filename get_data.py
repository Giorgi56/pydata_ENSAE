"""First method of data retrieval. Unfortunately, the website doesn't give the necessary permission"""
import os
import requests
url = ("https://data.earthdata.nasa.gov/nasa-earth/human-dimensions/"
        "sedac-root/downloads/data/epi/epi-environmental-performance"
       "-index-2022/2022-epi-raw-data-time-series-na-csv.zip"
       )
query_parameters = {"downloadformat": "csv"}

print('\n')

# response = requests.get(url)

# print HTTP status code

# handle the response data
# unzip in the ./raw_data folder

print('\n')
     
# log in
user_name, user_pass = os.environ["USER_NAME"], os.environ["USER_PASS"]

basic = requests.auth.HTTPBasicAuth(user_name, user_pass)
response = requests.get(url, auth=basic, params=query_parameters)
     

print(f"Status Code: {response.status_code}")

print('\n')

with open("random_ass_file", mode="wb") as file:
    file.write(response.content)

