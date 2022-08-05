from telebot.types import Message
from states.search_request import UserRequestState
from loader import bot
from keyboards.reply.amount_request import amount_request


@bot.message_handler(commands=['beastdeal'])
def bot_bestdeal(message: Message):
    bot.set_state(message.from_user.id, UserRequestState.city, message.chat.id)
    bot.send_message(message.chat.id, 'Запускаем поиск отелей в центре города. '
                                      'В каком городе искать отели?')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'beastdeal'


@bot.message_handler(state=UserRequestState.distance_from_center)
def get_distance(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, UserRequestState.price_per_night_max, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance_from_center'] = int(message.text)
            bot.send_message(message.chat.id, 'Хорошо. Какая максимальная стоимость отеля за ночь? '
                                              'Указывать в рублях.')
    else:
        bot.send_message(message.chat.id,
                         'Расстояние от центра должно быть указана числом (километры)')


@bot.message_handler(state=UserRequestState.price_per_night_max)
def get_max_price(message: Message):
    if message.text.isdigit() and int(message.text) > 0:
        bot.set_state(message.from_user.id, UserRequestState.date_out, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_price_per_night'] = int(message.text)
            bot.send_message(message.chat.id, 'Хорошо. Теперь укажи какое количество отелей '
                                              'надо вывести (от 1 до 10).',
                             reply_markup=amount_request())
    else:
        bot.send_message(message.chat.id,
                         'Стоимость отеля должна быть указана числом (рублей за ночь)')
