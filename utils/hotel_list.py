from repid_api.api_singleton import ApiSgltn


def hotel_list(data: list, duration: int):
    results = []
    hotel_id_in_res = 0
    for hotel_info in data:
        results.append(dict())
        results[hotel_id_in_res]['id'] = hotel_info['id']
        results[hotel_id_in_res]['name'] = hotel_info['name']
        results[hotel_id_in_res]['starRating'] = hotel_info['starRating']
        if 'streetAddress' in hotel_info['address']:
            results[hotel_id_in_res]['address'] = hotel_info['address']['streetAddress']
        else:
            results[hotel_id_in_res]['address'] = ' '
        results[hotel_id_in_res]['price'] = hotel_info['ratePlan']['price']['current']
        hotel_id_in_res += 1
    if hotel_id_in_res == 0:
        return False
    else:
        answer = []
        for hotel in results:
            answer.append('Отель {} {} звезды.\nАдрес:{}.\nЦена за ночь {}\nПолная стоимость {}'
                          '\nСсылка: https://www.hotels.com/ho{}\n'.format(
                          hotel['name'], hotel['starRating'], hotel['address'], hotel['price'],
                          int(hotel['price'][:-4].replace(',', '')) * duration, hotel['id']
            ))
        answer = ''.join(answer)
        return results, answer


def hotel_list_bestdeal(data: list, distance: int, hotel_amount: int, duration: int):
    results = []
    hotel_id_in_res = 0
    for hotel_info in data:
        for landmark in hotel_info['landmarks']:
            if landmark['label'] == 'Центр города' and float(landmark['distance'][:-3].replace(',', '.')) < distance:
                results.append(dict())
                results[hotel_id_in_res]['distance_from_center'] = landmark['distance']
                results[hotel_id_in_res]['id'] = hotel_info['id']
                results[hotel_id_in_res]['name'] = hotel_info['name']
                results[hotel_id_in_res]['starRating'] = hotel_info['starRating']
                if 'streetAddress' in hotel_info['address']:
                    results[hotel_id_in_res]['address'] = hotel_info['address']['streetAddress']
                else:
                    results[hotel_id_in_res]['address'] = ' '

                if 'ratePlan' in hotel_info:
                    results[hotel_id_in_res]['price'] = hotel_info['ratePlan']['price']['current']
                else:
                    results[hotel_id_in_res]['price'] = 'не указана'
                hotel_id_in_res += 1
                break
        if hotel_id_in_res == hotel_amount:
            break
    if hotel_id_in_res == 0:
        return False
    else:
        answer = []
        for hotel in results:
            answer.append('Отель {} {} звезд(ы).\nАдрес:{}.\nРастоянее от центра: {}'
                          '\nЦена за ночь {} \nПолная стоимость {}'
                          '\nСсылка: https://www.hotels.com/ho{}\n'.format(
                hotel['name'],
                hotel['starRating'],
                hotel['address'],
                hotel['distance_from_center'],
                hotel['price'],
                int(hotel['price'][:-4].replace(',', '')) * duration,
                hotel['id']
            ))
        answer = ''.join(answer)
        return results, answer


def add_photo(hotel_lst: list):
    for hotel in hotel_lst:
        photo_urls_lst = ApiSgltn().get_photo(hotel['id'])
        photo_urls = []
        count = 0
        if photo_urls_lst:
            for photo in photo_urls_lst:
                photo_url = photo['baseUrl'].replace('{size}', photo['sizes'][0]['suffix'])
                photo_urls.append(photo_url)
                count += 1
                if count == 10:
                    break
        hotel['photos'] = photo_urls
    return hotel_lst
