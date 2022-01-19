import os

import requests
import json
url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query":"екатеринбург"}

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPID_API_KEY", "")
    }

response = requests.request("GET", url, headers=headers, params=querystring)

sity_dict = json.loads(response.text)
sity_id = sity_dict['suggestions'][0]['entities'][0]['destinationId']


url = "https://hotels4.p.rapidapi.com/properties/list"

querystring = {"destinationId":sity_id,"pageNumber":"1","pageSize":"5","checkIn":"2020-01-08","checkOut":"2020-01-15","adults1":"1","sortOrder":"PRICE_HIGHEST_FIRST"}

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': "fcdef2e919mshede91a9f6719bc0p14536bjsn26e25f9238d5"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
