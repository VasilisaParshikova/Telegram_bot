from telebot.types import Message
from loader import bot
from states.search_request import UserRequestState


@bot.message_handler(commands=['highprice'])
def bot_highprice(message: Message):
    bot.set_state(message.from_user.id, UserRequestState.city, message.chat.id)
    bot.send_message(message.chat.id, 'Запускаем поиск самых дорогих отелей. '
                                      'В каком городе искать отели?')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'highprice'