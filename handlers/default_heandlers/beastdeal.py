from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['beastdeal'])
def bot_bestdeal(message: Message):
    bot.send_message(message.chat.id, 'Запускаем поиск отелей в центре города.'
                                      'В каком городе искать отели?')