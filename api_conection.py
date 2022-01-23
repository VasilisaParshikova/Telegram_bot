import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
url = "https://hotels4.p.rapidapi.com/locations/v2/search"

querystring = {"query": "екатеринбург"}

headers = {
    'x-rapidapi-host': "hotels4.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPID_API_KEY", "")
    }

response = requests.request("GET", url, headers=headers, params=querystring)

sity_dict = json.loads(response.text)
print(sity_dict)
sity_id = sity_dict['suggestions'][0]['entities'][0]['destinationId']
hotel_amount = 5

url = "https://hotels4.p.rapidapi.com/properties/list"

querystring = {"destinationId": sity_id, "pageNumber": "1", "pageSize": str(hotel_amount), "checkIn": "2020-02-02", "checkOut": "2020-02-15", "adults1": "1", "sortOrder": "PRICE"}
response = requests.request("GET", url, headers=headers, params=querystring)
hotels_dict = json.loads(response.text)
hotels_dict = hotels_dict['data']['body']['searchResults']['results']
print(hotels_dict)
print(hotels_dict[0]['guestReviews']['rating'])
results = []
hotel_id_in_res = 0
for hotel_info in hotels_dict:
    results.append(dict())
    results[hotel_id_in_res]['name'] = hotel_info['name']
    results[hotel_id_in_res]['starRating'] = hotel_info['starRating']
    results[hotel_id_in_res]['address'] = hotel_info['address']['streetAddress']
#    results[hotel_id_in_res]['guestRating'] = hotel_info['guestReviews']['rating']
    results[hotel_id_in_res]['price'] = hotel_info['ratePlan']['price']['current']
    hotel_id_in_res += 1
for hotel in results:
    print(hotel)