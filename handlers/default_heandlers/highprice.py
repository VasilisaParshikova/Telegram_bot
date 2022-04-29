from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['highprice'])
def bot_highprice(message: Message):
    bot.send_message(message.chat.id, 'Запускаем поиск самых дорогих отелей.'
                                      'В каком городе искать отели?')