import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()


class ApiSgltn:
    __instance = None

    def __init__(self):
        if not ApiSgltn.__instance:
            self.__headers = {
                'x-rapidapi-host': "hotels4.p.rapidapi.com",
                'x-rapidapi-key': os.getenv("RAPID_API_KEY", "")
            }
        else:
            return ApiSgltn.__instance

    def city_request(self, city: str):
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": city,
                       "locale": "ru_RU"}
        response = requests.request("GET", url, headers=self.__headers, params=querystring)
        city_dict = json.loads(response.text)
        if len(city_dict['suggestions'][0]['entities']) == 0:
            return False
        else:
            city_id = city_dict['suggestions'][0]['entities'][0]['destinationId']
            return city_id

    def get_results(self, city_id: int, hotel_amount: int, req_type: str, date_in: str, date_out: str):
        url = "https://hotels4.p.rapidapi.com/properties/list"
        req_types = {'lowprice': "PRICE",
                     'highprice': "PRICE_HIGHEST_FIRST"}

        querystring = {"destinationId": city_id,
                       "pageNumber": "1",
                       "pageSize": hotel_amount,
                       "checkIn": date_in,
                       "checkOut": date_out,
                       "adults1": "1",
                       "sortOrder": req_types[req_type],
                       "locale": "ru_RU",
                       "currency": "RUB"}
        print(querystring)
        response = requests.request("GET", url, headers=self.__headers, params=querystring)
        hotels_dict = json.loads(response.text)
        print(hotels_dict)
        hotels_dict = hotels_dict['data']['body']['searchResults']['results']

        return hotels_dict

    def get_results_bestdeal(self, city_id: int, hotel_amount: int,
                             date_in: str, date_out: str, distance: int, max_price: int):
        url = "https://hotels4.p.rapidapi.com/properties/list"

        querystring = {"destinationId": city_id,
                       "pageNumber": "1",
                       "pageSize": hotel_amount,
                       "checkIn": date_in,
                       "checkOut": date_out,
                       "adults1": "1",
                       "priceMin": "1",
                       "priceMax": max_price,
                       "sortOrder": "DISTANCE_FROM_LANDMARK",
                       "locale": "ru_RU",
                       "currency": "RUB",
                       "landmarkIds": "City center"}
        print(querystring)
        response = requests.request("GET", url, headers=self.__headers, params=querystring)
        hotels_dict = json.loads(response.text)
        print(hotels_dict)
        hotels_dict = hotels_dict['data']['body']['searchResults']['results']

        return hotels_dict

    def get_photo(self, hotel_id: int):
        url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
        querystring = {"id": hotel_id}
        response = requests.request("GET", url, headers=self.__headers, params=querystring)
        data = json.loads(response.text)
        return data['hotelImages']
