from telebot.types import Message
from telebot import types
from loader import bot
from states.search_request import UserRequestState
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta
from repid_api.api_singleton import ApiSgltn
from keyboards.reply.photo_reply import photo_reply
from keyboards.reply.amount_request import amount_request
from utils.hotel_list import hotel_list, hotel_list_bestdeal, add_photo

commands = [
    'lowprice',
    'highprice']


@bot.message_handler(state=UserRequestState.city)
def get_city(message: Message):
    city_id = ApiSgltn().city_request(message.text)
    if city_id:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
            data['city_id'] = int(city_id)
        bot.set_state(message.from_user.id, UserRequestState.date_in, message.chat.id)
        calendar, step = DetailedTelegramCalendar(min_date=date.today()).build()
        bot.send_message(message.chat.id, 'Хорошо. Теперь укажи дату заезда.', reply_markup=calendar)
    else:
        bot.send_message(message.chat.id, 'Название города указано не верно или '
                                          'такого города нет в базе сайта hotels.com. '
                                          'Попробуйте снова проверив написание города или выбрав другой.')


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal_date_in(c):
    result, key, step = DetailedTelegramCalendar(min_date=date.today()).process(c.data)
    if not result and key:
        bot.edit_message_text('Хорошо. Теперь укажи дату заезда.',
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Дата заезда: {result}",
                              c.message.chat.id,
                              c.message.message_id)
        with bot.retrieve_data(c.from_user.id, c.message.chat.id) as data:
            data['date_in'] = result
        bot.send_message(c.message.chat.id, 'Хорошо. Теперь укажи количество дней проживания.',
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(state=UserRequestState.date_in)
def get_date_out(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['duration'] = int(message.text)
            data['date_out'] = data['date_in'] + timedelta(days=data['duration'])
            if data['command'] == 'beastdeal':
                bot.set_state(message.from_user.id, UserRequestState.distance_from_center, message.chat.id)
                bot.send_message(message.chat.id, 'Хорошо. Теперь укажи максимальную удалённость отеля от центра '
                                                  'города в колиметрах.', reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.set_state(message.from_user.id, UserRequestState.date_out, message.chat.id)
                bot.send_message(message.chat.id, 'Хорошо. '
                                                  'Теперь укажи какое количество отелей надо вывести (от 1 до 10).',
                                 reply_markup=amount_request())
    else:
        bot.send_message(message.chat.id,
                         'Длительность проживания должна быть указана числом (количество дней)')


@bot.message_handler(state=UserRequestState.date_out)
def get_hotel_amount(message: Message):
    if message.text.isdigit():
        if 1 <= int(message.text) <= 10:
            bot.set_state(message.from_user.id, UserRequestState.hotel_amount, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotel_amount'] = int(message.text)
            bot.send_message(message.chat.id, 'Хорошо. '
                                              'Выберите формат вывода поиска:'
                                              '\nСписком - краткая информация о всех отелях одним текстовым сообщением'
                                              '\nС фото - для каждого отедя будет отправлено сообщение с '
                                              'фотографиями и кратким описанием', reply_markup=photo_reply())
    else:
        bot.send_message(message.chat.id, 'Необходимо указать число от 1 до 10')


@bot.message_handler(state=UserRequestState.hotel_amount)
def get_photo_flag(message: Message):
    correct_input = False
    photo_flag = False
    result_list = False
    if message.text.lower() == 'списком':
        bot.set_state(message.from_user.id, UserRequestState.photo_flag, message.chat.id)
        correct_input = True
    elif message.text.lower() in ['с фото', 'фото']:
        bot.set_state(message.from_user.id, UserRequestState.photo_flag, message.chat.id)
        correct_input = True
        photo_flag = True
    else:
        bot.send_message(message.chat.id, 'Необходимо выбрать один из вариантов: "список" или "с фото". '
                                          'Для удобства ввода воспользуйтесь специальной клавиатурой'
                                          ' внизу экрана')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if correct_input and data['command'] in commands:
            result = ApiSgltn().get_results(data['city_id'],
                                            data['hotel_amount'],
                                            data['command'],
                                            str(data['date_in']),
                                            str(data['date_out']), )
            if result:
                result_list = hotel_list(result)
            if result_list:
                data['result_dict'] = result_list
                answer = []
                for hotel in result_list:
                    answer.append('Отель {} {} звезды.\nАдрес:{}.\nЦена за ночь {}\n'.format(
                        hotel['name'], hotel['starRating'], hotel['address'], hotel['price']
                    ))
                answer = ''.join(answer)
                data['result_text'] = answer
            else:
                bot.send_message(message.chat.id, f'В городе {data["city"]} на период с {data["date_in"]} '
                                                  f'по {data["date_out"]} не было найдено отелей.',
                                 reply_markup=types.ReplyKeyboardRemove())

        if correct_input and data['command'] not in commands:
            result = ApiSgltn().get_results_bestdeal(data['city_id'],
                                                     data['hotel_amount'],
                                                     str(data['date_in']),
                                                     str(data['date_out']),
                                                     data['max_price_per_night'])
            if result:
                result_list = hotel_list_bestdeal(result, data['distance_from_center'], data['hotel_amount'])
            if result_list:
                data['result_dict'] = result_list
                answer = []
                for hotel in result_list:
                    answer.append('Отель {} {} звезды.\nАдрес:{}.\nРастоянее от центра: {}'
                                  '\nЦена за ночь {}\n'.format(
                        hotel['name'], hotel['starRating'],
                        hotel['address'],
                        hotel['distance_from_center'],
                        hotel['price']
                    ))
                answer = ''.join(answer)
                data['result_text'] = answer
            else:
                bot.send_message(message.chat.id, f'В городе {data["city"]} на период с {data["date_in"]} '
                                                  f'по {data["date_out"]} не было найдено отелей по '
                                                  f'указанным параметрам.',
                                 reply_markup=types.ReplyKeyboardRemove())

        if correct_input and photo_flag and result_list:
            data['result_dict'] = add_photo(data['result_dict'])
            if data['command'] not in commands:
                for hotel in data['result_dict']:
                    hotel_text = 'Отель {} {} звезды.\nАдрес:{}.\nРастоянее от центра: {}' \
                                 '\nЦена за ночь {}\n'.format(
                                                                  hotel['name'], hotel['starRating'],
                                                                  hotel['address'],
                                                                  hotel['distance_from_center'],
                                                                  hotel['price']
                                                                  )
                    if len(hotel['photos']) > 0:
                        media = []
                        media.append(types.InputMediaPhoto(media=hotel['photos'][0], caption=hotel_text))
                        for i in range(1, len(hotel['photos'])):
                            media.append(types.InputMediaPhoto(media=hotel['photos'][i]))
                        bot.send_media_group(chat_id=message.chat.id, media=media)
                    else:
                        bot.send_message(message.chat.id, '\n'.join([hotel_text,
                                                                     '*у данного отеля нет фотографий']))
            else:
                for hotel in data['result_dict']:
                    hotel_text = 'Отель {} {} звезды.\nАдрес:{}.\nЦена за ночь {}\n'.format(
                            hotel['name'], hotel['starRating'], hotel['address'], hotel['price'])
                    if len(hotel['photos']) > 0:
                        media = []
                        media.append(types.InputMediaPhoto(media=hotel['photos'][0], caption=hotel_text))
                        for i in range(1, len(hotel['photos'])):
                            media.append(types.InputMediaPhoto(media=hotel['photos'][i]))
                        bot.send_media_group(chat_id=message.chat.id, media=media)
                    else:
                        bot.send_message(message.chat.id, '\n'.join([hotel_text,
                                                                     '*у данного отеля нет фотографий']))
            bot.send_message(message.chat.id, 'Окончание результатов поиска',
                                 reply_markup=types.ReplyKeyboardRemove())

        if correct_input and not photo_flag and result_list:
            bot.send_message(message.chat.id, answer, reply_markup=types.ReplyKeyboardRemove())
