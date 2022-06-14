from telebot.types import Message
from loader import bot
from states.search_request import UserRequestState
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta
from repid_api.api_singleton import ApiSgltn
from keyboards.reply.yes_no import yes_no_reply
from keyboards.reply.amount_request import amount_request

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
        bot.send_message(c.message.chat.id, 'Хорошо. Теперь укажи количество дней проживания.')


@bot.message_handler(state=UserRequestState.date_in)
def get_date_out(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['duration'] = int(message.text)
            data['date_out'] = data['date_in'] + timedelta(days=data['duration'])
            if data['command'] == 'beastdeal':
                bot.set_state(message.from_user.id, UserRequestState.distance_from_center, message.chat.id)
                bot.send_message(message.chat.id, 'Хорошо. Теперь укажи максимальную удалённость отеля от центра '
                                                  'города в колиметрах.')
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
                                              'Выводить ли фотографии отелей?', reply_markup=yes_no_reply())
    else:
        bot.send_message(message.chat.id, 'Необходимо указать число от 1 до 10')


@bot.message_handler(state=UserRequestState.hotel_amount)
def get_foto_flag(message: Message):
    if message.text.lower() == 'да':
        bot.set_state(message.from_user.id, UserRequestState.foto_flag, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto_flag'] = True
        bot.send_message(message.chat.id, 'Сколько фото выводить (от 1 до 10)?',
                         reply_markup=amount_request())
    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, UserRequestState.foto_amount, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto_flag'] = False
            if data['command'] in commands:
                result = ApiSgltn().get_results(data['city_id'],
                                                data['hotel_amount'],
                                                data['command'],
                                                str(data['date_in']),
                                                str(data['date_out']), )
            else:
                result = ApiSgltn().get_results_bestdeal(data['city_id'],
                                                         data['hotel_amount'],
                                                         str(data['date_in']),
                                                         str(data['date_out']),
                                                         data['distance_from_center'],
                                                         data['max_price_per_night'])

            if result:
                bot.send_message(message.chat.id, result)
            else:
                bot.send_message(message.chat.id, f'В городе {data["city"]} на период с {data["date_in"]} '
                                                  f'по {data["date_out"]} не было найдено отелей.')
    else:
        bot.send_message(message.chat.id, 'Надо ответить да или нет')


@bot.message_handler(state=UserRequestState.foto_flag)
def get_foto_amount(message: Message):
    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        bot.set_state(message.from_user.id, UserRequestState.foto_amount, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto_amount'] = int(message.text)
            if data['command'] in commands:
                result = ApiSgltn().get_results(data['city_id'],
                                                data['hotel_amount'],
                                                data['command'],
                                                str(data['date_in']),
                                                str(data['date_out']), )
            else:
                result = ApiSgltn().get_results_bestdeal(data['city_id'],
                                                         data['hotel_amount'],
                                                         str(data['date_in']),
                                                         str(data['date_out']),
                                                         data['distance_from_center'],
                                                         data['max_price_per_night'])
            if result:
                bot.send_message(message.chat.id, result)
            else:
                bot.send_message(message.chat.id, f'В городе {data["city"]} на период с {data["date_in"]} '
                                                  f'по {data["date_out"]} не было найдено отелей.')
    else:
        bot.send_message(message.chat.id, 'Необходимо указать число от 1 до 10')
