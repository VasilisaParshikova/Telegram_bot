from telebot.types import Message
from loader import bot
from states.search_request import UserRequestState
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import date, timedelta


@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message):
    bot.set_state(message.from_user.id, UserRequestState.city, message.chat.id)
    bot.send_message(message.chat.id, 'Запускаем поиск самых дешёвых отелей. '
                                      'В каком городе искать отели?')


@bot.message_handler(state=UserRequestState.city)
def get_city(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text
    bot.set_state(message.from_user.id, UserRequestState.date_in, message.chat.id)
    calendar, step = DetailedTelegramCalendar(min_date=date.today()).build()
    bot.send_message(message.chat.id, 'Хорошо. Теперь укажи дату заезда.', reply_markup=calendar)


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
        bot.set_state(message.from_user.id, UserRequestState.date_out, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['duration'] = int(message.text)
            data['date_out'] = data['date_in'] + timedelta(days=data['duration'])
            bot.send_message(message.chat.id, 'Хорошо. '
                                              'Теперь укажи какое количество отелей надо вывести (от 1 до 10).')
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
                                              'Выводить ли фотографии отелей?')
    else:
        bot.send_message(message.chat.id, 'Необходимо указать число от 1 до 10')


@bot.message_handler(state=UserRequestState.hotel_amount)
def get_foto_flag(message: Message):
    if message.text.lower() == 'да':
        bot.set_state(message.from_user.id, UserRequestState.foto_flag, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto_flag'] = True
        bot.send_message(message.chat.id, 'Сколько фото выводить (от 1 до 10)?')
    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, UserRequestState.foto_amount, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto_flag'] = False
            text = f'Вы ищте самые дешёвые отели в городе {data["city"]} на период с {data["date_in"]} ' \
                   f'по {data["date_out"]}.' \
                   f'Надо вывести {data["hotel_amount"]} отелей без фото'
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Надо ответить да или нет')

@bot.message_handler(state=UserRequestState.foto_flag)
def get_foto_amount(message: Message):
    if message.text.isdigit() and 1 <= int(message.text) <= 10:
        bot.set_state(message.from_user.id, UserRequestState.foto_amount, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['foto_amount'] = int(message.text)
            text = f'Вы ищте самые дешёвые отели в городе {data["city"]} на период с {data["date_in"]} ' \
                   f'по {data["date_out"]}.' \
                   f'Надо вывести {data["hotel_amount"]} отелей c {data["foto_amount"]} фото'
            bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, 'Необходимо указать число от 1 до 10')

