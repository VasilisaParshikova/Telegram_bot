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

    def sity_request(self, sity: str):
        url = "https://hotels4.p.rapidapi.com/locations/v2/search"
        querystring = {"query": sity}
        response = requests.request("GET", url, headers=self.__headers, params=querystring)
        sity_dict = json.loads(response.text)
        if len(sity_dict['suggestions'][0]['entities']) == 0:
            return False
        else:
            sity_id = sity_dict['suggestions'][0]['entities'][0]['destinationId']
            return sity_id

    def get_results(self, sity_id: int, hotel_amount: int, req_type: int):
        url = "https://hotels4.p.rapidapi.com/properties/list"
        req_types = {0: "PRICE"}

        querystring = {"destinationId": sity_id , "pageNumber": "1", "pageSize": hotel_amount,
                       "checkIn": "2020-06-02",
                       "checkOut": "2020-06-03", "adults1": "1", "sortOrder": req_types[req_type]}
        response = requests.request("GET", url, headers=self.__headers, params=querystring)
        hotels_dict = json.loads(response.text)
        hotels_dict = hotels_dict['data']['body']['searchResults']['results']
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
        answer = []

        for hotel in results:
            answer.append('Отель {} {} звезды.\nАдрес:{}.\nЦена {}\n'.format(
                hotel['name'], hotel['starRating'], hotel['address'], hotel['price']
            ))
        answer = ''.join(answer)
        return answer
