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
