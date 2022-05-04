from telebot.types import Message
from loader import bot
from states.search_request import UserRequestState



@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message):
    bot.set_state(message.from_user.id, UserRequestState.city, message.chat.id)
    bot.send_message(message.chat.id, 'Запускаем поиск самых дешёвых отелей. '
                                      'В каком городе искать отели?')
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command'] = 'lowprice'




