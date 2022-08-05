import os
import requests
import json
from config_data import config


class ApiSgltn:
    __instance = None
    __basic_url = "https://hotels4.p.rapidapi.com/"
    __city_url = "locations/v2/search"
    __hotels_lst_url = "properties/list"
    __photo_url = "properties/get-hotel-photos"

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(ApiSgltn, cls).__new__(cls)
            cls.__instance.__headers = {
                'x-rapidapi-host': "hotels4.p.rapidapi.com",
                'x-rapidapi-key': config.RAPID_API_KEY
            }
        return ApiSgltn.__instance

    def request_func(self, url, querystring):
        try:
            response = requests.request("GET", ''.join([self.__basic_url, url]), headers=self.__headers,
                                        params=querystring, timeout=10)
            if response.status_code == requests.codes.ok:
                result = json.loads(response.text)
            else:
                result = False
            return result
        except Exception:
            return False

    def city_request(self, city: str):
        querystring = {"query": city,
                       "locale": "ru_RU"}
        city_dict = self.request_func(self.__city_url, querystring)
        if city_dict and len(city_dict['suggestions'][0]['entities']) == 0:
            return False
        else:
            city_id = city_dict['suggestions'][0]['entities'][0]['destinationId']
            return city_id

    def get_results(self, city_id: int, hotel_amount: int, req_type: str, date_in: str, date_out: str):
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

        hotels_dict = self.request_func(self.__hotels_lst_url, querystring)
        if not hotels_dict:
            return False
        else:
            hotels_dict = hotels_dict['data']['body']['searchResults']['results']
            return hotels_dict

    def get_results_bestdeal(self, city_id: int, hotel_amount: int,
                             date_in: str, date_out: str, max_price: int):

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
        hotels_dict = self.request_func(self.__hotels_lst_url, querystring)
        if not hotels_dict:
            return False
        else:
            hotels_dict = hotels_dict['data']['body']['searchResults']['results']
            return hotels_dict

    def get_photo(self, hotel_id: int):
        querystring = {"id": hotel_id}
        data = self.request_func(self.__photo_url, querystring)
        if not data:
            return False
        else:
            return data['hotelImages']
